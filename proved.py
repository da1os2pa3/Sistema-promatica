from proved_ABM import *
from funciones import *
# ----------------------------------------
#from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#import tkinter as tk
# ----------------------------------------
from datetime import date
from datetime import datetime
from PIL import Image, ImageTk

class Ventproved(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # ---------------------------------------------------------------------------------
        # Seteo pantalla master principal
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # INSTANCIACIONES

        # Creo una instancia de clientesABM de la clase datosClientes
        self.varProved = datosProved(self.master)
        # ---------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # TITULOS

        # Esto esta agregado para centrar las ventanas en la pantalla
        master.resizable(0, 0)

        """ Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y ancho de la pantalla
        wtotal = master.winfo_screenwidth()
        htotal = master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 950
        hventana = 580
        # Aplicamos la siguiente fórmula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # --------------------------------------------------------------------------

        self.create_widgets()

        # --------------------------------------------------------------------------
        # VARIABLES Y ESTADO INICIAL

        self.estado_A()

        self.llena_grilla("")

        # ------------------------------------------------------------------------------
        # Carga del Treeview y seteo de foco y punteros sobre el mismo (grid)
        item = self.grid_proved.identify_row(0)
        self.grid_proved.selection_set(item)
        self.grid_proved.focus(item)
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Estado inicial del Gui
        self.habilitar_text("disabled")
        self.habilitar_btn_B("disabled")
        self.habilitar_btn_A("normal")

    def create_widgets(self):

        # ------------------------------------------------------------------------------
        # TITULOS

        # Encabezado logo y título con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el título
        self.photo3 = Image.open('proveedor.png')
        self.photo3 = self.photo3.resize((75, 75), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_proved = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_proved = Label(self.frame_titulo_top, image=self.png_proved, bg="red", relief=RIDGE, bd=5)
        self.lbl_titulo = Label(self.frame_titulo_top, width=25, text="Proveedores", bg="black", fg="gold",
                                font=("Arial bold", 38, "bold"), bd=5, relief=RIDGE, padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_proved.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES -*-

        # Se usa para saber que filtro está activo y mantenerlo hasta que el usuario lo quite en Reset
        self.filtro_activo = "proved ORDER BY denominacion ASC"
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.var_Id = -1
        self.alta_modif = 0
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS -*-

        self.strvar_codigo = tk.StringVar(value="")
        self.strvar_denominacion = tk.StringVar(value="")
        self.strvar_direccion = tk.StringVar(value="")
        self.strvar_localidad = tk.StringVar(value="")
        self.strvar_provincia = tk.StringVar(value="")
        self.strvar_postal = tk.StringVar(value="")
        self.strvar_telef1 = tk.StringVar(value="")
        self.strvar_telef2 = tk.StringVar(value="")
        self.strvar_mail = tk.StringVar(value="")
        self.strvar_fecha_alta = tk.StringVar(value="")
        self.strvar_contacto = tk.StringVar(value="")
        self.strvar_observaciones = tk.StringVar(value="")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # BOTONES -*-

        # Frame botones
        barra_botones = LabelFrame(self.master)

        botones1 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        # Instalacion botones
        self.btnNuevo = Button(botones1, text="Nuevo", command=self.fNuevo, bg="blue", fg="white", width=10)
        self.btnNuevo.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
        self.btnModificar = Button(botones1, text="Modificar", command=self.fModificar, bg="blue", fg="white",
                                   width=10)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=5, ipadx=10)
        self.btnEliminar = Button(botones1, text="Eliminar", command=self.fEliminar, bg="red", fg="white",
                                  width=10)
        self.btnEliminar.grid(row=2, column=0, padx=5, pady=5, ipadx=10)
        self.btnGuardar = Button(botones1, text="Guardar", command=self.fGuardar, bg="green", fg="white",
                                 width=10)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.btnCancelar = Button(botones1, text="Cancelar", command=self.fCancelar, bg="black", fg="white",
                                  width=10)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        botones1.pack(side=TOP, padx=3, pady=3, fill=Y)

        botones2 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        self.btn_orden_codigo = Button(botones2, text="Orden Codigo", width=11, command=self.forden_codigo,
                                       bg="grey", fg="white")
        self.btn_orden_codigo.grid(row=5, column=0, padx=6, pady=5, ipadx=10)
        self.btn_orden_nombre = Button(botones2, text="Orden Denomin.", width=11, command=self.forden_denominacion,
                                         bg="grey", fg="white")
        self.btn_orden_nombre.grid(row=6, column=0, padx=6, pady=5, ipadx=10)
        self.btn_reset = Button(botones2, text="Reset", width=11, command=self.fReset, bg="black", fg="white")
        self.btn_reset.grid(row=7, column=0, padx=6, pady=5, ipadx=10)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(botones2, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=8, column=0, padx=5, sticky="nsew", pady=5)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(botones2, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=9, column=0, padx=5, sticky="nsew", pady=5)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        botones2.pack(side=TOP, padx=3, pady=3, fill=Y)

        botones3 = LabelFrame(barra_botones)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 40), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = Button(botones3, text="Salir", image=self.photo3, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

        botones3.pack(side=TOP, padx=3, pady=3, fill=Y)

        # PACK Frame de botones
        barra_botones.pack(side=LEFT, padx=15, pady=5, ipady=5, fill=Y)
        # -------------------------------------------------------------------------------

        # Frame TREEVIEW y BUSQUEDA
        self.frame_tv = Frame(self.master)

        # -------------------------------------------------------------------------------
        # BUSQUEDA EN GRID

        # FRAME linea de busqueda
        self.frame_buscar = LabelFrame(self.frame_tv)
        self.lbl_buscar_proved = Label(self.frame_buscar, text="Buscar: ")
        self.lbl_buscar_proved.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_proved = Entry(self.frame_buscar, width=50)
        self.entry_buscar_proved.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.btn_buscar_proved = Button(self.frame_buscar, text="Buscar", command=self.fBuscar_en_tabla, bg="blue",
                                        fg="white", width=24)
        self.btn_buscar_proved.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_showall = Button(self.frame_buscar, text="Mostrar todo", command=self.fShowall, bg="blue",
                                        fg="white", width=25)
        self.btn_showall.grid(row=0, column=3, padx=5, pady=2, sticky=W)
        self.frame_buscar.pack(expand=1, fill=X, pady=10, padx=10)

        # ---------------------------------------------------------------------------
        # TREEVIEW

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.frame_tv)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_proved = ttk.Treeview(self.frame_tv, columns=("col1", "col2", "col3", "col4", "col5", "col6",
                                                                  "col7", "col8", "col9", "col10", "col11", "col12"))

        self.grid_proved.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_proved.column("#0", width=60, anchor=CENTER)
        self.grid_proved.column("col1", width=60, anchor=CENTER)
        self.grid_proved.column("col2", width=180, anchor=CENTER)
        self.grid_proved.column("col3", width=220, anchor=CENTER)
        self.grid_proved.column("col4", width=220, anchor=CENTER)
        self.grid_proved.column("col5", width=120, anchor=CENTER)
        self.grid_proved.column("col6", width=90, anchor=CENTER)
        self.grid_proved.column("col7", width=150, anchor=CENTER)
        self.grid_proved.column("col8", width=150, anchor=CENTER)
        self.grid_proved.column("col9", width=200, anchor=CENTER)
        self.grid_proved.column("col10", width=200, anchor=CENTER)
        self.grid_proved.column("col11", width=150, anchor=CENTER)
        self.grid_proved.column("col12", width=200, anchor=CENTER)

        self.grid_proved.heading("#0", text="Id", anchor=CENTER)
        self.grid_proved.heading("col1", text="Codigo", anchor=CENTER)
        self.grid_proved.heading("col2", text="Denominacion", anchor=CENTER)
        self.grid_proved.heading("col3", text="Direccion", anchor=CENTER)
        self.grid_proved.heading("col4", text="Localidad", anchor=CENTER)
        self.grid_proved.heading("col5", text="Provincia", anchor=CENTER)
        self.grid_proved.heading("col6", text="Postal", anchor=CENTER)
        self.grid_proved.heading("col7", text="Telfono 1", anchor=CENTER)
        self.grid_proved.heading("col8", text="Telfono 2", anchor=CENTER)
        self.grid_proved.heading("col9", text="E-mail", anchor=CENTER)
        self.grid_proved.heading("col10", text="Fecha alta", anchor=CENTER)
        self.grid_proved.heading("col11", text="Contacto", anchor=CENTER)
        self.grid_proved.heading("col12", text="Observaciones", anchor=CENTER)

        self.grid_proved.tag_configure('oddrow', background='light grey')
        self.grid_proved.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tv, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tv, orient=VERTICAL)
        self.grid_proved.config(xscrollcommand=scroll_x.set)
        self.grid_proved.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_proved.xview)
        scroll_y.config(command=self.grid_proved.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_proved['selectmode'] = 'browse'

        # PACK - del treeview y el FRAME tv
        self.frame_buscar.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=3)
        self.grid_proved.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
        self.frame_tv.pack(side=TOP, fill=BOTH, padx=5, pady=5)
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # ENTRYS -*-
        # ----------------------------------------------------------------------------

        self.sector_entry = LabelFrame(self.master)

        # CODIGO
        self.lbl_codigo = Label(self.sector_entry, text="Ultimo Codigo: ")
        self.lbl_codigo.grid(row=0, column=0, padx=10, pady=3, sticky=W)
        self.entry_codigo = Entry(self.sector_entry, textvariable=self.strvar_codigo, justify="right", width=10)
        self.strvar_codigo.trace("w", lambda *args: self.limitador(self.strvar_codigo, 5))
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=3, sticky=W)
        # APELLIDO
        self.lbl_denomin = Label(self.sector_entry, text="Denominacion: ")
        self.lbl_denomin.grid(row=1, column=0, padx=10, pady=3, sticky=W)
        self.entry_denomin = Entry(self.sector_entry, textvariable=self.strvar_denominacion, justify="left", width=40)
        self.strvar_denominacion.trace("w", lambda *args: self.limitador(self.strvar_denominacion, 30))
        self.entry_denomin.grid(row=1, column=1, padx=10, pady=3, sticky=W)
        # DIRECCION
        self.lbl_direccion = Label(self.sector_entry, text="Direccion: ")
        self.lbl_direccion.grid(row=2, column=0, padx=10, pady=3, sticky=W)
        self.entry_direccion = Entry(self.sector_entry, textvariable=self.strvar_direccion, justify="left", width=40)
        self.strvar_direccion.trace("w", lambda *args: self.limitador(self.strvar_direccion, 30))
        self.entry_direccion.grid(row=2, column=1, padx=10, pady=3, sticky=W)
        # LOCALIDAD
        self.lbl_localidad = Label(self.sector_entry, text="Localidad: ")
        self.lbl_localidad.grid(row=3, column=0, padx=10, pady=3, sticky=W)
        self.entry_localidad = Entry(self.sector_entry, textvariable=self.strvar_localidad, justify="left", width=40)
        self.strvar_localidad.trace("w", lambda *args: self.limitador(self.strvar_localidad, 30))
        self.entry_localidad.grid(row=3, column=1, padx=10, pady=3, sticky=W)
        # PROVINCIA
        self.lbl_provincia = Label(self.sector_entry, text="Provincia: ")
        self.lbl_provincia.grid(row=4, column=0, padx=10, pady=3, sticky=W)
        self.entry_provincia = Entry(self.sector_entry, textvariable=self.strvar_provincia, justify="left", width=40)
        self.strvar_provincia.trace("w", lambda *args: self.limitador(self.strvar_provincia, 15))
        self.entry_provincia.grid(row=4, column=1, padx=10, pady=3, sticky=W)
        # POSTAL
        self.lbl_postal = Label(self.sector_entry, text="Cod. Postal: ")
        self.lbl_postal.grid(row=5, column=0, padx=10, pady=3, sticky=W)
        self.entry_postal = Entry(self.sector_entry, textvariable=self.strvar_postal, justify="left", width=40)
        self.strvar_postal.trace("w", lambda *args: self.limitador(self.strvar_postal, 5))
        self.entry_postal.grid(row=5, column=1, padx=10, pady=3, sticky=W)
        # TELEFONO PERSONAL
        self.lbl_telefono1 = Label(self.sector_entry, text="Telefono 1: ")
        self.lbl_telefono1.grid(row=0, column=2, padx=10, pady=3, sticky=W)
        self.entry_telefono1 = Entry(self.sector_entry, textvariable=self.strvar_telef1, justify="left", width=40)
        self.strvar_telef1.trace("w", lambda *args: self.limitador(self.strvar_telef1, 15))
        self.entry_telefono1.grid(row=0, column=3, padx=10, pady=3, sticky=W)
        # TELEFONO TRABAJO
        self.lbl_telefono2 = Label(self.sector_entry, text="Telefono 2: ")
        self.lbl_telefono2.grid(row=1, column=2, padx=10, pady=3, sticky=W)
        self.entry_telefono2 = Entry(self.sector_entry, textvariable=self.strvar_telef2, justify="left", width=40)
        self.strvar_telef2.trace("w", lambda *args: self.limitador(self.strvar_telef2, 15))
        self.entry_telefono2.grid(row=1, column=3, padx=10, pady=3, sticky=W)
        # CORREO ELECTRONICO
        self.lbl_mail = Label(self.sector_entry, text="Correo Electronico: ")
        self.lbl_mail.grid(row=2, column=2, padx=10, pady=3, sticky=W)
        self.entry_mail = Entry(self.sector_entry, textvariable=self.strvar_mail, justify="left", width=40)
        self.strvar_mail.trace("w", lambda *args: self.limitador(self.strvar_mail, 30))
        self.entry_mail.grid(row=2, column=3, padx=10, pady=5, sticky=W)
        # FECHA DE INGRESO
        self.lbl_fecha_alta = Label(self.sector_entry, text="Fecha Alta: ")
        self.lbl_fecha_alta.grid(row=3, column=2, padx=10, pady=3, sticky=W)
        self.entry_fecha_alta = Entry(self.sector_entry, textvariable=self.strvar_fecha_alta, justify="left", width=40)
        self.entry_fecha_alta.bind("<FocusOut>", self.formato_fecha)
        # self.strvar_fecha_alta.trace("w", lambda *args: self.limitador(self.strvar_fecha_alta, 10))
        self.entry_fecha_alta.grid(row=3, column=3, padx=10, pady=3, sticky=W)
        # CONTACTO
        self.lbl_contacto = Label(self.sector_entry, text="Contacto: ")
        self.lbl_contacto.grid(row=4, column=2, padx=10, pady=3, sticky=W)
        self.entry_contacto = Entry(self.sector_entry, textvariable=self.strvar_contacto, justify="left", width=40)
        self.strvar_contacto.trace("w", lambda *args: self.limitador(self.strvar_contacto, 25))
        self.entry_contacto.grid(row=4, column=3, padx=10, pady=3, sticky=W)
        # OBSERVACIONES
        self.lbl_observaciones = Label(self.sector_entry, text="Observaciones: ")
        self.lbl_observaciones.grid(row=5, column=2, padx=10, pady=3, sticky=W)
        self.entry_observaciones = Entry(self.sector_entry, textvariable=self.strvar_observaciones, justify="left",
                                         width=40)
        self.strvar_observaciones.trace("w", lambda *args: self.limitador(self.strvar_observaciones, 50))
        self.entry_observaciones.grid(row=5, column=3, padx=10, pady=3, sticky=W)

        # PACK
        self.sector_entry.pack(expand=1, fill=BOTH, pady=5, padx=5)

    # ----------------------------------------------------------------------------
    # ESTADO INICIAL -*-
    # ----------------------------------------------------------------------------

    def estado_A(self):

        # Variables
        self.filtro_activo = "proved ORDER BY denominacion ASC"
        self.var_Id = -1
        self.alta_modif = 0

        # Grilla
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')

        # Estado inicial del Gui
        self.limpiar_text()
        self.habilitar_btn_A("normal")
        self.habilitar_btn_B("disabled")
        self.habilitar_text("disabled")

    def habilitar_btn_A(self, estado):

        self.btnNuevo.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btn_buscar_proved.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.entry_buscar_proved.configure(state=estado)

        self.btnFinarch.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btn_orden_codigo.configure(state=estado)
        self.btn_orden_nombre.configure(state=estado)

    def habilitar_btn_B(self, estado):

        self.btnGuardar.configure(state=estado)

    # ----------------------------------------------------------------------------
    # GRID -*-
    # ----------------------------------------------------------------------------

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varProved.consultar_proved(self.filtro_activo)
        else:
            datos = self.varProved.consultar_proved("proved ORDER BY denominacion ASC")

        cont = 0
        for row in datos:

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[10], '%Y-%m-%d'), "hora_no")

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)
            self.grid_proved.insert("", END, tags=color, text=row[0], values=(row[1], row[2], row[3], row[4],
                                              row[5], row[6], row[7], row[8], row[9], forma_normal, row[11], row[12]))

        if len(self.grid_proved.get_children()) > 0:
            self.grid_proved.selection_set(self.grid_proved.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_proved.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_proved.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """
            """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_proved.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_proved.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_proved.yview(self.grid_proved.index(rg))
            return

        self.mover_puntero_topend("END")

    def habilitar_text(self, estado):

        # Agregado para manejar tema de readonly y que no quede el código escrito al limpiar
        self.entry_codigo.configure(state="normal")

        self.entry_codigo.delete(0, END)
        self.entry_codigo.configure(state=estado)
        self.entry_denomin.configure(state=estado)
        self.entry_direccion.configure(state=estado)
        self.entry_localidad.configure(state=estado)
        self.entry_provincia.configure(state=estado)
        self.entry_postal.configure(state=estado)
        self.entry_telefono1.configure(state=estado)
        self.entry_telefono2.configure(state=estado)
        self.entry_mail.configure(state=estado)
        self.entry_fecha_alta.configure(state=estado)
        self.entry_contacto.configure(state=estado)
        self.entry_observaciones.configure(state=estado)

        if self.alta_modif == 1:
            self.grid_proved['selectmode'] = 'none'
            self.grid_proved.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif == 2 or self.alta_modif == 0:
            self.grid_proved['selectmode'] = 'browse'
            self.grid_proved.bind("<Double-Button-1>", self.DobleClickGrid)

    def fNo_modifique(self, event):
        return

    def limpiar_text(self):

        self.entry_codigo.delete(0, END)
        self.entry_denomin.delete(0, END)
        self.entry_direccion.delete(0, END)
        self.entry_localidad.delete(0, END)
        self.entry_provincia.delete(0, END)
        self.entry_postal.delete(0, END)
        self.entry_telefono1.delete(0, END)
        self.entry_telefono2.delete(0, END)
        self.entry_mail.delete(0, END)
        self.entry_fecha_alta.delete(0, END)
        self.entry_contacto.delete(0, END)
        self.entry_observaciones.delete(0, END)

    def limpiar_Grid(self):

        for item in self.grid_proved.get_children():
            self.grid_proved.delete(item)

    def forden_codigo(self):

        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.filtro_activo = "proved ORDER BY codigo ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)
        self.puntero_modificacion(self.clave)

    def forden_denominacion(self):

        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.filtro_activo = "proved ORDER BY denominacion ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)
        self.puntero_modificacion(self.clave)

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.entry_buscar_proved.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.entry_buscar_proved.get()
        self.filtro_activo = "proved WHERE INSTR(denominacion, '" + se_busca + "') > 0" \
                             + " ORDER BY denominacion ASC"

        self.varProved.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_proved.selection()
        self.grid_proved.focus(item)

    def fShowall(self):

        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.filtro_activo = "proved ORDER BY denominacion ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    def DobleClickGrid(self, event):
        self.fModificar()

    # ----------------------------------------------------------------------------
    # CRUD -*-
    # ----------------------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")
        self.limpiar_text()
        # Obtengo el codigo en secuencia y pongo el entry en disabled para no modificar
        self.entry_codigo.insert(0, (int(self.varProved.traer_ultimo(1))) + 1)
        self.entry_codigo.configure(state="readonly")
        self.entry_localidad.insert(0, "Villa Carlos Paz")
        self.entry_provincia.insert(0, "Cordoba")
        self.entry_postal.insert(0, "5152")
        # Cambio el formato de la fecha
        una_fecha = date.today()
        self.entry_fecha_alta.insert(0, una_fecha.strftime('%d/%m/%Y'))
        self.entry_denomin.focus()

    def fModificar(self):

        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        self.var_Id = self.clave
        self.habilitar_text("normal")
        self.limpiar_text()

        self.filtro_activo = "proved WHERE Id = " + str(self.clave)

        valores = self.varProved.consultar_proved(self.filtro_activo)

        for row in valores:

            self.entry_codigo.insert(0, row[1])
            self.entry_denomin.insert(0, row[2])
            self.entry_direccion.insert(0, row[3])
            self.entry_localidad.insert(0, row[4])
            self.entry_provincia.insert(0, row[5])
            self.entry_postal.insert(0, row[6])
            self.entry_telefono1.insert(0, row[7])
            self.entry_telefono2.insert(0, row[8])
            self.entry_mail.insert(0, row[9])

            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[10], "%Y-%m-%d"), "hora_no")
            self.entry_fecha_alta.insert(0, fecha_convertida)
            self.entry_contacto.insert(0, row[11])
            self.entry_observaciones.insert(0, row[12])

            self.entry_codigo.configure(state="readonly")

        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")
        self.entry_denomin.focus()

    def fEliminar(self):

        self.selected = self.grid_proved.focus()
        self.selected_ant = self.grid_proved.prev(self.selected)
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.clave_ant = self.grid_proved.item(self.selected_ant, 'text')

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el GRID
        valores = self.grid_proved.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        self.varProved.eliminar_proved(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # control de codigo repetido (en funciones)
        codrep = codigo_repetido(self.strvar_codigo.get(), "proved", "codigo")

        if self.alta_modif == 1:
            # si viene algun dato, es que el codigo ya existe
            if len(codrep) > 0:
                messagebox.showerror("Error", "Codigo ya existe en la tabla - verifique", parent=self)
                self.entry_denomin.focus()
                return

        # --------------------------------------------------------------------
        # VALIDACION QUE EXISTA APELLIDO
        if self.strvar_denominacion.get() == "":
            messagebox.showwarning("Alerta", "No ingreso denominacion", parent=self)
            self.entry_denomin.focus()
            return
        # --------------------------------------------------------------------
        try:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori
            self.selected = self.grid_proved.focus()
            # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
            self.clave = self.grid_proved.item(self.selected, 'text')
            self.nuevo_prov = ""

            if self.alta_modif == 1:

                self.nuevo_prov = str(self.strvar_codigo.get())

                self.varProved.insertar_proved(self.strvar_codigo.get(), self.strvar_denominacion.get(),
                                               self.strvar_direccion.get(), self.strvar_localidad.get(),
                                               self.strvar_provincia.get(), self.strvar_postal.get(),
                                               self.strvar_telef1.get(), self.strvar_telef2.get(),
                                               self.strvar_mail.get(), self.strvar_fecha_alta.get(),
                                               self.strvar_contacto.get(), self.strvar_observaciones.get())

                messagebox.showinfo("Guardar", "Nuevo registro creado correctamente", parent=self)

            elif self.alta_modif == 2:

                self.varProved.modificar_proved(self.var_Id, self.strvar_codigo.get(),
                                                    self.strvar_denominacion.get(), self.strvar_direccion.get(),
                                                    self.strvar_localidad.get(), self.strvar_provincia.get(),
                                                    self.strvar_postal.get(), self.strvar_telef1.get(),
                                                    self.strvar_telef2.get(), self.strvar_mail.get(),
                                                    self.strvar_fecha_alta.get(), self.strvar_contacto.get(),
                                                    self.strvar_observaciones.get())

                self.var_Id == -1
                messagebox.showinfo("Modificacion", "Modificacion del registro fue exitosa", parent=self)

            self.filtro_activo = "proved ORDER BY denominacion"

            self.limpiar_Grid()
            self.limpiar_text()
            self.habilitar_btn_B("disabled")
            self.habilitar_btn_A("normal")

            if self.alta_modif == 1:
                ultimo_tabla_id = self.varProved.traer_ultimo(0)
                self.llena_grilla(ultimo_tabla_id)
            elif self.alta_modif == 2:
                self.llena_grilla(self.clave)

            self.alta_modif = 0

            # ojo este debe ir aca abajo sino da problema el browse del grid
            self.habilitar_text("disabled")

        except:

            messagebox.showerror("Error", "Revise datos ingresados por favor", parent=self)
            self.entry_fecha_ingreso.focus()
            return

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_A()

    def fReset(self):

        self.estado_A()
        self.limpiar_Grid()
        self.llena_grilla("")
        self.mover_puntero_topend("TOP")

    def fSalir(self):
        self.master.destroy()

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:caract])

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar all sus valores posibles, le paso la
        fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_alta.get()

        # FUNCION VALIDA FECHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_alta.get())

        if retorno_VerFal == "":
            self.strvar_fecha_alta.set(value=estado_antes)
            self.entry_fecha_alta.focus()
            return
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.entry_fecha_alta.focus()
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_alta.set(value=estado_antes)
            self.entry_fecha_alta.focus()
            return
        elif retorno_VerFal == "BLANCO":
            return
        else:
            self.strvar_fecha_alta.set(retorno_VerFal)

    # ----------------------------------------------------------------------------
    # PUNTEROS -*-
    # ----------------------------------------------------------------------------

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_proved.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_proved.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_proved.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_proved.yview(self.grid_proved.index(self.grid_proved.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_proved.get_children()
            # Barro la lista y me quedo con el ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_proved.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_proved.focus(rg)
            # lleva el foco al final del treeview
            self.grid_proved.yview(self.grid_proved.index(self.grid_proved.get_children()[-1]))
