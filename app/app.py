from flask import Flask, request, jsonify, render_template
import os
import base64
import requests
import zipfile
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-file-status')
def check_file_status():
    date = request.args.get('date')
    # ... (状態チェックのロジック)
    return jsonify(status="status_here")


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    date = request.form.get('date')
    filename = os.path.join(date, 'domain-names.txt')

    # 指定された日付のフォルダが存在しない場合、ファイルを生成
    if not os.path.exists(filename):
        if not generate_nrd_file(date):
            return jsonify({"error": "Unable to generate file"}), 500

    try:
        results = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if keyword.lower() in line.lower():
                    results.append(line.strip())
        return jsonify(results)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

def generate_nrd_file(date_str):
    file_name = f"{date_str}.zip"
    folder_name = f"{date_str}"

    if not os.path.exists(folder_name):
        encoded_date = base64.b64encode(file_name.encode()).decode()
        download_url = f"https://www.whoisds.com//whois-database/newly-registered-domains/{encoded_date}/nrd"

        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk:
                        file.write(chunk)

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall(folder_name)
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
