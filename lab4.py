from flask import Blueprint, render_template, request, redirect, url_for, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    elif int(x2) == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/add-form', methods=['GET'])
def add_form():
    return render_template('lab4/add-form.html')

@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0
    result = int(x1) + int(x2)
    return render_template('lab4/add-form.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/multiply-form', methods=['GET'])
def multiply_form():
    return render_template('lab4/multiply-form.html')

@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1
    result = int(x1) * int(x2)
    return render_template('lab4/multiply-form.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/subtract-form', methods=['GET'])
def subtract_form():
    return render_template('lab4/subtract-form.html')

@lab4.route('/lab4/subtract', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract-form.html', error='Оба поля должны быть заполнены!')
    result = int(x1) - int(x2)
    return render_template('lab4/subtract-form.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/power-form', methods=['GET'])
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/power-form.html', error='Оба поля должны быть заполнены!')
    if int(x1) == 0 and int(x2) == 0:
        return render_template('lab4/power-form.html', error='Оба поля не могут быть равны нулю для операции возведения в степень!')
    result = int(x1) ** int(x2)
    return render_template('lab4/power-form.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect(url_for('lab4.tree'))


# Список пользователей
users = [
    {'login': 'sonya', 'password': '2006', 'name': 'Софья Скобель', 'gender': 'female'},
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    {'login': 'alice', 'password': '789', 'name': 'Алиса Петрова', 'gender': 'female'},
    {'login': 'charlie', 'password': '456', 'name': 'Чарли Браун', 'gender': 'male'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_name = session.get('name')
        else:
            authorized = False
            user_name = ''
        return render_template('lab4/login.html', authorized=authorized, user_name=user_name)

    login = request.form.get('login')
    password = request.form.get('password')
    error = None

    # Проверка на пустые поля
    if not login:
        error = 'Не введён логин'
    elif not password:
        error = 'Не введён пароль'
    else:
        # Проверка логина и пароля по списку пользователей
        for user in users:
            if login == user['login'] and password == user['password']:
                session['login'] = login
                session['name'] = user['name']  # Сохраняем имя пользователя в сессии
                return redirect(url_for('lab4.login'))

        # Если логин или пароль неверны
        error = 'Неверные логин и/или пароль'

    return render_template('lab4/login.html', error=error, authorized=False, login=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)  # Удаляем логин из сессии
    return redirect(url_for('lab4.login'))


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    error = None
    temperature = request.form.get('temperature')
    message = ''
    snowflakes = ''

    if request.method == 'POST':
        try:
            temperature = int(temperature)
            if temperature < -12:
                message = 'Не удалось установить температуру — слишком низкое значение'
            elif temperature > -1:
                message = 'Не удалось установить температуру — слишком высокое значение'
            elif -12 <= temperature <= -9:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️❄️❄️'  # Три снежинки
            elif -8 <= temperature <= -5:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️❄️'  # Две снежинки
            elif -4 <= temperature <= -1:
                message = f'Установлена температура: {temperature}°С'
                snowflakes = '❄️'  # Одна снежинка
        except ValueError:
            error = 'Ошибка: не задана температура'

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, error=error)


@lab4.route('/lab4/grain-order', methods=['GET', 'POST'])
def grain_order():
    prices = {
        'ячмень': 12345,
        'овёс': 8522,
        'пшеница': 8722,
        'рожь': 14111
    }

    message = ''
    error = None
    discount_info = None

    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')

        # Проверка на наличие веса и его корректность
        try:
            weight = float(weight)
            if weight <= 0:
                error = 'Ошибка: вес должен быть больше 0.'
            elif weight > 500:
                error = 'Ошибка: такого объёма сейчас нет в наличии.'
            else:
                # Расчёт стоимости
                price_per_ton = prices.get(grain_type)
                total_cost = weight * price_per_ton

                # Применение скидки
                if weight > 50:
                    discount = 0.1  # Скидка 10%
                    discount_amount = total_cost * discount
                    total_cost -= discount_amount
                    discount_info = f'Применена скидка за большой объём: 10% (скидка составила {discount_amount:.2f} руб)'

                # Сообщение об успешном заказе
                message = (f'Заказ успешно сформирован. Вы заказали {grain_type}. '
                           f'Вес: {weight} т. Сумма к оплате: {total_cost:.2f} руб.')
        except ValueError:
            error = 'Ошибка: вес должен быть указан и быть числом.'

    return render_template('lab4/grain_order.html', prices=prices, message=message, error=error, discount_info=discount_info)
