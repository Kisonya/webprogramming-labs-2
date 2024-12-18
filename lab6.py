from flask import Blueprint, render_template, request, session

# Создание Blueprint для работы с маршрутом "lab6"
lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    # Добавляем стоимость аренды для каждого офиса
    price = 900 + (i % 3)
    offices.append({"number": i, "tenant": "", "price": price})

# Главная страница приложения
@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

# Определение маршрута для JSON-RPC API, доступного только через POST запрос
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    # Извлекаем JSON-данные из тела запроса
    data = request.json

    # Извлекаем идентификатор запроса для формирования ответа
    id = data['id']

    # Проверяем, если метод запроса равен "info"
    if data['method'] == 'info':
        # Возвращаем список офисов в формате JSON-RPC
        return {
            'jsonrpc': '2.0',  # Версия протокола JSON-RPC
            'result': offices,  # Результат - список офисов
            'id': id  # ID запроса
        }

    # Проверяем, авторизован ли пользователь
    login = session.get('login')  # Получаем логин из сессии
    if not login:  # Если логина нет, возвращаем ошибку
        return {
            'jsonrpc': '2.0',  # Версия протокола JSON-RPC
            'error': {
                'code': 1,  # Код ошибки "Unauthorized"
                'message': 'Unauthorized'  # Сообщение об ошибке
            },
            'id': id  # ID запроса
        }

    # Обрабатываем метод "booking" (бронирование офиса)
    if data['method'] == 'booking':
        office_number = data['params']  # Получаем номер офиса из параметров запроса
        for office in offices:  # Перебираем список офисов
            if office['number'] == office_number:  # Если найден офис с нужным номером
                if office['tenant'] != '':  # Проверяем, занят ли офис
                    # Возвращаем ошибку, если офис уже забронирован
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,  # Код ошибки "Already booked"
                            'message': 'Already booked'  # Сообщение об ошибке
                        },
                        'id': id  # ID запроса
                    }
                # Если офис свободен, бронируем его за текущим пользователем
                office['tenant'] = login
                # Возвращаем успех бронирования
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # Обрабатываем метод "cancellation" (отмена бронирования)
    if data['method'] == 'cancellation':
        office_number = data['params']  # Получаем номер офиса из параметров запроса
        for office in offices:  # Перебираем список офисов
            if office['number'] == office_number:  # Если найден офис с нужным номером
                if office['tenant'] == '':  # Проверяем, свободен ли офис
                    # Возвращаем ошибку, если офис не был забронирован
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,  # Код ошибки "Office is not booked"
                            'message': 'Office is not booked'  # Сообщение об ошибке
                        },
                        'id': id  # ID запроса
                    }
                if office['tenant'] != login:  # Проверяем, что офис забронирован текущим пользователем
                    # Возвращаем ошибку, если пользователь пытается отменить чужое бронирование
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,  # Код ошибки "Cannot cancel someone else's booking"
                            'message': 'Cannot cancel someone else\'s booking'  # Сообщение об ошибке
                        },
                        'id': id  # ID запроса
                    }
                # Отменяем бронирование, освобождая офис
                office['tenant'] = ''
                # Возвращаем успех отмены бронирования
                return {
                    'jsonrpc': '2.0',
                    'result': 'Booking cancelled successfully',
                    'id': id
                }

    # Если метод запроса не найден, возвращаем ошибку
    return {
        'jsonrpc': '2.0',  # Версия протокола JSON-RPC
        'error': {
            'code': -32601,  # Код ошибки "Method not found"
            'message': 'Method not found'  # Сообщение об ошибке
        },
        'id': id  # ID запроса
    }

