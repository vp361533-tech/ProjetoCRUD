# pages/newpad.py

import sqlite3
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from config import DB
from utils.auth import login_required

newpad_bp = Blueprint("newpad", __name__)


@newpad_bp.route("/newpad", methods=["GET", "POST"])
@login_required 
def newpad_page():

    user_uid = g.current_user["own_uid"]

    if request.method == "POST":

        title = request.form.get("padtitle", "").strip()
        content = request.form.get("padcontent", "").strip()
        markdown = "True" if request.form.get("padmarkdown") else "False"

        if len(title) < 4 or len(content) < 4:
            flash("Título e conteúdo devem ter pelo menos 4 caracteres.", "warning")
            return redirect(url_for("newpad.newpad_page"))

        with sqlite3.connect(DB["name"]) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO pads ( pad_title, pad_content, pad_owner, pad_is_markdown, pad_status ) VALUES (?, ?, ?, ?, 'ON') ",
                (title, content, user_uid, markdown)
            )

            conn.commit()

            new_pad_id = cursor.lastrowid

        flash("Pad criado com sucesso.", "success")
        return redirect(url_for("view.view_page", pad_id=new_pad_id))

    form = {
        "action": url_for("newpad.newpad_page"),
        "markdown": False,
        "padtitle": "",
        "padcontent": "",
        "title": "Novo Pad",
    }

    return render_template("padform.html", form=form)