from flask import Blueprint, render_template, request, redirect, url_for, flash  # flash добавлен
from flask_login import login_user, logout_user, login_required, current_user  # login_user и logout_user добавлены
from werkzeug.security import generate_password_hash, check_password_hash  # generate_password_hash и check_password_hash добавлены
from werkzeug.utils import secure_filename
import os
from db import db
from db.models import rgz_books, rgz_users
from flask import jsonify
import logging
import re
from flask import current_app as app


# Создаем Blueprint
rgz_books_bp = Blueprint('rgz_books', __name__, template_folder='templates')


def is_valid_login(login):
    # Проверяем, чтобы логин содержал только латинские буквы, цифры и знаки препинания
    pattern = r'^[a-zA-Z0-9._-]+$'
    return bool(re.match(pattern, login))


def is_valid_password(password):
    # Проверяем, чтобы пароль содержал только латинские буквы, цифры и знаки препинания и был не меньше 6 символов
    pattern = r'^[a-zA-Z0-9._-]+$'
    return bool(re.match(pattern, password)) and len(password) >= 6


def is_valid_login(login):
    # Проверяем, чтобы логин содержал только латинские буквы, цифры и знаки препинания
    pattern = r'^[a-zA-Z0-9._-]+$'
    return bool(re.match(pattern, login)) and len(login) >= 3  # Минимальная длина логина — 3 символа


def is_valid_password(password):
    # Проверяем, чтобы пароль содержал только латинские буквы, цифры и знаки препинания и был не меньше 6 символов
    pattern = r'^[a-zA-Z0-9._-]+$'
    return bool(re.match(pattern, password)) and len(password) >= 6


def is_valid_book_data(title, author, pages, publisher):
    # Проверяем, чтобы все строки были непустыми и содержали только допустимые символы
    if not title or not re.match(r'^[a-zA-Z0-9а-яА-ЯёЁ .,-]+$', title):
        return False, "Название книги содержит недопустимые символы или пустое."

    if not author or not re.match(r'^[a-zA-Zа-яА-ЯёЁ .,-]+$', author):
        return False, "Автор книги содержит недопустимые символы или пустое."

    if not publisher or not re.match(r'^[a-zA-Z0-9а-яА-ЯёЁ .,-]+$', publisher):
        return False, "Издательство содержит недопустимые символы или пустое."

    if pages <= 0:
        return False, "Количество страниц должно быть положительным."

    return True, None


@rgz_books_bp.route('/rgz', methods=['GET'])
@rgz_books_bp.route('/rgz/books', methods=['GET'])
def books_list():
    """Страница со списком книг"""
    page = int(request.args.get('page', 1))  # Номер страницы (по умолчанию 1)
    per_page = 20  # Количество книг на странице

    # Получение параметров фильтров
    author_filter = request.args.get('author')
    publisher_filter = request.args.get('publisher')
    pages_min_filter = request.args.get('pages_min', type=int)
    pages_max_filter = request.args.get('pages_max', type=int)
    sort_by = request.args.get('sort_by')

    # Базовый запрос
    query = db.session.query(rgz_books)

    # Применение фильтров
    if author_filter:
        query = query.filter(rgz_books.author.ilike(f"%{author_filter}%"))
    if publisher_filter:
        query = query.filter(rgz_books.publisher.ilike(f"%{publisher_filter}%"))
    if pages_min_filter is not None:
        if pages_min_filter < 0:
            flash("Минимальное количество страниц не может быть отрицательным.", "error")
            return redirect(url_for('rgz_books.books_list'))
    if pages_max_filter is not None:
        if pages_max_filter < 0:
            flash("Максимальное количество страниц не может быть отрицательным.", "error")
            return redirect(url_for('rgz_books.books_list'))

    # Сортировка
    if sort_by == 'title':
        query = query.order_by(rgz_books.title)
    elif sort_by == 'author':
        query = query.order_by(rgz_books.author)
    elif sort_by == 'pages':
        query = query.order_by(rgz_books.pages)
    elif sort_by == 'publisher':
        query = query.order_by(rgz_books.publisher)

    # Пагинация
    books = query.paginate(page=page, per_page=per_page)

    # Передаем книги в шаблон
    return render_template('rgz/books_list.html', books=books)


