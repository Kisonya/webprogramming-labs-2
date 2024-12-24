from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from db import db
from db.models import rgz_books
from flask import jsonify


# Создаем Blueprint
rgz_books = Blueprint('rgz_books', __name__, template_folder='templates')

# Главная страница с книгами
@rgz_books.route('/rgz', methods=['GET'])
@rgz_books.route('/rgz/books', methods=['GET'])
def books_list():
    """Страница со списком книг"""
    page = int(request.args.get('page', 1))  # Номер страницы (по умолчанию 1)
    per_page = 20  # Количество книг на странице

    # Получение списка книг с пагинацией
    books = db.session.query(rgz_books).paginate(page=page, per_page=per_page)

    # Передаем книги в шаблон
    return render_template('rgz/books_list.html', books=books)


# Добавление книги (только для администраторов)
@rgz_books.route('/rgz/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        return redirect(url_for('rgz_books.books_list'))  # Только администратор может добавлять книги

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        pages = request.form.get('pages', type=int)
        publisher = request.form.get('publisher')
        cover_image = request.files.get('cover_image')

        # Валидация данных
        if not (title and author and pages and publisher):
            return render_template('rgz/add_book.html', error="Все поля, кроме обложки, обязательны для заполнения")

        # Сохранение обложки (если передана)
        cover_image_path = None
        if cover_image:
            filename = secure_filename(cover_image.filename)
            cover_image_path = os.path.join('static', 'rgz', 'covers', filename)
            cover_image.save(cover_image_path)

        # Добавление книги в базу данных
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
        return redirect(url_for('rgz_books.books_list'))

    return render_template('rgz/add_book.html')


# Удаление книги
@rgz_books.route('/rgz/books/delete/<int:book_id>', methods=['POST'])
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
@rgz_books.route('/rgz/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        return redirect(url_for('rgz_books.books_list'))  # Только администратор может редактировать книги

    book = db.session.query(rgz_books).get_or_404(book_id)

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        pages = request.form.get('pages', type=int)
        publisher = request.form.get('publisher')
        cover_image = request.files.get('cover_image')

        # Валидация данных
        if not (title and author and pages and publisher):
            return render_template('rgz/edit_book.html', book=book, error="Все поля, кроме обложки, обязательны для заполнения")

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
        return redirect(url_for('rgz_books.books_list'))

    return render_template('rgz/edit_book.html', book=book)

