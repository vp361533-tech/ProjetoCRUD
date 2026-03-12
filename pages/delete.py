# pages/delete.py

import sqlite3
from flask import Blueprint, flash, g, redirect, url_for
from config import DB
from utils.auth import login_required

delete_bp = Blueprint("delete", __name__)


@delete_bp.route("/delete/<int:pad_id>")
@login_required
def delete_page(pad_id):

    userdata = dict(g.current_user)
    user_uid = userdata.get("own_uid")
    user_admin = userdata.get("own_is_admin") == "True"

    with sqlite3.connect(DB["name"]) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Busca o pad ativo
        cursor.execute("""
            SELECT pad_id, pad_owner
            FROM pads
            WHERE pad_id = ? AND pad_status = 'ON'
        """, (pad_id,))

        pad = cursor.fetchone()

        # Se não existe
        if not pad:
            flash("Pad não existe ou você não tem permissão para fazer isso.", "danger")
            return redirect(url_for("home.home_page"))

        # Verifica permissão
        if pad["pad_owner"] != user_uid and not user_admin:
            flash("Pad não existe ou você não tem permissão para fazer isso.", "danger")
            return redirect(url_for("home.home_page"))

        # Soft delete (mais seguro que DELETE)
        cursor.execute("""
            UPDATE pads
            SET pad_status = 'OFF'
            WHERE pad_id = ?
        """, (pad_id,))

        conn.commit()

    flash("Pad apagado com sucesso.", "success")
    return redirect(url_for("home.home_page"))