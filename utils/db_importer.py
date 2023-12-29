from app.models import NRD
from app import db

def import_nrd_to_db(folder_name):
    # NRDファイルのパスを指定
    file_path = f"{folder_name}/domain-names.txt"

    # ファイルを読み込み、DBにデータを格納
    with open(file_path, 'r') as file:
        for line in file:
            domain_name = line.strip()
            nrd_entry = NRD(domain_name=domain_name)
            db.session.add(nrd_entry)
        db.session.commit()
