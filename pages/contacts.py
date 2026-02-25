# pages/_modelbp.py
# Blueprint modelo
# As setas apontam os dados que precisam ser modificados
# Dica: localize a expressão "contacts" e troque pelo nome da blueprint / página

from flask import Blueprint, render_template

# ↓                   ↓
contacts_bp = Blueprint("contacts", __name__)

#  ↓               ↓
@contacts_bp.route("/contacts")
def contacts_page(): # ←
    # Lógica da contacts entra aqui

    #                        ↓
    return render_template("contacts.html")