from flask import Blueprint, render_template, request, session

lab9 = Blueprint('lab9', __name__)

# Глобальная переменная для хранения данных между шагами
user_data = {}

@lab9.route('/lab9/', methods=['GET', 'POST'])
def step1_name():
    if request.method == 'POST':
        session['name'] = request.form.get('name')  # Сохраняем имя в session
        return render_template('lab9/age.html')
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age', methods=['POST'])
def step2_age():
    session['age'] = int(request.form.get('age'))  # Сохраняем возраст в session
    return render_template('lab9/gender.html')

@lab9.route('/lab9/gender', methods=['POST'])
def step3_gender():
    session['gender'] = request.form.get('gender')  # Сохраняем пол в session
    return render_template('lab9/interest.html')

@lab9.route('/lab9/interest', methods=['POST'])
def step4_interest():
    session['interest'] = request.form.get('interest')  # Сохраняем интерес в session
    if session['interest'] == 'vkusnoe':
        return render_template('lab9/vkusnoe_choice.html')
    else:
        return render_template('lab9/krasivoe_choice.html')

@lab9.route('/lab9/result', methods=['POST'])
def step5_result():
    session['final_choice'] = request.form.get('final_choice')  # Сохраняем выбор в session

    # Чтение данных из session
    name = session.get('name', 'Гость')
    age = session.get('age', 0)
    gender = session.get('gender', 'male')
    interest = session.get('interest', 'unknown')
    final_choice = session.get('final_choice', 'unknown')

    # Определяем тип получателя
    is_child = age < 14  # Если младше 14 лет, считаем ребенком

    # Генерация подарка
    if interest == 'vkusnoe':  # Если выбрано "что-то вкусное"
        if final_choice == 'sladkoe':  # Если выбрано "сладкое"
            if is_child:
                gift = 'мешочек конфет'
                image = 'sweets.jpg'
            else:
                gift = 'коробка элитных шоколадных конфет'
                image = 'luxury_chocolates.jpg'
        else:  # Если выбрано "сытное"
            if is_child:
                gift = 'вкусный торт'
                image = 'cake.jpg'
            else:
                gift = 'праздничный пирог'
                image = 'pie.jpg'
    else:  # Если выбрано "что-то красивое"
        if final_choice == 'krasivoe':  # Если выбрано "красивое"
            if is_child:
                gift = 'яркая игрушка'
                image = 'toy.jpg'
            else:
                gift = 'букет из роз'
                image = 'roses.jpg'
        else:  # Если выбрано "оригинальное"
            if is_child:
                gift = 'интересная картина'
                image = 'painting.jpg'
            else:
                gift = 'картина известного художника'
                image = 'artwork.jpg'

    # Генерация поздравления
    if gender == 'male':
        if is_child:
            message = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным и счастливым! Вот тебе подарок — {gift}."
        else:
            message = f"Поздравляю вас, {name}, желаю успехов, здоровья и счастья! Вот вам подарок — {gift}."
    else:
        if is_child:
            message = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной и счастливой! Вот тебе подарок — {gift}."
        else:
            message = f"Поздравляю вас, {name}, желаю успехов, здоровья и счастья! Вот вам подарок — {gift}."

    return render_template('lab9/result.html', message=message, image=image)
