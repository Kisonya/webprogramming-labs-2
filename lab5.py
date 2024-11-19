from flask import Blueprint, render_template, request, session, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

lab5 = Blueprint('lab5', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kisonya_knowledge_base',
        user='kisonya_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
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
        # Отображение страницы регистрации, если запрос GET
        return render_template('lab5/register.html')

    # Получение данных из формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на заполненность полей
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')


    # Подключение к базе данных
    conn, cur = db_connect()

    # Проверка существующего пользователя
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        # Если пользователь уже существует, закрываем соединение и выводим ошибку
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    # Хэширование пароля
    password_hash = generate_password_hash(password)

    # Вставка нового пользователя с хэшированным паролем
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password_hash}');")
    conn.commit()

    # Закрытие подключения
    db_close(conn, cur)

    # Переход на страницу успешной регистрации
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()  # Подключение к базе данных

    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    user = cur.fetchone()

    if not user:  # Если пользователь не найден
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    # Проверка пароля с использованием хэша
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login  # Сохраняем логин в сессии

    db_close(conn, cur)  # Закрытие соединения с базой данных
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    # Получаем логин из сессии
    login = session.get('login')

    # Если пользователь не авторизован, перенаправляем на страницу логина
    if not login:
        return redirect('/lab5/login')

    # Если запрос GET, отобразить форму создания статьи
    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    # Получение данных из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Подключение к базе данных
    conn, cur = db_connect()

    # Получение ID пользователя по логину
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    # Вставка статьи в базу данных
    cur.execute(f"INSERT INTO articles (user_id, title, article_text) \
                VALUES ({login_id}, '{title}', '{article_text}');")


    # Закрытие подключения
    db_close(conn, cur)

    # Перенаправление на главную страницу
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list_articles():
    return render_template('lab5/list.html')


