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
        </html>"""

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
    return """<!doctype html>
        <html>
           <body>
               <h1>Дуб</h1>
               <img src=" """ + path + """ ">
           </body>
        </html>"""

count = 0
@app.route ('/lab1/counter') #добавляем еще 1 декоратор-роут,чтобы ф-я срабатывала на разные адреса
def counter():
    global count
    count += 1
    return """<!doctype html>
        <html>
           <body>
               Сколько раз вы сюда заходили: """ + str(count) + """
           </body>
        </html>"""

@app.route("/info")
def info():
    return redirect("/author")
