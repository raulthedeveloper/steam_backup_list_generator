from fpdf import FPDF
import os
from pathlib import Path


class GenerateReport:
    __pdf = FPDF()

    __pdf.add_page()

    __pdf.set_font("Times", size=12)

    __line_height = __pdf.font_size * 2.5

    __col_width = __pdf.epw / 2  # distribute content evenly

    __pdf_name = ""

    __new_list = [
        ["Game", "Location"]
    ]

    def __init__(self, backup_list, pn):
        self.backup_list_data = backup_list
        self.__pdf_name = pn

    def convert_data(self):
        for item in self.backup_list_data:
            self.__new_list.append([item.title, item.directory])

    def create(self):
        for row in self.__new_list:
            for datum in row:
                self.__pdf.multi_cell(self.__col_width, self.__line_height, datum, border=1,
                                      new_x="RIGHT", new_y="TOP", max_line_height=self.__pdf.font_size)
            self.__pdf.ln(self.__line_height)

        pdf = os.path.join(Path(os.path.realpath(__file__)).parent.parent, self.__pdf_name)

        # Get path of pdf file
        self.__pdf.output(name=pdf, dest="F")

        # Auto opens pdf file after generated
        os.startfile(pdf)

    def start(self):
        self.convert_data()
        self.create()
