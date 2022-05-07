import os
from os import listdir
from os.path import isfile, join
from pathlib import Path


class FileHandler:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def read_directory(self):
        path = Path(self.dir_path).parent
        path_list = os.listdir(path)

        # loops through folder in directory
        for folder in path_list:
            if folder != "steam_backup_list":
                # loops through folder in backup directory
                backup_path = os.path.join(path, folder)
                for backup_dir in os.listdir(backup_path):
                    if backup_dir == "Disk_1":
                        backup_files = os.listdir(os.path.join(backup_path, backup_dir))

                        # // its time to read the file
                        print(backup_files[-1])

    def convert_sis_to_txt(self):
        pass

    def create_html_list(self):
        pass

    def read_sku(self):
        pass
