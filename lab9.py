from flask import Blueprint, render_template  # Импортируем модули Flask для работы с шаблонами и создания Blueprint

# Создаём Blueprint для маршрутов 9-й лабораторной работы
lab9 = Blueprint('lab9', __name__)

# Маршрут для главной страницы 9-й лабораторной работы
@lab9.route('/lab9/')
def main():
    return render_template('lab9/lab9.html')
