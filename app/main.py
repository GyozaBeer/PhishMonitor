# app/main.py
from datetime import datetime, timedelta
from flask import current_app as app  # appインスタンスのインポート
from flask import Blueprint, render_template, jsonify, request, flash,redirect,url_for,current_app,session
from flask_login import login_required, current_user  
from utils import nrd_downloader, db_importer
from app.models import NRD
from app.database import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    app.logger.info("index.html requested")
    
    # ユーザーがログインしている場合、/dashboardにリダイレクト
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # ログインしていない場合、通常通りindex.htmlを表示
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
@main.route('/dashboard/<active_tab>', methods=['GET', 'POST'])
@login_required
def dashboard(active_tab='monitor'):
    keyword = ''  # keyword変数を関数の最初で初期化
    search_results = []  # 検索結果は空
    watched_nrd_ids = []
    monitored_nrds = []
    # active_tab の値に応じて処理を分岐
    if active_tab == 'monitor':
        # NRD監視の処理
        user = current_user
        monitored_nrds = user.nrds  # ユーザーの監視リストを取得
    elif active_tab == 'search':
        # NRD検索＆登録の処理
        if request.method == 'POST':
            keyword = request.form.get('keyword')
            session['last_search_keyword'] = keyword
        else:
            keyword = session.get('last_search_keyword', '')
        
        search_results = NRD.query.filter(NRD.domain_name.contains(keyword)).limit(10).all() if keyword else []
        watched_nrd_ids = [nrd.id for nrd in current_user.nrds]
    else:
        # 不正なタブが指定された場合はデフォルト（NRD監視）を表示
        active_tab = 'monitor'
        user = current_user
        monitored_nrds = user.nrds

    return render_template('dashboard.html', 
                           active_tab=active_tab, 
                           monitored_nrds=monitored_nrds,
                           search_results=search_results,
                           watched_nrd_ids=watched_nrd_ids,
                           last_search_keyword=keyword)


@main.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    nrd_id = request.form.get('nrd_id')
    keyword = request.form.get('keyword')
    current_app.logger.info(f'Received nrd_id: {nrd_id}')
    nrd = NRD.query.get(nrd_id)
    
    if nrd:
        current_app.logger.info(f'NRD found: {nrd.domain_name} with ID {nrd.id}')
        current_user.add_nrd_to_watchlist(nrd)
        db.session.commit()  # データベースに変更をコミット
        flash(f"{nrd.domain_name}を監視リストに追加しました。")
    else:
        current_app.logger.warning('NRD not found')
        flash('NRDが見つかりませんでした。')
    return redirect(url_for('main.dashboard', active_tab='search', keyword=keyword))


@main.route('/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist():
    active_tab = request.form.get('active_tab', 'monitor') # デフォルト値は'monitor'
    app.logger.info(f'active_tab : {active_tab}')
    nrd_id = request.form.get('nrd_id')
    nrd = NRD.query.get(nrd_id)
    if nrd:
        current_user.remove_nrd_from_watchlist(nrd)
        flash(f'{nrd.domain_name}を監視リストから除外しました。', 'info')
    else:
        flash('NRDが見つかりませんでした。', 'error')
    return redirect(url_for('main.dashboard', active_tab=active_tab, keyword=request.form.get('keyword')))

