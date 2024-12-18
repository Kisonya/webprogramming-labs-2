from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8/')
def main():
    """Главная страница"""
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    if request.method == 'GET':
        return render_template('lab8/register.html')

    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Логин и пароль не должны быть пустыми')

    # Проверка существования пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    # Хэширование пароля и создание пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Автоматический логин после регистрации
    login_user(new_user)
    return redirect(url_for('lab8.main'))

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'  # Галочка "Запомнить меня"

    # Поиск пользователя
    user = users.query.filter_by(login=login_form).first()

    # Проверка пароля
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)  # Передаём флаг remember
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error="Неверный логин или пароль")

@lab8.route('/lab8/logout/')
@login_required
def logout():
    """Выход пользователя"""
    logout_user()
    return redirect(url_for('lab8.main'))

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    """Список статей пользователя"""
    user_articles = articles.query.filter_by(user_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    """Создание новой статьи"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Проверка на заполненность полей
        if not title or not content:
            return render_template('lab8/create_article.html', error='Все поля должны быть заполнены')

        # Создание статьи
        new_article = articles(user_id=current_user.id, title=title, article_text=content)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('lab8.article_list'))

    return render_template('lab8/create_article.html')
