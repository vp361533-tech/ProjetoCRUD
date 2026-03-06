# initdb.py

import sqlite3
from config import DB


def init_db():
    # Conexão
    conn = sqlite3.connect(DB['name'])
    cursor = conn.cursor()

    # --- Criação das tabelas ---

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS owners (
            own_id INTEGER PRIMARY KEY AUTOINCREMENT,
            own_uid TEXT UNIQUE NOT NULL,
            own_display_name TEXT,
            own_email TEXT UNIQUE NOT NULL,
            own_photo_url TEXT,
            own_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            own_last_login_at TEXT DEFAULT CURRENT_TIMESTAMP,
            own_is_admin TEXT NOT NULL DEFAULT 'False' CHECK (own_is_admin IN ('True', 'False')),
            own_status TEXT NOT NULL DEFAULT 'ON' CHECK (own_status IN ('ON', 'OFF', 'DEL')),
            own_metadata TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pads (
            pad_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pad_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            pad_title TEXT NOT NULL,
            pad_content TEXT,
            pad_views INTEGER DEFAULT 0,
            pad_owner TEXT,
            pad_is_markdown TEXT NOT NULL DEFAULT 'False' CHECK (pad_is_markdown IN ('True', 'False')),
            pad_status TEXT NOT NULL DEFAULT 'ON' CHECK (pad_status IN ('ON', 'OFF', 'DEL')),
            pad_metadata TEXT,
            FOREIGN KEY (pad_owner) REFERENCES owners (own_uid)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            cnt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnt_created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            cnt_name TEXT,
            cnt_email TEXT,
            cnt_subject TEXT,
            cnt_message TEXT,
            cnt_status TEXT NOT NULL DEFAULT 'Recebido'
                CHECK (cnt_status IN ('Recebido','Lido','Respondido','Apagado')),
            cnt_metadata TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()