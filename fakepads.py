# fakepads.py

import sqlite3
import random

from config import DB


def seed_pads():
    conn = sqlite3.connect(DB['name'])
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(pad_id) FROM pads")
    total = cursor.fetchone()[0]
    if total > 0:
        print("Tabela 'pads' já contém registros. Seed ignorado.")
        conn.close()
        return

    cursor.execute("SELECT own_uid FROM owners WHERE own_status = 'ON'")
    owners = [row[0] for row in cursor.fetchall()]

    if not owners:
        print("Nenhum owner ativo encontrado.")
        conn.close()
        return

    pads = [
        ('Receita de Bolo de Chocolate', 'Ingredientes: 2 xícaras de farinha, 1 xícara de açúcar, 3 ovos. Modo: Misture tudo e asse por 30 min. Delícia!', '2025-11-11 10:00:00', 'ON'),
        ('Dicas para Viajar Barato', 'Compre passagens com antecedência, use hostels e coma street food. Aventura garantida!', '2025-11-10 14:30:00', 'ON'),
        ('Como Treinar Seu Cachorro', 'Use petiscos como recompensa, treine comandos básicos como senta e fica. Paciência é chave!', '2025-11-09 09:15:00', 'ON'),
        ('Receita de Pizza Caseira', 'Massa: farinha, água, fermento. Recheio: molho, queijo, pepperoni. Asse em forno quente.', '2025-11-08 16:45:00', 'ON'),
        ('Melhores Filmes de Comédia', 'Recomendo "Se Beber Não Case" e "Superbad". Risadas non-stop!', '2025-11-07 11:20:00', 'ON'),
        ('Dicas de Jardinagem para Iniciantes', 'Escolha plantas resistentes, regue moderadamente e use sol adequado. Verde na casa!', '2025-11-06 13:50:00', 'ON'),
        ('Receita de Smoothie Energético', 'Banana, morango, iogurte e espinafre. Bata no liquidificador para um boost matinal.', '2025-11-05 08:30:00', 'ON'),
        ('Histórias Engraçadas de Viagem', 'Uma vez, confundi o trem e acabei em outra cidade. Lição: leia as placas!', '2025-11-04 15:10:00', 'ON'),
        ('Como Fazer Exercícios em Casa', 'Flexões, abdominais e corrida no lugar. Sem academia necessária!', '2025-11-03 17:40:00', 'ON'),
        ('Receita de Cookies Perfeitos', 'Manteiga, açúcar, farinha e gotas de chocolate. Asse até dourar. Irresistíveis!', '2025-11-02 12:00:00', 'ON'),
        ( 'A importância da leitura','Ler é uma das melhores formas de aprender coisas novas',' 2025-11-03','ON')
        ()
    ]

    for title, content, created_at, status in pads:
        cursor.execute("""
            INSERT INTO pads
            (pad_title, pad_content, pad_created_at, pad_status, pad_owner)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            content,
            created_at,
            status,
            random.choice(owners)
        ))

    conn.commit()
    conn.close()
    print("Seed executado com sucesso.")


if __name__ == "__main__":
    seed_pads()