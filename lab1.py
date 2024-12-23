from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")  # Маршрут для страницы первой лабораторной
def lab():
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


@lab1.route("/lab1/web")  # изменяем роут с /web на /lab1/web
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


@lab1.route("/lab1/author")  # изменяем роут с /author на /lab1/author
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


@lab1.route("/lab1/info")  # изменяем роут с /info на /lab1/info
def info():
    return redirect("/lab1/author")  # изменили адрес перенаправления


# Оставшиеся маршруты
@lab1.route('/lab1/oak')
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
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
@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset_counter')
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


@lab1.route('/lab1/created')
def created():
    return """<!doctype html>
        <html>
           <body>
               <h1>Создано успешно</h1>
               <div><i> что-то создано... </i></div>
           </body>
        </html>"""


@lab1.route("/error404")
def error404(err=None):
    css_path = url_for("static", filename="lab1/error.css")
    img_path = url_for("static", filename="lab1/404_image.jpg")
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
@lab1.route("/error400")
def error400():
    return "400: Bad Request — сервер не может обработать запрос из-за синтаксической ошибки.", 400


# Страница с кодом 401
@lab1.route("/error401")
def error401():
    return "401: Unauthorized — для доступа к ресурсу требуется аутентификация.", 401


# Страница с кодом 402
@lab1.route("/error402")
def error402():
    return "402: Payment Required — требуется оплата для доступа к ресурсу (зарезервирован для будущего использования).", 402


# Страница с кодом 403
@lab1.route("/error403")
def error403():
    return "403: Forbidden — доступ к ресурсу запрещён.", 403


# Страница с кодом 405
@lab1.route("/error405")
def error405():
    return "405: Method Not Allowed — метод запроса не поддерживается для данного ресурса.", 405


# Страница с кодом 418
@lab1.route("/error418")
def error418():
    return "418: I'm a teapot — я чайник. Шутливый код, указанный в RFC 2324.", 418


@lab1.route("/error500")  # Маршрут для теста ошибки 500
def error500():
    # Создаем ошибку делением на ноль
    return 1 / 0


@lab1.route("/lab1/custom")  # Новый роут на выбор студента
def custom():
    # Указываем путь к изображению
    img_path = url_for("static", filename="lab1/9.jpg")
    
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