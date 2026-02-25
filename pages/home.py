# pages/home.py
# Página inicial

from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
@home_bp.route("/home")
def home_page():
    # Lógica da home entra aqui

    #                        ↓
    return render_template("home.html")