import requests
from django.core.management.base import BaseCommand
from core.models import Estado, Municipio, Distrito


class Command(BaseCommand):
    help = 'Importa estados, municípios e distritos do IBGE'

    def handle(self, *args, **options):
        self.importar_estados()
        self.importar_municipios()
        self.importar_distritos()
        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))

    def importar_estados(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        response = requests.get(url)
        estados = response.json()

        for estado in estados:
            Estado.objects.update_or_create(
                id=estado["id"],
                defaults={
                    "nome": estado["nome"],
                    "sigla": estado["sigla"]
                }
            )

    def importar_municipios(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response = requests.get(url)
        municipios = response.json()

        for municipio in municipios:
            uf_data = municipio["regiao-imediata"]["regiao-intermediaria"]["UF"]
            estado_id = uf_data["id"]

            try:
                estado = Estado.objects.get(id=estado_id)
            except Estado.DoesNotExist:
                continue

            Municipio.objects.update_or_create(
                id=municipio["id"],
                defaults={
                    "nome": municipio["nome"],
                    "estado": estado
                }
            )

    def importar_distritos(self):
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"
        response = requests.get(url)
        distritos = response.json()

        for distrito in distritos:
            municipio_id = distrito["municipio"]["id"]

            try:
                municipio = Municipio.objects.get(id=municipio_id)
            except Municipio.DoesNotExist:
                continue

            Distrito.objects.update_or_create(
                id=distrito["id"],
                defaults={
                    "nome": distrito["nome"],
                    "municipio": municipio
                }
            )
