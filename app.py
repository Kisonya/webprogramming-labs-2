from flask import Flask
app = Flask (__name__) #создаем объект

@app.route ("/") #указываем путь
def start():
    return "<!doctype html>" \
        "<html>" \
        "   <body>" \
        "       <h1>web-сервер на flask</h1>" \
        "   </body>" \
        "</html>"
