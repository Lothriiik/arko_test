from django.db import models

class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Distrito(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Empresa(models.Model):
 
    cnpj_basico = models.CharField(max_length=8, unique=True)
    razao_social = models.CharField(max_length=255)
    natureza_juridica = models.CharField(max_length=5)
    qualificacao_responsavel = models.CharField(max_length=2)
    capital_social = models.DecimalField(max_digits=20, decimal_places=2) 
    porte_da_empresa = models.CharField(max_length=2)
    ente_federativo_responsavel = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj_basico})"
    
class EmpresaCount(models.Model):
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Total Empresas: {self.total}"