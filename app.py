# app.py

from flask import Flask
from config import APP

from initdb import init_db
from pages.home import home_bp
from pages.about import about_bp
from pages.contacts import contacts_bp
from pages.login import login_bp
from pages.newpad import newpad_bp
from pages.search import search_bp
from pages.owner import owner_bp
from utils.filters import format_datetime_br

# Cria o objeto do Fask
app = Flask(__name__)


# Quando o aplicativo iniciar cria o banco de dados e as tabelas,
# mas somente se as estruturas não existem
init_db()

# Formata datas usando o filtro em utils.filter
app.jinja_env.filters["datetime_br"] = format_datetime_br


@app.context_processor
def inject_globals():
    return {
        "app_title": APP["title"],
        "app_name": APP["name"],
    }


app.register_blueprint(home_bp)
app.register_blueprint(about_bp)
app.register_blueprint(contacts_bp)
app.register_blueprint(login_bp)
app.register_blueprint(newpad_bp)
app.register_blueprint(search_bp)
app.register_blueprint(owner_bp)

if __name__ == "__main__":
    app.run(debug=True)
