import constants
from directory_tests import DirectoryTests
from filehandler import FileHandler
from generate_table import GenerateTable

if __name__ == '__main__':
    # Paste test methods here
    
    # rename_dirs_test = DirectoryTests(constants.CONST_BACKUP_SKUS_FOLDER_NAME, constants.CONST_PROJECT_NAME, constants.CONST_PDF_NAME)
    # rename_dirs_test.rename_directories()

    # End of test methods

    file_handler = FileHandler(constants.CONST_PDF_NAME,constants.CONST_BACKUP_SKUS_FOLDER_NAME, constants.CONST_PROJECT_NAME, constants.CONST_BACKUP_FOLDER_NAME)

    file_handler.start()

    generate_table = GenerateTable(file_handler.read_sku_txt())

    generate_table.convert_data()

    generate_table.create()
