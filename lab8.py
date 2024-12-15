from flask import Blueprint, render_template, session, redirect, url_for

# Создаём Blueprint для лабораторной работы 8
lab8 = Blueprint('lab8', __name__, template_folder='templates')

# Маршрут для главной страницы lab8
@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')

# Маршрут для входа
@lab8.route('/lab8/login')
def login():
    session['login'] = 'User123'  # Временная заглушка для входа
    return redirect(url_for('lab8.main'))

# Маршрут для выхода
@lab8.route('/lab8/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('lab8.main'))

# Маршрут для регистрации
@lab8.route('/lab8/register')
def register():
    return "Страница регистрации"

# Маршрут для списка статей
@lab8.route('/lab8/articles')
def articles():
    return "Список статей"

# Маршрут для создания статьи
@lab8.route('/lab8/create')
def create():
    return "Страница создания статьи"
