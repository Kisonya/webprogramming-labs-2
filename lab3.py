from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'Аноним')  # Если cookie 'name' не установлено, подставляем 'Аноним'
    age = request.cookies.get('age', 'Неизвестен')  # Если cookie 'age' не установлено, подставляем 'Неизвестен'
    name_color = request.cookies.get('name_color', 'black')  # Цвет по умолчанию, если не установлен
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response('Установка cookie', 200)
    resp.set_cookie('name', 'Sofia')
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'red')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('color')  # Исправлено название cookie
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors ={}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age', '')
    if not age:
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    # Цены за напитки
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70  # Зеленый чай

    # Добавки
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    # Получаем параметры стилей из запроса
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')

    # Если параметры переданы, устанавливаем их в куки
    if color or bg_color or font_size:
        resp = make_response(redirect('/lab3/settings'))

        if color:
            resp.set_cookie('color', color)  # Устанавливаем цвет текста в куки
        if bg_color:
            resp.set_cookie('bg_color', bg_color)  # Устанавливаем цвет фона в куки
        if font_size:
            resp.set_cookie('font_size', font_size)  # Устанавливаем размер шрифта в куки

        return resp  # Возвращаем ответ

    # Если параметры не переданы, получаем их из куки
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size))
    return resp  # Возвращаем страницу настроек с установленными стилями