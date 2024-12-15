from sqlalchemy import create_engine

# Параметры подключения
db_name = 'kisonya_orm'      # Название базы данных
db_user = 'kisonya_orm'      # Имя пользователя
db_password = '123'          # Пароль пользователя
host_ip = '127.0.0.1'        # Хост (локальный)
host_port = 5432             # Порт PostgreSQL по умолчанию

# Формируем строку подключения
db_url = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
try:
    # Создаем объект engine
    engine = create_engine(db_url)
    # Открываем соединение
    connection = engine.connect()
    print("Подключение успешно!")
    # Закрываем соединение
    connection.close()
except Exception as e:
    # Если ошибка подключения, выводим сообщение
    print("Ошибка подключения:", e)
