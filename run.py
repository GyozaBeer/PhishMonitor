# run.py
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import os
from flask_login import logout_user

app = create_app()

def create_admin_user(app):
    with app.app_context():
        if not User.query.filter_by(email='admin@example.com').first():
            admin_user = User(
                username='admin',
                email='admin@admin.com',
                password_hash=generate_password_hash('password'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            #logout_user()

if __name__ == "__main__":
    with app.app_context():
        # データベーススキーマの初期化
        db.create_all()

    # Flaskアプリケーションを実行する
    if os.environ.get('FLASK_ENV') == 'development':
     create_admin_user(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
