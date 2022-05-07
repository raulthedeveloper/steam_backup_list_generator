import os
import shutil
from os import listdir
from os.path import isfile, join
from pathlib import Path


class FileHandler:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    skus_dir = os.path.join(Path(dir_path).parent, "backup_skus")
    current_sku_number = 0

    def get_skus(self):
        path = Path(self.dir_path).parent
        path_list = os.listdir(path)
        skus = []
        # loops through folder in directory
        for folder in path_list:
            if folder != "steam_backup_list":
                # backup file path
                backup_path = os.path.join(path, folder)

                # loops through folder in backup directory
                for index, backup_dir in enumerate(os.listdir(backup_path)):

                    if backup_dir == "Disk_1":
                        backup_files = os.listdir(os.path.join(backup_path, backup_dir))

                        sku_dir = os.path.join(os.path.join(backup_path, backup_dir), "sku.sis")

                        self.move_to_skus_folder(sku_dir)

                        # // its time to read the file
                        skus.append(backup_files[-1])

        return skus

    def convert_sis_to_txt(self):
        pass

    def create_html_list(self):
        pass

    def move_to_skus_folder(self, file):
        self.current_sku_number += 1
        name_change = file.split(".", 1)
        name_change[1] = "txt"
        new_file_name = f"_{self.current_sku_number}.".join(name_change)
        print(file)

        # I have to change file  names before they get sent to this method and then change the extension.

        shutil.copy(file, self.skus_dir)


    def read_sku_txt(self):
        pass

    def create_skus_folder(self):

        if not (os.path.isdir(self.skus_dir)):
            os.mkdir(self.skus_dir)
