from flask import Blueprint, render_template, request, redirect, url_for
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

@lab4.route('/lab4/add-form', methods=['GET'])
def add_form():
    return render_template('lab4/add-form.html')

@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0
    result = int(x1) + int(x2)
    return render_template('lab4/add-form.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/multiply-form', methods=['GET'])
def multiply_form():
    return render_template('lab4/multiply-form.html')

@lab4.route('/lab4/multiply', methods=['POST'])
def multiply():
    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1
    result = int(x1) * int(x2)
    return render_template('lab4/multiply-form.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/subtract-form', methods=['GET'])
def subtract_form():
    return render_template('lab4/subtract-form.html')

@lab4.route('/lab4/subtract', methods=['POST'])
def subtract():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract-form.html', error='Оба поля должны быть заполнены!')
    result = int(x1) - int(x2)
    return render_template('lab4/subtract-form.html', x1=x1, x2=x2, result=result)



@lab4.route('/lab4/power-form', methods=['GET'])
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/power-form.html', error='Оба поля должны быть заполнены!')
    if int(x1) == 0 and int(x2) == 0:
        return render_template('lab4/power-form.html', error='Оба поля не могут быть равны нулю для операции возведения в степень!')
    result = int(x1) ** int(x2)
    return render_template('lab4/power-form.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect(url_for('lab4.tree'))


