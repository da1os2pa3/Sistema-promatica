import os
# ---------------------------------------------------
from articulos_ABM import *
from funciones import *
from funcion_new import *
# ---------------------------------------------------
import tkinter.font as tkFont
from tkinter import messagebox, filedialog
# ---------------------------------------------------
from datetime import date, datetime
from PIL import Image, ImageTk

class VentArt(Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master

        # ---------------------------------------------------------------------------------
        # Seteo pantalla master principal
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # Instanciaciones
        # Creo el objeto - clase definida en articulos_ABM.py
        self.varArtic = datosArtic(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ---------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)

        # -----------------------------------------------------------------------------
        # POSICIONAMIENTO VENTANA -*-

        """ Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1120
        hventana = 625
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # ---------------------------------------------------------------------------
        # SETEO INICIAL DEL GRID
        # ---------------------------------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        . Otras funciones para manejar los elementos seleccionados incluyen:
          -selection_add(): añade elementos a la selección.
          -selection_remove(): remueve elementos de la selección.
          -selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
          -selection_toggle(): cambia la selección de un elemento.
        # Carga del Treeview y seteo de foco y punteros sobre el mismo (grid) """

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_articulos.identify_row(0)
        # self.grid_articulos.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_articulos.focus(item)
        # -------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # WIDGETS -*-
    # ------------------------------------------------------------------------------

    def create_widgets(self):

        # ------------------------------------------------------------------------------
        # VARIABLES -*-
        # ------------------------------------------------------------------------------

        # para la funcion validate y controlar campos solo numericos
        vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # -------------------------------------------------------------------------------------
        # IMAGENES Y CARPETAS DE FOTOS DE ARTICULOS -*-
        # -------------------------------------------------------------------------------------

        self.imagen_defa = "tapiz.jpg"
        # Carpetas de trabajo
        self.carpeta_principal = os.path.dirname(__file__)
        # Debe existir la carpeta 'fotos' en la carpeta donde este el sistema
        self.carpeta_fotos = os.path.join(self.carpeta_principal, "fotos")
        # Verifico que existan carpetas
        if os.path.isfile(self.carpeta_fotos):
            messagebox.showerror("Error", "No existe carpeta de fotos")
            return
        # --------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------
        # TITULOS -*-
        # --------------------------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('productos.png')
        self.photo3 = self.photo3.resize((75, 75), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_articulos = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_articulos = Label(self.frame_titulo_top, image=self.png_articulos, bg="red", relief=RIDGE, bd=5)
        self.lbl_titulo = Label(self.frame_titulo_top, width=30, text="Articulos", bg="black", fg="gold",
                                font=("Arial bold", 38, "bold"), bd=5, relief=RIDGE, padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_articulos.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill=X, padx=5, pady=5)
        # ---------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------
        # STRINGVARS -*-
        # ---------------------------------------------------------------------------------------

        self.strvar_codigo = tk.StringVar(value="")
        self.strvar_descripcion = tk.StringVar(value="")
        self.strvar_marca = tk.StringVar(value="")
        self.strvar_rubro = tk.StringVar(value="")
        self.strvar_codbar = tk.StringVar(value="")
        self.strvar_observa = tk.StringVar(value="")
        self.strvar_fechaultact = tk.StringVar(value="")
        self.strvar_costo_historico = tk.StringVar(value="0.00")
        self.strvar_imagen_Art = tk.StringVar(value="")

        self.strvar_buscar_articulo = tk.StringVar(value="")

        self.strvar_costo_neto_dolar = tk.StringVar(value="0.00")
        self.costo_neto_dolar_comparado = tk.StringVar(value="0")
        self.strvar_costo_neto_pesos = tk.StringVar(value="0.00")
        self.strvar_tasa_iva = tk.StringVar(value="0.00")
        self.strvar_total_iva = tk.StringVar(value="0.00")
        self.strvar_tasa_impint = tk.StringVar(value="0.00")
        self.strvar_total_impint = tk.StringVar(value="0.00")
        self.strvar_subtotal = tk.StringVar(value="0.00")
        self.strvar_tasa_ganancia = tk.StringVar(value="0.00")
        self.strvar_total_ganancia = tk.StringVar(value="0.00")
        self.strvar_total_precio_venta = tk.StringVar(value="0.00")
        self.strvar_total_precio_venta_mas10 = tk.StringVar(value="0.00")
        self.strvar_costo_dolar_bruto = tk.StringVar(value="0.00")
        self.strvar_costo_pesos_bruto = tk.StringVar(value="0.00")
        self.strvar_recargo_tarjeta = tk.StringVar(value="0.00")

        self.strvar_dolar_actual = tk.StringVar()
        # -------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------
        #  BOTONES -*-
        # ---------------------------------------------------------------------------------------

        # LabelFrame para colocar los botones
        barra_botones = LabelFrame(self.master)

        botones1 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        # Instalacion botones
        self.btn_nuevo=Button(botones1, text="Nuevo", command=self.fNuevo, bg="blue", fg="white", width=14)
        self.btn_nuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        self.btn_editar=Button(botones1, text="Editar", command=self.fEditar, bg="blue", fg="white", width=14)
        self.btn_editar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        self.btn_eliminar=Button(botones1, text="Eliminar", command=self.fEliminar, bg="red", fg="white", width=14)
        self.btn_eliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        self.btn_guardar=Button(botones1, text="Guardar", command=self.fGuardar, bg="green", fg="white", width=14)
        self.btn_guardar.grid(row=3, column=0, padx=5, pady=3, ipadx=10)
        self.btn_cancelar=Button(botones1, text="Cancelar", command=self.fCancelar, bg="black", fg="white", width=14)
        self.btn_cancelar.grid(row=4, column=0, padx=5, pady=3, ipadx=10)

        botones1.pack(side="top", padx=3, pady=3, fill=Y)

        botones2 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        self.btn_orden_codigo = Button(botones2, text="Orden Rubro\nMarca-Descripcion", width=14,
                                       command=self.forden_codigo, bg="grey", fg="white")
        self.btn_orden_codigo.grid(row=5, column=0, padx=5, pady=3, ipadx=10)
        self.btn_orden_apellido = Button(botones2, text="Orden\n Marca-Descripcion", width=14,
                                         command=self.forden_descripcion, bg="grey", fg="white")
        self.btn_orden_apellido.grid(row=6, column=0, padx=5, pady=3, ipadx=10)
        self.btn_reset = Button(botones2, text="Reset", width=14, command=self.fReset, bg="black", fg="white")
        self.btn_reset.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btn_Toparch = Button(botones2, text="", image=self.photo4, command=self.fToparch, width=15, bg="grey",
                                 fg="white")
        self.btn_Toparch.grid(row=8, column=0, padx=5, pady=3, sticky="nsew")
        # ToolTip(self.btn_Toparch, msg="Ir a principio de archivo")

        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btn_Finarch = Button(botones2, text="", image=self.photo5, command=self.fFinarch, bg="grey", fg="white")
        self.btn_Finarch.grid(row=9, column=0, padx=5, pady=3, sticky="nsew")
        # ToolTip(self.btn_Finarch, msg="Ir al final del archivo")

        botones2.pack(side="top", padx=3, pady=3, fill="y")

        botones3 = LabelFrame(barra_botones, bd=2)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 40), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(botones3, text="Salir", image=self.photo3, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=10, column=0, padx=5, pady=3, sticky="nsew")

        botones3.pack(side="top", padx=3, pady=3, fill="y")

        botones4 = LabelFrame(barra_botones, bd=2)

        # VALOR DOLAR HOY - Aqui traigo de la tabla informa la cotizacion actual del dolar
        self.dev_informa = self.varArtic.consultar_informa()

        for row in self.dev_informa:
            self.strvar_dolar_actual.set(value=row[21])
            self.strvar_recargo_tarjeta.set(value=row[23])

        fff = tkFont.Font(family="Arial", size=11, weight="bold")
        self.lbl_cotiza_dolarhoy = Label(botones4, text="dolar Hoy:\n " + str(self.strvar_dolar_actual.get()),
                                         font=fff, foreground="BLUE")
        self.lbl_cotiza_dolarhoy.grid(row=12, column=0, padx=5, pady=3, sticky=S)

        # Pack barra botones
        botones4.pack(side="top", padx=3, pady=3, fill="y")
        # PACK - frame de botones
        barra_botones.pack(side="left", padx=5, pady=5, ipady=5, fill="y")
        # ---------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------
        # BUSQUEDAS -*-
        # ---------------------------------------------------------------------------------------

        self.frame_tv = Frame(self.master)
        # FRAME dentro del frame principal para poner la linea de busqueda
        self.frame_buscar = LabelFrame(self.frame_tv)

        # Combos de rubros
        self.strvar_bus_rubro = tk.StringVar(self.frame_buscar)
        self.combo_bus_rubro = ttk.Combobox(self.frame_buscar, textvariable=self.strvar_bus_rubro, state='readonly',
                                            width=20)
        self.combo_bus_rubro['value'] = self.varArtic.combo_input("ru_nombre", "rubros",
                                                                  "ru_nombre")
        self.combo_bus_rubro.grid(row=0, column=0, padx=3, pady=1, sticky=W)
        self.btn_reset_rubro=Button(self.frame_buscar, text="Reset", command=self.fResetrubro, width=5, bg='black',
                                    fg='white')
        self.btn_reset_rubro.grid(row=0, column=1, padx=3, pady=1, sticky=W)

        # combo marcas
        self.strvar_bus_marca = tk.StringVar(self.frame_buscar)
        self.combo_bus_marca = ttk.Combobox(self.frame_buscar, textvariable=self.strvar_bus_marca, state='readonly',
                                            width=20)
        self.combo_bus_marca['value'] = self.varArtic.combo_input("ma_nombre", "marcas","ma_nombre")
        self.combo_bus_marca.grid(row=0, column=2, padx=3, pady=1, sticky=W)
        self.btn_reset_marca=Button(self.frame_buscar, text="Reset", command=self.fResetmarca, width=5, bg='black',
                                    fg='white')
        self.btn_reset_marca.grid(row=0, column=3, padx=3, pady=1, sticky=W)

        # buscar un articulo
        self.lbl_buscar_articulo = Label(self.frame_buscar, text="Buscar: ")
        self.lbl_buscar_articulo.grid(row=0, column=4, padx=3, pady=2)
        self.entry_buscar_articulo=Entry(self.frame_buscar, textvariable=self.strvar_buscar_articulo, justify="left",
                                         width=31)
        self.entry_buscar_articulo.grid(row=0, column=5, padx=3, pady=2, sticky=W)
        self.btn_buscar_articulo = Button(self.frame_buscar, text="Filtrar", command=self.fBuscar_en_tabla,
                                          bg="CadetBlue", fg="white", width=16)
        self.btn_buscar_articulo.grid(row=0, column=6, padx=3, pady=2, sticky=W)
        self.btn_mostrar_todo=Button(self.frame_buscar, text="Mostrar Todo", command=self.fQuitarfiltros, width=17,
                                     bg='CadetBlue', fg='white')
        self.btn_mostrar_todo.grid(row=0, column=7, padx=3, pady=1, sticky=W)
        # ----------------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------------
        # TREEVIEWS -*-
        # ---------------------------------------------------------------------------------------

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tv)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_articulos = ttk.Treeview(self.frame_tv, height=11, columns=("col1", "col2", "col3", "col4", "col5",
                                                                              "col6", "col7", "col8", "col9", "col10",
                                                                              "col11", "col12"))

        self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        #self.grid_articulos.bind("<ButtonRelease-3>", self.muestradatos)

        self.grid_articulos.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_articulos.column("col1", width=100, anchor="w", minwidth=100)
        self.grid_articulos.column("col2", width=350, anchor="w", minwidth=350)
        self.grid_articulos.column("col3", width=110, anchor="center", minwidth=110)
        self.grid_articulos.column("col4", width=130, anchor="center", minwidth=130)
        self.grid_articulos.column("col5", width=80, anchor="e", minwidth=80)
        self.grid_articulos.column("col6", width=70, anchor="e", minwidth=70)
        self.grid_articulos.column("col7", width=100, anchor="center", minwidth=100)
        self.grid_articulos.column("col8", width=70, anchor="center", minwidth=70)
        self.grid_articulos.column("col9", width=60, anchor="center", minwidth=60)
        self.grid_articulos.column("col10", width=200, anchor="center", minwidth=200)
        self.grid_articulos.column("col11", width=100, anchor="center", minwidth=100)
        self.grid_articulos.column("col12", width=80, anchor="center", minwidth=80)
        #self.grid_articulos.column("col14", width=80, anchor="center", minwidth=150)

        self.grid_articulos.heading("#0", text="Id", anchor="center")
        self.grid_articulos.heading("col1", text="Codigo", anchor="w")
        self.grid_articulos.heading("col2", text="Descripcion", anchor="w")
        self.grid_articulos.heading("col3", text="Marca", anchor="center")
        self.grid_articulos.heading("col4", text="Rubro", anchor="center")
        self.grid_articulos.heading("col5", text="Pesos final", anchor="center")
        self.grid_articulos.heading("col6", text="Dolar neto", anchor="center")
        self.grid_articulos.heading("col7", text="Cod.Barras", anchor="center")
        self.grid_articulos.heading("col8", text="IVA", anchor="center")
        self.grid_articulos.heading("col9", text="% Ganancia", anchor="center")
        self.grid_articulos.heading("col10", text="Observaciones", anchor=W)
        self.grid_articulos.heading("col11", text="Fecha ultima Act.", anchor="center")
        self.grid_articulos.heading("col12", text="Costo Historico", anchor="center")
        #self.grid_articulos.heading("col14", text="Imagen", anchor="center")

        self.grid_articulos.tag_configure('oddrow', background='light grey')
        self.grid_articulos.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tv, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tv, orient=VERTICAL)
        self.grid_articulos.config(xscrollcommand=scroll_x.set)
        self.grid_articulos.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_articulos.xview)
        scroll_y.config(command=self.grid_articulos.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_articulos['selectmode'] = 'browse'

        # PACK - de el treeview y el FRAME tv
        self.frame_buscar.pack(side="top", fill=BOTH, expand=1, padx=5, pady=3)
        self. grid_articulos.pack(side= "top", fill=BOTH, expand=1, padx=5, pady=5)
        self.frame_tv.pack(side="top", fill="both", padx=5, pady=5)
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # ENTRYS -*-
        # ------------------------------------------------------------------------

        # FRAMES
        self.sector_entry = LabelFrame(self.master)
        self.sector_totales = LabelFrame(self.master)
        self.sector_imagen = LabelFrame(self.master)

        # CODIGO
        self.lbl_codigo = Label(self.sector_entry, text="Codigo: ")
        self.lbl_codigo.grid(row=0, column=0, padx=2, pady=1, sticky=W)
        self.entry_codigo = Entry(self.sector_entry, textvariable=self.strvar_codigo, justify="left", width=30)
        self.entry_codigo.grid(row=0, column=1, padx=2, pady=1, sticky='nsew')
        self.strvar_codigo.trace("w", lambda *args: self.limitador(self.strvar_codigo, 30))
        # DESCRIPCION
        self.lbl_descripcion = Label(self.sector_entry, text="Descripcion: ")
        self.lbl_descripcion.grid(row=1, column=0, padx=2, pady=1, sticky=W)
        self.entry_descripcion = Entry(self.sector_entry, textvariable=self.strvar_descripcion, justify="left",
                                       width=40)
        self.entry_descripcion.grid(row=1, column=1, padx=2, pady=1, sticky=W)
        self.strvar_descripcion.trace("w", lambda *args: self.limitador(self.strvar_descripcion, 150))
        # MARCA - COMBOBOX
        self.lbl_marca = Label(self.sector_entry, text="Marca: ")
        self.lbl_marca.grid(row=2, column=0, padx=2, pady=1, sticky=W)
        self.combo_marca = ttk.Combobox(self.sector_entry, textvariable=self.strvar_marca, state='readonly', width=40)
        self.combo_marca.grid(row=2, column=1, padx=2, pady=1, sticky=W)
        self.combo_marca['value'] = self.varArtic.combo_input("ma_nombre", "marcas", "ma_nombre")
        # RUBRO - COMBOBOX
        self.lbl_rubro = Label(self.sector_entry, text="Rubro: ")
        self.lbl_rubro.grid(row=3, column=0, padx=2, pady=1, sticky=W)
        self.combo_rubro = ttk.Combobox(self.sector_entry, textvariable=self.strvar_rubro, state='readonly', width=40)
        self.combo_rubro.grid(row=3, column=1, padx=2, pady=1, sticky=W)
        self.combo_rubro['value'] = self.varArtic.combo_input("ru_nombre", "rubros", "ru_nombre")
        # CODIGO DE BARRAS
        self.lbl_codbar = Label(self.sector_entry, text="Codigo Barras: ")
        self.lbl_codbar.grid(row=4, column=0, padx=2, pady=1, sticky=W)
        self.entry_codbar = Entry(self.sector_entry, textvariable=self.strvar_codbar, justify="left", width=30)
        self.entry_codbar.bind('<Tab>', lambda e: self.verif_existe())
        self.entry_codbar.grid(row=4, column=1, padx=2, pady=1, sticky=W)
        self.strvar_codbar.trace("w", lambda *args: self.limitador(self.strvar_codbar, 30))
        # OBSERVACIONES
        self.lbl_observa = Label(self.sector_entry, text="Observaciones: ")
        self.lbl_observa.grid(row=5, column=0, padx=2, pady=1, sticky=W)
        self.entry_observa = Entry(self.sector_entry, textvariable=self.strvar_observa, justify="left", width=40)
        self.entry_observa.grid(row=5, column=1, padx=2, pady=1, sticky=W)
        self.strvar_observa.trace("w", lambda *args: self.limitador(self.strvar_observa, 100))
        # FECHA DE ULTIMA ACTUALIZACION
        self.lbl_fechaultact = Label(self.sector_entry, text="Fecha ultima Act.: ")
        self.lbl_fechaultact.grid(row=6, column=0, padx=2, pady=1, sticky=W)
        self.entry_fechaultact = Entry(self.sector_entry, textvariable=self.strvar_fechaultact, justify="left",
                                       width=12)
        self.entry_fechaultact.grid(row=6, column=1, padx=2, pady=1, sticky=W)
        self.entry_fechaultact.bind("<FocusOut>", self.formato_fecha)
        #self.strvar_fechaultact.trace("w", lambda *args: self.limitador(self.strvar_fechaultact, 10))
        # COSTO HISTORICO
        self.lbl_costo_historico = Label(self.sector_entry, text="Costo Historico: ")
        self.lbl_costo_historico.grid(row=7, column=0, padx=2, pady=1, sticky=W)
        self.entry_costo_historico = Entry(self.sector_entry, textvariable=self.strvar_costo_historico, justify="right",
                                           width=15)
        self.entry_costo_historico.grid(row=7, column=1, padx=2, pady=1, sticky=W)
        self.entry_costo_historico.config(validate="key", validatecommand=vcmd)
        self.strvar_costo_historico.trace("w", lambda *args: self.limitador(self.strvar_costo_historico, 15))
        self.entry_costo_historico.bind('<Tab>', lambda e: self.calcular("nada"))

        # TOTALES ARRTICULOS

        # COSTO NETO EN DOLAR
        self.lbl_costo_neto_dolar = Label(self.sector_totales, text="Costo neto U$S:")
        self.lbl_costo_neto_dolar.grid(row=0, column=0, padx=2, pady=1, sticky=W)
        self.entry_costo_neto_dolar = Entry(self.sector_totales, textvariable=self.strvar_costo_neto_dolar,
                                            justify="right", width=15)
        self.entry_costo_neto_dolar.grid(row=0, column=1, padx=2, pady=1, sticky=W)
        self.entry_costo_neto_dolar.config(validate="key", validatecommand=vcmd)
        self.strvar_costo_neto_dolar.trace("w", lambda *args: self.limitador(self.strvar_costo_neto_dolar, 15))
        self.entry_costo_neto_dolar.bind('<Tab>', lambda e: self.calcular("dolar"))
        # COSTO NETO EN PESOS
        self.lbl_costo_neto_pesos = Label(self.sector_totales, text="Costo neto Pesos:")
        self.lbl_costo_neto_pesos.grid(row=1, column=0, padx=2, pady=1, sticky=W)
        self.entry_costo_neto_pesos = Entry(self.sector_totales, textvariable=self.strvar_costo_neto_pesos,
                                            justify="right", width=15)
        self.entry_costo_neto_pesos.grid(row=1, column=1, padx=2, pady=1, sticky=W)
        self.entry_costo_neto_pesos.config(validate="key", validatecommand=vcmd)
        self.strvar_costo_neto_pesos.trace("w", lambda *args: self.limitador(self.strvar_costo_neto_pesos, 15))
        self.entry_costo_neto_pesos.bind('<Tab>', lambda e: self.calcular("pesos"))
        # ALICUOTA TASA IVA y  TOTAL IVA
        self.lbl_tasa_iva = Label(self.sector_totales, text="% IVA:")
        self.lbl_tasa_iva.grid(row=2, column=0, padx=2, pady=1, sticky=W)
        self.combo_iva = ttk.Combobox(self.sector_totales, state="readonly", width=5)
        self.combo_iva['value'] = self.varArtic.combo_input("iva_alic", "alic_iva", "iva_alic")
        self.combo_iva.grid(row=2, column=1, padx=2, pady=1, sticky=W)
        self.strvar_total_iva.set(value="0.00")
        self.lbl_total_iva = Label(self.sector_totales, textvariable=self.strvar_total_iva, width=10, anchor='e')
        self.lbl_total_iva.grid(row=2, column=2, padx=2, pady=1, sticky='nsew')
        self.combo_iva.bind('<Tab>', lambda e: self.calcular("iva"))
        # TASA IMPUESTOS INTERNOS
        self.lbl_impint = Label(self.sector_totales, text="% Imp.Interno:")
        self.lbl_impint.grid(row=3, column=0, padx=2, pady=1, sticky=W)
        self.strvar_tasa_impint.set(value="0.00")
        self.strvar_total_impint.set(value="0.00")
        self.entry_tasa_impint = Entry(self.sector_totales, textvariable=self.strvar_tasa_impint, width=5,
                                       justify="right")
        self.entry_tasa_impint.grid(row=3, column=1, padx=2, pady=1, sticky=W)
        self.entry_tasa_impint.config(validate="key", validatecommand=vcmd)
        self.strvar_tasa_impint.trace("w", lambda *args: self.limitador(self.strvar_tasa_impint, 5))
        self.lbl_total_impint = Label(self.sector_totales, textvariable=self.strvar_total_impint, width=10, anchor='e')
        self.lbl_total_impint.grid(row=3, column=2, padx=2, pady=1, sticky='nsew')
        self.entry_tasa_impint.bind('<Tab>', lambda e: self.calcular("impint"))
        # SUBTOTAL COSTO CON IMPUESTOS ( BRUTO )
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_subtotal = Label(self.sector_totales, text="SubTotal:", font=fff, fg='green')
        self.lbl_subtotal.grid(row=5, column=1, padx=2, pady=1, sticky=W)
        self.strvar_subtotal.set(value="0.00")
        self.lbl_importe_subtotal = Label(self.sector_totales, textvariable=self.strvar_subtotal, fg='green', width=10,
                                          anchor='e')
        self.lbl_importe_subtotal.grid(row=5, column=2, padx=2, pady=1, sticky='nsew')
        # PORCIENTO GANANCIA
        self.lbl_tasa_ganancia = Label(self.sector_totales, text="% Ganancia:")
        self.lbl_tasa_ganancia.grid(row=6, column=0, padx=2, pady=1, sticky=W)
        self.strvar_tasa_ganancia.set(value="0.00")
        self.strvar_total_ganancia.set(value="0.00")
        self.entry_tasa_ganancia = Entry(self.sector_totales, textvariable=self.strvar_tasa_ganancia, width=8,
                                         justify="right")
        self.entry_tasa_ganancia.grid(row=6, column=1, padx=2, pady=1, sticky=W)
        self.entry_tasa_ganancia.config(validate="key", validatecommand=vcmd)
        self.strvar_tasa_ganancia.trace("w", lambda *args: self.limitador(self.strvar_tasa_ganancia, 6))
        self.lbl_total_ganancia = Label(self.sector_totales, textvariable=self.strvar_total_ganancia, width=10,
                                        anchor='e')
        self.lbl_total_ganancia.grid(row=6, column=2, padx=2, pady=1, sticky='nsew')
        self.entry_tasa_ganancia.bind('<Tab>', lambda e: self.calcular("porgan"))
        # TOTAL PRECIO DE VENTA PESOS ARTICULO
        fff = tkFont.Font(family="Arial", size=9, weight="bold")
        lbl_total_venta = Label(self.sector_totales, font=fff, text="Precio Venta: ", fg="blue")
        lbl_total_venta.grid(row=7, column=0, padx=2, pady=1, sticky=W)
        self.entry_total_precio_venta = Entry(self.sector_totales, textvariable=self.strvar_total_precio_venta,
                                              width=20, justify="right")
        self.entry_total_precio_venta.grid(row=7, column=2, padx=2, pady=1, sticky='nsew')
        self.entry_total_precio_venta.config(validate="key", validatecommand=vcmd)
        self.strvar_total_precio_venta.trace("w", lambda *args: self.limitador(self.strvar_total_precio_venta, 10))
        self.entry_total_precio_venta.bind('<Tab>', lambda e: self.calcular("totales"))
        fff = tkFont.Font(family="Arial", size=11, weight="bold")
        lbl_total_venta_grande = Label(self.sector_totales, font=fff, textvariable=self.strvar_total_precio_venta,
                                       fg="red")
        lbl_total_venta_grande.grid(row=8, column=0, padx=2, pady=1, sticky='nsew')
        # Total de venta mas el % de recargo por la venta con tarjeta
        lbl_total_venta_mas10 = Label(self.sector_totales, text="Tarjeta +10%: ", fg="blue")
        lbl_total_venta_mas10.grid(row=8, column=1, padx=2, pady=1, sticky=W)
        lbl_total_venta_grande_mas10 = Label(self.sector_totales, font=fff,
                                             textvariable=self.strvar_total_precio_venta_mas10, fg="red")
        lbl_total_venta_grande_mas10.grid(row=8, column=2, padx=2, pady=1, sticky=W)

        # COSTO DOLAR CON IMPUESTOS BRUTO
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.strvar_costo_dolar_bruto.set(value="0.00")
        self.lbltot_costo_dolar_bruto = Label(self.sector_totales, textvariable=self.strvar_costo_dolar_bruto, width=10,
                                              font=fff, fg='blue', anchor='e')
        self.lbltot_costo_dolar_bruto.grid(row=0, column=2, padx=2, pady=1, sticky='nsew')

        self.lbl_aclaracion1 = Label(self.sector_totales, text="c/Iva", fg='blue')
        self.lbl_aclaracion1.grid(row=0, column=3, padx=2, pady=1, sticky='nsew')

        # COSTO PESOS CON IMPUESTOS BRUTO
        self.strvar_costo_pesos_bruto.set(value="0.00")
        self.lbltot_costo_pesos_bruto = Label(self.sector_totales, textvariable=self.strvar_costo_pesos_bruto, width=10,
                                              font=fff, fg='blue', anchor='e')
        self.lbltot_costo_pesos_bruto.grid(row=1, column=2, padx=2, pady=1, sticky='nsew')

        self.lbl_aclaracion2 = Label(self.sector_totales, text="c/Iva", fg='blue')
        self.lbl_aclaracion2.grid(row=1, column=3, padx=2, pady=1, sticky='nsew')
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # PEDIDO IMAGEN ARTICULO -*-
        # ----------------------------------------------------------------------------

        # Nombre del archivo, no guarda la Ruta
        self.entry_imagen_art = Entry(self.sector_imagen, textvariable=self.strvar_imagen_Art, width=25)
        self.entry_imagen_art.bind('<Tab>', lambda e: self.validar_imagen())

        # Boton file dialogo (busqueda de archivo) va a carpeta fotos or default
        self.btn_ruta_imagen=Button(self.sector_imagen, text="Seleccione archivo", command=self.fBusco_archivo,
                                    width=20, bg='blue', fg='white')

        # muestra de la imagen
        # Viene en self.imagen.defa - "tapiz.jpg" por default definida en variables generales arriba
        self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
        self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.imagen_art = ImageTk.PhotoImage(self.photoa)
        # muestro la imagen en el frame
        self.lbl_imagen_art = Label(self.sector_imagen, image=self.imagen_art, bg="white", relief=RIDGE, bd=5)
        self.lbl_imagen_art.bind("<Double-Button-1>", self.amplia_img)

        # ------------------------------------------------------------------------
        # PACKS de estos tres ultimos
        self.entry_imagen_art.pack(expand=0, side="top", pady=3, padx=2)
        self.btn_ruta_imagen.pack(expand=0, side="top", pady=3, padx=2)
        self.lbl_imagen_art.pack(expand=1, side="top", fill="both", pady=2, padx=2)
        # ------------------------------------------------------------------------

        # PACKS GENERALES --------------------------------------------------------
        self.sector_entry.pack(expand=1, side="left", fill="both", pady=5, padx=2)
        self.sector_totales.pack(expand=1, side="left", fill="both", pady=5, padx=2)
        self.sector_imagen.pack(expand=1, side="left", fill="both", pady=5, padx=2)
        # ------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # GRID -*-
    # ----------------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_articulos.get_children():
            self.grid_articulos.delete(item)

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varArtic.consultar_articulo(self.filtro_activo)
        else:
            datos = self.varArtic.consultar_articulo("articulos ORDER BY rubro, marca, descripcion ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[11], '%Y-%m-%d'), "hora_no")

            precio_final_pesos = round(float((row[6]*(1+(row[7]/100))) * (1+(row[9]/100))) * float(self.strvar_dolar_actual.get()))

            self.grid_articulos.insert("", "end", tags=color, text=row[0], values=(row[1], row[2], row[3],
                                                    row[4], formatear_cifra(precio_final_pesos), row[6], row[5], row[7],
                                                    row[9], row[10], forma_normal, row[12], row[13]))

        if len(self.grid_articulos.get_children()) > 0:
            self.grid_articulos.selection_set(self.grid_articulos.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_articulos.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_articulos.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """

            if ult_tabla_id:
                """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """
                self.grid_articulos.selection_set(rg)
                # Para que no me diga que no hay nada seleccionado
                self.grid_articulos.focus(rg)
                # para que la linea seleccionada no me quede fuera del area visible del treeview
                self.grid_articulos.yview(self.grid_articulos.index(rg))
            else:
                # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
                self.mover_puntero_topend("END")

    # ------------------------------------------------------------------------
    # ESTADOS -*-
    # ------------------------------------------------------------------------

    def estado_inicial(self):

        # Variables
        self.filtro_activo = "articulos ORDER BY rubro, marca, descripcion ASC"
        self.var_Id = -1
        self.alta_modif = 0

        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_Btn_Oper("normal")
        self.habilitar_Btn_Final("disabled")

    def habilitar_text(self, estado):

        self.entry_codigo.configure(state=estado)
        self.entry_descripcion.configure(state=estado)
        self.combo_marca.configure(state=estado)
        self.combo_rubro.configure(state=estado)
        self.entry_codbar.configure(state=estado)
        self.entry_imagen_art.configure(state=estado)
        self.entry_costo_neto_dolar.configure(state=estado)
        self.entry_costo_neto_pesos.configure(state=estado)
        self.combo_iva.configure(state=estado)
        self.entry_tasa_impint.configure(state=estado)
        self.entry_tasa_ganancia.configure(state=estado)
        self.entry_total_precio_venta.configure(state=estado)
        self.entry_observa.configure(state=estado)
        self.entry_fechaultact.configure(state=estado)
        self.entry_costo_historico.configure(state=estado)
        self.btn_ruta_imagen.configure(state=estado)

        if self.alta_modif == 1:
            self.grid_articulos['selectmode'] = 'none'
            self.grid_articulos.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif == 2 or self.alta_modif == 0:
            self.grid_articulos['selectmode'] = 'browse'
            self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)

        # if estado == "disabled" or self.alta_modif == 2:
        #     self.grid_articulos['selectmode'] = 'browse'
        #     self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        # else:
        #     self.grid_articulos['selectmode'] = 'none'
        #     self.grid_articulos.bind("<Double-Button-1>", self.fNo_modifique)

    def limpiar_text(self):

        self.strvar_codigo.set(value="")
        self.strvar_descripcion.set(value="")
        self.strvar_codbar.set(value="")
        self.strvar_costo_neto_dolar.set(value="0.00")
        self.strvar_costo_neto_pesos.set(value="0.00")
        self.strvar_tasa_impint.set(value="0.00")
        self.strvar_tasa_ganancia.set(value="0.00")
        self.strvar_tasa_iva.set(value="0.00")
        self.strvar_observa.set(value="")
        self.strvar_fechaultact.set(value="")
        self.strvar_costo_historico.set(value="0.00")
        self.strvar_codbar.set(value="")
        self.strvar_observa.set(value="")
        self.strvar_imagen_Art.set(value="")
        self.strvar_total_iva.set(value="0.00")
        self.strvar_total_impint.set(value="0.00")
        self.strvar_subtotal.set(value="0.00")
        self.strvar_total_ganancia.set(value="0.00")
        self.strvar_total_precio_venta.set(value="0.00")
        self.strvar_total_precio_venta_mas10.set(value="0.00")
        self.strvar_costo_dolar_bruto.set(value="0.00")
        self.strvar_costo_pesos_bruto.set(value="0.00")
        self.strvar_buscar_articulo.set(value="")
        self.combo_marca.set("")
        self.combo_rubro.set("")
        self.combo_iva.set("")
        self.imagen_defa = "tapiz.jpg"
        self.recarga_imagen()

    def habilitar_Btn_Oper(self, estado):

        self.btn_nuevo.configure(state=estado)
        self.btn_eliminar.configure(state=estado)
        self.btn_editar.configure(state=estado)
        self.btn_Toparch.configure(state=estado)
        self.btn_Finarch.configure(state=estado)
        self.btn_orden_apellido.configure(state=estado)
        self.btn_orden_codigo.configure(state=estado)
        self.entry_buscar_articulo.configure(state=estado)
        self.btn_mostrar_todo.configure(state=estado)
        self.btn_buscar_articulo.configure(state=estado)
        self.combo_bus_marca.configure(state=estado)
        self.combo_bus_rubro.configure(state=estado)
        self.btn_reset_rubro.configure(state=estado)
        self.btn_reset_marca.configure(state=estado)

    def habilitar_Btn_Final(self, estado):

        self.btn_guardar.configure(state=estado)

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_inicial()
            # self.limpiar_text()
            # self.habilitar_Btn_Final("disabled")
            # self.habilitar_Btn_Oper("normal")
            # self.habilitar_text("disabled")

    def fReset(self):

        self.estado_inicial()
        self.fResetmarca()
        self.fResetrubro()
        self.limpiar_Grid()
        self.llena_grilla("")
        self.mover_puntero_topend("TOP")
        self.btn_nuevo.focus()
        # self.limpiar_text()
        # self.fQuitarfiltros()
        # self.habilitar_text("disabled")
        # self.habilitar_Btn_Final("disabled")
        # self.habilitar_Btn_Oper("normal")

    def DobleClickGrid(self, event):
        self.fEditar()

    def fNo_modifique(self, event):
        return "breack"

    def fSalir(self):
        self.master.destroy()

    # -----------------------------------------------------------------
    # CRUD -*-
    # -----------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.limpiar_text()
        self.habilitar_Btn_Final("normal")
        self.habilitar_Btn_Oper("disabled")

        self.combo_rubro.SelectedIndex = -1
        self.combo_rubro.set("")
        self.combo_marca.SelectedIndex = -1
        self.combo_marca.set("")
        self.combo_rubro.configure(state="readonly")
        self.combo_marca.configure(state="readonly")
        self.combo_iva.configure(state="readonly")
        self.combo_iva.current(0)

        # Cambio el formato de la fecha
        self.entry_fechaultact.insert(0, date.today().strftime('%d/%m/%Y'))
        self.entry_codigo.focus()

    def fEditar(self):

        """ self.selected = Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        * self.clave = Asi obtengo la clave de la base de datos campo Id que no es lo mismo que
        el otro (numero secuencial que pone la BD automaticamente al dar el alta. """

        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Editar", "No hay nada seleccionado", parent=self)
            return

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta
        self.alta_modif = 2

        self.habilitar_text('normal')
        self.limpiar_text()

        # --------------------------------------------
        # self.filtro_activo = "articulos WHERE Id = " + str(self.clave)
        """ para que permanezca mostrandose el filtro de busqueda actual luego de modificar el articulo que sea. 
        Por ejemplo: busco el cArtucho 133 y me muestra 10 registros, modifico uno de ellos y vuelvo al grid con 
        los mismo 10 aun seleccionados y filtrados"""

        self.filtro_edicion = "articulos WHERE Id = " + str(self.clave)
        valores = self.varArtic.consultar_articulo(self.filtro_edicion)
        # ---------------------------------------------

        for row in valores:

            self.strvar_codigo.set(value=row[1])
            self.strvar_descripcion.set(value=row[2])
            self.combo_marca.insert(0, row[3])
            self.combo_rubro.insert(0, row[4])
            self.combo_rubro.configure(state="readonly")
            self.combo_marca.configure(state="readonly")
            self.combo_iva.insert(0, row[7])
            self.combo_iva.configure(state="readonly")
            self.strvar_codbar.set(value=row[5])
            self.strvar_costo_neto_dolar.set(value=row[6])
            self.costo_neto_dolar_comparado.set(value=row[6]) # para ver si se cambio el precio y actualizar la fecha de ult. modif.
            self.strvar_tasa_impint.set(value=row[8])
            self.strvar_tasa_ganancia.set(value=row[9])
            self.strvar_observa.set(value=row[10])

            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[11], "%Y-%m-%d"), "hora_no")
            self.strvar_fechaultact.set(value=fecha_convertida)

            self.strvar_costo_historico.set(row[12])
            self.strvar_imagen_Art.set(value=row[13])

        # Recarga la imagen del producto
        self.recarga_imagen()

        self.habilitar_Btn_Final("normal")
        self.habilitar_Btn_Oper("disabled")

        # funcion que calcula los totales
        self.calcular('completo')
        self.entry_codigo.focus()

    def fEliminar(self):

        # selecciono el Id del GRID para su uso posterior
        self.selected = self.grid_articulos.focus()
        self.selected_ant = self.grid_articulos.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no son el mismo que el grid
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.clave_ant = self.grid_articulos.item(self.selected_ant, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_articulos.item(self.selected, 'values')
        data = "Id: "+str(self.clave)+" Nº: "+valores[0]+" Articulo: " + valores[4]

        r = messagebox.askquestion("Cuidado", "Confirma eliminar esta Orden?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Aviso", "Eliminacion cancelada", parent=self)
            return

        self.varArtic.eliminar_articulo(self.clave)

        messagebox.showinfo("Aviso", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # -----------------------------------------------------------------------------------
        # VALIDACIONES

        # 1 - Debe existir una descripcion-codigo de articulo-codigo de barras
        if self.strvar_descripcion.get() == "" or self.strvar_codigo.get() == "" or self.strvar_codbar.get() == "":
            messagebox.showwarning("Cuidado", "Deben existir Codigo, Descripcion y Codigo de Barras", parent=self)
            self.entry_descripcion.focus()
            return
        # ------------------------------------------------------------------------------------

        try:
            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
            self.selected = self.grid_articulos.focus()
            # Guardo Id del registro de la base datos _Tabla (no es el mismo del otro, este puedo verlo en la tabla) 1,2,3..
            self.clave = self.grid_articulos.item(self.selected, 'text')

            if self.alta_modif == 1:    #    #self.var_Id == -1:

                fecha_aux = datetime.strptime(self.strvar_fechaultact.get(), '%d/%m/%Y')
                self.varArtic.insertar_articulo(self.strvar_codigo.get(), self.strvar_descripcion.get(),
                                            self.combo_marca.get(), self.combo_rubro.get(), self.strvar_codbar.get(),
                                            self.strvar_costo_neto_dolar.get(), self.combo_iva.get(),
                                            self.strvar_tasa_impint.get(), self.strvar_tasa_ganancia.get(),
                                            self.strvar_observa.get(), fecha_aux, self.strvar_costo_historico.get(),
                                            self.strvar_imagen_Art.get())

                messagebox.showinfo("Guardar", "Nuevo registro creado correctamente", parent=self)

            elif self.alta_modif == 2:

                # Verifico que no haya cambiado el costo neto del dolar articulo, si es asi, cambio fecha de ultima modificacion
                if float(self.costo_neto_dolar_comparado.get()) != float(self.strvar_costo_neto_dolar.get()):
                    fecha_aux = datetime.today()
                else:
                    fecha_aux = datetime.strptime(self.strvar_fechaultact.get(), '%d/%m/%Y')

                self.varArtic.modificar_articulo(self.var_Id, self.strvar_codigo.get(), self.strvar_descripcion.get(),
                                                 self.combo_marca.get(), self.combo_rubro.get(),
                                                 self.strvar_codbar.get(), self.strvar_costo_neto_dolar.get(),
                                                 self.combo_iva.get(), self.strvar_tasa_impint.get(),
                                                 self.strvar_tasa_ganancia.get(),
                                                 self.strvar_observa.get(), fecha_aux,
                                                 self.strvar_costo_historico.get(), self.strvar_imagen_Art.get())

                self.var_Id == -1
                messagebox.showinfo("Modificacion", "La modificacion del registro fue exitosa", parent=self)

        except:

            messagebox.showerror("Error", "Revise datos ingresados por favor", parent=self)
            self.entry_descripcion.focus()
            return

        self.limpiar_Grid()
        self.limpiar_text()
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")

        #self.filtro_activo = "articulos ORDER BY rubro, marca, descripcion ASC"

        if self.alta_modif == 1:
            ultimo_tabla_id = self.varArtic.traer_ultimo(0)
            self.llena_grilla(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla(self.clave)

        self.alta_modif = 0

        # ojo este debe ir aca abajo sino da problema el browse del grid
        self.habilitar_text("disabled")

    # -----------------------------------------------------------------
    # VARIAS -*-
    # -----------------------------------------------------------------

    def fBusco_archivo(self):

        """ Esta funcion abre un dialogo para poder seleccionar el archivo imagen de articulo en el proceso de altas"""

        self.dev_ruta = self.varArtic.consultar_informa()

        self.strvar_ruta_fotos = StringVar(value="")

        for row in self.dev_informa:
            self.strvar_ruta_fotos.set(value=row[27])

        # Abro ventana dialogo en la ruta de las fotos
        self.file_ruta = filedialog.askopenfilename(initialdir="C:\\Proyectos_Python\\ABM_Clientes\\fotos",
                                                    title="Seleccione imagen", parent=self.master)
        # Guardo solo el nombre del archivo y no su ruta completa
        solo_nombre_archivo = os.path.basename(self.file_ruta)
        # asigno al stringvar el nombre del archivo - Si no selecciono, retorna
        if not solo_nombre_archivo:
            return
        self.strvar_imagen_Art.set(value=solo_nombre_archivo)

    def fResetrubro(self):
        self.combo_bus_rubro.set("")

    def fResetmarca(self):
        self.combo_bus_marca.set("")

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fechaultact.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fechaultact.get())

        if retorno_VerFal == "":
            self.strvar_fechaultact.set(value=estado_antes)
            self.entry_fechaultact.focus()
            return
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.entry_fechaultact.focus()
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fechaultact.set(value=estado_antes)
            self.entry_fechaultact.focus()
            return
        elif retorno_VerFal == "BLANCO":
            return
        else:
            self.strvar_fechaultact.set(retorno_VerFal)

    def verif_existe(self):

        """ Verifica que exista codigo de barras en el alta o modificacion del articulo """

        if self.alta_modif == 1:

            if len(self.entry_codbar.get()) > 0:

                se_busca = self.entry_codbar.get()
                que_busco = "articulos WHERE codbar = '" + se_busca + "'"
                retorno = self.varArtic.buscar_entabla(que_busco)

                if retorno != []:
                    # si encuentra el codigo de barras retorna y anula el alta
                    messagebox.showerror("Error", "Existe este codigo de barras en la Tabla", parent=self)
                    self.strvar_codbar.set(value="")
                    self.entry_codbar.focus()
                    return

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def recarga_imagen(self):

        """ Este lo usa el metodo de modificacion para cargar la imgen al editarlo, Tambien la usa "limpiartext" """

        try:

            # Borro u olvido el label anterior
            self.lbl_imagen_art.forget()
            # Regenero la imgaen del campo imgaen si existe nombre en la tabla, sino va default TAPIZ
            if len(self.strvar_imagen_Art.get()) != 0:
                self.imagen_defa = self.strvar_imagen_Art.get()
            else:
                self.imagen_defa = "tapiz.jpg"

            self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)
            self.lbl_imagen_art = Label(self.sector_imagen, image=self.imagen_art, bg="white", relief=RIDGE, bd=5)
            self.lbl_imagen_art.bind("<Double-Button-1>", self.amplia_img)

        except:

            messagebox.showerror("Error", "Revise nombre de imagen 'jpg'", parent=self)

        self.lbl_imagen_art.pack(expand=1, side=TOP, fill="both", pady=2, padx=2)

    def validar_imagen(self):

        """ Cuando doy alta y coloco el nombre de la imagen jpg, valido que exista en la carpeta fotos y ya la cargo
        y muestro """

        # Borro u olvido el label anterior
        self.lbl_imagen_art.forget()

        if len(self.strvar_imagen_Art.get()) != 0:
            self.imagen_defa = self.strvar_imagen_Art.get()
        else:
            self.imagen_defa = "tapiz.jpg"

        try:

            self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)

        except:

            messagebox.showerror("Error", "No existe la imagen", parent=self)

            self.imagen_defa = "tapiz.jpg"

            self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)

            self.strvar_imagen_Art.set(value="")
            self.entry_imagen_art.focus()

        # muestro la imagen en el frame
        self.lbl_imagen_art = Label(self.sector_imagen, image=self.imagen_art, bg="white", relief=RIDGE, bd=5)
        self.lbl_imagen_art.pack(expand=1, side=TOP, fill="both", pady=2, padx=2)

    def amplia_img(self,koko):

        if len(self.strvar_imagen_Art.get()) != 0:

            # crear toplevel con imagen grande
            self.vent_img = Toplevel()
            self.vent_img.geometry('420x500+1200+200')
            self.vent_img.config(bg='white', padx=5, pady=5)
            # ayuda_top.resizable(0,0)
            self.vent_img.resizable(1, 1)
            self.vent_img.title("Imagen ampliada")

            self.photo_b = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photo_b = self.photo_b.resize((300, 300), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art_b = ImageTk.PhotoImage(self.photo_b)

            # muestro la imagen en el frame
            self.lbl_im_art_b = Label(self.vent_img, image=self.imagen_art_b, bg="white", relief=RIDGE, bd=5)

            self.lbl_im_art_b.pack(expand=1, side=TOP, fill="both", pady=2, padx=2)
            self.vent_img.grab_set()
            self.vent_img.focus_set()

            mainloop()

    # -----------------------------------------------------------------
    # BUSQUEDAS -*-
    # -----------------------------------------------------------------

    def fBuscar_en_tabla(self):

        # verifico que venga algun string de busqueda para modificar el filtro_activo, si no lo dejo como estaba
        if self.combo_bus_rubro.get() == "" and self.combo_bus_marca.get() == "" and len(self.entry_buscar_articulo.get()) <= 0:
            messagebox.showinfo("Aviso", "Nada que buscar o  filtrar", parent=self)
            return

        try:

            c1 = 'rubro = ' + "'" + self.combo_bus_rubro.get() + "'"
            c2 = 'marca = ' + "'" + self.combo_bus_marca.get() + "'"

            self.filtro_activo = "articulos WHERE "

            # verificar combo rubros
            if self.combo_bus_rubro.get() == "" and self.combo_bus_marca.get() == "":

                if len(self.entry_buscar_articulo.get()) > 0:

                    se_busca = self.entry_buscar_articulo.get()

                    self.filtro_activo = self.filtro_activo + "INSTR(descripcion, '" + se_busca + "') > 0 OR "\
                                                              "INSTR(codigo, '" + se_busca + "') > 0 OR "\
                                                              "INSTR(codbar, '" + se_busca + "') > 0 ORDER BY rubro, marca, descripcion ASC"

            elif self.combo_bus_rubro.get() != "" and self.combo_bus_marca.get() == "":

                if len(self.entry_buscar_articulo.get()) > 0:

                    se_busca = self.entry_buscar_articulo.get()

                    self.filtro_activo = self.filtro_activo + c1 +" AND INSTR(descripcion, '" + se_busca + "') > 0 OR " + c1 + \
                                                              " AND INSTR(codigo, '" + se_busca + "') > 0 OR " + c1 + \
                                                              " AND INSTR(codbar, '" + se_busca + ("') > 0 "
                                                              "ORDER BY rubro, marca, descripcion ASC")
                else:

                    self.filtro_activo = self.filtro_activo + c1 + " ORDER BY rubro, marca, descripcion ASC"

            elif self.combo_bus_rubro.get() == "" and self.combo_bus_marca.get() != "":

                if len(self.entry_buscar_articulo.get()) > 0:

                    se_busca = self.entry_buscar_articulo.get()

                    self.filtro_activo = self.filtro_activo + c2 +" AND INSTR(descripcion, '" + se_busca + "') > 0 OR " + c2 + \
                                                              " AND INSTR(codigo, '" + se_busca + "') > 0 OR " + c2 + \
                                                              " AND INSTR(codbar, '" + se_busca + ("') > 0 "
                                                              "ORDER BY rubro, marca, descripcion ASC")

                else:

                    self.filtro_activo = self.filtro_activo + c2 + " ORDER BY rubro, marca, descripcion ASC"

            elif self.combo_bus_rubro.get() != "" and self.combo_bus_marca.get() != "":

                if len(self.entry_buscar_articulo.get()) > 0:

                    se_busca = self.entry_buscar_articulo.get()

                    self.filtro_activo = self.filtro_activo + c1 +' AND '+ c2 + " AND INSTR(descripcion, '" + se_busca + "') > 0 OR " + c1 +' AND '+ c2 +\
                                                              " AND INSTR(codigo, '" + se_busca + "') > 0 OR " + c1 +' AND '+ c2 +\
                                                              " AND INSTR(codbar, '" + se_busca + "') > 0 ORDER BY rubro, marca, descripcion ASC"
                else:

                    self.filtro_activo = self.filtro_activo + c1 + " AND " + c2 + " ORDER BY rubro, marca, descripcion ASC"

            self.varArtic.buscar_entabla(self.filtro_activo)
            self.limpiar_Grid()
            self.llena_grilla("")

            """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
            item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
            item = self.grid_articulos.selection()
            self.grid_articulos.focus(item)

        except:

            messagebox.showerror("Except_error", "Error de busqueda - Revise caracteres del texto a buscar", parent=self)
            self.entry_buscar_articulo.focus()
            return

    # -----------------------------------------------------------------
    # CALCULOS -*-
    # -----------------------------------------------------------------

    def calcular(self, que_campo):

        try:

            # Funcion que no permite pasar el valor ""
            if not self.control_blanco():
                self.entry_costo_historico.focus()
                return

            # reconstruye valores de variables a cero si es que borran el valor anterior y lo dejan en blanco en vez de cero
            self.control_valores()

            # Verifica que costos no esten en cero, porque sino da error el calculo de precio de venta final (divide zero)
            if que_campo != "nada":
                if float(self.strvar_costo_neto_dolar.get()) == 0 and float(self.strvar_costo_neto_pesos.get()) == 0:
                    messagebox.showwarning("Cuidado", "Debe colocar costo", parent=self)
                    self.entry_costo_neto_dolar.focus()
                    return

            if que_campo == "dolar":

                # Calulo el costo neto en dolar
                calc_pesos_neto = round((float(self.strvar_costo_neto_dolar.get()) * float(self.strvar_dolar_actual.get())), 2)
                self.strvar_costo_neto_pesos.set(value=str(round(float(calc_pesos_neto), 2)))

            elif que_campo == "nada":
                pass

            elif que_campo == "pesos":

                # Calculo el costo en pesos a partir del ingreso de pesos
                calc_dolar_neto = round((float(self.strvar_costo_neto_pesos.get()) / float(self.strvar_dolar_actual.get())), 2)
                self.strvar_costo_neto_dolar.set(value=str(round(float(calc_dolar_neto), 2)))

            elif que_campo == "iva":

                # Calculo el iva correspondiente segun la tasa seleccionada
                self.val1 = self.combo_iva.get()
                self.val2 = self.strvar_costo_neto_pesos.get()
                self.strvar_total_iva.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

            elif que_campo == "impint":

                # Calculo el Impuesto Interno
                self.val1 = self.strvar_tasa_impint.get()
                self.val2 = self.strvar_costo_neto_pesos.get()
                self.strvar_total_impint.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

            elif que_campo == "porgan":

                # Calculo el porcentaje de ganancia importe
                self.val1 = self.strvar_tasa_ganancia.get()
                self.val2 = self.strvar_subtotal.get()
                self.strvar_total_ganancia.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

            elif que_campo == "totales":

                # Aca es si cambio el total de venta en pesos
                # Debo recalcular el nuevo porc. % de ganancia y el importe de ganancia
                # Nuevo porcentaje ganancias
                self.val8 = round((((float(self.strvar_total_precio_venta.get()) -
                                     float(self.strvar_subtotal.get())) * 100) / float(self.strvar_subtotal.get())), 2)
                self.strvar_tasa_ganancia.set(value=str(self.val8))
                # Ahora recalculo el nuevo importe de la ganancia
                self.val1 = self.strvar_tasa_ganancia.get()
                self.val2 = self.strvar_subtotal.get()
                self.strvar_total_ganancia.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

                # calculo el precio de venta con el recargo por venta con tarjeta
                self.calc_total_ventas = float(self.strvar_total_precio_venta.get())
                self.calc_total_ventas_mas10 = self.calc_total_ventas * (
                            (float(self.strvar_recargo_tarjeta.get()) / 100) + 1)
                self.strvar_total_precio_venta_mas10.set(value=str(round(float(self.calc_total_ventas_mas10), 2)))
                return

            elif que_campo == "limp":

                # limpìa todos los campos al darle cancelar
                self.strvar_total_iva.set(value="0.00")
                self.strvar_subtotal.set(value="0.00")
                self.strvar_total_ganancia.set(value="0.00")
                self.strvar_costo_pesos_bruto.set(value="0.00")
                self.strvar_costo_dolar_bruto.set(value="0.00")
                return

            elif que_campo == "completo":

                # Calculo el costo neto en dolares
                calc_pesos_neto = round((float(self.strvar_costo_neto_dolar.get()) * float(self.strvar_dolar_actual.get())), 2)

                # self.strvar_costo_neto_pesos.set(value=0)
                self.strvar_costo_neto_pesos.set(value=str(round(float(calc_pesos_neto), 2)))

                # Calculo el costo en pesos neto a partir del ingreso de pesos
                calc_dolar_neto = str(round((float(self.strvar_costo_neto_pesos.get()) / float(self.strvar_dolar_actual.get())), 2))
                # self.strvar_costo_neto_dolar.set(value=0)
                self.strvar_costo_neto_dolar.set(value=str(round(float(calc_dolar_neto), 2)))

                # Calculo el iva correspondiente segun la tasa seleccionada
                self.val1 = self.combo_iva.get()
                self.val2 = self.strvar_costo_neto_pesos.get()
                self.strvar_total_iva.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

                # Calculo el Impuesto Interno
                self.val1 = self.strvar_tasa_impint.get()
                self.val2 = self.strvar_costo_neto_pesos.get()
                self.strvar_total_impint.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

                # Calculo la ganancia
                self.strvar_subtotal.set(value=str(round((float(self.strvar_costo_neto_pesos.get()) +
                                                      float(self.strvar_total_iva.get()) +
                                                      float(self.strvar_total_impint.get())), 2)))

                self.val1 = self.strvar_tasa_ganancia.get()
                self.val2 = self.strvar_subtotal.get()
                self.strvar_total_ganancia.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

            # Aca se recalculan todos los totales por si se modifica algo
            # Total IVA
            self.val1 = self.combo_iva.get()
            self.val2 = self.strvar_costo_neto_pesos.get()
            self.strvar_total_iva.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

            # Subtotal
            self.strvar_subtotal.set(value=str(round((float(self.strvar_costo_neto_pesos.get()) +
                                                  float(self.strvar_total_iva.get()) +
                                                  float(self.strvar_total_impint.get())), 2)))

            # pesos y dolar bruto con impuestos
            self.strvar_costo_pesos_bruto.set(value=str(round(float(self.strvar_subtotal.get()), 2)))
            self.strvar_costo_dolar_bruto.set(value=str(round((float(self.strvar_subtotal.get()) / float(self.strvar_dolar_actual.get())), 4)))

            # importe pesos de la ganancia
            self.val1 = self.strvar_tasa_ganancia.get()
            self.val2 = self.strvar_subtotal.get()
            self.strvar_total_ganancia.set(value=str(round(((float(self.val1) * float(self.val2)) / 100), 2)))

            # Total venta en pesos con la ganancia incluida
            self.calc_total_ventas = round((float(self.strvar_costo_neto_pesos.get()) + float(self.strvar_total_iva.get()) +
                                     float(self.strvar_total_impint.get()) + float(self.strvar_total_ganancia.get())), 2)

            self.strvar_total_precio_venta.set(value=str(round(float(self.calc_total_ventas), 2)))

            # calculo el precio de venta con el recargo por venta con tarjeta
            self.calc_total_ventas_mas10 = self.calc_total_ventas * ((float(self.strvar_recargo_tarjeta.get()) / 100) + 1)
            self.strvar_total_precio_venta_mas10.set(value=str(round(float(self.calc_total_ventas_mas10), 2)))

        except:

            messagebox.showerror("Except_error", "Revise datos numericos", parent=self)
            self.entry_costo_historico.focus()
            return

    # -----------------------------------------------------------------
    # VALIDACIONES -*-
    # -----------------------------------------------------------------

    def control_blanco(self):

        # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py ---------
        if not control_forma(list(self.strvar_costo_historico.get())):
            self.strvar_costo_historico.set(value="0")
            return False
        if not control_forma(list(self.strvar_costo_neto_dolar.get())):
            self.strvar_costo_neto_dolar.set(value="0")
            return False
        if not control_forma(list(self.strvar_costo_neto_pesos.get())):
            self.strvar_costo_neto_pesos.set(value="0")
            return False
        if not control_forma(list(self.strvar_tasa_impint.get())):
            self.strvar_tasa_impint.set(value="0")
            return False
        if not control_forma(list(self.strvar_tasa_ganancia.get())):
            self.strvar_tasa_ganancia.set(value="0")
            return False
        if not control_forma(list(self.strvar_total_precio_venta.get())):
            self.strvar_total_precio_venta.set(value="0")
            return False

        if (self.strvar_costo_historico.get() == "" or self.strvar_costo_historico.get() == "." or
                self.strvar_costo_historico.get() == "-"):
            self.strvar_costo_historico.set(value="0.00")
        if (self.strvar_costo_neto_dolar.get() == "" or self.strvar_costo_neto_dolar.get() == "." or
                self.strvar_costo_neto_dolar.get() == "-"):
            self.strvar_costo_neto_dolar.set(value="0.00")
        if (self.strvar_costo_neto_pesos.get() == "" or self.strvar_costo_neto_pesos.get() == "." or
                self.strvar_costo_neto_pesos.get() == "-"):
            self.strvar_costo_neto_pesos.set(value="0.00")
        if (self.strvar_tasa_impint.get() == "" or self.strvar_tasa_impint.get() == "." or
                self.strvar_tasa_impint.get() == "-"):
            self.strvar_tasa_impint.set(value="0.00")
        if (self.strvar_tasa_ganancia.get() == "" or self.strvar_tasa_ganancia.get() == "." or
                self.strvar_tasa_ganancia.get() == "-"):
            self.strvar_tasa_ganancia.set(value="0.00")
        if (self.strvar_total_precio_venta.get() == "" or self.strvar_total_precio_venta.get() == "." or
                self.strvar_total_precio_venta.get() == "-"):
            self.strvar_total_precio_venta.set(value="0.00")

        return True

    def control_valores(self):

        if float(self.strvar_costo_historico.get()) == 0:
            self.strvar_costo_historico.set(value="0.00")
        else:
            self.strvar_costo_historico.set(value=str(round(float(self.strvar_costo_historico.get()), 2)))
        if float(self.strvar_costo_neto_dolar.get()) == 0:
            self.strvar_costo_neto_dolar.set(value="0.00")
        else:
            self.strvar_costo_neto_dolar.set(value=str(round(float(self.strvar_costo_neto_dolar.get()), 2)))
        if float(self.strvar_costo_neto_pesos.get()) == 0:
            self.strvar_costo_neto_pesos.set(value="0.00")
        else:
            self.strvar_costo_neto_pesos.set(value=str(round(float(self.strvar_costo_neto_pesos.get()), 2)))
        if float(self.strvar_tasa_impint.get()) == 0:
            self.strvar_tasa_impint.set(value="0.00")
        else:
            self.strvar_tasa_impint.set(value=str(round(float(self.strvar_tasa_impint.get()), 2)))
        if float(self.strvar_tasa_ganancia.get()) == 0:
            self.strvar_tasa_ganancia.set(value="0.00")
        else:
            self.strvar_tasa_ganancia.set(value=str(round(float(self.strvar_tasa_ganancia.get()), 2)))
        if float(self.strvar_total_precio_venta.get()) == 0:
            self.strvar_total_precio_venta.set(value="0.00")
        else:
            self.strvar_total_precio_venta.set(value=str(round(float(self.strvar_total_precio_venta.get()), 2)))

    # --------------------------------------------------------------------------
    # PUNTEROS -*-
    # --------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_articulos.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return

            # selecciono el Id primero de la lista en este caso
            self.grid_articulos.selection_set(rg)
            # pone el primero Id
            self.grid_articulos.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_articulos.yview(self.grid_articulos.index(self.grid_articulos.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_articulos.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_articulos.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_articulos.focus(rg)
            # lleva el foco al final del treeview
            self.grid_articulos.yview(self.grid_articulos.index(self.grid_articulos.get_children()[-1]))

    def forden_codigo(self):

        #Por rubro, marca y descripcion
        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.filtro_activo = "articulos ORDER BY rubro, marca, descripcion ASC"
        self.limpiar_Grid()
        self.llena_grilla("")
        #self.puntero_modificacion(self.clave)

    def forden_descripcion(self):

        # Por marca y descripcion
        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.filtro_activo = "articulos ORDER BY marca, descripcion ASC"
        self.limpiar_Grid()
        self.llena_grilla("")
        #self.puntero_modificacion(self.clave)

    def fQuitarfiltros(self):

        self.filtro_activo = "articulos ORDER BY rubro, marca, descripcion ASC"
        self.limpiar_Grid()
        self.llena_grilla("")
        self.fResetmarca()
        self.fResetrubro()
        self.btn_nuevo.focus()
