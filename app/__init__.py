# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from celery import Celery
from config import Config

# アプリケーションインスタンスの作成
app = Flask(__name__)

# config.pyのConfigクラスから設定を読み込む
app.config.from_object(Config)

# データベースインスタンスの作成
db = SQLAlchemy(app)

# メールインスタンスの作成
mail = Mail(app)

# ログイン管理インスタンスの作成
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Celeryインスタンスの作成
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Blueprintの登録
from app.main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# モデルのインポート
from app import models
