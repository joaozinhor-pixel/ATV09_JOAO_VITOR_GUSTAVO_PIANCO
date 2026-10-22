# ATV09 – Migração do Portal para Django

## Identificação da dupla
- João Vitor Vieira da Costa
- Gustavo Piancó dos Santos
- Turma:513
Curso Técnico em Informática – IFAL.

## Descrição do projeto
Migração do portal "Site Gustagol e JVrau" (ATV07) para o framework Django.
O visual, o HTML semântico, as imagens e a responsividade foram mantidos. O que mudou:

- Os conteúdos das páginas ficam no banco de dados (model `Conteudo`).
- O menu lateral é montado dinamicamente a partir do model `Menu`
  (itens internos ligados a um `Conteudo` e links externos).
- Tudo é cadastrado e alterado pelo **Django Admin**, sem mexer nos templates.
- CSS, JavaScript, imagens e PDF ficam em arquivos estáticos (`paginas/static/paginas/`).

## Tecnologias utilizadas
Python 3, Django, SQLite, HTML5, CSS3 (Grid, Flexbox, Media Queries), JavaScript, Git e GitHub.

## Como executar

### 1. Criar e ativar o ambiente virtual
```bash
python -m venv venv
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate
```

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Executar as migrations
```bash
python manage.py makemigrations paginas
python manage.py migrate
```

### 4. Criar o superusuário
```bash
python manage.py createsuperuser
```

### 5. (Opcional) Carregar os dados iniciais
Cadastra no banco os 6 conteúdos internos e os 9 itens de menu (6 internos + 3 externos):
```bash
python manage.py carregar_dados
```
Também é possível cadastrar tudo manualmente pelo Admin. O HTML de cada página está em
`paginas/conteudos_iniciais/`.

### 6. Executar o servidor
```bash
python manage.py runserver
```

### 7. Acessar
- Portal: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/

## Estrutura
```
ATV09_JOAO_VITOR_GUSTAVO_PIANCO/
├── manage.py
├── requirements.txt
├── meusite/                  # projeto (settings, urls)
└── paginas/                  # aplicação
    ├── models.py             # Conteudo e Menu
    ├── admin.py
    ├── views.py
    ├── urls.py
    ├── context_processors.py # menu dinâmico em todos os templates
    ├── templates/paginas/    # base.html e conteudo.html
    ├── conteudos_iniciais/   # HTML de cada página (usado pelo carregar_dados)
    └── static/paginas/       # css/, js/, img/, pdf/
```
