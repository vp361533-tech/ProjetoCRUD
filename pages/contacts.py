# pages/contacts.py

from flask import Blueprint, render_template

contacts_bp = Blueprint("contacts", __name__)


@contacts_bp.route("/contacts")
def contacts_page():
    page_title = "Faça Contato"
    return render_template("contacts.html", page_title=page_title)