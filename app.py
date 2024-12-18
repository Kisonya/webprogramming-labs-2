import os
from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path

from db import db
from db.models import users, articles
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

# Создаём объект приложения
app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_viev = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# Подключение к базе данных
if app.config['DB_TYPE'] == 'postgres':
    db_name = 'kisonya_orm'
    db_user = 'kisonya_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "kisonya_orm.db")
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
