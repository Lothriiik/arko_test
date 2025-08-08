from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_empresacount'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS idx_cnpj_basico_prefix
                ON core_empresa (cnpj_basico varchar_pattern_ops);
                
                CREATE INDEX IF NOT EXISTS idx_porte_da_empresa_prefix
                ON core_empresa (porte_da_empresa varchar_pattern_ops);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS idx_cnpj_basico_prefix;
                DROP INDEX IF EXISTS idx_porte_da_empresa_prefix;
            """,
        ),
    ]
