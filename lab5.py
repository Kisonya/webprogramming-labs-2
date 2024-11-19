from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

# Создание Blueprint для работы с маршрутом "lab5"
lab5 = Blueprint('lab5', __name__)

# Функция для подключения к базе данных
def db_connect():
    # Проверяем, какая база данных используется
    if current_app.config['DB_TYPE'] == 'postgres':
        # Подключение к PostgreSQL
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kisonya_knowledge_base',
            user='kisonya_knowledge_base',
            password='123'
        )
        # Создаем курсор с поддержкой словарей
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # Подключение к SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

# Функция для закрытия подключения к базе данных
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Главная страница приложения
@lab5.route('/lab5/')
def index():
    user = session.get('login', "anonymous")
    return render_template('lab5/lab5.html', login=user)


# Регистрация нового пользователя
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка заполненности полей
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Проверка на существование пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    # Хэшируем пароль
    password_hash = generate_password_hash(password)

    # Сохранение нового пользователя в базу данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


# Вход в систему
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка заполненности полей
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    # Поиск пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login  # Сохраняем логин в сессии
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


# Выход из системы
@lab5.route('/lab5/logout')
def logout():
    session.clear()  # Очищаем сессию
    return redirect(url_for('lab5.index'))


# Создание новой статьи
# Создание новой статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')  # Проверяем, авторизован ли пользователь

    if request.method == 'GET':
        return render_template('lab5/create_article.html', login=login)

    # Получение данных из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'  # True, если галочка установлена

    # Проверка заполненности полей
    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Заполните все поля", login=login)

    conn, cur = db_connect()

    # Если пользователь авторизован
    if login:
        # Получаем ID пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))

        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return "Ошибка: пользователь не найден.", 400

        user_id = user['id']

        # Создаем статью с привязкой к пользователю
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public)
                VALUES (%s, %s, %s, %s);
            """, (user_id, title, article_text, is_public))
        else:
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public)
                VALUES (?, ?, ?, ?);
            """, (user_id, title, article_text, is_public))

    # Если пользователь не авторизован
    else:
        # Неавторизованный пользователь может создавать только публичные посты
        if not is_public:
            db_close(conn, cur)
            return render_template('lab5/create_article.html', error="Неавторизованный пользователь может создать только публичный пост", login=None)

        # Создаем статью без привязки к user_id
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public)
                VALUES (NULL, %s, %s, %s);
            """, (title, article_text, is_public))
        else:
            cur.execute("""
                INSERT INTO articles (user_id, title, article_text, is_public)
                VALUES (NULL, ?, ?, ?);
            """, (title, article_text, is_public))

    db_close(conn, cur)
    return redirect(url_for('lab5.list_articles') if login else url_for('lab5.public_articles'))


# Список статей пользователя
@lab5.route('/lab5/list', methods=['GET'])
def list_articles():
    login = session.get('login')  # Получаем текущего пользователя
    if not login:  # Проверяем авторизацию
        return redirect(url_for('lab5.login'))  # Перенаправляем на страницу входа

    conn, cur = db_connect()

    # Получение ID текущего пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return "Ошибка: пользователь не найден.", 400

    user_id = user['id']

    # Запрос на получение статей пользователя, сортированных по is_favorite
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT * FROM articles 
            WHERE user_id=%s 
            ORDER BY is_favorite DESC, id ASC;
        """, (user_id,))
    else:
        cur.execute("""
            SELECT * FROM articles 
            WHERE user_id=? 
            ORDER BY is_favorite DESC, id ASC;
        """, (user_id,))

    articles = cur.fetchall()

    db_close(conn, cur)

    # Если статей нет, выводим сообщение
    if not articles:
        return render_template('lab5/articles.html', articles=[], message="У вас пока нет статей")

    return render_template('lab5/articles.html', articles=articles)



# Удаление статьи
@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()

    # Удаление статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect(url_for('lab5.list_articles'))


# Редактирование статьи
@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()

    if request.method == 'GET':
        # Получение данных статьи
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))

        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return "Статья не найдена", 404

        return render_template('lab5/edit_article.html', article=article)

    # Сохранение изменений
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/edit_article.html', error="Заполните все поля", article={"id": article_id})

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect(url_for('lab5.list_articles'))


# Страница с выводом всех зарегистрированных пользователей
@lab5.route('/lab5/users')
def list_users():
    conn, cur = db_connect()  # Подключение к базе данных
    # Запрос на получение всех логинов из таблицы users
    cur.execute("SELECT login FROM users")
    users = cur.fetchall()
    db_close(conn, cur)  # Закрытие соединения с базой
    # Передаем список пользователей в шаблон
    return render_template('lab5/users.html', users=users)


# # Вывод публичных статей (is_public = 1)
# @lab5.route('/lab5/public_articles', methods=['GET'])
# def public_articles():
#     conn, cur = db_connect()

#     # Запрос для получения всех публичных статей
#     if current_app.config['DB_TYPE'] == 'postgres':
#         cur.execute("""
#             SELECT a.title, a.article_text, u.login AS author 
#             FROM articles a
#             JOIN users u ON a.user_id = u.id
#             WHERE a.is_public = 1
#             ORDER BY a.id ASC;
#         """)
#     else:
#         cur.execute("""
#             SELECT a.title, a.article_text, u.login AS author 
#             FROM articles a
#             JOIN users u ON a.user_id = u.id
#             WHERE a.is_public = 1
#             ORDER BY a.id ASC;
#         """)

#     public_articles = cur.fetchall()
#     db_close(conn, cur)

#     # Если публичных статей нет, отображаем сообщение
#     if not public_articles:
#         return render_template('lab5/public_articles.html', articles=[], message="Публичные статьи отсутствуют")

#     return render_template('lab5/public_articles.html', articles=public_articles)
