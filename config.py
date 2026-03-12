# config.py

# Configurações do site / aplicativo
APP = {
    # Nome do site para a tag `<title>...</title>`
    'title': 'MyPyPad',

    # Nome / logo do site, em HTML, para a tag `.navbar-brand` e outros usos
    'name': 'My<i class="bi bi-filetype-py text-warning px-0"></i>Pad',

    # Chave secreta (48 caracteres)
    # Obtenha essa chave rodando `python keygen.py`
    'secret_key': 'db90279b4cdd584af0742deff388fad5345e43ed22d6b62976c203446c215dba78c2e9a8bd1196a709236f84f1df8248',
}

# Configurações do banco de dados
DB = {
    'name': 'database.db',
}

# Configurações dos cookies
COOKIE = {
    'livedays': 30,
}