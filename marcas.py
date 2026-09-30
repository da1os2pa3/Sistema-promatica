import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from funcion_new import ClaseFuncionNew
from funciones import *
from marcas_ABM import DatosMarcas
from status_bar import StatusBar


class ClaseMarcas(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)

        # ---------------------------------------------------------------------------------
        # Instanciaciones - Creo una instancia de la clase marcas Abm y funcionnew
        self.varMarcas = DatosMarcas(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # ---------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------
        # Seteo pantalla master principal
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        self.pantalla()
        self.create_widgets()
        self.llena_grilla("")

        self.habilitar_text("disabled")
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")

    # -----------------------------------------------------------------------------
    # WIDGETS
    # -----------------------------------------------------------------------------

    def create_widgets(self):

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES
        self.filtro_activo = "ORDER BY ma_nombre"
        self.alta_modif = 0
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # TITULOS Y LOGO
        # --------------------------------------------------------------------------
        self.frame_titulo_top = tk.Frame(self.master)
        self.titulo_logo()
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=5)
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------
        # STRINGVARS
        self.sv_nombre = tk.StringVar(value="")
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # CUADRO DE BOTONES LATERAL

        barra_botones = tk.LabelFrame(self.master)

        # BOTONES 1
        self.cuadro_botones_crud = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.botones_crud()
        self.cuadro_botones_crud.pack(side="top", padx=3, pady=3, fill="y")
        # BOTONES 2
        self.cuadro_botones_tablero = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.botones_tablero()
        self.cuadro_botones_tablero.pack(side="top", padx=3, pady=3, fill="y")
        # BOTONES 3
        self.cuandro_boton_salida = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.boton_salida()
        self.cuandro_boton_salida.pack(side="top", padx=3, pady=3, fill="y")

        barra_botones.pack(side="left", padx=15, pady=5, ipady=5, fill="y")
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # BUSQUEDAS

        self.cuadro_grid = tk.Frame(self.master)

        # FRAME dentro del frame principal para poner la llinea de busqueda
        self.cuadro_busqueda = tk.LabelFrame(self.cuadro_grid)
        self.barra_busqueda()
        self.cuadro_busqueda.pack(expand=1, fill="x", pady=10, padx=5)

        self.armado_grid()

        self.cuadro_grid.pack(side="top", fill="both", padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # ENTRYS
        self.cuadro_entrys = tk.LabelFrame(self.master)
        self.sector_entrys()
        self.cuadro_entrys.pack(expand=1, fill="x", pady=5, padx=5)
        # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # GRID
    # ----------------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_marcas.get_children():
            self.grid_marcas.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varMarcas.consultar_marcas(self.filtro_activo)
        else:
            datos = self.varMarcas.consultar_marcas("ORDER BY ma_nombre ASC")

        cont = 0
        for row in datos:
            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_marcas.insert("", "end", tags=color, text=row[0], values=(row[1]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_marcas.get_children()
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
            self.grid_marcas.focus_set()
            self.grid_marcas.focus(posicion)
            self.grid_marcas.selection_set(posicion)
            self.grid_marcas.see(posicion)
        else:
            for item in children:
                texto = self.grid_marcas.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_marcas.update_idletasks()
                    self.grid_marcas.focus_set()
                    self.grid_marcas.selection_set(item)
                    self.grid_marcas.focus(item)
                    self.grid_marcas.see(item)
                    break

    # ----------------------------------------------------------------------------------
    # ESTADOS PANTALLA
    # ----------------------------------------------------------------------------------

    def habilitar_text(self, estado):
        self.entry_nombre.configure(state=estado)

    def limpiar_text(self):
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.delete(0, "end")

    def habilitar_btn_oper(self, estado):

        self.btnNuevo.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.entry_buscar_marca.configure(state=estado)
        self.btn_buscar_marca.configure(state=estado)
        self.btn_show_all.configure(state=estado)

    def habilitar_btn_final(self, estado):
        self.btnGuardar.configure(state=estado)

    # -------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------

    def fnuevo(self):

        self.alta_modif = 1
        self.habilitar_text("normal")
        self.habilitar_btn_final("normal")
        self.habilitar_btn_oper("disabled")
        self.limpiar_text()
        self.entry_nombre.focus()

    def fmodificar(self):

        self.selected = self.grid_marcas.focus()
        self.clave = self.grid_marcas.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        self.habilitar_text('normal')

        self.valores = self.grid_marcas.item(self.selected, 'values')

        self.limpiar_text()
        self.entry_nombre.insert(0, self.valores[0])
        self.habilitar_btn_final("normal")
        self.habilitar_btn_oper("disabled")
        self.entry_nombre.focus()

    def feliminar(self):

        # --------------------------------------------------------------------------
        # Tomo referencias de posicion del puntero para despues
        self.selected = self.grid_marcas.focus()
        self.selected_ant = self.grid_marcas.prev(self.selected)
        self.clave = self.grid_marcas.item(self.selected, 'text')
        self.clave_ant = self.grid_marcas.item(self.selected_ant, 'text')
        # --------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # ------------------------------------------------------------------------------
        # traigo valores desde el Grid
        valores = self.grid_marcas.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0]
        # ------------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # Verifico tabla articulos y si la marca ya existe asignado, lo modifico en todas sus apariciones
        exis = self.varMarcas.verifica_articulos(valores[0])
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        """ Si la marca existe en articulos, pido confirmacion de borrarlo en dichos articulos que lo tengan
        # asignado, dejaria la marca en blanco. """

        if exis != 0:
            r2 = messagebox.askquestion("Eliminar", "Existen articulos asignados a la marca y "
                                                    "se modificaran, Continua?\n " + valores[0], parent=self)
            if r2 == messagebox.NO:
                messagebox.showinfo("Eliminar", "Se cancelo la eliminacion del Registro", parent=self)
                return
        else:
            r = messagebox.askquestion("Eliminar", "Confirma eliminar marca?\n " + data, parent=self)
            if r == messagebox.NO:
                messagebox.showinfo("Eliminar", "Se cancelo la eliminacion del Registro", parent=self)
                return
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # Elimino la marca
        self.varMarcas.eliminar_marcas(self.clave)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # Elimino la marca de los articulos que la tengan
        if exis != 0:
            self.varMarcas.quitamarca(self.valores[0])
        # --------------------------------------------------------------------------

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        """ Vuelvo al inmediato anterior segun el orden establecido en el grid """
        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # VALIDACIONES -------------------------------------------------------
        if self.entry_nombre.get() == "":
            messagebox.showwarning("Alerta", "No ingreso Marca", parent=self)
            self.entry_nombre.focus()
            return

        # guardo el Id del Grid en selected para ubicacion del foco a posteriori --------------
        self.selected = self.grid_marcas.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_marcas.item(self.selected, 'text')
        # -------------------------------------------------------------------------------------

        # Preparo la fecha y pongo en la variable "dic_marcas" el diccionario completo con todos
        # los datos a ingresar a la tabla
        dic_marcas = self.get_marcas_dic()                  # funcion que genera el diccionario

        #-----------------------------------------------------------------
        # GUARDADO DATOS Y EVALUACION DEL PROCEDIMIENTO
        #-----------------------------------------------------------------
        id_ref = ""
        try:
            if self.alta_modif == 1:
                self.id_nuevo = self.varMarcas.insertar_marcas(dic_marcas)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                # Verifico tabla articulos y si la marca ya existe asignada, lo modifico en todas sus apariciones
                exis = self.varMarcas.verifica_articulos(self.valores[0])

                # si la marca existe, pido confirmacion de modificarlos en los articulos que lo tengan asignado
                if exis != 0:
                    r2 = messagebox.askquestion("Modificar", "Existen articulos asignados a la marca y "
                                                             "se modificaran, Continua?\n " + self.valores[0], parent=self)
                    if r2 == messagebox.NO:
                        return

                # Modificamos ya la marca en la tabla marcas pasando el Id -----
                self.varMarcas.modificar_marcas(dic_marcas)
                # --------------------------------------------------------------

                id_ref = self.clave

                if exis != 0:
                    # Modifica la marca en los articulos por la modificacion
                    self.varMarcas.modi_marca_enart(self.sv_nombre.get(), self.valores[0])

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

        self.entry_buscar_marca.delete(0, "end")
        self.selected = self.grid_marcas.focus()
        self.clave = self.grid_marcas.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY ma_nombre"
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.llena_grilla("")
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")

    def doble_click_grid(self, _event):
        self.fmodificar()

    # -----------------------------------------------------------------------------
    # VARIAS
    # -----------------------------------------------------------------------------

    @staticmethod
    def limitador(entry_text, caract):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:caract])

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_marcas, 'TOP')

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_marcas, 'END')

    def fbuscar_en_tabla(self):

        if not len(self.entry_buscar_marca.get()):
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.entry_buscar_marca.get()
        self.filtro_activo = "WHERE INSTR(ma_nombre, '" + se_busca + "') > 0" \
                             + " ORDER BY ma_nombre ASC"

        self.varMarcas.buscar_entabla(self.filtro_activo)
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_marcas.identify_row(0)
        self.grid_marcas.selection_set(item)
        self.grid_marcas.focus(item)

    def fshowall(self):

        self.selected = self.grid_marcas.focus()
        self.clave = self.grid_marcas.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY ma_nombre ASC"
        self.entry_buscar_marca.delete(0, "end")
        self.llena_grilla(self.clave)

    def pantalla(self):

        """ Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """
        self.master.resizable(0, 0)
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 790
        hventana = 500
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2)
        pheight = round(htotal / 2 - hventana / 2)
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

    def titulo_logo(self):

        # Armo el logo y el titulo
        self.photo3 = Image.open('marcas.png')
        self.photo3 = self.photo3.resize((105, 75), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_marca = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_marca = tk.Label(self.frame_titulo_top, image=self.png_marca, bg="red", relief="ridge", bd=5)

        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=19, text="Marcas", bg="black", fg="gold",
                                   font=("Arial bold", 36, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_marca.grid(row=0, column=0, sticky="w", padx=10, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, padx=5, sticky="nsew")

    def botones_crud(self):

        for c in range(1):
            self.cuadro_botones_crud.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.cargar_icono("archivo-nuevo.png")
        self.btnNuevo = tk.Button(self.cuadro_botones_crud, text="Nuevo", command=self.fnuevo, bg="blue", fg="white",
                                  width=10, compound="left")
        self.btnNuevo.image = icono
        self.btnNuevo.config(image=icono)
        self.btnNuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        icono = self.cargar_icono("editar.png")
        self.btnModificar = tk.Button(self.cuadro_botones_crud, text="Modificar", command=self.fmodificar, bg="blue",
                                      fg="white", width=10, compound="left")
        self.btnModificar.image = icono
        self.btnModificar.config(image=icono)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)

        icono = self.cargar_icono("eliminar.png")
        self.btnEliminar = tk.Button(self.cuadro_botones_crud, text="Eliminar", command=self.feliminar, bg="red",
                                     fg="white", width=10, compound="left")
        self.btnEliminar.image = icono
        self.btnEliminar.config(image=icono)
        self.btnEliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)

        icono = self.cargar_icono("guardar.png")
        self.btnGuardar = tk.Button(self.cuadro_botones_crud, text="Guardar", command=self.fguardar, bg="green",
                                    fg="white", width=10, compound="left")
        self.btnGuardar.image = icono
        self.btnGuardar.config(image=icono)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=3, columnspan=2)

        icono = self.cargar_icono("cancelar.png")
        self.btnCancelar = tk.Button(self.cuadro_botones_crud, text="Cancelar", command=self.fcancelar, bg="black",
                                     fg="white", width=10, compound="left")
        self.btnCancelar.image = icono
        self.btnCancelar.config(image=icono)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=3, columnspan=2)

        for widg in self.cuadro_botones_crud.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def botones_tablero(self):

        for c in range(1):
            self.cuadro_botones_tablero.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.cargar_icono("reset.png")
        self.btn_reset = tk.Button(self.cuadro_botones_tablero, text="Reset", width=11, command=self.freset,
                                   bg="black", fg="white", compound="left")
        self.btn_reset.image = icono
        self.btn_reset.config(image=icono)
        self.btn_reset.grid(row=7, column=0, padx=6, pady=3, ipadx=10)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.cuadro_botones_tablero, text="", image=self.photo4, command=self.ftoparch,
                                    bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.cuadro_botones_tablero, text="", image=self.photo5, command=self.ffinarch,
                                    bg="grey", fg="white")
        self.btnFinarch.grid(row=1, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        for widg in self.cuadro_botones_tablero.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def boton_salida(self):

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.cuandro_boton_salida, text="Salir", image=self.photo3, command=self.fsalir,
                                  bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")

    def barra_busqueda(self):

        for c in range(4):
            self.cuadro_busqueda.grid_columnconfigure(c, weight=1, minsize=140)

        # BUSCAR Linea de label y entry de busqueda
        self.lbl_buscar_marca = tk.Label(self.cuadro_busqueda, text="Buscar:")
        self.lbl_buscar_marca.grid(row=0, column=0, padx=3, pady=2)

        self.entry_buscar_marca = tk.Entry(self.cuadro_busqueda, width=20)
        self.entry_buscar_marca.grid(row=0, column=1, padx=3, pady=2, sticky="w")

        icono = self.cargar_icono("buscar.png")
        self.btn_buscar_marca = tk.Button(self.cuadro_busqueda, text="Buscar", command=self.fbuscar_en_tabla, bg="blue",
                                          fg="white", width=7, compound="left")
        self.btn_buscar_marca.image = icono
        self.btn_buscar_marca.config(image=icono)
        self.btn_buscar_marca.grid(row=0, column=2, padx=3, pady=2, sticky="w")

        icono = self.cargar_icono("ver_todo.png")
        self.btn_show_all = tk.Button(self.cuadro_busqueda, text="Mostrar todo", command=self.fshowall, bg="blue",
                                      fg="white", width=7, compound="left")
        self.btn_show_all.image = icono
        self.btn_show_all.config(image=icono)
        self.btn_show_all.grid(row=0, column=3, padx=3, pady=2, sticky="w")

        for widg in self.cuadro_busqueda.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def armado_grid(self):

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.cuadro_grid)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        # GRID
        self.grid_marcas = ttk.Treeview(self.cuadro_grid, columns="col1")
        self.grid_marcas.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_marcas.column("#0", width=60, anchor="center")
        self.grid_marcas.column("col1", width=250, anchor="center")

        self.grid_marcas.heading("#0", text="Id", anchor="center")
        self.grid_marcas.heading("col1", text="Nombre", anchor="center")

        self.grid_marcas.tag_configure('oddrow', background='light grey')
        self.grid_marcas.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.cuadro_grid, orient="horizontal")
        scroll_y = tk.Scrollbar(self.cuadro_grid, orient="vertical")
        self.grid_marcas.config(xscrollcommand=scroll_x.set)
        self.grid_marcas.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_marcas.xview)
        scroll_y.config(command=self.grid_marcas.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_marcas['selectmode'] = 'browse'

        # PACK - de el treeview y el FRAME tv
        #self.cuadro_busqueda.pack(side="top", fill="both", expand=1, padx=5, pady=3)
        self.grid_marcas.pack(side="top", fill="both", expand=1, padx=5, pady=5)

    def sector_entrys(self):

        self.lbl_nombre = tk.Label(self.cuadro_entrys, text="Nombre: ")
        self.lbl_nombre.grid(row=0, column=0, padx=10, pady=3, sticky="w")
        self.entry_nombre = tk.Entry(self.cuadro_entrys, textvariable=self.sv_nombre, justify="left", width=80)
        self.sv_nombre.trace("w", lambda *args: self.limitador(self.sv_nombre, 40))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=3, sticky="w")

    @staticmethod
    def cargar_icono(path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def get_marcas_dic(self):
        return {
            "Id":            self.clave,
            "ma_nombre":     self.sv_nombre.get()
        }
