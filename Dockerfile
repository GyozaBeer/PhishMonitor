# Dockerfile
FROM python:3.8

# アプリケーションディレクトリを設定
WORKDIR /app

# アプリケーションの依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションソースをコピー
COPY . .

# ファイル処理用ディレクトリを作成
RUN mkdir -p /app/files

# アプリケーションを実行
CMD ["python", "./run.py"]

EXPOSE 5000
