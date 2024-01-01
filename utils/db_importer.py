#utils/db_importer.py
from flask import current_app as app
from app.database import db
from app.models import NRD
import os
import shutil
from datetime import datetime

def clear_nrd_data():
    try:
        NRD.query.delete()
        db.session.commit()
        app.logger.info("Existing NRD data cleared.")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error clearing NRD data: {e}")

def delete_downloaded_files(folder_name):
    try:
        shutil.rmtree(folder_name)
        app.logger.info(f"Downloaded files in {folder_name} deleted.")
    except Exception as e:
        app.logger.error(f"Error deleting downloaded files: {e}")

def import_nrd_to_db(folder_name):
    clear_nrd_data()
    file_path = os.path.join(folder_name, 'domain-names.txt')

    if not os.path.exists(file_path):
        app.logger.info(f"File not found: {file_path}")
        return False

    nrd_list = []
    registration_date = datetime.strptime(folder_name, '%Y-%m-%d')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                domain_name = line.strip()
                nrd_entry = NRD(domain_name=domain_name, registration_date=registration_date)
                nrd_list.append(nrd_entry)

        db.session.bulk_save_objects(nrd_list)
        db.session.commit()
        delete_downloaded_files(folder_name)
        app.logger.info("NRD data imported successfully.")
        return True

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error importing NRD to database: {e}")
        return False
