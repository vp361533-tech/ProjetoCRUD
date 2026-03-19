# utils/auth.py

import sqlite3
from functools import wraps
from flask import request, redirect, url_for, g
from config import DB


def get_user_by_uid(uid):
    conn = sqlite3.connect(DB['name'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM owners WHERE own_uid = ? AND own_status = 'ON'",
        (uid,)
    )
    user = cursor.fetchone()

    conn.close()
    return user


def login_required(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):

        uid = request.cookies.get("owner_uid")

        if not uid:
            return redirect(url_for("home.home_page"))

        user = get_user_by_uid(uid)

        if not user:
            return redirect(url_for("home.home_page"))

        g.current_user = user

        return view_function(*args, **kwargs)

    return decorated_function


def get_user_is_admin(uid):
    user = get_user_by_uid(uid)
    if not user:
        return False
    return user['own_is_admin'].strip().lower() == 'true'