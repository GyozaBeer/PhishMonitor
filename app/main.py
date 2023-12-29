# app/main.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

# app/auth.py
from flask import Blueprint, render_template

@main.route('/profile')
def profile():
    return render_template('profile.html')
