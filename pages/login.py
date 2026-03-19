# pages/login.py

from flask import Blueprint, render_template

login_bp = Blueprint("login", __name__)


@login_bp.route("/login")
def login_page():
    page_title = "Loguin / Entrar"
    return render_template("login.html", page_title=page_title)