import PyPDF2
from fpdf import FPDF

pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(50,50, txt="abcdefrrrrrrrrrrrr",align="C")
pdf.output("hello2.pdf")