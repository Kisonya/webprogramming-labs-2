import os
from flask import Blueprint, render_template, request
from datetime import datetime
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from os import path

lab7 = Blueprint('lab7', __name__)

# Функция подключения к базе данных
def db_connect():
    db_type = os.environ.get('DB_TYPE', 'postgres')  # По умолчанию PostgreSQL
    if db_type == 'sqlite':
        # Подключение к SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        print(f"SQLite database path: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    else:
        # Подключение к PostgreSQL
        try:
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='kisonya_knowledge_base',
                user='kisonya_knowledge_base',
                password='123',
                client_encoding='UTF8'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    return conn, cur

# Валидация данных фильма
def validate_film(film):
    errors = {}
    current_year = datetime.now().year

    if not film.get('title_ru', '').strip():
        errors['title_ru'] = 'Русское название обязательно для заполнения.'

    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru'] + '*'

    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}.'
    except ValueError:
        errors['year'] = 'Год должен быть числом.'

    description = film.get('description', '')
    if not description.strip():
        errors['description'] = 'Описание обязательно для заполнения.'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов.'

    return errors

# Главная страница для фильмов
@lab7.route('/lab7/')
def main():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    conn.close()
    return render_template('lab7/lab7.html', films=films)

# REST API — Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = [dict(row) for row in cur.fetchall()]
    conn.close()
    return films

# REST API — Получение фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if os.environ.get('DB_TYPE', 'postgres') == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))

    film = cur.fetchone()
    conn.close()

    if not film:
        return {"error": "Фильм с указанным ID не найден"}, 404

    return dict(film)

# REST API — Добавление фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()
    if os.environ.get('DB_TYPE', 'postgres') == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s) RETURNING *;
        """, (film['title'], film['title_ru'], film['year'], film['description']))
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?);
        """, (film['title'], film['title_ru'], film['year'], film['description']))

    conn.commit()
    new_film = cur.fetchone()
    conn.close()
    return dict(new_film), 201

# REST API — Обновление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    errors = validate_film(film)
    if errors:
        return errors, 400

    conn, cur = db_connect()
    if os.environ.get('DB_TYPE', 'postgres') == 'postgres':
        cur.execute("""
            UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s
            WHERE id = %s RETURNING *;
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    else:
        cur.execute("""
            UPDATE films SET title = ?, title_ru = ?, year = ?, description = ?
            WHERE id = ?;
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))

    conn.commit()
    updated_film = cur.fetchone()
    conn.close()

    if not updated_film:
        return {"error": "Фильм с указанным ID не найден"}, 404
    return dict(updated_film)

# REST API — Удаление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn, cur = db_connect()
    if os.environ.get('DB_TYPE', 'postgres') == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s RETURNING id;", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ? RETURNING id;", (id,))

    conn.commit()
    deleted = cur.fetchone()
    conn.close()

    if not deleted:
        return {"error": "Фильм с указанным ID не найден"}, 404
    return '', 204
