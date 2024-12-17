from flask import Blueprint, render_template, request, redirect  # Основной фреймворк Flask
from werkzeug.security import generate_password_hash 
from db import db
from db.models import users, articles

# Создаём Blueprint для лабораторной работы 8
lab8 = Blueprint('lab8', __name__, template_folder='templates')

# Маршрут для главной страницы lab8
@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


# Маршрут для регистрации
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    # Проверка существования пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    # Хэширование пароля
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    # Добавляем нового пользователя в базу данных
    db.session.add(new_user)
    db.session.commit()

    # Перенаправляем на главную страницу
    return redirect('/lab8/')


