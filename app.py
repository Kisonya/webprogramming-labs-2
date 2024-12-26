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

login_manager = LoginManager()

# Определяем логику загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    # Проверяем текущий маршрут, чтобы определить модель пользователя
    if request.path.startswith('/rgz'):
        from db.models import rgz_users
        user = rgz_users.query.get(int(user_id))
        if user:
            print(f"DEBUG: Загрузили пользователя {user.login} из таблицы 'rgz_users'")
        return user
    elif request.path.startswith('/lab8'):
        from db.models import users
        user = users.query.get(int(user_id))
        if user:
            print(f"DEBUG: Загрузили пользователя {user.login} из таблицы 'users'")
        return user
    return None  # Если маршрут не RGZ и не Lab8

# Обработка неавторизованного доступа
@login_manager.unauthorized_handler
def handle_unauthorized():
    # Если пользователь пытается получить доступ к RGZ
    if request.path.startswith('/rgz'):
        return redirect(url_for('rgz_books.login'))  # Вход для RGZ

    # Если пользователь пытается получить доступ к Lab8
    elif request.path.startswith('/lab8'):
        return redirect(url_for('lab8.login'))  # Вход для Lab8

    # Если маршрут не относится к Lab8 или RGZ
    return "Unauthorized access", 401

# Инициализация LoginManager
login_manager.init_app(app)

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