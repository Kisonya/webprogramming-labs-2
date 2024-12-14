from werkzeug.security import generate_password_hash

password = '0620'  # Ваш пароль
hashed_password = generate_password_hash(password)
print(hashed_password)