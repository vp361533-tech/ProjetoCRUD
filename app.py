from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
    return '<h1>Hello, World!</h1>'

@app.route('/about')
def about_page():
    a = 10
    return f'<h1>Sombre {a}</h1>'

if __name__ == '__main__':
    app.run(debug=True)