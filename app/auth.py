#app/auth.py
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.database import db

# 認証関連のルーティング用のBlueprintを作成
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    # ユーザーがログイン済みの場合、プロファイルページにリダイレクト
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # ユーザーが存在しない場合、またはパスワードが間違っている場合
    if not user or not check_password_hash(user.password_hash, password):
        flash('ログインに失敗しました。<br>メールアドレスまたはパスワードが間違っています。')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:  # 既に同じメールアドレスでユーザーが存在する場合
        flash('このメールアドレスは既に使用されています。')
        return redirect(url_for('auth.signup'))   

    new_user = User(email=email, username=username, password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    # サインアップ成功のフラッシュメッセージを追加
    flash('アカウントの作成に成功しました。<br>ログインしてください。', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html')
    else:
        flash('アクセス権限がありません。')
        return redirect(url_for('main.profile'))
