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

    skus_dir = os.path.join(Path(dir_path).parent, "backup_skus")
    backup_skus_path = os.path.join(Path(dir_path).parent, "backup_skus")
    current_sku_number = 0
    current_backup_dir_index = 0
    disk_1 = "Disk_1"
    title_list = []
    path_list = []

    def __init__(self, f, s, t, fth):
        self.pdf_name = f
        self.sku_folder_name = s
        self.project_name = t
        self.backup_file_name = fth

    # Gets skus from the Disk_1 folder in each backup directory
    def get_skus(self) -> None:
        # Gets the list of folders from backup directory

        # loops through folder in directory
        for folder in self.path_list:
            # check if folder if file names are in folder so they can be skipped if not backup folders
            if folder not in self.project_name and folder not in self.pdf_name:
                # backup file path
                backup_path = os.path.join(self.path, folder)

                # loops through folder in backup directory
                for index, backup_dir in enumerate(os.listdir(backup_path)):

                    if backup_dir == self.disk_1:
                        # Gets list of sku files in Disk_1 folder in backup directory
                        sku_dir = os.path.join(os.path.join(backup_path, backup_dir), "sku.sis")
                        # Moves the sku.sis file to the new folder
                        self.move_to_skus_folder(sku_dir)

    # receives sku files from get_skus method and copies them to skus_backup_folder
    def move_to_skus_folder(self, file) -> None:
        # Increments property to keep track of index to be used for sku file name ex. sku_1
        self.current_sku_number += 1

        shutil.copy(file, self.skus_dir)

        # changes name of sku.sis to sku_1.txt
        self.rename_file(file)  # ex. file = D:\\Steam Backups\backup_0\Disk_1\sku.sis

    # Changes name of sku files to be added to backup_skus ,so they have unique names
    def rename_file(self, file) -> None:
        # goes up two level to get to the backup root
        folder = Path(file).parent.parent

        # Gets the folder name ex. backup_0
        folder_name = str(folder).split("\\", 2)[2]
        # Creates the path with the sis file in it ex. D:\Steam Backups\backup_skus\sku.sis
        old_file = os.path.join(self.backup_skus_path, "sku.sis")
        # Removes the sis extension from the sis file in the folder
        name_change = old_file.split(".", 1)
        # Changes sis extension txt
        name_change[1] = "txt"
        # add Joins the txt to the file name sku_1.txt
        new_file = f"_{self.current_sku_number}.".join(name_change)

        # renames the old sku.sis to its new name (sku_1.txt)
        os.rename(old_file, new_file)

        self.add_backup_folder_name_to_text_file(new_file, folder_name)

    # Add the backup folder name to text file to be later referenced for generated report
    def add_backup_folder_name_to_text_file(self, file_name, folder_name) -> None:
        # Add folder name to txt file
        with open(file_name, 'a+') as f:
            f.write(folder_name)
        f.close()

    def read_sku_txt(self) -> None:
        # So this method has to loot through directory and open and close the files
        for file in os.listdir(self.backup_skus_path):
            # Opens sku text files to extract titles
            with open(os.path.join(self.backup_skus_path, file), 'r') as f:
                lines = f.readlines()

                titles = lines[2].split("and")

                # Removes "name" string along  with space and " character
                titles[0].replace("\"name\"", "").lstrip()

                for title in titles[1:]:
                    self.title_list.append(gameBackupModel(title
                                                           .replace("â„¢", "")
                                                           .replace("\"", "")
                                                           .replace("Â® ", ""),
                                                           lines[-1]))

    # Empties sku folders so new copies can be added when
    def clear_skus_folder(self) -> None:
        for file in os.listdir(self.backup_skus_path):
            os.remove(os.path.join(self.backup_skus_path, file))

    def create_skus_folder(self):

        if not (os.path.isdir(self.skus_dir)):
            os.mkdir(self.skus_dir)

    # Refresh folder names so there will not be name collisions when generating new folders
    def create_temp_folder_name(self):
        for index, directory in enumerate(os.listdir(self.path)):
            if self.sku_folder_name not in directory and self.project_name not in directory and self.pdf_name not in directory:
                old_name = os.path.join(self.path, directory)
                new_name = os.path.join(self.path, f"temp - {index}")

                os.rename(old_name, new_name)

    def rename_backup_dirs(self):
        for index, directory in enumerate(os.listdir(self.path)):
            if self.sku_folder_name not in directory and self.project_name not in directory and self.pdf_name not in directory:
                old_name = os.path.join(self.path, directory)
                new_name = os.path.join(self.path, f"{self.backup_file_name}{self.current_backup_dir_index}")

                os.rename(old_name, new_name)
                self.current_backup_dir_index += 1

    def start(self) -> None:
        self.create_temp_folder_name()
        self.rename_backup_dirs()

        self.path_list = os.listdir(self.path)
        # Creates the skus folder if it doesn't exist
        self.create_skus_folder()

        # clears folder to update sku files
        self.clear_skus_folder()

        self.get_skus()

        self.read_sku_txt()
