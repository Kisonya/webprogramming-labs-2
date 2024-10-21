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


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        # Получаем данные формы
        fio = request.form.get('fio')
        polka = request.form.get('polka')
        with_bed = request.form.get('with_bed') == 'on'
        with_baggage = request.form.get('with_baggage') == 'on'
        age = int(request.form.get('age', 0))
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        travel_date = request.form.get('travel_date')
        insurance = request.form.get('insurance') == 'on'

        # Проверяем возраст
        if age < 1 or age > 120:
            return "Ошибка: возраст должен быть от 1 до 120 лет.", 400

        # Рассчитываем стоимость
        if age < 18:
            ticket_type = 'Детский билет'
            price = 700  # Детский билет
        else:
            ticket_type = 'Взрослый билет'
            price = 1000  # Взрослый билет

        # Увеличиваем стоимость в зависимости от выбора полки
        if polka in ['нижняя', 'нижняя боковая']:
            price += 100

        # Увеличиваем стоимость за бельё
        if with_bed:
            price += 75

        # Увеличиваем стоимость за багаж
        if with_baggage:
            price += 250

        # Увеличиваем стоимость за страховку
        if insurance:
            price += 150

        # Возвращаем страницу с билетом
        return render_template('lab3/ticket.html', 
                               fio=fio, polka=polka, with_bed=with_bed, 
                               with_baggage=with_baggage, age=age, 
                               departure=departure, destination=destination, 
                               travel_date=travel_date, insurance=insurance, 
                               ticket_type=ticket_type, price=price)

    # Если GET-запрос, рендерим форму
    return render_template('lab3/ticket_form.html')