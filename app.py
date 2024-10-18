from flask import Flask, url_for, redirect
app = Flask (__name__) #создаем объект

@app.route ("/") #указываем путь
@app.route ("/web") #добавляем еще 1 декоратор-роут,чтобы ф-я срабатывала на разные адреса
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body> 
        </html>""", 200, {
            "X-Server": "sample",
            "Content-Type": "text/plain; charset=utf-8"
        }

@app.route ("/author")
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
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route ('/lab1/oak') #добавляем еще 1 декоратор-роут,чтобы ф-я срабатывала на разные адреса
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")  # подключаем CSS
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
@app.route('/lab1/counter') # добавляем еще 1 декоратор-роут, чтобы ф-я срабатывала на разные адреса
def counter():
    global count
    count += 1
    return """<!doctype html>
        <html>
           <body>
               <p>Сколько раз вы сюда заходили: """ + str(count) + """</p>
               <a href="/lab1/reset_counter">Сбросить счетчик</a> <!-- Ссылка на сброс счетчика -->
           </body>
        </html>"""

@app.route('/lab1/reset_counter') # новый роут для сброса счетчика
def reset_counter():
    global count
    count = 0
    return """<!doctype html>
        <html>
           <body>
               <p>Счетчик сброшен!</p>
               <a href="/lab1/counter">Назад к счетчику</a> <!-- Ссылка для возврата на страницу счетчика -->
           </body>
        </html>"""

@app.route("/info")
def info():
    return redirect("/author")

@app.route ('/lab1/created') #добавляем еще 1 декоратор-роут,чтобы ф-я срабатывала на разные адреса
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
    return "нет такой страницы", 404