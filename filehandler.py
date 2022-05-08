import os
import shutil
from typing import List
from pathlib import Path
from game_backup_model import gameBackupModel


class FileHandler:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = Path(dir_path).parent
    path_list = os.listdir(path)
    skus_dir = os.path.join(Path(dir_path).parent, "backup_skus")
    backup_skus_path = os.path.join(Path(dir_path).parent, "backup_skus")
    current_sku_number = 0

    def get_skus(self) -> List[str]:

        skus = []
        # clears folder to update sku files
        self.clear_skus_folder()

        # loops through folder in directory
        for folder in self.path_list:
            if folder != "steam_backup_list":
                # backup file path
                backup_path = os.path.join(self.path, folder)

                # loops through folder in backup directory
                for index, backup_dir in enumerate(os.listdir(backup_path)):

                    if backup_dir == "Disk_1":
                        # Gets list of files in directory
                        backup_files = os.listdir(os.path.join(backup_path, backup_dir))

                        sku_dir = os.path.join(os.path.join(backup_path, backup_dir), "sku.sis")

                        self.move_to_skus_folder(sku_dir)

                        # // its time to read the file
                        skus.append(backup_files[-1])

        return skus

    def create_html_list(self):
        pass

    def move_to_skus_folder(self, file):
        self.current_sku_number += 1

        shutil.copy(file, self.skus_dir)

        # change the name here
        self.rename_file(file)

    def rename_file(self, file) -> None:
        old_file = os.path.join(self.backup_skus_path, "sku.sis")

        name_change = old_file.split(".", 1)

        name_change[1] = "txt"

        new_file = f"_{self.current_sku_number}.".join(name_change)

        os.rename(old_file, new_file)

    def read_sku_txt(self) -> List[str]:
        # So this method has to loot through directory and open and close the files
        title_list = []

        for file in os.listdir(self.backup_skus_path):
            # Opens sku text files to extract titles
            print(file)
            with open(os.path.join(self.backup_skus_path, file), 'r') as f:
                lines = f.readlines()

                titles = lines[2].split("and")

                # Removes "name" string along  with space and " character
                titles[0].replace("\"name\"", "").replace("\"", "").lstrip()

                for title in titles[1:]:
                    title_list.append(gameBackupModel(title, "string"))

        return title_list

    def clear_skus_folder(self):
        for file in os.listdir(self.backup_skus_path):
            print(f"{file} was removed")
            os.remove(os.path.join(self.backup_skus_path, file))

    def create_skus_folder(self):

        if not (os.path.isdir(self.skus_dir)):
            os.mkdir(self.skus_dir)

    def start(self) -> None:
        self.create_skus_folder()
        self.get_skus()
        # prints objects
        for game_objects in self.read_sku_txt():
            print(game_objects.title)
