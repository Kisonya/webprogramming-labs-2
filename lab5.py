from flask import Blueprint, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

# Заготовки маршрутов
@lab5.route('/lab5/')
def index():
    user = "anonymous"  # Имя пользователя (по умолчанию anonymous)
    return render_template('lab5/lab5.html', login=session.get('login'))


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    # Получение данных из формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на заполненность полей
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    # Подключение к базе данных
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='kisonya_knowledge_base',
        user='kisonya_knowledge_base',
        password='123'
    )
    cur = conn.cursor()

    # Проверка существующего пользователя
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    # Вставка нового пользователя
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()

    # Закрытие подключения
    cur.close()
    conn.close()

    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Отображение страницы с формой входа
        return render_template('lab5/login.html', error=None)

    # Получение данных из формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните все поля")

    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kisonya_knowledge_base',
            user='kisonya_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Проверка пользователя в базе данных
        cur.execute(f"SELECT * FROM users WHERE login = %s", (login,))
        user = cur.fetchone()

        # Если пользователь не найден
        if not user:
            cur.close()
            conn.close()
            return render_template('lab5/login.html', error="Логин и/или пароль неверны")

        # Проверка пароля
        if user['password'] != password:
            cur.close()
            conn.close()
            return render_template('lab5/login.html', error="Логин и/или пароль неверны")

        # Сохранение данных пользователя в сессии
        session['login'] = login

        cur.close()
        conn.close()

        # Переход на страницу успешного входа
        return render_template('lab5/success_login.html', login=login)
    except Exception as e:
        return render_template('lab5/login.html', error="Ошибка подключения к базе данных")


@lab5.route('/lab5/list')
def list_articles():
    return render_template('lab5/list.html')


@lab5.route('/lab5/create')
def create_article():
    return render_template('lab5/create.html')
