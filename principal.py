""" Este es el modulo menu principal desde donde accedemos a cada ABM y proceso del sistema"""
from clientes import Ventana
from proved import *
from articulos import VentArt
from orden_reparacion import *
from marcas import Vent_marcas
from rubros import Vent_rubros
from cotiz_vta import *
from configuracion import *
from planilla_caja import PlaniCaja
from ctacte import CuentaCorriente
from saldosctacte import Saldosctacte
from inf_tecnicos import clase_inf_tecnicos
from garantias import clase_garantias
from recibos import clase_recibos
from presupuestos import clase_presupuestos
from compras import clase_compras
from rma import clase_rma
from respaldos import *
from guias_tecnicas import clase_GuiasTecnicas
#------------------------------------------------------
import tkinter as tk
#------------------------------------------------------
from PIL import Image, ImageTk
import  locale

""" esta clase Principal, hereda de la clase Frame"""

class Principal(Frame):

    """ Al poner Frame como parametro en la clase Principal, estamos diciendo que hereda de la clase Frame.

    En el constructor (def __init__ (self, master=None)) siempre debe ir self y el parametro que recibe de la clase
    padre (master) es la pantalla que asi se llamarà. Master inicializada en vacia???.

    Luego indicamos el super() para pasar los parametros agregados en la clase hija o sea "Principal"
    (hereda todas las cosas de Frame) ademas del que ya teniamos "master" que debe ir primero. los parametros
    que agregamos son ancho y alto """

    def __init__(self, master=None):
        # herencia
        super().__init__(master, width=880, height=510)
        # propiedades instanciamientos
        self.master = master

        locale.setlocale(locale.LC_ALL, '')
        # locale.setlocale(locale.LC_ALL, 'ar_AR')
        # print(locale.localeconv())

        # ------------------------------------------------------------------------------
        # Agregado para centrar la pantalla principal
        # ------------------------------------------------------------------------------
        self.master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 880
        hventana = 510
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        # Se lo aplicamos a la geometría de la ventana
        self. master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # BARRA DE MENU
        # ---------------------------------------------------------------------
        menu_principal = tk.Menu(self.master)
        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_archivo.add_command(label='* Archivo de Clientes', command=self.fClientes)
        menu_archivo.add_command(label='* Archivo de Proveedores', command=self.fProved)
        menu_archivo.add_command(label='* Archivo de Marcas', command=self.m_marcas)
        menu_archivo.add_command(label='* Archivo de Rubros', command=self.fRubros)
        #menu_archivo.add_command(label='* Archivo items Ingresos y Egresos', command=self.fIngEgr)
        menu_archivo.add_command(label='* Configuracion', command=self.fConfiguracion)

        menu_informes = tk.Menu(menu_principal, tearoff=0)
        menu_informes.add_command(label='* Saldos cuenta corriente', command=self.fInf_ctacte)
        menu_informes.add_command(label='* Informes Tecnicos', command=self.fInf_tecnico)

        menu_tecnica = tk.Menu(menu_principal, tearoff=0)
        menu_tecnica.add_command(label='* Guias Tecnicas', command=self.fTecnicas)

        menu_principal.add_cascade(label='Archivos', menu=menu_archivo)
        menu_principal.add_cascade(label='Tecnica', menu=menu_tecnica)
        menu_principal.add_cascade(label='Informes', menu=menu_informes)
        menu_principal.add_command(label='Acerca de...')
        menu_principal.add_command(label='Salir', command=self.fsale_menu)

        self.master.config(menu=menu_principal)
        # --------------------------------------------------------------------

        self.create_widgets()

    def fsale_menu(self):

        self.master.quit()
        self.master.destroy()

    def create_widgets(self):

        # TITULO principal de pantalla - traer_nombre de Empresa
        # datos_retornados = self.consultar_parametros()

        # label1 = Label(self.master, text='Sistema Tecnico - ' + datos_retornados[1],
        #                bg="black", fg="gold", font=("times new roman", 30, "bold"),
        #                bd=12, relief=RIDGE)

        # ---------------------------------------------------------------
        # Foto fondo pantalla Promatica
        photo33 = Image.open("promatica.jpg")
        photo33 = photo33.resize((880, 510), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo33 = ImageTk.PhotoImage(photo33)
        fondopan = Label(self.master, image=photo33).place(x=0, y=85)

        label1 = Label(self.master, text='Gestion Comercial - Promatica Computacion', bg="black", fg="gold",
                       font=("times new roman", 30, "bold"), bd=12, relief=RIDGE)

        label1.pack(side=TOP, fill=X, pady=10, padx=5)
        # ---------------------------------------------------------------

        # ---------------------------------------------------------------
        # Creo el LabelFrame principal
        self.frame1 = LabelFrame(self.master, bg="#bfdaff")
        self.frame2 = LabelFrame(self.master, bg="#bfdaff")

        # ---------------------------------------------------------------
        #BARRA MENU INFERIOR

        # ARTICULOS CRUD - ABM ------------------------------------------------------------------------
        photo1 = Image.open('productos.png')
        photo1 = photo1.resize((80, 70), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo1 = ImageTk.PhotoImage(photo1)
        self.btnArticulos = Button(self.frame1, text="Articulos", image=photo1, compound=TOP, pady=3,
                                   border=3, command=self.fArticulos, bg="blue", fg="white")
        self.btnArticulos.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # ORDENES DE REPARACION -----------------------------------------------------------------------
        photo2 = Image.open('reparar.png')
        photo2 = photo2.resize((80, 70), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo2 = ImageTk.PhotoImage(photo2)
        self.btnorden_rep = Button(self.frame1, text="Orden Reparacion", image=photo2, compound=TOP, pady=3,
                                   border=3, command=self.m_orden_repara, bg="blue", fg="white")
        self.btnorden_rep.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # PRESUPUESTOS COTIZACIONES - INGRESO VENTAS -------------------------------------------------
        photo3 = Image.open('presupuesto.png')
        photo3 = photo3.resize((80, 70), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo3 = ImageTk.PhotoImage(photo3)
        self.btnCotvta = Button(self.frame1, text="Cotizar/Venta", image=photo3, compound=TOP, pady=3, command=self.fCotVta,
                                border=3, bg="blue", fg="white")
        self.btnCotvta.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # PLANILLA DE CAJA ---------------------------------------------------------------------------
        photo4 = Image.open('planilla.png')
        photo4 = photo4.resize((80, 70), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo4 = ImageTk.PhotoImage(photo4)
        self.btnPlaniCaja = Button(self.frame1, text="Planilla Caja", image=photo4, compound=TOP, pady=3,
                                   command=self.fPlaniCaja, border=3, bg="blue", fg="white")
        self.btnPlaniCaja.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # CUENTA CORRIENTE ---------------------------------------------------------------------------
        photo5 = Image.open('ctacte.png')
        photo5 = photo5.resize((80, 70), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo5 = ImageTk.PhotoImage(photo5)
        self.btnCtacte = Button(self.frame1, text="Cuenta Corriente", image=photo5, compound=TOP, pady=3,
                                   command=self.fCtacte, border=3, bg="blue", fg="white")
        self.btnCtacte.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # SALIDA DEL SISTEMA -------------------------------------------------------------------------
        photo6 = Image.open('salida.png')
        photo6 = photo6.resize((80, 70), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo6 = ImageTk.PhotoImage(photo6)
        self.btnSalida = Button(self.frame1, text="Salir", image=photo6, compound=TOP, pady=3, command=self.fSalir,
                                border=3, bg="yellow", fg="Black")
        self.btnSalida.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # ------------------------------------------------------
        # BARRA MENU SUPERIOR

        # CLIENTES ---------------------------------------------------------------------------------
        photo7 = Image.open('clientes4.png')
        photo7 = photo7.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo7 = ImageTk.PhotoImage(photo7)
        self.btnClientes = Button(self.frame2, text="Clientes", image=photo7, compound=TOP, pady=3,
                                   command=self.fClientes, height=53, border=3, bg="blue", fg="white")
        self.btnClientes.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # GARANTIAS ---------------------------------------------------------------------------------
        photo8 = Image.open('garantia.png')
        photo8 = photo8.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo8 = ImageTk.PhotoImage(photo8)
        self.btnCtacte = Button(self.frame2, text="Garantias", image=photo8, compound=TOP, pady=3,
                                   command=self.fGarantia, height=53, border=3, bg="blue", fg="white")
        self.btnCtacte.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # RECIBOS ----------------------------------------------------------------------------------
        photo9 = Image.open('recibo.png')
        photo9 = photo9.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo9 = ImageTk.PhotoImage(photo9)
        self.btnRecibos = Button(self.frame2, text="Recibos", image=photo9, compound=TOP, pady=3,
                                   command=self.fRecibos, height=53, border=3, bg="blue", fg="white")
        self.btnRecibos.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # PRESUPUESTOS -----------------------------------------------------------------------------
        photo10 = Image.open('presuequipo.png')
        photo10 = photo10.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo10 = ImageTk.PhotoImage(photo10)
        self.btnPresupuestos = Button(self.frame2, text="Presupuestos", image=photo10, compound=TOP, pady=3,
                                   command=self.fPresupuestos, height=53, border=3, bg="blue", fg="white")
        self.btnPresupuestos.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # ARTICULOS FALTANTES -----------------------------------------------------------------------
        photo11 = Image.open('comprasmay.png')
        photo11 = photo11.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo11 = ImageTk.PhotoImage(photo11)
        self.btnartfaltantes = Button(self.frame2, text="Articulos faltantes", image=photo11, compound=TOP, pady=3,
                                   command=self.fCompras, height=53, border=3, bg="blue", fg="white")
        self.btnartfaltantes.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # RMA --------------------------------------------------------------------------------------
        photo12 = Image.open('rma.png')
        photo12 = photo12.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo12 = ImageTk.PhotoImage(photo12)
        self.btnrma = Button(self.frame2, text="Agenda Pendientes\n(RMA)", image=photo12, compound=TOP, pady=3,
                                   command=self.fRma, border=3, bg="blue", fg="white")
        self.btnrma.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # Respaldos --------------------------------------------------------------------------------
        photo13 = Image.open('backup.png')
        photo13 = photo13.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        photo13 = ImageTk.PhotoImage(photo13)
        self.btnbackup = Button(self.frame2, text="Backup", image=photo13, compound=TOP, pady=3,
                                   command=self.fBackup, height=53, border=3, bg="blue", fg="white")
        self.btnbackup.pack(side=LEFT, expand=1, fill=X, pady=5, padx=3)

        # PACKS cierre de pantalla ------------------------------------------------------------------
        self.frame1.pack(side=BOTTOM, fill=X, pady=10, padx=5)
        self.frame2.pack(side=TOP, fill=X, pady=10, padx=5)

        self.frame1.mainloop()

    def fPlaniCaja(selff):

        # PLANILLA DE CAJA

        vent = Toplevel()
        vent.title("Planilla de Caja")
        vent.grab_set()
        vent.focus_set()
        app = PlaniCaja(vent)  # clase definida en .py
        app.mainloop()

    def fCotVta(self):

        # VENTAS COTIZACIONES

        vent = Toplevel()
        vent.title("Cotizaciones/Ventas")
        vent.grab_set()
        vent.focus_set()
        app = VentCotiz(vent)  # clase definida en cotiz_vta.py
        app.mainloop()

    def m_orden_repara(self):

        # ORDENES DE REPARACION

        """ Defino una variable vent que toma valores de una pantalla "TOPLEVEL" dependiendo
        de master de principal entiendo ???ver eso de depender de principal """
        vent = Toplevel()
        vent.title("Ordenes de Reparacion")
        # Asigno la clase Ventart que esta en articulos.py a la variable app
        app = OrdenesRepara(vent)
        app.mainloop()

    def m_marcas(self):

        # MARCAS PRODUCTOS

        vent = Toplevel(self.master)
        vent.title("ABM Marcas de Articulos")
        vent.grab_set()
        vent.focus_set()
        app = Vent_marcas(vent)  # clase definida en marcas.py
        vent.mainloop()

    def fRubros(self):

        # RUBROS DE PRODUCTOS

        vent = Toplevel(self.master)
        vent.title("ABM Rubros de Articulos")
        vent.grab_set()
        vent.focus_set()
        app = Vent_rubros(vent)  # clase definida en rubros.py
        vent.mainloop()

    def fClientes(self):

        # CLIENTES

        vent = Toplevel(self.master)
        vent.title("ABM Clientes")
        vent.grab_set()
        vent.focus_set()
        app = Ventana(vent)  # clase definida en clientes.py
        vent.mainloop()

    def fProved(self):

        # PROVEEDORES

        vent = Toplevel(self.master)
        vent.title("ABM Proveedores")
        vent.grab_set()
        vent.focus_set()
        app = Ventproved(vent)  # clase definida en proved.py
        vent.mainloop()

    def fArticulos(self):

        # ARTICULOS

        """
        Defino una variable vent que toma valores de una pantalla "TOPLEVEL" dependiendo
        de master de principal entiendo ???ver eso de depender de principal
        """

        vent = Toplevel()
        vent.title("ABM Articulos")
        # Asigno la clase Ventart que esta en articulos.py a la variable app
        app = VentArt(vent)
        app.mainloop()

    def fCtacte(self):

        # CUENTAS CORRIENTES

        vent = Toplevel()
        vent.title("Cuentas Corrientes")
        vent.grab_set()
        vent.focus_set()
        app = CuentaCorriente(vent)  # clase definida en .py
        app.mainloop()

    def fGarantia(self):

        # GARANTIAS

        vent = Toplevel()
        vent.title("Garantias")
        vent.grab_set()
        vent.focus_set()
        app = clase_garantias(vent)  # clase definida en .py
        app.mainloop()

    def fRecibos(self):

        # RECIBOS

        vent = Toplevel()
        vent.title("Recibos")
        vent.grab_set()
        vent.focus_set()
        app = clase_recibos(vent)  # clase definida en .py
        app.mainloop()

    def fPresupuestos(self):

        # PRESUPUESTOS

        vent = Toplevel()
        vent.title("Presupuestos")
        vent.grab_set()
        vent.focus_set()
        app = clase_presupuestos(vent)  # clase definida en .py
        app.mainloop()

    def fCompras(self):

        # COMPRAS

        vent = Toplevel()
        vent.title("Articulos Faltantes")
        vent.grab_set()
        vent.focus_set()
        app = clase_compras(vent)
        app.mainloop()

    def fRma(self):

        # RMA

        vent = Toplevel()
        vent.title("RMA")
        vent.grab_set()
        vent.focus_set()
        app = clase_rma(vent)
        app.mainloop()

    def fBackup(self):

        # BACKUP

        vent = Toplevel()
        vent.title("Backup")
        vent.grab_set()
        vent.focus_set()
        app = clase_backup(vent)
        app.mainloop()

    def fConfiguracion(self):

        # CONFIGURACION

        """
        Defino una variable vent que toma valores de una pantalla "TOPLEVEL" dependiendo
        de master de principal entiendo ???ver eso de depender de principal
        """

        vent = Toplevel()
        vent.title("Configuracion - Parametros")
        vent.grab_set()
        vent.focus_set()
        app = Ventconfig(vent)
        app.mainloop()

    def fInf_ctacte(self):

        # INFORME DE CUENTA CORRIENTE

        vent = Toplevel()
        vent.title("Saldos en Cuentas Corrientes")
        vent.grab_set()
        vent.focus_set()
        app = Saldosctacte(vent)  # clase definida en .py
        app.mainloop()

    def fInf_tecnico(self):

        # INFORMES TECNICOS

        vent = Toplevel()
        vent.title("Informes tecnicos")
        vent.grab_set()
        vent.focus_set()
        app = clase_inf_tecnicos(vent)  # clase definida en .py
        app.mainloop()

    def fTecnicas(self):

        # INFORMACION TECNICA Y VIDEOS/CONSULTAS

        vent = Toplevel()
        vent.title("Guias Tecnicas")
        vent.grab_set()
        vent.focus_set()
        app = clase_GuiasTecnicas(vent)  # clase definida en .py
        app.mainloop()

    def fSalir(self):
        self.master.destroy()
