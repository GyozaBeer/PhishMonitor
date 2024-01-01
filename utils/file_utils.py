import os
from datetime import datetime

def find_latest_folder(base_directory):
    latest_date = None
    latest_folder = None
    for folder in os.listdir(base_directory):
        try:
            folder_path = os.path.join(base_directory, folder)
            if os.path.isdir(folder_path):
                folder_date = datetime.strptime(folder, '%Y-%m-%d')
                if latest_date is None or folder_date > latest_date:
                    latest_date = folder_date
                    latest_folder = folder
        except ValueError:
            # フォルダ名が日付形式でない場合は無視
            continue
    return latest_folder

# 使用例
# latest_folder = find_latest_folder("/path/to/downloaded/nrd/files")
