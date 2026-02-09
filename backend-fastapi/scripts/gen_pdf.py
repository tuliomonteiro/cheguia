from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Paraguay PDF Fact: The Guarani currency was established in 1944.", ln=1, align="C")
pdf.output("test.pdf")
