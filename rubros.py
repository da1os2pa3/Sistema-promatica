from rubros_ABM import *
# -------------------------------------
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# -------------------------------------
from PIL import Image, ImageTk

class Vent_rubros(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Seteo pantalla master principal -------------------------------------------------
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # Instanciaciones -----------------------------------------------------------------
        # Creo una instancia de la clase rubros ABM
        self.varRubros = datosRubros(self.master)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ---------------------------------------------------------------------------------
        master.resizable(0, 0)
        """  Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
             mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = master.winfo_screenwidth()
        htotal = master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 670
        hventana = 490
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        # Se lo aplicamos a la geometría de la ventana
        master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()

        self.llena_grilla("")

        item = self.grid_rubros.identify_row(0)
        self.grid_rubros.selection_set(item)
        self.grid_rubros.focus(item)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # ESTADO INICIAL

        self.habilitar_text("disabled")
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")

    # --------------------------------------------------------------------------
    # WIDGETS
    # --------------------------------------------------------------------------

    def create_widgets(self):

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES

        self.filtro_activo = "rubros ORDER BY ru_nombre ASC"
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.var_Id = -1
        self.alta_modif = 0
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # TITULOS

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('rubro.png')
        self.photo3 = self.photo3.resize((75, 75), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_rubros = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_rubros = Label(self.frame_titulo_top, image=self.png_rubros, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=16, text="Rubros",
                                bg="black", fg="gold", font=("Arial bold", 38, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_rubros.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS

        self.strvar_nombre = StringVar(value="")
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # CUADRO DE BOTONES

        # Armar un frame para colocar los botones
        barra_botones = LabelFrame(self.master)

        # -------------------------------------------------------------------------
        # BOTONES 1

        botones1 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        # Instalacion botones
        self.btnNuevo = Button(botones1, text="Nuevo", command=self.fNuevo, bg="blue", fg="white", width=10)
        self.btnNuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        self.btnModificar = Button(botones1, text="Modificar", command=self.fEeditar, bg="blue", fg="white", width=10)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        self.btnEliminar = Button(botones1, text="Eliminar", command=self.fEliminar, bg="red", fg="white", width=10)
        self.btnEliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        self.btnGuardar = Button(botones1, text="Guardar", command=self.fGuardar, bg="green", fg="white", width=10)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=3, columnspan=2)
        self.btnCancelar = Button(botones1, text="Cancelar", command=self.fCancelar, bg="black", fg="white", width=10)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=3, columnspan=2)

        botones1.pack(side=TOP, padx=3, pady=3, fill=Y)

        # -------------------------------------------------------------------------
        # BOTONES 2

        botones2 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(botones2, text="", image=self.photo4, command=self.fToparch, bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(botones2, text="", image=self.photo5, command=self.fFinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=1, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")
        self.btn_reset = Button(botones2, text="Reset", width=11, command=self.fReset, bg="black", fg="white")
        self.btn_reset.grid(row=2, column=0, padx=6, pady=3, ipadx=10)

        botones2.pack(side=TOP, padx=3, pady=3, fill=Y)

        # -------------------------------------------------------------------------
        # BOTONES 3

        botones3 = LabelFrame(barra_botones, bd=5, relief=RIDGE)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = Button(botones3, text="Salir", image=self.photo3, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        botones3.pack(side=TOP, padx=3, pady=3, fill=Y)

        # -------------------------------------------------------------------------
        # PACK - frame de botones
        barra_botones.pack(side=LEFT, padx=15, pady=5, ipady=5, fill=Y)

        # --------------------------------------------------------------------------
        # BUSQUEDAS

        self.frame_tv = Frame(self.master)

        # FRAME dentro del frame principal para poner la llinea de busqueda
        self.frame_buscar = LabelFrame(self.frame_tv)

        # BUSCAR Linea de label y entry de busqueda
        self.lbl_buscar_rubro = Label(self.frame_buscar, text="Buscar: ")
        self.lbl_buscar_rubro.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_rubro = Entry(self.frame_buscar, width=21)
        self.entry_buscar_rubro.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.btn_buscar_rubro = Button(self.frame_buscar, text="Buscar", command=self.fBuscar_en_tabla, bg="blue",
                                       fg="white", width=17)
        self.btn_buscar_rubro.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_show_all = Button(self.frame_buscar, text="Mostrar todo", command=self.fShow_all, bg="blue",
                                   fg="white", width=17)
        self.btn_show_all.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        self.frame_buscar.pack(expand=1, fill=X, pady=10, padx=5)
        self.frame_buscar.pack(expand=1, fill=X, pady=10, padx=10)

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.frame_tv)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # TREEVIEW

        self.grid_rubros = ttk.Treeview(self.frame_tv, columns=("col1"))
        self.grid_rubros.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_rubros.column("#0", width=60, anchor=CENTER)
        self.grid_rubros.column("col1", width=250, anchor=CENTER)

        self.grid_rubros.heading("#0", text="Id", anchor=CENTER)
        self.grid_rubros.heading("col1", text="Nombre", anchor=CENTER)

        self.grid_rubros.tag_configure('oddrow', background='light grey')
        self.grid_rubros.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tv, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tv, orient=VERTICAL)
        self.grid_rubros.config(xscrollcommand=scroll_x.set)
        self.grid_rubros.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_rubros.xview)
        scroll_y.config(command=self.grid_rubros.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_rubros['selectmode'] = 'browse'

        # PACK - de el treeview y el FRAME tv
        self.frame_buscar.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=3)
        self.grid_rubros.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=5)
        self.frame_tv.pack(side=TOP, fill=BOTH, padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ENTRYS

        self.sector_entry = LabelFrame(self.master)

        # NOMBRE
        self.lbl_nombre = Label(self.sector_entry, text="Nombre: ")
        self.lbl_nombre.grid(row=0, column=0, padx=10, pady=3, sticky=W)
        self.entry_nombre = Entry(self.sector_entry, textvariable=self.strvar_nombre, justify="left", width=50)
        self.strvar_nombre.trace("w", lambda *args: self.limitador(self.strvar_nombre, 40))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=3, sticky=W)

        # PACK del frame "sector_entry"
        self.sector_entry.pack(expand=1, fill=X, pady=5, padx=5)

    # --------------------------------------------------------------------------
    #  GRID
    # --------------------------------------------------------------------------

    def limpiar_Grid(self):
        for item in self.grid_rubros.get_children():
            self.grid_rubros.delete(item)

    def llena_grilla(self, ult_tabla_id):

        # ----------------------------------------------------------------------------------
        # Insert normal en el GRID

        if len(self.filtro_activo) > 0:
            datos = self.varRubros.consultar_rubros(self.filtro_activo)
        else:
            datos = self.varRubros.consultar_rubros("rubros ORDER BY ru_nombre ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_rubros.insert("", END, tags=color, text=row[0], values=(row[1]))

        """ Deberia estudiar esta funcion... creo que es para poner el foco en el primero"""
        if len(self.grid_rubros.get_children()) > 0:
            self.grid_rubros.selection_set(self.grid_rubros.get_children()[0])
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_rubros.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_rubros.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """

            if ult_tabla_id:

                """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

                self.grid_rubros.selection_set(rg)
                # Para que no me diga que no hay nada seleccionado
                self.grid_rubros.focus(rg)
                # para que la linea seleccionada no me quede fuera del area visible del treeview
                self.grid_rubros.yview(self.grid_rubros.index(rg))

    # --------------------------------------------------------------------------
    #  ESTADOS WIDGETS
    # --------------------------------------------------------------------------

    def habilitar_text(self, estado):

        self.entry_nombre.configure(state=estado)

    def limpiar_text(self):

        self.entry_nombre.delete(0, END)
        self.entry_nombre.delete(0, END)

    def habilitar_Btn_Oper(self, estado):

        self.btnNuevo.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.entry_buscar_rubro.configure(state=estado)
        self.btn_buscar_rubro.configure(state=estado)

        if estado == "disabled":
            self.grid_rubros['selectmode'] = 'none'
        else:
            self.grid_rubros['selectmode'] = 'browse'

        if self.alta_modif == 2:
            self.grid_rubros['selectmode'] = 'browse'

    def habilitar_Btn_Final(self, estado):

        self.btnGuardar.configure(state=estado)

    # --------------------------------------------------------------------------
    # CRUD
    # --------------------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.habilitar_Btn_Final("normal")
        self.habilitar_Btn_Oper("disabled")
        self.limpiar_text()
        self.entry_nombre.focus()

    def fEeditar(self):

        self.selected = self.grid_rubros.focus()
        self.clave = self.grid_rubros.item(self.selected, 'text')
        #self.valores = self.grid_rubros.item(self.selected, 'values')

        self.alta_modif = 2          # MODIFICACION

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        self.var_Id = self.clave  #puede traer -1 , en ese caso seria un alta
        self.habilitar_text('normal')

        self.valores = self.grid_rubros.item(self.selected, 'values')

        self.limpiar_text()
        self.entry_nombre.insert(0, self.valores[0])
        self.habilitar_Btn_Final("normal")
        self.habilitar_Btn_Oper("disabled")
        self.entry_nombre.focus()

    def fEliminar(self):

        # ------------------------------------------------------------------------------
        self.selected = self.grid_rubros.focus()
        self.selected_ant = self.grid_rubros.prev(self.selected)
        # clave = Id del registro en la Tabla (45,23,99--......
        self.clave = self.grid_rubros.item(self.selected, 'text')
        self.clave_ant = self.grid_rubros.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # ------------------------------------------------------------------------------
        # cargo los valores desde el GRID
        self.valores = self.grid_rubros.item(self.selected, 'values')
        data = str(self.clave)+" "+self.valores[0]
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Verifico tabla articulos y si el rubro ya existe asignado, lo modifico en todas sus apariciones
        exis = self.varRubros.verifica_articulos(self.valores[0])

        if exis != 0:
            # El rubro SI esta asignado en articulos
            r2 = messagebox.askquestion("Eliminar", "Existen articulos asignados al rubro y se "
                                                    "modificaran, Continua?\n " + self.valores[0], parent=self)
            if r2 == messagebox.NO:
                messagebox.showinfo("Eliminar", "Se cancelo la eliminacion del Registro", parent=self)
                return
        else:
            r = messagebox.askquestion("Eliminar", "Confirma eliminar Rubro?\n " + data, parent=self)
            if r == messagebox.NO:
                messagebox.showinfo("Eliminar", "Se cancelo la eliminacion del Registro", parent=self)
                return
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        """ Si confirman eliminar el rubro, primero elimino el rubro y luego lo borro de los
        articulos que lo tengan asignado """

        # -----------------------------------------------------------------------------
        # ELIMINO EL RUBRO
        self.varRubros.eliminar_rubros(self.clave)
        # -----------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # QUITO LA ASIGNACION DEL RUBRO EN TABLA ARTICULOS
        if exis != 0:
            self.varRubros.quitarubro(self.valores[0])
        # --------------------------------------------------------------------------

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        """ Vuelvo al inmediato anterior segun el orden establecido en el grid """
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # VALIDACIONES
        if self.entry_nombre.get() == "":
            messagebox.showwarning("Alerta", "No ingreso Rubro", parent=self)
            self.entry_nombre.focus()
            return

        if self.alta_modif == 1:

            self.varRubros.insertar_rubros(self.strvar_nombre.get())
            messagebox.showinfo("Guardar", "Nuevo registro creado correctamente", parent=self)

        elif self.alta_modif == 2:

            # Verifico tabla articulos y si el rubro ya existe asignado, lo modifico en todas sus apariciones
            exis = self.varRubros.verifica_articulos(self.valores[0])

            # si la marca existe, pido confirmacion de borrarlo en los articulos que lo tengan asignado
            if exis != 0:
                r2 = messagebox.askquestion("Modificar", "Existen articulos asignados al rubro y se "
                                                         "modificaran, Continua?\n " + self.valores[0], parent=self)
                if r2 == messagebox.NO:
                    return

            # Modificamos ya el rubro en la tabla rubros pasando el Id
            self.varRubros.modificar_rubros(self.var_Id, self.strvar_nombre.get())

            if exis != 0:
                # Modifica el rubro en los articulos por la modificacion
                self.varRubros.modi_rub_enart(self.strvar_nombre.get(), self.valores[0])

            self.var_Id == -1
            messagebox.showinfo("Modificacion", "La modificacion del registro fue exitosa", parent=self)

        self.limpiar_Grid()
#        self.llena_grilla("")
        self.limpiar_text()
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")
        self.habilitar_text("disabled")

        if self.alta_modif == 1:
            ultimo_tabla_id = self.varRubros.traer_ultimo(0)
            self.llena_grilla(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla(self.clave)

        self.alta_modif = 0

    # --------------------------------------------------------------------------
    # CANCELAR - SALIR
    # --------------------------------------------------------------------------

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.limpiar_text()
            self.habilitar_Btn_Final("disabled")
            self.habilitar_Btn_Oper("normal")
            self.habilitar_text("disabled")

    def fSalir(self):
        self.master.destroy()

    def fReset(self):

        self.entry_buscar_rubro.delete(0, END)
        self.selected = self.grid_rubros.focus()
        self.clave = self.grid_rubros.item(self.selected, 'text')
        self.filtro_activo = "rubros ORDER BY ru_nombre ASC"
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.limpiar_Grid()
        self.llena_grilla("")
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")

    # --------------------------------------------------------------------------
    # VARIOS
    # --------------------------------------------------------------------------

    def DobleClickGrid(self, event):
        self.fEeditar()

    def limitador(self, entry_text, caract):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:caract])

    # --------------------------------------------------------------------------
    # PUNTEROS
    # --------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def fShow_all(self):

        self.selected = self.grid_rubros.focus()
        self.clave = self.grid_rubros.item(self.selected, 'text')
        self.filtro_activo = "rubros ORDER BY ru_nombre ASC"
        self.entry_buscar_rubro.delete(0, END)
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    # --------------------------------------------------------------------------
    # BUSQUEDAS
    # --------------------------------------------------------------------------

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.entry_buscar_rubro.get()) < 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.entry_buscar_rubro.get()
        self.filtro_activo = "rubros WHERE INSTR(ru_nombre, '" + se_busca + "') > 0" \
                             + " ORDER BY ru_nombre ASC"

        self.varRubros.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_rubros.selection()
        self.grid_rubros.focus(item)

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_rubros.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_rubros.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_rubros.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_rubros.yview(self.grid_rubros.index(self.grid_rubros.get_children()[0]))
        elif param_topend == 'END':
            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_rubros.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_rubros.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_rubros.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_rubros.yview(self.grid_rubros.index(self.grid_rubros.get_children()[-1]))
