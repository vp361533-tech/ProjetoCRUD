# utils/mail.py

import smtplib
from email.message import EmailMessage
from config import APP, MAIL


def send_contact_email(name, email, subject, message):

    msg = EmailMessage()
    msg["Subject"] = f"Novo contato em {APP['title']}"
    msg["From"] = MAIL["username"]
    msg["To"] = MAIL["admin_email"]

    msg.set_content(f"""
Novo contato enviado para {APP['title']}:

 - Nome: {name}
 - Email: {email}
 - Assunto: {subject}

Mensagem:
{message}

______________________________________________
ATENÇÃO! Não responda essa mensagem!

""")

    with smtplib.SMTP(MAIL["server"], MAIL["port"]) as server:
        server.starttls()
        server.login(MAIL["username"], MAIL["password"])
        server.send_message(msg)