# utils/nrd_downloader.py

import os
import base64
import requests
import zipfile
from datetime import datetime, timedelta

def download_and_store_nrd():
    # 日付を取得してフォーマットする
    date_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    file_name = f"{date_str}.zip"
    folder_name = f"{date_str}"

    # ファイルが既に存在するか確認
    if not os.path.exists(file_name):
        # Base64で日付をエンコードする
        encoded_date = base64.b64encode(file_name.encode()).decode()

        # ダウンロードURLを作成する
        download_url = f"https://www.whoisds.com//whois-database/newly-registered-domains/{encoded_date}/nrd"

        # リクエストを送信
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024): 
                    if chunk:
                        file.write(chunk)
            print(f'{file_name} has been downloaded.')

            # フォルダを作成
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # ZIPファイルを展開
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall(folder_name)
                print(f'{file_name} has been unzipped in {folder_name}.')
        else:
            print(f'Failed to download the file. Status code: {response.status_code}')
    else:
        print(f"File {file_name} already exists.")

