from fpdf import FPDF
#from datetime import datetime
from ordenrepar_ABM import *

varOr = DatosOrdenRepar("")

class PDF(FPDF):

    def header(self):
        # Logo
        self.image('logo1.jpg', 10, 8, 25)
        # Arial bold 15
        self.set_font('Arial', 'B', 7)
        # Move to the right
        self.cell(40)

        # Title
        datos_inf = varOr.consultar_informa()
        Titulo1 = datos_inf[1]+' - '+datos_inf[2]+' - '+datos_inf[3]+' - '+datos_inf[4]
        Titulo2 = datos_inf[6]+' - '+datos_inf[7]

        self.cell(w=130, h=7, txt=Titulo1, border=1, ln=0, align='C')
        self.ln(7)
        self.cell(40)
        self.cell(w=130, h=7, txt=Titulo2, border=1, ln=0, align='C')

        # Line break
        self.ln(10)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


# Instantiation of inherited class
# pdf = PDF()
# pdf.alias_nb_pages()
# pdf.add_page()
# pdf.set_font('Times', '', 12)
# for i in range(1, 41):
#     pdf.cell(0, 10, 'Printing line number ' + str(i), 0, 1)
# pdf.output('tuto2.pdf', 'F')