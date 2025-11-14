#--------------------------------------------------
# GRID
# ESTADOS
# CRUD
# VARIAS
# BUSQUEDAS
# CALCULOS
# SEL
# PUNTEROS
#--------------------------------------------------
from funciones import *
from funcion_new import *
from planilla_caja_ABM import datosPlanilla
#--------------------------------------------------
#from tkinter import *
#from tkinter import ttk
#from tkinter import messagebox
#import tkinter as tk
#--------------------------------------------------
from datetime import date, datetime, timedelta
import random
from PIL import Image, ImageTk
#from PDF_clase import *

class PlaniCaja(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        # ---------------------------------------------------------------------------------
        # Instanciaciones

        """ Creo una instancia de la clase en _ABM que le corresponde. Le paso la pantalla para poder usar los parent 
        en los messagebox. A varFuncion_new, le paso tambien la pantalla por el mismo motivo y ademas debo pasarle 
        la variable instanciada con el _ABM, de esa manera tambien le paso a funcion la instanciacion de clase del 
        _ABM y asi puede usar los metods que estan en el _ABM """

        self.master.grab_set()
        self.master.focus_set()

        self.varPlanilla = datosPlanilla(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # PANTALLA
        # ---------------------------------------------------------------------------------

        # Esto esta agregado para centrar las ventanas en la pantalla
        # master.geometry("880x510")
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 650
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        """ PROCEDIMIENTO PARA QUE QUEDE MOSTRANDO LA ULTIMA PLANILLA CARGADA - Obtengo la fecha de la ultima 
        planilla cargada filtrar la tabla (en str pero al reves YYY-mm-dd) """
        self.obtener_fecha_inicial()
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        self.create_widgets()
        self.llena_grilla("")
        # ------------------------------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        Otras funciones para manejar los elementos seleccionados incluyen:
        selection_add(): añade elementos a la selección.
        selection_remove(): remueve elementos de la selección.
        selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        selection_toggle(): cambia la selección de un elemento. """

        # guarda en item el Id del elemento fila en este caso fila 0
        item = self.grid_planilla.identify_row(0)
        self.grid_planilla.selection_set(item)
        # pone el foco en el item seleccionado
        self.grid_planilla.focus(item)

        # ---------------------------------------------------------------------------
        self.estado_inicial()
        # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  WIDGETS
    # ---------------------------------------------------------------------------

    def create_widgets(self):

        # ---------------------------------------------------------------------------------
        # TITULOS
        # ---------------------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('planilla.png')
        self.photo3 = self.photo3.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ventas = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_ventas = Label(self.frame_titulo_top, image=self.png_ventas, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Planilla de Caja",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ventas.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # VARIABLES GENERALES
        # ---------------------------------------------------------------------------------

        self.alta_modif = 0
        self.dato_seleccion = ""
        self.retorno = ""
        vcmd = (self.register(validar), '%P')
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------------------

        self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")

        self.traer_dolarhoy()

        # la obtengo en el metodo -obtener_fecha_inicial-
        self.strvar_fecha_planilla = tk.StringVar(value=self.fecha_aux)
        # esta fecha es para recuperar la fecha que estaba activa antes de cometer algun error
        # de ingreso de fecha (en blanco, etc), y asi poder recuperar la anterior que se estaba trabajando
        self.strvar_fecha_error = tk.StringVar(value=self.fecha_aux)

        self.strvar_tipomov = tk.StringVar(value="")
        self.strvar_detalle_movim = tk.StringVar(value="")
        self.strvar_cliente = tk.StringVar(value="")
        self.strvar_codcli = tk.StringVar(value="0")
        self.strvar_proved = tk.StringVar(value="")
        self.strvar_forma_pago = tk.StringVar(value="")
        self.strvar_detalle_pago = tk.StringVar(value="")
        self.strvar_garantia = tk.StringVar(value="")
        self.strvar_observaciones = tk.StringVar(value="")

        self.strvar_buscostring = tk.StringVar(value="")

        self.strvar_ingreso = tk.StringVar(value="0.00")
        self.strvar_costo = tk.StringVar(value="0.00")
        self.strvar_egreso = tk.StringVar(value="0.00")
        self.strvar_cantidad = tk.StringVar(value="1")
        self.strvar_pagos_ctacte = tk.StringVar(value="0.00")
        self.strvar_compras = tk.StringVar(value="0.00")

        # totales que surgen de multiplicar por la cantidad
        self.strvar_totingresos = tk.StringVar(value="0.00")
        self.strvar_totcosto = tk.StringVar(value="0.00")
        self.strvar_total_egresos = tk.StringVar(value="0.00")

        # totales de pie de pantalla
        self.strvar_total_ingresos = tk.StringVar(value="0.00")
        self.strvar_total_costos = tk.StringVar(value="0.00")
        self.strvar_total_utilidad = tk.StringVar(value="0.00")
        self.strvar_total_pagos = tk.StringVar(value="0.00")
        self.strvar_total_compras = tk.StringVar(value="0.00")
        self.strvar_total_util_menos_egr = tk.StringVar(value="0.00")
        self.strvar_total_limpio_artic = tk.StringVar(value="0.00")
        self.strvar_total_limpio_serv = tk.StringVar(value="0.00")

        # del checkbox
        self.strvar_check1 = tk.StringVar(value="0")

        # para mostrar datos del articulo
        self.strvar_marca_mostrar = tk.StringVar(value="")
        self.strvar_rubro_mostrar = tk.StringVar(value="")
        self.strvar_precio_mostrar = tk.StringVar(value="0.00")

        # para datos en tabla cuenta corriente
        self.strvar_clavemov = tk.StringVar(value="0")
        self.strvar_clavemov_ant = tk.StringVar(value="0")
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # TREEVIEW - GRID
        # ---------------------------------------------------------------------------------

        self.frame_tvw_planilla=LabelFrame(self.master, text="Planilla de caja: ", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_planilla)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_planilla = ttk.Treeview(self.frame_tvw_planilla, height=6, columns=("col1", "col2", "col3", "col4",
                                                    "col5", "col6", "col7", "col8", "col9", "col10", "col11", "col12",
                                                    "col13", "col14", "col15", "col16", "col17", "col18", "col19"))

        self.grid_planilla.bind("<Double-Button-1>", self.DobleClickGrid_pla)

        self.grid_planilla.column("#0", width=40, anchor=CENTER, minwidth=60)
        self.grid_planilla.column("col1", width=80, anchor=CENTER, minwidth=70)
        self.grid_planilla.column("col2", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col3", width=350, anchor=CENTER, minwidth=250)
        self.grid_planilla.column("col4", width=30, anchor=CENTER, minwidth=60)
        self.grid_planilla.column("col5", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col6", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col7", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col8", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col9", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col10", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col11", width=150, anchor=CENTER, minwidth=150)
        self.grid_planilla.column("col12", width=150, anchor=CENTER, minwidth=100)
        self.grid_planilla.column("col13", width=150, anchor=CENTER, minwidth=250)
        self.grid_planilla.column("col14", width=100, anchor=CENTER, minwidth=250)
        self.grid_planilla.column("col15", width=100, anchor=CENTER, minwidth=250)
        self.grid_planilla.column("col16", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col17", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col18", width=100, anchor=CENTER, minwidth=80)
        self.grid_planilla.column("col10", width=100, anchor=CENTER, minwidth=80)

        self.grid_planilla.heading("#0", text="Id", anchor=CENTER)
        self.grid_planilla.heading("col1", text="Fecha", anchor=CENTER)
        self.grid_planilla.heading("col2", text="Tipo Mov.", anchor=CENTER)
        self.grid_planilla.heading("col3", text="Detalle", anchor=CENTER)
        self.grid_planilla.heading("col4", text="Cant.", anchor=CENTER)
        self.grid_planilla.heading("col5", text="Ingresos(I)", anchor=CENTER)
        self.grid_planilla.heading("col6", text="Total Ingresos", anchor=CENTER)
        self.grid_planilla.heading("col7", text="Egresos(E)", anchor=CENTER)
        self.grid_planilla.heading("col8", text="Costos", anchor=CENTER)
        self.grid_planilla.heading("col9", text="Pagos CtaCte(I)", anchor=CENTER)
        self.grid_planilla.heading("col10", text="Compras(E)", anchor=CENTER)
        self.grid_planilla.heading("col11", text="Cliente", anchor=CENTER)
        self.grid_planilla.heading("col12", text="Tipo pago", anchor=CENTER)
        self.grid_planilla.heading("col13", text="Detalle pago", anchor=CENTER)
        self.grid_planilla.heading("col14", text="Garantia", anchor=CENTER)
        self.grid_planilla.heading("col15", text="Observaciones", anchor=CENTER)
        self.grid_planilla.heading("col16", text="Proveedor", anchor=CENTER)
        self.grid_planilla.heading("col17", text="CtaCte", anchor=CENTER)
        self.grid_planilla.heading("col18", text="ClaveMov", anchor=CENTER)
        self.grid_planilla.heading("col19", text="Codigo Cliente", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_planilla, orient="horizontal")
        scroll_y = Scrollbar(self.frame_tvw_planilla, orient="vertical")
        self.grid_planilla.config(xscrollcommand=scroll_x.set)
        self.grid_planilla.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_planilla.xview)
        scroll_y.config(command=self.grid_planilla.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_planilla['selectmode'] = 'browse'

        self.grid_planilla.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_planilla.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # BUSCAR UN MOVIMIENTO
        # ---------------------------------------------------------------------------------

        self.frame_buscar_movimiento=LabelFrame(self.master, text="", foreground="red")

        self.lbl_buscar_movim = Label(self.frame_buscar_movimiento, text="Buscar: ")
        self.lbl_buscar_movim.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_movim=Entry(self.frame_buscar_movimiento, textvariable=self.strvar_buscostring, width=70)
        self.entry_buscar_movim.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.btn_buscar_movim = Button(self.frame_buscar_movimiento, text="Buscar", command=self.fBuscar_en_tabla,
                                       bg="CadetBlue", fg="white", width=35)
        self.btn_buscar_movim.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_mostrar_todo = Button(self.frame_buscar_movimiento, text="Mostrar todo", command=self.fShowall,
                                       bg="CadetBlue", fg="white", width=35)
        self.btn_mostrar_todo.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        self.frame_buscar_movimiento.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # BOTONES
        # ---------------------------------------------------------------------------------

        self.frame_botones_tvw=LabelFrame(self.master, text="", foreground="red")

        # BOTONES DEL TREEVIEW
        self.btn_nuevoitem = Button(self.frame_botones_tvw, text="Nuevo Item", command=self.fNuevoItem, width=16,
                                    bg="blue", fg="white")
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)
        self.btn_editaitem = Button(self.frame_botones_tvw, text="Edita Item", command=self.fEditaItem, width=16,
                                    bg="blue", fg="white")
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)
        self.btn_borraitem = Button(self.frame_botones_tvw, text="Elimina Item", command=self.fBorraItem, width=16,
                                    bg="blue", fg="white")
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)
        self.btn_guardaritem = Button(self.frame_botones_tvw, text="Guardar item", command=self.fGuardar, width=16,
                                      bg="green", fg="white")
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)
        self.btn_Cancelar = Button(self.frame_botones_tvw, text="Cancelar", command=self.fCancelar, width=16,
                                   bg="black", fg="white")
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)
        self.btn_Reset = Button(self.frame_botones_tvw, text="Reset", command=self.fReset, width=16, bg="black",
                                fg="white")
        self.btn_Reset.grid(row=0, column=5, padx=5, pady=2)
        self.btn_Resumen = Button(self.frame_botones_tvw, text="Resumen mes", command=self.fResumen, width=18,
                                  bg="light blue", fg="black")
        self.btn_Resumen.grid(row=0, column=6, padx=5, pady=2)

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_botones_tvw, text="", image=self.photo4, command=self.fToparch,
                                 bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=7, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_botones_tvw, text="", image=self.photo5, command=self.fFinarch,
                                 bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=8, padx=5, sticky="nsew", pady=2)

        self.frame_botones_tvw.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # ENTRYS
        # ---------------------------------------------------------------------------------

        # CREACION LABELFRAMES ------------------------------------------------------------
        self.frame_entrys_planilla=LabelFrame(self.master, text="", foreground="red")
        self.frame_entrys_planilla2=LabelFrame(self.master, text="", foreground="red")
        self.frame_entrys_planilla3=LabelFrame(self.master, text="", foreground="red")
        self.frame_entrys_planilla4=LabelFrame(self.master, text="", foreground="red")
        self.frame_entrys_planilla5=LabelFrame(self.master, text="", foreground="red")

        # LABELFRAME DATOS GENERALES DEL MOVIMIENTO

        # FECHA ---------------------------------------------------------------------------
        self.lbl_fecha_planilla = Label(self.frame_entrys_planilla, text="Fecha: ", justify="left")
        self.lbl_fecha_planilla.grid(row=0, column=0, padx=3, pady=2, sticky=W)
        self.entry_fecha_planilla = Entry(self.frame_entrys_planilla, textvariable=self.strvar_fecha_planilla,
                                          width=10, justify="right")
        self.entry_fecha_planilla.bind("<FocusIn>", self.fVer_blanco)
        self.entry_fecha_planilla.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_planilla.grid(row=0, column=1, padx=3, pady=2, sticky=E)

        # ATRAS EN LA FECHA ---------------------------------------------------------------
        self.photo6 = Image.open('atras.png')
        self.photo6 = self.photo6.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo6 = ImageTk.PhotoImage(self.photo6)
        self.btnIzquierda = Button(self.frame_entrys_planilla, text="", image=self.photo6, command=self.fAntes,
                                   bg="grey", fg="white")
        self.btnIzquierda.grid(row=0, column=2, padx=5, sticky="nsew", pady=2)

        # ADELANTE EN LA FECHA -------------------------------------------------------------
        self.photo7 = Image.open('avance.png')
        self.photo7 = self.photo7.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo7 = ImageTk.PhotoImage(self.photo7)
        self.btnDerecha = Button(self.frame_entrys_planilla, text="", image=self.photo7, command=self.fDespues,
                                 bg="grey", fg="white")
        self.btnDerecha.grid(row=0, column=3, padx=5, sticky="nsew", pady=2)

        # COMBO TIPO DE MOVIMIENTO ----------------------------------------------------------
        self.lbl_tipomov = Label(self.frame_entrys_planilla, text="Tipo de movimiento: ", justify="left")
        self.lbl_tipomov.grid(row=0, column=4, padx=3, pady=2, sticky=W)
        self.combo_tipomov = ttk.Combobox(self.frame_entrys_planilla, textvariable=self.strvar_tipomov,
                                          state='readonly', width=23)
        self.combo_tipomov['value'] = self.varPlanilla.combo_input("tm_descripcion","tipo_movim",
                                                                   "tm_ingegr")
        # self.combo_tipomov['value'] = ["Ventas(I)", "Servicios MO(I)", "Pagos cuentas corrientes(I)",
        # "Ingresos varios(I)", "Compras(E)", "Egresos varios(E)"]
        self.combo_tipomov.current(0)
        self.combo_tipomov.bind('<Tab>', lambda e: self.divido_tipomov())
        self.combo_tipomov.grid(row=0, column=5, padx=5, pady=2, sticky=W)

        # BOTON BUSQUEDA CLIENTE -------------------------------------------------------------
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_entrys_planilla, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=6, padx=5, pady=2, sticky=E)

        # ENTRY CLIENTE -----------------------------------------------------------------------
        self.lbl_cliente = Label(self.frame_entrys_planilla, text="Cliente: ", justify="left")
        self.lbl_cliente.grid(row=0, column=7, padx=3, pady=2, sticky=W)
        self.entry_cliente = Entry(self.frame_entrys_planilla, textvariable=self.strvar_cliente, width=60, justify="left")
        self.entry_cliente.grid(row=0, column=8, padx=3, pady=2, sticky=E)
        self.lbl_codigo_cliente = Label(self.frame_entrys_planilla, textvariable=self.strvar_codcli, justify="left")
        self.lbl_codigo_cliente.grid(row=0, column=9, padx=3, pady=2, sticky=E)

        # LABELFRAME DETALLE DE MOVIMIENTOS

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE -----------------------------
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = Button(self.frame_entrys_planilla2, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=5, pady=2, sticky=E)

        # ENTRY DETALLE DEL MOVIMIENTO ----------------------------------------------------------
        self.lbl_detalle_movim = Label(self.frame_entrys_planilla2, text="Detalle/Articulo: ", justify="left")
        self.lbl_detalle_movim.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.entry_detalle_movim = Entry(self.frame_entrys_planilla2, textvariable=self.strvar_detalle_movim, width=144,
                                         justify="left")
        self.entry_detalle_movim.grid(row=0, column=2, padx=3, pady=2, sticky=E)

        # LABELFRAME IMPORTES DEL MOVIMIENTO

        # IMPORTE DEL INGRESO -------------------------------------------------------------------
        self.lbl_ingresos1 = Label(self.frame_entrys_planilla3, text="Ingresos: ", justify="left")
        self.lbl_ingresos1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.entry_ingresos = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_ingreso, width=10,
                                    justify="right")
        self.entry_ingresos.config(validate="key", validatecommand=vcmd)
        self.entry_ingresos.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_ingresos.grid(row=0, column=1, padx=2, pady=2, sticky=E)

        # IMPORTE COSTO -------------------------------------------------------------------------
        self.lbl_costo = Label(self.frame_entrys_planilla3, text="Costos: ", justify="left")
        self.lbl_costo.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_costo = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_costo, width=10, justify="right")
        self.entry_costo.config(validate="key", validatecommand=vcmd)
        self.entry_costo.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_costo.grid(row=0, column=3, padx=2, pady=2, sticky=E)

        # CANTIDAD -------------------------------------------------------------------------------
        self.lbl_cantidad = Label(self.frame_entrys_planilla3, text="Cantidad: ", justify="left")
        self.lbl_cantidad.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.entry_cantidad = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_cantidad, width=6,
                                    justify="right")
        self.entry_cantidad.config(validate="key", validatecommand=vcmd)
        self.entry_cantidad.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_cantidad.grid(row=0, column=5, padx=2, pady=2, sticky=E)

        # TOTAL CALCULADO INGRESO POR CANTIDAD ---------------------------------------------------
        self.lbl_totventart1 = Label(self.frame_entrys_planilla3, text="Total Ing.: ", justify="left")
        self.lbl_totventart1.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        self.lbl_totventart2 = Label(self.frame_entrys_planilla3, textvariable=self.strvar_totingresos, width=10,
                                     justify="right")
        self.lbl_totventart2.grid(row=0, column=7, padx=2, pady=2, sticky=E)

        # TOTAL CALCULADO COSTO POR CANTIDAD ------------------------------------------------------
        self.lbl_totcosto1 = Label(self.frame_entrys_planilla3, text="Total Costo: ", justify="left")
        self.lbl_totcosto1.grid(row=0, column=8, padx=2, pady=2, sticky=W)
        self.lbl_totcosto2 = Label(self.frame_entrys_planilla3, textvariable=self.strvar_totcosto, width=10,
                                   justify="right")
        self.lbl_totcosto2.grid(row=0, column=9, padx=2, pady=2, sticky=E)

        # IMPORTE DE EGRESO -----------------------------------------------------------------------
        self.lbl_egreso = Label(self.frame_entrys_planilla3, text="Egreso: ", justify="left")
        self.lbl_egreso.grid(row=0, column=10, padx=2, pady=2, sticky=W)
        self.entry_egreso = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_egreso, width=10,
                                  justify="right")
        self.entry_egreso.config(validate="key", validatecommand=vcmd)
        self.entry_egreso.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_egreso.grid(row=0, column=11, padx=2, pady=2, sticky=E)

        # IMPORTE PAGOS A CUENTA CORRIENTE ---------------------------------------------------------
        self.lbl_pagoscta = Label(self.frame_entrys_planilla3, text="Pagos cta.cte.: ", justify="left")
        self.lbl_pagoscta.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.entry_pagoscta = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_pagos_ctacte, width=10,
                                    justify="right")
        self.entry_pagoscta.config(validate="key", validatecommand=vcmd)
        self.entry_pagoscta.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_pagoscta.bind("<FocusOut>", self.tildo_cuenta)
        self.entry_pagoscta.grid(row=1, column=1, padx=2, pady=2, sticky=E)

        # IMPORTE DE COMPRAS A PROVEEDORES U OTRAS --------------------------------------------------
        self.lbl_compras = Label(self.frame_entrys_planilla3, text="Compras: ", justify="left")
        self.lbl_compras.grid(row=1, column=2, padx=2, pady=2, sticky=W)
        self.entry_compras = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_compras, width=10,
                                   justify="right")
        self.entry_compras.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_compras.config(validate="key", validatecommand=vcmd)
        self.entry_compras.grid(row=1, column=3, padx=2, pady=2, sticky=E)

        # BOTON BUSQUEDA PROVEEDOR SI CORRESPPONDE --------------------------------------------------
        self.photo_bus_prov = Image.open('buscar.png')
        self.photo_bus_prov = self.photo_bus_prov.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_prov = ImageTk.PhotoImage(self.photo_bus_prov)
        self.btn_bus_prov = Button(self.frame_entrys_planilla3, text="", image=self.photo_bus_prov,
                                   command=self.fBusprov, bg="grey", fg="white")
        self.btn_bus_prov.grid(row=1, column=4, padx=5, pady=2, sticky=E)

        # ENTRY PROVEEDOR ----------------------------------------------------------------------------
        self.lbl_proved = Label(self.frame_entrys_planilla3, text="Proveedor: ", justify="left")
        self.lbl_proved.grid(row=1, column=5, padx=3, pady=2, sticky=W)
        self.entry_proved = Entry(self.frame_entrys_planilla3, textvariable=self.strvar_proved, width=93, justify="left")
        self.entry_proved.grid(row=1, column=6, columnspan=8, padx=8, pady=2, sticky=E)

        # CHECKBOX SI ES MOVIMIENTO A CUENTA CORRIENTE -----------------------------------------------
        self.check_ctacte = tk.Checkbutton(self.frame_entrys_planilla3, text='CC', variable=self.strvar_check1,
                                           onvalue = 1, offvalue= 0)
        self.check_ctacte.grid(row=1, column=13, padx=3, pady=2, sticky=E)

        # COMBOBOS FORMA DE PAGO ----------------------------------------------------------------------
        self.lbl_forma_pago = Label(self.frame_entrys_planilla4, text="Pago: ", justify="left")
        self.lbl_forma_pago.grid(row=0, column=0, padx=3, pady=2, sticky=W)
        self.combo_forma_pago = ttk.Combobox(self.frame_entrys_planilla4, textvariable=self.strvar_forma_pago,
                                             state='readonly', width=20)
        self.combo_forma_pago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                          "Cheques", "Otros"]
        self.combo_forma_pago.current(0)
        self.combo_forma_pago.grid(row=0, column=1, padx=5, pady=2, sticky=W)

        # ENTRY  DETALLE DEL PAGO ---------------------------------------------------------------------
        self.entry_detalle_pago = Entry(self.frame_entrys_planilla4, textvariable=self.strvar_detalle_pago, width=135,
                                        justify="left")
        self.entry_detalle_pago.grid(row=0, column=2, padx=3, pady=2, sticky=E)

        # ENTRY GARANTIAS -----------------------------------------------------------------------------
        self.lbl_garantia = Label(self.frame_entrys_planilla5, text="Garantias: ", justify="left")
        self.lbl_garantia.grid(row=0, column=0, padx=3, pady=2, sticky=W)
        self.entry_garantia = Entry(self.frame_entrys_planilla5, textvariable=self.strvar_garantia, width=152,
                                    justify="left")
        self.entry_garantia.grid(row=0, column=1, padx=3, pady=2, sticky=E)

        # ENTRY OBSERVACIONES --------------------------------------------------------------------------
        self.lbl_observaciones = Label(self.frame_entrys_planilla5, text="Observaciones: ", justify="left")
        self.lbl_observaciones.grid(row=1, column=0, padx=3, pady=2, sticky=W)
        self.entry_observaciones = Entry(self.frame_entrys_planilla5, textvariable=self.strvar_observaciones, width=152,
                                         justify="left")
        self.entry_observaciones.grid(row=1, column=1, padx=3, pady=2, sticky=E)
        # ---------------------------------------------------------------------------------

        # packs
        self.frame_entrys_planilla.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_entrys_planilla2.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_entrys_planilla3.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_entrys_planilla4.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_entrys_planilla5.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        # ---------------------------------------------------------------------------------
        # CUADRO TOTALES MOVIMIENTO

        self.frame_totales=LabelFrame(self.master, text="", foreground="red")

#        fff = tkFont.Font(family="Arial", size=8, weight="bold")

        # TOTAL INGRESOS DE LA FECHA ------------------------------------------------------
        self.lbl_total_ventart1 = Label(self.frame_totales, text="Total ingresos: ", fg="green", justify="left")
        self.lbl_total_ventart1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_total_ventart2 = Label(self.frame_totales, textvariable=self.strvar_total_ingresos, width=12,
                                        justify="left")
        self.lbl_total_ventart2.grid(row=0, column=1, padx=2, pady=2, sticky=E)

        # TOTAL COSTOS DE LA FECHA --------------------------------------------------------
        self.lbl_total_costos1 = Label(self.frame_totales, text="Total costos: ", fg="red", justify="left")
        self.lbl_total_costos1.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.lbl_total_costos2 = Label(self.frame_totales, textvariable=self.strvar_total_costos, width=12,
                                       justify="left")
        self.lbl_total_costos2.grid(row=1, column=1, padx=2, pady=2, sticky=E)

        # TOTAL UTILIDAD DE LA FECHA ( VENTAS MENOS COSTOS) --------------------------------
        self.lbl_total_utilidad1 = Label(self.frame_totales, text="Utilidad: ", fg="blue", justify="left")
        self.lbl_total_utilidad1.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.lbl_total_utilidad2 = Label(self.frame_totales, textvariable=self.strvar_total_utilidad, width=12,
                                         justify="left")
        self.lbl_total_utilidad2.grid(row=0, column=3, padx=2, pady=2, sticky=E)

        # TOTAL EGRESOS DE LA FECHA --------------------------------------------------------
        self.lbl_total_egresos1 = Label(self.frame_totales, text="Total Egresos: ", fg="red", justify="left")
        self.lbl_total_egresos1.grid(row=1, column=2, padx=2, pady=2, sticky=W)
        self.lbl_total_egresos2 = Label(self.frame_totales, textvariable=self.strvar_total_egresos, width=12,
                                        justify="left")
        self.lbl_total_egresos2.grid(row=1, column=3, padx=2, pady=2, sticky=E)

        # TOTAL UTILIDAD PERO AHORA MENOS LOS EGRESOS ---------------------------------------
        self.lbl_total_util_menos_egre1 = Label(self.frame_totales, text="Total Util.-Egr.: ", fg="blue", justify="left")
        self.lbl_total_util_menos_egre1.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.lbl_total_util_menos_egre2 = Label(self.frame_totales, textvariable=self.strvar_total_util_menos_egr,
                                                width=12, justify="left")
        self.lbl_total_util_menos_egre2.grid(row=0, column=5, padx=2, pady=2, sticky=E)

        # TOTAL PAGOS DE LA FECHA -----------------------------------------------------------
        self.lbl_total_pagos1 = Label(self.frame_totales, text="Total Pagos: ", fg="green", justify="left")
        self.lbl_total_pagos1.grid(row=1, column=4, padx=2, pady=2, sticky=W)
        self.lbl_total_pagos2 = Label(self.frame_totales, textvariable=self.strvar_total_pagos, width=12, justify="left")
        self.lbl_total_pagos2.grid(row=1, column=5, padx=2, pady=2, sticky=E)

        # TOTAL COMPRAS DE LA FECHA ---------------------------------------------------------
        self.lbl_total_compras1 = Label(self.frame_totales, text="Total Compras: ", fg="red", justify="left")
        self.lbl_total_compras1.grid(row=0, column=8, padx=2, pady=2, sticky=W)
        self.lbl_total_compras2 = Label(self.frame_totales, textvariable=self.strvar_total_compras, width=12,
                                        justify="left")
        self.lbl_total_compras2.grid(row=0, column=9, padx=2, pady=2, sticky=E)

        # TOTAL GANANCIA LIMPIA POR VENTA DE ARTICULOS ---------------------------------------
        self.lbl_total_limpio_artic1 = Label(self.frame_totales, text="Ganancia Artic.: ", fg="green", justify="left")
        self.lbl_total_limpio_artic1.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        self.lbl_total_limpio_artic2 = Label(self.frame_totales, textvariable=self.strvar_total_limpio_artic, width=12,
                                             justify="left")
        self.lbl_total_limpio_artic2.grid(row=0, column=7, padx=2, pady=2, sticky=E)

        # TOTAL GANANCIA LIMPIA POR SERVICIOS -------------------------------------------------
        self.lbl_total_limpio_serv1 = Label(self.frame_totales, text="Ganancia Serv.: ", fg="green", justify="left")
        self.lbl_total_limpio_serv1.grid(row=1, column=6, padx=2, pady=2, sticky=W)
        self.lbl_total_limpio_serv2 = Label(self.frame_totales, textvariable=self.strvar_total_limpio_serv, width=12,
                                            justify="left")
        self.lbl_total_limpio_serv2.grid(row=1, column=7, padx=2, pady=2, sticky=E)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_totales, text="Salir", image=self.photo3, width=45, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=10, rowspan=2, padx=3, pady=3, sticky="nsew")

        for widg in self.frame_totales.winfo_children():
            widg.grid_configure(padx=4, pady=1, sticky='nsew')

        self.frame_totales.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

    # ---------------------------------------------------------------------------------
    # GRID
    # ---------------------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_planilla.get_children():
            self.grid_planilla.delete(item)

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varPlanilla.consultar_planilla(self.filtro_activo)
        else:
            datos = self.varPlanilla.consultar_planilla("planicaja ORDER BY pl_fecha ASC")

        # acumuladores
        acum_ingresos_ventas = 0
        acum_costos_ventas = 0
        acum_egresos = 0
        acum_pagos_ctacte = 0
        acum_compras = 0
        acum_utilidad = 0
        acum_util_egre = 0
        acum_neto_articulos = 0
        acum_neto_servicios = 0

        for row in datos:

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'))

            # cargo la grilla
            self.grid_planilla.insert("", END, text=row[0], values=(forma_normal, row[2], row[3], row[4], row[5],
                                                                    round((row[4]*row[5]), 2), row[6], row[7], row[8],
                                                                    row[9], row[10], row[11], row[12], row[13], row[14],
                                                                    row[15], row[16], row[17], row[18]))

            # Sumarizo los campos de importes totales por planilla
            acum_ingresos_ventas += row[5] * row[4]
            acum_costos_ventas += row[7] * row[4]
            acum_utilidad += (row[5] * row[4]) - (row[7] * row[4])
            acum_egresos += row[6]
            acum_pagos_ctacte += row[8]
            acum_compras += row[9]
            acum_util_egre += (row[5] * row[4]) - (row[7] * row[4]) - row[6]

            if row[2] == "Venta_articulos":
                acum_neto_articulos += (row[5] * row[4]) - (row[7] * row[4])
            elif row[2] == "Venta_servicios":
                acum_neto_servicios += (row[5] * row[4]) - (row[7] * row[4])

        self.strvar_total_ingresos.set(value=str(round(acum_ingresos_ventas, 2)))
        self.strvar_total_costos.set(value=str(round(acum_costos_ventas, 2)))
        self.strvar_total_utilidad.set(value=str(round(acum_utilidad, 2)))
        self.strvar_total_egresos.set(value=str(round(acum_egresos, 2)))
        self.strvar_total_pagos.set(value=str(round(acum_pagos_ctacte, 2)))
        self.strvar_total_compras.set(value=str(round(acum_compras, 2)))
        self.strvar_total_util_menos_egr.set(value=str(round(acum_util_egre, 2)))
        self.strvar_total_limpio_artic.set(value=str(round(acum_neto_articulos, 2)))
        self.strvar_total_limpio_serv.set(value=str(round(acum_neto_servicios, 2)))

        if len(self.grid_planilla.get_children()) > 0:
            self.grid_planilla.selection_set(self.grid_planilla.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_planilla.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                        la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                        tabla 57... y asi ira cambiando para cada rg
                    text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                        asignado en la tabla"""

                buscado = self.grid_planilla.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
                "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_planilla.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_planilla.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_planilla.yview(self.grid_planilla.index(rg))
            return

        # En caso de que el parametro sea "" muevo el puntero al final del GRID
        self.mover_puntero_topend("END")

    def filtrar_grilla(self, fecha_filtrar):

        # tiene que venir en str formato(05/06/2024) por ejemplo la paso a DATE en formato dd/mm/YYYY
        paso_a_date = datetime.strptime(fecha_filtrar, "%d/%m/%Y")
        # la paso a STR formato YYYY-mm-dd - este formato es el que acepta el filtro en el CAST
        fecha1 = datetime.strftime(paso_a_date, "%Y-%m-%d")

        self.filtro_activo = "planicaja WHERE CAST(pl_fecha AS date) = CAST('" + fecha1 + "' AS date)"
        self.limpiar_Grid()
        self.llena_grilla("")

    # ---------------------------------------------------------------------------------
    # ESTADOS
    # ---------------------------------------------------------------------------------

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)

        if r == messagebox.NO:
            return

        self.reset_stringvars()
        self.estado_inicial()
        self.btn_nuevoitem.focus()

    def fReset(self):

        r = messagebox.askquestion("Reset", "Confirma -reset- operacion actual?", parent=self)
        if r == messagebox.YES:
            self.reset_stringvars()
            self.obtener_fecha_inicial()
            # coloco en la variable fecha de planilla la fecha de la ultima planilla cargada
            self.strvar_fecha_planilla.set(value=self.fecha_aux)
            self.limpiar_Grid()
            self.llena_grilla("")
            self.estado_inicial()
            self.btn_nuevoitem.focus()

    def estado_inicial(self):

        # 1 - "Entry busqueda" y botones "Buscar" y "Mostrar all" =>activos
        self.entry_buscar_movim.configure(state="normal")
        self.btn_buscar_movim.configure(state="normal")
        self.btn_mostrar_todo.configure(state="normal")

        # 2 - Botones "Nuevo" "Editar" "Eliminar" activos
        self.btn_nuevoitem.configure(state="normal")
        self.btn_editaitem.configure(state="normal")
        self.btn_borraitem.configure(state="normal")

        # 3 - Guardar  => disabled
        self.btn_guardaritem.configure(state="disabled")

        # 4 - Cancelar - Reset - Resumen del mes - TOP - END
        self.btn_Cancelar.configure(state="normal")
        self.btn_Resumen.configure(state="normal")
        self.btnToparch.configure(state="normal")
        self.btnFinarch.configure(state="normal")

        # 5 - Entrys
        self.entry_fecha_planilla.configure(state="normal")
        self.combo_tipomov.configure(state="disabled")
        self.entry_cliente.configure(state="disabled")
        self.entry_detalle_movim.configure(state="disabled")
        self.entry_ingresos.configure(state="disabled")
        self.entry_costo.configure(state="disabled")

        self.entry_egreso.configure(state="disabled")
        self.entry_pagoscta.configure(state="disabled")
        self.entry_compras.configure(state="disabled")
        self.entry_proved.configure(state="disabled")
        self.entry_ingresos.configure(state="disabled")
        self.combo_forma_pago.configure(state="disabled")
        self.entry_detalle_pago.configure(state="disabled")
        self.entry_garantia.configure(state="disabled")
        self.entry_observaciones.configure(state="disabled")

        self.btnDerecha.configure(state="normal")
        self.btnIzquierda.configure(state="normal")
        self.btn_bus_art.configure(state="disabled")
        self.btn_bus_prov.configure(state="disabled")
        self.btn_bus_cli.configure(state="disabled")

        # 0 - Activar Browse
        self.grid_planilla['selectmode'] = 'browse'
        self.grid_planilla.bind("<Double-Button-1>", self.DobleClickGrid_pla)

    def estado_boton_nuevo(self):

        #1 - Desactivo los botones Nuevo - Editar - Eliminar - Resumen mes
        self.btn_nuevoitem.configure(state="disabled")
        self.btn_editaitem.configure(state="disabled")
        self.btn_borraitem.configure(state="disabled")
        self.btn_Resumen.configure(state="disabled")

        # Habilitar boton -Guardar-
        self.btn_guardaritem.configure(state="normal")

        # Desactivar Entry buscar - Boton Buscar - boton - Mostrar all-
        self.entry_buscar_movim.configure(state="disabled")
        self.btn_buscar_movim.configure(state="disabled")
        self.btn_mostrar_todo.configure(state="disabled")

        # Activar Entrys y combos
        self.combo_tipomov.configure(state="normal")

        self.btn_bus_cli.configure(state="normal")
        self.btn_bus_art.configure(state="normal")
        self.btn_bus_prov.configure(state="normal")
        self.entry_cliente.configure(state="normal")
        self.entry_detalle_movim.configure(state="normal")
        self.entry_proved.configure(state="normal")

        # Importes - cantidades - formas de pago - garantia y observaciones
        self.entry_cantidad.configure(state="normal")
        self.entry_ingresos.configure(state="normal")
        self.entry_costo.configure(state="normal")
        self.entry_egreso.configure(state="normal")
        self.entry_pagoscta.configure(state="normal")
        self.entry_compras.configure(state="normal")
        self.entry_detalle_pago.configure(state="normal")
        self.combo_forma_pago.configure(state="normal")
        self.entry_garantia.configure(state="normal")
        self.entry_observaciones.configure(state="normal")

        self.check_ctacte.configure(state="normal")

        self.divido_tipomov()

    def divido_tipomov(self):

        self.entry_egreso.configure(state="normal")
        self.entry_compras.configure(state="normal")
        self.entry_ingresos.configure(state="normal")
        self.entry_pagoscta.configure(state="normal")
        self.entry_costo.configure(state="normal")
        self.entry_cantidad.configure(state="normal")
        self.check_ctacte.configure(onvalue=1)
        self.check_ctacte.configure(state="normal")
        self.entry_proved.configure(state="normal")
        self.entry_cliente.configure(state="normal")

        match self.combo_tipomov.get():

            case "Venta_articulos":

                """ pongo en cero todos los camos numericos por si se cambio de tipo movimiento habiendo
                cargado previamente otro tipo de movimiento """

                self.strvar_egreso.set(value="0.00")
                self.strvar_compras.set(value="0.00")
                self.strvar_proved.set(value="")
                # si es venta deshabilito : Egresos y compras
                self.entry_egreso.configure(state="disabled")
                self.entry_compras.configure(state="disabled")
                self.entry_proved.configure(state="disabled")

            case "Venta_servicios":

                """ pongo en cero todos los campos numericos por si se cambio de tipo movimiento habiendo
                cargado previamente otro tipo de movimiento """

                self.strvar_egreso.set(value="0.00")
                self.strvar_compras.set(value="0.00")
                self.strvar_proved.set(value="")
                # si es venta servicios : Egresos y compras
                self.entry_egreso.configure(state="disabled")
                self.entry_compras.configure(state="disabled")
                self.entry_proved.configure(state="disabled")

            case "Ingresos_varios":

                """ Pongo en cero todos los camos numericos por si se cambio de tipo movimiento habiendo
                # cargado previamente otro tipo de movimiento. """

                self.strvar_egreso.set(value="0.00")
                self.strvar_compras.set(value="0.00")
                self.strvar_proved.set(value="")
                # si es ingresos varios : Egresos y compras
                self.entry_egreso.configure(state="disabled")
                self.entry_compras.configure(state="disabled")
                self.entry_proved.configure(state="disabled")

            case "Pagos_ctacte":

                """ Pongo en cero todos los camos numericos por si se cambio de tipo movimiento habiendo
                cargado previamente otro tipo de movimiento """

                self.strvar_compras.set(value="0.00")
                self.strvar_proved.set(value="")
                self.strvar_totingresos.set(value="0.00")
                # si es un pago a ctacte
                self.entry_compras.configure(state="disabled")
                self.entry_proved.configure(state="disabled")

            case "Compras":

                """ Pongo en cero todos los camos numericos por si se cambio de tipo movimiento habiendo
                cargado previamente otro tipo de movimiento. """

                self.strvar_ingreso.set(value="0.00")
                self.strvar_pagos_ctacte.set(value="0.00")
                self.strvar_costo.set(value="0.00")
                self.strvar_cantidad.set(value="0.00")
                self.strvar_egreso.set(value="0.00")
                self.strvar_totingresos.set(value="0.00")
                self.check_ctacte.configure(onvalue=1)

                self.entry_ingresos.configure(state="disabled")
                self.entry_pagoscta.configure(state="disabled")
                self.entry_costo.configure(state="disabled")
                self.entry_cantidad.configure(state="disabled")
                self.entry_egreso.configure(state="disabled")
                self.check_ctacte.configure(state="disabled")
                self.btn_bus_prov.configure(state="normal")

            case "Egresos_varios":

                self.strvar_ingreso.set(value="0.00")
                self.strvar_costo.set(value="0.00")
                self.strvar_compras.set(value="0.00")
                self.strvar_cantidad.set(value="0.00")
                self.strvar_totingresos.set(value="0.00")

                self.entry_ingresos.configure(state="disabled")
                self.entry_costo.configure(state="disabled")
                self.entry_compras.configure(state="disabled")
                self.entry_cantidad.configure(state="disabled")

            case _:
                pass

    def estado_resumen(self):

        # 0 - Desactivar Browse
        self.grid_planilla['selectmode'] = 'none'
        self.grid_planilla.bind("<Double-Button-1>", self.fNo_modifique)

        # 1 - "Entry busqueda" y botones "Buscar" y "Mostrar all" =>activos
        self.entry_buscar_movim.configure(state="disabled")
        self.btn_buscar_movim.configure(state="disabled")
        self.btn_mostrar_todo.configure(state="disabled")

        # 2 - Botones "Nuevo" "Editar" "Eliminar" activos
        self.btn_nuevoitem.configure(state="disabled")
        self.btn_editaitem.configure(state="disabled")
        self.btn_borraitem.configure(state="disabled")

        # 3 - Guardar  => disabled
        self.btn_guardaritem.configure(state="disabled")

        # 4 - Cancelar - Reset - Resumen del mes - TOP - END
        self.btn_Cancelar.configure(state="disabled")
        self.btn_Resumen.configure(state="normal")
        self.btnToparch.configure(state="normal")
        self.btnFinarch.configure(state="normal")

        # 5 - Entrys
        self.entry_fecha_planilla.configure(state="normal")
        self.combo_tipomov.configure(state="disabled")
        self.entry_cliente.configure(state="disabled")
        self.entry_detalle_movim.configure(state="disabled")
        self.entry_ingresos.configure(state="disabled")
        self.entry_costo.configure(state="disabled")
        self.entry_cantidad.configure(state="disabled")

        self.entry_egreso.configure(state="disabled")
        self.entry_pagoscta.configure(state="disabled")
        self.entry_compras.configure(state="disabled")
        self.entry_proved.configure(state="disabled")
        self.entry_ingresos.configure(state="disabled")
        self.combo_forma_pago.configure(state="disabled")
        self.entry_detalle_pago.configure(state="disabled")
        self.entry_garantia.configure(state="disabled")
        self.entry_observaciones.configure(state="disabled")

        self.btnDerecha.configure(state="disabled")
        self.btnIzquierda.configure(state="disabled")
        self.btn_bus_art.configure(state="disabled")
        self.btn_bus_prov.configure(state="disabled")
        self.btn_bus_cli.configure(state="disabled")

    def fNo_modifique(self, event):
        return "break"

    def reset_stringvars(self):

        self.strvar_tipomov.set(value="")
        self.combo_tipomov.current(0)
        self.strvar_detalle_movim.set(value="")
        self.strvar_proved.set(value="")
        self.strvar_cliente.set(value="")
        self.strvar_codcli.set(value=0)
        self.strvar_forma_pago.set(value="")
        self.combo_forma_pago.current(0)
        self.strvar_detalle_pago.set(value="")
        self.strvar_garantia.set(value="")
        self.strvar_observaciones.set(value="")

        self.strvar_ingreso.set(value="0.00")
        self.strvar_costo.set(value="0.00")
        self.strvar_egreso.set(value="0.00")
        self.strvar_cantidad.set(value=1)
        self.strvar_compras.set(value="0.00")
        self.strvar_totingresos.set(value="0.00")
        self.strvar_totcosto.set(value="0.00")
        self.strvar_pagos_ctacte.set(value="0.00")

        self.strvar_check1.set(value="0")

    # ----------------------------------------------------------------------
    # CRUD
    # ----------------------------------------------------------------------

    def fNuevoItem(self):

        self.alta_modif = 1
        self.grid_planilla.bind("<Double-Button-1>", self.fNo_modifique)
        self.grid_planilla['selectmode'] = 'none'
        self.estado_boton_nuevo()
        self.entry_fecha_planilla.focus_set()

    def fEditaItem(self):

        self.alta_modif = 2

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_planilla.focus()
        # Asi obtengo la clave de la Tabla campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta)
        self.clave = self.grid_planilla.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        self.estado_boton_nuevo()

        """ Traigo los valores directamente de la Tabla, para no cargar tanto de columnas el Grid"""

        valores = self.varPlanilla.consultar_planilla("planicaja WHERE Id = " + str(self.clave))

        """ Esto ya no lo hago, traigo directamente de la tabla
        En la lista valores cargo el registro completo con todos los campos desde el Grid
        valores = self.grid_planilla.item(self.selected, 'values') """

        self.reset_stringvars()

        for row in valores:

            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[1], "%Y-%m-%d"))
            self.strvar_fecha_planilla.set(value=fecha_convertida)
            self.strvar_tipomov.set(value=row[2])
            self.strvar_detalle_movim.set(value=row[3])
            self.strvar_cantidad.set(value=row[4])
            self.strvar_ingreso.set(value=row[5])
            self.strvar_egreso.set(value=row[6])
            self.strvar_costo.set(value=row[7])
            self.strvar_pagos_ctacte.set(value=row[8])
            self.strvar_compras.set(value=row[9])
            self.strvar_cliente.set(value=row[10])
            self.strvar_codcli.set(value=row[18])
            self.strvar_forma_pago.set(value=row[11])
            self.strvar_detalle_pago.set(value=row[12])
            self.strvar_garantia.set(value=row[13])
            self.strvar_observaciones.set(value=row[14])
            self.strvar_proved.set(value=row[15])
            self.strvar_check1.set(value=row[16])
            self.strvar_clavemov_ant.set(value=row[17])

        self.estado_boton_nuevo()

        self.calcular("general")
        self.entry_cliente.focus()

    def fBorraItem(self):

        # -----------------------------------------------------------
        """ Guardo en self.selected, el Id del item del grid o treeview (I010, IB14.... """
        self.selected = self.grid_planilla.focus()
        self.selected_ant = self.grid_planilla.prev(self.selected)
        """ Guardo en self. clave, el Id del treeview de la primer columna (12 . 23 . 25.....) """
        self.clave = self.grid_planilla.item(self.selected, 'text')
        self.clave_ant = self.grid_planilla.item(self.selected_ant, 'text')
        # -----------------------------------------------------------

        if self.clave == "" or self.selected == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_planilla.item(self.selected, 'values')

        # guardo clave de movimiento anterior para control de cuenta corriente
        self.clavemov_ant = valores[17]
        # data es para mostrar el movimiento que voy a borrar

        data = str(self.clave)+" "+valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)

        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            self.clavemov_ant = 0
            return

        # Elimino de tabla planicaja y opcionalmente de cuenta corriente
        n = self.varPlanilla.eliminar_item_planilla(self.clave)
        if n == 1:
            # Elimino de tabla ctacte si existe clave de movimiento
            if int(self.clavemov_ant) > 0:
                self.varPlanilla.eliminar_item_ctacte_xmodif(self.clavemov_ant)
                messagebox.showinfo("Eliminar", "Registro eliminado EN PLANILLA Y CUENTA CORRIENTE", parent=self)
            else:
                messagebox.showinfo("Eliminar", "Registro eliminado en PLANILLA", parent=self)

            self.limpiar_Grid()
            self.llena_grilla(self.clave_ant)

        self.clavemov_ant = 0

    def fGuardar(self):

        # VALIDACIONES PREVIAS

        # FECHA
        if not self.strvar_fecha_planilla.get():
            messagebox.showerror("Error", "La fecha es requerida", parent=self)
            # paso la fecha de hoy a string y la asigno a ultima fecha porque no hay otra
            self.fecha_blanco = date.today().strftime('%d/%m/%Y')
            self.strvar_fecha_planilla.set(value=self.fecha_blanco)
            self.entry_fecha_planilla.focus()
            return

        # DETALLE
        if self.strvar_detalle_movim.get() == "":
            messagebox.showerror("Error", "Agregue un detalle", parent=self)
            self.entry_detalle_movim.focus()
            return

        # CAMPOS DE IMPORTE
        if (self.combo_tipomov.get() == "Venta_articulos" or self.combo_tipomov.get() == "Venta_servicios"
                or self.combo_tipomov.get() == "Ingresos_varios"):

            # debe haber un valor en ingreso , puede haber pagos a ctacte , no puede haber egreso ni compras
            if float(self.strvar_ingreso.get()) == 0:
                messagebox.showerror("Error", "Importe de ingreso en cero", parent=self)
                self.entry_ingresos.focus()
                return
            # debe haber una cantidad
            if float(self.strvar_cantidad.get()) == 0:
                messagebox.showerror("Error", "Coloque cantidad", parent=self)
                self.entry_cantidad.focus()
                return
            # no debe haber importe de agreso
            if float(self.strvar_egreso.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe de egreso", parent=self)
                self.entry_egreso.focus()
                return
            # no debe haber importe de compras
            if float(self.strvar_compras.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe de compras", parent=self)
                self.entry_compras.focus()
                return

        elif self.combo_tipomov.get() == "Compras":

            # Es un valor de egreso

            # SI debe haber importe de compra
            if float(self.strvar_compras.get()) == 0:
                messagebox.showerror("Error", "Importe de compras en cero", parent=self)
                self.entry_compras.focus()
                return
            # NO puede haber importe de ingreso
            if float(self.strvar_ingreso.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe en ingreso", parent=self)
                self.entry_ingresos.focus()
                return
            # NO puede haber imoprte en pagos a ctacte
            if float(self.strvar_pagos_ctacte.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe en pagos ctacte", parent=self)
                self.entry_pagoscta.focus()
                return
            # NO puede haber importe de agreso
            if float(self.strvar_egreso.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe de egreso", parent=self)
                self.entry_egreso.focus()
                return

        elif self.combo_tipomov.get() == "Egresos_varios":

            # Es un valor de egreso

            # SI debe haber importe de egreso
            if float(self.strvar_egreso.get()) == 0:
                messagebox.showerror("Error", "Importe de egresos en cero", parent=self)
                self.entry_egreso.focus()
                return
            # NO puede haber importe de ingreso
            if float(self.strvar_ingreso.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe en ingreso", parent=self)
                self.entry_ingresos.focus()
                return
            # NO puede haber importe de compra
            if float(self.strvar_compras.get()) != 0:
                messagebox.showerror("Error", "No puede haber importe en compras", parent=self)
                self.entry_compras.focus()
                return

        # ---------------------------------------------------------------------------------
        aa = 0
        #try:
        if aa == 0:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori I001, IB003
            self.selected = self.grid_planilla.focus()
            # Guardo el Id del registro de la Tabla (no es el mismo que el otro, este puedo verlo en la base)
            self.clave = self.grid_planilla.item(self.selected, 'text')

            if self.alta_modif == 1:

                # debe ser cero si es un alta de nuevo movimiento
                self.strvar_clavemov.set(value="0")
                self.movim_a_cta = 'N'

                # verifico que sea un movimiento a cuenta corriente
                if self.strvar_check1.get() == "1":
                    # Si esta marcado el check es un movim a ctacte
                    self.movim_a_cta = 'S'

                if self.strvar_pagos_ctacte.get() == "":
                    self.strvar_pagos_ctacte.set(value=0)

                if float(self.strvar_pagos_ctacte.get()) != 0:
                    # Si pagos a cta trae un importe es un movim a ctacte
                    self.movim_a_cta = 'S'

                if self.movim_a_cta == 'S':

                    # debe existir codigo de cliente y nombre para ingresar movimientos a ctacte

                    # CODIGO CLIENTE
                    if not float(self.strvar_codcli.get()):
                        messagebox.showerror("Error", "Cuenta corriente debe tener codigo cliente - "
                                                      "falta codigo", parent=self)
                        self.entry_cliente.focus()
                        return
                    # NOMBRE DE CLLIENTE
                    if not self.strvar_cliente.get():
                        messagebox.showerror("Error", "Cuenta corriente debe tener nombre cliente - "
                                                      "falta nombre", parent=self)
                        self.entry_cliente.focus()
                        return

                    # Si la cosa es correcto, genero nueva clave aleatoria
                    self.strvar_clavemov.set(value=random.randint(1, 1000000))
                # ----------------------------------------------------------------------------

                # 2- Guardar movimiento en planilla de caja
                fecha_aux = datetime.strptime(self.strvar_fecha_planilla.get(), '%d/%m/%Y')

                self.varPlanilla.insertar_planilla(fecha_aux, self.strvar_tipomov.get(),
                                self.strvar_detalle_movim.get(), self.strvar_cantidad.get(), self.strvar_ingreso.get(),
                                self.strvar_egreso.get(), self.strvar_costo.get(), self.strvar_pagos_ctacte.get(),
                                self.strvar_compras.get(), self.strvar_cliente.get(), self.strvar_forma_pago.get(),
                                self.strvar_detalle_pago.get(), self.strvar_garantia.get(),
                                self.strvar_observaciones.get(), self.strvar_proved.get(), self.strvar_check1.get(),
                                self.strvar_clavemov.get(), self.strvar_codcli.get())

                if float(self.strvar_clavemov.get()) != "0" and self.movim_a_cta == 'S':

                    # guardo movimiento en ctacte
                    self.varPlanilla.insertar_ctacte(fecha_aux, self.strvar_detalle_movim.get(),
                                (float(self.strvar_ingreso.get()) * float(self.strvar_cantidad.get())),
                                self.strvar_pagos_ctacte.get(), self.strvar_codcli.get(),
                                self.strvar_cliente.get(), self.strvar_clavemov.get())

                    messagebox.showinfo("Correcto", "Item ingresado en Planilla y Cuenta Corriente", parent=self)

                else:

                    messagebox.showinfo("Correcto", "Item ingresado en Planilla", parent=self)

            else:

                # MODIFICACION

                self.strvar_clavemov.set(value="0")
                self.movim_a_cta = 'N'

                # ojo puede ser que haya sido uno que estaba en ctacte y ahora lo sacamos "ver bien"
                if self.strvar_check1.get() == "1":
                    # Si esta marcado el check es un movim a ctacte
                    self.movim_a_cta = 'S'

                    if self.strvar_pagos_ctacte.get() == "":
                        self.strvar_pagos_ctacte.set(value=0)

                    if float(self.strvar_pagos_ctacte.get()) != 0:
                        # Si pagos a cta trae un importe es un movim a ctacte
                        self.movim_a_cta = 'S'

                    if self.movim_a_cta == 'S':

                        if self.strvar_codcli.get() == "":
                            self.strvar_codcli.set(value=0)

                        if not float(self.strvar_codcli.get()):
                            messagebox.showerror("Error", "Es necesario codigo de cliente - falta codigo",
                                                 parent=self)
                            self.entry_cliente.focus()
                            return

                        # NOMBRE DE CLLIENTE
                        if not self.strvar_cliente.get():
                            messagebox.showerror("Error", "Es necesario nombre de clientee - falta nombre",
                                                 parent=self)
                            self.entry_cliente.focus()
                            return

                    # genero nueva clave aleatoria
                    self.strvar_clavemov.set(value=random.randint(1, 1000000))

                # borrar todos los movimientos en tabla ctacte con clavemov  = strvar_clavemov_Ant
                if float(self.strvar_clavemov_ant.get()) != 0 and self.movim_a_cta == 'S':
                    self.varPlanilla.eliminar_item_ctacte_xmodif(self.strvar_clavemov_ant.get())

                # guardo modificacion con clave nueva ( cero u otra )
                self.varPlanilla.modificar_planilla(self.var_Id, self.strvar_fecha_planilla.get(),
                            self.strvar_tipomov.get(), self.strvar_detalle_movim.get(), self.strvar_cantidad.get(),
                            self.strvar_ingreso.get(), self.strvar_egreso.get(), self.strvar_costo.get(),
                            self.strvar_pagos_ctacte.get(), self.strvar_compras.get(), self.strvar_cliente.get(),
                            self.strvar_forma_pago.get(), self.strvar_detalle_pago.get(), self.strvar_garantia.get(),
                            self.strvar_observaciones.get(), self.strvar_proved.get(), self.strvar_check1.get(),
                            self.strvar_clavemov.get(), self.strvar_codcli.get())

                if float(self.strvar_clavemov.get()) != 0 and self.movim_a_cta == 'S':

                    # guardo ( como ALTA) movimiento modificado en ctacte con clave nueva
                    fecha_aux = datetime.strptime(self.strvar_fecha_planilla.get(), '%d/%m/%Y')
                    self.varPlanilla.insertar_ctacte(fecha_aux, self.strvar_detalle_movim.get(),
                            (float(self.strvar_ingreso.get())*float(self.strvar_cantidad.get())),
                            self.strvar_pagos_ctacte.get(), self.strvar_codcli.get(),
                            self.strvar_cliente.get(), self.strvar_clavemov.get())

                    messagebox.showinfo("Modificacion", "Modificacion correcta en Planilla y Cuenta Corriente",
                                        parent=self)
                else:
                    messagebox.showinfo("Modificacion", "Modificacion correcta en Planilla", parent=self)

                self.var_Id == -1

            self.movim_a_cta = 'N'
            self.limpiar_Grid()
            self.reset_stringvars()

            self.estado_inicial()

            if self.alta_modif == 1:
                ultimo_tabla_id = self.varPlanilla.traer_ultimo(0)
                self.llena_grilla(ultimo_tabla_id)
            elif self.alta_modif == 2:
                self.llena_grilla(self.clave)

            self.alta_modif = 0

            self.btn_nuevoitem.focus()

        else:
        #except:

            messagebox.showerror("Error", "Error inesperado, revise datos ingresados", parent=self)
            self.entry_fecha_planilla.focus()
            return

    # ---------------------------------------------------------------------------------
    # VARIAS
    # ---------------------------------------------------------------------------------

    def fSalir(self):
        self.master.destroy()

    def traer_dolarhoy(self):

        dev_informa = self.varPlanilla.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles. le paso la fecha
        tipo string con barras o sin barras """

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_planilla.get())

        if retorno_VerFal == "":

            self.strvar_fecha_planilla.set(value=self.strvar_fecha_error.get())
            self.entry_fecha_planilla.focus()
            return ("error")

        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.filtro_activo = (
                        "planicaja WHERE CAST(pl_fecha AS date) = CAST('" + self.strvar_fecha_planilla.get()
                        + "' AS date)")

            self.limpiar_Grid()
            self.llena_grilla("")
            self.entry_fecha_planilla.focus()

        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            #            self.strvar_fecha_planilla.set(value=estado_antes)
            self.strvar_fecha_planilla.set(value=self.strvar_fecha_error.get())
            self.entry_fecha_planilla.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_planilla.set(value=retorno_VerFal)
            # funcion que hace las transformaciones de fecha para volver a generar el filtro activo
            self.filtrar_grilla(self.strvar_fecha_planilla.get())
        return ("bien")

    def tildo_cuenta(self, cposa):

        try:
            if self.strvar_pagos_ctacte.get() == "" or self.strvar_pagos_ctacte.get() == "-" or self.strvar_pagos_ctacte.get() == ".":
                self.strvar_pagos_ctacte.set(value="0.00")

            if float(self.strvar_pagos_ctacte.get()) != 0:
                self.strvar_check1.set(value=1)
            else:
                self.strvar_check1.set(value=0)
            return
        except:
            messagebox.showerror("Error", "Revise tilde ingreso a cuenta corriente", parent=self)
            self.entry_pagoscta.focus()
            return

    def obtener_fecha_inicial(self):

        self.ultima_fecha = self.varPlanilla.traer_ultimo(1)

        if self.ultima_fecha != 0:
            # Esta funcion la pasa a formato str pero al derecho normal de 2024-12-19 a 19/12/2024 esta en funciones
            self.fecha_aux = fecha_str_reves_normal(self, self.ultima_fecha)
        else:
            # paso la fecha de hoy a string y la asigno a ultima fecha porque no hay otra
            self.fecha_aux = date.today().strftime('%d/%m/%Y')
            self.ultima_fecha = self.fecha_aux

        """ En este filtro pongo la fecha que viene de la tabla, la cual viene con el formato (YYYY-mm-dd) y las 
        instrucciones SQL que utilizo en el filtro solo aceptan la fecha con este formato """

        self.filtro_activo =  "planicaja WHERE CAST(pl_fecha AS date) = CAST('" + self.ultima_fecha + "' AS date)"

    # ---------------------------------------------------------------------------------
    # BUSQUEDAS
    # ---------------------------------------------------------------------------------

    def fBuscar_en_tabla(self):

        # busca un texto cualquiera en la tabla de planillas de caja

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.strvar_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.strvar_buscostring.get()

        self.filtro_anterior = self.filtro_activo

        self.filtro_activo = "planicaja WHERE INSTR(pl_detalle, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(pl_cliente, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(pl_proved, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(pl_tipopago, '" + se_busca + "') > 0"

        self.varPlanilla.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        # -------------------------------------------------------------------------------
        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_planilla.selection()
        self.grid_planilla.focus(item)
        # -------------------------------------------------------------------------------

    def fShowall(self):

        self.selected = self.grid_planilla.focus()
        self.clave = self.grid_planilla.item(self.selected, 'text')
        self.filtrar_grilla(self.strvar_fecha_planilla.get())
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    # ---------------------------------------------------------------------------------
    # CALCULOS
    # ---------------------------------------------------------------------------------

    def fResumen(self):

        # debo tomar mes y año para realizar el filtrado de la fecha actual
        mes_filtro = str(datetime.strptime(self.strvar_fecha_planilla.get(), "%d/%m/%Y").month)
        ano_filtro = str(datetime.strptime(self.strvar_fecha_planilla.get(), "%d/%m/%Y").year)

        self.filtro_activo =  ("planicaja WHERE MONTH(pl_fecha) = '" + mes_filtro + "' AND YEAR(pl_fecha) = '"
                               + ano_filtro + "' ORDER BY pl_fecha")

        self.limpiar_Grid()
        self.llena_grilla("")

        self.estado_resumen()

    def calcular(self, que_campo):

        try:
            # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
            if not control_forma(list(self.strvar_ingreso.get())):
                self.strvar_ingreso.set(value="0")
                self.entry_ingresos.focus()
                return
            if not control_forma(list(self.strvar_costo.get())):
                self.strvar_costo.set(value=0)
                self.entry_costo.focus()
                return
            if not control_forma(list(self.strvar_cantidad.get())):
                self.strvar_cantidad.set(value="0")
                self.entry_cantidad.focus()
                return
            if not control_forma(list(self.strvar_egreso.get())):
                self.strvar_egreso.set(value="0")
                self.entry_egreso.focus()
                return
            if not control_forma(list(self.strvar_pagos_ctacte.get())):
                self.strvar_pagos_ctacte.set(value="0")
                self.entry_pagoscta.focus()
                return
            if not control_forma(list(self.strvar_compras.get())):
                self.strvar_compras.set(value=0)
                self.entry_compras.focus()
                return

            # Valido que los campos no me ingresen en blanco ---------------------------------------------
            if self.strvar_ingreso.get() == "" or self.strvar_ingreso.get() == "-" or self.strvar_ingreso.get() == ".":
                self.strvar_ingreso.set(value="0")
                self.entry_ingresos.focus()
                return
            else:
                self.strvar_ingreso.set(value=round(float(self.strvar_ingreso.get()), 2))

            if self.strvar_costo.get() == "" or self.strvar_costo.get() == "-" or self.strvar_costo.get() == ".":
                self.strvar_costo.set(value="0")
                self.entry_costo.focus()
                return
            else:
                self.strvar_costo.set(value=round(float(self.strvar_costo.get()), 2))

            if self.strvar_cantidad.get() == "" or self.strvar_cantidad.get() == "-" or self.strvar_cantidad.get() == ".":
                self.strvar_cantidad.set(value="0")
                self.entry_cantidad.focus()
                return
            else:
                self.strvar_cantidad.set(value=round(float(self.strvar_cantidad.get()), 2))

            if self.strvar_egreso.get() == "" or self.strvar_egreso.get() == "-" or self.strvar_egreso.get() == ".":
                self.strvar_egreso.set(value=0)
                self.entry_egreso.focus()
                return
            else:
                self.strvar_egreso.set(value=round(float(self.strvar_egreso.get()), 2))

            if self.strvar_pagos_ctacte.get() == "" or self.strvar_pagos_ctacte.get() == "-" or self.strvar_pagos_ctacte.get() == ".":
                self.strvar_pagos_ctacte.set(value=0)
                self.entry_pagoscta.focus()
                return
            else:
                self.strvar_pagos_ctacte.set(value=round(float(self.strvar_pagos_ctacte.get()), 2))

            if self.strvar_compras.get() == "" or self.strvar_compras.get() == "-" or self.strvar_compras.get() == ".":
                self.strvar_compras.set(value="0")
                self.entry_compras.focus()
                return
            else:
                self.strvar_compras.set(value=round(float(self.strvar_compras.get()), 2))

            # Evaluo segun el parametro de calculo que asigno en el Entry --------------------------------
            if que_campo == "general":

                self.strvar_totingresos.set(value=round(float(self.strvar_ingreso.get()) * float(self.strvar_cantidad.get()), 2))
                self.strvar_totcosto.set(value=round(float(self.strvar_costo.get()) * float(self.strvar_cantidad.get()), 2))

        except:

            messagebox.showerror("Except-Error", "Revise entradas numericas", parent=self)
            self.entry_detalle_movim.focus()
            return

    # ---------------------------------------------------------------------------------
    # SEL
    # ---------------------------------------------------------------------------------

    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en que
        campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de 
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                                                        "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes. """

        for item in valores_new:
            self.strvar_cliente.set(value=item[15])
            self.strvar_codcli.set(value=item[1])

        self.entry_cliente.focus()
        self.entry_cliente.icursor(tk.END)

    def fBusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.strvar_detalle_movim.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.strvar_detalle_movim.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.strvar_detalle_movim.get() + "') > 0" \
                    + " OR INSTR(codbar, '" + self.strvar_detalle_movim.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.strvar_detalle_movim.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.varFuncion_new.ventana_selec("articulos", "descripcion", "marca",
                                                        "costodolar", "Descripcion", "Marca",
                                                        "Precio dolar neto", que_busco,
                                                        "Orden: Rubro+Marca+Descripcion", "S")

        masiva = 0
        masganancia = 0

        for item in valores_new:

            self.strvar_detalle_movim.set(value=item[2]) # descripcion del articulo

            costopesos_neto = round((float(self.strvar_valor_dolar_hoy.get()) * float(item[6])), 2)
            masiva = round((float(costopesos_neto) * (1 + ((float(item[7]) / 100)))), 2)
            masganancia = round((float(masiva) * (1 + ((float(item[9]) / 100)))), 2)

        self.strvar_ingreso.set(value=masganancia)
        self.strvar_costo.set(value=masiva)

        self.entry_detalle_movim.focus()
        self.entry_detalle_movim.icursor(tk.END)

        # if len(self.strvar_detalle_articulo.get()) < 3:
        #     messagebox.showwarning("Aviso", "Falta argumento de busqueda minimo tres caracteres", parent=self)
        #     self.entry_detalle_articulo.focus()
        #     return

    def fBusprov(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en
        que campos debe hacerse """

        que_busco = "proved WHERE INSTR(denominacion, '" + self.strvar_proved.get() + "') > 0" \
                    + " OR INSTR(direccion, '" + self.strvar_proved.get() + "') > 0" \
                    + " ORDER BY denominacion"

        """  Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de 
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("proved", "denominacion", "codigo",
                      "direccion", "Nombre Empresa", "Codigo", "Direccion", que_busco,
                                                        "Orden: Nombre de Proveedor", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:
            self.strvar_proved.set(value=item[2])
            #self.strvar_codcli.set(value=item[1])

        self.entry_proved.focus()
        self.entry_proved.icursor(tk.END)

    def DobleClickGrid_pla(self, event):
        self.fEditaItem()

    def fVer_blanco(self, pollo):
        self.strvar_fecha_error.set(value=self.strvar_fecha_planilla.get())

    # ---------------------------------------------------------------------------------
    # PUNTEROS
    # ---------------------------------------------------------------------------------

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_planilla.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_planilla.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_planilla.focus(rg)
            # Lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_planilla.yview(self.grid_planilla.index(self.grid_planilla.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_planilla.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_planilla.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_planilla.focus(rg)
            # lleva el foco al final del treeview
            self.grid_planilla.yview(self.grid_planilla.index(self.grid_planilla.get_children()[-1]))

    def fAntes(self):

        # Controlo que la fecha no este vacia
        if self.strvar_fecha_planilla.get() == "":
            messagebox.showerror("Error", "La fecha es requerida", parent=self)
            self.strvar_fecha_planilla.set(value=self.strvar_fecha_error.get())
            self.entry_fecha_planilla.focus()
            return

        # primero paso la fecha a formato date
        paso_a_date = datetime.strptime(self.strvar_fecha_planilla.get(), "%d/%m/%Y")
        # le resto uno con timedelta - deben estar en formato date
        resto_a_date = paso_a_date - timedelta(days=1)
        # y ahora la paso a string
        fecha1 = datetime.strftime(resto_a_date, "%Y-%m-%d")
        # asigno la fecha nuevamente al stringvar pero lo vuelvo a convertir a string
        self.strvar_fecha_planilla.set(value=resto_a_date.strftime('%d/%m/%Y'))

        self.filtro_activo =  "planicaja WHERE CAST(pl_fecha AS date) = CAST('" + fecha1 + "' AS date)"

        self.limpiar_Grid()
        self.llena_grilla("")

    def fDespues(self):

        # Controlo que la fecha no este vacia
        if self.strvar_fecha_planilla.get() == "":
            messagebox.showerror("Error", "La fecha es requerida", parent=self)
            self.strvar_fecha_planilla.set(value=self.strvar_fecha_error.get())
            self.entry_fecha_planilla.focus()
            return

        # primero paso la fecha a formato date
        paso_a_date = datetime.strptime(self.strvar_fecha_planilla.get(), "%d/%m/%Y")
        # le resto uno con timedelta - deben estar en formato date
        resto_a_date = paso_a_date + timedelta(days=1)
        # y ahora la paso a string
        fecha1 = datetime.strftime(resto_a_date, "%Y-%m-%d")
        # asigno la fecha nuevamente al stringvar pero lo vuelvo a convertir a string
        self.strvar_fecha_planilla.set(value=resto_a_date.strftime('%d/%m/%Y'))

        self.filtro_activo =  "planicaja WHERE CAST(pl_fecha AS date) = CAST('" + fecha1 + "' AS date)"

        self.limpiar_Grid()
        self.llena_grilla("")

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')









class format_numero:
    def __init__(self, numero):
        self.numero = numero

    def __str__(self):
        # return f"{self.nombre} ({self.edad} años)"
        return formatear_cifra(self.numero)

p = format_numero("235623.25")
