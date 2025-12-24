from rma_ABM import *
from funciones import *
from funcion_new import *
# --------------------------------------
#from tkinter import *
#import tkinter as tk
#from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
#from tkinter.scrolledtext import *     # para campos text
# --------------------------------------
import os
from PDF_clase import *
from datetime import date, datetime
from PIL import Image, ImageTk

class clase_rma(Frame):

    # Creo la clase - clase definida en ABM

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        # ------------------------------------------------------------------
        # Seteo pantalla master principal
        self.master.grab_set()
        self.master.focus_set()
        # ------------------------------------------------------------------

        #-------------------------------------------------------------------
        # Instanciaciones
        self.varRma = datosRma()
        self.varFuncion_new = ClaseFuncion_new(self.master)
        #-------------------------------------------------------------------

        # ------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # ------ Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # ------ Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 520
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) - 0
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------

        # # Se usa para saber que filtro esta activo y mantenerlo - a continuacion se setea a un valor inicial
        # default = 'Pendiente'
        # self.filtro_activo =  "rma WHERE rm_estado = '" + default + "' ORDER BY rm_fecha ASC"

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        Otras funciones para manejar los elementos seleccionados incluyen:
        selection_add(): añade elementos a la selección.
        selection_remove(): remueve elementos de la selección.
        selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        selection_toggle(): cambia la selección de un elemento. """

        # # ======================== SETEO DE ESTADOS INICIALES ======================================
        # # guarda en item el Id del elemento fila en este caso fila 0 del grid principal
        # item = self.grid_rma.identify_row(0)
        # # Grid --------------------------------------------------------
        # self.grid_rma.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_rma.focus(item)
        # self.estado_inicial()
        # ------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        # ------------------------------------------------------------------
        # TITULOS
        # ------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('rma.png')
        self.photo3 = self.photo3.resize((60, 60), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_rma = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_rma = Label(self.frame_titulo_top, image=self.png_rma, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=49, text="Pendientes", bg="black", fg="gold",
                                                       font=("Arial bold", 22, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_rma.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # VARIABLES GENERALES
        # ------------------------------------------------------------------

        vcmd = (self.register(self.varFuncion_new.validar), '%P')

        # # Identifica que se esta seleccionando (cliente, articulo,....)
        # self.dato_seleccion = ""

        # # Se usa para saber que filtro esta activo y mantenerlo - a continuacion se setea a un valor inicial
        # se_busca = 'Pendiente'
        # self.filtro_activo =  "rma WHERE rm_estado = '" + se_busca + "' ORDER BY rm_fecha ASC"
        #self.filtro_activo_auxiliar = "faltanmtesaux_presup"

        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        # self.var_Id = -1
        # self.alta_modif = 0

        # para validar ingresos de numeros en gets numericos
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # STRINGVARS
        # ------------------------------------------------------------------

        una_fecha= date.today()
        self.strvar_fecha = tk.StringVar(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_proveedor = tk.StringVar(value="")
        self.strvar_articulo = tk.StringVar(value="")
        self.strvar_cliente = tk.StringVar(value="")
        self.strvar_problema = tk.StringVar(value="")
        self.strvar_costo_venta = tk.StringVar(value="")
        self.strvar_estado = tk.StringVar(value="")
        self.strvar_observaciones = tk.StringVar(value="")
        self.strvar_buscostring = tk.StringVar(value="")
        self.strvar_combo_estado = tk.StringVar(value="")
        self.strvar_combo_proceso = tk.StringVar(value="")
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # GRID
        # ------------------------------------------------------------------

        self.frame_rma = LabelFrame(self.master, text="RMA", foreground="#CD5C5C")
        self.frame_rma_uno = LabelFrame(self.frame_rma, text="", foreground="#CD5C5C")
        self.frame_rma_dos=LabelFrame(self.frame_rma, text="", foreground="#CD5C5C")
        self.frame_busqueda_rma=LabelFrame(self.frame_rma, text="", border=5, foreground="black", background="light blue")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_rma_dos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_rma = ttk.Treeview(self.frame_rma_dos, height=4, columns=("col1", "col2", "col3", "col4", "col5",
                                                                            "col6", "col7", "col8", "col9"))

        self.grid_rma.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_rma.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_rma.column("col1", width=60, anchor=W, minwidth=60)
        self.grid_rma.column("col2", width=180, anchor=W, minwidth=150)
        self.grid_rma.column("col3", width=40, anchor=CENTER, minwidth=40)
        self.grid_rma.column("col4", width=40, anchor=CENTER, minwidth=40)
        self.grid_rma.column("col5", width=40, anchor=CENTER, minwidth=40)
        self.grid_rma.column("col6", width=40, anchor=CENTER, minwidth=40)
        self.grid_rma.column("col7", width=40, anchor=CENTER, minwidth=40)
        self.grid_rma.column("col8", width=40, anchor=CENTER, minwidth=40)
        self.grid_rma.column("col9", width=40, anchor=CENTER, minwidth=40)

        self.grid_rma.heading("#0", text="Id", anchor=CENTER)
        self.grid_rma.heading("col1", text="Fecha", anchor=W)
        self.grid_rma.heading("col2", text="Articulo", anchor=W)
        self.grid_rma.heading("col3", text="Proceso", anchor=CENTER)
        self.grid_rma.heading("col4", text="Estado", anchor=CENTER)
        self.grid_rma.heading("col5", text="Proveedor", anchor=CENTER)
        self.grid_rma.heading("col6", text="Cliente", anchor=CENTER)
        self.grid_rma.heading("col7", text="Falla/motivo", anchor=CENTER)
        self.grid_rma.heading("col8", text="Costo/Venta", anchor=CENTER)
        self.grid_rma.heading("col9", text="Observaciones", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_rma_dos, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_rma_dos, orient=VERTICAL)
        self.grid_rma.config(xscrollcommand=scroll_x.set)
        self.grid_rma.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_rma.xview)
        scroll_y.config(command=self.grid_rma.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_rma['selectmode'] = 'browse'
        self.grid_rma.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # BOTONES
        # ------------------------------------------------------------------

        # Botones CRUD
        self.btn_nuevo_rma=Button(self.frame_rma_uno, text="Nuevo Movimiento", command=self.fNuevo_rma, width=17,
                                  bg='blue', fg='white')
        self.btn_nuevo_rma.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.btn_edito_rma=Button(self.frame_rma_uno, text="Editar Movimiento", command=self.fEdito_rma, width=17,
                                  bg='blue', fg='white')
        self.btn_edito_rma.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.btn_borro_rma=Button(self.frame_rma_uno, text="Borrar Movimiento", command=self.fBorro_rma, width=17,
                                  bg='red', fg='white')
        self.btn_borro_rma.grid(row=2, column=0, padx=3, pady=3, sticky=W)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_rma_uno, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=3, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_rma_uno, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=4, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # Buscar un articulo en Grid
        self.lbl_busqueda_rma = Label(self.frame_busqueda_rma, text="Texto a buscar: ", justify=LEFT, bg="light blue")
        self.lbl_busqueda_rma.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_busqueda_rma = Entry(self.frame_busqueda_rma, textvariable=self.strvar_buscostring,
                                                  state='normal', width=36, justify="left", bg="light blue")
        self.entry_busqueda_rma.grid(row=0, column=1, padx=5, pady=2, sticky='nsew')

        self.btn_buscar=Button(self.frame_busqueda_rma, text="Buscar", command=self.fBuscar_rma, width=16, bg='#5F9EA0',
                               fg='white')
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=2, sticky=W)

        # Otros botones
        self.btn_Pendientes=Button(self.frame_busqueda_rma, text="Pendientes", command=self.fPendientes, width=16,
                                   bg='#5F9EA0', fg='white')
        self.btn_Pendientes.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        self.btn_showall=Button(self.frame_busqueda_rma, text="Mostrar todo", command=self.fShowall, width=16,
                                bg='#5F9EA0', fg='white')
        self.btn_showall.grid(row=0, column=4, padx=5, pady=2, sticky=W)

        self.btn_imprime_presup=Button(self.frame_busqueda_rma, text="Imprimir", command=self.creopdf, width=16,
                                       bg='#5F9EF5', fg='white')
        self.btn_imprime_presup.grid(row=0, column=5, padx=2, pady=2, sticky=W)

        # PACKS ------------------------------------------------------------
        self.frame_rma_uno.pack(side=LEFT, fill=BOTH, padx=5, pady=2)
        self.frame_rma_dos.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        self.frame_busqueda_rma.pack(expand=0, side="top", fill=BOTH, padx=5, pady=2)
        self.frame_rma.pack(side=TOP, fill="both", padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS
        # ------------------------------------------------------------------

        self.frame_ingreso_datos = LabelFrame(self.master, text="", foreground="black")

        # Fecha de Anotacion
        self.lbl_fecha = Label(self.frame_ingreso_datos, text="Fecha: ", justify="left")
        self.lbl_fecha.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.entry_fecha = Entry(self.frame_ingreso_datos, textvariable=self.strvar_fecha, width=10)
        self.entry_fecha.grid(row=0, column=1, padx=3, pady=3, sticky=E)
        self.entry_fecha.bind("<FocusOut>", self.formato_fecha)

        # Entry proveedor
        self.lbl_proved = Label(self.frame_ingreso_datos, text="Proveedor: ", justify=LEFT)
        self.lbl_proved.grid(row=0, column=2, padx=3, pady=3, sticky=W)
        self.entry_proved = Entry(self.frame_ingreso_datos, textvariable=self.strvar_proveedor, width=30, justify=LEFT)
        self.entry_proved.grid(row=0, column=3, padx=3, pady=3, sticky=W)
        self.strvar_proveedor.trace("w", lambda *args: limitador(self.strvar_proveedor, 50))

        # Combo tipo de proceso del producto
        self.lbl_combo_proceso = Label(self.frame_ingreso_datos, text="Proceso", justify=LEFT, foreground="black")
        self.lbl_combo_proceso.grid(row=0, column=4, padx=3, pady=3, sticky=W)
        self.combo_proceso = ttk.Combobox(self.frame_ingreso_datos, textvariable=self.strvar_combo_proceso,
                                          state='readonly', width=15)
        self.combo_proceso['value'] = ["RMA", "Reparacion", "Prestamo"]
        self.combo_proceso.current(0)
        self.combo_proceso.grid(row=0, column=5, padx=3, pady=3, sticky=E)
        #self.combo_estado.bind('<Tab>', lambda e: self.calcular("completo"))

        # Combo estado dentro del proceso
        self.lbl_combo_estado = Label(self.frame_ingreso_datos, text="Estado", justify=LEFT, foreground="black")
        self.lbl_combo_estado.grid(row=0, column=6, padx=3, pady=3, sticky=W)
        self.combo_estado = ttk.Combobox(self.frame_ingreso_datos, textvariable=self.strvar_combo_estado,
                                         state='readonly', width=15)
        self.combo_estado['value'] = ["Pendiente", "Cambio", "Credito", "No reconocido", "Devolucion", "Finalizado"]
        self.combo_estado.current(0)
        self.combo_estado.grid(row=0, column=7, padx=3, pady=3, sticky=E)
        #self.combo_estado.bind('<Tab>', lambda e: self.calcular("completo"))

        # Entry Cliente
        self.lbl_cliente = Label(self.frame_ingreso_datos, text="Cliente: ", justify=LEFT)
        self.lbl_cliente.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.entry_cliente = Entry(self.frame_ingreso_datos, textvariable=self.strvar_cliente, width=151,
                                   justify="left")
        self.entry_cliente.grid(row=1, column=1, columnspan=7, padx=3, pady=3, sticky=W)
        self.strvar_cliente.trace("w", lambda *args: limitador(self.strvar_cliente, 80))

        # Entry articulo
        self.lbl_articulo = Label(self.frame_ingreso_datos, text="Articulo: ", justify=LEFT)
        self.lbl_articulo.grid(row=2, column=0, padx=3, pady=3, sticky=W)
        self.entry_articulo = Entry(self.frame_ingreso_datos, textvariable=self.strvar_articulo, width=151,
                                    justify="left")
        self.entry_articulo.grid(row=2, column=1, columnspan=7, padx=3, pady=3, sticky=W)
        self.strvar_articulo.trace("w", lambda *args: limitador(self.strvar_articulo, 150))

        # Entry fallo/motivo
        self.lbl_problema = Label(self.frame_ingreso_datos, text="Falla/motivo: ", justify=LEFT)
        self.lbl_problema.grid(row=3, column=0, padx=3, pady=3, sticky=W)
        self.entry_problema = Entry(self.frame_ingreso_datos, textvariable=self.strvar_problema, width=151,
                                    justify=LEFT)
        self.entry_problema.grid(row=3, column=1, columnspan=7, padx=3, pady=3, sticky=W)
        self.strvar_problema.trace("w", lambda *args: limitador(self.strvar_articulo, 200))

        # Entry observaciones del articulo
        self.lbl_costo_venta = Label(self.frame_ingreso_datos, text="Costo/Venta: ", justify=LEFT)
        self.lbl_costo_venta.grid(row=4, column=0, padx=3, pady=3, sticky=W)
        self.entry_costo_venta = Entry(self.frame_ingreso_datos, textvariable=self.strvar_costo_venta, width=151,
                                       justify=LEFT)
        self.entry_costo_venta.grid(row=4, column=1, columnspan=7, padx=3, pady=3, sticky=W)
        self.strvar_costo_venta.trace("w", lambda *args: limitador(self.strvar_costo_venta, 200))

        # Entry observaciones del articulo
        self.lbl_observa = Label(self.frame_ingreso_datos, text="Observaciones: ", justify=LEFT)
        self.lbl_observa.grid(row=5, column=0, padx=3, pady=3, sticky=W)
        self.entry_observa = Entry(self.frame_ingreso_datos, textvariable=self.strvar_observaciones, width=151,
                                   justify=LEFT)
        self.entry_observa.grid(row=5, column=1, columnspan=7, padx=3, pady=3, sticky=W)
        self.strvar_observaciones.trace("w", lambda *args: limitador(self.strvar_observaciones, 200))

        self.frame_ingreso_datos.pack(side="top", fill=BOTH, expand=0, padx=5, pady=5)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # BOTONES
        # ------------------------------------------------------------------

        self.frame_botones2 = LabelFrame(self.master)

        self.btn_guardar=Button(self.frame_botones2, text="Guardar", command=self.fGuardar, width=60, bg='Green',
                                fg='white')
        self.btn_guardar.grid(row=0, column=0, padx=5, pady=3, sticky='nsew')

        self.btn_cancelar=Button(self.frame_botones2, text="Cancelar", command=self.fCancelar, width=60, bg='black',
                                 fg='white')
        self.btn_cancelar.grid(row=0, column=1, padx=5, pady=3, sticky='nsew')

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((60, 40), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_botones2, text="Salir", image=self.photo3, width=130, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=2, padx=2, pady=3)

        # for widg in self.frame_botones2.winfo_children():
        #     widg.grid_configure(padx=5, pady=3, sticky='nsew')

        self.frame_botones2.pack(expand=0, side="top", fill=BOTH, pady=2, padx=5)

    # ------------------------------------------------------------------
    # ESTADOS
    # ------------------------------------------------------------------

    def estado_inicial(self):

        default = 'Pendiente'
        self.filtro_activo =  "rma WHERE rm_estado = '" + default + "' ORDER BY rm_fecha ASC"

        self.alta_modif = 0
        self.var_Id = -1

        una_fecha = date.today()
        self.strvar_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))

        self.limpiar_entrys()
        self.estado_entrys("disabled")
        self.estado_botones_dos("disabled")
        self.estado_botones_uno("normal")

    def limpiar_entrys(self):

        una_fecha = date.today()
        self.strvar_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_articulo.set(value="")
        self.strvar_proveedor.set(value="")
        self.strvar_problema.set(value="")
        self.strvar_cliente.set(value="")
        self.strvar_costo_venta.set(value="")
        self.strvar_observaciones.set(value="")
        self.combo_proceso.current(0)
        self.combo_estado.current(0)
        self.strvar_buscostring.set(value="")

    def estado_entrys(self, estado):

        self.entry_fecha.configure(state=estado)
        self.entry_articulo.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_problema.configure(state=estado)
        self.entry_cliente.configure(state=estado)
        self.entry_costo_venta.configure(state=estado)
        self.entry_observa.configure(state=estado)
        self.combo_proceso.configure(state=estado)
        self.combo_estado.configure(state=estado)
        self.entry_busqueda_rma.configure(state=estado)

    def estado_botones_uno(self, estado):

        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.btn_nuevo_rma.configure(state=estado)
        self.btn_edito_rma.configure(state=estado)
        self.btn_borro_rma.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_buscar.configure(state=estado)
        #self.btn_imprime_presup.configure(state=estado)
        self.entry_busqueda_rma.configure(state=estado)

    def estado_botones_dos(self, estado):

        self.btn_guardar.configure(state=estado)

    # ------------------------------------------------------------------
    # GRID
    # ------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_rma.get_children():
            self.grid_rma.delete(item)

    def llena_grilla(self, ult_tabla_id):

        datos = self.varRma.consultar_rma(self.filtro_activo)

        for row in datos:
            self.grid_rma.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4], row[5],
                                                                 row[6], row[7], row[8], row[9]))

        if len(self.grid_rma.get_children()) > 0:
               self.grid_rma.selection_set(self.grid_rma.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_rma.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_rma.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """

            if ult_tabla_id:
                """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """
                self.grid_rma.selection_set(rg)
                # Para que no me diga que no hay nada seleccionado
                self.grid_rma.focus(rg)
                # para que la linea seleccionada no me quede fuera del area visible del treeview
                self.grid_rma.yview(self.grid_rma.index(rg))
            else:
                # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
                self.mover_puntero_topend("END")

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def DobleClickGrid(self, event):
        self.fEdito_rma()

    def fNuevo_rma(self):

        self.alta_modif = 1
        self.estado_entrys("normal")
        self.estado_botones_dos("normal")
        self.estado_botones_uno("disabled")
        self.entry_fecha.focus()

    def fEdito_rma(self):

        self.selected = self.grid_rma.focus()
        self.clave = self.grid_rma.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.estado_entrys("normal")
        self.estado_botones_dos("normal")
        self.estado_botones_uno("disabled")
        self.entry_articulo.focus()

        self.var_Id = self.clave  #puede traer -1 , en ese caso seria un alta
        self.alta_modif = 2

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_rma.item(self.selected, 'values')

        una_fecha = datetime.strptime(valores[0], '%Y-%m-%d')
        self.strvar_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_articulo.set(value=valores[1])
        self.strvar_combo_proceso.set(value=valores[2])
        self.strvar_combo_estado.set(value=valores[3])
        self.strvar_proveedor.set(value=valores[4])
        self.strvar_cliente.set(value=valores[5])
        self.strvar_problema.set(value=valores[6])
        self.strvar_costo_venta.set(value=valores[7])
        self.strvar_observaciones.set(value=valores[8])

    def fBorro_rma(self):

        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_rma.focus()
        self.selected_ant = self.grid_rma.prev(self.selected)
        # guardo en clave el Id pero de la tabla (no son el mismo con el treeview)
        self.clave = self.grid_rma.item(self.selected, 'text')
        self.clave_ant = self.grid_rma.item(self.selected_ant, 'text')

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_rma.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        # Metodo que ellimina el registro
        self.varRma.eliminar_rma(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # 1- que articulo no este vacio
        if len(self.strvar_articulo.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de articulo", parent=self)
            self.entry_articulo.focus()
            return

        # Asi obtengo el Id del Grid (Treeview) de donde esta el foco (I006...I002...)
        self.selected = self.grid_rma.focus()
        # Asi obtengo la clave de la tabla (campo Id de la tabla - numero secuencial) que no es lo mismo que el del Treeview
        self.clave = self.grid_rma.item(self.selected, 'text')

        if self.alta_modif == 1:

            self.nuevo_art = str(self.strvar_articulo.get())
            self.varRma.insertar_registro(self.strvar_fecha.get(), self.strvar_articulo.get(),
            self.strvar_combo_proceso.get(), self.strvar_combo_estado.get(), self.strvar_proveedor.get(),
            self.strvar_cliente.get(), self.strvar_problema.get(), self.strvar_costo_venta.get(),
            self.strvar_observaciones.get())
            messagebox.showinfo("Guardar", "Nuevo registro creado correctamente", parent=self)

        elif self.alta_modif == 2:

            self.varRma.modificar_registro(self.var_Id, self.strvar_fecha.get(),
            self.strvar_articulo.get(), self.strvar_combo_proceso.get(), self.strvar_combo_estado.get(),
            self.strvar_proveedor.get(), self.strvar_cliente.get(), self.strvar_problema.get(),
            self.strvar_costo_venta.get(), self.strvar_observaciones.get())
            self.var_Id == -1
            messagebox.showinfo("Modificacion", "La modificacion del registro fue exitosa", parent=self)

        self.limpiar_Grid()
        self.estado_botones_uno("normal")
        self.estado_botones_dos("disabled")

        if self.alta_modif == 1:
            ultimo_tabla_id = self.varRma.traer_ultimo(0)
            self.llena_grilla(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla(self.clave)

        self.alta_modif = 0

        self.limpiar_entrys()
        self.estado_entrys("disabled")

    # ------------------------------------------------------------------
    # BOTONES
    # ------------------------------------------------------------------

    def fSalir(self):

        r = messagebox.askquestion("Salir", "Confirma Salida?", parent=self)
        if r == messagebox.NO:
            return
        self.master.destroy()

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys()
        self.estado_inicial()

    # ------------------------------------------------------------------
    # PUNTEROS
    # ------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_rma.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return

            # selecciono el Id primero de la lista en este caso
            self.grid_rma.selection_set(rg)
            # pone el primero Id
            self.grid_rma.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_rma.yview(self.grid_rma.index(self.grid_rma.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_rma.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_rma.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_rma.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_rma.yview(self.grid_rma.index(self.grid_rma.get_children()[-1]))

    def fShowall(self):

        self.selected = self.grid_rma.focus()
        self.clave = self.grid_rma.item(self.selected, 'text')
        self.filtro_activo = "rma ORDER BY rm_fecha"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    # ------------------------------------------------------------------
    # BUSQUEDAS
    # ------------------------------------------------------------------

    def fPendientes(self):

        default = 'Pendiente'
        self.filtro_activo =  "rma WHERE rm_estado = '" + default + "' ORDER BY rm_fecha ASC"
        self.limpiar_Grid()
        self.llena_grilla("")

    def fBuscar_rma(self):

        if len(self.strvar_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

        se_busca = self.strvar_buscostring.get()
        self.filtro_activo = "rma WHERE INSTR(rm_articulo, '" + se_busca + "') ORDER BY rm_fecha ASC"

        # self.filtro_activo = "resu_ventas WHERE INSTR(rv_cliente, '" + se_busca + "') > 0" \
        #                      + " OR " + "INSTR(nombres, '" + se_busca + "') > 0" \
        #                      + " ORDER BY apellido ASC"

        self.varRma.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_rma.selection()
        self.grid_rma.focus(item)

    # ------------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------------

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha.get())

        if retorno_VerFal == "":
            self.strvar_fecha.set(value=estado_antes)
            self.entry_fecha.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha.set(value=estado_antes)
            self.entry_fecha.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha.set(value=retorno_VerFal)
        return ("bien")

    # ------------------------------------------------------------------
    # INFORMES
    # ------------------------------------------------------------------

    def creopdf(self):

        # traigo el registro que quiero imprimir
        self.selected = self.grid_rma.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_rma.item(self.selected, 'text')

        # if self.clave == "":
        #     messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
        #     return

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
        # valores = self.grid_rma.item(self.selected, 'values')

        # armado de encabezado ------------------------------------------------------------
        sdf = date.today()          #,todatetime.strptime(valores[1], '%Y-%m-%d')
        feac = sdf.strftime('%d-%m-%Y')
        self.titulo = "RMA Estados"
        # self.pdf_numero_presupuesto = valores[0]
        # self.pdf_nombre_cliente = valores[2]
        # self.pdf_dolar_presupuesto = valores[3]
        # self.pdf_tasa_ganancia = valores[4]

        self.pdf_datos_encabezado = feac+' '+self.titulo
        # Imprimo el encabezado de pagina
        pdf.set_font('Arial', '', 8)
        # pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        # pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt=self.pdf_datos_encabezado, border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.cell(w=20, h=5, txt="Fecha", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=150, h=5, txt="Articulo", border=1, align='L', fill=0, ln=0)
        pdf.cell(w=20, h=5, txt="Estado", border=1, align='R', fill=0, ln=0)
        pdf.cell(w=0, h=5, txt="", border=0, align='L', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items = self.varRma.consultar_rma(self.filtro_activo)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 8)
        for row in self.items:

            fecha_conver = datetime.strftime(row[1], '%d-%m-%Y')
            pdf.cell(w=20, h=5, txt=fecha_conver, border=0, align='R', fill=0, ln=0)
            pdf.cell(w=150, h=5, txt=row[2], border=0, align='L', fill=0, ln=0)
            pdf.cell(w=20, h=5, txt=row[3], border=0, align='R', fill=0, ln=1)
            pdf.cell(w=150, h=5, txt="Proveedor: (" + row[4] + ") - Falla: (" + row[5] + ")", border=0, align='L', fill=0, ln=1)
            pdf.cell(w=150, h=5, txt="Observaciones: (" + row[6] + ")", border=0, align='L', fill=0, ln=1)

        #   # pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
        #   # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(neto_dolar_pesos, 2))), border=0, align='R', fill=0, ln=0)
        #   # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
        #     pdf.multi_cell(w=0, h=5, txt=str(row[3]), border=0, align='L', fill=0)
        #   # pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # pdf.cell(w=20, h=5, txt="Neto Dolar", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Bruto pesos", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Final", border=1, align='R', fill=0, ln=0)
        # pdf.multi_cell(w=0, h=5, txt="Estado", border=1, align='L', fill=0)

        # fecha_conver = fecha_str_reves_normal(self, valores[0])
        # pdf.cell(w=20, h=5, txt=fecha_conver, border=0, align='R', fill=0, ln=0)
        # pdf.cell(w=140, h=5, txt=valores[1], border=0, align='L', fill=0, ln=0)
        # pdf.cell(w=30, h=5, txt=valores[2], border=0, align='R', fill=0, ln=0)
        # pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)
        #
        # pdf.cell(w=50, h=5, txt="Proveedor: " + valores[3], border=0, align='L', fill=0, ln=1)
        # pdf.cell(w=50, h=5, txt="Fallo: " + valores[4], border=0, align='L', fill=0, ln=1)
        # pdf.cell(w=50, h=5, txt="Observaciones: " + valores[5], border=0, align='L', fill=0, ln=1)

        # # pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
        # # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(neto_dolar_pesos, 2))), border=0, align='R', fill=0, ln=0)
        # # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=str(row[3]), border=0, align='L', fill=0)


        # Espaciado -----------------------------------------------------------------------
#         pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        pdf.output('hoja.pdf')

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)
