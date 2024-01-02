# app/main.py
from datetime import datetime, timedelta
from flask import current_app as app  # appインスタンスのインポート
from flask import Blueprint, render_template, jsonify, request, flash,redirect,url_for
from flask_login import login_required, current_user  
from utils import nrd_downloader, db_importer
from app.models import NRD

main = Blueprint('main', __name__)

@main.route('/')
def index():
    app.logger.info("index.html requested")
    # 初期アクセス時には検索されていないとみなす
    return render_template('index.html', nrds=[], searched=False)

@main.route('/download_nrd', methods=['POST'])
@login_required
def download_nrd():
    # NRDダウンロードの処理をここに実装
    success = nrd_downloader.download_and_store_nrd()  
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error"}), 500

@main.route('/store_db', methods=['POST'])
@login_required
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

@main.route('/search_results')
def search_results():
    keyword = request.args.get('keyword')  # GETリクエストからキーワードを取得
    searched = False
    nrds = []

    if keyword:
        searched = True
        # 検索結果を10件に制限
        nrds = NRD.query.filter(NRD.domain_name.contains(keyword)).limit(10).all()

    return render_template('index.html', nrds=nrds, searched=searched)

@main.route('/dashboard')
@main.route('/dashboard/<active_tab>')
@login_required
def dashboard(active_tab='monitor'):
    # active_tab の値に応じて処理を分岐
    if active_tab == 'monitor':
        # NRD監視の処理
        user = current_user
        monitored_nrds = user.nrds  # ユーザーの監視リストを取得
        search_results = []  # 検索結果は空
    elif active_tab == 'search':
        # NRD検索＆登録の処理
        keyword = request.args.get('keyword')
        if keyword:
            search_results = NRD.query.filter(NRD.domain_name.contains(keyword)).limit(10).all()
        else:
            search_results = []  # キーワードがない場合は空のリスト
        monitored_nrds = []  # 監視リストは空
    else:
        # 不正なタブが指定された場合はデフォルト（NRD監視）を表示
        active_tab = 'monitor'
        user = current_user
        monitored_nrds = user.nrds
        search_results = []  # 検索結果は空

    return render_template('dashboard.html', 
                           active_tab=active_tab, 
                           monitored_nrds=monitored_nrds,
                           search_results=search_results)


@main.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    nrd_id = request.form.get('nrd_id')
    nrd = NRD.query.get(nrd_id)
    if nrd:
        current_user.add_nrd_to_watchlist(nrd)
        return jsonify({'status': 'success', 'message': 'NRDを監視リストに追加しました。'})
    else:
        return jsonify({'status': 'error', 'message': 'NRDが見つかりませんでした。'})
