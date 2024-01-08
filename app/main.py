# app/main.py
from datetime import datetime, timedelta
from flask import current_app as app  # appインスタンスのインポート
from flask import Blueprint, render_template, jsonify, request, flash,redirect,url_for,current_app,session
from flask_login import login_required, current_user  
from utils import nrd_downloader, db_importer, status_checker
from app.models import NRD
from app.database import db
from flask import jsonify


main = Blueprint('main', __name__)

def filter_keyword(keyword):
    excluded_keywords = {'www', 'co', 'jp', 'com', 'net', 'org'}  # 除外するキーワード
    segments = keyword.split('.')
    # 右側から最初に一致しないセグメントを探す
    for seg in reversed(segments):
        if seg not in excluded_keywords:
            return seg
    return None  # 何も見つからない場合はNoneを返す

@main.route('/')
def index():
    app.logger.info("index.html requested")
    
    # ユーザーがログインしている場合、/dashboardにリダイレクト
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # ログインしていない場合、通常通りindex.htmlを表示
    keyword = request.args.get('keyword', 'example.co.jp')  # デフォルトキーワードを設定
    filtered_keyword = filter_keyword(keyword)
    nrds = []

    if filtered_keyword:
        # フィルタリングされたキーワードで検索
        nrds = NRD.query.filter(NRD.domain_name.contains(filtered_keyword)).limit(10).all()

    app.logger.info("index.html requested with keyword: {}".format(filtered_keyword))
    return render_template('index.html', nrds=nrds, keyword=keyword,last_search_keyword=keyword)

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

@main.route('/search_results', methods=['GET'])
def search_results():
    raw_keyword = request.args.get('keyword', '')
    filtered_keyword = filter_keyword(raw_keyword)
    if filtered_keyword:
        # フィルタリングされたキーワードで検索
        nrds = NRD.query.filter(NRD.domain_name.contains(filtered_keyword)).all()
    else:
        # キーワードが不適切な場合（または何も入力されていない場合）
        nrds = []
    return render_template('index.html', nrds=nrds)

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
        

        # 検索するタイミングでkeywordにフィルターをかける
        filtered_keyword = filter_keyword(keyword)

        if filtered_keyword:
            # フィルタリングされたキーワードで検索
            search_results = NRD.query.filter(NRD.domain_name.contains(filtered_keyword)).limit(10).all() if keyword else []

        app.logger.info("index.html requested with keyword: {}".format(filtered_keyword))
        watched_nrd_ids = [nrd.id for nrd in current_user.nrds]

    elif active_tab == 'add_domain':
        # ドメイン追加の処理
        if request.method == 'POST':
            domain_name = request.form.get('domain_name')
            if not domain_name:
                flash('ドメイン名を入力してください。', 'error')
                return redirect(url_for('main.dashboard', active_tab='monitor'))

            new_nrd = NRD(domain_name=domain_name)  # 適切な値を設定
            db.session.add(new_nrd)
            db.session.commit()

            # 新しいNRDをユーザーの監視リストに追加
            current_user.add_nrd_to_watchlist(new_nrd)
            db.session.commit()

            flash(f'{new_nrd.domain_name}が監視対象に追加されました。', 'success')
            return redirect(url_for('main.dashboard', active_tab='monitor'))
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

@main.route('/add_domain', methods=['POST'])
@login_required
def add_domain():
    data = request.json
    domain_name = data.get('domain_name')
    if not domain_name:
        flash('ドメイン名を入力してください。', 'error')
        return redirect(url_for('main.dashboard', active_tab='monitor'))

    new_nrd = NRD(domain_name=domain_name)  # 適切な値を設定
    db.session.add(new_nrd)
    db.session.commit()

    # 新しいNRDをユーザーの監視リストに追加
    current_user.add_nrd_to_watchlist(new_nrd)
    db.session.commit()

    flash(f'{new_nrd.domain_name}が監視対象に追加されました。', 'success')
    return jsonify({
        'status': 'success',
        'message': 'ドメインを追加しました。',
        'new_nrd': {
            'id': new_nrd.id,
            'domain_name': new_nrd.domain_name,
            'registration_date': new_nrd.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    })






@main.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    data = request.json
    nrd_id = data.get('nrdId')  # JSONリクエストからnrdIdを取得
    current_app.logger.info(f'Received nrd_id: {nrd_id}')
    nrd = NRD.query.get(nrd_id)
    
    if nrd:
        current_app.logger.info(f'NRD found: {nrd.domain_name} with ID {nrd.id}')
        current_user.add_nrd_to_watchlist(nrd)
        db.session.commit()  # データベースに変更をコミット
        return jsonify({'status': 'success', 'message': f"{nrd.domain_name}を監視リストに追加しました。"})
    else:
        current_app.logger.warning('NRD not found')
        return jsonify({'status': 'error', 'message': 'ドメインが見つかりませんでした。'}), 404




@main.route('/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist():
    nrd_id = request.json.get('nrdId')  # JSONリクエストからnrdIdを取得
    nrd = NRD.query.get(nrd_id)
    if nrd:
        current_user.remove_nrd_from_watchlist(nrd)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'{nrd.domain_name}を監視リストから除外しました。'})
    else:
        return jsonify({'status': 'error', 'message': 'NRDが見つかりませんでした。'}), 404


@main.route('/check_status', methods=['POST'])
@login_required
def check_status():
    nrd_id = request.json.get('nrdId')
    nrd = NRD.query.get(nrd_id)
    app.logger.info(f"privious nrd.ping_status : {nrd.ping_status}")
    app.logger.info(f"privious nrd.curl_status : {nrd.curl_status}")
    if not nrd:
        return jsonify({'status': 'error', 'message': 'NRD not found'}), 404

    # PingとCurlの実行
    ping_status = status_checker.check_ping(nrd.domain_name)
    curl_status = status_checker.check_curl(nrd.domain_name)

    # 結果の保存
    nrd.ping_status = ping_status
    nrd.curl_status = curl_status
    nrd.last_checked = datetime.utcnow()
    app.logger.info(f"updated nrd.ping_status : {nrd.ping_status}")
    app.logger.info(f"updated nrd.curl_status : {nrd.curl_status}")

    db.session.commit()

    return jsonify({'status': 'success', 'ping': ping_status, 'curl': curl_status})
