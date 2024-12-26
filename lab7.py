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
    # Получение типа базы данных из переменной окружения DB_TYPE (по умолчанию PostgreSQL)
    db_type = os.environ.get('DB_TYPE', 'postgres')

    if db_type == 'sqlite':  # Если указана SQLite как база данных
        # Получение пути к текущему файлу
        dir_path = path.dirname(path.realpath(__file__))
        # Формирование пути к файлу базы данных SQLite
        db_path = path.join(dir_path, "database.db")
        # Вывод пути к базе данных в консоль
        print(f"SQLite database path: {db_path}")
        # Подключение к SQLite базе данных
        conn = sqlite3.connect(db_path)
        # Установка режима возврата строк в формате Row
        conn.row_factory = sqlite3.Row
        # Создание курсора для выполнения запросов
        cur = conn.cursor()
    else:  # Если используется PostgreSQL
        try:
            # Подключение к PostgreSQL базе данных
            conn = psycopg2.connect(
                host='127.0.0.1',  # Хост базы данных (локальный)
                database='kisonya_knowledge_base',  # Имя базы данных
                user='kisonya_knowledge_base',  # Имя пользователя базы данных
                password='123',  # Пароль пользователя
                options='-c client_encoding=UTF8'  # Установка кодировки клиента UTF-8
            )
            # Создание курсора с использованием RealDictCursor для возврата результатов в виде словаря
            cur = conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:  # Обработка ошибок подключения
            # Вывод сообщения об ошибке в консоль
            print(f"Error connecting to PostgreSQL: {e}")
            # Проброс исключения для дальнейшей обработки
            raise

    # Возвращение подключения и курсора
    return conn, cur


# Функция для валидации данных фильма
def validate_film(film):
    errors = {}  # Словарь для хранения ошибок валидации
    current_year = datetime.now().year  # Получаем текущий год

    # Проверка наличия русского названия фильма
    if not film.get('title_ru', '').strip():  # Если поле 'title_ru' отсутствует или пустое
        errors['title_ru'] = 'Русское название обязательно для заполнения.'

    # Если английское название ('title') отсутствует, но есть русское название ('title_ru')
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru'] + '*'  # Формируем английское название на основе русского

    # Проверка корректности года выпуска
    try:
        year = int(film.get('year', 0))  # Преобразуем значение года в целое число
        if year < 1895 or year > current_year:  # Проверяем, входит ли год в допустимый диапазон
            errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}.'
    except ValueError:  # Если преобразование в число не удалось
        errors['year'] = 'Год должен быть числом.'

    # Проверка наличия описания фильма
    description = film.get('description', '')  # Получаем описание фильма
    if not description.strip():  # Если описание отсутствует или пустое
        errors['description'] = 'Описание обязательно для заполнения.'
    elif len(description) > 2000:  # Если длина описания превышает 2000 символов
        errors['description'] = 'Описание не должно превышать 2000 символов.'

    # Возвращаем словарь с ошибками валидации
    return errors


# Главная страница для фильмов
@lab7.route('/lab7/')
def main():
    # Устанавливаем соединение с базой данных и создаем курсор
    conn, cur = db_connect()

    # Выполняем SQL-запрос для получения всех записей из таблицы 'films'
    cur.execute("SELECT * FROM films;")

    # Получаем результаты запроса (все строки из таблицы 'films')
    films = cur.fetchall()

    # Закрываем соединение с базой данных
    conn.close()

    # Отображаем HTML-шаблон 'lab7/lab7.html' и передаём в него список фильмов
    return render_template('lab7/lab7.html', films=films)

 
# REST API — Получение всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    # Устанавливаем соединение с базой данных и создаем курсор
    conn, cur = db_connect()

    # Выполняем SQL-запрос для получения всех записей из таблицы 'films'
    cur.execute("SELECT * FROM films;")

    # Извлекаем результаты запроса и преобразуем их в список словарей
    # Каждый ряд данных из базы данных преобразуется в словарь с ключами, соответствующими именам столбцов
    films = [dict(row) for row in cur.fetchall()]

    # Закрываем соединение с базой данных
    conn.close()

    # Возвращаем список фильмов в виде JSON-объекта
    # Flask автоматически преобразует Python-списки и словари в JSON
    return films


