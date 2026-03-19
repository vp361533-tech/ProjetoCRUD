# pages\contacts.py

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for
from config import DB, MAIL
from utils.auth import get_user_by_uid
from utils.mail import send_contact_email

contacts_bp = Blueprint('contacts', __name__)


@contacts_bp.route("/contacts", methods=["GET", "POST"])
def contacts_page():

    user_uid = request.cookies.get("owner_uid")
    user = get_user_by_uid(user_uid)
    userdata = dict(user) if user else None

    own_name = userdata["own_display_name"] if userdata else ""
    own_email = userdata["own_email"] if userdata else ""

    if request.method == "POST":

        form = {
            "name": request.form.get("name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "subject": request.form.get("subject", "").strip(),
            "message": request.form.get("message", "").strip(),
        }

        with sqlite3.connect(DB["name"]) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO contacts 
                (cnt_name, cnt_email, cnt_subject, cnt_message)
                VALUES (?, ?, ?, ?)
            """, (
                form["name"],
                form["email"],
                form["subject"],
                form["message"],
            ))
            conn.commit()

        # Confirma que o INSERT acima foi sucesso
        if cursor.rowcount == 1:

            if MAIL['send_contact']:
                try:
                    send_contact_email(
                        form["name"],
                        form["email"],
                        form["subject"],
                        form["message"]
                    )
                except Exception as e:
                    print("Erro ao enviar email:", e)

            flash("Contato enviado com sucesso!", "success")
        else:
            flash("Oooops! Não foi possível enviar o contato.", "danger")

        return redirect(url_for("contacts.contacts_page"))

    # Reinicia o formulário sempre que é acessado
    form = {
        "name": own_name,
        "email": own_email,
        "subject": "",
        "message": ""
    }

    return render_template(
        "contacts.html",
        form=form,
        page_title="Faça Contato"
    )