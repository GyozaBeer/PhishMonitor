# app/__init__.py
import logging
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from config import Config
from app.database import db

mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.setLevel(logging.INFO) 

    db.init_app(app)
    mail.init_app(app)

    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Celeryインスタンスの初期化
    from utils.celery_utils import make_celery
    celery = make_celery(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
