# 📊 Desafio Técnico ARKO

---

## 🚀 Tecnologias Utilizadas
- [Python 3.x](https://www.python.org/)
- [Django 5.x](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
---

## ⚙️ Configuração do Ambiente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Lothriiik/arko_test.git
cd arko_test
```
## 📂 Estrutura do Projeto
```
.
├── core/                      # Aplicação principal com models e views
├── templates/                 # Templates HTML
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
├── scripts/                   # Scripts para importação de dados
│   ├── import_ibge.py
│   └── import_receita.py
├── arko_test/                  # Configurações do projeto Django
├── manage.py
├── requirements.txt
├── .env                        # Variáveis de ambiente (NÃO subir para o GitHub)
└── README.md
```

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2️⃣ Criar e ativar ambiente virtual
```bash
python -m venv venv
# Ativar no Windows
venv\Scripts\activate
# Ativar no Linux/Mac
source venv/bin/activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Criar o arquivo `.env`
Na raiz do projeto, crie o arquivo `.env` com o seguinte conteúdo (ajuste conforme seu ambiente):

```
SECRET_KEY=sua_chave_secreta_django
DEBUG=True

DB_NAME=arkotest
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```
## 📥 Configuração do Banco de Dados e importação dos Dados

Rode as migrações:
```bash
python manage.py migrate
```

### IBGE
```bash
python importar_dados_ibge
```

### Receita Federal
```bash
python importar_empresas <caminho para o arquivo>
```

Esses scripts irão processar os arquivos e inserir os dados no banco.

---

## 🖥️ Executar o Servidor
```bash
python manage.py runserver
```

Acesse no navegador:  
[http://localhost:8000](http://localhost:8000)

---
