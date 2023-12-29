from celery import Celery
from celery.schedules import crontab
from utils.db_importer import import_nrd_to_db
from utils.nrd_downloader import download_and_store_nrd
from utils.domain_status_checker import check_domain_status

celery = Celery(__name__)
celery.conf.broker_url = 'redis://localhost:6379/0'

@celery.task
def download_nrd_task():
    download_and_store_nrd()

@celery.task
def import_nrd_to_db_task():
    # 適切なフォルダ名やファイル名を指定
    import_nrd_to_db("適切なフォルダ名")

celery.conf.beat_schedule = {
    'download-nrd-every-midnight': {
        'task': 'tasks.download_nrd_task',
        'schedule': crontab(hour=0, minute=0),
    },
    'import-nrd-to-db': {
        'task': 'tasks.import_nrd_to_db_task',
        'schedule': crontab(hour=1, minute=0),  # ダウンロード後に実行
    }
}

@celery.task
def check_domain_status_task(domain_list):
    for domain in domain_list:
        status = check_domain_status(domain)
        # ここで状態更新やログ記録などの処理
