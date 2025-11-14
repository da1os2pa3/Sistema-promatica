from funciones import *
from ordenrepar_ABM import *
from funcion_new import *
# ---------------------------------------------
import os
from fpdf import FPDF
from PDF_clase import *
# ---------------------------------------------
#from tkinter import *
#import tkinter as tk
#from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter.scrolledtext import *
# ---------------------------------------------
from PIL import Image, ImageTk
from datetime import date, datetime
#from tktooltip import ToolTip

class OrdenesRepara(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=1100, height=730)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # -----------------------------------------------------------------------
        # Instanciaciones

        """ Creo una instancia de clientes_ABM de la clase datosClientes
        -A varGarantia le paso la pantalla para poder usar los parent en los mensajes de messagebox
        -A varFuncion_new, le paso tambien la pantalla por el mismo motivo."""

        self.varOrdenes = DatosOrdenRepar(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos toddo el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Asignamos medidas a la ventana
        wventana = 1100
        hventana = 680
        # Aplicamos la siguiente formula para ubicarla en el centro
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # VARIABLES GENERALES
        # ---------------------------------------------------------------------

        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.var_Id = -1
        self.alta_modif = 0
        self.filtro_activo = "orden_repara WHERE fin_retirada = 'N' ORDER BY num_orden ASC"
        # ----------------------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno.
        # Otras funciones para manejar los elementos seleccionados incluyen:
        1- selection_add(): añade elementos a la selección.
        2- selection_remove(): remueve elementos de la selección.
        3- selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        4- selection_toggle(): cambia la selección de un elemento. """

        self.create_widgets()

        # Antes de llenar la grilla debo definir el filtro activo para determinar con que configuracion se
        # mostrara inicialmente el GRID (orden, filtros... etc )
        self.filtro_activo = "orden_repara WHERE fin_retirada = 'N' ORDER BY num_orden ASC"

        self.llena_grilla("")

        self.estado_inicial("disabled")

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_orden.identify_row(0)
        # self.grid_orden.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_orden.focus(item)

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        # validar: funcion en funciones.py que valida que lo ingresado sea un numeo o "-" o "."
        #vcmd = (self.register(validar), "%P")
        vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ------------------------------------------------------------------
        # STRINGVARS -*-
        # ------------------------------------------------------------------

        self.strvar_buscar_orden = tk.StringVar(value="")
        self.strvar_nombre_cliente = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_cli_datosmas = tk.StringVar(value="")
        self.strvar_cli_deuda = tk.StringVar(value="0")
        self.strvar_nro_orden = tk.StringVar(value="0")
        self.strvar_fecha_ingreso = tk.StringVar(value="")
        self.strvar_fecha_egreso = tk.StringVar(value="")
        self.strvar_equ_ingresa = tk.StringVar(value="")
        self.strvar_equ_grupo = tk.StringVar(value="")
        self.strvar_equ_accesorios = tk.StringVar(value="")
        self.strvar_equ_estado = tk.StringVar(value="")
        self.strvar_cuentas = tk.StringVar(value="")
        self.strvar_requerido = tk.StringVar(value="")
        self.strvar_presupuesto = tk.StringVar(value="")
        self.strvar_partes = tk.StringVar(value="")
        self.strvar_total_partes = tk.StringVar(value="0")
        self.strvar_total_manodeobra = tk.StringVar(value="0")
        self.strvar_tot_final = tk.StringVar(value="0.00")
        self.strvar_retirado = tk.StringVar(value="")
        self.strvar_componentes_equipo = tk.StringVar(value="")
        self.strvar_buscostring = tk.StringVar(value="")

        self.strvar_estad_total = tk.StringVar(value="0")
        self.strvar_estad_pendi = tk.StringVar(value="0")
        self.strvar_estad_mesact = tk.StringVar(value="0")
        self.strvar_estad_pespendi = tk.StringVar(value="0")
        self.strvar_estad_pesmesact = tk.StringVar(value="0")
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TREEVIEW -*-
        # ------------------------------------------------------------------

        # Defino los Frames
        self.frame_superior = Frame(self.master)
        self.frame_tvw_ordenes = LabelFrame(self.frame_superior, text="", foreground="#CF09BD")
        # self.frame_listbox_clientes = LabelFrame(self.frame_superior, text="", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_ordenes)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        # Este es el TV donde aparecen las ordenes de reparacion
        self.grid_orden = ttk.Treeview(self.frame_tvw_ordenes, height=6, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5", "col6", "col7", "col8"))
        self.grid_orden.bind("<Double-Button-1>", self.DobleClickGrid)
        #self.grid_orden.bind("<ButtonRelease-3>", self.muestradatos)

        self.grid_orden.column("#0", width=40, anchor=CENTER)
        self.grid_orden.column("col1", width=70, anchor=E)
        self.grid_orden.column("col2", width=130, anchor=CENTER)
        self.grid_orden.column("col3", width=130, anchor=CENTER)
        self.grid_orden.column("col4", width=50, anchor=E)
        self.grid_orden.column("col5", width=400, anchor=W)
        self.grid_orden.column("col6", width=90, anchor=E)
        self.grid_orden.column("col7", width=90, anchor=E)
        self.grid_orden.column("col8", width=90, anchor=E)

        self.grid_orden.heading("#0", text="Id", anchor="center")
        self.grid_orden.heading("col1", text="NºOrden", anchor="center")
        self.grid_orden.heading("col2", text="Fec/Hor Ingreso", anchor="center")
        self.grid_orden.heading("col3", text="Fecha Egreso", anchor="center")
        self.grid_orden.heading("col4", text="C", anchor=CENTER)
        self.grid_orden.heading("col5", text="Cliente", anchor=CENTER)
        self.grid_orden.heading("col6", text="Total", anchor=CENTER)
        self.grid_orden.heading("col7", text="Partes", anchor=CENTER)
        self.grid_orden.heading("col8", text="M.O.", anchor=CENTER)

        self.grid_orden.tag_configure('oddrow', background='light grey')
        self.grid_orden.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_ordenes, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_ordenes, orient="vertical")
        self.grid_orden.config(xscrollcommand=scroll_x.set)
        self.grid_orden.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_orden.xview)
        scroll_y.config(command=self.grid_orden.yview)
        scroll_y.pack(side=RIGHT, fill="y")
        scroll_x.pack(side=BOTTOM, fill="x")
        self.grid_orden['selectmode'] = 'browse'

        # PACKS del Treeview
        self.grid_orden.pack(side=TOP, fill=BOTH, expand=0, padx=3, pady=2)
        self.frame_tvw_ordenes.pack(side="left", fill="both", expand=1, padx=3, pady=2)
        self.frame_superior.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # # Reordeno los elementos del frame 1_0
        # for widg in self.frame_listbox_clientes.winfo_children():
        #     widg.grid_configure(padx=5, pady=3)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # BOTONES -*-
        # ---------------------------------------------------------------------------

        self.frame_segundo = LabelFrame(self.master, text="")

        self.btn_nueva_orden = Button(self.frame_segundo, text="Nueva", width=8, command=self.fNueva, bg="blue",
                                      fg="white")
        self.btn_nueva_orden.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
        self.btn_editar_orden = Button(self.frame_segundo, text="Editar", width=8, command=self.fModificar_orden,
                                       bg="blue", fg="white")
        self.btn_editar_orden.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.btn_borrar_orden = Button(self.frame_segundo, text="Eliminar", width=8, command=self.fEliminar_orden,
                                       bg="red", fg="white")
        self.btn_borrar_orden.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")
        self.btn_guardar_orden = Button(self.frame_segundo, text="Guardar", width=8, command=self.fGuardar_orden,
                                        bg="green", fg="white")
        self.btn_guardar_orden.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")
        self.btn_cancelar_orden = Button(self.frame_segundo, text="Cancelar/Reset", width=12, command=self.fCancelar,
                                         bg="black", fg="white")
        self.btn_cancelar_orden.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
        self.btn_imprime_orden = Button(self.frame_segundo, text="Imprimir", width=8, command=self.fImprimir,
                                        bg='#5F9EF5', fg="white")
        self.btn_imprime_orden.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        # botones para ir al tope y al fin del archivo
        self.photo_top_arch = Image.open('toparch.png')
        self.photo_top_arch = self.photo_top_arch.resize((25, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_top_arch = ImageTk.PhotoImage(self.photo_top_arch)
        self.btn_top_arch = Button(self.frame_segundo, text="", image=self.photo_top_arch, command=self.fToparch,
                                   bg="grey", fg="white")
        self.btn_top_arch.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo_fin_arch = Image.open('finarch.png')
        self.photo_fin_arch = self.photo_fin_arch.resize((25, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_fin_arch = ImageTk.PhotoImage(self.photo_fin_arch)
        self.btn_fin_arch = Button(self.frame_segundo, text="", image=self.photo_fin_arch, command=self.fFinarch,
                                   bg="grey", fg="white")
        self.btn_fin_arch.grid(row=0, column=8, padx=5, pady=2, sticky="nsew")
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # ----------------------------------------------------------------------
        # BUSCAR ORDENES *
        # ----------------------------------------------------------------------

        lbl_buscar_orden = Label(self.frame_segundo, text="Buscar:: ")
        lbl_buscar_orden.grid(row=0, column=9, padx=5, pady=2, sticky="nsew")
        self.entry_buscar_orden = Entry(self.frame_segundo, textvariable=self.strvar_buscar_orden, width=21)
        self.entry_buscar_orden.grid(row=0, column=10, padx=5, pady=2, sticky="nsew")
        self.btn_buscar_orden = Button(self.frame_segundo, text="Filtrar", width=9, command=self.fFiltrar_orden,
                                       bg="CadetBlue", fg="white")
        self.btn_buscar_orden.grid(row=0, column=11, padx=5, pady=2, sticky="nsew")
        self.btn_no_retiradas = Button(self.frame_segundo, text="No retiradas", width=10, command=self.fNoretiradas,
                                       bg="CadetBlue", fg="white")
        self.btn_no_retiradas.grid(row=0, column=12, padx=5, pady=2, sticky="nsew")
        # Mostrar all nuevamente
        self.btn_showall_orden = Button(self.frame_segundo, text="Mostrar todo", width=10, command=self.fShowall,
                                        bg="CadetBlue", fg="white")
        self.btn_showall_orden.grid(row=0, column=13, padx=5, pady=2, sticky="nsew")
        # Estadisticas
        self.btn_estadistica = Button(self.frame_segundo, text="Estadistica", width=9,
                                      command=self.fEstadistica, bg="CadetBlue", fg="white")
        self.btn_estadistica.grid(row=0, column=14, padx=5, pady=2, sticky="nsew")

        # reordenamiento de self.frame_segundo
        for widg in self.frame_segundo.winfo_children():
            widg.grid_configure(padx=4, pady=3, sticky='nsew')

        self.frame_segundo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS -*-
        # ------------------------------------------------------------------

        self.frame_tercero = LabelFrame(self.master, text="")

        # nombre de cliente
        lbl_nombre_cliente = Label(self.frame_tercero, text="Cliente:")
        lbl_nombre_cliente.grid(row=0, column=0)
        self.entry_nombre_cliente = Entry(self.frame_tercero, textvariable=self.strvar_nombre_cliente, width=70,
                                          justify="left")
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

        # codigo cliente
        self.lbl_codigo_cliente = Label(self.frame_tercero, textvariable=self.strvar_codigo_cliente, width=6,
                                        anchor='e')
        self.lbl_codigo_cliente.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")

        # cliente datos mas
        self.strvar_cli_datosmas.set(value="                                        ")
        lbl_cli_datosmas = Label(self.frame_tercero, text="Datos: ")
        lbl_cli_datosmas.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")
        lbl_cli_direccion = Label(self.frame_tercero, textvariable=self.strvar_cli_datosmas)
        lbl_cli_direccion.grid(row=0, column=8, padx=5, pady=2, sticky="nsew")
        lbl_cli_deuda1 = Label(self.frame_tercero, text="Deuda: ")
        lbl_cli_deuda1.grid(row=0, column=9, padx=5, pady=2, sticky="nsew")
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        lbl_cli_deuda2 = Label(self.frame_tercero, textvariable=self.strvar_cli_deuda, fg="red", font=fff)
        lbl_cli_deuda2.grid(row=0, column=10, padx=5, pady=2, sticky="nsew")

        # boton para buscar cliente
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_tercero, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")

        # reordenamiento de self.frame_tercero
        for widg in self.frame_tercero.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

        self.frame_tercero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        # Componentes
        self.frame_tercero_bis = LabelFrame(self.master, text="")

        lbl_componentes_equipo = Label(self.frame_tercero_bis, text="Componentes equipo:")
        lbl_componentes_equipo.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_componentes_equipo = Entry(self.frame_tercero_bis, textvariable=self.strvar_componentes_equipo,
                                              width=156, justify=LEFT)
        self.entry_componentes_equipo.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.strvar_componentes_equipo.trace("w",
                                             lambda *args: self.limitador(self.strvar_equ_ingresa, 250))

        self.frame_tercero_bis.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # Datos de la orden
        self.frame_cuarto = LabelFrame(self.master, text="")

        # nro. de orden
        lbl_nro_orden = Label(self.frame_cuarto, text="Nº Orden:")
        lbl_nro_orden.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.entry_nro_orden = Entry(self.frame_cuarto, textvariable=self.strvar_nro_orden, width=8, justify=RIGHT)
        self.entry_nro_orden.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")
        self.lbl_codigo_cliente.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")

        # Fecha y hora de ingreso
        lbl_fecha_ingreso = Label(self.frame_cuarto, text="Fecha y hora de ingreso: ")
        lbl_fecha_ingreso.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
        self.lbl_valor_fecha_ingreso = Label(self.frame_cuarto, textvariable=self.strvar_fecha_ingreso, width=20,
                                             justify=RIGHT)
        self.lbl_valor_fecha_ingreso.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        # Fecha y hora de egreso
        lbl_fecha_egreso = Label(self.frame_cuarto, text="Fecha de egreso: ")
        lbl_fecha_egreso.grid(row=0, column=6, padx=5, pady=2, sticky="nsew")
        self.lbl_valor_fecha_egreso = Label(self.frame_cuarto, textvariable=self.strvar_fecha_egreso, width=15,
                                            justify="right")
        self.lbl_valor_fecha_egreso.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")

        # Defino un combobox con los tipos de equipos que se reciben
        self.lbl_combo_tipos_equipo = Label(self.frame_cuarto, text="Tipo de equipo: ")
        self.lbl_combo_tipos_equipo.grid(row=0, column=8, padx=5, pady=2, sticky="nsew")
        # lbl_combo_tipos_equipo.place(x=2, y=55)
        self.combo_tipo_equipo = ttk.Combobox(self.frame_cuarto, textvariable=self.strvar_equ_grupo, state="readonly",
                                              width=14)
        # self.combo_tipo_equipo['value'] = self.varArtic.combo_input("ma_nombre", "marcas", "ma_nombre")
        self.combo_tipo_equipo["values"] = ("Notebooks", "PC", "Impresoras", "Fuentes UPS", "Monitores", "Varios")
        self.combo_tipo_equipo.current(0)
        self.combo_tipo_equipo.grid(row=0, column=9, padx=5, pady=2, sticky="nsew")

        # reordenamiento de self.frame_cuarto
        for widg in self.frame_cuarto.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

        self.frame_cuarto.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        self.frame_quinto = LabelFrame(self.master, text="")

        # Descripcion de equipo que ingresa
        lbl_equ_ingresa = Label(self.frame_quinto, text="Equipo:")
        lbl_equ_ingresa.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_equ_ingresa = Entry(self.frame_quinto, textvariable=self.strvar_equ_ingresa, width=80)
        self.strvar_equ_ingresa.trace("w", lambda *args: self.limitador(self.strvar_equ_ingresa, 100))
        self.entry_equ_ingresa.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

        # Accesorios que acompañan al equipo
        lbl_equ_accesorios = Label(self.frame_quinto, text="Accesorios:")
        lbl_equ_accesorios.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")
        self.entry_equ_accesorios = Entry(self.frame_quinto, textvariable=self.strvar_equ_accesorios, width=70)
        self.strvar_equ_accesorios.trace("w", lambda *args: self.limitador(self.strvar_equ_accesorios, 100))
        self.entry_equ_accesorios.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")

        # Estado del equipo
        lbl_equ_estado = Label(self.frame_quinto, text="Estado:")
        lbl_equ_estado.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_equ_estado = Entry(self.frame_quinto, textvariable=self.strvar_equ_estado, width=58)
        self.strvar_equ_estado.trace("w", lambda *args: self.limitador(self.strvar_equ_estado, 100))
        self.entry_equ_estado.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")

        # Contraseñas y cuentas
        lbl_equ_cuentas = Label(self.frame_quinto, text="Ctas/Cont.: ")
        lbl_equ_cuentas.grid(row=1, column=2)
        self.entry_cuentas = Entry(self.frame_quinto, textvariable=self.strvar_cuentas, width=70)
        self.strvar_cuentas.trace("w", lambda *args: self.limitador(self.strvar_cuentas, 100))
        self.entry_cuentas.grid(row=1, column=3, padx=5, pady=2, sticky="nsew")

        # Requerimientos
        lbl_equ_requerido = Label(self.frame_quinto, text="Requerido: ")
        lbl_equ_requerido.grid(row=2, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_requerido = Entry(self.frame_quinto, textvariable=self.strvar_requerido, width=60)
        self.strvar_requerido.trace("w", lambda *args: self.limitador(self.strvar_requerido, 200))
        self.entry_requerido.grid(row=2, column=1, columnspan=5, padx=5, pady=2, sticky="nsew")

        # reordenamiento de self.frame_quinto
        for widg in self.frame_quinto.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

        self.frame_quinto.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        self.frame_sexto = LabelFrame(self.master, text="")

        # Diagnostico
        lbl_diagnostico = Label(self.frame_sexto, text="Diagnostico:")
        lbl_diagnostico.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")
        self.text_diagnostico = ScrolledText(self.frame_sexto)
        self.text_diagnostico.config(width=41, height=6, wrap="word", padx=4, pady=2)
        self.text_diagnostico.grid(row=1, column=0, padx=4, pady=1, sticky="nsew")

        # Trbajo realizado
        lbl_trabajo_realizado = Label(self.frame_sexto, text="Trabajo:")
        lbl_trabajo_realizado.grid(row=0, column=1, padx=4, pady=1, sticky="nsew" )
        self.text_trabajo_realizado = ScrolledText(self.frame_sexto)
        self.text_trabajo_realizado.config(width=41, height=6, wrap="word", padx=4, pady=2)
        self.text_trabajo_realizado.grid(row=1, column=1, padx=4, pady=1, sticky="nsew")

        # Anotaciones
        lbl_anotaciones = Label(self.frame_sexto, text="Notas:")
        lbl_anotaciones.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")
        self.text_anotaciones = ScrolledText(self.frame_sexto)
        self.text_anotaciones.config(width=41, height=4, wrap="word", padx=4, pady=2)
        self.text_anotaciones.grid(row=1, column=2, padx=4, pady=1, sticky="nsew")

        # reordenamiento de self.frame_sexto
        for widg in self.frame_sexto.winfo_children():
            widg.grid_configure(padx=4, pady=3, sticky="nsew")

        self.frame_sexto.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        self.frame_septimo = LabelFrame(self.master, text="")

        # Presupuesto
        lbl_presupuesto = Label(self.frame_septimo, text="Detalle Presupuesto:")
        lbl_presupuesto.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")
        self.entry_presupuesto = Entry(self.frame_septimo, textvariable=self.strvar_presupuesto, width=157)
        self.strvar_presupuesto.trace("w", lambda *args: self.limitador(self.strvar_presupuesto, 200))
        self.entry_presupuesto.grid(row=0, column=1, padx=4, pady=1, sticky="nsew")

        # Partes reemplazadas
        lbl_partes = Label(self.frame_septimo, text="Partes reemplazadas:")
        lbl_partes.grid(row=1, column=0, padx=4, pady=1, sticky="nsew")
        self.entry_partes = Entry(self.frame_septimo, textvariable=self.strvar_partes, width=157)
        self.strvar_partes.trace("w", lambda *args: self.limitador(self.strvar_partes, 200))
        self.entry_partes.grid(row=1, column=1, padx=4, pady=1, sticky="nsew")

        # reordenamiento de self.frame_septimo
        for widg in self.frame_septimo.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

        self.frame_septimo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        self.frame_octavo = LabelFrame(self.master, text="")

        # Total pesos partes
        lbl_total_partes = Label(self.frame_octavo, text="Total partes:", justify=LEFT)
        lbl_total_partes.grid(row=0, column=0, padx=5, pady=2, sticky='nsew')
        self.entry_total_partes = Entry(self.frame_octavo, textvariable=self.strvar_total_partes, width=15,
                                        justify=RIGHT)
        self.entry_total_partes.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.entry_total_partes.config(validate="key", validatecommand=vcmd)
        self.strvar_total_partes.trace("w", lambda *args: self.limitador(self.strvar_total_partes, 14))
        # mando a la funcion que suma el total final
        self.entry_total_partes.bind('<FocusOut>', lambda e: self.sumar_totalfinal())

        # Total pesos mano de obra
        lbl_total_manodeobra = Label(self.frame_octavo, text="Total Mano de Obra:")
        lbl_total_manodeobra.grid(row=0, column=2, padx=5, pady=1, sticky='nsew')
        self.entry_total_manodeobra = Entry(self.frame_octavo, textvariable=self.strvar_total_manodeobra, width=15,
                                            justify="right")
        self.entry_total_manodeobra.grid(row=0, column=3, padx=5, pady=1, sticky="nsew")
        self.entry_total_manodeobra.config(validate="key", validatecommand=vcmd)
        self.strvar_total_manodeobra.trace("w",
                                           lambda *args: self.limitador(self.strvar_total_manodeobra, 14))
        # mando a la funcion que suma el total final
        self.entry_total_manodeobra.bind('<FocusOut>', lambda e: self.sumar_totalfinal())

        # Total global pesos
        lbl_total_global = Label(self.frame_octavo, text="Total a pagar:")
        lbl_total_global.grid(row=0, column=4, padx=4, pady=1, sticky=W)
        self.lbl_importe_global = Label(self.frame_octavo, textvariable=self.strvar_tot_final, width=6, anchor='e')
        self.lbl_importe_global.grid(row=0, column=5, padx=5, pady=1, sticky="nsew")

        # Equipo retirado ???
        lbl_equipo_retirado = Label(self.frame_octavo, text="Retirado? [S/N]:")
        lbl_equipo_retirado.grid(row=0, column=6, padx=4, pady=1, sticky=W)
        self.entry_retirado = Entry(self.frame_octavo, textvariable=self.strvar_retirado, width=2)
        self.strvar_retirado.trace("w", lambda *args: self.limitador(self.strvar_retirado, 1))
        self.entry_retirado.grid(row=0, column=7, padx=5, pady=1, sticky="nsew")

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btn_salir_orden = Button(self.frame_octavo, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                                      bg="yellow", fg="white")
        self.btn_salir_orden.grid(row=0, column=8, padx=10, pady=1, sticky="nsew")

        for widg in self.frame_octavo.winfo_children():
            widg.grid_configure(padx=24, pady=3, sticky="nsew")

        self.frame_octavo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

    # --------------------------------------------------------------------------------
    # ESTADOS -*-
    # --------------------------------------------------------------------------------

    def estado_inicial(self, estado):

        self.btn_guardar_orden.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_nro_orden.configure(state=estado)
        self.entry_equ_ingresa.configure(state=estado)
        self.combo_tipo_equipo.configure(state=estado)
        self.entry_equ_accesorios.configure(state=estado)
        self.entry_equ_estado.configure(state=estado)
        self.entry_cuentas.configure(state=estado)
        self.entry_partes.configure(state=estado)
        self.entry_requerido.configure(state=estado)
        self.text_anotaciones.configure(state=estado)
        self.text_trabajo_realizado.configure(state=estado)
        self.text_diagnostico.configure(state=estado)
        self.entry_presupuesto.configure(state=estado)
        self.entry_total_partes.configure(state=estado)
        self.entry_total_manodeobra.configure(state=estado)
        self.entry_retirado.configure(state=estado)
        self.entry_componentes_equipo.configure(state=estado)
        # 0 - Activar Browse
        self.grid_orden['selectmode'] = 'browse'
        self.grid_orden.bind("<Double-Button-1>", self.DobleClickGrid)

    def estado_botones(self, estado):

        self.btn_nueva_orden.configure(state=estado)
        self.btn_editar_orden.configure(state=estado)
        self.btn_borrar_orden.configure(state=estado)
        self.btn_imprime_orden.configure(state=estado)
        self.btn_buscar_orden.configure(state=estado)
        self.btn_showall_orden.configure(state=estado)
        self.btn_no_retiradas.configure(state=estado)
        self.btn_estadistica.configure(state=estado)
        self.entry_buscar_orden.configure(state=estado)

    def estado_global(self):

        self.entry_nombre_cliente.configure(state="normal")
        self.btn_cancelar_orden.configure(state="normal")
        self.btn_guardar_orden.configure(state="normal")
        self.btn_bus_cli.configure(state="normal")
        self.entry_equ_ingresa.configure(state="normal")
        self.entry_equ_accesorios.configure(state="normal")
        self.entry_equ_estado.configure(state="normal")
        self.entry_cuentas.configure(state="normal")
        self.entry_partes.configure(state="normal")
        self.entry_requerido.configure(state="normal")
        self.text_anotaciones.configure(state="normal")
        self.text_trabajo_realizado.configure(state="normal")
        self.text_diagnostico.configure(state="normal")
        self.entry_presupuesto.configure(state="normal")
        self.entry_total_partes.configure(state="normal")
        self.entry_total_manodeobra.configure(state="normal")
        self.entry_retirado.configure(state="normal")
        self.entry_componentes_equipo.configure(state="normal")
        self.combo_tipo_equipo.configure(state="normal")
        self.btn_nueva_orden.configure(state="disabled")
        self.btn_editar_orden.configure(state="disabled")
        self.btn_borrar_orden.configure(state="disabled")
        self.btn_imprime_orden.configure(state="disabled")
        self.btn_buscar_orden.configure(state="disabled")
        self.entry_buscar_orden.configure(state="disabled")
        self.btn_showall_orden.configure(state="disabled")
        self.btn_no_retiradas.configure(state="disabled")
        self.btn_estadistica.configure(state="disabled")

    def limpiar_text(self):

        self.entry_nombre_cliente.delete(0, END)

        # eston son solo labels de algunos datos mas del cliente
        self.strvar_codigo_cliente.set(value="0")
        self.strvar_cli_datosmas.set(value="")

        # tratamiento de nro de orden
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.delete(0, END)
        self.entry_nro_orden.configure(state="disabled")
        self.strvar_fecha_ingreso.set(value="")
        self.strvar_fecha_egreso.set(value="")
        self.strvar_equ_ingresa.set(value="")
        self.strvar_equ_accesorios.set(value="")
        self.strvar_equ_estado.set(value="")
        self.strvar_cuentas.set(value="")
        self.strvar_requerido.set(value="")
        self.strvar_partes.set(value="")
        self.text_anotaciones.delete('1.0', 'end')
        self.text_trabajo_realizado.delete('1.0', 'end')
        self.text_diagnostico.delete('1.0', 'end')
        self.strvar_presupuesto.set(value="")
        self.strvar_partes.set(value="")
        self.strvar_total_partes.set(value="0.00")
        self.strvar_total_manodeobra.set(value="0.00")
        self.strvar_retirado.set(value="")
        self.strvar_componentes_equipo.set(value="")
        self.combo_tipo_equipo.set("")
        self.combo_tipo_equipo.current(0)
        self.strvar_cli_deuda.set(value="0")

    # --------------------------------------------------------------------------------
    # GRILLA -*-
    # --------------------------------------------------------------------------------

    def llena_grilla(self, ult_tabla_id):

        datos = self.varOrdenes.consultar_ordenes(self.filtro_activo)

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            """ Leo en la lista datos todos los registros y los inserto en la grilla
            1- El " " nos da quien es el padre de este nodo (ninguno en este caso (nace en la raiz))
            2- END es en que posicion va (en este caso al final)
            3- text=row[0] - es el Id de la Tabla (21, 22, 23..."""

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'))

            self.grid_orden.insert("", END, tags=color, text=row[0], values=(row[1], forma_normal, row[3],
                                                                             row[4], row[5], (row[18]+row[17]),
                                                                             row[18], row[17]))

        """ get_children() es que obtiene todos los datos. El [0] indica que obtiene el elemento
        correspondiente a ese indice o sea el Id I001, si no le pongo nada, trae todos los Id)
        Esto parece hacer que el treeview se posicione en el primero """

        if len(self.grid_orden.get_children()) > 0:
            self.grid_orden.selection_set(self.grid_orden.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ Si NO es blanco - 
                regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_orden.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_orden.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_orden.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_orden.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_orden.yview(self.grid_orden.index(rg))
            return

        # En caso de que el parametro sea "" muevo el puntero al final del GRID
        self.muevo_puntero_topend("END")

    def llena_grilla2(self, argg2):

        datos = self.varOrdenes.consultar_ordenes(argg2)

        for row in datos:
            self.grid_orden.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))

        if len(self.grid_orden.get_children()) > 0:
            self.grid_orden.selection_set(self.grid_orden.get_children()[0])

    def limpiar_Grid(self):

        for item in self.grid_orden.get_children():
            self.grid_orden.delete(item)

    # --------------------------------------------------------------------------------
    # CRUD *
    # --------------------------------------------------------------------------------

    def fNueva(self):

        self.alta_modif = 1

        # 0 - Desactivar Browse
        self.grid_orden['selectmode'] = 'none'
        self.grid_orden.bind("<Double-Button-1>", self.fNo_modifique)

        # Ingreso de una nueva orden de reparacion
        self.estado_global()
        self.limpiar_text()
        self.entry_nombre_cliente.focus()

        # 2 - traer ultimo numero de orden mas uno para ingresar
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.insert(0, (int(self.varOrdenes.traer_ultimo(1)) + 1))
        self.entry_nro_orden.configure(state="disabled")

        # Fecha y hora de ingreso
        una_fecha = datetime.now()
        self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
        self.strvar_fecha_ingreso.set(self.fecha_final)
        self.entry_retirado.insert(0, "N")

    def fModificar_orden(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_orden.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        self.estado_global()
        self.limpiar_text()

        # Trae un solo el registro solicitado mediante su ID. Metodo de ordenrepar_ABM.
        datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)

        # Asigno el valor de la lista al campo desde la posicion 1
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.insert(0, datos_registro_selec[1])
        self.entry_nro_orden.configure(state="disabled")

        # Aqui analizo que no me llegue desde la TABLA ninguna fecha en "none" dado que ese es un error
        # en el caso que venga, la convierto datetime con la fecha actual tanto para ingreso como para egreso.
        una_fecha = (datos_registro_selec[2])
        self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
        self.strvar_fecha_ingreso.set(self.fecha_final)

        # Tratamiento de fecha de egreso porque aca puede venir None
        if (datos_registro_selec[3]) == None:
            self.strvar_fecha_egreso.set(value="")
        else:
            una_fecha = (datos_registro_selec[3])
            self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
            self.strvar_fecha_egreso.set(self.fecha_final)

        self.strvar_codigo_cliente.set(datos_registro_selec[4])
        self.strvar_nombre_cliente.set(value=datos_registro_selec[5])
        self.strvar_equ_ingresa.set(value=datos_registro_selec[6])
        self.strvar_equ_grupo.set(value=datos_registro_selec[7])
        self.strvar_equ_accesorios.set(value=datos_registro_selec[8])
        self.strvar_equ_estado.set(value=datos_registro_selec[9])
        self.strvar_cuentas.set(value=datos_registro_selec[10])
        self.strvar_requerido.set(value=datos_registro_selec[11])
        self.text_diagnostico.insert(END, datos_registro_selec[12])
        self.strvar_presupuesto.set(value=datos_registro_selec[13])
        self.text_trabajo_realizado.insert(END, datos_registro_selec[14])
        self.strvar_partes.set(value=datos_registro_selec[15])
        self.text_anotaciones.insert(END, datos_registro_selec[16])
        self.strvar_total_manodeobra.set(value=datos_registro_selec[17])
        self.strvar_total_partes.set(value=datos_registro_selec[18])
        self.strvar_retirado.set(value=datos_registro_selec[19])
        self.strvar_componentes_equipo.set(value=datos_registro_selec[20])

        self.strvar_cli_deuda.set(value=str(self.fTraedeuda(self.strvar_codigo_cliente.get())))

        # traer los datos del cliente direccion y telefono - Datos mas -
        retorno = self.varOrdenes.buscar_entabla("clientes WHERE codigo = '" + self.strvar_codigo_cliente.get() +"'")

        for item in retorno:
            self.strvar_cli_datosmas.set(value=str(item[4]+' - tel: '+item[8]+' / '+item[9]))

        self.sumar_totalfinal()
        self.entry_nombre_cliente.focus()

    def fEliminar_orden(self):

        # ---------------------------------------------------------------------------
        # selecciono el Id del Tv grid I010, IB020
        self.selected = self.grid_orden.focus()
        self.selected_ant = self.grid_orden.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no es el mismo del Tv - 23, 12, 33, ....
        self.clave = self.grid_orden.item(self.selected, 'text')
        self.clave_ant = self.grid_orden.item(self.selected_ant, 'text')
        # ---------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el GRID
        valores = self.grid_orden.item(self.selected, 'values')

        data = "Id: "+str(self.clave)+" Nº: "+valores[0]+" Cliente: " + valores[4]

        r = messagebox.askquestion("Cuidado", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Aviso", "Eliminacion cancelada", parent=self)
            return

        self.varOrdenes.eliminar_orden(self.clave)

        messagebox.showinfo("Aviso", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar_orden(self):

        self.strvar_retirado.set(value=(self.strvar_retirado.get().upper()))

        # no permito codigo ni nombre de cliente en blanco
        if int(self.strvar_codigo_cliente.get()) == 0 or self.strvar_nombre_cliente.get() == "":
            messagebox.showerror("Cuidado", "Faltan datos de cliente - verifique", parent=self)
            return
        # el numero de orden no puede ser vacio
        if self.strvar_nro_orden.get() == 0:
            messagebox.showerror("Cuidado", "Faltan numero de orden - verifique", parent=self)
            return
        # el -retirada- debe ser S o N
        if self.strvar_retirado.get() != "S" and self.strvar_retirado.get() != "N":
            messagebox.showerror("Cuidado", "El informe de retirada valor no aceptado, solo S o N - "
                                            "verifique", parent = self)
            return

        # guardo el Id del Tv en selected para ubicacion del foco a posteriori - I001, IB10
        self.selected = self.grid_orden.focus()
        # Guardo el Id del registro de la Tabla (no es el mismo que el otro, este puedo verlo en la TABLA - 21, 12..)
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.alta_modif == 1:

            self.varOrdenes.insertar_orden(self.strvar_nro_orden.get(), datetime.now(),
            self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
            self.strvar_equ_ingresa.get(), self.strvar_equ_grupo.get(), self.strvar_equ_accesorios.get(),
            self.strvar_equ_estado.get(), self.strvar_cuentas.get(), self.strvar_requerido.get(),
            self.text_diagnostico.get(1.0, 'end-1c'), self.strvar_presupuesto.get(),
            self.text_trabajo_realizado.get(1.0, 'end-1c'), self.strvar_partes.get(),
            self.text_anotaciones.get(1.0, 'end-1c'), self.strvar_total_manodeobra.get(),
            self.strvar_total_partes.get(), self.strvar_retirado.get(), self.strvar_componentes_equipo.get())

            messagebox.showinfo("Aviso", "Nuevo registro creado correctamente", parent=self)

        else:

            transformo_fecha_ingreso = datetime
            transformo_fecha_ingreso = transformo_fecha_ingreso.strptime(self.strvar_fecha_ingreso.get(), "%d-%m-%Y %H:%M:%S")

            if self.strvar_retirado.get() == "S":
                transformo_fecha_egreso = datetime.now()
            else:
                transformo_fecha_egreso = ""

            self.varOrdenes.modificar_orden(self.var_Id, self.strvar_nro_orden.get(), transformo_fecha_ingreso,
                          transformo_fecha_egreso, self.strvar_codigo_cliente.get(),
                          self.strvar_nombre_cliente.get(), self.strvar_equ_ingresa.get(),
                          self.strvar_equ_grupo.get(), self.strvar_equ_accesorios.get(),
                          self.strvar_equ_estado.get(), self.strvar_cuentas.get(),
                          self.strvar_requerido.get(), self.text_diagnostico.get(1.0, 'end-1c'),
                          self.strvar_presupuesto.get(), self.text_trabajo_realizado.get(1.0, 'end-1c'),
                          self.strvar_partes.get(), self.text_anotaciones.get(1.0, 'end-1c'),
                          self.strvar_total_manodeobra.get(), self.strvar_total_partes.get(),
                          self.strvar_retirado.get(), self.strvar_componentes_equipo.get())

            messagebox.showinfo("Aviso", "La modificacion del registro fue exitosa", parent=self)

        self.limpiar_Grid()
        self.limpiar_text()
        self.estado_inicial("disabled")
        self.estado_botones("normal")

        if self.alta_modif == 1:
            ultimo_tabla_id = self.varOrdenes.traer_ultimo(0)
            self.llena_grilla(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla(self.clave)

        self.alta_modif = 0
        self.btn_nueva_orden.focus()

    # --------------------------------------------------------------------------------
    # VARIAS *
    # --------------------------------------------------------------------------------

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.limpiar_text()
            self.estado_botones("normal")
            self.estado_inicial("disabled")

    def fSalir(self):
        self.master.destroy()

    def fToparch(self):
        self.muevo_puntero_topend('TOP')

    def fFinarch(self):
        self.muevo_puntero_topend('END')

    def DobleClickGrid(self, event):
        self.fModificar_orden()

    def fNo_modifique(self, event):
        return "break"

    def fImprimir(self):
        self.creopdf()

    def fShowall(self):

        self.filtro_activo = "orden_repara ORDER by num_orden ASC"
        self.limpiar_Grid()
        self.llena_grilla("")

    def fNoretiradas(self):

        self.filtro_activo = "orden_repara WHERE fin_retirada = 'N' ORDER BY num_orden ASC"
        self.limpiar_Grid()
        self.llena_grilla("")

    def fEstadistica(self):

        self.filtro_anterior = self.filtro_activo
        self.filtro_activo = "orden_repara ORDER BY num_orden"

        datos = self.varOrdenes.consultar_ordenes(self.filtro_activo)

        total_ordenes = 0
        total_orden_pendientes = 0
        total_pesos_pendientes = 0
        total_orden_mesactual = 0
        total_pesos_mesactual = 0

        for row in datos:

            fecha_orden = datetime.date(row[2])
            mes_orden = fecha_orden.month
            ano_orden = fecha_orden.year
            mes_comparacion = date.today().month
            ano_comparacion = date.today().year

            total_ordenes += 1

            if row[19] == "N":
                total_orden_pendientes += 1
                total_pesos_pendientes += (float(row[18])+float(row[17]))

            if mes_comparacion == mes_orden and ano_comparacion == ano_orden:
                total_orden_mesactual += 1
                total_pesos_mesactual += (float(row[18])+float(row[17]))

         # if len(self.grid_orden.get_children()) > 0:
         #    self.grid_orden.selection_set(self.grid_orden.get_children()[0])

        total_pesos_mesactual = formatear_cifra(total_pesos_mesactual)
        total_pesos_pendientes = formatear_cifra(total_pesos_pendientes)

        self.strvar_estad_total.set(value=str(total_ordenes))
        self.strvar_estad_pendi.set(value=str(total_orden_pendientes))
        self.strvar_estad_mesact.set(value=str(total_orden_mesactual))
        self.strvar_estad_pespendi.set(value=str(total_pesos_pendientes))
        self.strvar_estad_pesmesact.set(value=str(total_pesos_mesactual))

        self.pantalla_estad = Toplevel()
        self.pantalla_estad.geometry('220x180+1200+200')
        self.pantalla_estad.transient(master=self.master)
        self.pantalla_estad.config(bg='light green', padx=5, pady=5)
        self.pantalla_estad.resizable(1, 1)
        self.pantalla_estad.title("Estadisticas")

        # muestro la imagen en el frame
        self.lbl_total_ordenes1 = Label(self.pantalla_estad, text="Total ordenes: ", bg="light blue",
                                        relief=RIDGE, bd=5)
        self.lbl_total_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_total, bg="plum1",
                                        relief=RIDGE, bd=5)
        self.lbl_pendi_ordenes1 = Label(self.pantalla_estad, text="Ordenes pendientes: ", bg="light blue",
                                        relief=RIDGE, bd=5)
        self.lbl_pendi_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_pendi, bg="plum1",
                                        relief="ridge", bd=5)
        self.lbl_pespendi_ordenes1 = Label(self.pantalla_estad, text="Pesos pendientes: ", bg="light blue",
                                           relief="ridge", bd=5)
        self.lbl_pespendi_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_pespendi, bg="plum1",
                                           relief=RIDGE, bd=5)
        self.lbl_mesact_ordenes1 = Label(self.pantalla_estad, text="Ordenes mes actual: ", bg="light blue",
                                         relief=RIDGE, bd=5)
        self.lbl_mesact_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_mesact, bg="plum1",
                                         relief=RIDGE, bd=5)
        self.lbl_pesmesact_ordenes1 = Label(self.pantalla_estad, text="Pesos mes actual: ", bg="light blue",
                                            relief="ridge", bd=5)
        self.lbl_pesmesact_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_pesmesact, bg="plum1",
                                            relief="ridge", bd=5)

        self.lbl_total_ordenes1.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_total_ordenes2.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_pendi_ordenes1.grid(row=1, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_pendi_ordenes2.grid(row=1, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_pespendi_ordenes1.grid(row=2, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_pespendi_ordenes2.grid(row=2, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_mesact_ordenes1.grid(row=3, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_mesact_ordenes2.grid(row=3, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_pesmesact_ordenes1.grid(row=4, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_pesmesact_ordenes2.grid(row=4, column=1, padx=5, pady=3, sticky="nsew")

        for widg in self.pantalla_estad.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

        #self.lbl_total_ordenes.pack(expand=1, side=TOP, fill=BOTH, pady=2, padx=2)
        self.pantalla_estad.grab_set()
        self.pantalla_estad.focus_set()

        mainloop()

        self.filtro_activo = self.filtro_anterior

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def fTraedeuda(self, codigo_cli):

        # Trae la deuda del cliente que se selecciona
        datos = self.varOrdenes.suma_deuda(codigo_cli)

        sumasaldo = 0
        for row in datos:
            sumasaldo += row[3] - row[4]

        return(sumasaldo)

    # ----------------------------------------------------------------------------
    # SEL -*-
    # ----------------------------------------------------------------------------

    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
        en que campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a Funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de como 
        quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                        "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:
            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])
            self.strvar_cli_datosmas.set(value=str(item[4] + ' - tel: ' + item[8] + ' / ' + item[9]))

        self.strvar_cli_deuda.set(value=str(self.fTraedeuda(self.strvar_codigo_cliente.get())))
        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # ----------------------------------------------------------------------------
    # BUSQUEDAS -*-
    # ----------------------------------------------------------------------------

    def fFiltrar_orden(self):

        if len(self.strvar_buscar_orden.get()) > 0:
            se_busca = self.strvar_buscar_orden.get()

            self.filtro_activo = "orden_repara WHERE INSTR(nombre_cliente, '" + se_busca + "') > 0" \
                                 + " OR " + "INSTR(equ_descripcion, '" + se_busca + "') > 0" \
                                 + " OR " + "INSTR(equ_grupo, '" + se_busca + "') > 0" \
                                 + " OR " + "INSTR(det_equipo, '" + se_busca + "') > 0"

            self.retorno = self.varOrdenes.buscar_entabla(self.filtro_activo)

            self.limpiar_Grid()
            self.llena_grilla2(self.filtro_activo)
        else:
            messagebox.showwarning("Alerta", "No ingreso busqueda", parent=self)
            self.entry_buscar_orden.focus()

    # ----------------------------------------------------------------------------
    # CALCULOS -*-
    # ----------------------------------------------------------------------------

    def sumar_totalfinal(self):

        try:

            # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
            if not control_forma(list(self.strvar_total_partes.get())):
                self.strvar_total_partes.set(value="0")
                self.entry_total_partes.focus()
                return
            if not control_forma(list(self.strvar_total_manodeobra.get())):
                self.strvar_total_manodeobra.set(value="0")
                self.entry_total_manodeobra.focus()
                return

            # Control de valor en blanco o solo un . o -
            if (self.strvar_total_partes.get() == "" or self.strvar_total_partes.get() == "."
                    or self.strvar_total_partes.get() == "-"):
                self.strvar_total_partes.set(value="0")
            if (self.strvar_total_manodeobra.get() == "" or self.strvar_total_manodeobra.get() == "."
                    or self.strvar_total_manodeobra.get() == "-"):
                self.strvar_total_manodeobra.set(value="0")

            # control de valor en cero o si tiene mas de dos decimales lo trunco a dos
            if float(self.strvar_total_partes.get()) == 0:
                self.strvar_total_partes.set(value="0")
            else:
                self.strvar_total_partes.set(value=str(round(float(self.strvar_total_partes.get()), 2)))
            if float(self.strvar_total_manodeobra.get()) == 0:
                self.strvar_total_manodeobra.set(value="0")
            else:
                self.strvar_total_manodeobra.set(value=str(round(float(self.strvar_total_manodeobra.get()), 2)))

            v1 = float(self.strvar_total_partes.get())
            v2 = float(self.strvar_total_manodeobra.get())

            self.strvar_tot_final.set(value=str(round((v1 + v2), 2)))

        except:

            messagebox.showerror("Error", "Revise datos ingresados", parent=self)
            self.entry_total_partes.focus()
            return

    # ----------------------------------------------------------------------------
    # INFORMES -*-
    # ----------------------------------------------------------------------------

    def creopdf(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_orden.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return
        else:
            # Debo traer el registro completo desde la Tabla. Este metodo de abm_ordenrepar, me trase solo el
            # registro requerido con Id que esta en self.clave
            datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)
            # Cargo datos extra del cliente
            datos_cliente = self.varOrdenes.traer_un_cliente(datos_registro_selec[4])
            telef_cliente = datos_cliente[8]+' - '+datos_cliente[9]

        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """

        # esto siempre debe estar
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 5)
        # salto de hoja automatico
        pdf.set_auto_page_break(auto=True, margin=20)
        # -----------------------------------------------------------------------------------

        # armado de encabezado --------------------------------------------------------------
        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
        self.pdf_numero_orden = str(datos_registro_selec[1])
        self.pdf_codigo_cliente = str(datos_registro_selec[4])
        self.pdf_nombre_cliente = datos_registro_selec[5]
        self.pdf_datos_encabezado_orden = (self.pdf_numero_orden+' - '+self.pdf_nombre_cliente+
                                           ' - ('+self.pdf_codigo_cliente+') - Telefono '+str(telef_cliente))
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0, h=5, txt='Fecha/Hora: ' + feac + ' - Orden Nº ' + self.pdf_datos_encabezado_orden, border=1,
                 align='C', fill=0, ln=1)
        # ----------------------------------------------------------------------------------

        self.pdf_desc = str(datos_registro_selec[6])
        self.pdf_grupo = str(datos_registro_selec[7])
        self.pdf_acces = datos_registro_selec[8]
        self.pdf_estado = datos_registro_selec[9]
        self.pdf_cuenta = datos_registro_selec[10]
        self.pdf_requerido = datos_registro_selec[11]
        self.pdf_diagnostico = datos_registro_selec[12]
        self.pdf_presupuesto = datos_registro_selec[13]
        self.pdf_realizado = datos_registro_selec[14]
        self.pdf_partes = datos_registro_selec[15]
        self.pdf_anotaciones = datos_registro_selec[16]
        self.pdf_totpartes = str(datos_registro_selec[18])
        self.pdf_totmanobra = str(datos_registro_selec[17])
        self.totalpagar = str(datos_registro_selec[17]+datos_registro_selec[18])

        cuerpo_1 = 'Equipo: '+self.pdf_desc+' - '+self.pdf_grupo
        cuerpo_2 = 'Accesorios: '+self.pdf_acces
        cuerpo_12 = 'Estado del equipo: '+self.pdf_estado
        cuerpo_3 = 'Cuentas y contraseñas: '+self.pdf_cuenta
        cuerpo_4 = 'Requerimiento: '+self.pdf_requerido
        cuerpo_5 = 'Diagnostico: '+self.pdf_diagnostico
        cuerpo_6 = 'Presupuesto: '+self.pdf_presupuesto
        cuerpo_7 = 'Trabajo realizado: '+self.pdf_realizado
        cuerpo_8 = 'Trabajo partes reemplazadas: '+self.pdf_partes
        cuerpo_9 = 'Trabajo anotaciones: '+self.pdf_anotaciones
        cuerpo_10 = 'Total partes $ : '+self.pdf_totpartes+\
                    ' - Total Mano de Obra $: '+self.pdf_totmanobra+' - Total a pagar $: '+self.totalpagar
        cuerpo_11 = ('NOTA: Pasado 90 dias de recibir su equipo, la casa no se responsabiliza por el estado '
                     'ni el reintegro del mismo')

        # talon cliente ----------------------------------------------
        pdf.multi_cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_12, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0)
        # espacios
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_11, align='L', fill=0)

        # Espaciado entre cuerpos ------------------------------------
        pdf.cell(w=0, h=15, txt='', align='L', fill=0, ln=1)

        # talon interno ----------------------------------------------
        # Encabezado -------------------------------------------------
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0, h=5, txt='Fecha/Hora: ' + feac + '  - Orden Nº ' + self.pdf_datos_encabezado_orden, border=1,
                 align='C', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Cuerpo segundo talon ----------------------------------------
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Equipo: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=0, h=5, txt=self.pdf_desc, align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Accesorios y Estado del equipo: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=0, h=5, txt=self.pdf_acces+'  -  '+self.pdf_estado, align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Cuentas y contraseñas: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=0, h=5, txt=self.pdf_cuenta, align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Requerimiento: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=0, h=5, txt=self.pdf_requerido, align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Diagnostico: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_diagnostico, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Presupuesto: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=0, h=5, txt=self.pdf_presupuesto, align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Trabajo realizado: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_realizado, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Partes reemplazadas: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=0, h=5, txt=self.pdf_partes, align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Anotaciones: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_anotaciones, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='Bateria-Teclado-Camara-Sonido-Mic-Wifi-Lectora-Msconfig-Drivers-Fecha/Hora-Temperatura', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Disco-Antivirus-Actualizaciones-Navegadores-Crack-Restauracion-Ccleaner-Office', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Totales: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_10, align='L', fill=0)
        #pdf.line(10, 210, 190, 210)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Espaciado entre cuerpos ------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='Retirada................................ ', align='R', fill=0, ln=1)

        # # -----------------------------------------------------------------------------
        # pdf.multi_cell(w=0, h=5, txt='Orden de reparacion ' + self.pdf_datos_encabezado_orden, border=1, align='C', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_3, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_5, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_6, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_7, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_8, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_9, align='L', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=cuerpo_10, align='L', border=1, fill=0)
        # # -----------------------------------------------------------------------------

        """ para crear una linea recta
        #pdf.rect(x=50, y=80, w=70, h=95)
        #pdf.line(20, 150, 190, 180)
        # para crear una linea de puntos
        #pdf.dashed_line(15, 78, 80, 90, dash_length=5, space_length=6)
        # para crear un elipse
        #pdf.ellipse(x=10, y=15, w=50, h=80, style='')
        # insertar imagenes y texto
        #pdf.text(x=60, y=50, txt='Hola muchachos')
        #pd.image('impresora.png', x=10, y=10, w=30, h=30) #, link=url) """
        # ----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        """
        Para insertar lineas de escritura una debajo de otra
        por ejemplo :
        linea 1
        linea 2
        linea 3

        for i in range(1, 41):
            pdf.cell(0, 10, f'Esta es la linea {i} :D', ln=True)
        """
        # -------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # margenes izq derecha arriba y abajo
        """
        Margen antes de terminar la hoja o sea en tre la ultima linea de la hoja y el fin de la hoja
        pdf.set_auto_page_break(auto=True, margin=15)
        """
        # -------------------------------------------------------------------------------------

        # # para listar una base de datos forma simple basica
        # # lista_de_datos = retorno de la base de datos

        # # al ultimo le ponemos w=0 y abarca todo el resto del renglon hasta el final
        # pdf.cell(w=30, h=8, txt='Codigo', border=1, align='C', fill=0)
        # pdf.cell(w=25, h=8, txt='Rubro', border=1, align='C', fill=0)
        # pdf.cell(w=20, h=8, txt='Marca', border=1, align='C', fill=0)
        # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)

        # pdf.set_font('Arial', '', 5)
        # # retorno una lista con los registros
        # datos = self.varOrdenes.consultar_orden("")
        # for row in datos:
        #     pdf.cell(w=30, h=5, txt=row[1], border=1, align='C', fill=0)
        #     pdf.cell(w=25, h=5, txt=row[2], border=1, align='C', fill=0)
        #     pdf.cell(w=20, h=5, txt=row[3], border=1, align='C', fill=0)
        #     mostrar = row[4]
        #     cadena = (mostrar[:100])
        #     pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0)

        pdf.output('hoja.pdf')

        # # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    def muevo_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_orden.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_orden.selection_set(rg)
            # pone el primero Id
            self.grid_orden.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_orden.yview(self.grid_orden.index(self.grid_orden.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_orden.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_orden.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_orden.focus(rg)
            # lleva el foco al final del treeview
            self.grid_orden.yview(self.grid_orden.index(self.grid_orden.get_children()[-1]))
