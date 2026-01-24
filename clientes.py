from funciones import *
from clientes_ABM import *
#-------------------------------------------------
from tkinter import messagebox
#import tkinter as tk
import tkinter.font as tkFont
#-------------------------------------------------
from datetime import date
from datetime import datetime
from PIL import Image, ImageTk

class Ventana(Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master

        # Seteo pantalla master principal -------------------------------------------------
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # Instanciaciones -*-
        # Creo una instancia de clientesABM de la clase datosClientes
        self.varClientes = datosClientes(self.master)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # PANTALLA -*-
        # ---------------------------------------------------------------------------------

        # Esto esta agregado para centrar las ventanas en la pantalla
        master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega mas widgets).Esto 
        actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y  ancho de la pantalla
        wtotal = master.winfo_screenwidth()
        htotal = master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 980
        hventana = 615
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # ---------------------------------------------------------------------------
        # SETEO INICIAL DEL GRID
        # ---------------------------------------------------------------------------------

        # item = self.grid_clientes.identify_row(0)
        # self.grid_clientes.selection_set(item)
        # self.grid_clientes.focus(item)
        # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------
    # WIDGETS -*-
    # ---------------------------------------------------------------------------------

    def create_widgets(self):

        # --------------------------------------------------------------------------
        # TITULOS -*-
        # ---------------------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('clientes4.png')
        self.photo3 = self.photo3.resize((75, 75), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_clientes = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_clientes = Label(self.frame_titulo_top, image=self.png_clientes, bg="red", relief=RIDGE, bd=5,
                                      padx=7)
        self.lbl_titulo = Label(self.frame_titulo_top, width=25, text="Clientes", bg="black", fg="gold",
                                font=("Arial bold", 38, "bold"), bd=5, relief=RIDGE)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_clientes.grid(row=0, column=0, sticky=W, padx=8, ipadx=20)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew", padx=20)
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=8, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS -*-
        # ---------------------------------------------------------------------------------

        self.strvar_codigo = tk.StringVar(value="")
        self.strvar_apellido = tk.StringVar(value="")
        self.strvar_nombres = tk.StringVar(value="")
        self.strvar_direccion = tk.StringVar(value="")
        self.strvar_localidad = tk.StringVar(value="")
        self.strvar_provincia = tk.StringVar(value="")
        self.strvar_postal = tk.StringVar(value="")
        self.strvar_telef_pers = tk.StringVar(value="")
        self.strvar_telef_trab = tk.StringVar(value="")
        self.strvar_mail = tk.StringVar(value="")
        self.strvar_sit_fis = tk.StringVar(value="")
        self.strvar_cuit = tk.StringVar(value="")
        self.strvar_fecha_ingreso = tk.StringVar(value="")
        self.strvar_observaciones = tk.StringVar(value="")
        self.strvar_cant_clientes = tk.StringVar(value="0")
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # BOTONES -*-
        # ---------------------------------------------------------------------------------

        # BOTONES NUEVO - ELIMINAR - EDITAR - GUARDAR - CANCELAR
        barra_botones = LabelFrame(self.master)

        botones1 = LabelFrame(barra_botones, bd=5, relief="ridge")

        # Instalacion botones
        self.btnNuevo=Button(botones1, text="Nuevo", command=self.fNuevo, bg="blue", fg="white", width=10)
        self.btnNuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        self.btnEditar=Button(botones1, text="Editar", command=self.fEditar, bg="blue", fg="white", width=10)
        self.btnEditar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        self.btnEliminar=Button(botones1, text="Eliminar", command=self.fEliminar, bg="red", fg="white", width=10)
        self.btnEliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        self.btnGuardar=Button(botones1, text="Guardar", command=self.fGuardar, bg="green", fg="white", width=10)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=3, columnspan=2)
        self.btnCancelar=Button(botones1, text="Cancelar", command=self.fCancelar, bg="black", fg="white", width=10)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=3, columnspan=2)

        botones1.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES ORDEN - TOPE Y FIN DE ARCHIVO
        botones2 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        self.btn_orden_codigo = Button(botones2, text="Orden Codigo", width=11, command=self.forden_codigo, bg="grey",
                                       fg="white")
        self.btn_orden_codigo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        self.btn_orden_apellido = Button(botones2, text="Orden Apellido", width=11, command=self.forden_apellido,
                                         bg="grey", fg="white")
        self.btn_orden_apellido.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        self.btn_reset = Button(botones2, text="Reset", width=11, command=self.fReset, bg="black", fg="white")
        self.btn_reset.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(botones2, text="", image=self.photo4, command=self.fToparch, bg="grey", fg="white")
        self.btnToparch.grid(row=3, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(botones2, text="", image=self.photo5, command=self.fFinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=4, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        botones2.pack(side=TOP, padx=3, pady=3, fill=Y)

        # BOTONES SALIDA
        botones3 = LabelFrame(barra_botones)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(botones3, text="Salir", image=self.photo3, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")

        botones3.pack(side=TOP, padx=3, pady=3, fill=Y)

        botones4 = LabelFrame(barra_botones)

        fff = tkFont.Font(family="Arial", size=9, weight="bold")
        self.lbl_cant_clientes = Label(botones4, text="Clientes", font=fff)
        self.lbl_cant_clientes1= Label(botones4, textvariable=self.strvar_cant_clientes, font=fff)
        self.lbl_cant_clientes.grid(row=0, column=0, padx=5, pady=3, columnspan=2, sticky='nsew')
        self.lbl_cant_clientes1.grid(row=1, column=0, padx=5, pady=3, columnspan=2, sticky='nsew')

        botones4.pack(side="top", padx=3, pady=3, fill="y")
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # PACK - frame de botones
        barra_botones.pack(side="left", padx=10, pady=5, ipady=5, fill="y")
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # BUSQUEDA DE CLIENTES -*-
        # ---------------------------------------------------------------------------------

        self.frame_tv = Frame(self.master)
        # FRAME dentro del frame principal para poner la llinea de busqueda
        self.frame_buscar = LabelFrame(self.frame_tv)

        # BUSCAR Linea de label y entry de busqueda
        self.lbl_buscar_cliente = Label(self.frame_buscar, text="Buscar: ")
        self.lbl_buscar_cliente.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_cliente=Entry(self.frame_buscar, width=50)
        self.entry_buscar_cliente.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.btn_buscar_cliente = Button(self.frame_buscar, text="Buscar", command=self.fBuscar_en_tabla,
                                         bg="CadetBlue", fg="white", width=27)
        self.btn_buscar_cliente.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_mostrar_todo = Button(self.frame_buscar, text="Mostrar todo", command=self.fShowall, bg="CadetBlue",
                                       fg="white", width=27)
        self.btn_mostrar_todo.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        # -----------------------------------------------------------------------------
        # TREEVIEW -*-
        # -----------------------------------------------------------------------------

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.frame_tv)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_clientes = ttk.Treeview(self.frame_tv, columns=("col1", "col2", "col3", "col4", "col5", "col6",
                                                                  "col7", "col8", "col9", "col10", "col11", "col12",
                                                                  "col13", "col14"))

        self.grid_clientes.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_clientes.column("#0", width=60, anchor="center")
        self.grid_clientes.column("col1", width=60, anchor="center")
        self.grid_clientes.column("col2", width=180, anchor="w")
        self.grid_clientes.column("col3", width=220, anchor="w")
        self.grid_clientes.column("col4", width=220, anchor="w")
        self.grid_clientes.column("col5", width=120, anchor="center")
        self.grid_clientes.column("col6", width=90, anchor="center")
        self.grid_clientes.column("col7", width=60, anchor="center")
        self.grid_clientes.column("col8", width=200, anchor="center")
        self.grid_clientes.column("col9", width=200, anchor="center")
        self.grid_clientes.column("col10", width=200, anchor="center")
        self.grid_clientes.column("col11", width=150, anchor="center")
        self.grid_clientes.column("col12", width=100, anchor="center")
        self.grid_clientes.column("col13", width=100, anchor="center")
        self.grid_clientes.column("col14", width=200, anchor="center")

        self.grid_clientes.heading("#0", text="Id", anchor="center")
        self.grid_clientes.heading("col1", text="Codigo", anchor="center")
        self.grid_clientes.heading("col2", text="Apellido", anchor="center")
        self.grid_clientes.heading("col3", text="Nombres", anchor="center")
        self.grid_clientes.heading("col4", text="Direccion", anchor="center")
        self.grid_clientes.heading("col5", text="Localidad", anchor="center")
        self.grid_clientes.heading("col6", text="Provincia", anchor="center")
        self.grid_clientes.heading("col7", text="Postal", anchor="center")
        self.grid_clientes.heading("col8", text="Telf.Personal", anchor="center")
        self.grid_clientes.heading("col9", text="Telf.Trabajo", anchor="center")
        self.grid_clientes.heading("col10", text="E-mail", anchor="center")
        self.grid_clientes.heading("col11", text="Sit.Fiscal", anchor="center")
        self.grid_clientes.heading("col12", text="CUIT", anchor="center")
        self.grid_clientes.heading("col13", text="Fec.Ingreso", anchor="center")
        self.grid_clientes.heading("col14", text="Observaciones", anchor="center")

        self.grid_clientes.tag_configure('oddrow', background='light grey')
        self.grid_clientes.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tv, orient="horizontal")
        scroll_y = Scrollbar(self.frame_tv, orient="vertical")
        self.grid_clientes.config(xscrollcommand=scroll_x.set)
        self.grid_clientes.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_clientes.xview)
        scroll_y.config(command=self.grid_clientes.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # PACK - GENERALES
        self.frame_buscar.pack(side=TOP, fill=BOTH, expand=1, padx=1, pady=3)
        self. grid_clientes.pack(side= TOP, fill=BOTH, expand=1, padx=1, pady=5)
        self.frame_tv.pack(side=TOP, fill=BOTH, padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ENTRYS -*-
        # ---------------------------------------------------------------------------------

        self.sector_entry = LabelFrame(self.master)

        # CODIGO
        self.lbl_codigo = Label(self.sector_entry, text="Codigo: ")
        self.lbl_codigo.grid(row=0, column=0, padx=10, pady=3, sticky=W)
        self.entry_codigo = Entry(self.sector_entry, textvariable=self.strvar_codigo, justify="right", width=10)
        self.strvar_codigo.trace("w", lambda *args: self.limitador(self.strvar_codigo, 10))
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=3, sticky=W)
        # APELLIDO
        self.lbl_apellido = Label(self.sector_entry, text="Apellido: ")
        self.lbl_apellido.grid(row=1, column=0, padx=10, pady=3, sticky=W)
        self.entry_apellido=Entry(self.sector_entry, textvariable=self.strvar_apellido, justify="left", width=40)
        self.strvar_apellido.trace("w", lambda *args: self.limitador(self.strvar_apellido, 40))
        self.entry_apellido.grid(row=1, column=1, padx=10, pady=3, sticky=W)
        # NOMBRES
        self.lbl_nombres = Label(self.sector_entry, text="Nombres: ")
        self.lbl_nombres.grid(row=2, column=0, padx=10, pady=3, sticky=W)
        self.entry_nombres = Entry(self.sector_entry, textvariable=self.strvar_nombres, justify="left", width=40)
        self.strvar_nombres.trace("w", lambda *args: self.limitador(self.strvar_nombres, 40))
        self.entry_nombres.grid(row=2, column=1, padx=10, pady=3, sticky=W)
        # DIRECCION
        self.lbl_direccion = Label(self.sector_entry, text="Direccion: ")
        self.lbl_direccion.grid(row=3, column=0, padx=10, pady=3, sticky=W)
        self.entry_direccion=Entry(self.sector_entry, textvariable=self.strvar_direccion, justify="left", width=40)
        self.strvar_direccion.trace("w", lambda *args: self.limitador(self.strvar_direccion, 30))
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=3, sticky=W)
        # LOCALIDAD
        self.lbl_localidad = Label(self.sector_entry, text="Localidad: ")
        self.lbl_localidad.grid(row=4, column=0, padx=10, pady=3, sticky=W)
        self.entry_localidad=Entry(self.sector_entry, textvariable=self.strvar_localidad, justify="left", width=40)
        self.strvar_localidad.trace("w", lambda *args: self.limitador(self.strvar_localidad, 30))
        self.entry_localidad.grid(row=4, column=1, padx=10, pady=3, sticky=W)
        # PROVINCIA
        self.lbl_provincia = Label(self.sector_entry, text="Provincia: ")
        self.lbl_provincia.grid(row=5, column=0, padx=10, pady=3, sticky=W)
        self.entry_provincia=Entry(self.sector_entry, textvariable=self.strvar_provincia, justify="left", width=40)
        self.strvar_provincia.trace("w", lambda *args: self.limitador(self.strvar_provincia, 30))
        self.entry_provincia.grid(row=5, column=1, padx=10, pady=3, sticky=W)
        # POSTAL
        self.lbl_postal = Label(self.sector_entry, text="Cod. Postal: ")
        self.lbl_postal.grid(row=6, column=0, padx=10, pady=3, sticky=W)
        self.entry_postal=Entry(self.sector_entry, textvariable=self.strvar_postal, justify="left", width=40)
        self.strvar_postal.trace("w", lambda *args: self.limitador(self.strvar_postal, 30))
        self.entry_postal.grid(row=6, column=1, padx=10, pady=3, sticky=W)
        # TELEFONO PERSONAL
        self.lbl_telefono_pers = Label(self.sector_entry, text="Telefono Personal: ")
        self.lbl_telefono_pers.grid(row=0, column=2, padx=10, pady=3, sticky=W)
        self.entry_telefono_pers=Entry(self.sector_entry, textvariable=self.strvar_telef_pers, justify="left", width=40)
        self.strvar_telef_pers.trace("w", lambda *args: self.limitador(self.strvar_telef_pers, 30))
        self.entry_telefono_pers.grid(row=0, column=3, padx=10, pady=3, sticky=W)
        # TELEFONO TRABAJO
        self.lbl_telefono_trab = Label(self.sector_entry, text="Telefono Trabajo: ")
        self.lbl_telefono_trab.grid(row=1, column=2, padx=10, pady=3, sticky=W)
        self.entry_telefono_trab=Entry(self.sector_entry, textvariable=self.strvar_telef_trab, justify="left", width=40)
        self.strvar_telef_trab.trace("w", lambda *args: self.limitador(self.strvar_telef_trab, 30))
        self.entry_telefono_trab.grid(row=1, column=3, padx=10, pady=3, sticky=W)
        # CORREO ELECTRONICO
        self.lbl_mail = Label(self.sector_entry, text="Correo Electronico: ")
        self.lbl_mail.grid(row=2, column=2, padx=10, pady=3, sticky=W)
        self.entry_mail=Entry(self.sector_entry, textvariable=self.strvar_mail, justify="left", width=40)
        self.strvar_mail.trace("w", lambda *args: self.limitador(self.strvar_mail, 30))
        self.entry_mail.grid(row=2, column=3, padx=10, pady=5, sticky=W)
        # SITUACION FISCAL - COMBOBOX
        self.lbl_sit_fiscal = Label(self.sector_entry, text="Situacion Fiscal: ")
        self.lbl_sit_fiscal.grid(row=3, column=2, padx=10, pady=3, sticky=W)
        self.combo_sit_fiscal = ttk.Combobox(self.sector_entry, textvariable=self.strvar_sit_fis, state='readonly',
                                             width=40)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                           "RM - Responsable Monotributo", "EX - Exento",
                                           "RN - Responsable no inscripto"]
        self.combo_sit_fiscal.grid(row=3, column=3, padx=10, pady=5, sticky=W)
        # CUIT
        self.lbl_cuit = Label(self.sector_entry, text="CUIT - CUIL: ")
        self.lbl_cuit.grid(row=4, column=2, padx=10, pady=3, sticky=W)
        self.entry_cuit=Entry(self.sector_entry, textvariable= self.strvar_cuit, justify="left", width=40)
        self.strvar_cuit.trace("w", lambda *args: self.limitador(self.strvar_cuit, 11))
        self.entry_cuit.grid(row=4, column=3, padx=10, pady=3, sticky=W)
        # FECHA DE INGRESO
        self.lbl_fecha_ingreso = Label(self.sector_entry, text="Fecha Ingreso: ")
        self.lbl_fecha_ingreso.grid(row=5, column=2, padx=10, pady=3, sticky=W)
        self.entry_fecha_ingreso=Entry(self.sector_entry, textvariable=self.strvar_fecha_ingreso, justify="left",
                                       width=40)
        self.entry_fecha_ingreso.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_ingreso.grid(row=5, column=3, padx=10, pady=3, sticky=W)
        # Label y entry OBSERVACIONES
        self.lbl_observaciones = Label(self.sector_entry, text="Observaciones: ")
        self.lbl_observaciones.grid(row=6, column=2, padx=10, pady=3, sticky=W)
        self.entry_observaciones = Entry(self.sector_entry, textvariable=self.strvar_observaciones, justify="left",
                                         width=40)
        self.strvar_observaciones.trace("w", lambda *args: self.limitador(self.strvar_observaciones, 50))
        self.entry_observaciones.grid(row=6, column=3, padx=10, pady=3, sticky=W)

        # PACK del frame "sector_entry"
        self.sector_entry.pack(expand=1, fill="both", pady=5, padx=5)
        # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # GRID -*-
    # --------------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_clientes.get_children():
            self.grid_clientes.delete(item)

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varClientes.consultar_clientes(self.filtro_activo)
        else:
            datos = self.varClientes.consultar_clientes("clientes ORDER BY apellido, nombres ASC")

        self.strvar_cant_clientes.set(value=str(len(datos)))

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[13], '%Y-%m-%d'), "hora_no")

            self.grid_clientes.insert("", END, tags=color, text=row[0], values=(row[1], row[2], row[3], row[4],
                                                                      row[5], row[6], row[7], row[8], row[9], row[10],
                                                                      row[11], row[12], forma_normal, row[14]))

        if len(self.grid_clientes.get_children()) > 0:
            self.grid_clientes.selection_set(self.grid_clientes.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:
            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_clientes.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_clientes.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
                de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

            self.grid_clientes.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_clientes.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_clientes.yview(self.grid_clientes.index(rg))
        else:
            # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
            self.mover_puntero_topend("END")

    # --------------------------------------------------------------------------
    # INICIALIZACION SISTEMA -*-
    # --------------------------------------------------------------------------

    def estado_inicial(self):

        # Variables
        self.filtro_activo = "clientes ORDER BY apellido, nombres ASC"
        self.var_Id = -1
        self.alta_modif = 0

        self.limpiar_text()
        self.habilitar_btn_A("normal")
        self.habilitar_btn_B("disabled")
        self.habilitar_text("disabled")

    def limpiar_text(self):

        self.entry_codigo.delete(0, END)
        self.entry_apellido.delete(0, END)
        self.entry_nombres.delete(0, END)
        self.entry_direccion.delete(0, END)
        self.entry_localidad.delete(0, END)
        self.entry_provincia.delete(0, END)
        self.entry_postal.delete(0,END)
        self.entry_telefono_pers.delete(0, END)
        self.entry_telefono_trab.delete(0, END)
        self.entry_mail.delete(0, END)
        self.entry_fecha_ingreso.delete(0, END)
        self.combo_sit_fiscal.set("")
        self.combo_sit_fiscal.current(0)
        self.entry_cuit.delete(0, END)
        self.entry_observaciones.delete(0, END)

    def habilitar_text(self, estado):

        # Agregado para manejar tema de readonly y que no quede el codigo escrito al limpiar
        self.entry_codigo.configure(state="normal")
        self.entry_codigo.delete(0, END)
        self.entry_codigo.configure(state=estado)
        self.entry_apellido.configure(state=estado)
        self.entry_nombres.configure(state=estado)
        self.entry_direccion.configure(state=estado)
        self.entry_localidad.configure(state=estado)
        self.entry_provincia.configure(state=estado)
        self.entry_postal.configure(state=estado)
        self.entry_telefono_pers.configure(state=estado)
        self.entry_telefono_trab.configure(state=estado)
        self.entry_mail.configure(state=estado)
        self.entry_fecha_ingreso.configure(state=estado)
        self.combo_sit_fiscal.configure(state=estado)
        self.entry_cuit.configure(state=estado)
        self.entry_observaciones.configure(state=estado)

        if self.alta_modif == 1:
            self.grid_clientes['selectmode'] = 'none'
            self.grid_clientes.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif == 2 or self.alta_modif == 0:
            self.grid_clientes['selectmode'] = 'browse'
            self.grid_clientes.bind("<Double-Button-1>", self.DobleClickGrid)

    def habilitar_btn_A(self, estado):

        self.btnNuevo.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnEditar.configure(state=estado)
        self.entry_buscar_cliente.configure(state=estado)
        self.btn_buscar_cliente.configure(state=estado)
        self.btn_mostrar_todo.configure(state=estado)

        if self.alta_modif == 1 or self.alta_modif == 0:
            self.btnFinarch.configure(state=estado)
            self.btnToparch.configure(state=estado)
            self.btn_orden_codigo.configure(state=estado)
            self.btn_orden_apellido.configure(state=estado)

    def habilitar_btn_B(self, estado):

        self.btnGuardar.configure(state=estado)

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_inicial()

    def fReset(self):

        self.estado_inicial()
        self.limpiar_Grid()
        self.llena_grilla("")
        self.mover_puntero_topend("TOP")

    def fSalir(self):
        self.master.destroy()

    def fNo_modifique(self, event):
        return

    # --------------------------------------------------------------------------
    # CRUD -*-
    # --------------------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.limpiar_text()
        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")

        # Obtengo el codigo en secuencia y pongo el entry en disabled para no modificar
        self.entry_codigo.insert(0, (int(self.varClientes.traer_ultimo(1))) + 1)
        self.entry_codigo.configure(state="readonly")
        self.combo_sit_fiscal.configure(state="readonly")
        self.entry_localidad.insert(0, "Villa Carlos Paz")
        self.entry_provincia.insert(0, "Cordoba")
        self.entry_postal.insert(0, "5152")

        self.combo_sit_fiscal.current(0)

        # Cambio el formato de la fecha
        una_fecha = date.today()
        self.entry_fecha_ingreso.insert(0, una_fecha.strftime('%d/%m/%Y'))

        self.entry_apellido.focus()

    def fEditar(self):

        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Editar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2
        self.var_Id = self.clave  #puede traer -1 , en ese caso seria un alta

        self.habilitar_text('normal')
        self.limpiar_text()

        self.filtro_activo = "clientes WHERE Id = " + str(self.clave)

        valores = self.varClientes.consultar_clientes(self.filtro_activo)

        for row in valores:

            self.entry_codigo.insert(0, row[1])
            self.entry_apellido.insert(0, row[2])
            self.entry_nombres.insert(0, row[3])
            self.entry_direccion.insert(0, row[4])
            self.entry_localidad.insert(0, row[5])
            self.entry_provincia.insert(0, row[6])
            self.entry_postal.insert(0, row[7])
            self.entry_telefono_pers.insert(0, row[8])
            self.entry_telefono_trab.insert(0, row[9])
            self.entry_mail.insert(0, row[10])
            self.combo_sit_fiscal.set("")
            self.combo_sit_fiscal.insert(0, row[11])
            self.entry_cuit.insert(0, row[12])
            # convierto fecha de date a string y cambio a visualizacion español
            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[13], "%Y-%m-%d"), "hora_no")
            self.entry_fecha_ingreso.insert(0, fecha_convertida)
            self.entry_observaciones.insert(0, row[14])

        self.entry_codigo.configure(state="readonly")

        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")
        self.entry_apellido.focus()

    def fEliminar(self):

        # ------------------------------------------------------------------------------
        # selecciono el Id del GRID para su uso posterior
        self.selected = self.grid_clientes.focus()
        self.selected_ant = self.grid_clientes.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no son el mismo que el grid)
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.clave_ant = self.grid_clientes.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el GRID
        valores = self.grid_clientes.item(self.selected, 'values')
        data = "Id: "+str(self.clave)+" Nº: "+valores[0]+" Cliente: " + valores[1]+" "+valores[2]

        r = messagebox.askquestion("Confirmar", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        self.varClientes.eliminar_clientes(self.clave)

        messagebox.showinfo("Aviso", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        #-----------------------------------------------------------------
        # VALIDACIONES
        #-----------------------------------------------------------------

        # CONTROLO CODIGO REPETIDO - control de codigo de cliente repetido (en funciones)
        codrep = codigo_repetido(self.strvar_codigo.get(), "clientes", "codigo")

        if self.alta_modif == 1:
            # si viene algun dato, es que el codigo ya existe
            if len(codrep) > 0:
                messagebox.showerror("Error", "El codigo ya existe en la tabla - verifique", parent=self)
                self.entry_apellido.focus()
                return
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # VALIDACION QUE EXISTA APELLIDO y NOMBRE

        if self.strvar_apellido.get() == "":
            messagebox.showwarning("Alerta", "Ingrese apellido/s", parent=self)
            self.entry_apellido.focus()
            return
        if self.strvar_nombres.get() == "":
            messagebox.showwarning("Alerta", "Ingrese nombre/s", parent=self)
            self.entry_nombres.focus()
            return
        # VALIDAR CUIT - en modulo funciones.py
        if not validar_cuit(self, self.strvar_cuit.get()):
            messagebox.showwarning("Alerta", "CUIT incorrecto", parent=self)
            self.entry_cuit.focus()
            return
        # ----------------------------------------------------------------

        try:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
            self.selected = self.grid_clientes.focus()
            # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo
            # verlo en la base 1, 2, 3, 4......)
            self.clave = self.grid_clientes.item(self.selected, 'text')

            if self.alta_modif == 1:

                self.varClientes.insertar_clientes(self.strvar_codigo.get(), self.strvar_apellido.get(),
                self.strvar_nombres.get(), self.strvar_direccion.get(),
                self.strvar_localidad.get(), self.strvar_provincia.get(), self.strvar_postal.get(),
                self.strvar_telef_pers.get(), self.strvar_telef_trab.get(),
                self.strvar_mail.get(), self.strvar_fecha_ingreso.get(), self.strvar_sit_fis.get(),
                self.strvar_cuit.get(), self.strvar_observaciones.get(),
                self.strvar_apellido.get()+' '+self.strvar_nombres.get())

                messagebox.showinfo("Correcto", "Nuevo registro creado correctamente", parent=self)

            elif self.alta_modif == 2:

                self.varClientes.modificar_clientes(self.var_Id, self.strvar_codigo.get(),
                self.strvar_apellido.get(), self.strvar_nombres.get(), self.strvar_direccion.get(),
                self.strvar_localidad.get(), self.strvar_provincia.get(), self.strvar_postal.get(),
                self.strvar_telef_pers.get(), self.strvar_telef_trab.get(),
                self.strvar_mail.get(), self.strvar_fecha_ingreso.get(), self.strvar_sit_fis.get(),
                self.strvar_cuit.get(), self.strvar_observaciones.get(),
                self.strvar_apellido.get()+' '+self.strvar_nombres.get())

                self.var_Id == -1
                messagebox.showinfo("Correcto", "La modificacion del registro fue exitosa", parent=self)

            self.limpiar_Grid()
            self.limpiar_text()
            self.habilitar_btn_B("disabled")
            self.habilitar_btn_A("normal")

            self.filtro_activo = "clientes ORDER BY apellido, nombres ASC"

            if self.alta_modif == 1:
                ultimo_tabla_id = self.varClientes.traer_ultimo(0)
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

    # --------------------------------------------------------------------------
    # VARIAS -*-
    # --------------------------------------------------------------------------

    def DobleClickGrid(self, event):

        self.fEditar()

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta el :5 limitas la cantidad d caracteres
            entry_text.set(entry_text.get()[:caract])

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        # FUNCION VALIDA FECCHAS en modulo funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_ingreso.get())

        una_fecha = date.today()

        if retorno_VerFal == "":
            # Retorno con error
            self.strvar_fecha_ingreso.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.entry_fecha_ingreso.focus()
            return "error"
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.entry_fecha_ingreso.focus()
            return "bien"
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_ingreso.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.entry_fecha_ingreso.focus()
            return "error"
        elif retorno_VerFal == "BLANCO":
            return "bien"
        else:
            self.strvar_fecha_ingreso.set(retorno_VerFal)
            return "bien"

    # --------------------------------------------------------------------------
    # PUNTEROS Y ORDEN -*-
    # --------------------------------------------------------------------------

    def forden_codigo(self):

        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.filtro_activo = "clientes ORDER BY codigo ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    def forden_apellido(self):

        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.filtro_activo = "clientes ORDER BY apellido, nombres ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def fBuscar_en_tabla(self):

        # Buscar en el TREVIEW
        if len(self.entry_buscar_cliente.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.entry_buscar_cliente.get()

        self.filtro_activo = "clientes WHERE INSTR(apellido, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(nombres, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(apenombre, '" + se_busca + "') > 0" \
                             + " ORDER BY apellido, nombres ASC"

        self.varClientes.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_clientes.selection()
        self.grid_clientes.focus(item)

    def fShowall(self):

        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.filtro_activo = "clientes ORDER BY apellido, nombres ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview (I001, I002.....
            regis = self.grid_clientes.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_clientes.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_clientes.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_clientes.yview(self.grid_clientes.index(self.grid_clientes.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview (I001, I002, ..........
            regis = self.grid_clientes.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            # barro hasta el ultimo
            for rg in regis:
                continue
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_clientes.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_clientes.focus(rg)
            # lleva el foco al final del treeview
            self.grid_clientes.yview(self.grid_clientes.index(self.grid_clientes.get_children()[-1]))
