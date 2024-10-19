from flask import Flask, url_for, redirect, url_for, render_template
app = Flask(__name__)  # создаем объект

@app.route("/")  # добавляем маршрут для "/"
@app.route("/index")  # добавляем маршрут для "/index"
def index():
    return render_template('index.html')


@app.route("/lab1")  # Маршрут для страницы первой лабораторной
def lab1():
    return """<!doctype html>
        <html>
           <head>
               <title>Лабораторная 1</title> <!-- Заголовок страницы -->
           </head>
           <body>
               <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
               <a href="/">На главную</a> <!-- Ссылка на корень -->
               <h2>Список роутов</h2> <!-- Заголовок h2 -->
               <ul>
                   <li><a href="/">Главная</a></li>
                   <li><a href="/lab1/oak">Страница с дубом</a></li>
                   <li><a href="/lab1/counter">Счетчик посещений</a></li>
                   <li><a href="/lab1/reset_counter">Сбросить счетчик</a></li>
                   <li><a href="/lab1/author">Автор</a></li>
                   <li><a href="/lab1/custom">Путешествия по России</a></li>
                   <li><a href="/error400">Ошибка 400</a></li>
                   <li><a href="/error401">Ошибка 401</a></li>
                   <li><a href="/error402">Ошибка 402</a></li>
                   <li><a href="/error403">Ошибка 403</a></li>
                   <li><a href="/error404">Ошибка 404</a></li>
                   <li><a href="/error405">Ошибка 405</a></li>
                   <li><a href="/error418">Ошибка 418</a></li>
                   <li><a href="/error500">Ошибка 500</a></li>
               </ul>
           </body>
        </html>"""



@app.route("/lab1/web")  # изменяем роут с /web на /lab1/web
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a> <!-- Изменили ссылку -->
           </body>
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/plain; charset=utf-8"
        }

@app.route("/lab1/author")  # изменяем роут с /author на /lab1/author
def author():
    name = "Скобель Софья Валентиновна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p> Студент: """ + name + """</p>
                <p> Группа: """ + group + """</p>
                <p> Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a> <!-- Изменили ссылку -->
            </body>
        </html>"""

@app.route("/lab1/info")  # изменяем роут с /info на /lab1/info
def info():
    return redirect("/lab1/author")  # изменили адрес перенаправления

# Оставшиеся маршруты
@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return """<!doctype html>
        <html>
           <head>
               <link rel="stylesheet" type="text/css" href=" """ + css_path + """ ">
           </head>
           <body>
               <h1>Дуб</h1>
               <img src=" """ + path + """ ">
           </body>
        </html>"""

count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return """<!doctype html>
        <html>
           <body>
               <p>Сколько раз вы сюда заходили: """ + str(count) + """</p>
               <a href="/lab1/reset_counter">Сбросить счетчик</a>
           </body>
        </html>"""

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return """<!doctype html>
        <html>
           <body>
               <p>Счетчик сброшен!</p>
               <a href="/lab1/counter">Назад к счетчику</a>
           </body>
        </html>"""

@app.route('/lab1/created')
def created():
    return """<!doctype html>
        <html>
           <body>
               <h1>Создано успешно</h1>
               <div><i> что-то создано... </i></div>
           </body>
        </html>"""

@app.errorhandler(404)
def not_found(err):
    return redirect(url_for('error404'))

@app.route("/error404")
def error404(err=None):
    css_path = url_for("static", filename="error.css")
    img_path = url_for("static", filename="404_image.jpg")
    return """<!doctype html>
        <html>
           <head>
               <title>Страница не найдена</title>
               <link rel="stylesheet" type="text/css" href=" """ + css_path + """ ">
           </head>
           <body>
               <div class="error-container">
                   <h1>Ой! Что-то пошло не так...</h1>
                   <p>Похоже, вы заблудились. Но не волнуйтесь, мы вас вернем на правильный путь.</p>
                   <img src=" """ + img_path + """ " alt="404 image" class="error-img">
                   <p><a href="/">Вернуться на главную страницу</a></p>
               </div>
           </body>
        </html>""", 404

# Страница с кодом 400
@app.route("/error400")
def error400():
    return "400: Bad Request — сервер не может обработать запрос из-за синтаксической ошибки.", 400

# Страница с кодом 401
@app.route("/error401")
def error401():
    return "401: Unauthorized — для доступа к ресурсу требуется аутентификация.", 401

