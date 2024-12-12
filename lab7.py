from flask import Blueprint, render_template

lab7 = Blueprint('lab7', __name__)

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
        "description": "Алчность и классовая дискриминация угрожают новой симбиотической связи между богатой семьей и бедной семьёй."
    }
]

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


@lab7.route('/lab7/rest-api/films/del/<int:id>', methods=['DELETE'])
def del_film(id):
    # Проверяем, находится ли id в корректном диапазоне
    if id < 0 or id >= len(films):
        return {"error": "Фильм с указанным ID не найден"}, 404
    
    # Удаляем фильм с указанным ID
    del films[id]
    return '', 204

