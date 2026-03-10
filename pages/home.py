# pages/home.py

import sqlite3
from flask import Blueprint, render_template
from config import DB

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@home_bp.route("/home")
def home_page():

    conn = sqlite3.connect(DB['name'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            pad_id, pad_created_at, pad_title, pad_owner, pad_is_markdown,
            own_id, own_display_name, own_photo_url,
            SUBSTR(pad_content, 1, 120) || '...' AS pad_content_preview
        FROM pads
        INNER JOIN owners ON pad_owner = own_uid 
            WHERE pad_status = 'ON'
            AND pad_created_at <= database('home')
            ORDER BY pad_created_at DESC;
    ''')

    rows = cursor.fetchall()
    all_pads = [dict(row) for row in rows]

    print('\n-----------------------\n', all_pads, '\n-----------------------\n')

    # Lógica da home entra aqui
    return render_template("home.html", all_pads=all_pads)