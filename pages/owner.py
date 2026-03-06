# pages\owner.py

import sqlite3
from flask import Blueprint, make_response, redirect, request, jsonify, url_for
from config import COOKIE, DB

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')

@owner_bp.route('/login', methods=['POST'])
def owner_login():

    # Recebe os dados do usuário, vindos do front-end, em JSON
    data = request.json
    print('\n\n\n', data, '\n\n\n')  # Debug - Exibe o JSON que vem do front-end

    # Validação básica dos dados recebidos (ajuste conforme necessário)
    if not data or 'uid' not in data or 'email' not in data or 'createdAt' not in data or 'lastLoginAt' not in data:
        return jsonify({'error': 'Dados incompletos ou inválidos'}), 400

    # Conecta ao banco de dados
    conn = sqlite3.connect(DB['name'])
    cursor = conn.cursor()

    # Verifica se o usuário já existe na tabela owners (baseado no UID do Firebase)
    cursor.execute(
        'SELECT own_id FROM owners WHERE own_uid = ?', (data['uid'],))
    # True → usuário existe; False = usuário não existe
    existing_user = cursor.fetchone()

    if existing_user:
        # Atualiza os dados existentes (exceto created_at, que permanece o original)
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
        # Insere um novo usuário
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

    # Cria a resposta JSON
    response = make_response(jsonify({'message': 'Usuário persistido com sucesso'}), 200)

    # Defina o tempo de vida do cookie em segundos
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