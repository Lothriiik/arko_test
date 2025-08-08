from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Empresa, EmpresaCount

def atualizar_contagem_empresas():
    total = Empresa.objects.count()
    obj, created = EmpresaCount.objects.get_or_create(id=1)
    obj.total = total
    obj.save()

@receiver(post_save, sender=Empresa)
def empresa_salva(sender, instance, **kwargs):
    atualizar_contagem_empresas()

@receiver(post_delete, sender=Empresa)
def empresa_deletada(sender, instance, **kwargs):
    atualizar_contagem_empresas()
