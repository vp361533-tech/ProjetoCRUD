# pages/newpad.py

from flask import Blueprint, render_template

newpad_bp = Blueprint("newpad", __name__)


@newpad_bp.route("/newpad")
def newpad_page():
    page_title = "Novo Pad"
    return render_template("newpad.html", page_title=page_title)