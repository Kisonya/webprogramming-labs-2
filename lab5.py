from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к базе данных
def db_connect():
    # Проверяем, какой тип базы данных указан в конфигурации
    if current_app.config['DB_TYPE'] == 'postgres':
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kisonya_knowledge_base',  # Имя базы данных
            user='kisonya_knowledge_base',  # Имя пользователя
            password='123'  # Пароль
        )
        # Создаем курсор с использованием RealDictCursor для возврата данных в виде словаря
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # Подключение к SQLite
        dir_path = path.dirname(path.realpath(__file__))  # Определяем путь к текущему файлу
        db_path = path.join(dir_path, "database.db")  # Создаем путь к файлу SQLite базы данных
        conn = sqlite3.connect(db_path)  # Подключение к SQLite базе данных
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()  # Создаем стандартный курсор для SQLite
    
    # Возвращаем соединение и курсор
    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# Заготовки маршрутов
@lab5.route('/lab5/')
def index():
    user = "anonymous"  # Имя пользователя (по умолчанию anonymous)
    return render_template('lab5/lab5.html', login=session.get('login'))


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Проверка существующего пользователя
    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    # Хэширование пароля
    password_hash = generate_password_hash(password)

    # Вставка нового пользователя
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    db_close(conn, cur)

    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Получение пользователя
    cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    # Проверка пароля
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    conn, cur = db_connect()

    # Получение ID пользователя
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return "Ошибка: пользователь не найден.", 400

    user_id = user['id']

    # Вставка статьи
    cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);",
                (user_id, title, article_text))
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list', methods=['GET'])
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Получение ID пользователя
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return "Ошибка: пользователь не найден.", 400

    user_id = user['id']

    # Получение статей
    cur.execute("SELECT * FROM articles WHERE user_id=%s;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

    # Получаем логин пользователя из сессии
    login = session.get('login')
    if not login:
        # Если пользователь не авторизован, перенаправляем на страницу логина
        return redirect('/lab5/login')

    # Подключение к базе данных
    conn, cur = db_connect()

    # Получение ID пользователя по логину
    cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    user = cur.fetchone()

    user_id = user["id"]

    # Получение статей пользователя
    cur.execute("SELECT * FROM articles WHERE user_id = %s;", (user_id,))
    articles = cur.fetchall()

        # Закрытие подключения
    db_close(conn, cur)

        # Передача статей в шаблон
    return render_template('lab5/articles.html', articles=articles)