from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Логин и пароль не должны быть пустыми')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)  # Автоматический логин
    return redirect(url_for('lab8.main'))

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember)
        return redirect(url_for('lab8.main'))
    return render_template('lab8/login.html', error='Неверный логин или пароль')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    articles_list = articles.query.all()
    return render_template('lab8/articles.html', articles=articles_list)

@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_article = articles(title=title, article_text=content, login_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('lab8.article_list'))
    return render_template('lab8/create_article.html')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('lab8.main'))
