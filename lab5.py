from flask import Blueprint, render_template

lab5 = Blueprint('lab5', __name__)

# Заготовки маршрутов
@lab5.route('/lab5/')
def index():
    user = "anonymous"  # Имя пользователя (по умолчанию anonymous)
    return render_template('lab5/lab5.html', user=user)

@lab5.route('/lab5/login')
def login():
    return render_template('lab5/login.html')

@lab5.route('/lab5/register')
def register():
    return render_template('lab5/register.html')

@lab5.route('/lab5/list')
def list_articles():
    return render_template('lab5/list.html')

@lab5.route('/lab5/create')
def create_article():
    return render_template('lab5/create.html')
