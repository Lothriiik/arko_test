import pandas as pd
import csv
import io
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from core.models import Empresa
from django.conf import settings

class Command(BaseCommand):
    help = 'Importa dados de empresas de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        
        colunas = [
            'cnpj_basico',
            'razao_social',
            'natureza_juridica',
            'qualificacao_responsavel',
            'capital_social',
            'porte_da_empresa',
            'ente_federativo_responsavel',
        ]
        
        registros_processados = 0
        try:
            self.stdout.write(self.style.NOTICE('Lendo o arquivo CSV...'))
            df = pd.read_csv(csv_file_path, sep=';', encoding='latin1', header=None, names=colunas, usecols=range(7))

            df['capital_social'] = df['capital_social'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            df['capital_social'] = pd.to_numeric(df['capital_social'], errors='coerce').fillna(0)

            df['qualificacao_responsavel'] = df['qualificacao_responsavel'].astype(str).str.slice(0, 2)
            df['porte_da_empresa'] = pd.to_numeric(df['porte_da_empresa'], errors='coerce').fillna(0).astype(int).astype(str)
            df['natureza_juridica'] = df['natureza_juridica'].astype(str).str.slice(0, 5)

            temp_table_name = 'temp_empresas_import'

            self.stdout.write(self.style.NOTICE('Carregando dados'))

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(f'DROP TABLE IF EXISTS "{temp_table_name}";')
                    cursor.execute(f"""
                        CREATE TABLE "{temp_table_name}" (
                            cnpj_basico VARCHAR(8),
                            razao_social VARCHAR(255),
                            natureza_juridica VARCHAR(5),
                            qualificacao_responsavel VARCHAR(2),
                            capital_social NUMERIC(20, 2),
                            porte_da_empresa VARCHAR(2),
                            ente_federativo_responsavel VARCHAR(255)
                        );
                    """)

                chunk_size = 50000

                for i in range(0, len(df), chunk_size):
                    chunk_df = df.iloc[i:i + chunk_size]
                    
                    with connection.cursor() as cursor:
                        string_io = io.StringIO()
                        chunk_df.to_csv(
                            string_io,
                            sep='\t',
                            header=False,
                            index=False,
                            quoting=csv.QUOTE_NONE,
                            escapechar='\\'
                        )
                        string_io.seek(0)
                        cursor.copy_from(string_io, temp_table_name, sep='\t', columns=colunas)

                    self.stdout.write(self.style.NOTICE(f'Lote {i // chunk_size + 1} de {len(df) // chunk_size + 1} carregado.'))

                registros_processados = len(df)

                self.stdout.write(self.style.NOTICE('Executando a transformação e mesclagem de dados...'))

                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        INSERT INTO core_empresa (
                            cnpj_basico,
                            razao_social,
                            natureza_juridica,
                            qualificacao_responsavel,
                            capital_social,
                            porte_da_empresa,
                            ente_federativo_responsavel
                        )
                        SELECT
                            cnpj_basico,
                            razao_social,
                            natureza_juridica,
                            qualificacao_responsavel,
                            capital_social,
                            porte_da_empresa,
                            ente_federativo_responsavel
                        FROM
                            "{temp_table_name}"
                        ON CONFLICT (cnpj_basico) DO UPDATE SET
                            razao_social = EXCLUDED.razao_social,
                            natureza_juridica = EXCLUDED.natureza_juridica,
                            qualificacao_responsavel = EXCLUDED.qualificacao_responsavel,
                            capital_social = EXCLUDED.capital_social,
                            porte_da_empresa = EXCLUDED.porte_da_empresa,
                            ente_federativo_responsavel = EXCLUDED.ente_federativo_responsavel;
                    """)

                    cursor.execute(f'DROP TABLE "{temp_table_name}";')

            self.stdout.write(self.style.SUCCESS('---'))
            self.stdout.write(self.style.SUCCESS(f'Processo concluído com sucesso!'))
            self.stdout.write(self.style.SUCCESS(f'Total de registros processados: {registros_processados}'))
            self.stdout.write(self.style.SUCCESS('---'))

        except FileNotFoundError:
            raise CommandError(f'O arquivo CSV não foi encontrado no caminho: {csv_file_path}')
        except Exception as e:
            raise CommandError(f'Ocorreu um erro grave durante a importação: {e}')
