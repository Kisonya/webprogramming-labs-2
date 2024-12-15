from flask import Blueprint, render_template, request  # Импортируем необходимые компоненты Flask для создания маршрутов и обработки запросов
from datetime import datetime  # Импортируем модуль для работы с текущей датой и временем

# Создаём Blueprint для маршрутов лабораторной работы 7
lab7 = Blueprint('lab7', __name__)

# Предопределённый список фильмов с данными о них
films = [
    {
        "title": "Inception",  # Оригинальное название фильма
        "title_ru": "Начало",  # Русское название фильма
        "year": 2010,  # Год выпуска фильма
        "description": "Вор, который крадёт корпоративные секреты с помощью технологий совместного сна, получает шанс искупить свои преступления, внедрив идею в сознание генерального директора."  # Описание фильма
    },
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": "Компьютерный хакер узнаёт от загадочных повстанцев правду о своей реальности и о своей роли в войне против её создателей."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Группа исследователей путешествует через червоточину в космосе в попытке обеспечить выживание человечества."
    },
    {
        "title": "Parasite",
        "title_ru": "Паразиты",
        "year": 2019,
        "description": "Алчность и классовая дискриминация угрожают новой симбиотической связи между богатой семьёй и бедной семьёй."
    }
]

# Маршрут для главной страницы лабораторной работы 7
@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html', films=films)  # Возвращает HTML-страницу с информацией о фильмах

# API: Получение списка всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films  # Возвращает список всех фильмов в формате JSON

# API: Получение информации о конкретном фильме по ID
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):  # Проверка, существует ли фильм с указанным ID
        return {"error": "Фильм с указанным ID не найден"}, 404  # Возвращает ошибку, если ID некорректен
    return films[id]  # Возвращает информацию о фильме с указанным ID

# API: Удаление фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):  # Проверка, существует ли фильм с указанным ID
        return {"error": "Фильм с указанным ID не найден"}, 404  # Возвращает ошибку, если ID некорректен
    
    del films[id]  # Удаляет фильм из списка по ID
    return '', 204  # Возвращает успешный ответ без содержимого

# API: Валидация данных фильма
def validate_film(film):
    errors = {}  # Словарь для хранения ошибок валидации
    current_year = datetime.now().year  # Получаем текущий год

    # Проверка русскоязычного названия
    if not film.get('title_ru', '').strip():  # Если русское название пустое или отсутствует
        errors['title_ru'] = 'Русское название обязательно для заполнения.'

    # Проверка оригинального названия
    if not film.get('title', '').strip() and not film.get('title_ru', '').strip():  # Если оба названия пусты
        errors['title'] = 'Название на оригинальном языке обязательно, если русское название пустое.'

    # Проверка года
    try:
        year = int(film.get('year', 0))  # Преобразуем год в число
        if year < 1895 or year > current_year:  # Год должен быть в диапазоне от 1895 до текущего
            errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}.'
    except ValueError:  # Обрабатываем случай, если год не является числом
        errors['year'] = 'Год должен быть числом.'

    # Проверка описания
    description = film.get('description', '')  # Получаем описание фильма
    if not description.strip():  # Если описание пустое
        errors['description'] = 'Описание обязательно для заполнения.'
    elif len(description) > 2000:  # Если длина описания превышает 2000 символов
        errors['description'] = 'Описание не должно превышать 2000 символов.'

    return errors  # Возвращаем словарь с ошибками

# API: Обновление информации о фильме по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):  # Проверка, существует ли фильм с указанным ID
        return {"error": "Фильм с указанным ID не найден"}, 404

    film = request.get_json()  # Получаем данные фильма из запроса

    # Если оригинальное название пустое, заполняем его русским названием
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']

    # Выполняем валидацию
    errors = validate_film(film)  # Проверяем данные фильма на корректность
    if errors:
        return errors, 400  # Возвращаем ошибки валидации, если они есть

    films[id] = film  # Обновляем данные фильма
    return films[id]

# API: Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()  # Получаем данные нового фильма из запроса

    # Если оригинальное название пустое, заполняем его русским названием
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']

    # Выполняем валидацию
    errors = validate_film(film)  # Проверяем данные фильма на корректность
    if errors:
        return errors, 400  # Возвращаем ошибки валидации, если они есть

    films.append(film)  # Добавляем новый фильм в список
    return films[-1], 201  # Возвращаем добавленный фильм и статус 201 (Created)
