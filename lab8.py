from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
# Импорт функций для работы с хэшированием паролей:
# - generate_password_hash: хэширование паролей для безопасного хранения.
# - check_password_hash: проверка соответствия пароля хэшу.

from flask_login import login_user, login_required, current_user, logout_user
# Импорт функций и переменных для работы с авторизацией:
# - login_user: авторизация пользователя.
# - login_required: декоратор для ограничения доступа только для авторизованных пользователей.
# - current_user: текущий авторизованный пользователь.
# - logout_user: выход пользователя из системы.

from db import db
# Импорт объекта базы данных для выполнения операций (SQLAlchemy).

from db.models import users, articles
# Импорт моделей базы данных:
# - users: таблица пользователей.
# - articles: таблица статей.


lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8/')
def main():
    """Главная страница"""
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    if request.method == 'GET':  # Если метод запроса GET
        return render_template('lab8/register.html')  # Отображаем форму регистрации

    # Получаем данные из формы
    login_form = request.form.get('login')  # Логин пользователя
    password_form = request.form.get('password')  # Пароль пользователя

    # Проверка на пустые поля
    if not login_form or not password_form:  # Если логин или пароль не заполнены
        return render_template('lab8/register.html', error='Логин и пароль не должны быть пустыми')

    # Проверка существования пользователя
    login_exists = users.query.filter_by(login=login_form).first()  # Поиск пользователя с таким логином
    if login_exists:  # Если пользователь уже существует
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    # Хэшируем пароль и создаем пользователя
    password_hash = generate_password_hash(password_form)
    print(f"Хэшированный пароль: {password_hash}")  # Отладочное сообщение
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    print(f"Пользователь {login_form} успешно зарегистрирован")


    # Автоматический логин после регистрации
    login_user(new_user)  # Авторизуем нового пользователя
    return redirect(url_for('lab8.main'))  # Перенаправляем на главную страницу


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # Если метод запроса GET
        return render_template('lab8/login.html')  # Отображаем страницу входа

    # Получаем данные из формы
    login_form = request.form.get('login')  # Логин пользователя
    password_form = request.form.get('password')  # Пароль пользователя
    remember_me = request.form.get('remember') == 'on'  # Проверяем, отмечена ли галочка "Запомнить меня"

    # Поиск пользователя
    user = users.query.filter_by(login=login_form).first()  # Ищем пользователя с указанным логином

    # Проверка пароля
    if user and check_password_hash(user.password, password_form):
        print(f"Авторизация успешна для пользователя: {user.login}")
        login_user(user, remember=remember_me)
        return redirect('/lab8/')
    else:
        print(f"Ошибка авторизации для логина: {login_form}")


    # Если данные неверны, отображаем страницу входа с сообщением об ошибке
    return render_template('lab8/login.html', error="Неверный логин или пароль")


@lab8.route('/lab8/logout/')
@login_required
def logout():
    """Выход пользователя"""
    logout_user()
    return redirect(url_for('lab8.main'))

@lab8.route('/lab8/articles/')
@login_required  # Ограничиваем доступ только для авторизованных пользователей
def article_list():
    """Список статей пользователя"""
    # Извлекаем статьи, принадлежащие текущему авторизованному пользователю
    user_articles = articles.query.filter_by(user_id=current_user.id).all()

    # Отображаем страницу с шаблоном и передаём список статей
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required  # Ограничиваем доступ только для авторизованных пользователей
def create_article():
    article = None  # Переменная для передачи в шаблон при создании новой статьи

    if request.method == 'POST':  # Если метод запроса POST
        title = request.form.get('title')  # Получаем заголовок статьи из формы
        content = request.form.get('article_text')  # Получаем текст статьи из формы

        # Проверка на пустые поля
        if not title or not content:  # Если поля не заполнены
            return render_template('lab8/create_article.html', error="Заполните все поля", article=article)

        # Создание новой статьи
        new_article = articles(  # Создаём объект статьи
            title=title,  # Устанавливаем заголовок
            article_text=content,  # Устанавливаем текст
            user_id=current_user.id  # Указываем ID текущего пользователя как автора статьи
        )
        db.session.add(new_article)  # Добавляем новую статью в сессию базы данных
        db.session.commit()  # Сохраняем изменения в базе данных
        return redirect(url_for('lab8.article_list'))  # Перенаправляем на список статей

    return render_template('lab8/create_article.html', article=article)  # Отображаем форму создания статьи




# Маршрут для редактирования статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required  # Ограничиваем доступ только для авторизованных пользователей
def edit_article(article_id):
    # Ищем статью по ID, принадлежащую текущему авторизованному пользователю
    article = articles.query.filter_by(id=article_id, user_id=current_user.id).first()

    # Если статья не найдена или не принадлежит текущему пользователю
    if not article:
        return redirect(url_for('lab8.article_list'))  # Перенаправляем на список статей

    if request.method == 'POST':  # Если метод запроса POST
        title = request.form.get('title')  # Получаем заголовок статьи из формы
        content = request.form.get('article_text')  # Получаем текст статьи из формы

        # Проверка заполненности полей
        if not title or not content:  # Если хотя бы одно поле пустое
            return render_template('lab8/create_article.html', error="Заполните все поля", article=article)

        # Обновляем поля статьи
        article.title = title  # Обновляем заголовок
        article.article_text = content  # Обновляем текст статьи
        db.session.commit()  # Сохраняем изменения в базе данных
        return redirect(url_for('lab8.article_list'))  # Перенаправляем на список статей

    # Если метод запроса GET, отображаем форму редактирования статьи
    return render_template('lab8/create_article.html', article=article)



# Маршрут для удаления статьи
@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required  # Ограничиваем доступ только для авторизованных пользователей
def delete_article(article_id):
    # Ищем статью по ID, принадлежащую текущему авторизованному пользователю
    article = articles.query.filter_by(id=article_id, user_id=current_user.id).first()

    # Если статья найдена и принадлежит текущему пользователю
    if article:
        db.session.delete(article)  # Удаляем статью из сессии базы данных
        db.session.commit()  # Сохраняем изменения в базе данных

    # Перенаправляем на список статей
    return redirect(url_for('lab8.article_list'))
