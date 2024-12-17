import os
import logging  # Добавляем логирование

from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from db import db
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from os import path

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Создаём объект приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

# Подключение к базе данных
try:
    if app.config['DB_TYPE'] == 'postgres':
        db_name = 'kisonya_orm'
        db_user = 'kisonya_orm'
        db_password = '123'
        host_ip = '127.0.0.1'
        host_port = 5432

        logger.debug(f"Подключаемся к PostgreSQL: host={host_ip}, port={host_port}, db_name={db_name}")
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
    elif app.config['DB_TYPE'] == 'sqlite':
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "kisonya_orm.db")
        logger.debug(f"Подключаемся к SQLite: path={db_path}")
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    else:
        raise ValueError("Unsupported DB_TYPE. Use 'postgres' or 'sqlite'.")
except Exception as e:
    logger.error(f"Ошибка при настройке подключения к базе данных: {e}")

# Инициализация БД
try:
    db.init_app(app)
    logger.info("База данных инициализирована успешно")
except Exception as e:
    logger.critical(f"Не удалось инициализировать базу данных: {e}")

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
    logger.warning("Ошибка 404: Страница не найдена")
    return redirect(url_for('lab1.error404'))


@app.errorhandler(500)
def internal_error(err):
    logger.error("Ошибка 500: Внутренняя ошибка сервера")
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