# Страница с кодом 402
@app.route("/error402")
def error402():
    return "402: Payment Required — требуется оплата для доступа к ресурсу (зарезервирован для будущего использования).", 402

# Страница с кодом 403
@app.route("/error403")
def error403():
    return "403: Forbidden — доступ к ресурсу запрещён.", 403

# Страница с кодом 405
@app.route("/error405")
def error405():
    return "405: Method Not Allowed — метод запроса не поддерживается для данного ресурса.", 405

# Страница с кодом 418
@app.route("/error418")
def error418():
    return "418: I'm a teapot — я чайник. Шутливый код, указанный в RFC 2324.", 418

@app.route("/error500")  # Маршрут для теста ошибки 500
def error500():
    # Создаем ошибку делением на ноль
    return 1 / 0

@app.errorhandler(500)
def internal_error(err):
    return """<!doctype html>
        <html>
           <head>
               <title>Ошибка сервера</title>
           </head>
           <body>
               <h1>500: Внутренняя ошибка сервера</h1>
               <p>Произошла непредвиденная ошибка. Мы уже работаем над её исправлением.</p>
               <p><a href="/">Вернуться на главную страницу</a></p>
           </body>
        </html>""", 500

@app.route("/lab1/custom")  # Новый роут на выбор студента
def custom():
    # Указываем путь к изображению
    img_path = url_for("static", filename="9.jpg")
    
    # HTML-контент с текстом и картинкой
    content = """
    <!doctype html>
    <html>
        <head>
            <title>Путешествия по России</title>
        </head>
        <body>
            <h1>Путешествия по России: самые интересные места</h1>
            <p>Россия — это страна с огромной территорией и разнообразием ландшафтов. От широких степей до заснеженных гор, от современных мегаполисов до удалённых деревень — путешествия по России могут быть удивительными и непредсказуемыми. В каждом регионе можно найти уникальные места, которые поразят своей природой или архитектурой.</p>
            <p>Одно из самых популярных направлений для путешествий — Золотое кольцо России. Этот маршрут включает в себя несколько древних городов, которые сохранили свою историческую ценность. В них можно увидеть старинные монастыри, церкви и кремли, которые переносят нас в прошлое России.</p>
            <p>Ещё одно уникальное место — озеро Байкал. Это самое глубокое озеро в мире, и его кристально чистая вода привлекает туристов со всего мира. Окрестности Байкала изобилуют красивыми ландшафтами и уникальной флорой и фауной. Это место обязательно стоит посетить для тех, кто любит природу и активный отдых.</p>
            <img src="{}" alt="Пейзаж России" style="width: 300px; height: auto;">
        </body>
    </html>
    """.format(img_path)

    # Возвращаем HTML-контент с заголовками
    return content, 200, {
        "Content-Language": "ru",  # Указываем язык контента
        "X-Custom-Header-1": "Student-Custom-Value1",  # Нестандартный заголовок 1
        "X-Custom-Header-2": "Student-Custom-Value2"   # Нестандартный заголовок 2
    }

#   ВТОРАЯ ЛАБОРАТОРНАЯ РАБОТА!!!!!!!!!!!!

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/a/')
def a():
    return 'ok'

@app.route('/lab2/a')
def a2():
    return 'ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']  # Список доступных цветов

@app.route('/lab2/add_flower/')
@app.route('/lab2/add_flower/<name>')
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

@app.route('/lab2/show_flowers')
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

@app.route('/lab2/flowers/<int:flower_id>')  # Маршрут, принимающий числовой идентификатор цветка
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

@app.route('/lab2/clear_flowers')
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

@app.route('/lab2/example')  # Маршрут для страницы с примером
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


@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
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

@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
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

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

cats = [
    {'name': 'Барсик', 'description': 'Ленивый котик, который любит спать целый день.', 'image': 'static/cat1.jpg'},
    {'name': 'Мурзик', 'description': 'Очень активный и любит играть с игрушками.', 'image': 'static/cat2.jpg'},
    {'name': 'Снежок', 'description': 'Белоснежный котик с мягкой шерстью.', 'image': 'static/cat3.jpg'},
    {'name': 'Рыжик', 'description': 'Забавный рыжий кот, обожает бегать за мышкой.', 'image': 'static/cat4.jpg'},
    {'name': 'Черныш', 'description': 'Серьёзный и важный кот, всегда сохраняет спокойствие.', 'image': 'static/cat5.jpg'}
]

@app.route('/lab2/cats')
def show_cats():
    return render_template('cats.html', cats=cats)
