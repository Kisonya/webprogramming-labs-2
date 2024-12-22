from flask import Blueprint, render_template, request

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
    user_data['final_choice'] = request.form.get('final_choice')

    # Генерация поздравления
    name = user_data['name']
    age = user_data['age']
    gender = user_data['gender']
    interest = user_data['interest']
    final_choice = user_data['final_choice']

    if gender == 'male':
        pronoun = 'ты'
        ending = 'лся'
    else:
        pronoun = 'ты'
        ending = 'лась'

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

    message = f"Поздравляю тебя, {name}, желаю, чтобы {pronoun} быстро вырос{ending}, был умным и счастливым! Вот тебе подарок — {gift}."
    return render_template('lab9/result.html', message=message, image=image)
