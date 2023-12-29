from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import app, db
from app.models import User, NRD

@app.route('/')
def home():
    return render_template('home.html')  # ホームページのテンプレート

@app.route('/about')
def about():
    return render_template('about.html')  # アバウトページのテンプレート

@app.route('/contact')
def contact():
    return render_template('contact.html')  # コンタクトページのテンプレート

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')  # ユーザープロフィールページのテンプレート

@app.route('/dashboard')
@login_required
def dashboard():
    # ユーザーに関連するNRDデータを取得するロジックをここに実装
    return render_template('dashboard.html')  # ダッシュボードページのテンプレート

# その他のルーティングとビュー関数はここに追加

# RESTful APIのルーティング（今後の開発で実装予定）
# @app.route('/api/v1/resources')
# def api_resources():
#     pass

# エラーハンドリング（例: 404ページ）
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# ... その他のルーティングとビュー関数 ...
