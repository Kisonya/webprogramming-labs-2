from flask import Blueprint, render_template, request
import psycopg2

lab5 = Blueprint('lab5', __name__)

# Заготовки маршрутов
@lab5.route('/lab5/')
def index():
    user = "anonymous"  # Имя пользователя (по умолчанию anonymous)
    return render_template('lab5/lab5.html', user=user)


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

    # Закрытие подключения
    cur.close()
    conn.close()

    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login')
def login():
    return render_template('lab5/login.html')


@lab5.route('/lab5/list')
def list_articles():
    return render_template('lab5/list.html')


@lab5.route('/lab5/create')
def create_article():
    return render_template('lab5/create.html')
