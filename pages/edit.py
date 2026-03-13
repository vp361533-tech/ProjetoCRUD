# pages/edit.py

import sqlite3
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from config import DB
from utils.auth import login_required

edit_bp = Blueprint("edit", __name__)


@edit_bp.route("/edit/<int:pad_id>", methods=["GET", "POST"])
@login_required
def edit_page(pad_id):

    user_uid = g.current_user["own_uid"]
    user_admin = g.current_user["own_is_admin"]

    with sqlite3.connect(DB["name"]) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM pads WHERE pad_id = ? AND pad_status = 'ON'",
            (pad_id,)
        )
        pad = cursor.fetchone()

        if not pad:
            flash("Pad não encontrado.", "danger")
            return redirect(url_for("home.home_page"))

        if pad["pad_owner"] != user_uid and not user_admin:
            flash("Você não tem permissão para editar este pad.", "danger")
            return redirect(url_for("view.view_page", pad_id=pad_id))

        if request.method == "POST":

            title = request.form.get("padtitle", "").strip()
            content = request.form.get("padcontent", "").strip()
            markdown = "True" if request.form.get("padmarkdown") else "False"

            if len(title) < 4 or len(content) < 4:
                flash("Título e conteúdo devem ter pelo menos 4 caracteres.", "warning")
                return redirect(url_for("view.view_page", pad_id=pad_id))

            cursor.execute(
                " UPDATE pads SET pad_title = ?, pad_content = ?, pad_is_markdown = ? WHERE pad_id = ?",
                (title, content, markdown, pad_id)
            )

            conn.commit()

            flash("Pad atualizado com sucesso.", "success")
            return redirect(url_for("view.view_page", pad_id=pad_id))

        form = {
            "action": url_for("edit.edit_page", pad_id=pad_id),
            "markdown": pad["pad_is_markdown"] == "True",
            "padtitle": pad["pad_title"],
            "padcontent": pad["pad_content"],
            "title": "Editar Pad",
        }

        return render_template("padform.html", form=form)