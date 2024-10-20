from flask import Blueprint, url_for, redirect, render_template
lab2 = Blueprint('lab3', __name__)

@lab2.route('/lab3/')
def lab():
    return render_template('lab3/lab3.html')
