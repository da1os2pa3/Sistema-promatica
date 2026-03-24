""" Este es el modulo menu principal desde donde accedemos a cada ABM y proceso del sistema"""
import locale
import tkinter as tk
from PIL.Image import Resampling

from articulos import VentArt
from clientes import Ventana
from compras import clase_compras
from configuracion import *
from cotiz_vta import *
from ctacte import CuentaCorriente
from garantias import clase_garantias
from guias_tecnicas import clase_GuiasTecnicas
from inf_tecnicos import clase_inf_tecnicos
from marcas import Vent_marcas
from orden_reparacion import *
from planilla_caja import PlaniCaja
from presupuestos import clase_presupuestos
from proved import *
from recibos import clase_recibos
from respaldos import *
from rma import clase_rma
from rubros import Vent_rubros
from saldosctacte import Saldosctacte

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
        super().__init__(master)

        # propiedades instanciamientos (serian las variables de la clase)
        self.master = master

        locale.setlocale(locale.LC_ALL, '')
        # locale.setlocale(locale.LC_ALL, 'ar_AR')
        # print(locale.localeconv())

        # ---------------------------------------------------------------------
        # PARAMETRIZO LA PANTALLA
        # ---------------------------------------------------------------------

        # Determino ancho y alto de pantalla ----------------------------------
        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()
        # asigno el 70% para que no me ocupe toda el area
        self.ancho_ventana = int(ancho * 0.6)
        self.alto_ventana = int(alto * 0.6)
        # Calcular posición para centrar
        x = int((ancho - self.ancho_ventana) / 2)
        y = int((alto - self.alto_ventana) / 2)
        self.master.geometry(f"{self.ancho_ventana}x{self.alto_ventana}+{x}+{y}")
        # ----------------------------------------------------------------------

        # Imagen de fondo -------------------------------------------------------
        self.imagen = Image.open("promatica.jpg")
        self.imagen = self.imagen.resize((self.ancho_ventana, self.alto_ventana), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.fondo = ImageTk.PhotoImage(self.imagen)
        self.label_fondo = tk.Label(self.master, image=self.fondo)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        # self.master.bind("<Configure>", self.ajustar_fondo)
        #tk.Label(self.master, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
        # -----------------------------------------------------------------------

        # Barra de titulo superior ----------------------------------------------
        label1 = tk.Label(self.master, text='Gestion Comercial - Promatica Computacion', bg="black", fg="gold",
                       font=("times new roman", 30, "bold"), bd=12, relief="ridge")
        label1.pack(side="top", fill="x", pady=10, padx=5)
        # -----------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # BARRA DE MENU
        # ---------------------------------------------------------------------
        menu_principal = tk.Menu(self.master)
        menu_archivo = tk.Menu(menu_principal, tearoff=0)
        menu_archivo.add_command(label='* Archivo de Clientes', command=self.fClientes)
        menu_archivo.add_command(label='* Archivo de Proveedores', command=self.fProved)
        menu_archivo.add_command(label='* Archivo de Marcas', command=self.m_marcas)
        menu_archivo.add_command(label='* Archivo de Rubros', command=self.fRubros)
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
        # ---------------------------------------------------------------------

        self.create_widgets()

    def create_widgets(self):

        # ---------------------------------------------------------------
        # CINTA MENU INFERIOR
        # ---------------------------------------------------------------
        self.frame1 = LabelFrame(self.master, bg="#bfdaff")
        self.cuadro_cinta_inferior()
        self.frame1.pack(side="bottom", fill="x", pady=10, padx=5)

        # ------------------------------------------------------
        # CINTA MENU SUPERIOR
        # ------------------------------------------------------
        self.frame2 = LabelFrame(self.master, bg="#bfdaff")
        self.cuadro_cinta_superior()
        self.frame2.pack(side="top", fill="x", pady=10, padx=5)

        self.master.mainloop()


    # def ajustar_fondo(self, event):
    #
    #     if event.width < 10 or event.height < 10:
    #         return
    #
    #     imagen_redimensionada = self.imagen.resize(
    #         (event.width, event.height),
    #         Image.Resampling.LANCZOS
    #     )
    #
    #     self.fondo = ImageTk.PhotoImage(imagen_redimensionada)
    #     self.label_fondo.config(image=self.fondo)


    def cuadro_cinta_superior(self):

        for c in range(7):
            self.frame2.grid_columnconfigure(c, weight=1, minsize=100)

        # CLIENTES
        img = Image.open("clientes4.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_clientes = Button(self.frame2, text="Clientes",compound="top", pady=3,
                                   command=self.fClientes, height=53, border=3, bg="blue", fg="white")
        self.btn_clientes.image = icono
        self.btn_clientes.config(image=icono)
        self.btn_clientes.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        # GARANTIAS
        img = Image.open("garantia.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_ctacte = Button(self.frame2, text="Garantias", compound="top", pady=3, command=self.fGarantia,
                                 height=53, border=3, bg="blue", fg="white")
        self.btn_ctacte.image = icono
        self.btn_ctacte.config(image=icono)
        self.btn_ctacte.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")

        # RECIBOS
        img = Image.open("recibo.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_recibos = Button(self.frame2, text="Recibos", compound="top", pady=3, command=self.fRecibos, height=53,
                                 border=3, bg="blue", fg="white")
        self.btn_recibos.image = icono
        self.btn_recibos.config(image=icono)
        self.btn_recibos.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")

        # PRESUPUESTOS
        img = Image.open("presuequipo.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_presupuestos = Button(self.frame2, text="Presupuestos", compound="top", pady=3,
                                      command=self.fPresupuestos, height=53, border=3, bg="blue", fg="white")
        self.btn_presupuestos.image = icono
        self.btn_presupuestos.config(image=icono)
        self.btn_presupuestos.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")

        # ARTICULOS FALTANTES
        img = Image.open("comprasmay.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_art_faltantes = Button(self.frame2, text="Articulos\na comprar", compound="top", pady=3,
                                   command=self.fCompras, height=53, border=3, bg="blue", fg="white")
        self.btn_art_faltantes.image = icono
        self.btn_art_faltantes.config(image=icono)
        self.btn_art_faltantes.grid(row=0, column=4, padx=3, pady=3, sticky="nsew")

        # Pendientes
        img = Image.open("rma.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_rma = Button(self.frame2, text="Agenda\nPendientes", compound="top", pady=3, command=self.fRma,
                             border=3, bg="blue", fg="white")
        self.btn_rma.image = icono
        self.btn_rma.config(image=icono)
        self.btn_rma.grid(row=0, column=5, padx=3, pady=3, sticky="nsew")

        # Respaldos
        img = Image.open("backup.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_backup = Button(self.frame2, text="Backup", compound="top", pady=3, command=self.fBackup, height=53,
                                border=3, bg="blue", fg="white")
        self.btn_backup.image = icono
        self.btn_backup.config(image=icono)
        self.btn_backup.grid(row=0, column=6, padx=3, pady=3, sticky="nsew")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame2.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def cuadro_cinta_inferior(self):

        for c in range(6):
            self.frame1.grid_columnconfigure(c, weight=1, minsize=100)

        # ARTICULOS CRUD - ABM
        img = Image.open("productos.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_articulos = Button(self.frame1, text="Articulos", compound="top", pady=3, border=3,
                                   command=self.fArticulos, bg="blue", fg="white")
        self.btn_articulos.image = icono
        self.btn_articulos.config(image=icono)
        self.btn_articulos.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        # ORDENES DE REPARACION
        img = Image.open("reparar.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_orden_rep = Button(self.frame1, text="Orden Reparacion", compound="top", pady=3, border=3,
                                   command=self.m_orden_repara, bg="blue", fg="white")
        self.btn_orden_rep.image = icono
        self.btn_orden_rep.config(image=icono)
        self.btn_orden_rep.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")

        # PRESUPUESTOS COTIZACIONES - INGRESO VENTAS
        img = Image.open("presupuesto.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_presupuestos = Button(self.frame1, text="Cotizar/Venta", compound="top", pady=3, command=self.fCotVta,
                                border=3, bg="blue", fg="white")
        self.btn_presupuestos.image = icono
        self.btn_presupuestos.config(image=icono)
        self.btn_presupuestos.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")

        # PLANILLA DE CAJA
        img = Image.open("planilla.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_planicaja = Button(self.frame1, text="Planilla Caja", compound="top", pady=3, command=self.fPlaniCaja,
                                   border=3, bg="blue", fg="white")
        self.btn_planicaja.image = icono
        self.btn_planicaja.config(image=icono)
        self.btn_planicaja.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")

        # CUENTA CORRIENTE
        img = Image.open("ctacte.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btnCtacte = Button(self.frame1, text="Cuenta Corriente", compound="top", pady=3, command=self.fCtacte,
                                border=3, bg="blue", fg="white")
        self.btnCtacte.image = icono
        self.btnCtacte.config(image=icono)
        self.btnCtacte.grid(row=0, column=4, padx=3, pady=3, sticky="nsew")

        # SALIDA DEL SISTEMA
        img = Image.open("salida.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btnSalida = Button(self.frame1, text="Salir", compound="top", pady=3, command=self.fSalir, border=3,
                                bg="yellow", fg="Black")
        self.btnSalida.image = icono
        self.btnSalida.config(image=icono)
        self.btnSalida.grid(row=0, column=5, padx=3, pady=3, sticky="nsew")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame1.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def fsale_menu(self):

        self.master.quit()
        self.master.destroy()

    """ En los proximos metods, Defino una variable vent que toma valores de una pantalla "TOPLEVEL" dependiendo
        de master de principal entiendo ???ver eso de depender de principal """

    def fPlaniCaja(self):

        # PLANILLA DE CAJA

        vent = Toplevel()
        vent.title("Planilla de Caja")
        vent.grab_set()
        vent.focus_set()
        app = PlaniCaja(vent)
        app.mainloop()

    def fCotVta(self):

        # VENTAS COTIZACIONES

        vent = Toplevel()
        vent.title("Cotizaciones/Ventas")
        vent.grab_set()
        vent.focus_set()
        app = VentCotiz(vent)
        app.mainloop()

    def m_orden_repara(self):

        # ORDENES DE REPARACION

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
        app = Vent_marcas(vent)
        vent.mainloop()

    def fRubros(self):

        # RUBROS DE PRODUCTOS

        vent = Toplevel(self.master)
        vent.title("ABM Rubros de Articulos")
        vent.grab_set()
        vent.focus_set()
        app = Vent_rubros(vent)
        vent.mainloop()

    def fClientes(self):

        # CLIENTES

        vent = Toplevel(self.master)
        vent.title("ABM Clientes")
        vent.grab_set()
        vent.focus_set()
        app = Ventana(vent)
        vent.mainloop()

    def fProved(self):

        # PROVEEDORES

        vent = Toplevel(self.master)
        vent.title("ABM Proveedores")
        vent.grab_set()
        vent.focus_set()
        app = Ventproved(vent)
        vent.mainloop()

    def fArticulos(self):

        # ARTICULOS

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
        app = CuentaCorriente(vent)
        app.mainloop()

    def fGarantia(self):

        # GARANTIAS

        vent = Toplevel()
        vent.title("Garantias")
        vent.grab_set()
        vent.focus_set()
        app = clase_garantias(vent)
        app.mainloop()

    def fRecibos(self):

        # RECIBOS

        vent = Toplevel()
        vent.title("Recibos")
        vent.grab_set()
        vent.focus_set()
        app = clase_recibos(vent)
        app.mainloop()

    def fPresupuestos(self):

        # PRESUPUESTOS

        vent = Toplevel()
        vent.title("Presupuestos")
        vent.grab_set()
        vent.focus_set()
        app = clase_presupuestos(vent)
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
        app = Saldosctacte(vent)
        app.mainloop()

    def fInf_tecnico(self):

        # INFORMES TECNICOS

        vent = Toplevel()
        vent.title("Informes tecnicos")
        vent.grab_set()
        vent.focus_set()
        app = clase_inf_tecnicos(vent)
        app.mainloop()

    def fTecnicas(self):

        # INFORMACION TECNICA Y VIDEOS/CONSULTAS

        vent = Toplevel()
        vent.title("Guias Tecnicas")
        vent.grab_set()
        vent.focus_set()
        app = clase_GuiasTecnicas(vent)
        app.mainloop()

    def fSalir(self):
        self.master.destroy()
