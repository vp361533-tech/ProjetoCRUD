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

# Configurações do e-mail
MAIL = {
    # Boolean: True envia e-mails, False não envia 
    "send_contact": False,

    # Servidor SMTP e porta do Gmail / provedor
    "server": "smtp.gmail.com",
    "port": 587,

    # Conta de e-mail do administrador do site
    "username": "vp361533@gmail",
    "admin_email": "vp361533@gmail",
    
    # Acesse https://myaccount.google.com/apppasswords para gerar a senha de aplicativo abaixo
    "password": "senha de aplicativo aqui",
}