# pages/owner.py

from utils.auth import login_required
import sqlite3
from flask import Blueprint, g, make_response, redirect, render_template, request, jsonify, url_for
from config import COOKIE, DB
from utils import _debug
from utils.auth import get_user_by_uid, login_required

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')


@owner_bp.route('/login', methods=['POST'])
def owner_login():

    data = request.json
    # print(data)  # Debug - Exibe o JSON que vem do front-end

    if not data or 'uid' not in data or 'email' not in data or 'createdAt' not in data or 'lastLoginAt' not in data:
        return jsonify({'error': 'Dados incompletos ou inválidos'}), 400

    conn = sqlite3.connect(DB['name'])
    cursor = conn.cursor()

    cursor.execute(
        'SELECT own_id FROM owners WHERE own_uid = ?', (data['uid'],))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute('''
            UPDATE owners SET
                own_display_name = ?,
                own_email = ?,
                own_photo_url = ?,
                own_last_login_at = ?
            WHERE own_uid = ?
        ''', (
            data.get('displayName'),
            data.get('email'),
            data.get('photoURL'),
            data.get('lastLoginAt'),
            data.get('uid')
        ))
    else:
        cursor.execute('''
            INSERT INTO owners (
                own_uid, 
                own_display_name, 
                own_email, 
                own_photo_url, 
                own_created_at, 
                own_last_login_at, 
                own_status
            ) VALUES (?, ?, ?, ?, ?, ?, 'ON')
        ''', (
            data.get('uid'),
            data.get('displayName'),
            data.get('email'),
            data.get('photoURL'),
            data.get('createdAt'),
            data.get('lastLoginAt')
        ))

    conn.commit()
    conn.close()

    response = make_response(
        jsonify({'message': 'Usuário persistido com sucesso'}), 200)

    max_age = 3600 * 24 * COOKIE['livedays']

    # Define o cookie seguro com o UID quando fizer login
    # - secure=True: Envia apenas via HTTPS (em produção; em dev, defina como False se necessário)
    # - httponly=True: Impede acesso via JavaScript (protege contra XSS)
    # - samesite='Strict': Protege contra CSRF, permitindo apenas do mesmo site
    response.set_cookie(
        'owner_uid',
        data['uid'],
        max_age=max_age,
        secure=True,
        httponly=True,
        samesite='Strict'
    )

    return response


@owner_bp.route('/logout', methods=['POST'])
def owner_logout():
    try:
        data = request.get_json(silent=True) or {}
    except:
        data = {}

    if data.get('action') != 'logout':
        return jsonify({'error': 'Ação inválida'}), 400

    redirect_to = data.get('redirectTo', '/').strip()
    if not redirect_to.startswith('/'):
        redirect_to = '/'

    response = make_response(redirect(redirect_to))
    response.delete_cookie(
        'owner_uid',
        path='/',
        secure=True,
        httponly=True,
        samesite='Strict'
    )
    return response


@owner_bp.route('/profile')
@login_required
def owner_profile():

    userdata = dict(g.current_user)
    page_title = f"Perfil de {userdata.get('own_display_name', 'Usuário')}"
    user_uid = userdata.get('own_uid', None)

    with sqlite3.connect(DB["name"]) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT pad_id, pad_title FROM pads WHERE pad_owner = ? AND pad_status = 'ON' ORDER BY pad_created_at DESC",
            (user_uid,)
        )

        rows = cursor.fetchall()
        all_pads = [dict(row) for row in rows]

    return render_template(
        "profile.html",
        page_title=page_title,
        userdata=userdata,
        all_pads=all_pads,
    )  # pages/owner.py


owner_bp = Blueprint('owner', __name__, url_prefix='/owner')


@owner_bp.route('/login', methods=['POST'])
def owner_login():

    data = request.json
    # print(data)  # Debug - Exibe o JSON que vem do front-end

    if not data or 'uid' not in data or 'email' not in data or 'createdAt' not in data or 'lastLoginAt' not in data:
        return jsonify({'error': 'Dados incompletos ou inválidos'}), 400

    conn = sqlite3.connect(DB['name'])
    cursor = conn.cursor()

    cursor.execute(
        'SELECT own_id FROM owners WHERE own_uid = ?', (data['uid'],))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.execute('''
            UPDATE owners SET
                own_display_name = ?,
                own_email = ?,
                own_photo_url = ?,
                own_last_login_at = ?
            WHERE own_uid = ?
        ''', (
            data.get('displayName'),
            data.get('email'),
            data.get('photoURL'),
            data.get('lastLoginAt'),
            data.get('uid')
        ))
    else:
        cursor.execute('''
            INSERT INTO owners (
                own_uid, 
                own_display_name, 
                own_email, 
                own_photo_url, 
                own_created_at, 
                own_last_login_at, 
                own_status
            ) VALUES (?, ?, ?, ?, ?, ?, 'ON')
        ''', (
            data.get('uid'),
            data.get('displayName'),
            data.get('email'),
            data.get('photoURL'),
            data.get('createdAt'),
            data.get('lastLoginAt')
        ))

    conn.commit()
    conn.close()

    response = make_response(
        jsonify({'message': 'Usuário persistido com sucesso'}), 200)

    max_age = 3600 * 24 * COOKIE['livedays']

    # Define o cookie seguro com o UID quando fizer login
    # - secure=True: Envia apenas via HTTPS (em produção; em dev, defina como False se necessário)
    # - httponly=True: Impede acesso via JavaScript (protege contra XSS)
    # - samesite='Strict': Protege contra CSRF, permitindo apenas do mesmo site
    response.set_cookie(
        'owner_uid',
        data['uid'],
        max_age=max_age,
        secure=True,
        httponly=True,
        samesite='Strict'
    )

    return response


@owner_bp.route('/logout', methods=['POST'])
def owner_logout():
    try:
        data = request.get_json(silent=True) or {}
    except:
        data = {}

    if data.get('action') != 'logout':
        return jsonify({'error': 'Ação inválida'}), 400

    redirect_to = data.get('redirectTo', '/').strip()
    if not redirect_to.startswith('/'):
        redirect_to = '/'

    response = make_response(redirect(redirect_to))
    response.delete_cookie(
        'owner_uid',
        path='/',
        secure=True,
        httponly=True,
        samesite='Strict'
    )
    return response


@owner_bp.route('/profile')
@login_required
def owner_profile():

    userdata = dict(g.current_user)
    page_title = f"Perfil de {userdata.get('own_display_name', 'Usuário')}"
    user_uid = userdata.get('own_uid', None)

    with sqlite3.connect(DB["name"]) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT pad_id, pad_title FROM pads WHERE pad_owner = ? AND pad_status = 'ON' ORDER BY pad_created_at DESC",
            (user_uid,)
        )

        rows = cursor.fetchall()
        all_pads = [dict(row) for row in rows]

    return render_template(
        "profile.html",
        page_title=page_title,
        userdata=userdata,
        all_pads=all_pads,
    )

# Exibe uma página com todos os pads do usuário identificado pelo uid


@owner_bp.route('/pads/<string:uid>')
def ownerpads_page(uid):

    user_data = get_user_by_uid(uid)

    if not user_data:
        return redirect(url_for("home.home_page"))
    
    with sqlite3.connect(DB["name"]) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
                -- Seleciona todos os pads ativos de um owner específico
                SELECT * FROM pads
                WHERE pad_owner = ?
                    AND pad_status = 'ON'
                ORDER BY pad_created_at DESC;
            """,
            (user_data['own_uid'],)
        )
        pads = cursor.fetchall()

    return render_template('pads.html', owner=user_data, pads=pads)
