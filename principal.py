""" Este es el modulo menu principal desde donde accedemos a cada ABM y proceso del sistema"""
# import locale
import tkinter as tk
from tkinter import Frame, LabelFrame, Button, Toplevel
from tkinter import messagebox

from PIL import Image, ImageTk

from articulos import ClaseArticulos
from clientes import ClaseClientes
from compras import ClaseCompras
from configuracion import ClaseConfiguracion
from cotiz_vta import VentasPrincipal
from ctacte import ClaseCuentaCorriente
from garantias import ClaseGarantias
#from guias_tecnicas import Clase_GuiasTecnicas
from inf_tecnicos import ClaseInformeTecnico
from marcas import ClaseMarcas
from orden_reparacion import ClaseOrdenesRepara
from planilla_caja import ClasePlaniCaja
from presup_nuevo import ClasePresupuestos
from presupuestos import Clase_Presupuestos
from proved import ClaseProved
from recibos import ClaseRecibos
from respaldos import ClaseBackup
from rma import ClaseRma
from rubros import ClaseRubros
from saldosctacte import ClaseSaldosCuentaCorriente

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

        # locale.setlocale(locale.LC_ALL, '')
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

        # -----------------------------------------------------------------------
        # Acá el error no debería frenar el arranque del sistema — si falta la imagen, mejor
        # mostrar la ventana sin fondo que no mostrar nada.
        try:
            self.imagen = Image.open("promatica.jpg")
            self.imagen = self.imagen.resize((self.ancho_ventana, self.alto_ventana), Image.Resampling.LANCZOS)
            self.fondo = ImageTk.PhotoImage(self.imagen)
            self.label_fondo = tk.Label(self.master, image=self.fondo)
            self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("No se encontró la imagen de fondo, se continúa sin ella")
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
        menu_archivo.add_command(label='* Archivo de Clientes', command=self.fclientes)
        menu_archivo.add_command(label='* Archivo de Proveedores', command=self.fproved)
        menu_archivo.add_command(label='* Archivo de Marcas', command=self.fmarcas)
        menu_archivo.add_command(label='* Archivo de Rubros', command=self.frubros)
        menu_archivo.add_command(label='* Configuracion', command=self.fconfiguracion)

        menu_informes = tk.Menu(menu_principal, tearoff=0)
        menu_informes.add_command(label='* Saldos cuenta corriente', command=self.finf_ctacte)
        menu_informes.add_command(label='* Informes Tecnicos', command=self.finf_tecnico)

        menu_tecnica = tk.Menu(menu_principal, tearoff=0)
        menu_tecnica.add_command(label='* Guias Tecnicas', command=self.ftecnicas)

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
        self.frame2.pack(side="top", fill="x", pady=3, padx=5)

    def cuadro_cinta_superior(self):

        for c in range(7):
            self.frame2.grid_columnconfigure(c, weight=1, minsize=100)

        # CLIENTES
        self.btn_clientes = self.crear_boton(self.frame2, "Clientes", "clientes4.png", self.fclientes, col=0, height=53)
        # GARANTIAS
        self.btn_garantia = self.crear_boton(self.frame2, "Garantias", "garantia.png", self.fgarantia, col=1, height=53)
        # RECIBOS
        self.btn_recibos = self.crear_boton(self.frame2, "Recibos", "recibo.png", self.frecibos, col=2, height=53)
        # # PRESUPUESTOS
        # self.btn_presupuestos = self.crear_boton(self.frame2, "Presupuestos", "presuequipo.png", self.fpresupuestos,
        #                                          col=3, height=53)
        # ARTICULOS FALTANTES
        self.btn_art_faltantes = self.crear_boton(self.frame2, "Compras\nArticulos", "comprasmay.png", self.fcompras,
                                                  col=3, height=53)
        # Pendientes
        self.btn_rma = self.crear_boton(self.frame2, "Agenda\nPendientes", "rma.png", self.frma, col=4, height=53)
        # Respaldos
        self.btn_backup = self.crear_boton(self.frame2, "Backups", "backup.png", self.fbackup, col=5, height=53)
        # PRESUPUESTOS nuevo
        self.btn_presupuestos2 = self.crear_boton(self.frame2, "Presupuestos", "presuequipo.png", self.fpresu_pest,
                                                  col=6, height=53)

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame2.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def cuadro_cinta_inferior(self):

        for c in range(6):
            self.frame1.grid_columnconfigure(c, weight=1, minsize=100)

        # ARTICULOS CRUD - ABM
        icono = self.cargar_icono("productos.png")
        self.btn_articulos = Button(self.frame1, text="Articulos", compound="top", pady=3, border=3,
                                   command=self.farticulos, bg="blue", fg="white")
        self.btn_articulos.image = icono
        self.btn_articulos.config(image=icono)
        self.btn_articulos.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        # ORDENES DE REPARACION
        icono = self.cargar_icono("reparar.png")
        self.btn_orden_rep = Button(self.frame1, text="Orden Reparacion", compound="top", pady=3, border=3,
                                   command=self.forden_repara, bg="blue", fg="white")
        self.btn_orden_rep.image = icono
        self.btn_orden_rep.config(image=icono)
        self.btn_orden_rep.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")

        # PRESUPUESTOS COTIZACIONES - INGRESO VENTAS
        icono = self.cargar_icono("presupuesto.png")
        self.btn_cotiz_vta = Button(self.frame1, text="Cotizar/Venta", compound="top", pady=3, command=self.fcotiza_venta,
                                border=3, bg="blue", fg="white")
        self.btn_cotiz_vta.image = icono
        self.btn_cotiz_vta.config(image=icono)
        self.btn_cotiz_vta.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")

        # PLANILLA DE CAJA
        img = Image.open("planilla.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_planicaja = Button(self.frame1, text="Planilla Caja", compound="top", pady=3, command=self.fplani_caja,
                                   border=3, bg="blue", fg="white")
        self.btn_planicaja.image = icono
        self.btn_planicaja.config(image=icono)
        self.btn_planicaja.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")

        # CUENTA CORRIENTE
        icono = self.cargar_icono("ctacte.png")
        self.btnCtacte = Button(self.frame1, text="Cuenta Corriente", compound="top", pady=3, command=self.fctacte,
                                border=3, bg="blue", fg="white")
        self.btnCtacte.image = icono
        self.btnCtacte.config(image=icono)
        self.btnCtacte.grid(row=0, column=4, padx=3, pady=3, sticky="nsew")

        # SALIDA DEL SISTEMA
        icono = self.cargar_icono("salida.png")
        self.btnSalida = Button(self.frame1, text="Salir", compound="top", pady=3, command=self.fsalir, border=3,
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

    # ----------------------------------------------------------------------------

    """ En los proximos metods, Defino una variable vent que toma valores de una pantalla "TOPLEVEL" dependiendo
        de master de principal entiendo ???ver eso de depender de principal """

    def fplani_caja(self):
        self.abrir_ventana(ClasePlaniCaja, "Planilla de caja")
    def fcotiza_venta(self):
        self.abrir_ventana(VentasPrincipal, "Cotizaciones - Ventas")
    def forden_repara(self):
        self.abrir_ventana(ClaseOrdenesRepara, "Ordenes de reparacion")
    def fmarcas(self):
        self.abrir_ventana(ClaseMarcas, "Marcas")
    def frubros(self):
        self.abrir_ventana(ClaseRubros, "Rubros de Articulos")
    def fclientes(self):
        self.abrir_ventana(ClaseClientes, "ABM Clientes")
    def fproved(self):
        self.abrir_ventana(ClaseProved, "ABM Proveeores")
    def farticulos(self):
        self.abrir_ventana(ClaseArticulos, "ABM Articulos")
    def fctacte(self):
        self.abrir_ventana(ClaseCuentaCorriente, "ABM Cuentas Corrientes")
    def fgarantia(self):
        self.abrir_ventana(ClaseGarantias, "Garantias")
    def frecibos(self):
        self.abrir_ventana(ClaseRecibos, "Recibos")
    def fpresupuestos(self):
        pass
        #self.abrir_ventana(Clase_Presupuestos, "Presupuestos")
    def fpresu_pest(self):
        self.abrir_ventana(ClasePresupuestos, "Presupuestos")
    def fcompras(self):
        self.abrir_ventana(ClaseCompras, "Articulos faltantes")
    def frma(self):
        self.abrir_ventana(ClaseRma, "RMA")
    def fbackup(self):
        self.abrir_ventana(ClaseBackup, "Backup")
    def fconfiguracion(self):
        self.abrir_ventana(ClaseConfiguracion, "Configuracion - Parametros")
    def finf_ctacte(self):
        self.abrir_ventana(ClaseSaldosCuentaCorriente, "Saldos en Cuentas Corrientes")
    def finf_tecnico(self):
        self.abrir_ventana(ClaseInformeTecnico, "Informes tecnicos")
    def ftecnicas(self):
        pass
        #self.abrir_ventana(Clase_GuiasTecnicas, "Guias tecnicas")
    # --------------------------------------------------------------------------

    def fsalir(self):
        self.master.destroy()

    def abrir_ventana(self, clase, titulo):
        try:
            vent = Toplevel(self.master)
            vent.withdraw()
            vent.title(titulo)
            clase(vent)
            vent.deiconify()
            vent.grab_set()
            vent.focus_set()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir '{titulo}':\n{e}")
            vent.destroy()

    @staticmethod
    def crear_boton(frame, texto, imagen, comando, col, row=0, **kwargs):
        try:
            img = Image.open(imagen).resize((35, 35))
            icono = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            icono = None
        btn = Button(frame, text=texto, image=icono, compound="top", pady=13,
                     command=comando, border=3, bg="blue", fg="white", **kwargs)
        btn.image = icono
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        return btn

    @staticmethod
    def cargar_icono(path, size=(35, 35)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
