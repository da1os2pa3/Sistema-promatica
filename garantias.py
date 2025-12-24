from funciones import *
from funcion_new import *
from garantias_ABM import datosGarantias
#------------------------------------------------
#import tkinter as tk
#from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import *
#------------------------------------------------
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from PIL import Image, ImageTk

class clase_garantias(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # Instanciaciones -----------------------------------------------------------------

        """ Creo una instancia de clase varGarantia. Le paso la pantalla para poder usar los parent 
            en los mensajes de messagebox. """
        self.varGarantia = datosGarantias(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # PANTALLA

        # Esto esta agregado para centrar las ventanas en la pantalla
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 620
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # ------------------------------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. """

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_garantias.identify_row(0)
        # self.grid_garantias.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_garantias.focus(item)

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        # --------------------------------------------------------------
        # TITULOS
        # --------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('garantia.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_garantia = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_garantia = Label(self.frame_titulo_top, image=self.png_garantia, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Garantias",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_garantia.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES
        # --------------------------------------------------------------------------

        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # --------------------------------------------------------------------------
        # STRINGVARS
        # --------------------------------------------------------------------------

        self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")
        self.traer_dolarhoy()

        self.strvar_buscostring =tk.StringVar(value="")
        self.strvar_nombre_cliente = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.strvar_fecha_movim = tk.StringVar(value=una_fecha)
        self.strvar_fecha_vto = tk.StringVar(value=una_fecha)
        self.strvar_detalle_articulo = tk.StringVar(value="")
        self.strvar_total_oper = tk.StringVar(value="0")
        self.strvar_meses = tk.StringVar(value="1")
        self.strvar_numero_factura = tk.StringVar(value="")
        self.strvar_observaciones = tk.StringVar(value="")

        # ------------------------------------------------------------------------
        # TREVIEEW
        # ------------------------------------------------------------------------

        self.frame_tvw_garantias=LabelFrame(self.master, text="Garantias: ", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_garantias)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_garantias = ttk.Treeview(self.frame_tvw_garantias, height=5, columns=("col1", "col2", "col3", "col4",
                                                                               "col5", "col6", "col7", "col8", "col9"))

        self.grid_garantias.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_garantias.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_garantias.column("col1", width=100, anchor="center", minwidth=80)
        self.grid_garantias.column("col2", width=50, anchor="center", minwidth=50)
        self.grid_garantias.column("col3", width=100, anchor="center", minwidth=80)
        self.grid_garantias.column("col4", width=50, anchor="center", minwidth=50)
        self.grid_garantias.column("col5", width=300, anchor=W, minwidth=280)
        self.grid_garantias.column("col6", width=600, anchor=W, minwidth=600)
        self.grid_garantias.column("col7", width=100, anchor="center", minwidth=100)
        self.grid_garantias.column("col8", width=80, anchor="center", minwidth=80)
        self.grid_garantias.column("col9", width=200, anchor="center", minwidth=200)

        self.grid_garantias.heading("#0", text="Id", anchor="center")
        self.grid_garantias.heading("col1", text="Fecha venta", anchor="center")
        self.grid_garantias.heading("col2", text="meses", anchor="center")
        self.grid_garantias.heading("col3", text="Fecha vencimiento", anchor="center")
        self.grid_garantias.heading("col4", text="", anchor="center")
        self.grid_garantias.heading("col5", text="Cliente", anchor="center")
        self.grid_garantias.heading("col6", text="Articulo", anchor="center")
        self.grid_garantias.heading("col7", text="Importe", anchor="center")
        self.grid_garantias.heading("col8", text="Factura", anchor="center")
        self.grid_garantias.heading("col9", text="Observaciones", anchor="center")

        self.grid_garantias.tag_configure('oddrow', background='light grey')
        self.grid_garantias.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_garantias, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_garantias, orient=VERTICAL)
        self.grid_garantias.config(xscrollcommand=scroll_x.set)
        self.grid_garantias.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_garantias.xview)
        scroll_y.config(command=self.grid_garantias.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_garantias['selectmode'] = 'browse'

        self.grid_garantias.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_garantias.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # BUSQUEDA DE UNA GARANTIA
        # --------------------------------------------------------------------------

        self.frame_busco_garantia=LabelFrame(self.master, text="", background="light blue", foreground="red")

        self.lbl_buscar_titulo = Label(self.frame_busco_garantia, text="Buscar garantia nombre cliente: ",
                                       background="light blue")
        self.lbl_buscar_titulo.grid(row=0, column=0, padx=5, pady=3, sticky='nsew')

        # ENTRY BUSCAR
        self.entry_buscar_movim=Entry(self.frame_busco_garantia,textvariable=self.strvar_buscostring, width=50)
        self.entry_buscar_movim.grid(row=0, column=1, padx=5, pady=3, sticky='nsew')

        # BOTON FILTRAR
        self.btn_filtrar_movim = Button(self.frame_busco_garantia, text="Buscar", command=self.fBuscar_en_tabla,
                                       bg="blue", fg="white", width=34)
        self.btn_filtrar_movim.grid(row=0, column=2, padx=5, pady=3, sticky='nsew')

        # BOTON SHOW ALL
        self.btn_showall_movim = Button(self.frame_busco_garantia, text="Mostrar todo", command=self.fShowall,
                                 bg="blue", fg="white", width=34)
        self.btn_showall_movim.grid(row=0, column=3, padx=5, pady=3, sticky='nsew')

        self.frame_busco_garantia.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=3)
        # ------------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------------
        # BOTONES DEL TREEVIEW
        # --------------------------------------------------------------------------

        # FRAME primero
        self.frame_primero=LabelFrame(self.master, text="", foreground="red")

        # BOTON NUEVO
        self.btn_nuevoitem = Button(self.frame_primero, text="Nuevo Garantia", command=self.fNuevo, width=22, bg="blue",
                                    fg="white")
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)
        # BOTON EDITAR
        self.btn_editaitem = Button(self.frame_primero, text="Edita Garantia", command=self.fEditar, width=22,
                                    bg="blue", fg="white")
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)
        # BOTON BORRAR
        self.btn_borraitem = Button(self.frame_primero, text="Elimina Garantia", command=self.fBorrar, width=22,
                                    bg="red", fg="white")
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)
        # BOTON GUARDAR
        self.btn_guardaritem = Button(self.frame_primero, text="Guardar Garantia", command=self.fGuardar, width=21,
                                      bg="green", fg="white")
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)
        # BOTON CANCELAR
        self.btn_Cancelar = Button(self.frame_primero, text="Cancelar", command=self.fCancelar, width=21, bg="black",
                                   fg="white")
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)
        # -----------------------------------------------------------------------------

        # botones fin y principio archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_primero, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=5, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_primero, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=6, padx=5, sticky="nsew", pady=2)
        # ---------------------------------------------------------------------------

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_primero, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")

        self.frame_primero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # ENTRYS - PEDIDO DE DATOS
        # --------------------------------------------------------------------------

        self.frame_segundo=LabelFrame(self.master, text="", foreground="red")

        # Fecha del movimiento
        self.lbl_fecha_movim = Label(self.frame_segundo, text="Fecha Ingreso: ", justify=LEFT)
        self.lbl_fecha_movim.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_fecha_movim = Entry(self.frame_segundo, textvariable=self.strvar_fecha_movim, width=10,
                                       justify=RIGHT)
        self.entry_fecha_movim.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        #self.entry_fecha_movim.bind("<FocusOut>", self.formato_fecha)
        #self.entry_fecha_movim.bind('<Tab>', lambda e: self.calcular())

        # Importe Debito
        self.lbl_meses = Label(self.frame_segundo, text="Meses garantia: ", justify=LEFT)
        self.lbl_meses.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.entry_meses = Entry(self.frame_segundo, textvariable=self.strvar_meses, width=5, justify=RIGHT)
        self.entry_meses.config(validate="key", validatecommand=self.vcmd)
        self.entry_meses.grid(row=0, column=3, padx=5, pady=2, sticky=W)
        self.strvar_meses.trace("w", lambda *args: self.limitador(self.strvar_meses, 2))
        self.entry_meses.bind('<Tab>', lambda e: self.calcular_fechas())

        # Fecha vencimiento de garantia
        self.lbl_fecha_vto = Label(self.frame_segundo, text="Fecha Vencimiento: ", justify=LEFT)
        self.lbl_fecha_vto.grid(row=0, column=4, padx=5, pady=2, sticky=W)
        self.lbl_fecha_vto_strvar = Label(self.frame_segundo, textvariable=self.strvar_fecha_vto, width=10,
                                          justify=RIGHT)
        #self.lbl_fecha_vto_strvar.bind("<FocusOut>", self.formato_fecha)
        self.lbl_fecha_vto_strvar.grid(row=0, column=5, padx=5, pady=2, sticky=W)

        # Importe venta articulo
        self.lbl_total_oper = Label(self.frame_segundo, text="Total operacion: ", justify=LEFT)
        self.lbl_total_oper.grid(row=0, column=6, padx=5, pady=2, sticky=W)
        self.entry_total_oper = Entry(self.frame_segundo, textvariable=self.strvar_total_oper, width=15, justify=RIGHT)
        self.entry_total_oper.config(validate="key", validatecommand=self.vcmd)
        self.entry_total_oper.grid(row=0, column=7, padx=5, pady=2, sticky=W)
        self.entry_total_oper.config(validate="key", validatecommand=self.vcmd)
        self.strvar_total_oper.trace("w", lambda *args: self.limitador(self.strvar_total_oper, 15))

        self.frame_segundo.pack(side=TOP, fill=BOTH,expand=0, padx=5, pady=3)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        self.frame_tercero=LabelFrame(self.master, text="", foreground="red")

        # Detalle del articulo
        self.lbl_detalle_articulo = Label(self.frame_tercero, text="Detalle articulo: ", justify=LEFT)
        self.lbl_detalle_articulo.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.photo_bus_art = Image.open('buscar.png')
        self.photo_bus_art = self.photo_bus_art.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = Button(self.frame_tercero, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=1, padx=5, pady=3)
        self.entry_detalle_articulo = Entry(self.frame_tercero, textvariable=self.strvar_detalle_articulo, width=143,
                                            justify=LEFT)
        self.strvar_detalle_articulo.trace("w", lambda *args: limitador(self.strvar_detalle_articulo, 150))
        self.entry_detalle_articulo.grid(row=0, column=2, columnspan=6, padx=5, pady=2, sticky=W)

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_tercero, text="Cliente garantia: ", justify=LEFT)
        self.lbl_texto_nombre_cliente.grid(row=1, column=0, padx=5, pady=2, sticky=W)
        # BOTON BUSCAR CLIENTE EN LISTBOX
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_tercero, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=1, column=1, padx=5, pady=3)
        self.entry_nombre_cliente = Entry(self.frame_tercero, textvariable=self.strvar_nombre_cliente, width=52)
        self.entry_nombre_cliente.grid(row=1, column=2, padx=5, pady=2, sticky=W)
        self.lbl_texto_codigo_cliente = Label(self.frame_tercero, textvariable=self.strvar_codigo_cliente, width=10 )
        self.lbl_texto_codigo_cliente.grid(row=1, column=3, padx=5, pady=2, sticky=W)

        self.frame_tercero.pack(side="top", fill=BOTH,expand=0, padx=5, pady=3)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        self.frame_cuarto=LabelFrame(self.master, text="", foreground="red")

        # DATOS FACTURA Y OBSERVACIONES
        self.lbl_numero_factura = Label(self.frame_cuarto, text="Factura Nº: ", justify=LEFT)
        self.lbl_numero_factura.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_numero_factura = Entry(self.frame_cuarto, textvariable=self.strvar_numero_factura, width=15,
                                          justify=RIGHT)
        #self.entry_numero_factura.config(validate="key", validatecommand=vcmd)
        self.entry_numero_factura.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.strvar_numero_factura.trace("w", lambda *args: self.limitador(self.strvar_numero_factura, 15))
        self.lbl_observaciones = Label(self.frame_cuarto, text="Observaciones: ", justify=LEFT)
        self.lbl_observaciones.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.entry_observaciones = Entry(self.frame_cuarto, textvariable=self.strvar_observaciones, width=120,
                                         justify=LEFT)
        self.entry_observaciones.grid(row=0, column=3, padx=5, pady=2, sticky=W)
        self.strvar_observaciones.trace("w", lambda *args: self.limitador(self.strvar_observaciones, 150))

        self.frame_cuarto.pack(side=TOP, fill=BOTH,expand=0, padx=5, pady=3)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        self.frame_quinto=LabelFrame(self.master, text="", foreground="red")

        # DETALLES NOVEDADES
        # lbl_detalle = Label(self.frame_segundo_2, text="Detalle:", height=1)
        # lbl_detalle.grid(row=1, column=0, padx=4, pady=1, sticky="nsew")
        self.text_detalle = ScrolledText(self.frame_quinto)
        self.text_detalle.config(width=120, height=6, wrap="word", padx=4, pady=3)
        self.text_detalle.grid(row=1, column=1, padx=4, pady=5, sticky="nsew")

        self.frame_quinto.pack(side=TOP, fill=BOTH,expand=0, padx=5, pady=3)
        # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    # GRID
    # -----------------------------------------------------------------------------

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varGarantia.consultar_garantia(self.filtro_activo)
        else:
            datos = self.varGarantia.consultar_garantia("garantias ORDER BY gt_fechavto ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'), "hora_no")
            forma_normal2 = fecha_str_reves_normal(self, datetime.strftime(row[3], '%Y-%m-%d'), "hora_no")

            self.grid_garantias.insert("", END, tags=color, text=row[0], values=(forma_normal, row[2],
                                                    forma_normal2, row[4], row[5], row[6], row[7], row[8], row[9]))

        if len(self.grid_garantias.get_children()) > 0:
            self.grid_garantias.selection_set(self.grid_garantias.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_garantias.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_garantias.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """
            """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_garantias.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_garantias.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_garantias.yview(self.grid_garantias.index(rg))
            return
        else:
            self.mover_puntero_topend("END")

    def limpiar_Grid(self):

        for item in self.grid_garantias.get_children():
            self.grid_garantias.delete(item)

    # -----------------------------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------------------------

    def estado_inicial(self):

        # Variables
        self.var_Id = -1
        self.alta_modif = 0
        self.dato_seleccion = ""
        self.filtro_activo = "garantias ORDER BY gt_fechavto ASC"

        # Grilla
        self.selected = self.grid_garantias.focus()
        self.clave = self.grid_garantias.item(self.selected, 'text')

        # Estado inicial del Gui
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_A("normal")
        self.habilitar_btn_B("disabled")
        self.habilitar_Btn_busquedas("normal")

    def limpiar_text(self):

        # Limpio los entrys y asigno valores iniciales en algunos campos necesarios

        if self.alta_modif == 1:
            una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
            self.strvar_fecha_movim.set(value=una_fecha)
            self.strvar_fecha_vto.set(value=una_fecha)
        elif self.alta_modif == 2 or self.alta_modif == 0:
            self.strvar_fecha_movim.set(value="")
            self.strvar_fecha_vto.set(value="")

        self.strvar_meses.set(value="1")
        self.strvar_total_oper.set(value="0")
        self.strvar_detalle_articulo.set(value="")
        self.strvar_nombre_cliente.set(value="")
        self.strvar_codigo_cliente.set(value="0")
        self.strvar_numero_factura.set(value="")
        self.strvar_observaciones.set(value="")
        self.text_detalle.delete('1.0', 'end')

    def habilitar_text(self, estado):

        self.entry_fecha_movim.configure(state=estado)
        self.entry_meses.configure(state=estado)
        self.entry_total_oper.configure(state=estado)
        self.entry_detalle_articulo.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_numero_factura.configure(state=estado)
        self.entry_observaciones.configure(state=estado)
        self.btn_bus_art.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)
        self.text_detalle.configure(state=estado)
        if self.alta_modif == 1:
            self.grid_garantias['selectmode'] = 'none'
            self.grid_garantias.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif == 2 or self.alta_modif == 0:
            self.grid_garantias['selectmode'] = 'browse'
            self.grid_garantias.bind("<Double-Button-1>", self.DobleClickGrid)

    def habilitar_btn_A(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)

    def habilitar_btn_B(self, estado):

        self.btn_guardaritem.configure(state=estado)

    def habilitar_Btn_busquedas(self, estado):

        self.btn_filtrar_movim.configure(state=estado)
        self.btn_showall_movim.configure(state=estado)
        self.entry_buscar_movim.configure(state=estado)

    def fNo_modifique(self, event):
        return

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()

            self.filtro_anterior = self.filtro_activo

            self.filtro_activo = ("garantias WHERE INSTR(gt_nomcli, '" + se_busca + "') > 0")

            self.varGarantia.buscar_entabla(self.filtro_activo)
            self.limpiar_Grid()
            self.llena_grilla("")

            """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
            item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
            item = self.grid_garantias.selection()
            self.grid_garantias.focus(item)

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

    def fShowall(self):

        self.selected = self.grid_garantias.focus()
        self.clave = self.grid_garantias.item(self.selected, 'text')
        self.filtro_activo = "garantias ORDER BY gt_fechavto ASC"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    # -------------------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.limpiar_text()
        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_btn_A("disabled")
        self.habilitar_btn_B("normal")
        self.entry_fecha_movim.focus()

    def fEditar(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_garantias.focus()
        # Asi obtengo la clave de la tabla (campo Id) que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_garantias.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Editar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2
        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        self.habilitar_text('normal')
        self.limpiar_text()

        self.filtro_activo = "garantias WHERE Id = " + str(self.clave)

        valores = self.varGarantia.consultar_garantia(self.filtro_activo)

        for row in valores:

            if row[1] == "None":
                messagebox.showerror("Error", "Error de fechas en Tabla, elimine el item y "
                                              "vuelva a cargarlo ", parent=self)
                self.estado_inicial()
                return

            # Convierto fechas a dd/mm/aaa
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'), "hora_no")
            forma_normal2 = fecha_str_reves_normal(self, datetime.strftime(row[3], '%Y-%m-%d'), "hora_no")

            self.entry_fecha_movim.insert(0, forma_normal)
            self.strvar_fecha_vto.set(value=forma_normal2)
            self.entry_meses.insert(0, row[2])
            self.strvar_codigo_cliente.set(value=row[4])
            self.entry_nombre_cliente.insert(0, row[5])
            self.entry_detalle_articulo.insert(0, row[6])
            self.entry_total_oper.insert(0, row[7])
            self.entry_numero_factura.insert(0, row[8])
            self.entry_observaciones.insert(0, row[9])
            self.text_detalle.insert(END, row[10])

        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_btn_A("disabled")
        self.habilitar_btn_B("normal")
        self.entry_nombre_cliente.focus()

    def fBorrar(self):

        # ------------------------------------------------------------------------------
        # guardo item seleccionado en el grid
        self.selected = self.grid_garantias.focus()
        self.selected_ant = self.grid_garantias.prev(self.selected)
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_garantias.item(self.selected, 'text')
        self.clave_ant = self.grid_garantias.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_garantias.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[4]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion Cancelada", parent=self)
            return

        self.varGarantia.eliminar_item_garantia(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # -------------------------------------------------------------------
        # VALIDACIONES

        # FECHA
        if not self.strvar_fecha_movim.get() or not self.strvar_fecha_vto.get():
            messagebox.showerror("Error", "Fecha en blanco", parent=self)
            self.entry_fecha_movim.focus()
            return

        # DETALLE
        if not self.strvar_nombre_cliente.get():
            messagebox.showerror("Error", "Agregue un cliente", parent=self)
            self.entry_nombre_cliente.focus()
            return

        # aaa = 0
        # if aaa == 0:
        try:

            # guardo el Id del Treeview en selected para ubicacion del foco a posterior (i001, i002....
            self.selected = self.grid_garantias.focus()
            # Guardo Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en TABLA 1,2,3)
            self.clave = self.grid_garantias.item(self.selected, 'text')

            if self.alta_modif == 1:

                # Convierto fechas a yyyy-mmy-dd
                fecha_aux = datetime.strptime(self.strvar_fecha_movim.get(), '%d/%m/%Y')
                fecha_aux2 = datetime.strptime(self.strvar_fecha_vto.get(), '%d/%m/%Y')

                self.varGarantia.insertar_garantias(fecha_aux, self.strvar_meses.get(), fecha_aux2,
                                                    self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                                    self.strvar_detalle_articulo.get(), self.strvar_total_oper.get(),
                                                    self.strvar_numero_factura.get(), self.strvar_observaciones.get(),
                                                    self.text_detalle.get(1.0, 'end-1c'))

                messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

            else:

                # Convierto fechas a yyyy-mmy-dd
                fecha_aux = datetime.strptime(self.strvar_fecha_movim.get(), '%d/%m/%Y')
                fecha_aux2 = datetime.strptime(self.strvar_fecha_vto.get(), '%d/%m/%Y')

                self.varGarantia.modificar_garantias(self.var_Id, fecha_aux, self.strvar_meses.get(), fecha_aux2,
                            self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                            self.strvar_detalle_articulo.get(), self.strvar_total_oper.get(),
                            self.strvar_numero_factura.get(), self.strvar_observaciones.get(),
                            self.text_detalle.get(1.0, 'end-1c'))

                self.var_Id == -1
                messagebox.showinfo("Modificacion", "La modificacion fue exitosa", parent=self)

            self.filtro_activo = "garantias ORDER BY gt_fechavto ASC"

            # cierre de las novedades y reseteando pantalla para nuevo movimiento - actualizando grilla
            self.limpiar_Grid()
            self.limpiar_text()

            # ordenamiento puntero en treeview
            if self.alta_modif == 1:
                ultimo_tabla_id = self.varGarantia.traer_ultimo(0)
                self.llena_grilla(ultimo_tabla_id)
            elif self.alta_modif == 2:
                self.llena_grilla(self.clave)

            self.estado_inicial()
            self.btn_nuevoitem.focus()

        except:

            messagebox.showerror("Error", "Al guardar los datos - fGuardar", parent=self)
            self.entry_fecha_planilla.focus()
            return

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_inicial()

    def fSalir(self):
        self.master.destroy()

    # -------------------------------------------------------------------------
    # PUNTEROS
    # -------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_garantias.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_garantias.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_garantias.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_garantias.yview(self.grid_garantias.index(self.grid_garantias.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_garantias.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_garantias.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_garantias.focus(rg)
            # lleva el foco al final del treeview
            self.grid_garantias.yview(self.grid_garantias.index(self.grid_garantias.get_children()[-1]))

    # ------------------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------------------

    def formato_fecha(self, pollo):

        """ Aqui llamo a la funcion validar fechas para revisar todas sus valores posibles. Le paso la fecha
        tipo string con barras o sin barras. """

        estado_antes = self.strvar_fecha_movim.get()

        # FUNCION que valida las fechas en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_movim.get())

        if retorno_VerFal == "":
            self.strvar_fecha_movim.set(value=estado_antes)
            self.entry_fecha_movim.focus()
            return ("error")
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            # OJO REVISAR
            self.filtro_activo = ("garantias WHERE CAST(gt_fechavto AS date) = CAST('" +
                                  self.strvar_fecha_movim.get() + "' AS date)")
            self.limpiar_Grid()
            self.llena_grilla("")
            self.entry_fecha_movim.focus()
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_movim.set(value=estado_antes)
            self.entry_fecha_movim.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_movim.set(value=retorno_VerFal)

        return ("bien")

    def traer_dolarhoy(self):

        dev_informa = self.varGarantia.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def DobleClickGrid(self, event):
        self.fEditar()

    def calcular_fechas(self):

        # paso a date
        fecha1 = (datetime.strptime(self.strvar_fecha_movim.get(), '%d/%m/%Y'))
        # sumo los meses a fecha 1 y obtengo fecha de vencimiento
        meses = int(self.strvar_meses.get())
        fecha2 = fecha1 + relativedelta(months=meses)
        self.strvar_fecha_vto.set(value=datetime.strftime(fecha2, '%d/%m/%Y'))

    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda
        y en que campos debe hacerse. """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de como 
        quiero verlos. -Titulos para cada columna de esos campos y String de busqueda definido arriba (que_busco). """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                                                        "Orden: Alfabetico cliente", "N")

        """  Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes. """

        for item in valores_new:
            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # ------------------------------------------------------------------------------
    # ARTICULO

    def fBusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse. """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.strvar_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.strvar_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.strvar_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(codbar, '" + self.strvar_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.strvar_detalle_articulo.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.varFuncion_new.ventana_selec("articulos", "descripcion", "rubro",
                                                "marca", "Descripcion", "Rubro","Marca",
                                                        que_busco, "Orden: Rubro+Marca+Descripcion","N")

        for item in valores_new:
            self.strvar_detalle_articulo.set(value=item[2]) # d<escripcion del articulo
            #self.strvar__codigo_cliente.set(value=item[1])

        self.entry_detalle_articulo.focus()
        self.entry_detalle_articulo.icursor(tk.END)
