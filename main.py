from filehandler import FileHandler
from generate_table import GenerateTable
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


if __name__ == '__main__':
    file_handler = FileHandler()

    file_handler.start()

    generate_table = GenerateTable(file_handler.read_sku_txt())

    generate_table.convert_data()

    generate_table.create()
