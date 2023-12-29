# app/main.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/profile')
def profile():
    return render_template('profile.html')  # profile.html テンプレートを用意する必要がある
