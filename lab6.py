from flask import Blueprint, render_template

# Создание Blueprint для работы с маршрутом "lab5"
lab6 = Blueprint('lab6', __name__)

# Главная страница приложения
@lab6.route('/lab5/')
def main():
    return render_template('lab6/lab6.html')