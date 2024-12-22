from flask import Blueprint, render_template, request, session

lab9 = Blueprint('lab9', __name__)

# Глобальная переменная для хранения данных между шагами
user_data = {}

@lab9.route('/lab9/', methods=['GET', 'POST'])
def step1_name():
    if request.method == 'POST':
        user_data['name'] = request.form.get('name')
        return render_template('lab9/age.html')
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age', methods=['POST'])
def step2_age():
    user_data['age'] = int(request.form.get('age'))
    return render_template('lab9/gender.html')

@lab9.route('/lab9/gender', methods=['POST'])
def step3_gender():
    user_data['gender'] = request.form.get('gender')
    return render_template('lab9/interest.html')

@lab9.route('/lab9/interest', methods=['POST'])
def step4_interest():
    user_data['interest'] = request.form.get('interest')
    if user_data['interest'] == 'vkusnoe':
        return render_template('lab9/vkusnoe_choice.html')
    else:
        return render_template('lab9/krasivoe_choice.html')

@lab9.route('/lab9/result', methods=['POST'])
def step5_result():
    # Получаем данные из session
    user_data = session.get('user_data', {})
    user_data['final_choice'] = request.form.get('final_choice')
    session['user_data'] = user_data

    # Генерация поздравления
    name = user_data.get('name', 'Гость')
    age = user_data.get('age', 'неизвестного возраста')
    gender = user_data.get('gender', 'male')  # Значение по умолчанию
    interest = user_data.get('interest', 'unknown')
    final_choice = user_data.get('final_choice', 'unknown')

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
