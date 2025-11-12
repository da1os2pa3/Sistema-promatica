from funciones import *
import os
from tkinter import *
import tkinter.font as tkFont
from datetime import datetime, date
from PIL import Image, ImageTk
from cotiz_ABM import *
from PDF_clase import *

class VentCotiz(Frame):

    # Creo una instancia de la clase definida en cotiz_ABM.py (datosCotiz)
    varCotiz = datosCotiz()

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # ------ Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # ------ Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 765
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 100
        pheight = round(htotal / 2 - hventana / 2) - 50
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.llena_grilla()
        self.llena_grilla_resuventa()

        # guarda en item el Id del elemento fila en este caso fila 0
        item = self.grid_tvw_venta_art.identify_row(0)

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        Otras funciones para manejar los elementos seleccionados incluyen:
        selection_add(): añade elementos a la selección.
        selection_remove(): remueve elementos de la selección.
        selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        selection_toggle(): cambia la selección de un elemento. """

        # Grid de auxventas --------------------------------------------------------
        self.grid_tvw_venta_art.selection_set(item)
        # pone el foco en el item seleccionado
        self.grid_tvw_venta_art.focus(item)
        # vacio tabla auxiliar de ventas
        self.habilitar_text("disabled")
        # habilitar botones
        self.habilitar_botones("disabled", "normal", "browse")


    # =====================================================================================
    # =============================== WIDGETS =============================================
    # =====================================================================================

    def create_widgets(self):

        # TITULOS -------------------------------------------------------------------------------
        # Encabezado logo y titulo con PACK
        # self.frame_titulo_top = Frame(self.master)
        #
        # # Armo el logo y el titulo
        # self.photo3 = Image.open('productos.png')
        # self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        # self.png_ventas = ImageTk.PhotoImage(self.photo3)
        # self.lbl_png_ventas = Label(self.frame_titulo_top, image=self.png_ventas, bg="red", relief=RIDGE, bd=5)
        #
        # self.lbl_titulo = Label(self.frame_titulo_top, width=76, text="Ventas",
        #                         bg="black", fg="gold", font=("Arial bold", 15, "bold"), bd=5, relief=RIDGE, padx=5)
        #
        # # Coloco logo y titulo en posicion de pantalla
        # self.lbl_png_ventas.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        # self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        # self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # --------------------------------------------------------------------------

        # VARIABLES GENERALES ----------------------------------------------------------------
        # Identifica que se esta seleccionando (cliente, articulo,....)
        self.dato_seleccion = ""
        # Se usa para saber que filtro esta activo y mantenerlo - a continuacion se setea a un valor inicial
        # Activo filtro inicial en auxventas
        self.filtro_activo = "aux_ventas ORDER BY av_desc_art ASC"
        self.filtro_activo_resuventa = "resu_ventas ORDER BY rv_fecha"
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        # self.var_Id = -1
        self.alta_modif = 0
        # Para ver si es un articulo de la tabla de articulos cargados o es libre (0 de table - 1 Libre)
        self.art_detabla = 0
        # para validar ingresos de numeros en gets numericos
        vcmd = (self.register(validar), '%P')

        self.varCotiz.vaciar_auxventas("aux_ventas")

        # ==============================================================================
        # ============================ STRINGVARS ======================================
        # ==============================================================================

        # DATOS DE LA VENTA Y DATOS CLIENTE --------------------------------------------
        self.strvar_nro_venta = tk.StringVar(value=0)
        self.strvar_fecha_venta = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value=0)
        self.strvar_nombre_cliente = tk.StringVar(value="Consumidor Final")
        self.strvar_sit_fiscal = tk.StringVar(value="")
        self.strvar_cuit = tk.StringVar(value="")

        # VALOR DEL DOLAR HOY ----------------------------------------------------------
        self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")
        self.traer_dolarhoy()

        # ARTICULO ITEM INGRESADO A AUX_VENTAS -----------------------------------------
        self.strvar_it_codigo_articulo = tk.StringVar(value="")
        self.strvar_it_descripcion_articulo = tk.StringVar(value="")
        self.strvar_it_marca_articulo = tk.StringVar(value="")
        self.strvar_it_rubro_articulo = tk.StringVar(value="")
        self.strvar_it_ultima_actual = tk.StringVar(value="")

        # TOTALES REFERIDOS A CARGA DEL ITEM DE VENTA -----------------------------------
        # cantidad a comprar
        self.strvar_cantidad_venta = tk.StringVar(value=1)

        # costo dolares neto articulo unidad
        self.strvar_unidad_costo_dolar = tk.StringVar()
        # costo dolares bruto articulo unidad
        self.strvar_unidad_costo_dolar_bruto = tk.StringVar(value="0.00")

        # costo pesos bruto articulo unidad
        self.strvar_unidad_costo_bruto_pesos = tk.StringVar(value="0.00")
        # Costo pesos NETO articulo unidad
        self.strvar_unidad_neto_pesos = tk.StringVar(value="0.00")
        # Costo pesos NETO articulo X cantidad
        self.strvar_xcanti_neto_total = tk.StringVar(value="0.00")

        # Venta pesos final articulo unidad
        self.strvar_unidad_total_precio_venta = tk.StringVar(value="0.00")
        # Venta pesos final articulo por cantidad
        self.strvar_xcanti_total_precio_venta = tk.StringVar(value="0.00")

        # Tasa del iva %
        self.strvar_combo_tasa_iva = tk.StringVar()
        # Importe iva articulo (21 o 10.5) unidad
        self.strvar_unidad_total_iva = tk.StringVar(value="0.00")
        # Importe iva articulo por la cantidad
        self.strvar_xcanti_total_iva = tk.StringVar(value="0.00")
        # Importe iva del articulo 21% (separo para guardar)
        self.strvar_unidad_total_iva_21 = tk.StringVar(value="0.00")
        # Importe iva del articulo 10,5% (separo para guardar)
        self.strvar_unidad_total_iva_105 = tk.StringVar(value="0.00")

        # Tasa Ganancia por articulo
        self.strvar_unidad_tasa_ganancia = tk.StringVar(value="0.00")
        # Importe ganancia del articulo unidad
        self.strvar_unidad_total_ganancia = tk.StringVar(value="0.00")
        # Importe ganancia del articulo X cantidad
        self.strvar_xcanti_total_ganancia = tk.StringVar(value="0.00")

        # TIPOS DE PAGO
        self.strvar_combo_formas_pago = tk.StringVar()
        self.strvar_detalle_pago = tk.StringVar(value="")

        # TOTALES FINALES GLOBALES TODA LA VENTA
        # 1 pago
        self.strvar_global_final_venta = tk.StringVar(value=0)
        self.strvar_global_final_venta_iva21 = tk.StringVar(value=0)
        self.strvar_global_final_venta_iva105 = tk.StringVar(value=0)
        self.strvar_global_final_venta_neto = tk.StringVar(value=0)

        self.strvar_buscostring = tk.StringVar(value="")


        # ========================================================================
        # ======================== TREEVIEW VENTAS ===============================
        # ========================================================================

        self.frame_tvw_todaslasventas=LabelFrame(self.master, text="", foreground="#CD5C5C")
        self.frame_todaslasventas1=LabelFrame(self.frame_tvw_todaslasventas, text="", foreground="#CD5C5C")
        self.frame_todaslasventas2=LabelFrame(self.frame_tvw_todaslasventas, text="", foreground="#CD5C5C")
        self.frame_busqueda_venta=LabelFrame(self.frame_tvw_todaslasventas, text="", border=5, foreground="black",
                                             background="light blue")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_todaslasventas2)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_todaslasventas = ttk.Treeview(self.frame_todaslasventas2, height=4, columns=("col1", "col2",
                                                                                                   "col3", "col4",
                                                                                                   "col5","col6"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        self.grid_tvw_todaslasventas.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_todaslasventas.column("col1", width=100, anchor=W, minwidth=100)
        self.grid_tvw_todaslasventas.column("col2", width=80, anchor=W, minwidth=80)
        self.grid_tvw_todaslasventas.column("col3", width=350, anchor=CENTER, minwidth=350)
        self.grid_tvw_todaslasventas.column("col4", width=100, anchor=CENTER, minwidth=100)
        self.grid_tvw_todaslasventas.column("col5", width=100, anchor=CENTER, minwidth=100)
        self.grid_tvw_todaslasventas.column("col6", width=130, anchor=CENTER, minwidth=130)

        self.grid_tvw_todaslasventas.heading("#0", text="Id", anchor=CENTER)
        self.grid_tvw_todaslasventas.heading("col1", text="Nº Venta", anchor=W)
        self.grid_tvw_todaslasventas.heading("col2", text="Fecha", anchor=W)
        self.grid_tvw_todaslasventas.heading("col3", text="Cliente", anchor=CENTER)
        self.grid_tvw_todaslasventas.heading("col4", text="Total venta", anchor=CENTER)
        self.grid_tvw_todaslasventas.heading("col5", text="Forma pago", anchor=CENTER)
        self.grid_tvw_todaslasventas.heading("col6", text="Detalle pago", anchor=CENTER)

        self.grid_tvw_todaslasventas.tag_configure('oddrow', background='light grey')
        self.grid_tvw_todaslasventas.tag_configure('evenrow', background='light blue')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_todaslasventas2, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_todaslasventas2, orient=VERTICAL)
        self.grid_tvw_todaslasventas.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_todaslasventas.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_todaslasventas.xview)
        scroll_y.config(command=self.grid_tvw_todaslasventas.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_tvw_todaslasventas['selectmode'] = 'browse'
        self.grid_tvw_todaslasventas.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)

        self.btn_nueva_venta=Button(self.frame_todaslasventas1, text="Nueva Venta", command=self.fNuevo_venta,
                                    width=12, bg='blue', fg='white')
        self.btn_nueva_venta.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.btn_edito_venta=Button(self.frame_todaslasventas1, text="Editar Venta", command=self.fEdito_venta,
                                    width=12, bg='blue', fg='white')
        self.btn_edito_venta.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.btn_borro_venta=Button(self.frame_todaslasventas1, text="Borrar Venta", command=self.fBorro_venta,
                                    width=12, bg='blue', fg='white')
        self.btn_borro_venta.grid(row=2, column=0, padx=3, pady=3, sticky=W)

        # botones para ir al tope y al fin del archivo -------------------------------------
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_todaslasventas1, text="", image=self.photo4, command=self.fToparch,
                                 bg="grey", fg="white")
        self.btnToparch.grid(row=3, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_todaslasventas1, text="", image=self.photo5, command=self.fFinarch,
                                 bg="grey", fg="white")
        self.btnFinarch.grid(row=4, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # =============================================================================
        # ======================= BUSQUEDA DE UNA VENTA ===============================
        # =============================================================================

        self.lbl_busqueda_venta = Label(self.frame_busqueda_venta, text="Texto a buscar: ", justify=LEFT, bg="light blue")
        self.lbl_busqueda_venta.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_busqueda_venta = Entry(self.frame_busqueda_venta, textvariable=self.strvar_buscostring,
                                                  state='normal', width=50, justify=LEFT, bg="light blue")
        self.entry_busqueda_venta.grid(row=0, column=1, padx=5, pady=2, sticky='nsew')

        self.btn_buscar=Button(self.frame_busqueda_venta, text="Buscar", command=self.fBuscar_resuventa, width=31,
                               bg='#5F9EA0', fg='white')
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_showall=Button(self.frame_busqueda_venta, text="Mostrar todo", command=self.fShowall, width=31,
                                bg='#5F9EA0', fg='white')
        self.btn_showall.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        self.frame_todaslasventas1.pack(side=LEFT, fill=BOTH, padx=5, pady=2)
        self.frame_todaslasventas2.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        self.frame_busqueda_venta.pack(expand=0, side=TOP, fill=BOTH, pady=2, padx=5)
        self.frame_tvw_todaslasventas.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # ========================================================================================================

        # =================================================================
        # ==================== ENCABEZADO VENTA ===========================
        # =================================================================

        # ========================================================================================================
        self.frame_cliente = LabelFrame(self.master, text="", foreground="blue")

        fff = tkFont.Font(family="Arial", size=8, weight="bold")
        www = tkFont.Font(family="Arial", size=10, weight="bold")

        # NUMERO DE VENTA
        self.strvar_nro_venta.set(value=(int(self.varCotiz.traer_ultimo()) + 1))
        self.lbl_texto_nro_venta = Label(self.frame_cliente, text="Nº venta: ", font=www, fg="red", justify=LEFT)
        self.lbl_texto_nro_venta.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_nro_venta = Label(self.frame_cliente, textvariable=self.strvar_nro_venta, font=www, fg="red", width=6)
        self.lbl_nro_venta.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        # FECHA DE VENTA
        una_fecha = date.today()
        self.strvar_fecha_venta.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.lbl_texto_fecha_venta = Label(self.frame_cliente, text="Fecha venta: ", justify=LEFT)
        self.lbl_texto_fecha_venta.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_fecha_venta = Entry(self.frame_cliente, textvariable=self.strvar_fecha_venta, width=10)
        self.entry_fecha_venta.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.entry_fecha_venta.bind("<FocusOut>", self.formato_fecha)

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_cliente, text="Cliente: ", justify=LEFT)
        self.lbl_texto_nombre_cliente.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_cliente, textvariable=self.strvar_nombre_cliente, width=52)
        self.entry_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky=W)

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_cliente, text="", image=self.photo_bus_cli, command=self.fBuscli, bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=6, padx=5, pady=2, sticky='nsew')

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = Label(self.frame_cliente, text="")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=3, pady=2, sticky=W)
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_cliente, textvariable=self.strvar_sit_fiscal, justify=LEFT, state='readonly', width=25)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky=W)

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = Label(self.frame_cliente, text="CUIT:", justify=LEFT)
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=2, pady=2, sticky=W)
        self.entry_cuit_cliente = Entry(self.frame_cliente, textvariable=self.strvar_cuit, justify=RIGHT, width=15)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=2, pady=2, sticky=W)

        self.frame_cliente.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=3)
        # ========================================================================================

        # ========================================================================================
        # ============================= PEDIDO DE ARTICULO A VENDER ==============================
        # ========================================================================================

        # ========================================================================================
        self.frame_pido_articulo = LabelFrame(self.master, text="Articulo", foreground="black")

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = Button(self.frame_pido_articulo, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=4, pady=2, sticky=E)

        # ENTRY ARTICULO
        self.lbl_detalle_movim = Label(self.frame_pido_articulo, text="Articulo: ", justify=LEFT)
        self.lbl_detalle_movim.grid(row=0, column=1, padx=4, pady=2, sticky=W)
        self.entry_detalle_movim = Entry(self.frame_pido_articulo, textvariable=self.strvar_it_descripcion_articulo,
                                         width=90, justify=LEFT)
        self.entry_detalle_movim.grid(row=0, column=2, padx=4, pady=2, sticky=E)

        # COMBO TASA IVA
        self.lbl_combo_tasa_iva = Label(self.frame_pido_articulo, justify=LEFT, foreground="black", text="IVA %")
        self.lbl_combo_tasa_iva.grid(row=0, column=3, padx=4, pady=2, sticky=W)
        self.combo_tasa_iva = ttk.Combobox(self.frame_pido_articulo, textvariable=self.strvar_combo_tasa_iva,
                                           state='readonly', width=8)
        self.combo_tasa_iva['value'] = ["21.00", "10.50"]
        self.combo_tasa_iva.current(0)
        self.combo_tasa_iva.grid(row=0, column=4, padx=4, pady=2, sticky=W)
        #     self.combo_tasa_iva.bind('<Tab>', lambda e: self.calcular("totales_por_item"))

        # COTIZACION DEL DOLAR DEL DIA
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_dolarhoy1 = Label(self.frame_pido_articulo, text="Dolar hoy:", justify=LEFT, font=fff, foreground="red")
        self.lbl_dolarhoy1.grid(row=0, column=5, padx=4, pady=2, sticky=W)
        self.lbl_dolarhoy2 = Label(self.frame_pido_articulo, textvariable=self.strvar_valor_dolar_hoy, width=10,
                                   justify=RIGHT, font=fff, foreground="red")
        self.lbl_dolarhoy2.grid(row=0, column=6, padx=4, pady=2, sticky='nsew')

        self.frame_pido_articulo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        # Precios y cantidades -------------------------------------------------------------------
        self.frame_importes_articulo = LabelFrame(self.master, text="", foreground="black")
        self.frame_importes_articulo_uno = LabelFrame(self.frame_importes_articulo)
        self.frame_importes_articulo_dos = LabelFrame(self.frame_importes_articulo)

        # PRECIO VENTA FINAL
        self.lbl_precio_venta_unidad1 = Label(self.frame_importes_articulo_uno, text="Precio Venta: ", justify=LEFT)
        self.lbl_precio_venta_unidad1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.entry_precio_venta_unidad = Entry(self.frame_importes_articulo_uno,
                                               textvariable=self.strvar_unidad_total_precio_venta, width=15,
                                               justify=RIGHT)
        self.entry_precio_venta_unidad.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')
        self.entry_precio_venta_unidad.config(validate="key", validatecommand=vcmd)
        self.entry_precio_venta_unidad.bind('<Tab>', lambda e: self.calcular("precio_venta_unidad"))

        # CANTIDAD A COMPRAR DEL ARTICULO
        self.lbl_cantidad_venta = Label(self.frame_importes_articulo_uno, justify=LEFT, text="Cantidad: ")
        self.lbl_cantidad_venta.grid(row=1, column=0, padx=3, pady=2, sticky=W)
        self.entry_cantidad_venta = Entry(self.frame_importes_articulo_uno, textvariable=self.strvar_cantidad_venta,
                                          width=8, justify=RIGHT)
        self.entry_cantidad_venta.grid(row=1, column=1, padx=3, pady=2, sticky=W)
        self.entry_cantidad_venta.config(validate="key", validatecommand=vcmd)
        self.entry_cantidad_venta.bind('<Tab>', lambda e: self.calcular("cantidad"))

        # TASA GANANCIA
        self.lbl_tasa_ganancia_unidad1 = Label(self.frame_importes_articulo_uno, text="% Ganancia : ", justify=LEFT)
        self.lbl_tasa_ganancia_unidad1.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_tasa_ganancia_unidad2 = Entry(self.frame_importes_articulo_uno,
                                                 textvariable=self.strvar_unidad_tasa_ganancia, width=10, justify=RIGHT)
        self.entry_tasa_ganancia_unidad2.grid(row=0, column=3, padx=3, pady=2, sticky='nsew')
        self.entry_tasa_ganancia_unidad2.config(validate="key", validatecommand=vcmd)
        self.entry_tasa_ganancia_unidad2.bind('<Tab>', lambda e: self.calcular("tasa_ganancia_unidad"))

        # GANANCIA
        self.lbl_ganancia_pesos_unidad1 = Label(self.frame_importes_articulo_uno, text="Ganancia : ", justify=LEFT)
        self.lbl_ganancia_pesos_unidad1.grid(row=1, column=2, padx=2, pady=2, sticky=W)
        self.entry_ganancia_pesos_unidad2 = Entry(self.frame_importes_articulo_uno,
                                                  textvariable=self.strvar_unidad_total_ganancia, width=15,
                                                  justify=RIGHT)
        self.entry_ganancia_pesos_unidad2.grid(row=1, column=3, padx=3, pady=2, sticky='nsew')
        self.entry_ganancia_pesos_unidad2.config(validate="key", validatecommand=vcmd)
        self.entry_ganancia_pesos_unidad2.bind('<Tab>', lambda e: self.calcular("importe_ganancia_unidad"))

        # COSTO PESOS BRUTO UNIDAD
        self.lbl_costo_pesos_bruto_unidad1 = Label(self.frame_importes_articulo_uno, text="Costo Bruto: ", justify=LEFT)
        self.lbl_costo_pesos_bruto_unidad1.grid(row=2, column=0, padx=2, pady=2, sticky=W)
        self.lbl_costo_pesos_bruto_unidad2 = Label(self.frame_importes_articulo_uno,
                                                   textvariable=self.strvar_unidad_costo_bruto_pesos, state='normal',
                                                   width=15, justify=RIGHT)
        self.lbl_costo_pesos_bruto_unidad2.grid(row=2, column=1, padx=3, pady=2, sticky='nsew')
        #self.entry_costo_pesos_bruto_unidad2.config(validate="key", validatecommand=vcmd)
        #self.entry_costo_pesos_bruto_unidad2.bind('<Tab>', lambda e: self.calcular("costo_pesos_bruto"))

        # COSTO DOLAR UNIDAD
        self.lbl_total_costodolar_unidad1 = Label(self.frame_importes_articulo_uno, text="Costo Dolar Bruto: ",
                                                  justify=LEFT)
        self.lbl_total_costodolar_unidad1.grid(row=2, column=2, padx=2, pady=2, sticky=W)
        self.lbl_total_costodolar_unidad2 = Label(self.frame_importes_articulo_uno,
                                                  textvariable=self.strvar_unidad_costo_dolar_bruto, width=15,
                                                  justify=RIGHT)
        self.lbl_total_costodolar_unidad2.grid(row=2, column=3, padx=3, pady=2, sticky='nsew')

        # NETO VENTA UNIDAD
        self.lbl_total_netoventa_unidad1 = Label(self.frame_importes_articulo_uno, text="Neto Venta unidad: ",
                                                 justify=LEFT)
        self.lbl_total_netoventa_unidad1.grid(row=0, column=5, padx=2, pady=2, sticky=W)
        self.lbl_total_netoventa_unidad2 = Label(self.frame_importes_articulo_uno,
                                                 textvariable=self.strvar_unidad_neto_pesos, width=15, justify=RIGHT)
        self.lbl_total_netoventa_unidad2.grid(row=0, column=6, padx=3, pady=2, sticky='nsew')

        # TOTAL IVA
        self.lbl_totaliva_unidad1 = Label(self.frame_importes_articulo_uno, text="IVA unidad: ", justify=LEFT)
        self.lbl_totaliva_unidad1.grid(row=1, column=5, padx=2, pady=2, sticky=W)
        self.lbl_totaliva_unidad2 = Label(self.frame_importes_articulo_uno, textvariable=self.strvar_unidad_total_iva,
                                          width=15, justify=RIGHT)
        self.lbl_totaliva_unidad2.grid(row=1, column=6, padx=3, pady=2, sticky='nsew')

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        # TOTAL GANANCIA X CANTIDAD
        self.lbl_ganancia_xcanti1 = Label(self.frame_importes_articulo_dos, text="Ganancia articulo: ", font=fff,
                                          fg="orange",justify=LEFT)
        self.lbl_ganancia_xcanti1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_ganancia_xcanti2 = Label(self.frame_importes_articulo_dos,
                                          textvariable=self.strvar_xcanti_total_ganancia, font=fff, fg="orange",
                                          width=15, justify=RIGHT)
        self.lbl_ganancia_xcanti2.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # TOTAL VENTA X CANTIDAD
        self.lbl_total_venta_xcanti1 = Label(self.frame_importes_articulo_dos, text="Venta articulo: ", font=fff,
                                             fg="red", justify=LEFT)
        self.lbl_total_venta_xcanti1.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.lbl_total_venta_xcanti2 = Label(self.frame_importes_articulo_dos,
                                             textvariable=self.strvar_xcanti_total_precio_venta,
                                             font = fff, fg="red", width=15, justify=RIGHT)
        self.lbl_total_venta_xcanti2.grid(row=1, column=1, padx=3, pady=2, sticky='nsew')

        self.frame_importes_articulo_uno.pack(side=LEFT, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_importes_articulo_dos.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_importes_articulo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # ===================================================================================

        ######################### FORMA DE PAGO ##########################

        # ===================================================================================
        self.frame_forma_pago = LabelFrame(self.master, text="", foreground="black")

        # forma de pago y detalle
        self.lbl_combo_formapago = Label(self.frame_forma_pago, text="Forma de Pago: ", justify=LEFT)
        self.lbl_combo_formapago.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.combo_formapago = ttk.Combobox(self.frame_forma_pago, textvariable=self.strvar_combo_formas_pago,
                                            state='readonly', width=15)
        self.combo_formapago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                         "Tarjeta Credito", "Cheque"]
        self.combo_formapago.current(0)
        self.combo_formapago.grid(row=0, column=1, padx=4, pady=2, sticky=W)

        self.lbl_deta_formapago = Label(self.frame_forma_pago, text="Detalle: ", justify=LEFT)
        self.lbl_deta_formapago.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_deta_formapago = Entry(self.frame_forma_pago, textvariable=self.strvar_detalle_pago, width=123)
        self.entry_deta_formapago.grid(row=0, column=3, padx=4, pady=2, sticky=W)

        self.frame_forma_pago.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        self.entry_fecha_venta.focus()
        # =====================================================================================

        # =====================================================================================
        # ========================== TREEVIEW ARTICULOS A VENDER ==============================
        # =====================================================================================

        # =====================================================================================
        self.frame_tvw_venta_art=LabelFrame(self.master, text="Articulos venta actual ", foreground="#CD5C5C")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_venta_art)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_venta_art = ttk.Treeview(self.frame_tvw_venta_art, height=3, columns=("col1", "col2", "col3",
                                                                                            "col4", "col5", "col6",
                                                                                            "col7", "col8", "col9",
                                                                                            "col10", "col11"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        self.grid_tvw_venta_art.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_venta_art.column("col1", width=80, anchor=W, minwidth=80)
        self.grid_tvw_venta_art.column("col2", width=430, anchor=W, minwidth=430)
        self.grid_tvw_venta_art.column("col3", width=110, anchor=CENTER, minwidth=110)
        self.grid_tvw_venta_art.column("col4", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_venta_art.column("col5", width=130, anchor=CENTER, minwidth=130)
        self.grid_tvw_venta_art.column("col6", width=70, anchor=CENTER, minwidth=70)
        self.grid_tvw_venta_art.column("col7", width=70, anchor=CENTER, minwidth=70)
        self.grid_tvw_venta_art.column("col8", width=70, anchor=CENTER, minwidth=70)
        self.grid_tvw_venta_art.column("col9", width=70, anchor=CENTER, minwidth=70)
        self.grid_tvw_venta_art.column("col10", width=70, anchor=CENTER, minwidth=70)
        self.grid_tvw_venta_art.column("col11", width=70, anchor=CENTER, minwidth=70)

        self.grid_tvw_venta_art.heading("#0", text="Id", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col1", text="Codigo", anchor=W)
        self.grid_tvw_venta_art.heading("col2", text="Descripcion", anchor=W)
        self.grid_tvw_venta_art.heading("col3", text="Marca", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col4", text="Cant", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col5", text="Precio Venta", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col6", text="Neto Venta", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col7", text="IVA 21", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col8", text="IVA 10.5", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col9", text="Ganancia", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col10", text="Costo Bruto", anchor=CENTER)
        self.grid_tvw_venta_art.heading("col11", text="Tasa IVA", anchor=CENTER)

        self.grid_tvw_venta_art.tag_configure('oddrow', background='light grey')
        self.grid_tvw_venta_art.tag_configure('evenrow', background='light blue')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_venta_art, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_venta_art, orient=VERTICAL)
        self.grid_tvw_venta_art.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_venta_art.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_venta_art.xview)
        scroll_y.config(command=self.grid_tvw_venta_art.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_tvw_venta_art['selectmode'] = 'browse'
        self.grid_tvw_venta_art.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_venta_art.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # =====================================================================================

        # =====================================================================================
        # ======================= BOTONES SOBRE TREEVIEW ARTICULOS A VENDER ===================
        # =====================================================================================

        # =====================================================================================
        self.frame_botones2 = LabelFrame(self.master)

        self.btn_ingresar_itemventa=Button(self.frame_botones2, text="Ingresar articulo a venta",
                                           command=self.fInsertar_item_venta, width=19, bg='#5F9EA0', fg='white')
        self.btn_ingresar_itemventa.grid(row=0, column=0, padx=3, pady=2, sticky=W)

        self.btn_eliminar_itemventa=Button(self.frame_botones2, text="Quitar articulo de venta",
                                           command=self.fQuitar_item_venta, width=19, bg='#5F9EA0', fg='white')
        self.btn_eliminar_itemventa.grid(row=0, column=1, padx=3, pady=2, sticky=W)

        self.btn_cerrar_venta=Button(self.frame_botones2, text="Cerrar venta actual", command=self.fCerrarVenta,
                                     width=19, bg='green', fg='white')
        self.btn_cerrar_venta.grid(row=0, column=2, padx=3, pady=2, sticky=W)

        self.btn_reset_art=Button(self.frame_botones2, text="Reset Articulo", command=self.fReset_articulo,
                                  width=19, bg='red', fg='white')
        self.btn_reset_art.grid(row=0, column=3, padx=3, pady=2, sticky=W)

        self.btn_reset_venta=Button(self.frame_botones2, text="Cancelar", command=self.fReset_venta, width=19,
                                    bg='red', fg='white')
        self.btn_reset_venta.grid(row=0, column=4, padx=3, pady=2, sticky=W)

        self.btn_imprime_venta=Button(self.frame_botones2, text="Imprime Venta", command=self.creopdf, width=19,
                                      bg='#5F9EF5', fg='white')
        self.btn_imprime_venta.grid(row=0, column=5, padx=5, pady=2, sticky=W)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_botones2, text="Salir", image=self.photo3, width=85, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=6, padx=5, pady=2, sticky="nsew")

        for widg in self.frame_botones2.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

        self.frame_botones2.pack(expand=0, side=TOP, fill=BOTH, pady=2, padx=5)
        # =============================================================================

        # =============================================================================
        # ======================== TREVIEW DE SELECCION ===============================
        # =============================================================================

        # =============================================================================
        # frame principal
        self.frame_primero=Frame(self.master)
        # frame del treeview
        self.lframe_tw_funcsel=LabelFrame(self.frame_primero, text="", border=5, foreground="black",
                                          background="light blue")
        # Frame Boton seleccionar
        self.lframe_boton_elegir=LabelFrame(self.frame_primero, text="", border=5, foreground="black",
                                            background="light blue")

        # STYLE TREEVIEW
        style = ttk.Style(self.lframe_tw_funcsel)
        # ESTA LINEA CAMBIA EL COLOR DE FONDO
        #style = ttk.Style().configure("Treeview", background="black", foreground="white", fieldbackground="black")
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white", fieldbackground="black")

        self.grid_funcsel = ttk.Treeview(self.lframe_tw_funcsel, height=4, columns=("col1", "col2", "col3", "col4", "col5"))
        self.grid_funcsel.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_funcsel.column("#0", width=40, anchor=CENTER, minwidth=40)
        self.grid_funcsel.column("col1", width=253, anchor=CENTER, minwidth=250)
        self.grid_funcsel.column("col2", width=90, anchor=CENTER, minwidth=90)
        self.grid_funcsel.column("col3", width=90, anchor=CENTER, minwidth=90)
        self.grid_funcsel.column("col4", width=90, anchor=CENTER, minwidth=90)
        self.grid_funcsel.column("col5", width=90, anchor=CENTER, minwidth=90)

        self.grid_funcsel.heading("#0", text="Id", anchor=CENTER)
        self.grid_funcsel.heading("col1", text="Dato1", anchor=CENTER)
        self.grid_funcsel.heading("col2", text="Dato2", anchor=CENTER)
        self.grid_funcsel.heading("col3", text="Dato3", anchor=CENTER)
        self.grid_funcsel.heading("col4", text="Dato4", anchor=CENTER)
        self.grid_funcsel.heading("col5", text="Dato5", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.lframe_tw_funcsel, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.lframe_tw_funcsel, orient=VERTICAL)
        self.grid_funcsel.config(xscrollcommand=scroll_x.set)
        self.grid_funcsel.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_funcsel.xview)
        scroll_y.config(command=self.grid_funcsel.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_funcsel['selectmode'] = 'browse'

        # Boton seleccionar
        self.btn_elegir_movim = Button(self.lframe_boton_elegir, text="Selec", command=self.fSelec_sel, bg="blue",
                                       fg="white", width=5)
        self.btn_reset_sel = Button(self.lframe_boton_elegir, text="Reset", command=self.limpiar_Grid_sel, bg="blue",
                                       fg="white", width=5)

        # PACKS TREEVIEW
        self.grid_funcsel.pack(side=TOP, fill=BOTH, expand=False, padx=3, pady=2)
        # PACKS FRAME DEL TREEVIEW
        self.lframe_tw_funcsel.pack(side=LEFT, fill=BOTH, expand=0, padx=1, pady=2)
        # PACKS BOTON DE SELECCIONAR
        self.btn_elegir_movim.pack(side=TOP, fill=BOTH, expand=Y, padx=3, pady=2)
        self.btn_reset_sel.pack(side=TOP, fill=BOTH, expand=Y, padx=3, pady=2)
        # PACKS FRAME DEL BOTON ELEGIR
        self.lframe_boton_elegir.pack(side=LEFT, fill=BOTH, expand=0, padx=3, pady=2)
        # PACK cuadro principal
        self.frame_primero.pack(side=TOP, fill=BOTH, expand=0, padx=3, pady=2)
        # =====================================================================================

        # =====================================================================================
        # ======================= CUADRO TOTALES VENTA ACUMULADA ==============================
        # =====================================================================================

        # =====================================================================================
        self.frame_totales_todo=LabelFrame(self.frame_primero, text="Total Venta", border=5, foreground="black",
                                           background="light blue")

        # TOTAL NETO VENTA ACUMULADO
        self.lbl_acumulado_neto_venta1 = Label(self.frame_totales_todo, text="Total Neto Venta: ", justify=LEFT,
                                               bg="light blue")
        self.lbl_acumulado_neto_venta1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_acumulado_neto_venta2 = Label(self.frame_totales_todo, textvariable=self.strvar_global_final_venta_neto,
                                                  state='normal', width=15, justify=RIGHT, bg="light blue")
        self.lbl_acumulado_neto_venta2.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # TOTAL IVA PESOS ACUMULADO
        # iva 21%
        self.lbl_acumulado_totaliva211 = Label(self.frame_totales_todo, text="Total IVA 21%: ", justify=LEFT,
                                               bg="light blue")
        self.lbl_acumulado_totaliva211.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.lbl_acumulado_totaliva212 = Label(self.frame_totales_todo, textvariable=self.strvar_global_final_venta_iva21,
                                              width=15, justify=RIGHT, bg="light blue")
        self.lbl_acumulado_totaliva212.grid(row=1, column=1, padx=3, pady=2, sticky='nsew')
        # iva 10.5%
        self.lbl_acumulado_totaliva1051 = Label(self.frame_totales_todo, text="Total IVA 10.5%: ", justify=LEFT,
                                                bg="light blue")
        self.lbl_acumulado_totaliva1051.grid(row=2, column=0, padx=2, pady=2, sticky=W)
        self.lbl_acumulado_totaliva1052 = Label(self.frame_totales_todo,
                                                textvariable=self.strvar_global_final_venta_iva105, width=15,
                                                justify=RIGHT, bg="light blue")
        self.lbl_acumulado_totaliva1052.grid(row=2, column=1, padx=3, pady=2, sticky='nsew')

        # TOTAL VENTA PESOS ACUMULADO
        self.lbl_acumulado_totalventa1 = Label(self.frame_totales_todo, text="Total Venta: ", justify=LEFT,
                                               bg="light blue")
        self.lbl_acumulado_totalventa1.grid(row=3, column=0, padx=2, pady=2, sticky=W)
        self.lbl_acumulado_totalventa2 = Label(self.frame_totales_todo, textvariable=self.strvar_global_final_venta,
                                              width=15, justify=RIGHT, bg="light blue")
        self.lbl_acumulado_totalventa2.grid(row=3, column=1, padx=3, pady=2, sticky='nsew')

        # for widg in self.frame_totales_todo.winfo_children():
        #     widg.grid_configure(padx=10, pady=3, sticky='nsew')

        self.frame_totales_todo.pack(expand=0, side=TOP, fill=BOTH, pady=2, padx=5)
        # ==================================================================================

    # ======================================================================================
    # ==================================== WIDGETS =========================================
    # ======================================================================================

    # ====================================== GRIDS =========================================
    def limpiar_Grid(self):
        # LIMPIA GRID de la venta actual

        for item in self.grid_tvw_venta_art.get_children():
            self.grid_tvw_venta_art.delete(item)

    def llena_grilla(self):
        # llena la grilla de la venta actual

        datos = self.varCotiz.consultar_articulo_item_vta(self.filtro_activo)

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_tvw_venta_art.insert("", END, tags=color, text=row[0], values=(row[1], row[2], row[3],
                                                                                 row[4], row[5],
                                                                                 row[6], row[7], row[8], row[9],
                                                                                 row[10], row[12]))
        if len(self.grid_tvw_venta_art.get_children()) > 0:
               self.grid_tvw_venta_art.selection_set(self.grid_tvw_venta_art.get_children()[0])

    def limpiar_Grid_resuventa(self):
        # limpiala grilla de las ventas historicas ya realizadas (la de mas arriba )

        for item in self.grid_tvw_todaslasventas.get_children():
            self.grid_tvw_todaslasventas.delete(item)

    def llena_grilla_resuventa(self):
        # llena la grilla de las ventas historicas ya realizadas (la de mas arriba )

        datos = self.varCotiz.consultar_articulo_item_vta(self.filtro_activo_resuventa)

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_tvw_todaslasventas.insert("", END, tags=color, text=row[0], values=(row[1], row[2], row[4],
                                                                                          row[10], row[7], row[8]))

        if len(self.grid_tvw_todaslasventas.get_children()) > 0:
               self.grid_tvw_todaslasventas.selection_set(self.grid_tvw_todaslasventas.get_children()[0])

        self.mover_puntero('END')
    # ========================================================================================

    # ================ ACTIVAR/DESACTIVAR BOTONES - lIMPIAR ENTRYS - STRINGVARS ==============
    def habilitar_botones(self, estado1, estado2, estado3):

        self.grid_tvw_todaslasventas.configure(selectmode=estado3)
        self.btn_ingresar_itemventa.configure(state=estado1)
        self.btn_eliminar_itemventa.configure(state=estado1)
        self.btn_cerrar_venta.configure(state=estado1)
        self.btn_nueva_venta.configure(state=estado2)
        self.btn_edito_venta.configure(state=estado2)
        self.btn_borro_venta.configure(state=estado2)
        self.btn_reset_art.config(state=estado1)
        self.btn_imprime_venta.configure(state=estado1)
        self.btn_bus_art.configure(state=estado1)
        self.btn_bus_cli.configure(state=estado1)
        if estado3 == "none":
            self.btnFinarch.configure(state="disabled")
            self.btnToparch.configure(state="disabled")
        else:
            self.btnFinarch.configure(state="normal")
            self.btnToparch.configure(state="normal")

    def habilitar_text(self, estado):

        self.entry_nombre_cliente.configure(state=estado)
        self.entry_detalle_movim.configure(state=estado)
        self.entry_fecha_venta.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cantidad_venta.configure(state=estado)
        self.entry_tasa_ganancia_unidad2.configure(state=estado)
        self.entry_ganancia_pesos_unidad2.configure(state=estado)
        self.entry_precio_venta_unidad.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)

    def limpiar_entrys(self, parte):

        if parte == "todo":
            # datos del cliente
            self.strvar_codigo_cliente.set(value=0)
            self.strvar_nombre_cliente.set(value="Consumidor Final")
            self.combo_sit_fiscal_cliente.current(0)
            self.strvar_cuit.set(value="")

        # datos del articulo
        self.strvar_it_codigo_articulo.set(value="")
        self.strvar_it_descripcion_articulo.set(value="")
        self.strvar_it_marca_articulo.set(value="")
        self.strvar_it_rubro_articulo.set(value="")
        self.strvar_it_ultima_actual.set(value="")
        # cantidad a comprar
        self.strvar_cantidad_venta.set(value=1)
        # costo dolares neto articulo unidad
        self.strvar_unidad_costo_dolar.set(value="0.00")
        # costo dolares bruto articulo unidad
        self.strvar_unidad_costo_dolar_bruto.set(value="0.00")
        # costo pesos bruto articulo unidad
        self.strvar_unidad_costo_bruto_pesos.set(value="0.00")
        # Costo pesos NETO articulo unidad
        self.strvar_unidad_neto_pesos.set(value="0.00")
        # Costo pesos NETO articulo X cantidad
        self.strvar_xcanti_neto_total.set(value="0.00")
        # Venta pesos final articulo unidad
        self.strvar_unidad_total_precio_venta.set(value="0.00")
        # Venta pesos final articulo por cantidad
        self.strvar_xcanti_total_precio_venta.set(value="0.00")
        # Tasa del iva %
#        self.strvar_combo_tasa_iva = tk.StringVar()
        self.combo_tasa_iva.current(0)
        # Importe iva articulo (21 o 10.5) unidad
        self.strvar_unidad_total_iva.set(value="0.00")
        # Importe iva articulo por la cantidad
        self.strvar_xcanti_total_iva.set(value="0.00")
        # Importe iva del articulo 21% (separo para guardar)
        self.strvar_unidad_total_iva_21.set(value="0.00")
        # Importe iva del articulo 10,5% (separo para guardar)
        self.strvar_unidad_total_iva_105.set(value="0.00")
        # Tasa Ganancia por articulo
        self.strvar_unidad_tasa_ganancia.set(value="0.00")
        # Importe ganancia del articulo unidad
        self.strvar_unidad_total_ganancia.set(value="0.00")
        # Importe ganancia del articulo X cantidad
        self.strvar_xcanti_total_ganancia.set(value="0.00")

#         # TOTALES FINALES GLOBALES TODA LA VENTA
#         # 1 pago
#         self.strvar_global_final_venta = tk.StringVar(value=0)
#         self.strvar_global_final_venta_iva21 = tk.StringVar(value=0)
#         self.strvar_global_final_venta_iva105 = tk.StringVar(value=0)
#         self.strvar_global_final_venta_neto = tk.StringVar(value=0)
    # ===============================================================================

    # ========================== BOTONES VENTAS =====================================

    # ===============================================================================
    def fReset_venta(self):
        # Boton CANCELAR

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.fReiniciar_todo()

    def fReiniciar_todo(self):

        # limpio los grids de auxventa y seleccion de articulo
        # self.varCotiz.vaciar_auxventas("aux_ventas")
        self. limpiar_Grid_sel()
        self. limpiar_Grid_auxventas()

        # 2 - Desactivar campos y botones
        self.habilitar_text("disabled")
        self.habilitar_botones("disabled", "normal", "browse")

        # 3 - Poner en cero totales grupales
        self.strvar_global_final_venta_neto.set(value="0.00")
        self.strvar_global_final_venta_iva21.set(value="0.00")
        self.strvar_global_final_venta_iva105.set(value="0.00")
        self.strvar_global_final_venta.set(value="0.00")

        self.limpiar_entrys("todo")

        una_fecha = date.today()
        self.strvar_fecha_venta.set(value=una_fecha.strftime('%d/%m/%Y'))

        # buscar numero de venta
        self.strvar_nro_venta.set(value=(int(self.varCotiz.traer_ultimo()) + 1))

    def fInsertar_item_venta(self):
        # Boton INSERTAR ITEM VENTA

        # Validar los items ingresados -----------------------------------------------------
        # 1- que articulo no este vacio
        if len(self.strvar_it_descripcion_articulo.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de articulo", parent=self)
            return

        if float(self.strvar_cantidad_venta.get()) == 0:
            messagebox.showerror("Error", "Falta cantidad de articulo", parent=self)
            self.entry_cantidad_venta.focus()
            return

        # INSERTO ARTICULO EN AUXILIAR DE VENTA (aux_ventas) ------------------------------
        if self.strvar_combo_tasa_iva.get() == "21.00":
            self.strvar_unidad_total_iva_21.set(value=self.strvar_unidad_total_iva.get())
        elif self.strvar_combo_tasa_iva.get() == "10.50":
            self.strvar_unidad_total_iva_105.set(value=self.strvar_unidad_total_iva.get())

        self.varCotiz.insertar_auxventa(self.strvar_it_codigo_articulo.get(),
                                        self.strvar_it_descripcion_articulo.get(),
                                        self.strvar_it_marca_articulo.get(),
                                        self.strvar_cantidad_venta.get(),
                                        self.strvar_unidad_total_precio_venta.get(),
                                        self.strvar_unidad_neto_pesos.get(),
                                        self.strvar_unidad_total_iva_21.get(),
                                        self.strvar_unidad_total_iva_105.get(),
                                        self.strvar_unidad_total_ganancia.get(),
                                        self.strvar_unidad_costo_bruto_pesos.get(),
                                        self.strvar_unidad_costo_dolar.get(),
                                        self.strvar_combo_tasa_iva.get())

        self.calcular("totalventa")

        self.limpiar_Grid()
        self.llena_grilla()

        # dejar en blanco todos los entrys del articulo
        self.limpiar_entrys("articulo")

        # poner disabled datos del cliente
        self.entry_nombre_cliente.configure(state="disabled")
        self.combo_sit_fiscal_cliente.configure(state="disabled")
        self.entry_cuit_cliente.configure(state="disabled")
        self.btn_bus_cli.configure(state="disabled")

        messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

        self.entry_detalle_movim.focus()

    def fQuitar_item_venta(self):
        # Boton QUITAR ITEM DE VENTA

        self.selected = self.grid_tvw_venta_art.focus()
        self.clave = self.grid_tvw_venta_art.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        que_paso = self.puntabla1(self.selected, "E")

        valores = self.grid_tvw_venta_art.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.YES:
            n = self.varCotiz.eliminar_auxventa(self.clave)
            if n == 1:
                messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
                self.limpiar_Grid()
                self.llena_grilla()
                que_paso = self.puntabla1(self.selected, "F")
            else:
                messagebox.showinfo("Eliminar", "No fue posible eliminar el Registro", parent=self)

        self.calcular("totalventa")

    def fCerrarVenta(self):
        # Boton CERRA VENTA

        # valido que haya items en venta
        if len(self.grid_tvw_venta_art.get_children()) <= 0:
            messagebox.showerror("Error", "No hay items en ventas", parent=self)
            return
        # velido nro venta
        if self.strvar_nro_venta.get() == 0:
            messagebox.showerror("Error", "Verifique numero de venta", parent=self)
            return
        # valido fecha venta
        if self.strvar_fecha_venta.get() == "":
            messagebox.showerror("Error", "Verifique fecha de venta", parent=self)
            return
        # # valido nombre de cliente
        # if self.strvar_nombre_cliente.get() == "":
        #     messagebox.showerror("Error", "Ingrese nombre de cliente", parent=self)
        #     return

        # borrar este numero de venta si existiera como en el caso de una modificacion en resuventas y en detaventas
        self.varCotiz.eliminar_detaventa(self.strvar_nro_venta.get())
        self.varCotiz.eliminar_resuventa2(self.strvar_nro_venta.get())

        # Inserto en deta_ventas
        datos = self.varCotiz.consultar_detalle_auxventas("aux_ventas")

        total_ventas = 0

        for row in datos:
            # inserto en tabla DETA_VENTAS
            self.varCotiz.insertar_detaventa(self.strvar_nro_venta.get(),
                                             row[1],  # codigo articulo
                                             row[2],  # desc.articulo
                                             row[3],  # marca articulo
                                             row[4],  # cantidad vendida
                                             row[5],  # final venta
                                             row[6],  # neto venta
                                             row[7],  # iva 21
                                             row[8],  # iva 10.5
                                             row[9],  # importe ganancia
                                             row[11],  # costo articulo en dolares
                                             row[10], # costo pesos bruto
                                             row[12]) # tasa iva
            total_ventas += row[4] * row[5]

        # inserto en RESU_VENTAS
        fecha_aux = datetime.strptime(self.strvar_fecha_venta.get(), '%d/%m/%Y')
        self.varCotiz.insertar_resuventa(self.strvar_nro_venta.get(), fecha_aux,
                                         self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                         self.strvar_sit_fiscal.get(), self.strvar_cuit.get(),
                                         self.strvar_combo_formas_pago.get(), self.strvar_detalle_pago.get(),
                                         self.strvar_valor_dolar_hoy.get(), total_ventas)

        messagebox.showinfo("Guardar", "Ingreso correcto detalle y resumen", parent=self)

        # refresco grid de resuventas para que se me actualie la grilla de resuventas
        self.limpiar_Grid_resuventa()
        self.llena_grilla_resuventa()

        # pongo all en blanco como si recien iniciara para que se pueda pedir una nueva venta
        self.fReiniciar_todo()

    def fNuevo_venta(self):

        self.varCotiz.vaciar_auxventas("aux_ventas")
        self.habilitar_text("normal")
        self.habilitar_botones("normal", "disabled", "none")
        # sumo uno a nueva venta
        self.strvar_nro_venta.set(value=(int(self.varCotiz.traer_ultimo()) + 1))
        self.entry_nombre_cliente.focus()

    def fEdito_venta(self):

        self.alta_modif = 2

        self.varCotiz.vaciar_auxventas("aux_ventas")

        self.habilitar_text("normal")
        self.habilitar_botones("normal", "disabled", "none")
        self.entry_detalle_movim.focus()

        # 1 - Obtener el numero de ventas_interno

        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')

        # self.limpiar_text()

        self.strvar_nro_venta.set(value=valores[0])

        # 2 - Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta

        datos_resuventa = self.varCotiz.traer_resu_venta(self.strvar_nro_venta.get())

        fechapaso = datos_resuventa[2].strftime('%d/%m/%Y')
        self.strvar_fecha_venta.set(fechapaso)
        self.strvar_codigo_cliente.set(value=datos_resuventa[3])
        self.strvar_nombre_cliente.set(value=datos_resuventa[4])
        self.strvar_sit_fiscal.set(value=datos_resuventa[5])
        self.strvar_cuit.set(value=datos_resuventa[6])
        self.strvar_combo_formas_pago.set(value=datos_resuventa[7])
        self.strvar_detalle_pago.set(value=datos_resuventa[8])

        # 3 - Cargar los itemd de venta DE DETA_VENTA

        datos_detaventa = self.varCotiz.traer_deta_venta(self.strvar_nro_venta.get())

        # # VALOR DEL DOLAR HOY
        # self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")
        # self.traer_dolarhoy()

        for row in datos_detaventa:

            # INSERTO ARTICULO EN AUXILIAR DE VENTA (aux_ventas)
            if self.strvar_combo_tasa_iva.get() == "21.00":
                self.strvar_unidad_total_iva_21.set(value=self.strvar_unidad_total_iva.get())
            elif self.strvar_combo_tasa_iva.get() == "10.50":
                self.strvar_unidad_total_iva_105.set(value=self.strvar_unidad_total_iva.get())

            self.varCotiz.insertar_auxventa(row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13])

            self.calcular("totalventa")

        self.limpiar_Grid()
        self.llena_grilla()

    def fBorro_venta(self):

        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_tvw_todaslasventas.focus()
        # guardo en clave el Id pero de la Bd (no son el mismo
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')

        que_paso = self.puntabla1(self.selected, "E")

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[0]+" " + valores[2]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar Venta?\n " + data, parent=self)
        if r == messagebox.YES:

            # Elimino de resu_vents y deta_ventas
            n = self.varCotiz.eliminar_resuventa(self.clave)
            self.varCotiz.eliminar_detaventa(valores[0])

            if n == 1:
                messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
                self.limpiar_Grid_resuventa()
                self.llena_grilla_resuventa()
            else:
                messagebox.showinfo("Eliminar", "No fue posible eliminar el Registro", parent=self)

        que_paso = self.puntabla1(self.selected, "F")

    def fReset_articulo(self):

        self.strvar_it_descripcion_articulo.set(value="")
        self.strvar_unidad_costo_bruto_pesos.set(value="0.00")
        self.strvar_unidad_total_ganancia.set(value="0.00")
        self.strvar_unidad_tasa_ganancia.set(value="0.00")
        self.strvar_unidad_total_precio_venta.set(value="0.00")
        self.strvar_unidad_neto_pesos.set(value="0.00")
        self.strvar_unidad_costo_dolar_bruto.set(value="0.00")
        self.strvar_xcanti_total_precio_venta.set(value="0.00")
        self.strvar_xcanti_total_ganancia.set(value="0.00")
        self.strvar_cantidad_venta.set(value="1")
        self.strvar_unidad_total_iva.set(value="0.00")
        self.entry_detalle_movim.focus()

    def fSalir(self):
        self.master.destroy()

    def fBuscar_resuventa(self):

        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()
            self.filtro_activo_resuventa = "resu_ventas WHERE INSTR(rv_cliente, '" + se_busca + "') ORDER BY rv_fecha ASC"

            # self.filtro_activo = "resu_ventas WHERE INSTR(rv_cliente, '" + se_busca + "') > 0" \
            #                      + " OR " + "INSTR(nombres, '" + se_busca + "') > 0" \
            #                      + " ORDER BY apellido ASC"

            self.varCotiz.buscar_entabla(self.filtro_activo)
            self.limpiar_Grid_resuventa()
            self.llena_grilla_resuventa()

            # funcion que acomoda el puntero en el TV
            que_paso = self.puntabla("", "S")

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
    # ==================================================================================


    def puntabla(self, registro, tipo_mov):

        # metodo para posicionar el puntero en el TV luego de las distintas acciones sobre los datos

        # trae el indice de la tabla "I001"
        regis = self.grid_tvw_todaslasventas.get_children()
        rg = ""
        contador = 0
        # --------------------------------------------------------------------------------

        # aca traigo el codigo del registr0 (cod.cliente, cod. art.... que estoy dando de alta porque aun no tengo ID)
        # ALTA
        if tipo_mov == "A":
            for rg in regis:
                buscado = self.grid_tvw_todaslasventas.item(rg)['values']
                # contador = contador + 1
                # busco el codigo de contrato que ingrese nuevo - Aca busco un campo de la tabla
                # a registro se le paso el nro de contrato en este caso
                if str(buscado[0]) == registro:
                    break
        # ----------------------------------------------------------------------------------------------------

        # Aca es para acomodar el puntero cuando el registro si existe en la tabla, entonces puedo usar el ID
        # MODIFICACION
        if tipo_mov == "B":
            for rg in regis:
                # En buscado guardo el Id de la tabla (base datos) del que estoy posicionado
                buscado = self.grid_tvw_todaslasventas.item(rg)['text']
                # en registro viene "clave" que es el Id del que estoy parado y lo paso a la funcion como parametro
                contador += 1
                # busco el ID de la tabla con el que guarde antes en "clave" - aca busco un Id de la tabla
                # a registro se le paso el Id de la tabla (es distinto la busqueda a ALTA)
                if buscado == registro:  # 72
                    break
        # -----------------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 1 -es la parte donde tomo el Id del registro que le sigue al que voy a eliminar
        if tipo_mov == 'E':
            control = 1
            lista = [""]
            self.buscado2 = ""
            for rg in regis:
                contador += 1
                lista.append(rg)
                if control == 0:
                    # guardo Id del que sigue
                    buscado = self.grid_tvw_todaslasventas.item(rg)['values']
                    self.buscado2 = str(buscado[0])

                    # ---------------------------------------------------------------------------------------
                    # esto agregue para que no se me mueva el puntero al posterior registro del treeview
                    xxx = len(lista) - 2
                    print(xxx)
                    x_rg = lista[xxx]

                    self.grid_tvw_todaslasventas.selection_set(x_rg)
                    self.grid_tvw_todaslasventas.focus(x_rg)
                    self.grid_tvw_todaslasventas.yview(self.grid_tvw_todaslasventas.index(x_rg))

                    if rg == "":
                        return False
                    return True
                    # -------------------------------------------------------------------------------------

                    break

                if rg == registro:  # registro seria self.selected o sea el Id de la BD
                    control = 0
        # -------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id delque obtuve antes
        # que es el que sigue al que borre
        if tipo_mov == 'F':
            for rg in regis:
                buscado = self.grid_tvw_todaslasventas.item(rg)['values']
                if self.buscado2 == str(buscado[0]):
                    break
        # ------------------------------------------------------------------------------------------

        # BUSCAR EN TABLA - Viene de la funcion que busca en la tabla lo que se requiere
        if tipo_mov == 'S':
            if regis != ():
                for rg in regis:
                    break
                if rg == "":
#                    self.btn_buscar_cliente.configure(state="disabled")
                    return
        # ----------------------------------------------------------------------------------------

        self.grid_tvw_todaslasventas.selection_set(rg)
        self.grid_tvw_todaslasventas.focus(rg)
        self.grid_tvw_todaslasventas.yview(self.grid_tvw_todaslasventas.index(rg))

        if rg == "":
            return False
        return True

    def puntabla1(self, registro, tipo_mov):

        # trae el indice de la tabla "I001"
        regis = self.grid_tvw_venta_art.get_children()
        rg = ""
        contador = 0

        # ELIMINAR REGISTRO PARTE 1 -es la parte donde tomo el Id del registro que le sigue al que voy a eliminar
        if tipo_mov == 'E':
            control = 1
            self.buscado2 = ""
            for rg in regis:
                contador += 1
                if control == 0:
                    # guardo Id del que sigue
                    buscado = self.grid_tvw_venta_art.item(rg)['values']
                    self.buscado2 = str(buscado[0])
                    break
                if rg == registro:  # registro seria self.selected o sea el Id de la BD
                    control = 0

        # ELIMINAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id delque obtuve antes
        # que es el que sigue al que borre
        if tipo_mov == 'F':
            for rg in regis:
                buscado = self.grid_tvw_venta_art.item(rg)['values']
                if self.buscado2 == str(buscado[0]):
                    break

        self.grid_tvw_venta_art.selection_set(rg)
        self.grid_tvw_venta_art.focus(rg)
        self.grid_tvw_venta_art.yview(self.grid_tvw_venta_art.index(rg))

        if rg == "":
            return False
        return True


    # ===================================================================================
    # ========================== CALCULOS  Y CONTROL DE VARIABLES =======================
    # ===================================================================================


    def calcular(self, que_campo):

        #Esta funcion solo controla todos los Entrys numericos que no contengan el valor "" o mas de un "-" o un "."
        self.control_valores()




        ii = 1

        #try:
        if ii == 1:















            if que_campo == "cantidad":
                # modifico la cantidad
                # 1 - Precio final venta por cantidad comprada
                self.strvar_xcanti_total_precio_venta.set(value=round(float(self.strvar_unidad_total_precio_venta.get()) *
                                                                      float(self.strvar_cantidad_venta.get()), 2))
                # 2 - Ganancia por cantidad
                self.strvar_xcanti_total_ganancia.set(value=round(float(self.strvar_unidad_total_ganancia.get()) *
                                                                  float(self.strvar_cantidad_venta.get()), 2))

            if que_campo == "costo_pesos_bruto":
                # controlo que no sea cero por errores en los calculos, en realidad podria serlo por si vendo
                # un articulo que me regalaron pero al menos le vamos a poner un costo de un peso

                if float(self.strvar_unidad_costo_bruto_pesos.get()) == 0:
                    messagebox.showerror('Error', 'Costo no puede ser cero', parent=self)
                    self.strvar_unidad_costo_bruto_pesos.set(value=1)
                    #self.entry_costo_pesos_bruto_unidad2.focus()
                    return

                self.calcular("precio_venta_unidad")

            if que_campo == "tasa_ganancia_unidad":
                # modifico la tasa de ganancia

                # 1 - Calculo nuevo importe de ganancia
                self.strvar_unidad_total_ganancia.set(value=round((float(self.strvar_unidad_costo_bruto_pesos.get()) *
                                                                  (float(self.strvar_unidad_tasa_ganancia.get()) / 100)), 2))
                # 2 - Calculo nuevo importe de venta
                self.strvar_unidad_total_precio_venta.set(value=round(float(self.strvar_unidad_costo_bruto_pesos.get()) +
                                                                      float(self.strvar_unidad_total_ganancia.get()), 2))

            if que_campo == "importe_ganancia_unidad":
                # modifico el importe de la ganancia

                # 1 - Calculo la nueva tasa de ganancia
                self.strvar_unidad_tasa_ganancia.set(value=round(((float(self.strvar_unidad_total_ganancia.get()) * 100) /
                                                        float(self.strvar_unidad_costo_bruto_pesos.get())), 2))
                # 2 - Calculo nuevo importe de venta
                self.strvar_unidad_total_precio_venta.set(value=round(float(self.strvar_unidad_costo_bruto_pesos.get()) +
                                                                      float(self.strvar_unidad_total_ganancia.get()), 2))
            if que_campo == "precio_venta_unidad":
                # modifico el precio de venta

                # 1 - Calculo nueva ganancia unidad
                self.strvar_unidad_total_ganancia.set(value=round(float(self.strvar_unidad_total_precio_venta.get()) -
                                                                      float(self.strvar_unidad_costo_bruto_pesos.get()), 2))
                # 2 - Calculo nueva Tasa de ganancia unidad
                self.strvar_unidad_tasa_ganancia.set(value=round(((float(self.strvar_unidad_total_ganancia.get()) /
                                                                   float(self.strvar_unidad_costo_bruto_pesos.get())) * 100), 2))
                # calculo nuevo neto unidad
                calcu_nuevo_neto = (float(self.strvar_unidad_total_precio_venta.get()) / float((1 + (float(self.strvar_combo_tasa_iva.get()) / 100))))
                self.strvar_unidad_neto_pesos.set(value=round(calcu_nuevo_neto, 2))
                # - importe del IVA unidad para el 21 o el 105... segun cual venga es lo mismo
                self.strvar_unidad_total_iva.set(value=round(float(self.strvar_unidad_neto_pesos.get()) *
                                                            (float(self.strvar_combo_tasa_iva.get()) / 100), 2))
                # - importe del IVA unidad por cantidad vendida
                #self.strvar_xcanti_total_iva.set(value=round(float(self.strvar_unidad_total_iva.get()) * float(self.strvar_cantidad_venta.get()), 2))

#            self.strvar_xcanti_total_precio_venta.set(value=round(float(self.strvar_xcanti_total_precio_venta.get())))

            # 3 - Multiplico nuevos importes por cantidad
            # - Precio final venta por cantidad comprada
            self.strvar_xcanti_total_precio_venta.set(value=round(float(self.strvar_unidad_total_precio_venta.get()) *
                                                                  float(self.strvar_cantidad_venta.get()), 2))
            # - Ganancia por cantidad
            self.strvar_xcanti_total_ganancia.set(value=round(float(self.strvar_unidad_total_ganancia.get()) *
                                                              float(self.strvar_cantidad_venta.get()), 2))

            if que_campo == "totalventa":

                datos = self.varCotiz.consultar_articulo_item_vta("aux_ventas")
                sumatot = 0
                sumaiva21 = 0
                sumaiva105 = 0
                sumanetos = 0

                for row in datos:
                    sumatot = sumatot + (row[5] * row[4])
                    sumaiva21 = sumaiva21 + (row[7] * row[4])
                    sumaiva105 = sumaiva105 + (row[8] * row[4])
                    sumanetos = sumanetos + ((row[6]) * row[4])

                self.strvar_global_final_venta.set(value=round(sumatot))
                self.strvar_global_final_venta_iva21.set(value=round(sumaiva21, 2))
                self.strvar_global_final_venta_iva105.set(value=round(sumaiva105, 2))
                self.strvar_global_final_venta_neto.set(value=float(sumanetos))

        else:
        #except:

            messagebox.showerror("Error", "Revise entradas numericas", parent=self)
            return

    def limpiar_Grid_sel(self):
        # limpio el treeview de seleccion de articulo
        for item in self.grid_funcsel.get_children():
            self.grid_funcsel.delete(item)

    def limpiar_Grid_auxventas(self):
        # limpio el treeview de auxiliar venta
        for item in self.grid_tvw_venta_art.get_children():
            self.grid_tvw_venta_art.delete(item)

    def fShowall(self):

        self.filtro_activo_resuventa = "resu_ventas ORDER BY rv_fecha"
        self.limpiar_Grid_resuventa()
        self.llena_grilla_resuventa()

    # ==================================================================================
    # =========================== FUNCION SEL ==========================================
    # ==================================================================================

    def fBuscli(self):
        self.fBusSel("cliente")

    def fBusart(self):
        self.fBusSel("articulo")

    def fBusSel(self, selparam):

        self.dato_seleccion = ""

        if selparam == "cliente":

            self.dato_seleccion = "cliente"

            if len(self.strvar_nombre_cliente.get())<=0:
                messagebox.showwarning("Alerta", "No ingreso busqueda", parent=self)
                return

            # limpio el treeview
            self.limpiar_Grid_sel()

            # Cliente a buscar
            se_busca = self.strvar_nombre_cliente.get()

            que_busco = "clientes WHERE INSTR(apellido, '" + se_busca + "') > 0" \
                            + " OR " + "INSTR(nombres, '" + se_busca + "') > 0"\
                            + " OR " + "INSTR(CONCAT(apellido,' ',nombres), '" + se_busca + "') > 0"\
                            + " ORDER BY apellido, nombres"

            retorno = self.varCotiz.buscar_entabla(que_busco)

            # cargo el treeview
            for index, reto in enumerate(retorno):
                if reto[2] == "":
                    nombre_cliente = reto[3]
                else:
                    nombre_cliente = (reto[2] + ' ' + reto[3])

                # cargo la grilla
                self.grid_funcsel.insert("", END, text=reto[0], values=(nombre_cliente, reto[1], reto[11], reto[12]))

            if len(self.grid_funcsel.get_children()) > 0:
                self.grid_funcsel.selection_set(self.grid_funcsel.get_children()[0])

        if selparam == "articulo":

            self.dato_seleccion = "articulo"

            if len(self.strvar_it_descripcion_articulo.get())<=0:
                messagebox.showwarning("Alerta", "No ingreso busqueda", parent=self)
                return

            # limpio el treeview
            self.limpiar_Grid_sel()

            # Cliente a buscar
            se_busca = self.strvar_it_descripcion_articulo.get()

            que_busco = "articulos WHERE INSTR(descripcion, '" + se_busca + "') > 0"\
                        + " OR INSTR(marca, '" + se_busca + "') > 0" \
                        + " OR INSTR(rubro, '" + se_busca + "') > 0" \
                        + " OR INSTR(codbar, '" + se_busca + "') > 0" \
                        + " OR INSTR(codigo, '" + se_busca + "') > 0"\
                        + " ORDER BY rubro, marca, descripcion"

            retorno = self.varCotiz.buscar_entabla(que_busco)

            # cargo el treeview -----------------------------------------------------------------
            # costopesos_neto = 0
            masiva = 0
            masganancia = 0
            for index, reto in enumerate(retorno):
                costopesos_neto = round((float(self.strvar_valor_dolar_hoy.get()) * float(reto[6])), 2)
                masiva = round((float(costopesos_neto) * (1 + ((float(reto[7]) / 100)))), 2)
                masganancia = round((float(masiva) * (1 + ((float(reto[9]) / 100)))), 2)

                self.grid_funcsel.insert("", END, text=reto[0], values=(reto[2], reto[4], reto[3], masganancia, masiva))

            if len(self.grid_funcsel.get_children()) > 0:
                self.grid_funcsel.selection_set(self.grid_funcsel.get_children()[0])

    def fSelec_sel(self):
        # selecciono el item desde el treeview de seleccion

        if self.dato_seleccion == "cliente":

            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_funcsel.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            self.clave = self.grid_funcsel.item(self.selected, 'text')

            if self.clave == "":
                messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
                return
            else:
                valores = self.grid_funcsel.item(self.selected, 'values')
                self.strvar_nombre_cliente.set(value=valores[0])
                self.strvar_codigo_cliente.set(value=valores[1])
                self.strvar_cuit.set(value=valores[3])
                self.strvar_sit_fiscal.set(value=valores[2])

            self.entry_detalle_movim.focus()

        if self.dato_seleccion == "articulo":

            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_funcsel.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            self.clave = self.grid_funcsel.item(self.selected, 'text')

            if self.clave == "":
                messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
                return
            else:
                # Pongo en cero los Entrys de precios.
                self.strvar_unidad_neto_pesos.set(value="0.00")
                self.strvar_unidad_costo_bruto_pesos.set(value="0.00")
                self.strvar_unidad_tasa_ganancia.set(value="0.00")
                self.strvar_unidad_total_ganancia.set(value="0.00")
                self.strvar_unidad_total_precio_venta.set(value="0.00")
                self.strvar_cantidad_venta.set(value=1)
                self.strvar_xcanti_total_ganancia.set(value="0.00")
                self.strvar_xcanti_total_precio_venta.set(value="0.00")

                # Variables para calculos
                # importe iva 21 calculado sobre el costo del articulo
                self.strvar_it_costo_iva21 = tk.StringVar(value="0.00")
                # importe iva 105 calculado sobre el costo del articulo
                self.strvar_it_costo_iva105 = tk.StringVar(value="0.00")
                # importe del costo en pesos del articulo
                self.strvar_it_costo_pesos_neto = tk.StringVar(value="0.00")

                valores = self.grid_funcsel.item(self.selected, 'values')
                self.strvar_it_descripcion_articulo.set(value=valores[0])

                # traigo el resto de los valores
                datos = self.varCotiz.consultar_articulo("articulos WHERE descripcion = '" + self.strvar_it_descripcion_articulo.get() + "'")

                for row in datos:

                    self.strvar_it_codigo_articulo.set(value=row[1])
                    self.strvar_it_marca_articulo.set(value=row[3])
                    self.strvar_it_rubro_articulo.set(value=row[4])
                    self.strvar_it_ultima_actual.set(value=row[11])
                    self.strvar_combo_tasa_iva.set(value=row[7])

                    # costo en dolares sin impuesto NETO unidad
                    self.strvar_unidad_costo_dolar.set(value=row[6])

                    # -------------------------------------------------------------------
                    # costo en pesos sin impuesto NETO unidad -
                    # (costo neto en dolares del articulo * valor dolar pesos del dia)
                    var_calculo = round(float(row[6]) * float(self.strvar_valor_dolar_hoy.get()), 2)
                    self.strvar_it_costo_pesos_neto.set(value=var_calculo)
                    # -------------------------------------------------------------------

                    # -------------------------------------------------------------------
                    # costo del artiulo en dolares mas IVA (BRUTO) para la unidad
                    var_calculo = round(float(self.strvar_unidad_costo_dolar.get()) *
                                        (1 + (float(self.strvar_combo_tasa_iva.get()) / 100)), 4)
                    self.strvar_unidad_costo_dolar_bruto.set(value=var_calculo)
                    # -------------------------------------------------------------------

                    # ------------------------------------------------------------------
                    # Calculo el IVA sobre el costo de la unidad en pesos
                    # Calculo el costo con el IVA cargado (BRUTO)
                    if row[7] == 21.00:

                        # Costo en pesos neto * TASA de IVA / 100
                        var_calculo = (float(self.strvar_it_costo_pesos_neto.get()) * (float(row[7])/100))
                        self.strvar_it_costo_iva21.set(value=var_calculo)

                        # Precio costo neto en pesos + importe del IVA
                        var_calculo = round((float(self.strvar_it_costo_pesos_neto.get()) +
                                             float(self.strvar_it_costo_iva21.get())), 2)
                        self.strvar_unidad_costo_bruto_pesos.set(value=var_calculo)

                    else:

                        # idem para el 10.5
                        var_calculo = (float(self.strvar_it_costo_pesos_neto.get()) * (float(row[7])/100))
                        self.strvar_it_costo_iva105.set(value=var_calculo)

                        # Precio costo neto en pesos + importe del IVA
                        var_calculo = round((float(self.strvar_it_costo_pesos_neto.get()) +
                                             float(self.strvar_it_costo_iva105.get())), 2)
                        self.strvar_unidad_costo_bruto_pesos.set(value=var_calculo)
                    # -----------------------------------------------------------------------

                    # -----------------------------------------------------------------------
                    # tasa de ganancia y calculo del importe de la ganancia por unidad
                    self.strvar_unidad_tasa_ganancia.set(value=row[9])
                    # importe solo de la ganancia para la unidad
                    # costo de la unidad BRUTO en pesos * TASA de ganancia / 100
                    var_calculo = round((float(self.strvar_unidad_costo_bruto_pesos.get()) * (float(row[9])/100)), 2)
                    self.strvar_unidad_total_ganancia.set(value=var_calculo)
                    # -----------------------------------------------------------------------

                    # -----------------------------------------------------------------------
                    # calculo el precio final de venta en pesos por unidad
                    # Costo bruto pesos por unidad + total importe ganancia por unidad
                    var_calculo = round(float(self.strvar_unidad_costo_bruto_pesos.get()) +
                                        float(self.strvar_unidad_total_ganancia.get()), 2)
                    self.strvar_unidad_total_precio_venta.set(value=var_calculo)
                    # -----------------------------------------------------------------------

                    # -----------------------------------------------------------------------
                    # calculo los "importes" del IVA 21 y 10,5 sobre el precio final de venta de la unidad
                    self.strvar_unidad_final_iva21 = tk.StringVar()
                    self.strvar_unidad_final_iva105 = tk.StringVar()

                    # - Calculo el Precio neto de la venta para unidad - quito IVA
                    # Precio venta final por unidad / (1+(TASA IVA / 100))
                    calcu_iva = (float(self.strvar_unidad_total_precio_venta.get()) / float((1 + (row[7] / 100))))
                    self.strvar_unidad_neto_pesos.set(value=round(calcu_iva, 2))

                    if row[7] == 21.00:

                        # importe del IVA 21% del precio final de venta en pesos unidad
                        # precio venta total por unidad - precio neto total de venta por unidad
                        var_calculo = float(self.strvar_unidad_total_precio_venta.get())-calcu_iva
                        self.strvar_unidad_final_iva21.set(value=var_calculo)

                    else:

                        # importe del IVA 10.5% del precio final de venta en pesos unidad
                        # precio venta total por unidad - precio neto total de venta por unidad
                        var_calculo = float(self.strvar_unidad_total_precio_venta.get())-calcu_iva
                        self.strvar_unidad_final_iva105.set(value=var_calculo)
                    # --------------------------------------------------------------------------

                    # --------------------------------------------------------------------------
                    # - importe del IVA unidad
                    # precio pesos neto unidad * TASA IVA / 100
                    var_calculo = round(float(self.strvar_unidad_neto_pesos.get()) *
                                        (float(self.strvar_combo_tasa_iva.get()) / 100), 2)
                    self.strvar_unidad_total_iva.set(value=var_calculo)
                    # --------------------------------------------------------------------------

                    # CALCULOS POR LA CANTIDAD -------------------------------------------------

                    # --------------------------------------------------------------------------
                    # - importe del IVA unidad por cantidad comprada
                    # importe iva de la unidad * cantidad vendida
                    var_calculo = round(float(self.strvar_unidad_total_iva.get()) * float(self.strvar_cantidad_venta.get()), 2)
                    self.strvar_xcanti_total_iva.set(value=var_calculo)
                    # --------------------------------------------------------------------------

                    # --------------------------------------------------------------------------
                    # - calculo ganancia * cantidad                     # total ganancia * cantidad
                    var_calculo = round(float(self.strvar_unidad_total_ganancia.get()) *
                                        float(self.strvar_cantidad_venta.get()), 2)
                    self.strvar_xcanti_total_ganancia.set(value=var_calculo)
                    # --------------------------------------------------------------------------

                    # --------------------------------------------------------------------------
                    # calculo precio venta * cantidad
                    # precio total venta unidad * cantidad vendida
                    var_calculo = round(float(self.strvar_unidad_total_precio_venta.get()) *
                                        float(self.strvar_cantidad_venta.get()), 2)
                    self.strvar_xcanti_total_precio_venta.set(value=var_calculo)
                    # --------------------------------------------------------------------------

                self.entry_precio_venta_unidad.focus()

    def DobleClickGrid(self, event):
        self.fSelec_sel()

    # def DobleClickGrid_pla(self, event):
    #     self.fEditaItem()


    # =====================================================================================
    # ===================== VALIDACION ENTRADAS============================================
    # =====================================================================================

    def control_valores(self):

        # Hago Control (control_forma) de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
        # Tambien todos los demas controles numericos que hacen falta

        self.strvar_unidad_total_precio_venta.set(value=control_numerico(self.strvar_unidad_total_precio_venta.get(), "0"))



        self.strvar_unidad_costo_bruto_pesos.set(value=control_numerico(self.strvar_unidad_costo_bruto_pesos.get(), "1"))
        self.strvar_cantidad_venta.set(value=control_numerico(self.strvar_cantidad_venta.get(), "1"))
        self.strvar_unidad_tasa_ganancia.set(value=control_numerico(self.strvar_unidad_tasa_ganancia.get(), "0"))

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_venta.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_venta.get())

        if retorno_VerFal == "":
            self.strvar_fecha_venta.set(value=estado_antes)
            self.entry_fecha_venta.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_venta.set(value=estado_antes)
            self.entry_fecha_venta.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_venta.set(value=retorno_VerFal)
        return ("bien")


    # ===================================================================================
    # ============================== INFORMES ==========================================
    # ===================================================================================

    def creopdf(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_tvw_venta_art.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_venta_art.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # Traer todos los registros de la tabla de articulos vendidos
        self.datos_articulos_vendidos = self.varCotiz.consultar_detalle_auxventas("aux_ventas")

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
        pdf.set_font('Times', '', 12)
        # -----------------------------------------------------------------------------------

        # armado de encabezado
        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
        self.pdf_numero_venta = self.strvar_nro_venta.get()
        self.pdf_codigo_cliente = self.strvar_codigo_cliente.get()
        self.pdf_nombre_cliente = self.strvar_nombre_cliente.get()

        #str(self.datos_articulos_vendidos[1])
        # self.pdf_nombre_cliente = datos_registro_selec[5]
        self.pdf_datos_encabezado_orden = self.pdf_numero_venta+' - '+self.pdf_nombre_cliente+' ( '+self.pdf_codigo_cliente+' )'
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Presupuesto / Nota de Venta ', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Fecha y Hora: ' + feac + '  -  Numero de Venta ' + self.pdf_datos_encabezado_orden,
                 border=1, align='C', fill=0, ln=1)
        # -----------------------------------------------------------------------

        # Espaciado entre cuerpos ------------------------------------
        pdf.cell(w=0, h=4, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Arial', '', 5)
        # retorno una lista con los registros
        # datos = self.varOrdenes.consultar_orden("")
        sumotot = 0
        for row in self.datos_articulos_vendidos:
            # Descripcion articulo
            pdf.cell(w=120, h=5, txt=row[2], border=0, align='L', fill=0, ln=0)
            # Marca
            pdf.cell(w=20, h=5, txt=row[3], border=0, align='L', fill=0, ln=0)
            # Total pesos del articulo
            pdf.cell(w=0, h=5, txt=str(row[4]), border=0, align='R', fill=0, ln=1)
            sumotot += row[4]

        # Total
        pdf.cell(w=0, h=5, txt="Total: " + str(sumotot), border=0, align='R', fill=0, ln=1)





            # mostrar = row[4]
            # cadena = (mostrar[:100])
            # pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0)










        # self.pdf_desc = str(datos_registro_selec[6])
        # self.pdf_grupo = str(datos_registro_selec[7])
        # self.pdf_acces = datos_registro_selec[8]
        # self.pdf_estado = datos_registro_selec[9]
        # self.pdf_cuenta = datos_registro_selec[10]
        # self.pdf_requerido = datos_registro_selec[11]
        # self.pdf_diagnostico = datos_registro_selec[12]
        # self.pdf_presupuesto = datos_registro_selec[13]
        # self.pdf_realizado = datos_registro_selec[14]
        # self.pdf_partes = datos_registro_selec[15]
        # self.pdf_anotaciones = datos_registro_selec[16]
        # self.pdf_totpartes = str(datos_registro_selec[17])
        # self.pdf_totmanobra = str(datos_registro_selec[18])
        # self.totalpagar = str(datos_registro_selec[17]+datos_registro_selec[18])
        #
        # cuerpo_1 = 'Equipo: '+self.pdf_desc+' - '+self.pdf_grupo
        # cuerpo_2 = 'Accesorios: '+self.pdf_acces+' - Estado del equipo: '+self.pdf_estado
        # cuerpo_3 = 'Cuentas y contraseñas: '+self.pdf_cuenta
        # cuerpo_4 = 'Requerimiento: '+self.pdf_requerido
        # cuerpo_5 = 'Diagnostico: '+self.pdf_diagnostico
        # cuerpo_6 = 'Presupuesto: '+self.pdf_presupuesto
        # cuerpo_7 = 'Trabajo realizado: '+self.pdf_realizado
        # cuerpo_8 = 'Trabajo partes reemplazadas: '+self.pdf_partes
        # cuerpo_9 = 'Trabajo anotaciones: '+self.pdf_anotaciones
        # cuerpo_10 = 'Trabajo Total partes $ : '+self.pdf_totpartes+\
        #             ' - Trabajo Total Mano de Obra $: '+self.pdf_totmanobra+' - Total a pagar $: '+self.totalpagar
        #
        # # talon cliente ----------------------------------------------
        # pdf.cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0, ln=1)
        #
        # # Espaciado entre cuerpos ------------------------------------
        # pdf.cell(w=0, h=50, txt='', align='L', fill=0, ln=1)
        #
        # # talon interno ----------------------------------------------
        # pdf.cell(w=0, h=5, txt='Orden de reparacion ' + self.pdf_datos_encabezado_orden, border=1, align='C', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_3, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_5, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_6, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_7, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_8, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_9, align='L', fill=0, ln=1)
        # pdf.cell(w=0, h=5, txt=cuerpo_10, align='L', border=1, fill=0, ln=1)
        # #pdf.cell(w=0, h=5, txt=cuerpo_11, align='L', fill=0, ln=1)






        # # -----------------------------------------------------------------------------
        # """ para crear una linea recta
        # #pdf.rect(x=50, y=80, w=70, h=95)
        # #pdf.line(20, 150, 190, 180)
        # # para crear una linea de puntos
        # #pdf.dashed_line(15, 78, 80, 90, dash_length=5, space_length=6)
        # # para crear un elipse
        # #pdf.ellipse(x=10, y=15, w=50, h=80, style='')
        # # insertar imagenes y texto
        # #pdf.text(x=60, y=50, txt='Hola muchachos')
        # #pd.image('impresora.png', x=10, y=10, w=30, h=30) #, link=url) """
        # # ----------------------------------------------------------------------------
        #
        # # -----------------------------------------------------------------------------
        # """
        # Para insertar lineas de escritura una debajo de otra
        # por ejemplo :
        # linea 1
        # linea 2
        # linea 3
        #
        # for i in range(1, 41):
        #     pdf.cell(0, 10, f'Esta es la linea {i} :D', ln=True)
        # """
        # # -------------------------------------------------------------------------------
        #
        # # --------------------------------------------------------------------------------
        # # margenes izq derecha arriba y abajo
        # """
        # Margen antes de terminar la hoja o sea en tre la ultima linea de la hoja y el fin de la hoja
        # pdf.set_auto_page_break(auto=True, margin=15)
        # """
        # # -------------------------------------------------------------------------------------
        #
        # # # para listar una base de datos forma simple basica
        # # # lista_de_datos = retorno de la base de datos
        #
        #
        # # # al ultimo le ponemos w=0 y abarca todo el resto del renglon hasta el final
        # # pdf.cell(w=30, h=8, txt='Codigo', border=1, align='C', fill=0)
        # # pdf.cell(w=25, h=8, txt='Rubro', border=1, align='C', fill=0)
        # # pdf.cell(w=20, h=8, txt='Marca', border=1, align='C', fill=0)
        # # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)
        #
        # # pdf.set_font('Arial', '', 5)
        # # # retorno una lista con los registros
        # # datos = self.varOrdenes.consultar_orden("")
        # # for row in datos:
        # #     pdf.cell(w=30, h=5, txt=row[1], border=1, align='C', fill=0)
        # #     pdf.cell(w=25, h=5, txt=row[2], border=1, align='C', fill=0)
        # #     pdf.cell(w=20, h=5, txt=row[3], border=1, align='C', fill=0)
        # #     mostrar = row[4]
        # #     cadena = (mostrar[:100])
        # #     pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0)
        # #

        pdf.output('hoja.pdf')

        # # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    # ===============================================================================
    # =========================== VARIAS ============================================
    # ===============================================================================

    def traer_dolarhoy(self):
        dev_informa = self.varCotiz.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])

    def fToparch(self):
        self.mover_puntero('TOP')

    def fFinarch(self):
        self.mover_puntero('END')

    def mover_puntero(self, param_topend):

        # PARA IR A TOPE O FIN DE ARCHIVO

        if param_topend == "":
            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...) ----------------------
            self.selected = self.grid_tvw_todaslasventas.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')

        # Si es tope de archivo ----------------------------------------------------------------------
        if param_topend == 'TOP':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_tvw_todaslasventas.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return

            # selecciono el Id primero de la lista en este caso
            self.grid_tvw_todaslasventas.selection_set(rg)
            # pone el primero Id
            self.grid_tvw_todaslasventas.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_tvw_todaslasventas.yview(self.grid_tvw_todaslasventas.index(self.grid_tvw_todaslasventas.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_tvw_todaslasventas.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_tvw_todaslasventas.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_tvw_todaslasventas.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_tvw_todaslasventas.yview(self.grid_tvw_todaslasventas.index(self.grid_tvw_todaslasventas.get_children()[-1]))
