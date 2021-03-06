import constants
from filehandler import FileHandler
from generate_report import GenerateReport


if __name__ == '__main__':

    file_handler = FileHandler(constants.CONST_PDF_NAME,
                               constants.CONST_BACKUP_SKUS_FOLDER_NAME,
                               constants.CONST_PROJECT_NAME,
                               constants.CONST_BACKUP_FOLDER_NAME)

    # Has to run first to generate data for report
    file_handler.start()

    generate_report = GenerateReport(file_handler.get_title_list(), constants.CONST_PDF_NAME)

    generate_report.start()
