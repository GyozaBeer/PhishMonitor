# run.py
from app import app

# Flaskアプリケーションを実行する
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
