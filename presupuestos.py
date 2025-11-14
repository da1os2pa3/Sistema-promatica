from funciones import *
from funcion_new import *
from presupuestos_ABM import *
from articulos import *
#--------------------------------------
#from tkinter import *
#from tkinter import ttk
from tkinter import messagebox
#import tkinter as tk
import tkinter.font as tkFont
from tkinter.scrolledtext import *     # para campos text
#--------------------------------------
import os
from PDF_clase import *
from PIL import Image, ImageTk
from datetime import date, datetime
# -------------------------------------

class clase_presupuestos(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ---------------------------------------------------------------------------------
        # Instanciaciones
        self.varPresupuestos = datosPresupuestos(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # PANTALLA
        # ----------------------------------------------------------------------------------

        # Esto esta agregado para centrar las ventanas en la pantalla
        # master.geometry("880x510")
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega mas widgets).Esto 
        actualiza el ancho y alto de la ventana en caso de crecer. """

        #Obtenemos el ancho y alto de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Asiganamos medidas a la ventana
        wventana = 1035
        hventana = 700
        # Formula para calcular el centro, si le sumos valores puedo correrla a partir del centro
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()

        # ------------------------------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno.
        Otras funciones para manejar los elementos seleccionados incluyen:
        1 - selection_add(): añade elementos a la selección.
        2 - selection_remove(): remueve elementos de la selección.
        3 - selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        4 - selection_toggle(): cambia la selección de un elemento. """

        # ----------------------------------------------------------------------
        # ESTADO INICIAL
        # ----------------------------------------------------------------------

        # # guarda en item el Id del elemento fila en este caso fila 0 del grid principal
        # item = self.grid_tvw_resupresup.identify_row(0)
        # # Grid de auxpresup
        # self.grid_tvw_resupresup.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_tvw_resupresup.focus(item)

        # Obtengo el numero del presupuesto siguiente al ultimo cargado
        self.strvar_nro_presup.set(value=(int(self.varPresupuestos.traer_ultimo(1)) + 1))

        """ Seteos iniciales: self.limpiar_entrys_total()-
        self.strvar_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))-self.estado_entrys_inicial("disabled")-
        self.estado_botones_dos("disabled")-self.estado_botones_uno("normal")-
        self.varPresupuestos.vaciar_auxpresup("aux_presup")-self.limpiar_Grid_auxiliar()-self.alta_modif_aux = 0
        self.alta_modif_presup = 0-self.grid_tvw_resupresup['selectmode'] = 'browse'-
        self.grid_tvw_resupresup.bind("<Double-Button-1>", self.DobleClickGrid) """

        self.estado_inicial()

        # Designo un orden antes de llenar la grilla
        self.filtro_activo_resu_presup = "resu_presup ORDER BY rp_fecha, rp_numero ASC"

        self.llena_grilla_resu_presup("")
        # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # WIDGETS
    # ----------------------------------------------------------------------

    def create_widgets(self):

        # ----------------------------------------------------------------------
        #  TITULOS
        # ----------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        # self.frame_titulo_top = Frame(self.master)
        # # Armo el logo y el titulo
        # self.photo3 = Image.open('productos.png')
        # self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        # self.png_ventas = ImageTk.PhotoImage(self.photo3)
        # self.lbl_png_ventas = Label(self.frame_titulo_top, image=self.png_ventas, bg="red", relief=RIDGE, bd=5)
        # self.lbl_titulo = Label(self.frame_titulo_top, width=76, text="Ventas",
        #                         bg="black", fg="gold", font=("Arial bold", 15, "bold"), bd=5, relief=RIDGE, padx=5)
        # # Coloco logo y titulo en posicion de pantalla
        # self.lbl_png_ventas.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        # self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        # self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # STRINGVARS
        # ----------------------------------------------------------------------

        # DATOS DE LA VENTA Y DATOS CLIENTE
        self.strvar_nro_presup = tk.StringVar(value="0")
        self.strvar_fecha_presup = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_nombre_cliente = tk.StringVar(value="Consumidor Final")
        self.strvar_sit_fiscal = tk.StringVar(value="")
        self.strvar_cuit = tk.StringVar(value="")

        # VALOR DEL DOLAR HOY
        self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")
        self.traer_dolarhoy()

        # ARTICULO ITEM INGRESADO A AUX_VENTAS
        self.strvar_componente = tk.StringVar(value="")
        self.strvar_combo_tasa_iva = tk.StringVar()
        self.strvar_cantidad_vendida = tk.StringVar(value="1")
        self.strvar_tasa_ganancia = tk.StringVar(value="0.00")
        self.strvar_proveedor = tk.StringVar(value="")
        self.strvar_codigo_componente = tk.StringVar(value="")

        # VALORES
        self.strvar_neto_dolar = tk.StringVar(value="0.00")

        self.strvar_costo_neto_pesos_unidad = tk.StringVar(value="0.00")
        self.strvar_costo_neto_pesos_xcanti = tk.StringVar(value="0.00")

        self.strvar_costo_bruto_pesos_unidad = tk.StringVar(value="0.00")
        self.strvar_costo_bruto_pesos_xcanti = tk.StringVar(value="0.00")

        self.strvar_importe_iva_unidad = tk.StringVar(value="0.00")
        self.strvar_importe_iva_xcanti = tk.StringVar(value="0.00")

        self.strvar_importe_ganancia_unidad = tk.StringVar(value="0.00")
        self.strvar_importe_ganancia_xcanti = tk.StringVar(value="0.00")

        self.strvar_precio_final_unidad = tk.StringVar(value="0.00")
        self.strvar_precio_final_xcanti = tk.StringVar(value="0.00")

        # sumatoria de todos los componentes
        self.strvar_total_presupuesto = tk.StringVar(value="0.00")
        self.strvar_total_item_redondo = tk.StringVar(value="0.00")
        self.strvar_total_ganancia = tk.StringVar(value="0.00")
        self.strvar_total_costos = tk.StringVar(value="0.00")
        self.strvar_total_presup_redondo = tk.StringVar(value="0.00")

        # TIPOS DE PAGO
        self.strvar_combo_formas_pago = tk.StringVar()
        self.strvar_detalle_pago = tk.StringVar(value="")

        self.strvar_buscostring = tk.StringVar(value="")
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------------------------

        # Identifica que se esta seleccionando (cliente, articulo,....)
        self.dato_seleccion = ""
        # Activo filtro inicial en resu_presup
        self.filtro_activo_resu_presup = "resu_presup ORDER BY rp_fecha, rp_numero ASC"
        self.filtro_activo_auxiliar = "aux_presup"
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        # self.var_Id = -1
        self.alta_modif_aux = 0         # tabla aux_presu
        self.alta_modif_presup = 0      # tabla resu_presu
        # para validar ingresos de numeros en gets numericos
        vcmd = (self.register(validar), '%P')
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # PREPARO TABLA AUXILIAR

        # Vacio la tabla auxiliar de componentes aux_presup
        self.varPresupuestos.vaciar_auxpresup("aux_presup")
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # GRID RESUMEN DE PRESUPUESTOS
        # ----------------------------------------------------------------------

        self.frame_grid_botones=LabelFrame(self.master, text="", foreground="#CD5C5C")

        self.frame_resupresup_dos=LabelFrame(self.frame_grid_botones, text="Presupuesto entregados", foreground="#CD5C5C")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_resupresup_dos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_resupresup = ttk.Treeview(self.frame_resupresup_dos, height=4, columns=("col1", "col2", "col3",
                                                                       "col4", "col5","col6", "col7", "col8", "col9"))

        self.grid_tvw_resupresup.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_tvw_resupresup.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_resupresup.column("col1", width=100, anchor=W, minwidth=100)
        self.grid_tvw_resupresup.column("col2", width=80, anchor=W, minwidth=80)
        self.grid_tvw_resupresup.column("col3", width=350, anchor=CENTER, minwidth=350)
        self.grid_tvw_resupresup.column("col4", width=100, anchor=CENTER, minwidth=100)
        self.grid_tvw_resupresup.column("col5", width=100, anchor=CENTER, minwidth=100)
        self.grid_tvw_resupresup.column("col6", width=130, anchor=CENTER, minwidth=130)
        self.grid_tvw_resupresup.column("col7", width=130, anchor=CENTER, minwidth=130)
        self.grid_tvw_resupresup.column("col8", width=130, anchor=CENTER, minwidth=130)
        self.grid_tvw_resupresup.column("col9", width=130, anchor=CENTER, minwidth=130)

        self.grid_tvw_resupresup.heading("#0", text="Id", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col1", text="Nº Venta", anchor=W)
        self.grid_tvw_resupresup.heading("col2", text="Fecha", anchor=W)
        self.grid_tvw_resupresup.heading("col3", text="Cliente", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col4", text="Dolar", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col5", text="% Ganancia", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col6", text="Total venta", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col7", text="Redondeo", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col8", text="Forma pago", anchor=CENTER)
        self.grid_tvw_resupresup.heading("col9", text="Detalle pago", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_resupresup_dos, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_resupresup_dos, orient=VERTICAL)
        self.grid_tvw_resupresup.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_resupresup.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_resupresup.xview)
        scroll_y.config(command=self.grid_tvw_resupresup.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_tvw_resupresup['selectmode'] = 'browse'
        self.grid_tvw_resupresup.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # BOTONES
        # ----------------------------------------------------------------------

        # Botones Nuevo-Edito-Borro-Guardar-Guardar como-Cancelar
        self.frame_resupresup_uno=LabelFrame(self.frame_grid_botones, text="", foreground="#CD5C5C")

        # cuadro 1 ------------------------------------------------------------
        self.frame_cuadro1 = LabelFrame(self.frame_resupresup_uno, text="")

        # botones CRUD
        self.btn_nuevo_presup=Button(self.frame_cuadro1, text="Nuevo Presupuesto",
                                    command=self.fNuevo_presupuesto, width=17, bg='blue', fg='white')
        self.btn_nuevo_presup.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.btn_edito_presup=Button(self.frame_cuadro1, text="Editar Presupuesto",
                                    command=self.fEdito_presupuesto, width=17, bg='blue', fg='white')
        self.btn_edito_presup.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.btn_borro_presup=Button(self.frame_cuadro1, text="Borrar Presupuesto",
                                    command=self.fBorro_presupuesto, width=17, bg='red', fg='white')
        self.btn_borro_presup.grid(row=2, column=0, padx=3, pady=3, sticky=W)

        self.frame_cuadro1.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # cuadro 2
        self.frame_cuadro2 = LabelFrame(self.frame_resupresup_uno, text="")

        self.btn_cerrar_presupuesto=Button(self.frame_cuadro2, text="Cerrar/Guardar\npresupuesto",
                                           command=self.fGuardar, width=17, bg='green', fg='white')
        self.btn_cerrar_presupuesto.grid(row=3, column=0, padx=3, pady=3, sticky=W)
        self.btn_guardar_como=Button(self.frame_cuadro2, text="Guardar como...",
                                           command=self.fGuardar_como, width=17, bg='light green', fg='black')
        self.btn_guardar_como.grid(row=4, column=0, padx=3, pady=3, sticky=W)
        self.btn_cancelar_presupuesto=Button(self.frame_cuadro2, text="Cancelar", command=self.fCancela_presup,
                                             width=17, bg='black', fg='white')
        self.btn_cancelar_presupuesto.grid(row=5, column=0, padx=3, pady=3, sticky=W)

        self.frame_cuadro2.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # cuadro 3
        self.frame_cuadro3 = LabelFrame(self.frame_resupresup_uno, text="")

        # Botones +componente -com ponente Ingresar componente al presupuesto
        self.btn_mas_componente=Button(self.frame_cuadro3, text="+ Componente", command=self.fMas_componente,
                                       width=17, bg='blue', fg='white')
        self.btn_mas_componente.grid(row=6, column=0, padx=3, pady=3, sticky=W)
        self.btn_menos_componente=Button(self.frame_cuadro3, text="- Componente", command=self.fMenos_componente,
                                         width=17, bg='blue', fg='white')
        self.btn_menos_componente.grid(row=7, column=0, padx=3, pady=3, sticky=W)
        self.btn_editar_componente=Button(self.frame_cuadro3, text="Editar componente",
                                           command=self.fEditar_item_auxpresup, width=17, bg='blue', fg='white')
        self.btn_editar_componente.grid(row=8, column=0, padx=3, pady=3, sticky=W)
        self.btn_ingresar_componente=Button(self.frame_cuadro3, text="Ingresar componente\nal presupuesto",
                                           command=self.fInsertar_item_auxpresup, width=17, bg='light green',
                                            fg='black')
        self.btn_ingresar_componente.grid(row=9, column=0, padx=3, pady=3, sticky=W)
        self.btn_reset_componente=Button(self.frame_cuadro3, text="Suspender ingreso\nde componente",
                                         command=self.fReset_articulo, width=17, bg='black', fg='white')
        self.btn_reset_componente.grid(row=10, column=0, padx=2, pady=2, sticky=W)

        self.frame_cuadro3.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # cuadro 4
        self.frame_cuadro4 = LabelFrame(self.frame_resupresup_uno, text="")

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_cuadro4, text="Salir", image=self.photo3, width=120, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=11, column=0, padx=3, pady=3, sticky = 'nsew')

        self.frame_cuadro4.pack(side=TOP, fill=BOTH, expand = 1, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # BUSCAR UN PRESUPUESTO
        # ----------------------------------------------------------------------

        self.frame_busqueda_resupresup=LabelFrame(self.frame_grid_botones, text="", border=5, foreground="black",
                                                  background="light blue")
        self.lbl_busqueda_presup = Label(self.frame_busqueda_resupresup, text="Buscar cliente en presupuesto: ",
                                         justify=LEFT, bg="light blue")
        self.lbl_busqueda_presup.grid(row=0, column=0, padx=3, pady=2, sticky=W)
        self.entry_busqueda_presup = Entry(self.frame_busqueda_resupresup, textvariable=self.strvar_buscostring,
                                                  state='normal', width=23, justify=LEFT)
        self.entry_busqueda_presup.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')
        self.btn_buscar=Button(self.frame_busqueda_resupresup, text="Buscar", command=self.fBuscar_presupuesto,
                               width=11, bg='Blue', fg='white')
        self.btn_buscar.grid(row=0, column=2, padx=3, pady=2, sticky=W)
        self.btn_showall=Button(self.frame_busqueda_resupresup, text="Mostrar todo", command=self.fShowall, width=11,
                                bg='Blue', fg='white')
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # BOTONES IMPRESION
        # ----------------------------------------------------------------------

        self.btn_showall.grid(row=0, column=3, padx=4, pady=2, sticky=W)
        self.btn_imprime_presup_int=Button(self.frame_busqueda_resupresup, text="Imp Presup. interno",
                                           command=self.creopdfint, width=15, bg='#5F9EF5', fg='white')
        self.btn_imprime_presup_int.grid(row=0, column=4, padx=4, pady=2, sticky=W)
        self.btn_imprime_presup_ext=Button(self.frame_busqueda_resupresup, text="Imp Presup. externo",
                                           command=self.creopdfext, width=15, bg='#5F9EF5', fg='white')
        self.btn_imprime_presup_ext.grid(row=0, column=5, padx=4, pady=2, sticky=W)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # BOTONES FIN PRINCIPIO ARCHIVO
        # ----------------------------------------------------------------------

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_busqueda_resupresup, text="", image=self.photo4, command=self.fToparch,
                                 bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=6, padx=4, sticky="nsew", pady=2)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_busqueda_resupresup, text="", image=self.photo5, command=self.fFinarch,
                                 bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=7, padx=4, sticky="nsew", pady=2)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # PACKS
        self.frame_resupresup_uno.pack(side=LEFT, fill=BOTH, padx=5, pady=2)
        self.frame_resupresup_dos.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        self.frame_busqueda_resupresup.pack(expand=0, side=TOP, fill=BOTH, pady=2, padx=5)
        self.frame_grid_botones.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # CAJA DE TEXTO PARA DETALLES EXTENSOS DE DESCRIPCION

        self.frame_cajatexto = LabelFrame(self.frame_grid_botones, text="Descripcion adicional", fg="red")

        self.text_especificaciones = ScrolledText(self.frame_cajatexto)
        self.text_especificaciones.config(width=120, height=4, wrap="word", padx=5, pady=5)
        self.text_especificaciones.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_cajatexto.pack(expand=0, side=TOP, fill=BOTH, pady=3, padx=5)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # TREEVIEW DETALLE PRESUPUESTO
        # ----------------------------------------------------------------------

        self.frame_tvw_auxcomp=LabelFrame(self.frame_grid_botones, text="Componentes presupuesto actual",
                                          foreground="#CD5C5C")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_auxcomp)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_auxcomp = ttk.Treeview(self.frame_tvw_auxcomp, height=5, columns=("col1", "col2", "col3", "col4",
                                                                    "col5", "col6", "col7", "col8", "col9", "col10"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        self.grid_tvw_auxcomp.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_auxcomp.column("col1", width=100, anchor=W, minwidth=100)
        self.grid_tvw_auxcomp.column("col2", width=30, anchor=W, minwidth=30)
        self.grid_tvw_auxcomp.column("col3", width=160, anchor=CENTER, minwidth=130)
        self.grid_tvw_auxcomp.column("col4", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_auxcomp.column("col5", width=60, anchor=CENTER, minwidth=60)
        self.grid_tvw_auxcomp.column("col6", width=100, anchor=CENTER, minwidth=80)
        self.grid_tvw_auxcomp.column("col7", width=100, anchor=CENTER, minwidth=80)
        self.grid_tvw_auxcomp.column("col8", width=100, anchor=CENTER, minwidth=80)
        self.grid_tvw_auxcomp.column("col9", width=100, anchor=CENTER, minwidth=80)
        self.grid_tvw_auxcomp.column("col10", width=100, anchor=CENTER, minwidth=80)

        self.grid_tvw_auxcomp.heading("#0", text="Id", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col1", text="Proveedor", anchor=W)
        self.grid_tvw_auxcomp.heading("col2", text="Cod.Componente", anchor=W)
        self.grid_tvw_auxcomp.heading("col3", text="Componente", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col4", text="%IVA", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col5", text="Cantidad", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col6", text="Costo Neto dolar", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col7", text="Total Presupuesto", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col8", text="Total redondeo", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col9", text="Total Ganancia", anchor=CENTER)
        self.grid_tvw_auxcomp.heading("col10", text="Total Costo", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_auxcomp, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_auxcomp, orient=VERTICAL)
        self.grid_tvw_auxcomp.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_auxcomp.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_auxcomp.xview)
        scroll_y.config(command=self.grid_tvw_auxcomp.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_tvw_auxcomp['selectmode'] = 'browse'
        self.grid_tvw_auxcomp.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)

        self.frame_tvw_auxcomp.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS DATOS DEL CLIENTE
        # ----------------------------------------------------------------------

        self.frame_cliente = LabelFrame(self.master, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                        highlightbackground="blue" )

        fff = tkFont.Font(family="Arial", size=8, weight="bold")
        www = tkFont.Font(family="Arial", size=10, weight="bold")

        # NUMERO DE PRESUPUESTO
        self.lbl_nro_presup = Label(self.frame_cliente, text="Nº: ", font=www, fg="red", bg="#CEF2EF", justify=RIGHT)
        self.lbl_nro_presup.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_nro_presup2 = Label(self.frame_cliente, textvariable=self.strvar_nro_presup, font=www, bg="#CEF2EF",
                                     fg="red", width=5)
        self.lbl_nro_presup2.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        # FECHA DE VENTA
        self.lbl_fecha_presup = Label(self.frame_cliente, text="Fecha: ", bg="#CEF2EF", justify=RIGHT)
        self.lbl_fecha_presup.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_fecha_presup = Entry(self.frame_cliente, textvariable=self.strvar_fecha_presup, width=10)
        self.entry_fecha_presup.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.entry_fecha_presup.bind("<FocusOut>", self.formato_fecha)

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_cliente, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=4, pady=2, sticky='nsew')

        # NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_cliente, text="Cliente: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_texto_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_cliente, textvariable=self.strvar_nombre_cliente, width=40)
        self.entry_nombre_cliente.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        self.strvar_nombre_cliente.trace("w", lambda *args: limitador(self.strvar_nombre_cliente, 50))

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = Label(self.frame_cliente, text="", bg="#CEF2EF")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=2, pady=2, sticky=W)
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_cliente, textvariable=self.strvar_sit_fiscal,
                                                     justify=LEFT, state='readonly', width=22)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky=W)

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = Label(self.frame_cliente, text="CUIT:", bg="#CEF2EF", justify=LEFT)
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=2, pady=2, sticky=W)
        self.entry_cuit_cliente = Entry(self.frame_cliente, textvariable=self.strvar_cuit, justify=RIGHT, width=12)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=2, pady=2, sticky=W)

        # % GANANCIA
        self.lbl_tasa_ganancia = Label(self.frame_cliente, text="Gan.%: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_tasa_ganancia.grid(row=0, column=11, padx=3, pady=2, sticky=W)
        self.entry_tasa_ganancia = Entry(self.frame_cliente, textvariable=self.strvar_tasa_ganancia, width=5,
                                         justify=RIGHT)
        self.entry_tasa_ganancia.grid(row=0, column=12, padx=2, pady=2, sticky=E)
        self.entry_tasa_ganancia.config(validate="key", validatecommand=vcmd)
        self.entry_tasa_ganancia.bind('<Tab>', lambda e: self.calcular("completo"))

        # COTIZACION DEL DOLAR DEL DIA
        #fff = tkFont.Font(family="Arial", size=8, weight="bold")
        self.lbl_dolarhoy1 = Label(self.frame_cliente, text="Dolar:", justify=LEFT, bg="#CEF2EF", foreground="red")
        self.lbl_dolarhoy1.grid(row=0, column=13, padx=4, pady=2, sticky=W)
        self.entry_dolarhoy2 = Entry(self.frame_cliente, textvariable=self.strvar_valor_dolar_hoy, width=8,
                                     justify=RIGHT, foreground="red")
        self.entry_dolarhoy2.grid(row=0, column=14, padx=2, pady=2, sticky=E)

        self.frame_cliente.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=3)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS FORMA DE PAGO
        # ----------------------------------------------------------------------

        self.frame_forma_pago = LabelFrame(self.master, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                        highlightbackground="blue")

        # forma de pago y detalle
        self.lbl_combo_formapago = Label(self.frame_forma_pago, text="Forma de Pago: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_combo_formapago.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.combo_formapago = ttk.Combobox(self.frame_forma_pago, textvariable=self.strvar_combo_formas_pago,
                                            state='readonly', width=15)
        self.combo_formapago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                         "Tarjeta Credito", "Cheque"]
        self.combo_formapago.current(0)
        self.combo_formapago.grid(row=0, column=1, padx=4, pady=2, sticky=W)

        # Detalle de pago
        self.lbl_deta_formapago = Label(self.frame_forma_pago, text="Detalle: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_deta_formapago.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_deta_formapago = Entry(self.frame_forma_pago, textvariable=self.strvar_detalle_pago, width=123)
        self.entry_deta_formapago.grid(row=0, column=3, padx=4, pady=2, sticky=W)

        self.frame_forma_pago.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS DATOS ARTICULO/COMPONENTE A VENDER
        # ----------------------------------------------------------------------

        self.frame_componentes = LabelFrame(self.master, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                        highlightbackground="blue")

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = Button(self.frame_componentes, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=2, pady=2, sticky=E)

        # ENTRY ARTICULO
        self.lbl_componente = Label(self.frame_componentes, text="Componente: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_componente.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.entry_componente = Entry(self.frame_componentes, textvariable=self.strvar_componente, width=51,
                                      justify=LEFT)
        self.entry_componente.grid(row=0, column=2, padx=2, pady=2, sticky=E)
        self.strvar_componente.trace("w", lambda *args: limitador(self.strvar_componente, 100))

        # COMBO TASA IVA
        self.lbl_combo_tasa_iva = Label(self.frame_componentes, justify=LEFT, foreground="black", bg="#CEF2EF",
                                        text="IVA %")
        self.lbl_combo_tasa_iva.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.combo_tasa_iva = ttk.Combobox(self.frame_componentes, textvariable=self.strvar_combo_tasa_iva,
                                           state='readonly', width=6)
        self.combo_tasa_iva['value'] = ["21.00", "10.50"]
        self.combo_tasa_iva.current(0)
        self.combo_tasa_iva.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.combo_tasa_iva.bind('<Tab>', lambda e: self.calcular("completo"))

        # ENTRY CANTIDAD
        self.lbl_cantidad = Label(self.frame_componentes, text="Cant.: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_cantidad.grid(row=0, column=7, padx=2, pady=2, sticky=W)
        self.entry_cantidad = Entry(self.frame_componentes, textvariable=self.strvar_cantidad_vendida, width=4,
                                    justify=RIGHT)
        self.entry_cantidad.grid(row=0, column=8, padx=2, pady=2, sticky=E)
        self.entry_cantidad.config(validate="key", validatecommand=vcmd)
        self.entry_cantidad.bind('<Tab>', lambda e: self.calcular("completo"))

        # ENTRY NETO DOLAR
        self.lbl_neto_dolar = Label(self.frame_componentes, text="Neto dolar: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_neto_dolar.grid(row=0, column=9, padx=2, pady=2, sticky=W)
        self.entry_neto_dolar = Entry(self.frame_componentes, textvariable=self.strvar_neto_dolar, width=8,
                                      justify=RIGHT)
        self.entry_neto_dolar.grid(row=0, column=10, padx=2, pady=2, sticky=E)
        self.entry_neto_dolar.config(validate="key", validatecommand=vcmd)
        self.entry_neto_dolar.bind('<Tab>', lambda e: self.calcular("completo"))

        self.lbl_proved = Label(self.frame_componentes, text="Prov.: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_proved.grid(row=0, column=11, padx=2, pady=2, sticky=W)
        self.entry_proved = Entry(self.frame_componentes, textvariable=self.strvar_proveedor, width=15, justify=LEFT)
        self.entry_proved.grid(row=0, column=12, padx=2, pady=2, sticky=W)

        self.lbl_codigo_componente = Label(self.frame_componentes, text="Cod.: ", bg="#CEF2EF", justify=LEFT)
        self.lbl_codigo_componente.grid(row=0, column=13, padx=2, pady=2, sticky=W)
        self.entry_codigo_componente = Entry(self.frame_componentes, textvariable=self.strvar_codigo_componente,
                                             width=15, justify=LEFT)
        self.entry_codigo_componente.grid(row=0, column=14, padx=2, pady=2, sticky=W)

        self.frame_componentes.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS IMPORTES DEL PRESUPUESTO - Linea de totales del item a cargar
        # ----------------------------------------------------------------------

        self.frame_importes_articulo = LabelFrame(self.master, text="", foreground="black", relief="solid")

        fff = tkFont.Font(family="Arial", size=9, weight="bold")

        # COSTO PESOS CON IVA
        self.lbl_costo_pesos_bruto_unidad = Label(self.frame_importes_articulo, text="Costo Unidad: ", justify=LEFT)
        self.lbl_costo_pesos_bruto_unidad.grid(row=2, column=0, padx=1, pady=2, sticky=W)
        self.lbl_costo_pesos_bruto_unidad2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_costo_bruto_pesos_unidad, width=10,
                                                  font= fff, fg="blue", justify=RIGHT)
        self.lbl_costo_pesos_bruto_unidad2.grid(row=2, column=1, padx=1, pady=2, sticky=E)

        # COSTO PESOS CON IVA * CANTIDAD
        self.lbl_costo_bruto_pesos_xcanti = Label(self.frame_importes_articulo, text="Costo total: ", justify=LEFT)
        self.lbl_costo_bruto_pesos_xcanti.grid(row=2, column=2, padx=1, pady=2, sticky=W)
        self.lbl_costo_bruto_pesos_xcanti2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_costo_bruto_pesos_xcanti, width=10,
                                                  font= fff, fg="blue", justify=RIGHT)
        self.lbl_costo_bruto_pesos_xcanti2.grid(row=2, column=3, padx=1, pady=2, sticky=E)

        # IMPORTE PESOS GANANCIA * CANTIDAD
        self.lbl_importe_ganancia_xcanti = Label(self.frame_importes_articulo, text="Ganancia: ", justify=LEFT)
        self.lbl_importe_ganancia_xcanti.grid(row=2, column=4, padx=1, pady=2, sticky=W)
        self.lbl_importe_ganancia_xcanti2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_importe_ganancia_xcanti, width=10,
                                                  fg="blue", font= fff, justify=RIGHT)
        self.lbl_importe_ganancia_xcanti2.grid(row=2, column=5, padx=1, pady=2, sticky=E)

        # PRECIO DE VENTA
        self.lbl_precio_final_xcanti = Label(self.frame_importes_articulo, text="Precio venta: ", justify=LEFT)
        self.lbl_precio_final_xcanti.grid(row=2, column=6, padx=1, pady=2, sticky=W)
        self.lbl_precio_final_xcanti2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_precio_final_xcanti, width=10,
                                                  fg="blue", font= fff, justify=RIGHT)
        self.lbl_precio_final_xcanti2.grid(row=2, column=7, padx=1, pady=2, sticky=E)

        # Redondeo del total del Item
        self.lbl_total_item_redondo = Label(self.frame_importes_articulo, text="Redondeo: ", justify=LEFT)
        self.lbl_total_item_redondo.grid(row=2, column=8, padx=1, pady=2, sticky=W)
        self.entry_total_item_redondo = Entry(self.frame_importes_articulo, textvariable=self.strvar_total_item_redondo,
                                              width=15, justify=RIGHT)
        self.entry_total_item_redondo.grid(row=2, column=9, padx=1, pady=2, sticky=E)
        self.entry_total_item_redondo.config(validate="key", validatecommand=vcmd)
        self.entry_total_item_redondo.bind('<Tab>', lambda e: self.calcular("precio_venta_unidad"))

        self.btn_detalle_precio_articulo=Button(self.frame_importes_articulo, text="Detalle precio",
                                                command=self.fDetalle_precio_articulo, width=15, bg='blue', fg='white')
        self.btn_detalle_precio_articulo.grid(row=2, column=10, padx=5, pady=2, sticky=W)

        self.btn_articulo=Button(self.frame_importes_articulo, text="Articulos",
                                                command=self.fVerArticulos, width=14, bg='blue', fg='white')
        self.btn_articulo.grid(row=2, column=11, padx=5, pady=2, sticky=W)

        #self.frame_importes_articulo_uno.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_importes_articulo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # LABELS TOTALES GENERALES
        # ----------------------------------------------------------------------

        self.frame_totales_generales = LabelFrame(self.master, text="", foreground="black", border=5, relief=RIDGE)

        fff = tkFont.Font(family="Arial", size=9, weight="bold")

        # TOTAL COSTO BRUTO
        self.lbl_total_costos = Label(self.frame_totales_generales, text="Total Costos: ", justify=LEFT, font=fff,
                                      foreground="#ff33f6")
        self.lbl_total_costos.grid(row=0, column=0, padx=8, pady=2, sticky=W)
        self.lbl_total_costos2 = Label(self.frame_totales_generales, textvariable=self.strvar_total_costos, width=15,
                                       justify=RIGHT, font=fff, foreground="#ff33f6")
        self.lbl_total_costos2.grid(row=0, column=1, padx=8, pady=2, sticky=E)

        # TOTAL GANANCIA
        self.lbl_total_ganancia = Label(self.frame_totales_generales, text="Total ganancia: ", justify=LEFT, font=fff,
                                        foreground="#ff33f6")
        self.lbl_total_ganancia.grid(row=0, column=2, padx=8, pady=2, sticky=W)
        self.lbl_total_ganancia2 = Label(self.frame_totales_generales, textvariable=self.strvar_total_ganancia,
                                         width=15, justify=RIGHT, font=fff, foreground="#ff33f6")
        self.lbl_total_ganancia2.grid(row=0, column=3, padx=8, pady=2, sticky=E)

        # TOTAL PRESUPUESTO GLOBAL
        self.lbl_total_presupuesto = Label(self.frame_totales_generales, text="Total presupuesto: ", justify=LEFT,
                                           font=fff, foreground="#ff33f6")
        self.lbl_total_presupuesto.grid(row=0, column=4, padx=8, pady=2, sticky=W)
        self.lbl_total_presupuesto2 = Label(self.frame_totales_generales, textvariable=self.strvar_total_presupuesto,
                                            width=15, justify=RIGHT, font=fff, foreground="#ff33f6")
        self.lbl_total_presupuesto2.grid(row=0, column=5, padx=8, pady=2, sticky=E)

        # TOTAL PRESUPUESTO REDONDEADO
        self.lbl_total_presup_redondo = Label(self.frame_totales_generales, text="Total redondeado: ", justify=LEFT,
                                              font=fff, foreground="#ff33f6")
        self.lbl_total_presup_redondo.grid(row=0, column=6, padx=8, pady=2, sticky=W)
        self.lbl_total_presup_redondo2 = Label(self.frame_totales_generales,
                                               textvariable=self.strvar_total_presup_redondo, width=15, justify=RIGHT,
                                               font=fff, foreground="#ff33f6")
        self.lbl_total_presup_redondo2.grid(row=0, column=7, padx=8, pady=2, sticky=E)

        self.frame_totales_generales.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

    # ----------------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------------

    def estado_inicial(self):

        """ Es el estado que le doy a entrys y botones al iniciar el modulo """

        # limpia todos los entrys - borro los datos que puedan tener
        self.limpiar_entrys_total()
        # preparo fecha del presupuesto - paso a string
        una_fecha = date.today()
        self.strvar_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))
        # desactivo todos los entrys
        self.estado_entrys_inicial("disabled")
        # Desactivo los botones de la parte de los componentes
        self.estado_botones_dos("disabled")
        # Activo los botones del CRUD principal - Nuevo-Edito_Borro presupuesto
        self.estado_botones_uno("normal")
        # Vacio el TVW auxpresup - donde cargo los componentes
        self.varPresupuestos.vaciar_auxpresup("aux_presup")
        self.limpiar_Grid_auxiliar()
        self.alta_modif_aux = 0
        self.alta_modif_presup = 0
        # Modo activo el browse del Grid  de los presupuesto
        self.grid_tvw_resupresup['selectmode'] = 'browse'
        self.grid_tvw_resupresup.bind("<Double-Button-1>", self.DobleClickGrid)

    def estado_entrys_inicial(self, estado):

        """ Estado inicial de los entrys todos - cliente y componentes - solo se ejecuta una vez al entrar al modulo """

        self.entry_fecha_presup.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_componente.configure(state=estado)
        self.btn_bus_art.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)
        self.entry_dolarhoy2.configure(state=estado)
        self.entry_cantidad.configure(state=estado)
        self.entry_tasa_ganancia.configure(state=estado)
        self.entry_neto_dolar.configure(state=estado)
        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_codigo_componente.configure(state=estado)
        self.entry_total_item_redondo.configure(state=estado)
        self.text_especificaciones.configure(state=estado)
        self.btn_detalle_precio_articulo.configure(state=estado)
        self.btn_articulo.configure(state=estado)
        self.btn_reset_componente.configure(state=estado)

    def estado_entrys_crud(self, estado):

        """ Cuando pido nuevo presupuesto solo activo los entrys de resumen de presupuesto  - no de los componentes """

        self.entry_fecha_presup.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.entry_dolarhoy2.configure(state=estado)
        self.entry_tasa_ganancia.configure(state=estado)
        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)
        self.text_especificaciones.configure(state=estado)

    def estado_entrys_crud_2(self, estado):

        """ Activo entrys de la parte de (componentes) cuando presiono boton (+ componente) """

        self.entry_componente.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)
        self.entry_cantidad.configure(state=estado)
        self.entry_neto_dolar.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_codigo_componente.configure(state=estado)
        self.entry_total_item_redondo.configure(state=estado)
        self.text_especificaciones.configure(state=estado)
        self.btn_detalle_precio_articulo.configure(state=estado)
        self.btn_articulo.configure(state=estado)
        self.btn_reset_componente.configure(state=estado)

    def estado_botones_uno(self, estado):

        """ Activo/desactiva los botones principales del CRUD - nuevo, borro, edito, toparch """

        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.btn_nuevo_presup.configure(state=estado)
        self.btn_edito_presup.configure(state=estado)
        self.btn_borro_presup.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_buscar.configure(state=estado)
        self.btn_imprime_presup_int.configure(state=estado)
        self.btn_imprime_presup_ext.configure(state=estado)
        self.entry_busqueda_presup.configure(state=estado)

        if self.alta_modif_presup == 1:
            self.grid_tvw_resupresup['selectmode'] = 'none'
            self.grid_tvw_resupresup.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif_presup == 2 or self.alta_modif_presup == 0:
            self.grid_tvw_resupresup['selectmode'] = 'browse'
            self.grid_tvw_resupresup.bind("<Double-Button-1>", self.DobleClickGrid)

    def estado_botones_dos(self, estado):

        """ Activo/desactivo los botones de la parte de los componentes - + componente - componente Cierre etc... """

        self.btn_ingresar_componente.configure(state=estado)
        self.btn_editar_componente.configure(state=estado)
        self.btn_mas_componente.configure(state=estado)
        self.btn_menos_componente.configure(state=estado)
        self.btn_cerrar_presupuesto.configure(state=estado)
        self.btn_guardar_como.configure(state=estado)
        self.btn_cancelar_presupuesto.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)
        self.btn_bus_art.configure(state=estado)

    def fNo_modifique(self, event):
        return

    def limpiar_entrys_parcial(self):

        """ Vacio los entrys relaionados con la carga del componente y totales """

        self.strvar_componente.set(value="")
        self.combo_tasa_iva.current(0)
        self.strvar_cantidad_vendida.set(value="1")
        self.strvar_neto_dolar.set(value="0.00")
        self.strvar_proveedor.set(value="")
        self.strvar_codigo_componente.set(value="")
        self.strvar_costo_neto_pesos_unidad.set(value="0.00")
        self.strvar_costo_neto_pesos_xcanti.set(value="0.00")
        self.strvar_total_item_redondo.set(value="0.00")

    def limpiar_entrys_total(self):

        """ Limpia totdos los e Entrys - se usa en inicial y para cancelar """

        una_fecha = date.today()
        self.strvar_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_nombre_cliente.set(value="Consumidor Final")
        self.strvar_codigo_cliente.set(value=0)
        self.combo_sit_fiscal_cliente.current(0)
        self.strvar_cuit.set(value="")
        self.strvar_tasa_ganancia.set(value="0.00")
        self.strvar_componente.set(value="")
        self.combo_tasa_iva.current(0)
        self.strvar_valor_dolar_hoy.set(value="0.00")
        self.traer_dolarhoy()
        self.strvar_cantidad_vendida.set(value=1)
        #self.strvar_tasa_ganancia.set(value="0.00")
        self.strvar_neto_dolar.set(value="0.00")
        self.combo_formapago.current(0)
        self.strvar_detalle_pago.set(value="")
        self.strvar_proveedor.set(value="")
        self.strvar_codigo_componente.set(value="")
        self.strvar_costo_neto_pesos_unidad.set(value="0.00")
        self.strvar_costo_neto_pesos_xcanti.set(value="0.00")
        self.strvar_total_presupuesto.set(value="0.00")
        self.strvar_total_ganancia.set(value="0.00")
        self.strvar_total_costos.set(value="0.00")
        self.strvar_total_item_redondo.set(value="0.00")
        self.strvar_total_presup_redondo.set(value="0.00")
        self.text_especificaciones.delete('1.0', 'end')

    def limpiar_totales(self):

        """ Limpia los totales generales """

        self.strvar_costo_neto_pesos_unidad.set(value="0.00")
        self.strvar_costo_neto_pesos_xcanti.set(value="0.00")
        self.strvar_costo_bruto_pesos_unidad.set(value="0.00")
        self.strvar_costo_bruto_pesos_xcanti.set(value="0.00")
        self.strvar_importe_iva_unidad.set(value="0.00")
        self.strvar_importe_iva_xcanti.set(value="0.00")
        self.strvar_importe_ganancia_unidad.set(value="0.00")
        self.strvar_importe_ganancia_xcanti.set(value="0.00")
        self.strvar_precio_final_unidad.set(value="0.00")
        self.strvar_precio_final_xcanti.set(value="0.00")

    # -----------------------------------------------------------------
    # GRIDS
    # -----------------------------------------------------------------

    def limpiar_Grid_resu_presup(self):

        for item in self.grid_tvw_resupresup.get_children():
            self.grid_tvw_resupresup.delete(item)

    def llena_grilla_resu_presup(self, ult_tabla_id):

        try:

            datos = self.varPresupuestos.consultar_presupuestos(self.filtro_activo_resu_presup)

            for row in datos:

                # convierto fecha de 2024-12-19 a 19/12/2024
                forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'))

                self.grid_tvw_resupresup.insert("", END, text=row[0], values=(row[1], forma_normal, row[4],
                                                                         row[7], row[8], row[9], row[10]))

            if len(self.grid_tvw_resupresup.get_children()) > 0:
                   self.grid_tvw_resupresup.selection_set(self.grid_tvw_resupresup.get_children()[0])

            self.mover_puntero_topend('END')

        except:

            messagebox.showinfo("Error", "Fallo carga de grilla resu_presup", parent=self)
            return

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_tvw_resupresup.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_tvw_resupresup.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """
            """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_tvw_resupresup.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_tvw_resupresup.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_tvw_resupresup.yview(self.grid_tvw_resupresup.index(rg))
            return

        self.mover_puntero_topend("END")

    def limpiar_Grid_auxiliar(self):

        for item in self.grid_tvw_auxcomp.get_children():
            self.grid_tvw_auxcomp.delete(item)

    def llena_grilla_auxiliar(self, ult_tabla_id):

        try:

            datos = self.varPresupuestos.consultar_presupuestos(self.filtro_activo_auxiliar)

            for row in datos:
                self.grid_tvw_auxcomp.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4],
                                                                                  row[5], row[6], row[7], row[8],
                                                                                  row[9], row[10]))

            if len(self.grid_tvw_auxcomp.get_children()) > 0:
                   self.grid_tvw_auxcomp.selection_set(self.grid_tvw_auxcomp.get_children()[0])

        except:

            messagebox.showinfo("Error", "Fallo carga de grilla auxiliar", parent=self)
            return

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_tvw_auxcomp.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_tvw_auxcomp.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """

            if ult_tabla_id:

                """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

                self.grid_tvw_auxcomp.selection_set(rg)
                # Para que no me diga que no hay nada seleccionado
                self.grid_tvw_auxcomp.focus(rg)
                # para que la linea seleccionada no me quede fuera del area visible del treeview
                self.grid_tvw_auxcomp.yview(self.grid_tvw_auxcomp.index(rg))

    # ----------------------------------------------------------------------
    # BOTONES Nuevo presupuesto - Editar - Eliminar - Cancelar
    # ----------------------------------------------------------------------

    def fNuevo_presupuesto(self):

        self.alta_modif_presup = 1

        self.estado_entrys_crud("normal")
        self.estado_botones_uno("disabled")
        self.estado_botones_dos("normal")
        self.limpiar_entrys_total()
        self.strvar_nro_presup.set(value=(int(self.varPresupuestos.traer_ultimo(1)) + 1))
        self.entry_fecha_presup.focus()

    def fEdito_presupuesto(self):

        self.estado_entrys_crud("normal")
        self.estado_botones_uno("disabled")
        self.estado_botones_dos("normal")
        self.limpiar_entrys_total()

        self.alta_modif_presup = 2

        self.varPresupuestos.vaciar_auxpresup("aux_presup")

        # 1 - Obtener el numero de presupuesto

        self.selected = self.grid_tvw_resupresup.focus()
        self.clave = self.grid_tvw_resupresup.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_tvw_resupresup.item(self.selected, 'values')
        self.strvar_nro_presup.set(value=valores[0])

        # 2 - Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta

        datos_resupresup = self.varPresupuestos.traer_resu_presup(self.strvar_nro_presup.get())

        fechapaso = datos_resupresup[2].strftime('%d/%m/%Y')
        self.strvar_fecha_presup.set(fechapaso)
        self.strvar_codigo_cliente.set(value=datos_resupresup[3])
        self.strvar_nombre_cliente.set(value=datos_resupresup[4])
        self.strvar_sit_fiscal.set(value=datos_resupresup[5])
        self.strvar_cuit.set(value=datos_resupresup[6])
        self.strvar_valor_dolar_hoy.set(value=datos_resupresup[7])
        self.strvar_tasa_ganancia.set(value=datos_resupresup[8])
        self.strvar_combo_formas_pago.set(value=datos_resupresup[11])
        self.strvar_detalle_pago.set(value=datos_resupresup[12])
        self.strvar_total_presup_redondo.set(value=datos_resupresup[10])
        self.text_especificaciones.configure(state="normal")
        self.text_especificaciones.insert(END, datos_resupresup[13])

        # 3 - Cargar los componentes del presupuesto de deta_presup

        datos_detapresup = self.varPresupuestos.traer_deta_presup(self.strvar_nro_presup.get())

        for row in datos_detapresup:

            dolar_a_pesos = float(row[7]) * float(self.strvar_valor_dolar_hoy.get())
            iva_a_cargar = dolar_a_pesos * (float(row[5]) / 100)
            ganancia_a_cargar = (dolar_a_pesos + iva_a_cargar) * (float(self.strvar_tasa_ganancia.get()) / 100)
            total_presupuesto = dolar_a_pesos + iva_a_cargar + ganancia_a_cargar

            self.varPresupuestos.insertar_auxpresup(row[2], row[3], row[4], row[5], row[6], row[7],
                                                    total_presupuesto, row[8], ganancia_a_cargar, dolar_a_pesos)

        self.calcular("completo")
        self.calcular("totalpresupuesto")
        self.limpiar_Grid_auxiliar()
        self.llena_grilla_auxiliar("")
        #self.entry_componente.focus()

    def fBorro_presupuesto(self):

        # ----------------------------------------------------------------------
        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_tvw_resupresup.focus()
        self.selected_ant = self.grid_tvw_resupresup.prev(self.selected)
        # guardo en clave el Id pero de la Bd (no son el mismo
        self.clave = self.grid_tvw_resupresup.item(self.selected, 'text')
        self.clave_ant = self.grid_tvw_resupresup.item(self.selected_ant, 'text')
        # ----------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_tvw_resupresup.item(self.selected, 'values')
        #        data = str(self.clave)+" "+valores[0]+" " + valores[2]
        data = " Presupuesto Nº " + valores[0] + " de " + valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar presupuesto?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion Cancelada", parent=self)
            return

        # Elimino de resu_ventas y deta_ventas
        self.varPresupuestos.eliminar_resupresup1(self.clave)
        self.varPresupuestos.eliminar_detapresup(valores[0])  # por numero de venta

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid_resu_presup()
        self.llena_grilla_resu_presup(self.clave_ant)

    def fCancela_presup(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys_total()
        self.limpiar_totales()
        self.estado_inicial()
        self.varPresupuestos.vaciar_auxpresup("aux_presup")
        self.entry_fecha_presup.focus()

    def DobleClickGrid(self, event):

        self.limpiar_entrys_parcial()
        self.estado_entrys_crud_2("disabled")
        self.fEdito_presupuesto()

    def fSalir(self):

        r = messagebox.askquestion("Salir", "Confirma Salir?", parent=self)
        if r == messagebox.NO:
            return
        self.master.destroy()

    # ----------------------------------------------------------------------
    # BOTONES sobre componentes - Nuevo componente - Editar - Eliminar - Cancelar
    # ----------------------------------------------------------------------

    def fMas_componente(self):

        """ Agrega un componente al presupuesto - activa el sistema para ingresar componentes """

        # Los Entrys propios del componente
        self.estado_entrys_crud_2("normal")
        # deshabilito los botones del crud 2
        self.btn_mas_componente.configure(state="disabled")
        self.btn_menos_componente.configure(state="disabled")
        self.btn_editar_componente.configure(state="disabled")
        self.entry_componente.focus()

    def fMenos_componente(self):

        # ---------------------------------------------------------------------------------
        """ Elimina un coponente previamente cargado del presupuesto """

        self.selected = self.grid_tvw_auxcomp.focus()
        self.selected_ant = self.grid_tvw_auxcomp.prev(self.selected)
        self.clave = self.grid_tvw_auxcomp.item(self.selected, 'text')
        self.clave_ant = self.grid_tvw_auxcomp.item(self.selected_ant, 'text')
        # ---------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_tvw_auxcomp.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        self.varPresupuestos.eliminar_auxpresup(self.clave)

        self.limpiar_Grid_auxiliar()
        self.llena_grilla_auxiliar(self.clave_ant)
        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.calcular("totalventa")
        self.calcular("totalpresupuesto")

    def fInsertar_item_auxpresup(self):

        """ Inserto el componente en tabla auxiliar (aux_presup) """

        # VALIDACIONES
        # 1- que articulo no este vacio y que haya cantidad
        if len(self.strvar_componente.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de componente", parent=self)
            self.entry_componente.focus()
            return
        if float(self.strvar_cantidad_vendida.get()) == 0:
            messagebox.showerror("Error", "Falta cantidad de articulo", parent=self)
            self.entry_cantidad.focus()
            return

        # controlo que no sea una modificacion para borrar el componente anterior
        if self.alta_modif_aux == 1:

            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_tvw_auxcomp.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            self.clave = self.grid_tvw_auxcomp.item(self.selected, 'text')

            n = self.varPresupuestos.eliminar_auxpresup(self.clave)

        # vuelvo a cero la bandera de modificacion
        self.alta_modif_aux = 0

        # Insertamos el componente en el auxilliar de presupuesto (aux_presup)

        self.varPresupuestos.insertar_auxpresup(self.strvar_proveedor.get(), self.strvar_codigo_componente.get(),
                                                self.strvar_componente.get(), self.strvar_combo_tasa_iva.get(),
                                                self.strvar_cantidad_vendida.get(), self.strvar_neto_dolar.get(),
                                                self.strvar_precio_final_xcanti.get(),
                                                self.strvar_total_item_redondo.get(),
                                                self.strvar_importe_ganancia_xcanti.get(),
                                                self.strvar_costo_bruto_pesos_xcanti.get())

        self.calcular("totalpresupuesto")

        self.limpiar_Grid_auxiliar()

        ultimo_tabla_id = self.varPresupuestos.traer_ultimo(0)
        self.llena_grilla_auxiliar(ultimo_tabla_id)

        # dejar en blanco todos los entrys del articulo
        self.limpiar_entrys_parcial()
        # desactivar los entrys de la parte dos (componentes)
        self.estado_entrys_crud_2("disabled")
        # limpiar los totales del componente
        self.limpiar_totales()

        messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

        # Botones de la parte componentes vuelven a estado inicial (+ compon... - compon...
        self.estado_botones_dos("normal")
        self.entry_componente.focus()

    def fEditar_item_auxpresup(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_tvw_auxcomp.focus()
        # Asi obtengo la clave de la Tabla campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_auxcomp.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        # activo entrys de segundo nivel (componentes)
        self.estado_entrys_crud_2("normal")

        # Desactivo botones de novel 2 excepto "Cancelar, ingresar componente y cerrar presupuesto"
        self.estado_botones_dos("disabled")
        self.btn_ingresar_componente.configure(state="normal")
        self.btn_cerrar_presupuesto.configure(state="normal")
        self.btn_guardar_como.configure(state="normal")
        self.btn_cancelar_presupuesto.configure(state="normal")
        self.btn_reset_componente.configure(state="normal")

        # activo bandera de modificacion de tabla auxpresup
        self.alta_modif_aux = 1

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        # En la lista valores cargo toda la liena del treeview completa
        valores = self.grid_tvw_auxcomp.item(self.selected, 'values')

        self.strvar_proveedor.set(value=valores[0])
        self.strvar_codigo_componente.set(value=valores[1])
        self.strvar_componente.set(value=valores[2])
        self.strvar_combo_tasa_iva.set(value=valores[3])
        self.strvar_cantidad_vendida.set(value=valores[4])
        self.strvar_neto_dolar.set(value=valores[5])
        self.strvar_total_item_redondo.set(value=valores[7])

        self.calcular("completo")

        #self.llena_grilla_auxiliar(self.clave)

        self.entry_componente.focus()

    def fReset_articulo(self):

        r = messagebox.askquestion("Resetr", "Confirma anular componente?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys_parcial()
        self.limpiar_totales()
        self.estado_entrys_crud_2("disabled")
        self.estado_botones_dos("normal")
        self.alta_modif_aux = 0
        self.alta_modif_presup = 0
        self.entry_componente.focus()

    # -----------------------------------------------------------------------------
    # GUARDAR PRESUPUESTOS
    # -----------------------------------------------------------------------------

    def fGuardar(self):
        self.fCerrarPresupuesto("normal")

    def fGuardar_como(self):
        self.fCerrarPresupuesto("como")

    def fCerrarPresupuesto(self, parametro):

        # VALIDACIONES

        # valido que haya items en venta
        if len(self.grid_tvw_auxcomp.get_children()) <= 0:
            messagebox.showerror("Error", "No hay items cargados", parent=self)
            return
        # velido nro venta
        if self.strvar_nro_presup.get() == 0:
            messagebox.showerror("Error", "Verifique numero de venta", parent=self)
            return
        # valido fecha venta
        if self.strvar_fecha_presup.get() == "":
            messagebox.showerror("Error", "Verifique fecha de venta", parent=self)
            return
        # valido nombre de cliente
        if self.strvar_nombre_cliente.get() == "":
            messagebox.showerror("Error", "Ingrese nombre de cliente", parent=self)
            return
        # --------------------------------------------------------------------

        if parametro == "normal":
            r = messagebox.askquestion("Cerrar presupuesto", "Guardamos el presupuesto? ", parent=self)
            if r == messagebox.NO:
                return

        if parametro == "como":
            r = messagebox.askquestion("Cerrar presupuesto", "Guardar como... asignando numero siguiente ",
                                       parent=self)
            if r == messagebox.NO:
                return

        if parametro == "normal":

            # borrar este numero de venta si existiera como en el caso de una modificacion en resu_presup y
            # en deta_presup
            self.varPresupuestos.eliminar_detapresup(self.strvar_nro_presup.get())
            self.varPresupuestos.eliminar_resupresup2(self.strvar_nro_presup.get())

        if parametro == "como":

            # Si es -guardar_como- busco solamente aignar un  numero mas de presupuesto como si fuera uno nuevo
            self.strvar_nro_presup.set(value=(int(self.varPresupuestos.traer_ultimo(1)) + 1))

        # Inserto en deta_presup
        datos = self.varPresupuestos.consultar_detalle_auxpresup("aux_presup")

        for row in datos:

            # inserto en tabla DETA_PRESUP
            self.varPresupuestos.insertar_detapresup(self.strvar_nro_presup.get(),
                                             row[1],  # nombre proveedor
                                             row[2],  # codigo componente proveedor
                                             row[3],  # descripcion del componente
                                             row[4],  # tasa IVA del componente
                                             row[5],  # cantidad presupuestada
                                             row[6],  # costo neto componente en dolares
                                             row[8])  # Total en pesos redondeado

        self.nuevo_presupuesto = self.strvar_nro_presup.get()

        # Inserto en resu_presup
        fecha_aux = datetime.strptime(self.strvar_fecha_presup.get(), '%d/%m/%Y')
        self.varPresupuestos.insertar_resupresup(self.strvar_nro_presup.get(), fecha_aux,
                                         self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                         self.combo_sit_fiscal_cliente.get(), self.strvar_cuit.get(),
                                         self.strvar_valor_dolar_hoy.get(), self.strvar_tasa_ganancia.get(),
                                         self.strvar_total_presupuesto.get(), self.strvar_total_presup_redondo.get(),
                                         self.combo_formapago.get(), self.strvar_detalle_pago.get(),
                                         self.text_especificaciones.get(1.0, 'end-1c'))

        messagebox.showinfo("Guardar", "Ingreso correcto detalle y resumen", parent=self)

        # refresco grid de resupresup para que se me actualie la grilla de resu_presup
        self.limpiar_Grid_resu_presup()

        # acomodo el puntero en el presupuesto recien ingresado
        ultimo_tabla_id = self.varPresupuestos.traer_ultimo(0)
        self.llena_grilla_resu_presup(ultimo_tabla_id)

        # pongo all en blanco como si recien iniciara para que se pueda pedir un nuevo presupuesto
        self.estado_inicial()

    # -----------------------------------------------------------------------------
    # BUSQUEDAS DE PRESUPUESTOS
    # -----------------------------------------------------------------------------

    def fBuscar_presupuesto(self):

        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()
            self.filtro_activo_resu_presup = "resu_presup WHERE INSTR(rp_nomcli, '" + se_busca + "') ORDER BY rp_fecha ASC"

            self.varPresupuestos.buscar_entabla(self.filtro_activo_resu_presup)

            self.limpiar_Grid_resu_presup()
            self.llena_grilla_resu_presup("")

            """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el
            item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
            item = self.grid_tvw_resupresup.selection()
            self.grid_tvw_resupresup.focus(item)

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

    # --------------------------------------------------------------------------
    # MOVIMIENTOS PUNTERO EN EL GRID
    # --------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        # Si es tope de archivo
        if param_topend == 'TOP':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_tvw_resupresup.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return

            # selecciono el Id primero de la lista en este caso
            self.grid_tvw_resupresup.selection_set(rg)
            # pone el primero Id
            self.grid_tvw_resupresup.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_tvw_resupresup.yview(self.grid_tvw_resupresup.index(self.grid_tvw_resupresup.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_tvw_resupresup.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return

            # Selecciono el ultimo Id en este caso
            self.grid_tvw_resupresup.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_tvw_resupresup.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_tvw_resupresup.yview(self.grid_tvw_resupresup.index(self.grid_tvw_resupresup.get_children()[-1]))

    def fShowall(self):

        self.selected = self.grid_tvw_resupresup.focus()
        self.clave = self.grid_tvw_resupresup.item(self.selected, 'text')
        self.filtro_activo_resu_presup = "resu_presup ORDER BY rp_fecha"
        self.limpiar_Grid_resu_presup()
        self.llena_grilla_resu_presup(self.clave)

    # ----------------------------------------------------------
    # CALCULOS
    # ----------------------------------------------------------

    def calcular(self, que_campo):

        #Esta funcion solo controla todos los Entrys numericos que no contengan el valor "" o mas de un "-" o un "."
        self.control_valores()

        #ii = 1

        try:
        #if ii == 1:

            if que_campo == "completo":

                # -------------------------------------------------------------
                # 1 - Costo neto unidad pesos y cantidad

                self.strvar_costo_neto_pesos_unidad.set(value=str(round(float(self.strvar_neto_dolar.get()) *
                                                                    float(self.strvar_valor_dolar_hoy.get()), 2)))

                self.strvar_costo_neto_pesos_xcanti.set(value=str(round(float(self.strvar_neto_dolar.get()) *
                                                                    float(self.strvar_valor_dolar_hoy.get()) *
                                                                    float(self.strvar_cantidad_vendida.get()), 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 2 - Importe IVA unidad y cantidad

                importe_iva = (((float(self.strvar_neto_dolar.get()) * float(self.strvar_valor_dolar_hoy.get())) *
                              float(self.strvar_combo_tasa_iva.get())) / 100)

                importe_ivaxcanti = ((((float(self.strvar_neto_dolar.get()) *
                                        float(self.strvar_valor_dolar_hoy.get())) *
                                        float(self.strvar_combo_tasa_iva.get())) / 100) *
                                        float(self.strvar_cantidad_vendida.get()))

                self.strvar_importe_iva_unidad.set(value=round(importe_iva, 2))
                self.strvar_importe_iva_xcanti.set(value=round(importe_ivaxcanti, 2))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 3 - Costo BRUTO pesos unidad y cantidad

                # Costo en Pesos mas IVA * unidad
                self.strvar_costo_bruto_pesos_unidad.set(value= str(round(float(self.strvar_costo_neto_pesos_unidad.get()) +
                                                                      float(self.strvar_importe_iva_unidad.get()), 2)))
                # Costo en Pesos  ms IVA * unidad * la cantidad vendida
                self.strvar_costo_bruto_pesos_xcanti.set(value= str(round((float(self.strvar_costo_neto_pesos_unidad.get()) +
                                                                       float(self.strvar_importe_iva_unidad.get())) *
                                                                       float(self.strvar_cantidad_vendida.get()), 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 4 - Importe ganancia por unidad y por cantidad

                ganancia_unidad = round(((float(self.strvar_costo_bruto_pesos_unidad.get()) *
                                          float(self.strvar_tasa_ganancia.get())) / 100), 2)

                ganancia_xcanti = round((((float(self.strvar_costo_bruto_pesos_unidad.get()) *
                                           float(self.strvar_tasa_ganancia.get())) / 100) *
                                           float(self.strvar_cantidad_vendida.get())), 2)

                self.strvar_importe_ganancia_unidad.set(value=str(ganancia_unidad))
                self.strvar_importe_ganancia_xcanti.set(value=str(ganancia_xcanti))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 4 - Total final del componente por unidad y cantidad

                total_final_unidad = (float(self.strvar_importe_ganancia_unidad.get()) +
                                      float(self.strvar_costo_bruto_pesos_unidad.get()))
                total_final_xcanti = total_final_unidad *  float(self.strvar_cantidad_vendida.get())

                self.strvar_precio_final_unidad.set(value=str(round(total_final_unidad, 2)))
                self.strvar_precio_final_xcanti.set(value=str(round(total_final_xcanti, 2)))
                # -------------------------------------------------------------

            if que_campo == "totalpresupuesto":

                """ Guardo todos los items que compnen el presupuesto """
                datos = self.varPresupuestos.consultar_presupuestos("aux_presup")

                sumatot_presu = 0
                sumatot_redondo = 0
                sumatot_costos = 0

                """ Itero dentro de los componentes y calculo los totales generales """
                for row in datos:

                    # total costos mas IVA
                    sumatot_costos += row[10] * (1 + (row[4]/100))
                    sumatot_presu += row[7]
                    sumatot_redondo += row[8]

                """ La ganancia la calculo entre el total redondeado y el costo total bruto para todos los 
                articulos o componentes ingresadosde los articulos """

                sumatot_ganancia = sumatot_redondo - sumatot_costos

                # ganancia calculada sobre diferencia entre el "total redondeado" y el "costo total del articulo con IVA"
                self.strvar_total_ganancia.set(value=str(round(sumatot_ganancia, 2)))
                # total costos con IVA incluido
                self.strvar_total_costos.set(value=str(round(sumatot_costos, 2)))
                # Total del presupuesto real - sin redondeo
                self.strvar_total_presupuesto.set(value=str(round(sumatot_presu)))
                # total presupuesto redondeado
                self.strvar_total_presup_redondo.set(value=str(round(sumatot_redondo, 2)))

        #else:
        except:

            messagebox.showerror("Error", "Error en funcion de Calculos - revise entradas numericas", parent=self)
            return

    # -----------------------------------------------------------
    # VALIDACION ENTRADAS
    # -----------------------------------------------------------

    def control_valores(self):

        """ Hago Control (control_forma) de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
        Tambien todos los demas controles numericos que hacen falta """

        self.strvar_neto_dolar.set(value=control_numerico(self.strvar_neto_dolar.get(), "0"))
        self.strvar_cantidad_vendida.set(value=control_numerico(self.strvar_cantidad_vendida.get(), "1"))
        self.strvar_valor_dolar_hoy.set(value=control_numerico(self.strvar_valor_dolar_hoy.get(), "1"))
        self.strvar_tasa_ganancia.set(value=control_numerico(self.strvar_tasa_ganancia.get(), "1"))
        self.strvar_total_item_redondo.set(value=control_numerico(self.strvar_total_item_redondo.get(), "0"))

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_presup.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_presup.get())

        if retorno_VerFal == "":
            self.strvar_fecha_presup.set(value=estado_antes)
            self.entry_fecha_presup.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_presup.set(value=estado_antes)
            self.entry_fecha_presup.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_presup.set(value=retorno_VerFal)
        return ("bien")

    # ------------------------------------------------------------------------
    # INFORMES
    # ------------------------------------------------------------------------

    def creopdfext(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_tvw_resupresup.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_resupresup.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # ==================================================================================
        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """
        # esto siempre debe estar ----------------------------------------------------------
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 12)
        # ----------------------------------------------------------------------------------
        # ==================================================================================

        # Cargo la linea del treeview de resu_presu ---------------------------------------
        valores = self.grid_tvw_resupresup.item(self.selected, 'values')

        # sdf = datetime.strptime(valores[1], '%Y-%m-%d')
        # feac = sdf.strftime('%d-%m-%Y')

        # armado de encabezado ------------------------------------------------------------
        fecha_presup = valores[1]
        self.pdf_numero_presupuesto   = valores[0]
        self.pdf_nombre_cliente       = valores[2]
        self.pdf_dolar_presupuesto    = valores[3]
        self.pdf_tasa_ganancia        = valores[4]
        self.pdf_total_presup_redondo = valores[6]

        # Traigo, si es que hay, el detalle extenso del producto presupuestado de la tabla resu_presup
        datos_resupresup = self.varPresupuestos.traer_resu_presup(self.pdf_numero_presupuesto)
        self.pdf_detalle = datos_resupresup[13]

        # Encabezado
        self.pdf_datos_encabezado_orden = '('+self.pdf_numero_presupuesto+') - '+self.pdf_nombre_cliente
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Fecha: ' + fecha_presup + '  -  Numero Presupuesto ' + self.pdf_datos_encabezado_orden,
                 border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.cell(w=100, h=5, txt="Item", border=1, align='C', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="IVA", border=1, align='R', fill=0, ln=0)
        pdf.cell(w=10, h=5, txt="Cant", border=1, align='R', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="Neto Dolar", border=1, align='R', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="Bruto pesos", border=1, align='R', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="Final", border=1, align='R', fill=0, ln=0)
        pdf.multi_cell(w=0, h=5, txt="Total", border=1, align='R', fill=0)

        pdf.cell(w=0, h=2, txt="", border=0, align='C', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items_presupuesto = self.varPresupuestos.traer_deta_presup(self.pdf_numero_presupuesto)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 8)
        total_presupuesto = 0

        for row in self.items_presupuesto:

            # calculos ----------------------------------------------------------
            bruto_dolar = round((row[6] * float(row[7])) * (1+(float(row[5])/100)), 2)
            sumo_precio_final_conganancia = round((bruto_dolar * float(self.strvar_valor_dolar_hoy.get())) * (1+(float(self.pdf_tasa_ganancia)/100)), 2)
            total_presupuesto += sumo_precio_final_conganancia

            # Descripcion item
            pdf.cell(w=100, h=5, txt=row[4], border=0, align='L', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(row[5]), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=10, h=5, txt=str(row[6]), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(bruto_dolar, 2))), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
            pdf.multi_cell(w=0, h=5, txt=str(formatear_cifra(row[8])), border=0, align='R', fill=0)
            #pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Impresion del detalle extenso ---------------------------------------------------
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Detalle: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_detalle, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        # Total final --------------------------------------------------------------------
        total_presupuesto = formatear_cifra(total_presupuesto)
        total_redondo = formatear_cifra(round(float(self.pdf_total_presup_redondo), 2))
        #pdf.cell(w=0, h=5, txt="Total: " + str(total_presupuesto), border=0, align='R', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt="Total: " + str(total_redondo), border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        try:
            pdf.output('hoja.pdf')
        except:
            messagebox.showinfo("Error", "Verifique listados abiertos en otras terminales", parent=self)
            return

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    def creopdfint(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_tvw_resupresup.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_resupresup.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # ==================================================================================
        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """
        # esto siempre debe estar ----------------------------------------------------------
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 12)
        # ----------------------------------------------------------------------------------
        # ==================================================================================

        # Cargo la linea del treeview de resu_presu ---------------------------------------
        valores = self.grid_tvw_resupresup.item(self.selected, 'values')

        # # armado de encabezado ------------------------------------------------------------
        # forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'))

        # sdf = datetime.strptime(valores[1], '%Y-%m-%d')
        # fecha_presup = sdf.strftime('%d-%m-%Y')
        fecha_presup = valores[1]
        self.pdf_numero_presupuesto =   valores[0]
        self.pdf_nombre_cliente =       valores[2]
        self.pdf_dolar_presupuesto =    valores[3]
        self.pdf_tasa_ganancia =        valores[4]
        self.pdf_total_presup_redondo = valores[6]

        # Traigo, si es que hay, el detalle extenso del producto presupuestado de la tabla resu_presup
        datos_resupresup = self.varPresupuestos.traer_resu_presup(self.pdf_numero_presupuesto)
        self.pdf_detalle = datos_resupresup[13]

        # Encabezado
        self.pdf_datos_encabezado_orden = '('+self.pdf_numero_presupuesto+') - '+self.pdf_nombre_cliente
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Fecha: ' + fecha_presup + '  -  Numero Presupuesto ' + self.pdf_datos_encabezado_orden,
                 border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.set_font('Arial', '', 7)
        pdf.cell(w=100, h=5, txt="Item", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=10, h=5, txt="IVA", border=1, align='R', fill=0, ln=0)
        pdf.cell(w=5, h=5, txt="Ct", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=10, h=5, txt="BDU", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=17, h=5, txt="BPT", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=17, h=5, txt="Final", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=17, h=5, txt="Ganancia", border=1, align='C', fill=0, ln=0)
        pdf.multi_cell(w=0, h=5, txt="Redondo", border=1, align='R', fill=0)
        #pdf.cell(w=20, h=5, txt="Redondeo", border=1, align='R', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items_presupuesto = self.varPresupuestos.traer_deta_presup(self.pdf_numero_presupuesto)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 7)

        # Sumatoria totales finales
        total_presupuesto = 0
        total_ganancia = 0
        total_costo_dolar = 0
        total_costo_pesos = 0

        for row in self.items_presupuesto:

            # calculos ----------------------------------------------------------

            # costo total bruto en dolar
            # cantidad * precio neto dolar * 1.105 0 1.21
            bruto_dolar = round((row[6] * float(row[7])) * (1+(float(row[5])/100)), 2)
            # sumarizo el costo en dolares bruto c/iva
            total_costo_dolar += bruto_dolar

            # costo total Bruto en pesos c/iva
            # (cantidad * neto_dolar) * dolar_presupuesto * (1+(tasa_iva/100))
            # bruto_pesos = round(((row[6] * float(row[7])) * float(self.pdf_dolar_presupuesto)) * (1+(float(row[5])/100)), 2)
            bruto_pesos = round((bruto_dolar * float(self.pdf_dolar_presupuesto)), 2)
            # sumarizo el costo bruto pesos (c/iva)
            total_costo_pesos += bruto_pesos

            # calculo y sumarizo la ganancia
            item_ganancia = round(bruto_pesos * (float(self.pdf_tasa_ganancia) / 100), 2)
            total_ganancia += item_ganancia

            # costo bruto * (1+(tasa_ganancia/100))
            sumo_precio_final_conganancia = round(bruto_pesos * (1+(float(self.pdf_tasa_ganancia)/100)), 2)
            total_presupuesto += sumo_precio_final_conganancia

            # Descripcion item
            pdf.cell(w=100, h=5, txt=row[4], border=0, align='L', fill=0, ln=0)
            pdf.cell(w=10, h=5, txt=str(row[5]), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=5, h=5, txt=str(row[6]), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=10, h=5, txt=str(formatear_cifra(row[7] * (1+(row[5]/100)))), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=10, h=5, txt=str(formatear_cifra(bruto_dolar)), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=17, h=5, txt=str(formatear_cifra(bruto_pesos)), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=17, h=5, txt=str(formatear_cifra(sumo_precio_final_conganancia)), border=0, align='R', fill=0)
            pdf.cell(w=17, h=5, txt=str(formatear_cifra(item_ganancia)), border=0, align='R', fill=0)
            pdf.multi_cell(w=0, h=5, txt=str(row[8]), border=0, align='R', fill=0)
            #pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # Impresion linea final de totales ------------------------------------------------
        total_ganancia = formatear_cifra(total_ganancia)
        total_costo_dolar = formatear_cifra(total_costo_dolar)
        total_costo_pesos = formatear_cifra(total_costo_pesos)

        pdf.set_font('Courier', 'B', 8)

        pdf.cell(w=0, h=5, txt='* Dolar: '+self.pdf_dolar_presupuesto+' - Total Ganancia: '+str(total_ganancia)+
                               ' Costo Dolar: '+str(total_costo_dolar)+' Costo pesos: '+str(total_costo_pesos),
                                align='L', border=1, fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # Impresion del detalle extenso ---------------------------------------------------
        pdf.set_font('Courier', 'B', 8)
        pdf.cell(w=0, h=5, txt='* Detalle: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 8)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_detalle, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        # Total final --------------------------------------------------------------------
        total_presupuesto = formatear_cifra(round(total_presupuesto, 2))
        total_redondo = formatear_cifra(round(float(self.pdf_total_presup_redondo), 2))
        pdf.cell(w=0, h=5, txt="Total: " + str(total_presupuesto), border=0, align='R', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt="Redondo: " + str(total_redondo), border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        try:
            pdf.output('hoja.pdf')
        except:
            messagebox.showinfo("Error", "Verifique listados abiertos en otras terminales", parent=self)
            return

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    # -------------------------------------------------------------
    # VARIAS
    # -------------------------------------------------------------

    def traer_dolarhoy(self):
        dev_informa = self.varPresupuestos.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])

    # --------------------------------------------------------------
    # SEL CLIENTE
    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
        en que campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """  Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de 
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                                                        "direccion", "Apellido y nombre", "Codigo",
                                                        "Direccion", que_busco, "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:
            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])
            self.strvar_sit_fiscal.set(value=item[11])
            self.strvar_cuit.set(value=item[12])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # --------------------------------------------------------------------
    # SEL ARTICULO

    def fBusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(codbar, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.strvar_componente.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.varFuncion_new.ventana_selec("articulos", "descripcion", "codigo",
                                                        "costodolar", "Descripcion", "Codigo",
                                                        "Precio dolar neto", que_busco,
                                                        "Orden: Rubro+Marca+Descripcion", "S")

        for item in valores_new:

            self.strvar_componente.set(value=item[2]) # d<escripcion del articulo
            self.strvar_combo_tasa_iva.set(value=item[7])
            self.strvar_neto_dolar.set(value=item[6])

        self.entry_componente.focus()
        self.entry_componente.icursor(tk.END)

    def fCerrar5(self):

        self.pantalla_detalle.destroy()
        self.master.grab_set()
        self.master.focus_set()

    def fVerArticulos(self):

        vent = Toplevel()
        vent.title("ABM Articulos")
        # Asigno la clase Ventart que esta en articulos.py a la variable app
        app = VentArt(vent)
        app.mainloop()

    def fDetalle_precio_articulo(self):

        # PANTALLA FLOTANTE DETALLE PRECIO DEL ARTICULO

        self.pantalla_detalle = Toplevel()

        self.pantalla_detalle.protocol("WM_DELETE_WINDOW", self.fCerrar5)
        self.pantalla_detalle.geometry('580x260+600+400')
        self.pantalla_detalle.config(bg='#27BEF5', padx=5, pady=5)
        # ayuesizable(0,0)
        self.pantalla_detalle.resizable(1, 1)
        self.pantalla_detalle.title("Detalle precio del articulo")
        self.pantalla_detalle.focus_set()
        self.pantalla_detalle.grab_set()
        self.pantalla_detalle.transient(master=self.master)

        self.frame_detalle_articulo=LabelFrame(self.pantalla_detalle, text="", foreground="#CF09BD")

        # -------------------------------------------------------------------
        # DOLARES

        # DOLARES Precio neto
        lbl_neto_dolar_articulo=Label(self.frame_detalle_articulo,
        text=f"DOLARES - Costo neto x unidad: U$S {self.strvar_neto_dolar.get()} - "
             f"Total costo neto: U$S"
             f" {float(self.strvar_neto_dolar.get())*float(self.strvar_cantidad_vendida.get())}")
        lbl_neto_dolar_articulo.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        # DOLARES Importe del IVA
        self.iva_en_dolares = round(float(self.strvar_neto_dolar.get()) * (float(self.strvar_combo_tasa_iva.get()) / 100), 2)

        lbl_iva_dolar_articulo=Label(self.frame_detalle_articulo,
        text=f"DOLARES - Importe IVA x unidad: U$S {self.iva_en_dolares} - "
             f"Total IVA: U$S {self.iva_en_dolares * float(self.strvar_cantidad_vendida.get())}")
        lbl_iva_dolar_articulo.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # DOLARES Precio Bruto (con VIA)
        lbl_bruto_dolar_articulo=Label(self.frame_detalle_articulo,
        text=f"DOLARES - Costo bruto x unidad: U$S {self.iva_en_dolares+float(self.strvar_neto_dolar.get())} - "
             f"Total costo bruto: U$S "
             f"{float(self.strvar_cantidad_vendida.get()) * (self.iva_en_dolares+float(self.strvar_neto_dolar.get()))}")
        lbl_bruto_dolar_articulo.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        # ------------------------------------------------------------------
        # PESOS

        # PESOS Precio neto
        lbl_neto_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Costo neto x unidad: $ {self.strvar_costo_neto_pesos_unidad.get()} - "
             f"Total costo neto: $ {self.strvar_costo_neto_pesos_xcanti.get()}")
        lbl_neto_pesos_articulo.grid(row=3, column=0, padx=5, pady=2, sticky="w")

        # PESOS Importe del IVA
        self.iva_en_pesos = round(float(self.strvar_costo_neto_pesos_unidad.get()) * (float(self.strvar_combo_tasa_iva.get()) / 100), 2)

        lbl_iva_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Importe IVA x unidad: $ {self.iva_en_pesos} - "
             f"Total IVA: $ {self.iva_en_pesos * float(self.strvar_cantidad_vendida.get())}")
        lbl_iva_pesos_articulo.grid(row=4, column=0, padx=5, pady=2, sticky="w")

        # PESOS Precio Bruto (con VIA)
        lbl_bruto_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Costo bruto x unidad: $ {self.iva_en_pesos+float(self.strvar_costo_neto_pesos_unidad.get())} - "
             f"Total costo bruto: $ "
             f"{float(self.strvar_cantidad_vendida.get()) * (self.iva_en_pesos+float(self.strvar_costo_neto_pesos_unidad.get()))}")
        lbl_bruto_pesos_articulo.grid(row=5, column=0, padx=5, pady=2, sticky="w")

        # GANANCIA PESOS
        importe_ganancia_unidad =round(float(self.strvar_costo_bruto_pesos_unidad.get()) * (float(self.strvar_tasa_ganancia.get()) / 100), 2)
        importe_ganancia_total = importe_ganancia_unidad * float(self.strvar_cantidad_vendida.get())
        lbl_ganancia_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Ganancia: % {self.strvar_tasa_ganancia.get()} - "
             f"Importe ganancia x unidad: "
             f"{importe_ganancia_unidad} - "
             f"Total Importe ganancia: "
             f"{importe_ganancia_total}")
        lbl_ganancia_pesos_articulo.grid(row=6, column=0, padx=5, pady=2, sticky="w")

        # PRECIO VENTA FINAL EN PESOS
        precio_venta_final_unidad = round(float(self.strvar_costo_bruto_pesos_unidad.get()) * (1 + (float(self.strvar_tasa_ganancia.get()) / 100)), 2)
        precio_venta_final_total = round(precio_venta_final_unidad * float(self.strvar_cantidad_vendida.get()), 2)

        lbl_precio_pesos_venta_final=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Precio venta final x unidad: {precio_venta_final_unidad} - "
             f"Precio venta final: {precio_venta_final_total} - Redondeo: {self.strvar_total_item_redondo.get()}")
        lbl_precio_pesos_venta_final.grid(row=7, column=0, padx=5, pady=2, sticky="w")

        self.frame_detalle_articulo.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)

        self.btn_volver_pantalla = Button(self.frame_detalle_articulo, text="Volver", command=self.fCerrar5, width=22,
                                    bg="blue", fg="white")
        self.btn_volver_pantalla.grid(row=8, column=0, padx=10, pady=2, sticky="nsew")

        self.pantalla_detalle.mainloop()

    def puntero_busqueda(self,registro):

        """ # registro = Viene en blanco
            # regis = Indice del registro en el treeview tabla "I00E1", "I00F".......
            # (rg) = Es el iterante dentro de regis, esta el "Index" del Treeview (I00E, I00F...) """

        regis = self.grid_tvw_resupresup.get_children()
        rg = ""

        if regis != ():
            for rg in regis:
                break
            if rg == "":
                self.btn_buscar.configure(state="disabled")
                return



    # def muevo_el_puntero_resu(self, posicion):
    #
    #     # Entonces, "rg" es el Text o Index del registro en el Treeview y ahi posiciono el foco con las
    #     # siguientes instrucciones
    #     self.grid_tvw_resupresup.selection_set(posicion)
    #     # Para que no me diga que no hay nada seleccionado
    #     self.grid_tvw_resupresup.focus(posicion)
    #     # para que la linea seleccionada no me quede fuera del area visible del treeview
    #     self.grid_tvw_resupresup.yview(self.grid_tvw_resupresup.index(posicion))
    #     return



    # ----------------------------------------------------------------------------------------
    # MOVIMIENTO DEL PUNTERO PARA EL TREEVIEW DE RESUPRESUP - RESUMENES DE PRESUPUESTO
    # ----------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------------
    # ALTAS

    # def puntero_altas(self, registro):
    #
    #     """ # registro: Trae el CODIGO DE CLIENTE que le asigne solo en altas y modificaciones.
    #         # regis = Indice del registro del treeview ('IA18', 'IA19', 'IA1A', 'IA1B', 'IA1C', 'IA1D', .....
    #         # rg = Iterante dentro de regis """
    #
    #     regis = self.grid_tvw_resupresup.get_children()
    #     rg = ""
    #
    #     for rg in regis:
    #         # mueve toda la lina de datos del treeview a la variable buscado
    #         buscado = self.grid_tvw_resupresup.item(rg)['values']
    #         if str(buscado[0]) == registro:
    #             # el buscado[0] tiene el codigo de cliente, el cual comparo con el que viene en registro
    #             break
    #
    #     self.muevo_el_puntero_resu(rg)
    #
    # # ----------------------------------------------------------------------------------------
    # # BORRAR
    #
    # def puntero_borrar(self, registro):
    #
    #     # ELIMINAR REGISTRO PARTE 1
    #     """ # registro = Aqui trae el index Id del treview ('IA18', 'IA19', 'IA1A', 'IA1B', .....Aqui seria (self.selected)
    #         # regis = Indice del registro en el treeview tabla "I00E1", "I00F".......
    #         # (rg) = Es el iterante dentro de regis, esta el "Index" del Treeview (I00E, I00F...) """
    #
    #     regis = self.grid_tvw_resupresup.get_children()
    #     rg = ""
    #
    #     """ ELIMINAR REGISTRO PARTE 1 -es la parte donde tomo el Id del registro que le sigue al que voy a eliminar
    #         control = variable que uso para cuando (rg sea igual a registro) salir del for """
    #
    #     control = 1
    #     # lista = guardo los Id del treeview ('IA18', 'IA19', 'IA1A', 'IA1B', .....
    #     lista = [""]
    #     # buscado2 = Guarda el Id de la Tabla (1,2,3...) del registro siguiente al que vamos a eliminar
    #     self.buscado2 = ""
    #     for rg in regis:
    #         # Ingreso cada elemento de la lista regis('IA18', 'IA19', 'IA1A', 'IA1B', .....
    #         lista.append(rg)
    #         if control == 0:
    #             # buscado =
    #             buscado = self.grid_tvw_resupresup.item(rg)['values']
    #             # buscado2 = Id de la tabla clientes(1,2,3,4.......
    #             self.buscado2 = str(buscado[0])
    #             # ---------------------------------------------------------------------------------------
    #             # esto agregue para que no se me mueva el puntero al posterior registro del treeview
    #             xxx = len(lista) - 2
    #             x_rg = lista[xxx]
    #             self.grid_tvw_resupresup.selection_set(x_rg)
    #             self.grid_tvw_resupresup.focus(x_rg)
    #             self.grid_tvw_resupresup.yview(self.grid_tvw_resupresup.index(x_rg))
    #             # -------------------------------------------------------------------------------------
    #             break
    #         if rg == registro:
    #             control = 0
    #     return
    #
    # def puntero_borrar2(self, registro):
    #
    #     """ # ELIMINAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id del que obtuve antes
    #           que es el que sigue al que borre
    #         # --------------------------------------------------------------------------------
    #         # registro = (parametro de la funcion-self.selected del treeview), esta vez trae el
    #         # index del treeview (I00E, I00F,...) del siguiente al que quiero eliminar.
    #         # regis = Indice del registro en el treeview tabla "I00E1", "I00F".......
    #         # (rg) = Es el iterante dentro de regis, esta el "Index" del Treeview (I00E, I00F...) """
    #
    #     regis = self.grid_tvw_resupresup.get_children()
    #     rg = ""
    #
    #     for rg in regis:
    #
    #         """ # rg = Es el iterante dentro de regis, esta el "Index" del Treeview (I00E, I00F...)
    #             # buscado = Es la lista de los valores de la fila del treeview del que le sigue al que se va a eliminar
    #             # buscado[0] = es el primer valor de la lista, o sea el Id del registro de la tabla (1,2,3...)
    #             # ojo, buscado 2 conserva el vaalor que se le asigno en eliminar parte 1 """
    #
    #         buscado = self.grid_tvw_resupresup.item(rg)['values']
    #         if self.buscado2 == str(buscado[0]):
    #             break
    #
    #     self.muevo_el_puntero_resu(rg)
