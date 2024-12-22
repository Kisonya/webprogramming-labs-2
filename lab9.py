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
    age = session.get('age', 'неизвестного возраста')
    gender = session.get('gender', 'male')
    interest = session.get('interest', 'unknown')
    final_choice = session.get('final_choice', 'unknown')

    # Генерация поздравления
    if interest == 'vkusnoe':
        if final_choice == 'sladkoe':
            gift = 'мешочек конфет'
            image = 'sweets.jpg'
        else:
            gift = 'вкусный торт'
            image = 'cake.jpg'
    else:
        if final_choice == 'krasivoe':
            gift = 'красивый букет'
            image = 'flowers.jpg'
        else:
            gift = 'картину'
            image = 'painting.jpg'

    if gender == 'male':
        message = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным и счастливым! Вот тебе подарок — {gift}."
    else:
        message = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной и счастливой! Вот тебе подарок — {gift}."

    return render_template('lab9/result.html', message=message, image=image)
