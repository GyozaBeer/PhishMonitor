# app/main.py
from datetime import datetime, timedelta
from flask import current_app as app  # appインスタンスのインポート
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user  
from utils import nrd_downloader, db_importer
from app.models import NRD

main = Blueprint('main', __name__)

@main.route('/')
def index():
    app.logger.info("index.html requested")
    # データベースからNRDデータを取得
    try:
        nrds = NRD.query.order_by(NRD.registration_date.desc()).limit(10).all()
        app.logger.info(f"Retrieved {len(nrds)} NRD records")
    except Exception as e:
        app.logger.error(f"Error retrieving NRD records: {e}")
        nrds = []

    # index.html テンプレートにデータを渡す
    return render_template('index.html', nrds=nrds)

@main.route('/download_nrd', methods=['POST'])
#@login_required
def download_nrd():
    # NRDダウンロードの処理をここに実装
    success = nrd_downloader.download_and_store_nrd()  
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"}), 500

@main.route('/store_db', methods=['POST'])
def store_db():
    # 現在の日付から遡って3日分の日付を計算
    dates_to_import = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(2, 5)]

    success = True
    for date_str in dates_to_import:
        if not db_importer.import_nrd_to_db(date_str):
            success = False
            break

    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"}), 500

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)
