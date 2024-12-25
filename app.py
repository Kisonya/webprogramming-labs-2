import os
from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import path

from db import db
from db.models import users, articles, rgz_users, rgz_books
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz_books import rgz_books_bp 

# Создаём экземпляр приложения Flask
app = Flask(__name__)

# RGZ LoginManager
rgz_login_manager = LoginManager()
rgz_login_manager.init_app(app)
rgz_login_manager.login_view = 'rgz_books_bp.login'

@rgz_login_manager.user_loader
def load_rgz_user(user_id):
    from db.models import rgz_users
    return rgz_users.query.get(int(user_id))


# Lab8 LoginManager
lab8_login_manager = LoginManager()
lab8_login_manager.init_app(app)
lab8_login_manager.login_view = 'lab8.login'

@lab8_login_manager.user_loader
def load_lab8_user(user_id):
    from db.models import users
    return users.query.get(int(user_id))


# Установите уникальные cookie для каждого приложения
@app.before_request
def set_session_cookie():
    if request.path.startswith('/rgz'):
        app.config['SESSION_COOKIE_NAME'] = 'rgz_session'
    elif request.path.startswith('/lab8'):
        app.config['SESSION_COOKIE_NAME'] = 'lab8_session'

# Настройка секретного ключа приложения
# Используем значение из переменной окружения или задаём дефолтный ключ
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key').encode('utf-8').decode('latin1')

# Устанавливаем тип базы данных (по умолчанию PostgreSQL)
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# Настройка подключения к базе данных
if app.config['DB_TYPE'] == 'postgres':  # Если выбрана база PostgreSQL
    db_name = 'kisonya_orm'  # Имя базы данных
    db_user = 'kisonya_orm'  # Имя пользователя базы данных
    db_password = '123'  # Пароль пользователя базы данных
    host_ip = '127.0.0.1'  # IP-адрес хоста базы данных
    host_port = 5432  # Порт базы данных
    # Формируем строку подключения для PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:  # Если выбрана база SQLite
    dir_path = path.dirname(path.realpath(__file__))  # Определяем путь к текущему файлу
    db_path = path.join(dir_path, "kisonya_orm.db")  # Путь к файлу базы SQLite
    # Формируем строку подключения для SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Инициализация БД
db.init_app(app)

# Регистрация Blueprint
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz_books_bp )

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.errorhandler(404)
def not_found(err):
    return redirect(url_for('lab1.error404'))

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