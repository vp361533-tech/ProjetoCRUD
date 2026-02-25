# pages/_modelbp.py
# Blueprint modelo
# As setas apontam os dados que precisam ser modificados
# Dica: localize a expressão "modelbp" e troque pelo nome da blueprint / página

from flask import Blueprint, render_template

# ↓                   ↓
home_bp = Blueprint("modelbp", __name__)

#  ↓               ↓
@home_bp.route("/modelbp")
def home_page(): # ←
    # Lógica da modelbp entra aqui

    #                        ↓
    return render_template("modelbp.html")