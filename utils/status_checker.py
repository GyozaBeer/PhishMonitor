import subprocess
import requests
from flask import current_app as app  # appインスタンスのインポート

def check_ping(domain):
    try:
        response = subprocess.run(["ping", "-c", "1", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    except Exception as e:
        app.logger.info(f"{e}")
        return False

def check_curl(domain):
    try:
        response = requests.get("http://" + domain, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

