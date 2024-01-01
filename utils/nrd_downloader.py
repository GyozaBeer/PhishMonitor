#utils/nrd_downloader.py
from flask import current_app as app  # appインスタンスのインポート
import os
import base64
import requests
import zipfile
from datetime import datetime, timedelta

def download_and_store_nrd():
    success=False
    for i in range(2, 5):  
        # 日付を取得してフォーマットする
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        file_name = f"{date_str}.zip"
        folder_name = f"{date_str}"

        # ファイルが既に存在するか確認
        if not os.path.exists(os.path.join(folder_name, file_name)):
            # Base64で日付をエンコードする
            encoded_date = base64.b64encode(file_name.encode()).decode()

            # ダウンロードURLを作成する
            download_url = f"https://www.whoisds.com//whois-database/newly-registered-domains/{encoded_date}/nrd"
            app.logger.info(f"Downloading from: {download_url}")  # ダウンロードURLを出力

            # リクエストを送信
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                # フォルダを作成
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                file_path = os.path.join(folder_name, file_name)

                # ファイルを書き込む
                with open(file_path, 'wb') as file:
                    file.write(response.content)  # ストリームではなく一括で書き込む
                app.logger.info(f'{file_name} has been downloaded to {folder_name}. File size: {os.path.getsize(file_path)} bytes.')  # ファイルサイズを出力

                # ZIPファイルを検証
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_content = zip_ref.namelist()  # ZIPファイル内のファイルリストを取得
                        app.logger.info(f'ZIP file contains: {zip_content}')  # ZIPファイルの内容を出力
                        zip_ref.extractall(folder_name)
                        app.logger.info(f'{file_name} has been unzipped in {folder_name}.')
                        success=True
                except zipfile.BadZipFile:
                    app.logger.error(f'Error: The file downloaded from {download_url} was not a valid ZIP file.')
                    success = False  # ZIPファイルが無効な場合は、成功フラグをFalseに設定します
            else:
                app.logger.error(f'Failed to download the file for {date_str}. Status code: {response.status_code}')
                success = False
        else:
            app.logger.info(f"File {file_name} already exists in {folder_name}.")
    # 処理の終了をロギング
    if success:
        app.logger.info("NRD download and storage process completed successfully.")
    else:
        app.logger.error("NRD download and storage process failed.")
    return success  # 全ての処理の後で、成功かどうかのフラグを返します