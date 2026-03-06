# pages/search.py

from flask import Blueprint, render_template

search_bp = Blueprint("search", __name__)


@search_bp.route("/search")
def search_page():
    page_title = "Procurar"
    return render_template("search.html", page_title=page_title)