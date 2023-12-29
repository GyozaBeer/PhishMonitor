# app/user.py
from flask import Blueprint, render_template

user = Blueprint('user', __name__)

@user.route('/')
def index():
    return render_template('index.html')
