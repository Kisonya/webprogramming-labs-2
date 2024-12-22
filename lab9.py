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
                if gender == 'male':
                    gift = 'мешочек конфет с игрушкой-сюрпризом'
                    image = 'sweets_toy.jpg'
                else:
                    gift = 'набор сладостей и брошка'
                    image = 'sweets_brooch.jpg'
            else:
                if gender == 'male':
                    gift = 'набор премиальных шоколадных батончиков'
                    image = 'luxury_choco_set.jpg'
                else:
                    gift = 'фруктовая корзина с шоколадом'
                    image = 'fruit_choco_basket.jpg'
        else:  # Если выбрано "сытное"
            if is_child:
                if gender == 'male':
                    gift = 'набор мини-бургеров'
                    image = 'mini_burgers.jpg'
                else:
                    gift = 'детская пицца с забавным дизайном'
                    image = 'kids_pizza.jpg'
            else:
                if gender == 'male':
                    gift = 'стейк с ароматными специями'
                    image = 'steak.jpg'
                else:
                    gift = 'праздничный сет суши'
                    image = 'sushi_set.jpg'
    else:  # Если выбрано "что-то красивое"
        if final_choice == 'krasivoe':  # Если выбрано "красивое"
            if is_child:
                if gender == 'male':
                    gift = 'набор для создания моделей машин'
                    image = 'car_model_kit.jpg'
                else:
                    gift = 'набор для плетения браслетов'
                    image = 'bracelet_kit.jpg'
            else:
                if gender == 'male':
                    gift = 'элегантный настольный органайзер'
                    image = 'desk_organizer.jpg'
                else:
                    gift = 'набор дизайнерской косметики'
                    image = 'makeup_set.jpg'
        else:  # Если выбрано "оригинальное"
            if is_child:
                if gender == 'male':
                    gift = 'конструктор с подсветкой'
                    image = 'light_constructor.jpg'
                else:
                    gift = 'набор для создания кукольного домика'
                    image = 'dollhouse_kit.jpg'
            else:
                if gender == 'male':
                    gift = 'персонализированный кожаный кошелёк'
                    image = 'leather_wallet.jpg'
                else:
                    gift = 'набор украшений ручной работы'
                    image = 'handmade_jewelry.jpg'

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
