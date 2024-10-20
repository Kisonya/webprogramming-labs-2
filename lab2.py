from flask import Blueprint, url_for, redirect, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/a/')
def a():
    return 'ok'

@lab2.route('/lab2/a')
def a2():
    return 'ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']  # Список доступных цветов

@lab2.route('/lab2/add_flower/')
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name=None):
    if not name:
        return "400: Вы не задали имя цветка", 400  # Возвращаем ошибку 400, если имя не указано
    flower_list.append(name)
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Добавлен новый цветок</h1>
            <p>Название нового цветка: {name}</p>
            <p>Всего цветов: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
        </body>
    </html>
    '''

@lab2.route('/lab2/show_flowers')
def show_flowers():
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Список всех цветов</h1>
            <p>Всего цветов: {len(flower_list)}</p>
            <ul>
                {''.join(f'<li>{flower}</li>' for flower in flower_list)}
            </ul>
            <a href="/lab2/clear_flowers">Очистить список цветов</a>
        </body>
    </html>
    '''

@lab2.route('/lab2/flowers/<int:flower_id>')  # Маршрут, принимающий числовой идентификатор цветка
def flowers(flower_id):
    if flower_id >= len(flower_list):  # Проверяем, если идентификатор превышает длину списка
        return '''
        <!doctype html>
        <html>
            <body>
                <h1>Ошибка</h1>
                <p>Такого цветка нет</p>
                <a href="/lab2/show_flowers">Посмотреть все цветы</a>
            </body>
        </html>
        ''', 404
    else:
        return f'''
        <!doctype html>
        <html>
            <body>
                <h1>Информация о цветке</h1>
                <p>Цветок: {flower_list[flower_id]}</p>
                <a href="/lab2/show_flowers">Посмотреть все цветы</a>
            </body>
        </html>
        '''

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()  # Очищаем список
    return '''
    <!doctype html>
    <html>
        <body>
            <h1>Список цветов очищен</h1>
            <a href="/lab2/show_flowers">Посмотреть все цветы</a>
        </body>
    </html>
    '''

@lab2.route('/lab2/example')  # Маршрут для страницы с примером
def example():
    name, lab_num, group, course = 'Иван Иванов', 2, 'ФБИ-00', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template(
        'example.html', 
        name=name, 
        lab_num=lab_num, 
        group=group, 
        course=course, 
        fruits=fruits
    )


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
    <!doctype html>
    <html>
        <body>
            <h1>Расчёт с параметрами:</h1>
            <ul>
                <li>{a} + {b} = {a + b}</li>
                <li>{a} - {b} = {a - b}</li>
                <li>{a} * {b} = {a * b}</li>
                <li>{a} / {b} = {a / b if b != 0 else "∞ (деление на ноль)"}</li>
                <li>{a} ^ {b} = {a ** b}</li>
            </ul>
            <a href="/lab2/calc">Вернуться к калькулятору по умолчанию</a>
        </body>
    </html>
    '''

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

books = [
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225},
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Фантастика', 'pages': 480},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 316},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Роман', 'pages': 352},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Поэма', 'pages': 240},
    {'author': 'Антон Чехов', 'title': 'Вишнёвый сад', 'genre': 'Пьеса', 'pages': 154},
    {'author': 'Максим Горький', 'title': 'На дне', 'genre': 'Пьеса', 'pages': 160},
    {'author': 'Борис Пастернак', 'title': 'Доктор Живаго', 'genre': 'Роман', 'pages': 592},
    {'author': 'Владимир Набоков', 'title': 'Лолита', 'genre': 'Роман', 'pages': 336}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

cats = [
    {'name': 'Барсик', 'description': 'Ленивый котик, который любит спать целый день.', 'image': 'static/cat1.jpg'},
    {'name': 'Мурзик', 'description': 'Очень активный и любит играть с игрушками.', 'image': 'static/cat2.jpg'},
    {'name': 'Снежок', 'description': 'Белоснежный котик с мягкой шерстью.', 'image': 'static/cat3.jpg'},
    {'name': 'Рыжик', 'description': 'Забавный рыжий кот, обожает бегать за мышкой.', 'image': 'static/cat4.jpg'},
    {'name': 'Черныш', 'description': 'Серьёзный и важный кот, всегда сохраняет спокойствие.', 'image': 'static/cat5.jpg'}
]

@lab2.route('/lab2/cats')
def show_cats():
    return render_template('cats.html', cats=cats)
