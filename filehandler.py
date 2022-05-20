import os
import sys
import shutil
import random
from pathlib import Path
from game_backup_model import gameBackupModel
import ctypes  # An included library with Python install.


class FileHandler:
    dir_path = os.getcwd()

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
    non_backup_flag = "__"
    __title_list = []
    path_list = []

    def __init__(self, f, s, t, fth):
        self.pdf_name = f
        self.sku_folder_name = s
        self.project_name = t
        self.backup_file_name = fth

    @staticmethod
    def mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    # Gets skus from the Disk_1 folder in each backup directory
    def __get_skus(self) -> None:
        # Gets the list of folders from backup directory

        # loops through folder in directory
        for folder in self.path_list:
            # check if folder if file names are in folder so they can be skipped if not backup folders
            if folder not in self.project_name and folder not in self.pdf_name:
                # backup file path
                backup_path = os.path.join(self.path, folder)

                # loops through folder in backup directory
                for backup_dir in os.listdir(backup_path):

                    if backup_dir == self.disk_1:
                        # Gets list of sku files in Disk_1 folder in backup directory
                        sku_dir = os.path.join(os.path.join(backup_path, backup_dir), "sku.sis")
                        # Moves the sku.sis file to the new folder
                        self.__move_to_skus_folder(sku_dir)
                        break

    # receives sku files from get_skus method and copies them to skus_backup_folder
    def __move_to_skus_folder(self, file) -> None:
        # Increments property to keep track of index to be used for sku file name ex. sku_1
        self.current_sku_number += 1

        shutil.copy(file, self.skus_dir)

        # changes name of sku.sis to sku_1.txt
        self.__rename_file(file)  # ex. file = D:\\Steam Backups\backup_0\Disk_1\sku.sis

    # Changes name of sku files to be added to backup_skus ,so they have unique names
    def __rename_file(self, file) -> None:
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

        self.__add_backup_folder_name_to_text_file(new_file, folder_name)

    # Add the backup folder name to text file to be later referenced for generated report
    def __add_backup_folder_name_to_text_file(self, file_name, folder_name) -> None:
        # Add folder name to txt file
        with open(file_name, 'a+') as f:
            f.write(folder_name)
        f.close()

    def __save_sku_txt_to_list(self) -> None:
        # So this method has to loot through directory and open and close the files
        for file in os.listdir(self.backup_skus_path):
            # Opens sku text files to extract titles
            with open(os.path.join(self.backup_skus_path, file), 'r') as f:
                lines = f.readlines()

                titles = lines[2].split("and")

                # Removes "name" string along  with space and " character
                titles[0].replace("\"name\"", "").lstrip()

                for title in titles[1:]:
                    self.__title_list.append(gameBackupModel(title
                                                             .replace("â„¢", "")
                                                             .replace("\"", "")
                                                             .replace("Â® ", ""),
                                                             lines[-1]))

    # Empties sku folders so new copies can be added when
    def __clear_skus_folder(self) -> None:
        for file in os.listdir(self.backup_skus_path):
            os.remove(os.path.join(self.backup_skus_path, file))

    def __create_skus_folder(self):

        if not (os.path.isdir(self.skus_dir)):
            os.mkdir(self.skus_dir)

    # Refresh folder names so there will not be name collisions when generating new folders
    def __create_temp_folder_name(self):
        for index, directory in enumerate(os.listdir(self.path)):
            if self.sku_folder_name not in directory and self.project_name not in directory and self.pdf_name not in directory:
                old_name = os.path.join(self.path, directory)
                new_name = os.path.join(self.path, f"temp - {index}")

                # prevents not backup files from being renamed
                if self.non_backup_flag not in old_name:
                    os.rename(old_name, new_name)

    def __rename_backup_dirs(self):
        for index, directory in enumerate(os.listdir(self.path)):
            if self.sku_folder_name not in directory and self.project_name not in directory and self.pdf_name not in directory:
                old_name = os.path.join(self.path, directory)
                new_name = os.path.join(self.path, f"{self.backup_file_name}{self.current_backup_dir_index}")

                # prevents not backup files from being renamed
                if self.non_backup_flag not in old_name:
                    os.rename(old_name, new_name)
                    self.current_backup_dir_index += 1

    def __check_if_any_backups_directories(self):

        if len(os.listdir(self.path)) > 1:
            for folder in os.listdir(self.path):

                # check if folder if file names are in folder so they can be skipped if not backup folders
                if folder not in self.project_name and folder not in self.pdf_name and folder not in self.sku_folder_name:
                    # backup file path
                    backup_path = os.path.join(self.path, folder)

                    if os.listdir(backup_path):
                        # loops through folder in backup directory
                        for backup_dir in os.listdir(backup_path):
                            # allow program to skip over files that aren't the backup directory and files
                            if os.path.isfile(os.path.join(backup_path, backup_dir)) or backup_dir != self.disk_1:
                                pass

                            elif backup_dir == self.disk_1:
                                # Gets list of sku files in Disk_1 folder in backup directory
                                sku_dir = os.path.join(os.path.join(backup_path, backup_dir), "sku.sis")

                                if os.path.exists(sku_dir):
                                    break
                                else:
                                    FileHandler.alert_message("Alert", folder, backup_dir, "sku.sys", "missing_target")
                            else:
                                FileHandler.alert_message("Alert", folder, backup_dir, self.disk_1, "empty_target_dir")

                    else:

                        if self.non_backup_flag not in backup_path:
                            try:
                                os.rename(backup_path, backup_path + self.non_backup_flag)
                            except:
                                # Generates random ID + number to fix duplicate folder names
                                rand_id = str(random.randrange(1, 400))
                                # New path name with the generated ID added to folder name
                                new_path = F"{backup_path}-ID{rand_id}{self.non_backup_flag}"

                                os.rename(backup_path, new_path)

                                # Creates alert popup to inform the user of the changes made
                                FileHandler.mbox("Alert", F"{backup_path} was changed to {new_path} because of "
                                                          F"name duplication", 0)

        else:
            FileHandler.alert_message("Alert", None, None, None, "no_backups_files")

    @staticmethod
    def alert_message(heading, directory, target_dir, target, message_type):
        if message_type == "missing_target":
            FileHandler.mbox(heading, f'Application can not find "{target}" in "{os.path.join(os.getcwd(),target_dir)}."'
                                      f'Please replace steam backup files in {target_dir} directory'
                                      f' or remove empty "{target_dir}" folder', 0)
        elif message_type == "empty_target_dir":
            FileHandler.mbox(heading, f'Please remove empty "{target}" folder from "{target_dir}" folder'
                                      f' in the "{directory}" directory'
                                      f' or replace backup files', 0)
        elif message_type == "no_backup_files":
            FileHandler.mbox(heading, f'Please place program directory into the backup directory', 0)
        sys.exit()

    def get_title_list(self):
        # raises warning if method is ran before start and if proper backup folders aren't present
        if not self.__title_list:
            raise Warning(
                "Please run the start methods first to populate list, or please add proper backup directories")
        else:
            return self.__title_list

    def start(self) -> None:

        self.__check_if_any_backups_directories()
        self.__create_temp_folder_name()
        self.__rename_backup_dirs()

        self.path_list = os.listdir(self.path)

        # Creates the skus folder if it doesn't exist
        self.__create_skus_folder()

        # clears folder to update sku files
        self.__clear_skus_folder()

        self.__get_skus()

        self.__save_sku_txt_to_list()
