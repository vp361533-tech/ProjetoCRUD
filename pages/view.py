# pages\view.py

import sqlite3
from flask import Blueprint, flash, redirect, render_template, request, url_for
from config import DB
from markdown_it import MarkdownIt

from utils.auth import get_user_is_admin

view_bp = Blueprint('view', __name__)
md = MarkdownIt()


@view_bp.route("/view/<int:pad_id>")
def view_page(pad_id):

    owner_uid = request.cookies.get('owner_uid')

    conn = sqlite3.connect(DB['name'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            pads.*, own_uid, own_display_name, own_photo_url, own_status
        FROM pads
        INNER JOIN owners ON pad_owner = own_uid
        WHERE pad_id = ? 
            AND pad_created_at <= datetime('now')
            AND pad_status = 'ON'
    ''', (pad_id,))

    row = cursor.fetchone()

    if row is None:
        flash('Este bloco de notas não existe ou foi removido.', 'info')
        return redirect(url_for('home.home_page'))

    is_owner = (row['pad_owner'] == owner_uid)
    is_admin = get_user_is_admin(owner_uid)

    pad_html = None
    if row["pad_is_markdown"] == "True":
        pad_html = md.render(row["pad_content"])

    cursor.execute("UPDATE pads SET pad_views = pad_views + 1 WHERE pad_id = ?", (pad_id,))
    conn.commit()
    conn.close()

    return render_template(
        "view.html",
        pad=row,
        is_owner=is_owner,
        is_admin=is_admin,
        pad_html=pad_html,
        page_title=row['pad_title']
    )