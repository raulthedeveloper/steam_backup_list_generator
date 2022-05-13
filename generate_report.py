from fpdf import FPDF
import os
from pathlib import Path


class GenerateTable:
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Times", size=12)

    line_height = pdf.font_size * 2.5

    col_width = pdf.epw / 2  # distribute content evenly

    pdf_name = "steam_backup_list.pdf"

    new_list = [
        ["Game", "Location"]
    ]

    def __init__(self, backup_list):
        self.backup_list_data = backup_list

    def convert_data(self):
        for item in self.backup_list_data:
            self.new_list.append([item.title, item.directory])

    def create(self):
        for row in self.new_list:
            for datum in row:
                self.pdf.multi_cell(self.col_width, self.line_height, datum, border=1,
                                    new_x="RIGHT", new_y="TOP", max_line_height=self.pdf.font_size)
            self.pdf.ln(self.line_height)

        pdf = os.path.join(Path(os.path.realpath(__file__)).parent.parent, self.pdf_name)

        # Get path of pdf file
        self.pdf.output(name=pdf, dest="F")

        # Auto opens pdf file after generated
        os.startfile(pdf)