# REST API — Получение фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    try:
        conn, cur = db_connect()
        db_type = os.environ.get('DB_TYPE', 'postgres')
        if db_type == 'postgres':
            cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("SELECT * FROM films WHERE id = ?;", (id,))

        film = cur.fetchone()
        conn.close()

        if not film:
            return {"error": "Фильм с указанным ID не найден"}, 404

        return dict(film)
    except Exception as e:
        print(f"Ошибка при получении фильма: {e}")
        return {"error": f"Ошибка при получении фильма: {e}"}, 500



# REST API — Добавление фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    # Получаем данные фильма из тела запроса в формате JSON
    film = request.get_json()

    # Валидируем данные фильма с использованием функции validate_film
    errors = validate_film(film)
    if errors:  # Если есть ошибки валидации
        return errors, 400  # Возвращаем ошибки с кодом состояния 400 (Bad Request)

    # Устанавливаем соединение с базой данных и создаем курсор
    conn, cur = db_connect()

    # Определяем тип базы данных из переменной окружения (по умолчанию PostgreSQL)
    db_type = os.environ.get('DB_TYPE', 'postgres')

    if db_type == 'postgres':  # Для PostgreSQL
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s) RETURNING *;
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        new_film = cur.fetchone()  # Извлекаем данные добавленного фильма
    else:  # Для SQLite
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?);
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        conn.commit()  # Подтверждаем изменения в базе данных
        # Выполняем запрос, чтобы получить данные последней добавленной записи
        cur.execute("SELECT * FROM films ORDER BY id DESC LIMIT 1;")
        new_film = cur.fetchone()  # Извлекаем данные добавленного фильма

    # Закрываем соединение с базой данных
    conn.close()

    # Проверяем, успешно ли был добавлен фильм
    if not new_film:
        return {"error": "Ошибка добавления фильма в базу данных"}, 500

    # Возвращаем данные добавленного фильма в формате JSON с кодом состояния 201 (Created)
    return dict(new_film), 201


# REST API — Обновление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    # Получаем данные фильма из тела запроса в формате JSON
    film = request.get_json()

    # Валидируем данные фильма
    errors = validate_film(film)
    if errors:
        return errors, 400  # Ошибки валидации

    # Подключаемся к базе данных
    conn, cur = db_connect()
    db_type = os.environ.get('DB_TYPE', 'postgres')

    # Обновляем фильм
    if db_type == 'postgres':
        cur.execute("""
            UPDATE films
            SET title = %s, title_ru = %s, year = %s, description = %s
            WHERE id = %s RETURNING *;
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        updated_film = cur.fetchone()
    else:
        cur.execute("""
            UPDATE films
            SET title = ?, title_ru = ?, year = ?, description = ?
            WHERE id = ?;
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        conn.commit()
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
        updated_film = cur.fetchone()

    conn.close()

    if not updated_film:
        return {"error": "Фильм с указанным ID не найден"}, 404

    return dict(updated_film)


# REST API — Удаление фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def delete_film(id):
    try:
        # Подключаемся к базе данных
        conn, cur = db_connect()
        db_type = os.environ.get('DB_TYPE', 'postgres')

        # Удаляем фильм
        if db_type == 'postgres':
            cur.execute("DELETE FROM films WHERE id = %s RETURNING id;", (id,))
            deleted = cur.fetchone()
        else:
            cur.execute("DELETE FROM films WHERE id = ?;", (id,))
            conn.commit()
            cur.execute("SELECT * FROM films WHERE id = ?", (id,))
            deleted = cur.fetchone()

        conn.close()

        if not deleted:
            return {"error": "Фильм с указанным ID не найден"}, 404

        return {"message": f"Фильм с ID {id} успешно удален"}, 200
    except Exception as e:
        print(f"Ошибка при удалении фильма: {e}")
        return {"error": f"Ошибка при удалении фильма: {e}"}, 500



# Альтернативный маршрут для метода POST (удаление через _method: DELETE)
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['POST'])
def delete_film_fallback(id):
    if request.json.get('_method') == 'DELETE':
        print(f"POST запрос для удаления фильма с ID {id} через _method=DELETE.")
        return delete_film(id)
    print(f"Ошибка: Неподдерживаемый метод для фильма с ID {id}.")
    return {"error": "Метод не поддерживается"}, 405