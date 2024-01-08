# # app/tasks.py
# from utils.db_importer import import_nrd_to_db
# from utils.nrd_downloader import download_and_store_nrd
# from utils.celery_utils import celery

# @celery.task
# def download_nrd_task():
#     download_and_store_nrd()

# @celery.task
# def import_nrd_to_db_task():
#     import_nrd_to_db("適切なフォルダ名")

# @celery.task
# def check_domain_status_task(domain_list):
#     for domain in domain_list:
#         status = check_domain_status(domain)
#         # ここで状態更新やログ記録などの処理
