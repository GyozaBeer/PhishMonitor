# run.py
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        # データベーススキーマの初期化
        db.create_all()

    # Flaskアプリケーションを実行する
    app.run(host='0.0.0.0', port=5000, debug=True)