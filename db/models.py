from . import db  # Импортируем объект SQLAlchemy

# Модель таблицы пользователей
class users(db.Model):
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
