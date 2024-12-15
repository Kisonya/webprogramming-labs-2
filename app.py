import os
from dotenv import load_dotenv
load_dotenv()  # Загружаем переменные окружения из .env файла

from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy  # Импорт SQLAlchemy для работы с базой данных
from db import db  # Импортируем объект db из файла __init__.py
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from os import path

# Создаём объект приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')  # Устанавливаем секретный ключ приложения
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')  # Устанавливаем тип базы данных (по умолчанию Postgres)

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'kisonya_orm'  # Название базы данных
    db_user = 'kisonya_orm'  # Имя пользователя базы данных
    db_password = '123'      # Пароль пользователя базы данных
    host_ip = '127.0.0.1'    # Локальный IP-адрес
    host_port = 5432         # Порт PostgreSQL

    # Строка подключения к PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

elif app.config['DB_TYPE'] == 'sqlite':
    # Настройка для SQLite
    dir_path = path.dirname(path.realpath(__file__))  # Путь к текущей директории
    db_path = path.join(dir_path, "kisonya_orm.db")   # Путь к SQLite базе данных
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    raise ValueError("Unsupported DB_TYPE. Use 'postgres' or 'sqlite'.")  # Обработка ошибки, если указан неизвестный тип БД


db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

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