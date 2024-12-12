from flask import Flask, url_for, redirect, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
import os

app = Flask(__name__)  # создаем объект
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')  # Устанавливаем секретный ключ приложения
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')  # Устанавливаем тип базы данных (по умолчанию Postgres)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

@app.route("/")  # добавляем маршрут для "/"
@app.route("/index")  # добавляем маршрут для "/index"


def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(err):
    return redirect(url_for('error404'))


@app.errorhandler(500)
def internal_error(err):
    return """<!doctype html>
        <html>
           <head>
               <title>Ошибка сервера</title>
           </head>
           <body>
               <h1>500: Внутренняя ошибка сервера</h1>
               <p>Произошла непредвиденная ошибка. Мы уже работаем над её исправлением.</p>
               <p><a href="/">Вернуться на главную страницу</a></p>
           </body>
        </html>""", 500