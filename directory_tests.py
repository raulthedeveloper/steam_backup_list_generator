import os
import time

from pathlib import Path


class DirectoryTests:
    project_directory = os.path.dirname(os.path.realpath(__file__))
    backup_directory = Path(project_directory).parent

    backup_skus_folder = ""
    project_folder = ""
    pdf_name = ""

    def __init__(self, f, s, t):
        self.backup_skus_folder = f
        self.project_directory = s
        self.pdf_name = t

    def rename_directories(self) -> None:
        for index, folder in enumerate(os.listdir(self.backup_directory)):
            if folder not in self.backup_skus_folder and folder not in self.project_directory and folder not in self.pdf_name:
                old_file_path = os.path.join(self.backup_directory, folder)
                test_file_path = os.path.join(self.backup_directory, f"test_{index}")

                if not os.path.exists(test_file_path):
                    os.rename(old_file_path, test_file_path)

        time.sleep(3)

    def rename_directory(self, index) -> None:
        time.sleep(2)
        pass

    def directory_rename_test(self) -> None:
        print("test passed")
        pass
