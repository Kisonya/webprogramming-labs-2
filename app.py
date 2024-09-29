from flask import Flask
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