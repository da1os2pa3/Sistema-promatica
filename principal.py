""" Este es el modulo menu principal desde donde accedemos a cada ABM y proceso del sistema"""
from tkinter import Frame, LabelFrame, Button, Toplevel
from PIL import Image, ImageTk

#import locale
import tkinter as tk

from articulos import ClaseArticulos
from clientes import ClaseClientes
from compras import ClaseCompras
from configuracion import ClaseConfiguracion
from cotiz_vta import VentasPrincipal
from ctacte import ClaseCuentaCorriente
from garantias import ClaseGarantias
from guias_tecnicas import Clase_GuiasTecnicas
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

        # Imagen de fondo -------------------------------------------------------
        self.imagen = Image.open("promatica.jpg")
        # Redimension (Alto, Ancho)
        self.imagen = self.imagen.resize((self.ancho_ventana, self.alto_ventana), Image.Resampling.LANCZOS)
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
        menu_archivo.add_command(label='* Archivo de Marcas', command=self.fMarcas)
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

    def cuadro_cinta_superior(self):

        for c in range(8):
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

        # PRESUPUESTOS nuevo
        img = Image.open("presuequipo.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_presupuestos = Button(self.frame2, text="Presupuestos dos", compound="top", pady=3,
                                      command=self.fPresu_pest, height=53, border=3, bg="blue", fg="white")
        self.btn_presupuestos.image = icono
        self.btn_presupuestos.config(image=icono)
        self.btn_presupuestos.grid(row=0, column=7, padx=3, pady=3, sticky="nsew")




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
                                   command=self.forden_repara, bg="blue", fg="white")
        self.btn_orden_rep.image = icono
        self.btn_orden_rep.config(image=icono)
        self.btn_orden_rep.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")

        # PRESUPUESTOS COTIZACIONES - INGRESO VENTAS
        img = Image.open("presupuesto.png").resize((35, 35))
        icono = ImageTk.PhotoImage(img)
        self.btn_cotiz_vta = Button(self.frame1, text="Cotizar/Venta", compound="top", pady=3, command=self.fcotVta,
                                border=3, bg="blue", fg="white")
        self.btn_cotiz_vta.image = icono
        self.btn_cotiz_vta.config(image=icono)
        self.btn_cotiz_vta.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")

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

    # ----------------------------------------------------------------------------

    """ En los proximos metods, Defino una variable vent que toma valores de una pantalla "TOPLEVEL" dependiendo
        de master de principal entiendo ???ver eso de depender de principal """

    def fPlaniCaja(self):
        self.abrir_ventana(ClasePlaniCaja, "Planilla de caja")

    # def fPlaniCaja(self):
    #     # PLANILLA DE CAJA
    #     vent = Toplevel()
    #     vent.title("Planilla de Caja")
    #     vent.grab_set()
    #     vent.focus_set()
    #     app = PlaniCaja(vent)
    #     app.mainloop()

    # def fcotVta(self):
    #     self.abrir_ventana(Clase_CotizVenta, "Cotizaciones - Ventas")

    def fcotVta(self):
        self.abrir_ventana(VentasPrincipal, "Cotizaciones - Ventas")

    def forden_repara(self):
        self.abrir_ventana(ClaseOrdenesRepara, "Ordenes de reparacion")

    def fMarcas(self):
        self.abrir_ventana(ClaseMarcas, "Marcas")

    def fRubros(self):
        self.abrir_ventana(ClaseRubros, "Rubros de Articulos")

    def fClientes(self):
        self.abrir_ventana(ClaseClientes, "ABM Clientes")

    def fProved(self):
        self.abrir_ventana(ClaseProved, "ABM Proveeores")

    def fArticulos(self):
        self.abrir_ventana(ClaseArticulos, "ABM Articulos")

    def fCtacte(self):
        self.abrir_ventana(ClaseCuentaCorriente, "ABM Cuentas Corrientes")

    def fGarantia(self):
        self.abrir_ventana(ClaseGarantias, "Garantias")

    def fRecibos(self):
        self.abrir_ventana(ClaseRecibos, "Recibos")

    def fPresupuestos(self):
        self.abrir_ventana(Clase_Presupuestos, "Presupuestos")

    def fPresu_pest(self):
        self.abrir_ventana(ClasePresupuestos, "Presupuestos")

    def fCompras(self):
        self.abrir_ventana(ClaseCompras, "Articulos faltantes")

    def fRma(self):
        self.abrir_ventana(ClaseRma, "RMA")

    def fBackup(self):
        self.abrir_ventana(ClaseBackup, "Backup")

    def fConfiguracion(self):
        self.abrir_ventana(ClaseConfiguracion, "Configuracion - Parametros")

    def fInf_ctacte(self):
        self.abrir_ventana(ClaseSaldosCuentaCorriente, "Saldos en Cuentas Corrientes")

    def fInf_tecnico(self):
        self.abrir_ventana(ClaseInformeTecnico, "Informes tecnicos")

    def fTecnicas(self):
        self.abrir_ventana(Clase_GuiasTecnicas, "Guias tecnicas")
    # --------------------------------------------------------------------------

    def fSalir(self):
        self.master.destroy()



    def abrir_ventana(self, clase, titulo):

        vent = Toplevel(self.master) #Crea una nueva ventana hija de la ventana principal (self.master).
        vent.withdraw()              # Oculta la ventana
        vent.title(titulo)           # asignás el título:
        clase(vent)                  #
        vent.deiconify()             # La muestra cuando ya está construida
        vent.grab_set()              # Hace que esa ventana sea modal.
        vent.focus_set()