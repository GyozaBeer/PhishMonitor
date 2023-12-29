# config.py
import os
from dotenv import load_dotenv

# 環境変数ファイルのパスを指定して読み込みます
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flaskの秘密鍵、セキュリティに関わる重要なキーです
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # データベースの接続設定
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Flask-SQLAlchemyイベントシステムを無効にする

    # メールサーバの設定
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == '1'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Celeryの設定
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

    # ファイル処理用ディレクトリ
    FILE_PROCESSING_DIR = os.environ.get('FILE_PROCESSING_DIR')

    # その他の設定はここに追加...

# config.pyの末尾
