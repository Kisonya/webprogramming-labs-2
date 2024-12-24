from . import db  # Импортируем объект SQLAlchemy
from flask_login import UserMixin

# Модель таблицы пользователей
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный ID пользователя
    login = db.Column(db.String(30), nullable=False, unique=True)  # Логин пользователя (уникальный)
    password = db.Column(db.String(162), nullable=False)  # Хэш пароля (обязательное поле)

# Модель таблицы статей
class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный ID статьи
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Внешний ключ (ссылка на пользователя)
    title = db.Column(db.String(50), nullable=False)  # Заголовок статьи
    article_text = db.Column(db.Text, nullable=False)  # Текст статьи
    is_favorite = db.Column(db.Boolean)  # Флаг "Избранная статья"
    is_public = db.Column(db.Boolean)  # Флаг "Публичная статья"
    likes = db.Column(db.Integer)  # Количество лайков статьи

# Модель таблицы пользователей для РГЗ
class rgz_users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Модель таблицы книг для РГЗ
class rgz_books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey('rgz_users.id'), nullable=False)