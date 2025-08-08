from django.shortcuts import render
from django.core.cache import cache
from django.core.paginator import Paginator
from .models import Estado, Distrito, Municipio, Empresa, EmpresaCount

def home(request):
    return render(request, 'base.html')

def estados(request):
    nome = request.GET.get('nome', '').strip()
    sigla = request.GET.get('sigla', '').strip()

    lista_estados = Estado.objects.all()

    if nome:
        lista_estados = lista_estados.filter(nome__istartswith=nome)
    if sigla:
        lista_estados = lista_estados.filter(sigla__istartswith=sigla)

    lista_estados = lista_estados.order_by('nome')
    paginator = Paginator(lista_estados, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'estados.html', {'page_obj': page_obj, 'nome': nome, 'sigla': sigla})


def distritos(request):
    filtro_nome = request.GET.get('nome', '').strip()
    filtro_municipio = request.GET.get('municipio', '').strip()

    lista_distritos = Distrito.objects.all()

    if filtro_nome:
        lista_distritos = lista_distritos.filter(nome__istartswith=filtro_nome)
    if filtro_municipio:
        lista_distritos = lista_distritos.filter(municipio__nome__istartswith=filtro_municipio)

    lista_distritos = lista_distritos.order_by('nome')

    paginator = Paginator(lista_distritos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filtro_nome': filtro_nome,
        'filtro_municipio': filtro_municipio,
    }

    return render(request, 'distritos.html', context)


def empresas(request):
    PAGE_SIZE = 15
    last_id = request.GET.get('last_id')
    prev_id = request.GET.get('prev_id')
    campo = request.GET.get('campo', 'razao_social')
    termo = request.GET.get('termo', '').strip()

    quantidade_mostrada = request.session.get('quantidade_mostrada', 0)

    last_id = int(last_id) if last_id and last_id.isdigit() else None
    prev_id = int(prev_id) if prev_id and prev_id.isdigit() else None

    campos_permitidos = {
        'razao_social',
        'cnpj_basico',
        'natureza_juridica',
        'qualificacao_responsavel',
        'porte_da_empresa',
        'ente_federativo_responsavel',
    }

    empresas_qs = Empresa.objects.all()

    if termo and campo in campos_permitidos:
        filtro = {f"{campo}__istartswith": termo}
        empresas_qs = empresas_qs.filter(**filtro)

    empresas_qs = empresas_qs.order_by('id')

    if last_id is not None:
        empresas_qs = empresas_qs.filter(id__gt=last_id)[:PAGE_SIZE]
        tem_anterior = last_id > 0
        tem_mais = empresas_qs.count() == PAGE_SIZE
        novo_last_id = last_id + PAGE_SIZE
        novo_prev_id = last_id - PAGE_SIZE
        if novo_prev_id < 0:
            novo_prev_id = 0
        quantidade_mostrada += len(empresas_qs)

    elif prev_id is not None:
        if prev_id == 0:
            empresas_qs = empresas_qs[:PAGE_SIZE]
            tem_anterior = False
            tem_mais = empresas_qs.count() == PAGE_SIZE
            novo_last_id = PAGE_SIZE
            novo_prev_id = 0
            quantidade_mostrada = len(empresas_qs)
        else:
            empresas_qs = empresas_qs.filter(id__gt=prev_id)[:PAGE_SIZE]
            tem_anterior = prev_id > 0
            tem_mais = empresas_qs.count() == PAGE_SIZE
            novo_last_id = prev_id + PAGE_SIZE
            novo_prev_id = prev_id - PAGE_SIZE
            if novo_prev_id < 0:
                novo_prev_id = 0
            quantidade_mostrada = max(quantidade_mostrada - PAGE_SIZE, PAGE_SIZE)

    else:
        empresas_qs = empresas_qs[:PAGE_SIZE]
        tem_anterior = False
        tem_mais = empresas_qs.count() == PAGE_SIZE
        novo_last_id = PAGE_SIZE
        novo_prev_id = 0
        quantidade_mostrada = len(empresas_qs)

    request.session['quantidade_mostrada'] = quantidade_mostrada

    count_obj = EmpresaCount.objects.first()
    total_empresas = count_obj.total if count_obj else 0

    return render(request, 'empresas.html', {
        'empresas': list(empresas_qs),
        'tem_mais': tem_mais,
        'tem_anterior': tem_anterior,
        'novo_last_id': novo_last_id,
        'novo_prev_id': novo_prev_id,
        'quantidade_mostrada': quantidade_mostrada,
        'total_empresas': total_empresas,
        'campo': campo,
        'termo': termo,
    })

def municipios(request):
    nome = request.GET.get('nome', '').strip()
    estado_nome = request.GET.get('estado', '').strip()

    lista_municipios = Municipio.objects.all()

    if nome:
        lista_municipios = lista_municipios.filter(nome__istartswith=nome)
    if estado_nome:
        lista_municipios = lista_municipios.filter(estado__nome__istartswith=estado_nome)

    lista_municipios = lista_municipios.order_by('nome')
    paginator = Paginator(lista_municipios, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'municipios.html', {
        'page_obj': page_obj,
        'nome': nome,
        'estado': estado_nome,
    })


