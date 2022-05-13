import os
import shutil
from typing import List
from pathlib import Path
from game_backup_model import gameBackupModel


class FileHandler:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    sku_folder_name = ""
    pdf_name = ""
    project_name = ""
    backup_file_name = ""

    path = Path(dir_path).parent
    path_list = os.listdir(path)
    skus_dir = os.path.join(Path(dir_path).parent, "backup_skus")
    backup_skus_path = os.path.join(Path(dir_path).parent, "backup_skus")
    current_sku_number = 0
    disk_1 = "Disk_1"

    def __init__(self, f, s, t, fth):
        self.pdf_name = f
        self.sku_folder_name = s
        self.project_name = t
        self.backup_file_name = fth


    def get_skus(self) -> None:

        # loops through folder in directory
        for folder in self.path_list:
            # check if folder if file names are in folder so they can be skipped if not backup folders
            if folder not in self.project_name and folder not in self.pdf_name:
                # backup file path
                backup_path = os.path.join(self.path, folder)

                # loops through folder in backup directory
                for index, backup_dir in enumerate(os.listdir(backup_path)):

                    if backup_dir == self.disk_1:
                        # Gets list of files in directory
                        backup_files = os.listdir(os.path.join(backup_path, backup_dir))

                        sku_dir = os.path.join(os.path.join(backup_path, backup_dir), "sku.sis")

                        self.move_to_skus_folder(sku_dir)



    def move_to_skus_folder(self, file):
        self.current_sku_number += 1

        shutil.copy(file, self.skus_dir)
        # change the name here
        self.rename_file(file)

    def rename_file(self, file) -> None:
        folder = Path(file).parent.parent

        folder_name = str(folder).split("\\", 2)[2]

        old_file = os.path.join(self.backup_skus_path, "sku.sis")

        name_change = old_file.split(".", 1)

        name_change[1] = "txt"

        new_file = f"_{self.current_sku_number}.".join(name_change)

        os.rename(old_file, new_file)

        self.add_folder_name(new_file, folder_name)

    def add_folder_name(self, file_name, folder_name) -> None:
        # Add folder name to txt file
        with open(file_name, 'a+') as f:
            f.write(folder_name)
        f.close()

    def read_sku_txt(self) -> List[str]:
        # So this method has to loot through directory and open and close the files
        title_list = []

        for file in os.listdir(self.backup_skus_path):
            # Opens sku text files to extract titles
            with open(os.path.join(self.backup_skus_path, file), 'r') as f:
                lines = f.readlines()

                titles = lines[2].split("and")

                # Removes "name" string along  with space and " character
                titles[0].replace("\"name\"", "").lstrip()

                for title in titles[1:]:
                    title_list.append(gameBackupModel(title.replace("â„¢", "").replace("\"", ""), lines[-1]))

        return title_list

    def clear_skus_folder(self) -> None:
        for file in os.listdir(self.backup_skus_path):
            os.remove(os.path.join(self.backup_skus_path, file))

    def create_skus_folder(self):

        if not (os.path.isdir(self.skus_dir)):
            os.mkdir(self.skus_dir)

    def rename_backup_dirs(self):
        for index, directory in enumerate(os.listdir(self.path)):
            if self.sku_folder_name not in directory and self.project_name not in directory and self.pdf_name not in directory:
                old_name = os.path.join(self.path, directory)
                new_name = os.path.join(self.path, f"{self.backup_file_name}{index}")

                if not os.path.exists(new_name):
                    os.rename(old_name, new_name)

    def start(self) -> None:
        # Creates the skus folder if it doesn't exist
        self.create_skus_folder()

        # clears folder to update sku files
        self.clear_skus_folder()

        self.get_skus()
        self.rename_backup_dirs()
