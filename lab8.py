from flask import Blueprint, render_template, request, redirect, session  # Основные модули Flask
from werkzeug.security import generate_password_hash, check_password_hash  # Хэширование паролей
from flask_login import login_user, login_required, current_user  # Flask-Login для авторизации
from db import db  # Подключение базы данных
from db.models import users, articles  # Модели пользователей и статей

# Создаём Blueprint для лабораторной работы 8
lab8 = Blueprint('lab8', __name__, template_folder='templates')

# Маршрут для главной страницы lab8
@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


# Маршрут для регистрации
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    # Проверка существования пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    # Хэширование пароля
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    # Добавляем нового пользователя в базу данных
    db.session.add(new_user)
    db.session.commit()

    # Перенаправляем на главную страницу
    return redirect('/lab8/')


# Создаём маршрут (роут) для авторизации пользователя
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    # Если метод GET — показываем форму авторизации
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    # Чтение данных из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form or not password_form:
        return render_template('lab8/login.html', error='Логин и пароль не должны быть пустыми')

    # Поиск пользователя в базе данных по логину
    user = users.query.filter_by(login=login_form).first()

    # Проверка наличия пользователя и валидация пароля
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=False)  # Логиним пользователя
            return redirect('/lab8/')
    
    # Если авторизация не удалась, возвращаем форму снова с ошибкой
    return render_template('lab8/login.html', error='Неверный логин или пароль')


# Маршрут для вывода всех статей (доступен только авторизованным пользователям)
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "список статей"


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    # Здесь логика создания статьи
    return redirect(url_for('lab8.article_list'))