# Добавление книги (только для администраторов)
@rgz_books_bp.route('/rgz/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        flash('Ошибка: Только администратор может добавлять книги.', 'error')
        return redirect(url_for('rgz_books.books_list'))

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        pages = request.form.get('pages', type=int)
        publisher = request.form.get('publisher')
        cover_image = request.files.get('cover_image')

        # Валидация данных книги
        if not (title and author and pages and publisher):
            flash("Все поля, кроме обложки, обязательны для заполнения.", "error")
            return render_template('rgz/add_book.html')

        if pages <= 0:
            flash("Количество страниц должно быть положительным.", "error")
            return render_template('rgz/add_book.html')

        # Сохранение обложки (если передана)
        cover_image_path = None
        if cover_image:
            filename = secure_filename(cover_image.filename)
            cover_image_path = os.path.join('static', 'rgz', 'covers', filename)
            cover_image.save(cover_image_path)

        # Добавление книги
        new_book = rgz_books(
            title=title,
            author=author,
            pages=pages,
            publisher=publisher,
            cover_image=cover_image_path,
            added_by=current_user.id
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('rgz_books.books_list'))

    return render_template('rgz/add_book.html')


# Удаление книги
@rgz_books_bp.route('/rgz/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403

    book = rgz_books.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return redirect('/rgz/books')


# Редактирование книги
@rgz_books_bp.route('/rgz/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        flash('Ошибка: Только администратор может редактировать книги.', 'error')
        return redirect(url_for('rgz_books.books_list'))

    book = rgz_books.query.get_or_404(book_id)

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        pages = request.form.get('pages', type=int)
        publisher = request.form.get('publisher')
        cover_image = request.files.get('cover_image')

        # Валидация данных книги
        is_valid, error_message = is_valid_book_data(title, author, pages, publisher)
        if not is_valid:
            flash(f'Ошибка: {error_message}', 'error')
            return render_template('rgz/edit_book.html', book=book)

        # Обновление данных книги
        book.title = title
        book.author = author
        book.pages = pages
        book.publisher = publisher

        # Сохранение новой обложки (если передана)
        if cover_image:
            filename = secure_filename(cover_image.filename)
            cover_image_path = os.path.join('static', 'rgz', 'covers', filename)
            cover_image.save(cover_image_path)
            book.cover_image = cover_image_path

        db.session.commit()
        flash('Книга успешно обновлена!', 'success')
        return redirect(url_for('rgz_books.books_list'))

    return render_template('rgz/edit_book.html', book=book)


@rgz_books_bp.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        # Валидация логина
        if not is_valid_login(login):
            flash('Ошибка: Логин должен содержать только латинские буквы, цифры и знаки препинания, и быть не менее 3 символов.', 'error')
            return render_template('rgz/register.html')

        # Валидация пароля
        if not is_valid_password(password):
            flash('Ошибка: Пароль должен содержать только латинские буквы, цифры и знаки препинания, и быть не менее 6 символов.', 'error')
            return render_template('rgz/register.html')

        # Проверка существующего пользователя
        user_exists = rgz_users.query.filter_by(login=login).first()
        if user_exists:
            flash('Ошибка: Пользователь с таким логином уже существует.', 'error')
            return render_template('rgz/register.html')

        # Добавление нового пользователя
        new_user = rgz_users(
            login=login,
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь войдите в свой аккаунт.', 'success')
        return redirect(url_for('rgz_books.login'))

    return render_template('rgz/register.html')


# Настраиваем логирование
logging.basicConfig(
    filename='rgz_auth.log',  # Имя лог-файла
    level=logging.INFO,       # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# Вход пользователя
@rgz_books_bp.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        # Поиск пользователя в базе данных
        user = rgz_users.query.filter_by(login=login).first()

        if not user:
            flash('Ошибка: Пользователь с таким логином не найден.', 'error')
            return render_template('rgz/login.html')

        if not check_password_hash(user.password, password):
            flash('Ошибка: Неверный пароль.', 'error')
            return render_template('rgz/login.html')

        # Авторизация пользователя
        login_user(user)
        app.logger.info(f"Пользователь {user.login} (id: {user.id}) авторизовался через таблицу 'rgz_users'.")
        flash(f"Добро пожаловать, {user.login}!", 'success')
        return redirect(url_for('rgz_books.books_list'))

    return render_template('rgz/login.html')


# Выход пользователя
@rgz_books_bp.route('/rgz/logout')
@login_required
def logout():
    # Логируем факт выхода пользователя
    logging.info(f"Пользователь {current_user.login} (id: {current_user.id}) вышел из системы.")
    
    logout_user()
    flash('Вы успешно вышли из системы.')
    return redirect(url_for('rgz_books.login'))


# Удаление аккаунта авторизованным пользователем
@rgz_books_bp.route('/rgz/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    user_login = current_user.login

    # Удаляем аккаунт из базы данных
    user = rgz_users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        logout_user()  # Выход из системы после удаления аккаунта
        flash(f'Ваш аккаунт "{user_login}" успешно удален.')
        app.logger.info(f'Пользователь {user_login} (id: {user_id}) удалил свой аккаунт.')
    else:
        flash('Аккаунт не найден.')

    return redirect(url_for('rgz_books.books_list'))