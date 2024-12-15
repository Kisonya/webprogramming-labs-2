from flask import Blueprint, render_template, request  # Импортируем компоненты Flask
from datetime import datetime  # Импортируем модуль для работы с датой

# Создаём Blueprint для маршрутов лабораторной работы 7
lab7 = Blueprint('lab7', __name__)

# Предопределённый список фильмов с данными о них
films = [
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Вор, который крадёт корпоративные секреты с помощью технологий совместного сна, получает шанс искупить свои преступления, внедрив идею в сознание генерального директора."
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

# Маршрут для отображения страницы
@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html', films=films)

# API: Получение списка всех фильмов
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

# API: Получение информации о конкретном фильме по ID
@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм с указанным ID не найден"}, 404
    return films[id]

# API: Удаление фильма
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм с указанным ID не найден"}, 404
    
    del films[id]
    return '', 204

# API: Валидация данных фильма
def validate_film(film):
    errors = {}
    current_year = datetime.now().year

    # Проверка русскоязычного названия
    if not film.get('title_ru', '').strip():
        errors['title_ru'] = 'Русское название обязательно для заполнения.'

    # Проверка оригинального названия
    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']

    # Проверка года
    try:
        year = int(film.get('year', 0))
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть в диапазоне от 1895 до {current_year}.'
    except ValueError:
        errors['year'] = 'Год должен быть числом.'

    # Проверка описания
    description = film.get('description', '')
    if not description.strip():
        errors['description'] = 'Описание обязательно для заполнения.'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов.'

    return errors

# API: Добавление нового фильма
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    # Устанавливаем оригинальное название, если оно пустое
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    films.append(film)
    return film, 201

# API: Обновление информации о фильме по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм с указанным ID не найден"}, 404

    film = request.get_json()

    # Устанавливаем оригинальное название, если оно пустое
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return errors, 400

    films[id] = film
    return film
