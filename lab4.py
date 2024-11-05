from flask import Blueprint, render_template, request
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    elif int(x2) == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/add-form', methods=['POST'])
def add():
    x1 = request.form.get('x1') or 0  # Если поле пустое, принимаем его как 0
    x2 = request.form.get('x2') or 0
    result = int(x1) + int(x2)
    return render_template('lab4/add.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1') or 1  # Если поле пустое, принимаем его как 1
    x2 = request.form.get('x2') or 1
    result = int(x1) * int(x2)
    return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/subtract', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract.html', error='Оба поля должны быть заполнены!')
    result = int(x1) - int(x2)
    return render_template('lab4/subtract.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/power.html', error='Оба поля должны быть заполнены!')
    if int(x1) == 0 and int(x2) == 0:
        return render_template('lab4/power.html', error='Оба поля не могут быть равны нулю для операции возведения в степень!')
    result = int(x1) ** int(x2)
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)
