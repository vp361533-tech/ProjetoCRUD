# pages/_modelbp.py
# Blueprint modelo
# As setas apontam os dados que precisam ser modificados
# Dica: localize a expressão "modelbp" e troque pelo nome da blueprint / página

from flask import Blueprint, render_template

# ↓                   ↓
modelbp_bp = Blueprint("modelbp", __name__)

#  ↓               ↓
@modelbp_bp.route("/modelbp")
def modelbp_page(): # ←
    # Lógica da modelbp entra aqui

    #                        ↓
    return render_template("modelbp.html")