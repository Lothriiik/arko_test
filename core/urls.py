# core/urls.py
from django.urls import path
from .views import home, empresas, distritos, estados, municipios

urlpatterns = [
    path('', distritos, name='distritos'),
    path('empresas', empresas, name='empresas'),
    path('distritos', distritos, name='distritos'),
    path('estados', estados, name='estados'),
    path('municipios', municipios, name='municipios'),
    
]
