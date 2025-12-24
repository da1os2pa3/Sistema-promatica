from funciones import *
from funcion_new import *
from recibos_ABM import *
# ----------------------------------------
#from tkinter import *
#from tkinter import ttk
from tkinter import messagebox
#import tkinter as tk
import tkinter.font as tkFont
from tkinter.scrolledtext import *
# ----------------------------------------
import os
from PDF_clase import *
from datetime import date, datetime
from PIL import Image, ImageTk
# ----------------------------------------

class clase_recibos(Frame):

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ---------------------------------------------------------------------------------
        # Instanciaciones
        # Objeto creado con la clase de ABM recibos
        self.varRecibos = datosRecibos(self.master)
        #self.varFuncion_new = ClaseFuncion_new(self.master, self.varRecibos)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # TITULOS
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 540
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # """ guarda en item el Id (I001, IB03, ..) del elemento fila en el que pase el puntero del mouse en este caso
        # fila 0 el método identify_row() se usa para saber qué fila(item) del Treev está bajo una posición del mouse."""
        # item = self.grid_recibos.identify_row(0)
        # """ En Tkinter(módulo ttk), el método selection_set() del Treeview se usa para seleccionar uno o varios
        #    ítems de forma programática(por código)."""
        # self.grid_recibos.selection_set(item)
        # """ pone el foco en el item seleccionado"""
        # self.grid_recibos.focus(item)

        # funciones
        # self.habilitar_text("disabled")
        # self.habilitar_btn_inino("disabled")
        # self.habilitar_btn_inisi("normal")
        # self.habilitar_btn_busqueda("normal")

    # ------------------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------------------

    def create_widgets(self):

        # ------------------------------------------------------------------------------
        # TITULOS
        # ------------------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('recibo.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_recibo = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_recibo = Label(self.frame_titulo_top, image=self.png_recibo, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Recibos",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_recibo.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS
        # --------------------------------------------------------------------------

        self.strvar_buscostring =tk.StringVar(value="")
        self.strvar_numero_recibo = tk.StringVar(value="0")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_nombre_cliente = tk.StringVar(value="")
        self.strvar_fecha_recibo = tk.StringVar(value="")
        self.strvar_importe_recibo = tk.StringVar(value="0.00")

        # --------------------------------------------------------------------------
        # VARIABLES ESPECIALES
        # --------------------------------------------------------------------------

        # La pongo aca porque si la saco arriba no tiene alcance en el scope
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        self.strvar_fecha_recibo.set(value=datetime.strftime(date.today(), "%d/%m/%Y"))

        # --------------------------------------------------------------------------
        # TREVIEEW
        # --------------------------------------------------------------------------

        self.frame_tvw_recibos=LabelFrame(self.master, text="Recibos", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_recibos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_recibos = ttk.Treeview(self.frame_tvw_recibos, height=5, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5"))

        self.grid_recibos.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_recibos.column("#0", width=40, anchor="center", minwidth=40)
        self.grid_recibos.column("col1", width=50, anchor="center", minwidth=40)
        self.grid_recibos.column("col2", width=60, anchor="center", minwidth=60)
        self.grid_recibos.column("col3", width=120, anchor="center", minwidth=100)
        self.grid_recibos.column("col4", width=100, anchor="center", minwidth=80)
        self.grid_recibos.column("col5", width=250, anchor="center", minwidth=220)

        self.grid_recibos.heading("#0", text="Id", anchor="center")
        self.grid_recibos.heading("col1", text="Numero", anchor="center")
        self.grid_recibos.heading("col2", text="Fecha", anchor="center")
        self.grid_recibos.heading("col3", text="Cliente", anchor="center")
        self.grid_recibos.heading("col4", text="Importe", anchor="center")
        self.grid_recibos.heading("col5", text="Detalle", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_recibos, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_recibos, orient=VERTICAL)
        self.grid_recibos.config(xscrollcommand=scroll_x.set)
        self.grid_recibos.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_recibos.xview)
        scroll_y.config(command=self.grid_recibos.yview)
        scroll_y.pack(side=RIGHT, fill="y")
        scroll_x.pack(side=BOTTOM, fill="x")
        self.grid_recibos['selectmode'] = 'browse'

        self.grid_recibos.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_recibos.pack(side=TOP, fill=BOTH, padx=5, pady=2)

        # Armado de los Frames
        self.frame_primero=LabelFrame(self.master, text="", foreground="red")
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # BOTONES DEL TREEVIEW
        # --------------------------------------------------------------------------------

        self.btn_nuevoitem = Button(self.frame_primero, text="Nuevo", command=self.fNuevo, width=24, bg="blue",
                                    fg="white")
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)
        self.btn_editaitem = Button(self.frame_primero, text="Editar", command=self.fEditar, width=24, bg="blue",
                                    fg="white")
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)
        self.btn_borraitem = Button(self.frame_primero, text="Eliminar", command=self.fBorrar, width=24, bg="red",
                                    fg="white")
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)
        self.btn_guardaritem = Button(self.frame_primero, text="Guardar", command=self.fGuardar, width=24, bg="green",
                                      fg="white")
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)
        self.btn_Cancelar = Button(self.frame_primero, text="Cancelar", command=self.fCancelar, width=24, bg="black",
                                   fg="white")
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_primero, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")

        self.frame_primero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # -------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------
        # BUSQUEDA
        # --------------------------------------------------------------------------------

        self.frame_tercero=LabelFrame(self.master, text="", foreground="red")

        self.lbl_buscar_recibo = Label(self.frame_tercero, text="Buscar: ", justify=LEFT)
        self.lbl_buscar_recibo.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.entry_buscar_recibo = Entry(self.frame_tercero, textvariable=self.strvar_buscostring, width=50)
        self.entry_buscar_recibo.grid(row=0, column=1, padx=5, pady=3, sticky=W)
        self.btn_buscar_movim = Button(self.frame_tercero, text="Buscar", command=self.fBuscar_en_tabla,
                                       bg="blue", fg="white", width=24)
        self.btn_buscar_movim.grid(row=0, column=2, padx=5, pady=3, sticky=W)
        self.btn_showall = Button(self.frame_tercero, text="Mostrar todo", command=self.fShowall,
                                  bg="blue", fg="white", width=24)
        self.btn_showall.grid(row=0, column=3, padx=5, pady=3, sticky=W)
        self.btn_reset_buscar = Button(self.frame_tercero, text="Limpiar busqueda", command=self.fReset_buscar,
                                       bg="blue", fg="white", width=24)
        self.btn_reset_buscar.grid(row=0, column=4, padx=5, pady=3, sticky=W)

        # ------------------------------------------------------------------------------
        # botones fin y principio archivo
        # --------------------------------------------------------------------------------

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_tercero, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=5, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_tercero, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=6, padx=5, sticky="nsew", pady=2)

        self.frame_tercero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # ENTRYS
        # --------------------------------------------------------------------------------

        self.frame_segundo=LabelFrame(self.master, text="", foreground="red")

        self.frame_segundo_1=LabelFrame(self.frame_segundo, text="", foreground="red")

        # NUMERO DE RECIBO
        fff = tkFont.Font(family="Arial", size=12, weight="bold")
        self.lbl_numero_recibo = Label(self.frame_segundo_1, text="Nº Recibo: ", justify=LEFT)
        self.lbl_numero_recibo.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_numero_recibo = Label(self.frame_segundo_1, textvariable=self.strvar_numero_recibo, font=fff,
                                         fg="blue", width=10, justify=RIGHT)
        self.entry_numero_recibo.grid(row=0, column=1, padx=5, pady=2, sticky=E)

        # FECHA DEL RECIBO
        self.lbl_fecha_recibo = Label(self.frame_segundo_1, text="Fecha: ", justify=LEFT)
        self.lbl_fecha_recibo.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.entry_fecha_recibo = Entry(self.frame_segundo_1, textvariable=self.strvar_fecha_recibo, width=10,
                                        justify=RIGHT)
        self.entry_fecha_recibo.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_recibo.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_segundo_1, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=5)

        # DATOS NOMBRE CLIENTE
        self.lbl_nombre_cliente = Label(self.frame_segundo_1, text="Cliente: ", justify=LEFT)
        self.lbl_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_segundo_1, textvariable=self.strvar_nombre_cliente, width=52)
        self.entry_nombre_cliente.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        self.lbl_codigo_cliente = Label(self.frame_segundo_1, text="(" + self.strvar_codigo_cliente.get() + ")",
                                        justify=LEFT)
        self.lbl_codigo_cliente.grid(row=0, column=7, padx=2, pady=2, sticky=W)

        # IMPORTE RECIBO
        self.lbl_importe_recibo = Label(self.frame_segundo_1, text="Importe: ", justify=LEFT)
        self.lbl_importe_recibo.grid(row=0, column=8, padx=5, pady=2, sticky=W)
        self.entry_importe_recibo = Entry(self.frame_segundo_1, textvariable=self.strvar_importe_recibo, width=20,
                                          justify=RIGHT)
        self.entry_importe_recibo.config(validate="key", validatecommand=self.vcmd)
        self.entry_importe_recibo.grid(row=0, column=9, padx=5, pady=2, sticky=W)
        self.entry_importe_recibo.bind('<Tab>', lambda e: self.controlar())
        self.strvar_importe_recibo.trace("w", lambda *args: limitador(self.strvar_importe_recibo, 15))

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = Button(self.frame_segundo_1, image=self.photo_imp, pady=3, command=self.fImprime, border=3)
        self.btn_imprime.grid(row=0, column=10, padx=4, pady=2)

        self.frame_segundo_1.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        self.frame_segundo_2=LabelFrame(self.frame_segundo, text="Detalle recibo", foreground="red")

        # DETALLE Novedades
        self.text_detalle = ScrolledText(self.frame_segundo_2)
        self.text_detalle.config(width=120, height=6, wrap="word", padx=4, pady=3)
        self.text_detalle.grid(row=1, column=1, padx=4, pady=5, sticky="nsew")

        self.frame_segundo_2.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=3)

        self.frame_segundo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=3)

    # -----------------------------------------------------------------------------
    # GRID
    # -----------------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_recibos.get_children():
            self.grid_recibos.delete(item)

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varRecibos.consultar_recibos(self.filtro_activo)
        else:
            datos = self.varRecibos.consultar_recibos("recibos ORDER BY cc_fecha ASC")

        for row in datos:

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'), "hora_no")
            self.grid_recibos.insert("", END, text=row[0], values=(row[1], forma_normal, row[4], row[5], row[6]))

        if len(self.grid_recibos.get_children()) > 0:
            self.grid_recibos.selection_set(self.grid_recibos.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_recibos.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_recibos.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """
            """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_recibos.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_recibos.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_recibos.yview(self.grid_recibos.index(rg))
        else:
            self.mover_puntero_topend("END")

    # -----------------------------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo = "recibos ORDER BY rc_fecha ASC"
        self.dato_seleccion = ""
        self.var_Id = -1
        self.alta_modif = 0

        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_inino("disabled")
        self.habilitar_btn_inisi("normal")
        self.habilitar_btn_busqueda("normal")

    def limpiar_text(self):

        self.strvar_fecha_recibo.set(value=datetime.strftime(date.today(), "%d/%m/%Y"))
        self.strvar_codigo_cliente.set(value="0")
        self.strvar_nombre_cliente.set(value="")
        self.strvar_importe_recibo.set(value="0")
        self.text_detalle.delete('1.0', 'end')
        self.strvar_buscostring.set(value="")

    def habilitar_text(self, estado):

        self.entry_fecha_recibo.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_importe_recibo.configure(state=estado)
        self.text_detalle.configure(state=estado)

    def habilitar_btn_inino(self, estado):

        self.btn_guardaritem.configure(state=estado)
        self.btn_Cancelar.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)

    def habilitar_btn_inisi(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)
        self.btn_imprime.configure(state=estado)
        self.entry_buscar_recibo.configure(state=estado)

    def habilitar_btn_busqueda(self, estado):

        self.btn_buscar_movim.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_reset_buscar.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)

    # -----------------------------------------------------------------------------
    # CRUD
    # -----------------------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.strvar_fecha_recibo.set(value=datetime.strftime(date.today(), "%d/%m/%Y"))

        self.habilitar_text("normal")
        self.habilitar_btn_inino("normal")
        self.habilitar_btn_inisi("disabled")
        self.habilitar_btn_busqueda("disabled")
        self.entry_fecha_recibo.focus()
        self.strvar_numero_recibo.set(value=(int(self.varRecibos.traer_ultimo(1)) + 1))

    def fEditar(self):

        self.alta_modif = 2

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_recibos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_recibos.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta
        self.habilitar_text('normal')
        self.limpiar_text()

        self.filtro_activo = "recibos WHERE Id = " + str(self.clave)

        valores = self.varRecibos.consultar_recibos(self.filtro_activo)

        self.filtro_activo = "recibos ORDER BY rc_fecha ASC"

        for row in valores:

            # Convierto fechas a dd/mm/aaa
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'), "hora_no")

            self.strvar_fecha_recibo.set(value=forma_normal)
            self.strvar_numero_recibo.set(value=row[1])
            self.strvar_nombre_cliente.set(value=row[4])
            self.strvar_importe_recibo.set(value=row[5])
            self.text_detalle.insert(END, row[6])

            self.habilitar_text("normal")
            self.habilitar_btn_inino("normal")
            self.habilitar_btn_inisi("disabled")
            self.habilitar_btn_busqueda("disabled")

            self.entry_fecha_recibo.focus()

    def fBorrar(self):

        # -----------------------------------------------------------
        """ Guardo en self.selected, el Id del item del grid o treeview (I010, IB14.... """
        self.selected = self.grid_recibos.focus()
        self.selected_ant = self.grid_recibos.prev(self.selected)
        """ Guardo en self. clave, el Id del treeview de la primer columna (12 . 23 . 25.....) """
        self.clave = self.grid_recibos.item(self.selected, 'text')
        self.clave_ant = self.grid_recibos.item(self.selected_ant, 'text')
        # -----------------------------------------------------------

        if self.clave == "" or self.selected == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # -----------------------------------------------------------
        """ Guardo en valores la lista con todos los valores de la fila del grid correspondiente al que voy a borrar """
        valores = self.grid_recibos.item(self.selected, 'values')
        """ En data guardo codigo y nombre del que voy a borrar para mostrar en el messagebox """
        data = str(self.clave)+" "+valores[2]
        # -----------------------------------------------------------

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        self.varRecibos.eliminar_item_recibos(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # --------------------------------------------------------------------
        # VALIDACIONES

        # FECHA
        if self.strvar_fecha_recibo.get() == "":
            messagebox.showerror("Error", "Fecha en blanco", parent=self)
            self.entry_fecha_recibo.focus()
            return
        # Importe
        if float(self.strvar_importe_recibo.get()) == 0:
            messagebox.showerror("Error", "Importe en cero", parent=self)
            self.entry_importe_recibo.focus()
            return
        # Nombre de cliente
        if self.strvar_nombre_cliente.get() == "":
            messagebox.showerror("Error", "Indique cliente", parent=self)
            self.entry_nombre_cliente.focus()
            return

        try:

            # guardo el Id del Treeview (I001, IB00, ...) en selected para ubicacion del foco a posteriori
            self.selected = self.grid_recibos.focus()
            # Guardo el Id del registro de la Tabla (no es el mismo que el otro, este puedo verlo en la base (12, 20...)
            self.clave = self.grid_recibos.item(self.selected, 'text')
            # self.nuevo_itemrec = ""

            if self.alta_modif == 1:

                # guardo movimiento
                fecha_aux = datetime.strptime(self.strvar_fecha_recibo.get(), '%d/%m/%Y')
                self.varRecibos.insertar_recibo(self.strvar_numero_recibo.get(), fecha_aux,
                                self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                self.strvar_importe_recibo.get(), self.text_detalle.get(1.0, 'end-1c'))

                messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

            else:

                fecha_aux = datetime.strptime(self.strvar_fecha_recibo.get(), '%d/%m/%Y')
                self.varRecibos.modificar_recibos(self.var_Id, self.strvar_numero_recibo.get(), fecha_aux,
                                                  self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                                  self.strvar_importe_recibo.get(),
                                                  self.text_detalle.get(1.0, 'end-1c'))

                self.var_Id == -1

                messagebox.showinfo("Modificacion", "La modificacion fue exitosa", parent=self)

            # cierre de las novedades y reseteando pantalla para nuevo movimiento - actualizando grilla
            self.limpiar_Grid()
            self.limpiar_text()

            if self.alta_modif == 1:
                ultimo_tabla_id = self.varRecibos.traer_ultimo(0)
                self.llena_grilla(ultimo_tabla_id)
            elif self.alta_modif == 2:
                self.llena_grilla(self.clave)

        except:

            messagebox.showerror("Error", "Error inesperado - Funcion guardar", parent=self)
            return

        self.habilitar_text("disabled")
        self.habilitar_btn_inino("disabled")
        self.habilitar_btn_inisi("normal")
        self.strvar_numero_recibo.set(value=(int(self.varRecibos.traer_ultimo(1)) + 1))
        self.grid_recibos.focus()

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)

        if r == messagebox.YES:

            self.fShowall()
            self.limpiar_text()
            self.habilitar_text("disabled")
            self.habilitar_btn_inino("disabled")
            self.habilitar_btn_inisi("normal")
            self.habilitar_btn_busqueda("normal")
            self.strvar_numero_recibo.set(value=(int(self.varRecibos.traer_ultimo(1)) + 1))
            self.grid_recibos.focus()

    def fSalir(self):
        self.master.destroy()

    # -----------------------------------------------------------------------------
    # PUNTEROS
    # -----------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_recibos.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_recibos.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_recibos.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_recibos.yview(self.grid_recibos.index(self.grid_recibos.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_recibos.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_recibos.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_recibos.focus(rg)
            # lleva el foco al final del treeview
            self.grid_recibos.yview(self.grid_recibos.index(self.grid_recibos.get_children()[-1]))

    # -----------------------------------------------------------------------------
    # BUSQUEDAS
    # -----------------------------------------------------------------------------

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.strvar_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.strvar_buscostring.get()

        self.filtro_anterior = self.filtro_activo

        self.filtro_activo = ("recibos WHERE INSTR(rc_nomcli, '" + se_busca + "') > 0")

        self.varRecibos.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_recibos.selection()
        self.grid_recibos.focus(item)

    def fShowall(self):

        self.filtro_activo = "recibos ORDER BY rc_fecha ASC"
        self.selected = self.grid_recibos.focus()
        self.clave = self.grid_recibos.item(self.selected, 'text')
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    def fReset_buscar(self):

        self.strvar_buscostring.set(value="")
        self.fShowall()

    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en que
        campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden 
        de como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido 
        arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                                                        "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:
            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    def DobleClickGrid(self, event):
        self.fEditar()

    # -----------------------------------------------------------------------------
    # VALIDACIONES
    # -----------------------------------------------------------------------------

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_recibo.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_recibo.get())

        if retorno_VerFal == "":
            self.strvar_fecha_recibo.set(value=estado_antes)
            self.entry_fecha_recibo.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_recibo.set(value=estado_antes)
            self.entry_fecha_recibo.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_recibo.set(value=retorno_VerFal)
        return ("bien")

    # def limitador(self, entry_text, caract):
    #
    #     if len(entry_text.get()) > 0:
    #         # donde esta CARACT va la cantidad de caracteres
    #         entry_text.set(entry_text.get()[:caract])

    def controlar(self):

        # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
        if not control_forma(list(self.strvar_importe_recibo.get())):
            self.strvar_importe_recibo.set(value="0")
            self.entry_importe_recibo.focus()
            return
        # Valido que los campos no me ingresen en blanco
        if self.strvar_importe_recibo.get() == "" or self.strvar_importe_recibo.get() == "-" or self.strvar_importe_recibo.get() == ".":
            self.strvar_importe_recibo.set(value="0")
            self.entry_importe_recibo.focus()
            return
        else:
            self.strvar_importe_recibo.set(value=round(float(self.strvar_importe_recibo.get()), 2))

    # -----------------------------------------------------------------------------
    # INFORMES - PDF
    # -----------------------------------------------------------------------------

    def fImprime(self):

        # traigo el registro que quiero imprimir
        self.selected = self.grid_recibos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_recibos.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # Debo filtrar el cliente seleccionado
        # adad = self.strvar_codigo_cliente.get()
        # datos_registro_selec = self.varRecibos.consultar_recibos("recibos WHERE rc_codcli = '" + adad + "' ORDER BY rc_fecha ASC")

        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """

        # esto siempre debe estar ------------------------------------------------------------
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 12)
        # -----------------------------------------------------------------------------------

        valores = self.grid_recibos.item(self.selected, 'values')
        numero_recibo = valores[0]
        feac = valores[1]
        cliente = valores[2]
        importe = valores[3]
        detalle = valores[4]

        # armado de encabezado --------------------------------------------------------------
        # feactual = datetime.now()
        # feac = self.strvar_fecha_recibo.get()    #feactual.strftime("%d-%m-%Y %H:%M:%S")

        # Imprimo el encabezado de pagina ---------------------------------------------------
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0, h=5, txt="Recibo Nº: " + str(numero_recibo) + " - Fecha y Hora: " + feac , border=1, align='C',
                 fill=0, ln=1)
        # -----------------------------------------------------------------------------------

        importe_format = formatear_cifra(float(importe))

        var_descripcion = ("Recibi del Sr./a " + cliente + " la suma de pesos " + importe_format +" "+
                           numero_to_letras(float(importe)) + ", segun el siguiente detalle: " + " " + detalle )

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=var_descripcion, align='L', fill=0)
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        pdf.multi_cell(w=0, h=5, txt="Total recibido $: "+importe_format+"----------------------", align='L', fill=0)
        pdf.cell(w=0, h=15, txt='', align='L', fill=0, ln=1)

        pdf.multi_cell(w=0, h=5, txt="...........................................", align='R', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)
        pdf.multi_cell(w=0, h=5, txt="Promatica Computacion", align='R', fill=0)

#         pdf.cell(w=15, h=8, txt=var_descripcion, border=1, align='C', fill=0)
#         pdf.cell(w=100, h=8, txt='Detalle', border=1, align='C', fill=0)
#         pdf.cell(w=20, h=8, txt='Ingreso', border=1, align='C', fill=0)
#         pdf.cell(w=20, h=8, txt='Egreso', border=1, align='C', fill=0)
#         pdf.multi_cell(w=0, h=8, txt=var_descripcion, border=0, align='C', fill=0)
#         # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)
#         pdf.set_font('Arial', '', 5)

#         tot_saldo = 0
#         for row in datos_registro_selec:

#             fecha1 = datetime.strftime(row[1], "%d-%m-%Y")
#             tot_saldo += row[3] - row[4]
#             pdf.cell(w=15, h=6, txt=var_descripcion, border=1, align='C', fill=0)
#             pdf.cell(w=100, h=6, txt=row[2], border=1, align='C', fill=0)
#             pdf.cell(w=20, h=6, txt=str(row[3]), border=1, align='C', fill=0)
#             pdf.cell(w=20, h=6, txt=str(row[4]), border=1, align='C', fill=0)
#             pdf.multi_cell(w=0, h=6, txt=str(tot_saldo), border=1, align='E', fill=0)

        pdf.output('hoja.pdf')
        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)
