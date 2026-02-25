# pages/about.py
# Páginas "estáticas" tem suas rotas aqui

from flask import Blueprint, render_template

about_bp = Blueprint("about", __name__)

@about_bp.route("/about")
def about_page():
    page_title = "Sobre..."
    return render_template("about.html", page_title=page_title)

@about_bp.route("/privacy")
def privacy_page():
    page_title = "Políticas de Privacidade"
    return render_template("privacy.html", page_title=page_title)