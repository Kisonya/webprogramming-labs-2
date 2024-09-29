from flask import Flask
app = Flask (__name__) #создаем объект

@app.route ("/") #указываем путь
def start():
    return "web-сервер на flask" #возвращает строчку «web-сервер на flask»
