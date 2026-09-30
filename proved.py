import tkinter as tk
from datetime import date
from tkinter import ttk

from PIL import Image, ImageTk

from funcion_new import ClaseFuncionNew
from funciones import *
from proved_ABM import Datosproved
from status_bar import StatusBar


class ClaseProved(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)

        # ---------------------------------------------------------------------------------
        # Seteo pantalla master principal
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------
        # INSTANCIACIONES
        self.varProved = Datosproved(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # ---------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------
        # TITULOS
        self.titulos()
        # ---------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_A()
        self.llena_grilla("")

        # ---------------------------------------------------------------------------------
        # Carga del Treeview y seteo de foco y punteros sobre el mismo (grid)
        item = self.grid_proved.identify_row(0)
        self.grid_proved.selection_set(item)
        self.grid_proved.focus(item)
        # ----------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------
        # Estado inicial del Gui
        self.habilitar_text("disabled")
        self.habilitar_btn_B("disabled")
        self.habilitar_btn_A("normal")

    def create_widgets(self):

        # ----------------------------------------------------------------------------------
        # TITULOS

        # Encabezado logo y título con PACK
        self.frame_titulo_top = tk.Frame(self.master)

        # Armo el logo y el título
        self.photo3 = Image.open('proveedor.png')
        self.photo3 = self.photo3.resize((105, 75), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_proved = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_proved = tk.Label(self.frame_titulo_top, image=self.png_proved, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=25, text="Proveedores", bg="black", fg="gold",
                                font=("Arial bold", 37, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_proved.grid(row=0, column=0, sticky=tk.W, padx=10, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, padx=5, sticky="nsew")

        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES -*-
        # Se usa para saber que filtro está activo y mantenerlo hasta que el usuario lo quite en Reset
        self.filtro_activo = "ORDER BY denominacion ASC"
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.alta_modif = 0
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS -*-
        self.sv_codigo = tk.StringVar(value="")
        self.sv_denominacion = tk.StringVar(value="")
        self.sv_direccion = tk.StringVar(value="")
        self.sv_localidad = tk.StringVar(value="")
        self.sv_provincia = tk.StringVar(value="")
        self.sv_postal = tk.StringVar(value="")
        self.sv_telef1 = tk.StringVar(value="")
        self.sv_telef2 = tk.StringVar(value="")
        self.sv_mail = tk.StringVar(value="")
        self.sv_fecha_alta = tk.StringVar(value="")
        self.sv_contacto = tk.StringVar(value="")
        self.sv_observaciones = tk.StringVar(value="")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # BOTONES -*-
        # Frame botones
        barra_botones = tk.LabelFrame(self.master)

        # botones del CRUD
        self.cuadro_botones_crud = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.botones_crud()
        self.cuadro_botones_crud.pack(side="top", padx=3, pady=3, fill="y")

        self.cuadro_botones_busqueda = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.botones_busqueda()
        self.cuadro_botones_busqueda.pack(side="top", padx=3, pady=3, fill="y")

        self.cuadro_boton_salida = tk.LabelFrame(barra_botones)
        self.boton_salida()
        self.cuadro_boton_salida.pack(side="top", padx=3, pady=3, fill="y")

        barra_botones.pack(side="left", padx=15, pady=5, ipady=5, fill="y")
        # -------------------------------------------------------------------------------

        # -------------------------------------------------------------------------------
        # Frame TREEVIEW y BUSQUEDA
        # -------------------------------------------------------------------------------
        self.frame_grid = tk.Frame(self.master)

        # FRAME linea de busqueda
        self.cuadro_buscar_grid = tk.LabelFrame(self.frame_grid)
        self.buscar_en_grid()
        self.cuadro_buscar_grid.pack(expand=1, fill="x", pady=10, padx=10)
        # GRID
        self.armo_grid()

        self.frame_grid.pack(side="top", fill="both", padx=5, pady=5)
        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------
        # ENTRYS -*-
        # ----------------------------------------------------------------------------
        self.cuadro_entrys = tk.LabelFrame(self.master)
        self.sector_entrys()
        self.cuadro_entrys.pack(expand=1, fill="both", pady=5, padx=5)

    # ----------------------------------------------------------------------------
    # ESTADO INICIAL -*-
    # ----------------------------------------------------------------------------

    def estado_A(self):

        # Variables
        self.filtro_activo = "ORDER BY denominacion ASC"
        self.alta_modif = 0

        # Grilla
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')

        # Estado inicial del Gui
        self.limpiar_text()
        self.habilitar_btn_A("normal")
        self.habilitar_btn_B("disabled")
        self.habilitar_text("disabled")

    def habilitar_btn_A(self, estado):

        self.btnNuevo.configure(state=estado)
        self.btnEliminar.configure(state=estado)
        self.btnModificar.configure(state=estado)
        self.btn_buscar_proved.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.entry_buscar_proved.configure(state=estado)

        self.btnFinarch.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btn_orden_codigo.configure(state=estado)
        self.btn_orden_nombre.configure(state=estado)

    def habilitar_btn_B(self, estado):
        self.btnGuardar.configure(state=estado)

    # ----------------------------------------------------------------------------
    # GRID -*-
    # ----------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_proved.get_children():
            self.grid_proved.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varProved.consultar_proved(self.filtro_activo)
        else:
            datos = self.varProved.consultar_proved("ORDER BY denominacion ASC")

        cont = 0
        for row in datos:

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[10], '%Y-%m-%d'), False)

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)
            self.grid_proved.insert("", "end", tags=color, text=row[0], values=(row[1], row[2], row[3], 
                                                                                row[4], row[5], row[6], row[7], row[8], 
                                                                                row[9], forma_normal, row[11], row[12]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_proved.get_children()
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
            self.grid_proved.focus_set()
            self.grid_proved.focus(posicion)
            self.grid_proved.selection_set(posicion)
            self.grid_proved.see(posicion)
        else:
            for item in children:
                texto = self.grid_proved.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_proved.update_idletasks()
                    self.grid_proved.focus_set()
                    self.grid_proved.selection_set(item)
                    self.grid_proved.focus(item)
                    self.grid_proved.see(item)
                    break

    def habilitar_text(self, estado):

        # Agregado para manejar tema de readonly y que no quede el código escrito al limpiar
        self.entry_codigo.configure(state="normal")

        self.entry_codigo.delete(0, "end")
        self.entry_codigo.configure(state=estado)
        self.entry_denomin.configure(state=estado)
        self.entry_direccion.configure(state=estado)
        self.entry_localidad.configure(state=estado)
        self.entry_provincia.configure(state=estado)
        self.entry_postal.configure(state=estado)
        self.entry_telefono1.configure(state=estado)
        self.entry_telefono2.configure(state=estado)
        self.entry_mail.configure(state=estado)
        self.entry_fecha_alta.configure(state=estado)
        self.entry_contacto.configure(state=estado)
        self.entry_observaciones.configure(state=estado)

    def fno_modifique(self, event):
        return

    def limpiar_text(self):

        self.entry_codigo.delete(0, "end")
        self.entry_denomin.delete(0, "end")
        self.entry_direccion.delete(0, "end")
        self.entry_localidad.delete(0, "end")
        self.entry_provincia.delete(0, "end")
        self.entry_postal.delete(0, "end")
        self.entry_telefono1.delete(0, "end")
        self.entry_telefono2.delete(0, "end")
        self.entry_mail.delete(0, "end")
        self.entry_fecha_alta.delete(0, "end")
        self.entry_contacto.delete(0, "end")
        self.entry_observaciones.delete(0, "end")

    def forden_codigo(self):
        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY codigo ASC"
        self.llena_grilla(self.clave)

    def forden_denominacion(self):
        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY denominacion ASC"
        self.llena_grilla(self.clave)

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_proved, 'TOP')

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_proved, 'END')

    def fbuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.entry_buscar_proved.get()) <= 0:
            self.status.set_status("❌ No ingreso busqueda", "error")
            return

        se_busca = self.entry_buscar_proved.get()
        self.filtro_activo = "WHERE INSTR(denominacion, '" + se_busca + "') > 0" \
                             + " ORDER BY denominacion ASC"

        self.varProved.buscar_entabla(self.filtro_activo)
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_proved.selection()
        if item:
            self.grid_proved.focus(item[0])

    def fshowall(self):
        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY denominacion ASC"
        self.llena_grilla(self.clave)

    def doble_click_grid(self, _event):
        self.fmodificar()

    # ----------------------------------------------------------------------------
    # CRUD -*-
    # ----------------------------------------------------------------------------

    def fnuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")
        self.limpiar_text()
        # Obtengo el codigo en secuencia y pongo el entry en disabled para no modificar
        self.entry_codigo.insert(0, str((int(self.varProved.traer_ultimo())) + 1))
        self.entry_codigo.configure(state="readonly")
        self.entry_localidad.insert(0, "Villa Carlos Paz")
        self.entry_provincia.insert(0, "Cordoba")
        self.entry_postal.insert(0, "5152")
        # Cambio el formato de la fecha
        una_fecha = date.today()
        self.entry_fecha_alta.insert(0, una_fecha.strftime('%d/%m/%Y'))
        self.entry_denomin.focus()

    def fmodificar(self):

        self.selected = self.grid_proved.focus()
        self.clave = self.grid_proved.item(self.selected, 'text')

        if self.clave == "":
            self.status.set_status("⚠ No hay nada seleccionado", "warn")
            return

        self.alta_modif = 2

        self.habilitar_text("normal")
        self.limpiar_text()

        self.filtro_activo = "WHERE Id = " + str(self.clave)

        valores = self.varProved.consultar_proved(self.filtro_activo)

        for row in valores:

            self.entry_codigo.insert(0, row[1])
            self.entry_denomin.insert(0, row[2])
            self.entry_direccion.insert(0, row[3])
            self.entry_localidad.insert(0, row[4])
            self.entry_provincia.insert(0, row[5])
            self.entry_postal.insert(0, row[6])
            self.entry_telefono1.insert(0, row[7])
            self.entry_telefono2.insert(0, row[8])
            self.entry_mail.insert(0, row[9])
            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[10], "%Y-%m-%d"), False)
            self.entry_fecha_alta.insert(0, fecha_convertida)
            self.entry_contacto.insert(0, row[11])
            self.entry_observaciones.insert(0, row[12])

            self.entry_codigo.configure(state="readonly")

        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")
        self.entry_denomin.focus()

    def feliminar(self):

        self.selected = self.grid_proved.focus()
        self.selected_ant = self.grid_proved.prev(self.selected)
        self.clave = self.grid_proved.item(self.selected, 'text')
        self.clave_ant = self.grid_proved.item(self.selected_ant, 'text')

        if self.clave == "":
            self.status.set_status("⚠ No hay nada seleccionado", "warn")
            return

        # guardo todos los valores en una lista desde el GRID
        valores = self.grid_proved.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        self.varProved.eliminar_proved(self.clave)

        self.status.set_status("🗑 Registro eliminado correctamente", "ok")

        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # control de codigo repetido (en funciones)
        codrep = codigo_repetido(self.sv_codigo.get(), "proved", "codigo")

        # si es alta y existe el codigo... error
        if self.alta_modif == 1 and len(codrep) > 0:
            messagebox.showerror("Error", "Codigo ya existe en la tabla - verifique", parent=self)
            self.entry_denomin.focus()
            return

        # --------------------------------------------------------------------
        # VALIDACION QUE EXISTA APELLIDO
        if self.sv_denominacion.get() == "":
            messagebox.showwarning("Alerta", "No ingreso denominacion", parent=self)
            self.entry_denomin.focus()
            return
        # --------------------------------------------------------------------

        # guardo el Id del Grid en selected para ubicacion del foco a posteriori
        self.selected = self.grid_proved.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_proved.item(self.selected, 'text')

        # Preparo la fecha y pongo en la variable "dic_proved" el diccionario completo con todos
        # los datos a ingresar a la tabla
        fecha_aux = datetime.strptime(self.sv_fecha_alta.get(), '%d/%m/%Y')
        dic_proved = self.get_proved_dic(fecha_aux)                  # funcion que genera el diccionario

        #-----------------------------------------------------------------
        # GUARDADO DATOS Y EVALUACION DEL PROCEDIMIENTO
        #-----------------------------------------------------------------
        id_ref = ""
        try:
            if self.alta_modif == 1:
                self.id_nuevo = self.varProved.insertar_proved(dic_proved)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                self.varProved.modificar_proved(dic_proved)
                id_ref = self.clave
        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Insertar/Modificar", str(e))
            return
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        self.filtro_activo = "ORDER BY denominacion"
        self.limpiar_text()
        self.habilitar_btn_B("disabled")
        self.habilitar_btn_A("normal")
        self.llena_grilla(id_ref)
        self.alta_modif = 0
        self.habilitar_text("disabled")

    def fcancelar(self):
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_A()

    def freset(self):
        self.estado_A()
        self.llena_grilla("")
        self.varFuncion_new.mover_puntero_topend(self.grid_proved, "TOP")

    def fsalir(self):
        self.master.destroy()

    @staticmethod
    def limitador(entry_text, caract):
        if len(entry_text.get()) > 0:
            entry_text.set(entry_text.get()[:caract])

    def formato_fecha(self, _pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar all sus valores posibles, le paso la
        fecha tipo string con barras o sin barras """

        # FUNCION VALIDA FECHAS en programa funcion
        retorno_validacion = self.varFuncion_new.validar_fecha(self.sv_fecha_alta, self.entry_fecha_alta)

        una_fecha = date.today()

        match retorno_validacion:

            case "break":
                self.entry_fecha_alta.focus()
                return
            case "S":
                self.entry_fecha_alta.focus()
            case "N" | "BLANCO":
                pass
            case "":
                self.sv_fecha_alta.set(una_fecha.strftime('%d/%m/%Y'))
                self.entry_fecha_alta.focus()
            case _:
                return

    def titulos(self):

        self.master.resizable(0, 0)
        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """

        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()
        # Asigno fijo un ancho y un alto
        ancho_ventana = 970
        alto_ventana = 600
        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def botones_crud(self):

        for c in range(1):
            self.cuadro_botones_crud.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.cargar_icono("archivo-nuevo.png")
        self.btnNuevo = tk.Button(self.cuadro_botones_crud, text="Nuevo", command=self.fnuevo, bg="blue", fg="white",
                                  width=10, compound="left")
        self.btnNuevo.image = icono
        self.btnNuevo.config(image=icono)
        self.btnNuevo.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
        self.btnNuevo.image = icono
        self.btnNuevo.config(image=icono)

        icono = self.cargar_icono("editar.png")
        self.btnModificar = tk.Button(self.cuadro_botones_crud, text="Modificar", command=self.fmodificar, bg="blue",
                                      fg="white", width=10, compound="left")
        self.btnModificar.image = icono
        self.btnModificar.config(image=icono)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=5, ipadx=10)

        icono = self.cargar_icono("eliminar.png")
        self.btnEliminar = tk.Button(self.cuadro_botones_crud, text="Eliminar", command=self.feliminar, bg="red",
                                     fg="white", width=10, compound="left")
        self.btnEliminar.image = icono
        self.btnEliminar.config(image=icono)
        self.btnEliminar.grid(row=2, column=0, padx=5, pady=5, ipadx=10)

        icono = self.cargar_icono("guardar.png")
        self.btnGuardar = tk.Button(self.cuadro_botones_crud, text="Guardar", command=self.fguardar, bg="green",
                                    fg="white", width=10, compound="left")
        self.btnGuardar.image = icono
        self.btnGuardar.config(image=icono)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=5, columnspan=2)

        icono = self.cargar_icono("cancelar.png")
        self.btnCancelar = tk.Button(self.cuadro_botones_crud, text="Cancelar", command=self.fcancelar, bg="black",
                                     fg="white", width=10, compound="left")
        self.btnCancelar.image = icono
        self.btnCancelar.config(image=icono)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        for widg in self.cuadro_botones_crud.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def botones_busqueda(self):

        for c in range(1):
            self.cuadro_botones_busqueda.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.cargar_icono("ordenar.png")
        self.btn_orden_codigo = tk.Button(self.cuadro_botones_busqueda, text="Orden Codigo", width=11,
                                          command=self.forden_codigo, bg="grey", fg="white", compound="left")
        self.btn_orden_codigo.image = icono
        self.btn_orden_codigo.config(image=icono)
        self.btn_orden_codigo.grid(row=5, column=0, padx=6, pady=5, ipadx=10)

        icono = self.cargar_icono("ordenar.png")
        self.btn_orden_nombre = tk.Button(self.cuadro_botones_busqueda, text="Orden Denomin.", width=11,
                                          command=self.forden_denominacion, bg="grey", fg="white", compound="left")
        self.btn_orden_nombre.image = icono
        self.btn_orden_nombre.config(image=icono)
        self.btn_orden_nombre.grid(row=6, column=0, padx=6, pady=5, ipadx=10)

        icono = self.cargar_icono("reset.png")
        self.btn_reset = tk.Button(self.cuadro_botones_busqueda, text="Reset", width=11, command=self.freset,
                                   bg="black", fg="white", compound="left")
        self.btn_reset.image = icono
        self.btn_reset.config(image=icono)
        self.btn_reset.grid(row=7, column=0, padx=6, pady=5, ipadx=10)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.cuadro_botones_busqueda, text="", image=self.photo4, command=self.ftoparch,
                                    bg="grey", fg="white")
        self.btnToparch.grid(row=8, column=0, padx=5, sticky="nsew", pady=5)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")

        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.cuadro_botones_busqueda, text="", image=self.photo5, command=self.ffinarch,
                                    bg="grey", fg="white")
        self.btnFinarch.grid(row=9, column=0, padx=5, sticky="nsew", pady=5)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        for widg in self.cuadro_botones_busqueda.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def boton_salida(self):
        
        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 40), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.cuadro_boton_salida, text="Salir", image=self.photo3, command=self.fsalir,
                                  bg="yellow", fg="white")
        self.btnSalir.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

    def buscar_en_grid(self):

        for c in range(4):
            self.cuadro_buscar_grid.grid_columnconfigure(c, weight=1, minsize=140)

        self.lbl_buscar_proved = tk.Label(self.cuadro_buscar_grid, text="Buscar: ")
        self.lbl_buscar_proved.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_proved = tk.Entry(self.cuadro_buscar_grid, width=50)
        self.entry_buscar_proved.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        icono = self.cargar_icono("buscar.png")
        self.btn_buscar_proved = tk.Button(self.cuadro_buscar_grid, text="Buscar", command=self.fbuscar_en_tabla,
                                           bg="blue", fg="white", width=24, compound="left")
        self.btn_buscar_proved.image = icono
        self.btn_buscar_proved.config(image=icono)
        self.btn_buscar_proved.grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)

        icono = self.cargar_icono("ver_todo.png")
        self.btn_showall = tk.Button(self.cuadro_buscar_grid, text="Mostrar todo", command=self.fshowall, bg="blue",
                                        fg="white", width=25, compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)

        for widg in self.cuadro_buscar_grid.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def armo_grid(self):

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.frame_grid)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_proved = ttk.Treeview(self.frame_grid, columns=("col1", "col2", "col3", "col4", "col5", "col6",
                                                                  "col7", "col8", "col9", "col10", "col11", "col12"))

        self.grid_proved.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_proved.column("#0", width=60, anchor="center")
        self.grid_proved.column("col1", width=60, anchor="center")
        self.grid_proved.column("col2", width=180, anchor="center")
        self.grid_proved.column("col3", width=220, anchor="center")
        self.grid_proved.column("col4", width=220, anchor="center")
        self.grid_proved.column("col5", width=120, anchor="center")
        self.grid_proved.column("col6", width=90, anchor="center")
        self.grid_proved.column("col7", width=150, anchor="center")
        self.grid_proved.column("col8", width=150, anchor="center")
        self.grid_proved.column("col9", width=200, anchor="center")
        self.grid_proved.column("col10", width=200, anchor="center")
        self.grid_proved.column("col11", width=150, anchor="center")
        self.grid_proved.column("col12", width=200, anchor="center")

        self.grid_proved.heading("#0", text="Id", anchor="center")
        self.grid_proved.heading("col1", text="Codigo", anchor="center")
        self.grid_proved.heading("col2", text="Denominacion", anchor="center")
        self.grid_proved.heading("col3", text="Direccion", anchor="center")
        self.grid_proved.heading("col4", text="Localidad", anchor="center")
        self.grid_proved.heading("col5", text="Provincia", anchor="center")
        self.grid_proved.heading("col6", text="Postal", anchor="center")
        self.grid_proved.heading("col7", text="Telfono 1", anchor="center")
        self.grid_proved.heading("col8", text="Telfono 2", anchor="center")
        self.grid_proved.heading("col9", text="E-mail", anchor="center")
        self.grid_proved.heading("col10", text="Fecha alta", anchor="center")
        self.grid_proved.heading("col11", text="Contacto", anchor="center")
        self.grid_proved.heading("col12", text="Observaciones", anchor="center")

        self.grid_proved.tag_configure('oddrow', background='light grey')
        self.grid_proved.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_grid, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_grid, orient="vertical")
        self.grid_proved.config(xscrollcommand=scroll_x.set)
        self.grid_proved.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_proved.xview)
        scroll_y.config(command=self.grid_proved.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # PACK - del treeview y el FRAME tv
        self.cuadro_buscar_grid.pack(side="top", fill="both", expand=1, padx=5, pady=3)
        self.grid_proved.pack(side="top", fill="both", expand=1, padx=5, pady=5)

    def sector_entrys(self):

        # CODIGO
        self.lbl_codigo = tk.Label(self.cuadro_entrys, text="Ultimo Codigo: ")
        self.lbl_codigo.grid(row=0, column=0, padx=10, pady=3, sticky=tk.W)
        self.entry_codigo = tk.Entry(self.cuadro_entrys, textvariable=self.sv_codigo, justify="right", width=10)
        self.sv_codigo.trace("w", lambda *args: limitador(self.sv_codigo, 5))
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=3, sticky=tk.W)
        # APELLIDO
        self.lbl_denomin = tk.Label(self.cuadro_entrys, text="Denominacion: ")
        self.lbl_denomin.grid(row=1, column=0, padx=10, pady=3, sticky=tk.W)
        self.entry_denomin = tk.Entry(self.cuadro_entrys, textvariable=self.sv_denominacion, justify="left", width=40)
        self.sv_denominacion.trace("w", lambda *args: limitador(self.sv_denominacion, 30))
        self.entry_denomin.grid(row=1, column=1, padx=10, pady=3, sticky=tk.W)
        # DIRECCION
        self.lbl_direccion = tk.Label(self.cuadro_entrys, text="Direccion: ")
        self.lbl_direccion.grid(row=2, column=0, padx=10, pady=3, sticky=tk.W)
        self.entry_direccion = tk.Entry(self.cuadro_entrys, textvariable=self.sv_direccion, justify="left", width=40)
        self.sv_direccion.trace("w", lambda *args: self.limitador(self.sv_direccion, 30))
        self.entry_direccion.grid(row=2, column=1, padx=10, pady=3, sticky=tk.W)
        # LOCALIDAD
        self.lbl_localidad = tk.Label(self.cuadro_entrys, text="Localidad: ")
        self.lbl_localidad.grid(row=3, column=0, padx=10, pady=3, sticky=tk.W)
        self.entry_localidad = tk.Entry(self.cuadro_entrys, textvariable=self.sv_localidad, justify="left", width=40)
        self.sv_localidad.trace("w", lambda *args: self.limitador(self.sv_localidad, 30))
        self.entry_localidad.grid(row=3, column=1, padx=10, pady=3, sticky=tk.W)
        # PROVINCIA
        self.lbl_provincia = tk.Label(self.cuadro_entrys, text="Provincia: ")
        self.lbl_provincia.grid(row=4, column=0, padx=10, pady=3, sticky=tk.W)
        self.entry_provincia = tk.Entry(self.cuadro_entrys, textvariable=self.sv_provincia, justify="left", width=40)
        self.sv_provincia.trace("w", lambda *args: self.limitador(self.sv_provincia, 15))
        self.entry_provincia.grid(row=4, column=1, padx=10, pady=3, sticky=tk.W)
        # POSTAL
        self.lbl_postal = tk.Label(self.cuadro_entrys, text="Cod. Postal: ")
        self.lbl_postal.grid(row=5, column=0, padx=10, pady=3, sticky=tk.W)
        self.entry_postal = tk.Entry(self.cuadro_entrys, textvariable=self.sv_postal, justify="left", width=40)
        self.sv_postal.trace("w", lambda *args: self.limitador(self.sv_postal, 5))
        self.entry_postal.grid(row=5, column=1, padx=10, pady=3, sticky=tk.W)
        # TELEFONO PERSONAL
        self.lbl_telefono1 = tk.Label(self.cuadro_entrys, text="Telefono 1: ")
        self.lbl_telefono1.grid(row=0, column=2, padx=10, pady=3, sticky=tk.W)
        self.entry_telefono1 = tk.Entry(self.cuadro_entrys, textvariable=self.sv_telef1, justify="left", width=40)
        self.sv_telef1.trace("w", lambda *args: self.limitador(self.sv_telef1, 15))
        self.entry_telefono1.grid(row=0, column=3, padx=10, pady=3, sticky=tk.W)
        # TELEFONO TRABAJO
        self.lbl_telefono2 = tk.Label(self.cuadro_entrys, text="Telefono 2: ")
        self.lbl_telefono2.grid(row=1, column=2, padx=10, pady=3, sticky=tk.W)
        self.entry_telefono2 = tk.Entry(self.cuadro_entrys, textvariable=self.sv_telef2, justify="left", width=40)
        self.sv_telef2.trace("w", lambda *args: self.limitador(self.sv_telef2, 15))
        self.entry_telefono2.grid(row=1, column=3, padx=10, pady=3, sticky=tk.W)
        # CORREO ELECTRONICO
        self.lbl_mail = tk.Label(self.cuadro_entrys, text="Correo Electronico: ")
        self.lbl_mail.grid(row=2, column=2, padx=10, pady=3, sticky=tk.W)
        self.entry_mail = tk.Entry(self.cuadro_entrys, textvariable=self.sv_mail, justify="left", width=40)
        self.sv_mail.trace("w", lambda *args: self.limitador(self.sv_mail, 30))
        self.entry_mail.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)
        # FECHA DE INGRESO
        self.lbl_fecha_alta = tk.Label(self.cuadro_entrys, text="Fecha Alta: ")
        self.lbl_fecha_alta.grid(row=3, column=2, padx=10, pady=3, sticky=tk.W)
        self.entry_fecha_alta = tk.Entry(self.cuadro_entrys, textvariable=self.sv_fecha_alta, justify="left", width=40)
        self.entry_fecha_alta.bind("<FocusOut>", self.formato_fecha)
        # self.sv_fecha_alta.trace("w", lambda *args: self.limitador(self.sv_fecha_alta, 10))
        self.entry_fecha_alta.grid(row=3, column=3, padx=10, pady=3, sticky=tk.W)
        # CONTACTO
        self.lbl_contacto = tk.Label(self.cuadro_entrys, text="Contacto: ")
        self.lbl_contacto.grid(row=4, column=2, padx=10, pady=3, sticky=tk.W)
        self.entry_contacto = tk.Entry(self.cuadro_entrys, textvariable=self.sv_contacto, justify="left", width=40)
        self.sv_contacto.trace("w", lambda *args: self.limitador(self.sv_contacto, 25))
        self.entry_contacto.grid(row=4, column=3, padx=10, pady=3, sticky=tk.W)
        # OBSERVACIONES
        self.lbl_observaciones = tk.Label(self.cuadro_entrys, text="Observaciones: ")
        self.lbl_observaciones.grid(row=5, column=2, padx=10, pady=3, sticky=tk.W)
        self.entry_observaciones = tk.Entry(self.cuadro_entrys, textvariable=self.sv_observaciones, justify="left",
                                         width=40)
        self.sv_observaciones.trace("w", lambda *args: self.limitador(self.sv_observaciones, 50))
        self.entry_observaciones.grid(row=5, column=3, padx=10, pady=3, sticky=tk.W)

    @staticmethod
    def cargar_icono(path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def get_proved_dic(self, fecha_aux):

        return {
            "Id":            self.clave,
            "codigo":        self.sv_codigo.get(),
            "denominacion":      self.sv_denominacion.get(),
            "direccion":     self.sv_direccion.get(),
            "localidad":     self.sv_localidad.get(),
            "provincia":     self.sv_provincia.get(),
            "postal":        self.sv_postal.get(),
            "telefono1":     self.sv_telef1.get(),
            "telefono2":     self.sv_telef2.get(),
            "mail":          self.sv_mail.get(),
            "fecha_alta": fecha_aux,
            "contacto":      self.sv_contacto.get(),
            "observaciones": self.sv_observaciones.get()
        }
