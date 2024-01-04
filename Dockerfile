# Dockerfile
FROM python:3.12

# pipのアップグレード
RUN python -m pip install --upgrade pip

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*
    
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
