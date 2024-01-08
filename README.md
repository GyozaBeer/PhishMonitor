# はじめに
このWebアプリは、フィッシングサイトの可能性のあるドメインの死活監視を行うものです。  
セキュリティリスクがあるため、サンドボックスなどの安全な環境で実行してください。

# 使い方

## 1. 起動方法
git clone https://github.com/GyozaBeer/PhishMonitor.git  
docker compose up

## 2. ドメイン検索
最初にSing UPページからアカウントを作成してください。  
その後、ログインしてからDashboardのドメイン検索タブからキーワードを入力してください。  
(例 smbc,amazon.com,rakuten.co.jp など)  
検索でドメインがヒットしたら、監視対象に追加してください。

## 3. フィッシングサイト監視
Dashboardのフィッシングサイト監視画面で更新ボタンを押してください（ここでping/curlが実行されます）  
検索にヒットしなかった場合は、直接ドメインを入力することもできます。
