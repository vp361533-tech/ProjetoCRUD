# app.py

from flask import Flask

# Importa a constante `APP` de `config.py`
from config import APP

# Importa as blueprints
from pages.home import home_bp
from pages.about import about_bp

app = Flask(__name__)

# Injeta as variáveis globalmente, com os valores de `config.APP`


@app.context_processor
def inject_globals():
    return {
        "app_title": APP["title"],
        "app_name": APP["name"],
    }


# Registra as blueprints
app.register_blueprint(home_bp)
app.register_blueprint(about_bp)

if __name__ == '__main__':
    app.run(debug=True)
