from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    db_type = os.environ.get('DB_TYPE', 'sqlite')
    if db_type == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kisonya_knowledge_base',
            user='kisonya_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/')
def index():
    user = session.get('login', "anonymous")
    return render_template('lab5/lab5.html', login=user)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    query = "SELECT login FROM users WHERE login=?"
    if os.environ.get('DB_TYPE') == 'postgres':
        query = "SELECT login FROM users WHERE login=%s"

    cur.execute(query, (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    insert_query = "INSERT INTO users (login, password) VALUES (?, ?)"
    if os.environ.get('DB_TYPE') == 'postgres':
        insert_query = "INSERT INTO users (login, password) VALUES (%s, %s)"

    cur.execute(insert_query, (login, password_hash))
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    if not (title and article_text):
        return render_template('lab5/create_article.html', error="Заполните все поля")

    conn, cur = db_connect()
    user_query = "SELECT id FROM users WHERE login=?"
    if os.environ.get('DB_TYPE') == 'postgres':
        user_query = "SELECT id FROM users WHERE login=%s"

    cur.execute(user_query, (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return "Ошибка: пользователь не найден.", 400

    user_id = user['id']
    insert_query = "INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?)"
    if os.environ.get('DB_TYPE') == 'postgres':
        insert_query = "INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s)"

    cur.execute(insert_query, (user_id, title, article_text))
    db_close(conn, cur)
    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/list', methods=['GET'])
def list_articles():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    user_query = "SELECT id FROM users WHERE login=?"
    if os.environ.get('DB_TYPE') == 'postgres':
        user_query = "SELECT id FROM users WHERE login=%s"

    cur.execute(user_query, (login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return "Ошибка: пользователь не найден.", 400

    user_id = user['id']
    articles_query = "SELECT * FROM articles WHERE user_id=?"
    if os.environ.get('DB_TYPE') == 'postgres':
        articles_query = "SELECT * FROM articles WHERE user_id=%s"

    cur.execute(articles_query, (user_id,))
    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/articles.html', articles=articles)
