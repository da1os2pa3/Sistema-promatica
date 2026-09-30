import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from funcion_new import ClaseFuncionNew
from funciones import *
from rubros_ABM import DatosRubros
from status_bar import StatusBar


class ClaseRubros(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)


        # Seteo pantalla master principal -------------------------------------------------
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # Instanciaciones -----------------------------------------------------------------
        # Creo una instancia de la clase rubros ABM
        self.varRubros = DatosRubros(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # ---------------------------------------------------------------------------------

        self.pantalla()
        self.create_widgets()
        self.llena_grilla("")

        # ---------------------------------------------------------------------------------
        item = self.grid_rubros.identify_row(0)
        self.grid_rubros.selection_set(item)
        self.grid_rubros.focus(item)
        # -----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        # ESTADO INICIAL
        self.habilitar_text("disabled")
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")

    # --------------------------------------------------------------------------
    # WIDGETS
    # --------------------------------------------------------------------------

    def create_widgets(self):

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES
        self.filtro_activo = "ORDER BY ru_nombre ASC"
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.alta_modif = 0
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # TITULOS
        self.frame_titulo_superior = tk.Frame(self.master)
        self.titulo_logo()
        self.frame_titulo_superior.pack(side="top", fill="x", padx=5, pady=5)
        # --------------------------------------------------------------------------
        # STRINGVARS
        self.sv_nombre_rubro = tk.StringVar(value="")

        # -------------------------------------------------------------------------
        # CUADRO DE BOTONES
        barra_botones = tk.LabelFrame(self.master)
        # -------------------------------------------------------------------------
        # BOTONES 1
        self.cuadro_botones_crud = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.botones_crud()
        self.cuadro_botones_crud.pack(side="top", padx=3, pady=3, fill="y")
        # -------------------------------------------------------------------------
        # BOTONES 2
        self.cuadro_botones_grid = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.botones_grid()
        self.cuadro_botones_grid.pack(side="top", padx=3, pady=3, fill="y")
        # -------------------------------------------------------------------------
        # BOTONES 3
        self.cuadro_boton_salir = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.boton_salir()
        self.cuadro_boton_salir.pack(side="top", padx=3, pady=3, fill="y")
        barra_botones.pack(side="left", padx=15, pady=5, ipady=5, fill="y")
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # BUSQUEDAS Y GRID
        self.cuadro_grid = tk.Frame(self.master)

        # FRAME dentro del frame principal para poner la llinea de busqueda
        self.cuadro_buscar = tk.LabelFrame(self.cuadro_grid)
        self.linea_buscador()
        self.cuadro_buscar.pack(expand=1, fill="x", pady=10, padx=10)

        self.armado_grid()

        self.cuadro_grid.pack(side="top", fill="both", padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ENTRYS
        self.cuadro_entrys = tk.LabelFrame(self.master)
        self.entradas_entrys()
        self.cuadro_entrys.pack(expand=1, fill="x", pady=5, padx=5)

    # --------------------------------------------------------------------------
    #  GRID FUNCIONES
    # --------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_rubros.get_children():
            self.grid_rubros.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varRubros.consultar_rubros(self.filtro_activo)
        else:
            datos = self.varRubros.consultar_rubros("ORDER BY ru_nombre ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_rubros.insert("", "end", tags=color, text=row[0], values=(row[1]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_rubros.get_children()
        # Si no hay filas (grid vacio), salgo sin intentar seleccionar
        if not children:
            self.status.set_status("ℹ Grid vacio...", "info")
            return

        # Si el parametro set_foco esta vacío (no hay foco), voy al ultimo de la grilla,
        # caso contrario, voy a la clave que se haya enviado en set_foco para dejar el puntero.
        if not set_foco:
            # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
            # posicion = children[-1]                      # ultimo
            posicion = children[0]                     # primero
            self.grid_rubros.focus_set()
            self.grid_rubros.focus(posicion)
            self.grid_rubros.selection_set(posicion)
            self.grid_rubros.see(posicion)
        else:
            for item in children:
                texto = self.grid_rubros.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_rubros.update_idletasks()
                    self.grid_rubros.focus_set()
                    self.grid_rubros.selection_set(item)
                    self.grid_rubros.focus(item)
                    self.grid_rubros.see(item)
                    break

    # --------------------------------------------------------------------------
    #  ESTADOS WIDGETS
    # --------------------------------------------------------------------------

    def habilitar_text(self, estado):

        self.entry_nombre_rubro.configure(state=estado)

    def limpiar_text(self):

        self.entry_nombre_rubro.delete(0, "end")
        self.entry_nombre_rubro.delete(0, "end")

    def habilitar_btn_oper(self, estado):

        self.btnNuevo.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.entry_buscar_rubro.configure(state=estado)
        self.btn_buscar_rubro.configure(state=estado)

    def habilitar_btn_final(self, estado):
        self.btnGuardar.configure(state=estado)

    # --------------------------------------------------------------------------
    # CRUD
    # --------------------------------------------------------------------------

    def fnuevo(self):

        self.alta_modif = 1
        self.habilitar_text("normal")
        self.habilitar_btn_final("normal")
        self.habilitar_btn_oper("disabled")
        self.limpiar_text()
        self.entry_nombre_rubro.focus()

    def feditar(self):

        self.selected = self.grid_rubros.focus()
        self.clave = self.grid_rubros.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2
        self.habilitar_text('normal')

        self.valores = self.grid_rubros.item(self.selected, 'values')

        self.limpiar_text()
        self.entry_nombre_rubro.insert(0, self.valores[0])
        self.habilitar_btn_final("normal")
        self.habilitar_btn_oper("disabled")
        self.entry_nombre_rubro.focus()

    def feliminar(self):

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

        """ Vuelvo al inmediato anterior segun el orden establecido en el grid """
        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # VALIDACIONES
        if self.entry_nombre_rubro.get() == "":
            messagebox.showwarning("Alerta", "No ingreso Rubro", parent=self)
            self.entry_nombre_rubro.focus()
            return

        # guardo el Id del Grid en selected para ubicacion del foco a posteriori --------------
        self.selected = self.grid_rubros.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_rubros.item(self.selected, 'text')
        # -------------------------------------------------------------------------------------

        # Preparo la fecha y pongo en la variable "dic_marcas" el diccionario completo con todos
        # los datos a ingresar a la tabla
        dic_rubros = self.get_rubros_dic()                  # funcion que genera el diccionario

        #-----------------------------------------------------------------
        # GUARDADO DATOS Y EVALUACION DEL PROCEDIMIENTO
        #-----------------------------------------------------------------
        id_ref = ""
        try:
            if self.alta_modif == 1:
                self.id_nuevo = self.varRubros.insertar_rubros(dic_rubros)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                # Verifico tabla articulos y si la marca ya existe asignada, lo modifico en todas sus apariciones
                exis = self.varRubros.verifica_articulos(self.valores[0])

                # si la marca existe, pido confirmacion de modificarlos en los articulos que lo tengan asignado
                if exis != 0:
                    r2 = messagebox.askquestion("Modificar", "Existen articulos asignados al rubro y "
                                                             "se modificaran, Continua?\n " + self.valores[0], parent=self)
                    if r2 == messagebox.NO:
                        return

                # Modificamos ya la marca en la tabla marcas pasando el Id -----
                self.varRubros.modificar_rubros(dic_rubros)
                # --------------------------------------------------------------

                id_ref = self.clave
                if exis != 0:
                    # Modifica la marca en los articulos por la modificacion
                    self.varRubros.modi_rub_enart(self.sv_nombre_rubro.get(), self.valores[0])

        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Insertar/Modificar", str(e))
            return
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        self.limpiar_text()
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")
        self.habilitar_text("disabled")
        self.llena_grilla(id_ref)
        self.alta_modif = 0

    # --------------------------------------------------------------------------
    # CANCELAR - SALIR
    # --------------------------------------------------------------------------

    def fcancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return 

        self.limpiar_text()
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")
        self.habilitar_text("disabled")

    def fsalir(self):

        self.master.destroy()

    def freset(self):

        self.entry_buscar_rubro.delete(0, "end")
        self.selected = self.grid_rubros.focus()
        self.clave = self.grid_rubros.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY ru_nombre ASC"
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.llena_grilla("")
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")

    # --------------------------------------------------------------------------
    # VARIOS
    # --------------------------------------------------------------------------

    def doble_click_grid(self, _event):
        self.feditar()

    @staticmethod
    def limitador(entry_text, caract):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:caract])

    # --------------------------------------------------------------------------
    # PUNTEROS
    # --------------------------------------------------------------------------

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_rubros, 'TOP')

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_rubros, 'END')

    def fshow_all(self):

        self.selected = self.grid_rubros.focus()
        self.clave = self.grid_rubros.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY ru_nombre ASC"
        self.entry_buscar_rubro.delete(0, "end")
        self.llena_grilla(self.clave)

    # --------------------------------------------------------------------------
    # BUSQUEDAS
    # --------------------------------------------------------------------------

    def fbuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.entry_buscar_rubro.get()) < 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.entry_buscar_rubro.get()
        self.filtro_activo = "WHERE INSTR(ru_nombre, '" + se_busca + "') > 0" \
                             + " ORDER BY ru_nombre ASC"

        self.varRubros.buscar_entabla(self.filtro_activo)
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_rubros.identify_row(0)
        self.grid_rubros.selection_set(item)
        self.grid_rubros.focus(item)

    def botones_crud(self):

        for c in range(1):
            self.cuadro_botones_crud.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.cargar_icono("archivo-nuevo.png")
        self.btnNuevo = tk.Button(self.cuadro_botones_crud, text=" Nuevo", command=self.fnuevo, bg="blue", fg="white",
                                  width=10, compound="left")
        self.btnNuevo.image = icono
        self.btnNuevo.config(image=icono)
        self.btnNuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        icono = self.cargar_icono("editar.png")
        self.btnModificar = tk.Button(self.cuadro_botones_crud, text=" Modificar", command=self.feditar, bg="blue", fg="white",
                                      width=10, compound="left")
        self.btnModificar.image = icono
        self.btnModificar.config(image=icono)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)

        icono = self.cargar_icono("eliminar.png")
        self.btnEliminar = tk.Button(self.cuadro_botones_crud, text=" Eliminar", command=self.feliminar, bg="red", fg="white",
                                     width=10, compound="left")
        self.btnEliminar.image = icono
        self.btnEliminar.config(image=icono)
        self.btnEliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)

        icono = self.cargar_icono("guardar.png")
        self.btnGuardar = tk.Button(self.cuadro_botones_crud, text=" Guardar", command=self.fguardar, bg="green", fg="white",
                                    width=10, compound="left")
        self.btnGuardar.image = icono
        self.btnGuardar.config(image=icono)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=3, columnspan=2)

        icono = self.cargar_icono("cancelar.png")
        self.btnCancelar = tk.Button(self.cuadro_botones_crud, text=" Cancelar", command=self.fcancelar, bg="black", fg="white",
                                     width=10, compound="left")
        self.btnCancelar.image = icono
        self.btnCancelar.config(image=icono)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=3, columnspan=2)

        for widg in self.cuadro_botones_crud.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def botones_grid(self):

        for c in range(1):
            self.cuadro_botones_grid.grid_columnconfigure(c, weight=1, minsize=140)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.cuadro_botones_grid, text="", image=self.photo4, command=self.ftoparch, bg="grey",
                                    fg="white")
        self.btnToparch.grid(row=0, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.cuadro_botones_grid, text="", image=self.photo5, command=self.ffinarch, bg="grey",
                                    fg="white")
        self.btnFinarch.grid(row=1, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        icono = self.cargar_icono("reset.png")
        self.btn_reset = tk.Button(self.cuadro_botones_grid, text=" Reset", width=11, command=self.freset, bg="black",
                                   fg="white", compound="left")
        self.btn_reset.image = icono
        self.btn_reset.config(image=icono)
        self.btn_reset.grid(row=2, column=0, padx=6, pady=3, ipadx=10)

        for widg in self.cuadro_botones_grid.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def boton_salir(self):

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.cuadro_boton_salir, text="Salir", image=self.photo3, command=self.fsalir, bg="yellow",
                                  fg="white")
        self.btnSalir.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def linea_buscador(self):

        # BUSCAR Linea de label y tk.Entry de busqueda
        self.lbl_buscar_rubro = tk.Label(self.cuadro_buscar, text="Buscar: ")
        self.lbl_buscar_rubro.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_rubro = tk.Entry(self.cuadro_buscar, width=21)
        self.entry_buscar_rubro.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.btn_buscar_rubro = tk.Button(self.cuadro_buscar, text="Buscar", command=self.fbuscar_en_tabla, bg="blue",
                                          fg="white", width=17)
        self.btn_buscar_rubro.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.btn_show_all = tk.Button(self.cuadro_buscar, text="Mostrar todo", command=self.fshow_all, bg="blue",
                                      fg="white", width=17)
        self.btn_show_all.grid(row=0, column=3, padx=5, pady=2, sticky="w")

    def armado_grid(self):

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.cuadro_grid)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        # GRID

        self.grid_rubros = ttk.Treeview(self.cuadro_grid, columns="col1")
        #self.grid_rubros.bind("<Double-tk.Button-1>", self.doble_click_grid)

        self.grid_rubros.column("#0", width=60, anchor="center")
        self.grid_rubros.column("col1", width=250, anchor="center")

        self.grid_rubros.heading("#0", text="Id", anchor="center")
        self.grid_rubros.heading("col1", text="Nombre", anchor="center")

        self.grid_rubros.tag_configure('oddrow', background='light grey')
        self.grid_rubros.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.cuadro_grid, orient="horizontal")
        scroll_y = tk.Scrollbar(self.cuadro_grid, orient="vertical")
        self.grid_rubros.config(xscrollcommand=scroll_x.set)
        self.grid_rubros.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_rubros.xview)
        scroll_y.config(command=self.grid_rubros.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_rubros['selectmode'] = 'browse'

        # PACK - de el treeview y el FRAME tv
        self.grid_rubros.pack(side="top", fill="both", expand=1, padx=5, pady=5)

    def entradas_entrys(self):

        # NOMBRE
        self.lbl_nombre = tk.Label(self.cuadro_entrys, text="Nombre: ")
        self.lbl_nombre.grid(row=0, column=0, padx=10, pady=3, sticky="w")
        self.entry_nombre_rubro = tk.Entry(self.cuadro_entrys, textvariable=self.sv_nombre_rubro, justify="left", width=50)
        self.sv_nombre_rubro.trace("w", lambda *args: self.limitador(self.sv_nombre_rubro, 40))
        self.entry_nombre_rubro.grid(row=0, column=1, padx=10, pady=3, sticky="w")

    @staticmethod
    def cargar_icono(path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def pantalla(self):

        self.master.resizable(0, 0)
        """  Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
             mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 700
        hventana = 510
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))

    def titulo_logo(self):

        self.photo3 = Image.open('rubro.png')
        self.photo3 = self.photo3.resize((105, 75), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_rubros = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_rubros = tk.Label(self.frame_titulo_superior, image=self.png_rubros, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = tk.Label(self.frame_titulo_superior, width=18, text="Rubros", bg="black", fg="gold",
                                   font=("Arial bold", 34, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_rubros.grid(row=0, column=0, sticky="w", padx=10, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, padx=5, sticky="nsew")

    def get_rubros_dic(self):
        return {
            "Id":            self.clave,
            "ru_nombre":     self.sv_nombre_rubro.get()
        }
