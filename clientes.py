"""Ctrl + Alt + O → Optimize Imports (elimina imports no usados y ordena los que quedan).
Ctrl + Alt + L → Reformat Code (reformatea el código según las reglas configuradas).
Ctrl + Alt + Shift + L → abre el cuadro de diálogo para elegir opciones avanzadas de reformateo."""

from funciones import *
from funcion_new import ClaseFuncionNew
from clientes_ABM import datosClientes
#-------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkfont
#-------------------------------------------------
from datetime import date, datetime
from PIL import Image, ImageTk
from tktooltip import ToolTip
from status_bar import StatusBar

class ClaseClientes(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)

        # Seteo pantalla master principal -------------------------------------------------
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # Instanciaciones -----------------------------------------------------------------
        # Creo una instancia de clientesABM de la clase datosClientes
        self.varClientes = datosClientes(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # PANTALLA -*-
        # ---------------------------------------------------------------------------------
        self.master.resizable(0, 0)
        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """
        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()
        # Asigno fijo un ancho y un alto
        ancho_ventana = 980
        alto_ventana = 630
        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

    def create_widgets(self):

        # --------------------------------------------------------------------------
        # TITULOS -*-
        # --------------------------------------------------------------------------
        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = tk.Frame(self.master)
        self.cuadro_titulos()
        self.frame_titulo_top.pack(side="top", fill="x", padx=8, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS -*-
        # --------------------------------------------------------------------------
        self.sv_codigo = tk.StringVar(value="")
        self.sv_apellido = tk.StringVar(value="")
        self.sv_nombres = tk.StringVar(value="")
        self.sv_direccion = tk.StringVar(value="")
        self.sv_localidad = tk.StringVar(value="")
        self.sv_provincia = tk.StringVar(value="")
        self.sv_postal = tk.StringVar(value="")
        self.sv_telef_pers = tk.StringVar(value="")
        self.sv_telef_trab = tk.StringVar(value="")
        self.sv_mail = tk.StringVar(value="")
        self.sv_sit_fis = tk.StringVar(value="")
        self.sv_cuit = tk.StringVar(value="")
        self.sv_fecha_ingreso = tk.StringVar(value="")
        self.sv_observaciones = tk.StringVar(value="")
        self.sv_cant_clientes = tk.StringVar(value="0")

        # --------------------------------------------------------------------------
        # BARRA LATERAL DE MENU
        # --------------------------------------------------------------------------
        # cuadro principal contenedor - barra izquierda
        self.barra_botones = tk.LabelFrame(self.master)
        self.barra_lateral_botones()
        self.barra_botones.pack(side="left", padx=10, pady=5, ipady=5, fill="y")
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # CUADRO PRINCIPAL CONTENEDOR DEL GRID Y BARRA DE BUSQUEDAS
        self.frame_principal = tk.Frame(self.master)

        # BUSQUEDA DE CLIENTES -----------------------------------------------------
        self.frame_buscar = tk.LabelFrame(self.frame_principal)
        self.cuadro_buscar()
        self.frame_buscar.pack(side="top", fill="both", expand=1, padx=1, pady=3)
        # -------------------------------------------------------------------------
        # GRID --------------------------------------------------------------------
        self.cuadro_grid_clientes()

        self.frame_principal.pack(side="top", fill="both", padx=5, pady=5)
        # --------------------------------------------------------------------------

        # ENTRYS -------------------------------------------------------------------
        self.sector_entry = tk.LabelFrame(self.master)
        self.cuadro_entrys()
        self.sector_entry.pack(expand=1, fill="both", pady=5, padx=5)
        # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # GRID -*- METODOS
    # --------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        """ En set_foco viene el Id de la tabla que identidica el registro donde quiero oner el foco - 2312, 23, 456..
        Puede llegar a venir en vacio """

        # Limpio el grid --------------------------------------------------------
        for item in self.grid_clientes.get_children():
            self.grid_clientes.delete(item)

        # Asigno orden -----------------------------------------------------------
        if self.filtro_activo:
            datos = self.varClientes.consultar_clientes(self.filtro_activo)
        else:
            datos = self.varClientes.consultar_clientes("ORDER BY apellido, nombres ASC")

        # Tomo la cantidad de clientes -------------------------------------------
        self.sv_cant_clientes.set(value=str(len(datos)))

        # Inserto items en el Grid -----------------------------------------------
        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)
            # convierto fecha de 2024-12-19 a 19/12/2024
#            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[13], '%Y-%m-%d'), False)
            forma_normal = self.varFuncion_new.fecha_es(datetime.strftime(row[13], '%Y-%m-%d'), False)
            self.grid_clientes.insert("", "end", tags=color, text=row[0], values=(row[1], row[2], row[3],
                                                               row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                                                               row[11], row[12], forma_normal, row[14]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_clientes.get_children()
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
            self.grid_clientes.focus_set()
            self.grid_clientes.focus(posicion)
            self.grid_clientes.selection_set(posicion)
            self.grid_clientes.see(posicion)
        else:
            for item in children:
                texto = self.grid_clientes.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_clientes.update_idletasks()
                    self.grid_clientes.focus_set()
                    self.grid_clientes.selection_set(item)
                    self.grid_clientes.focus(item)
                    self.grid_clientes.see(item)
                    break

    # --------------------------------------------------------------------------
    # INICIALIZACION SISTEMA -*-
    # --------------------------------------------------------------------------

    def estado_inicial(self):

        # Variables
        self.filtro_activo = "ORDER BY apellido, nombres ASC"
        self.alta_modif = 0
        self.limpiar_text()
        self.habilitar_btn_A("normal")
        self.habilitar_btn_B("disabled")
        self.habilitar_text("disabled")

    def habilitar_text(self, estado):

        for entry in [
            self.entry_apellido,
            self.entry_nombres,
            self.entry_direccion,
            self.entry_localidad,
            self.entry_provincia,
            self.entry_postal,
            self.entry_telefono_pers,
            self.entry_telefono_trab,
            self.entry_mail,
            self.entry_fecha_ingreso,
            self.combo_sit_fiscal,
            self.entry_cuit,
            self.entry_observaciones
        ]:
            entry.configure(state=estado)

    def limpiar_text(self):

        self.combo_sit_fiscal.set(""),
        self.combo_sit_fiscal.current(0),

        # Agregado para manejar tema de readonly y que no quede el codigo escrito al limpiar
        self.entry_codigo.configure(state="normal")
        self.entry_codigo.delete(0, "end")
        self.entry_codigo.configure(state="disabled")

        for entry in [
#            self.entry_codigo,
            self.entry_apellido,
            self.entry_nombres,
            self.entry_direccion,
            self.entry_localidad,
            self.entry_provincia,
            self.entry_postal,
            self.entry_telefono_pers,
            self.entry_telefono_trab,
            self.entry_mail,
            self.entry_cuit,
            self.entry_observaciones
        ]:
            entry.delete(0, "end")

    def habilitar_btn_A(self, estado):

        for entry in [
            self.btn_nuevo,
            self.btn_eliminar,
            self.btn_editar,
            self.entry_buscar_cliente,
            self.btn_buscar_cliente,
            self.btn_mostrar_todo
        ]:
            entry.configure(state=estado)

        if self.alta_modif == 1 or self.alta_modif == 0:
            self.btnFinarch.configure(state=estado)
            self.btnToparch.configure(state=estado)
            self.btn_orden_codigo.configure(state=estado)
            self.btn_orden_apellido.configure(state=estado)

    def habilitar_btn_B(self, estado):
        self.btn_guardar.configure(state=estado)

    def fcancelar(self):
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_inicial()

    def freset(self):
        self.estado_inicial()
        self.llena_grilla("")
        self.varFuncion_new.mover_puntero_topend(self.grid_clientes, 'TOP')

    def fsalir(self):
        self.master.destroy()

    def fno_modifique(self, event):
        return

    # --------------------------------------------------------------------------
    # CRUD -*-
    # --------------------------------------------------------------------------

    def fnuevo(self):

        self.alta_modif = 1

        # preparacion
        self.habilitar_text("normal")
        self.limpiar_text()
        self.entry_fecha_ingreso.delete(0, "end")
        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")

        # Obtengo el ultimo codigo + 1 y pongo el entry en readonly para no modificar
        self.entry_codigo.configure(state="normal")
        self.entry_codigo.insert(0, (int(self.varClientes.traer_ultimo())) + 1)
        self.entry_codigo.configure(state="readonly")

        # readonly combo de situacion fiscal
        self.combo_sit_fiscal.current(0)
        self.combo_sit_fiscal.configure(state="readonly")

        # Valores preestablecidos
        self.entry_localidad.insert(0, "Villa Carlos Paz")
        self.entry_provincia.insert(0, "Cordoba")
        self.entry_postal.insert(0, "5152")

        # Cambio el formato de la fecha
        una_fecha = date.today()
        self.entry_fecha_ingreso.insert(0, una_fecha.strftime('%d/%m/%Y'))

        self.entry_apellido.focus()

    def feditar(self):

        # claves del Grid
        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')

        if self.clave == "":
            self.status.set_status("✔ No hay nada seleccionado", "ok")
            return

        self.alta_modif = 2

        # preparacion
        self.habilitar_text('normal')
        self.limpiar_text()

        # carga valores Entrys
        self.filtro_activo = "WHERE Id = " + str(self.clave)

        valores = self.varClientes.consultar_clientes(self.filtro_activo)

        for row in valores:

            self.entry_codigo.configure(state="normal")
            self.entry_codigo.insert(0, row[1])
            self.entry_codigo.configure(state="readonly")

            self.entry_apellido.insert(0, row[2])
            self.entry_nombres.insert(0, row[3])
            self.entry_direccion.insert(0, row[4])
            self.entry_localidad.insert(0, row[5])
            self.entry_provincia.insert(0, row[6])
            self.entry_postal.insert(0, row[7])
            self.entry_telefono_pers.insert(0, row[8])
            self.entry_telefono_trab.insert(0, row[9])
            self.entry_mail.insert(0, row[10])
            self.combo_sit_fiscal.set(row[11])
            self.entry_cuit.insert(0, row[12])
            # convierto fecha de date a string y cambio a visualizacion español
            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[13], "%Y-%m-%d"), False)
            self.entry_fecha_ingreso.insert(0, fecha_convertida)
            self.sv_fecha_ingreso.set(value=fecha_convertida)
            self.entry_observaciones.insert(0, row[14])

        # termino preparacion
        self.habilitar_btn_B("normal")
        self.habilitar_btn_A("disabled")
        self.entry_apellido.focus()

    def feliminar(self):

        # ------------------------------------------------------------------------------
        """ prev(self.selected) → intenta traer el item anterior Si no existe(por ejemplo, estás en el
        primero) → devuelve "" Entonces entra el or → usa self.selected. """
        self.selected = self.grid_clientes.focus()
        self.selected_ant = self.grid_clientes.prev(self.selected) or self.selected
        # guardo en clave el Id pero de la Tabla (no son el mismo que el grid)
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.clave_ant = self.grid_clientes.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "":
            self.status.set_status("❌ No hay nada seleccionado", "error")
            return

        # guardo todos los valores en una lista desde el GRID
        valores = self.grid_clientes.item(self.selected, 'values')
        data = " Nº: "+valores[0]+" Cliente: " + valores[1]+" "+valores[2]

        r = messagebox.askquestion("Confirmar", "Confirma eliminar cliente?\n " + data, parent=self)
        if r == messagebox.NO:
            self.status.set_status("ℹ Eliminacion cancelada", "info")
            return

        try:
            # Elimino el cliente -----------------------
            self.varClientes.eliminar_clientes(self.clave)
            # ------------------------------------------
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("🗑 Cliente eliminado correctamente", "ok")

        # recarga del Grid
        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # VALIDACIONES ---------------------------------------------------

        # CONTROLO CODIGO REPETIDO - control de codigo de cliente repetido (en funciones)
        # si viene algun dato, es que el codigo ya existe
        codrep = codigo_repetido(self.sv_codigo.get(), "clientes", "codigo")
        if self.alta_modif == 1 and len(codrep) > 0:
            self.status.set_status("❌ El Codigo ya existe, error al guardar", "error")
            self.entry_apellido.focus()
            return

        # VALIDACION QUE EXISTA APELLIDO y NOMBRE
        if self.sv_apellido.get() == "":
            self.status.set_status("⚠ Ingrese apellido/s", "warn")
            self.entry_apellido.focus()
            return
        if self.sv_nombres.get() == "":
            self.status.set_status("⚠ Ingrese nombre/s", "warn")
            self.entry_nombres.focus()
            return
        # VALIDAR CUIT - en modulo funciones.py
        if not validar_cuit(self, self.sv_cuit.get()):
            self.status.set_status("⚠ CUIT incorrecto", "warn")
            self.entry_cuit.focus()
            return
        # ----------------------------------------------------------------

        #-----------------------------------------------------------------
        # GUARDO ID Y CLAVE PARA GRID Y POOSICIONAR PUNTERO
        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
        self.selected = self.grid_clientes.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo
        # verlo en la base 1, 2, 3, 4......)
        self.clave = self.grid_clientes.item(self.selected, 'text')
        #-----------------------------------------------------------------

        # Preparo la fecha y pongo en la variable "dic_clientes" el diccionario completo con todos
        # los datos a ingresar a la tabla
        fecha_aux = datetime.strptime(self.sv_fecha_ingreso.get(), '%d/%m/%Y')
        dic_clientes = self.get_clientes_dic(fecha_aux)    # funcion que genera el diccionario

        """
        # clientes = {
        #     "Id": self.clave,
        #     "codigo": self.sv_codigo.get(),
        #     "apellido": self.sv_apellido.get(),
        #     "nombres": self.sv_nombres.get(),
        #     "direccion": self.sv_direccion.get(),
        #     "localidad": self.sv_localidad.get(),
        #     "provincia": self.sv_provincia.get(),
        #     "postal": self.sv_postal.get(),
        #     "telef_pers": self.sv_telef_pers.get(),
        #     "telef_trab": self.sv_telef_trab.get(),
        #     "mail": self.sv_mail.get(),
        #     "fecha_ingreso": self.sv_fecha_ingreso.get(),
        #     "sit_fis": self.sv_sit_fis.get(),
        #     "cuit": self.sv_cuit.get(),
        #     "observaciones": self.sv_observaciones.get(),
        #     "apenombre": self.sv_apellido.get() + ' ' + self.sv_nombres.get()
        # }
        """

        #-----------------------------------------------------------------
        # GUARDADO DATOS Y EVALUACION DEL PROCEDIMIENTO
        #-----------------------------------------------------------------
        id_ref = ""
        try:
            if self.alta_modif == 1:
                self.id_nuevo = self.varClientes.insertar_clientes(dic_clientes)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                self.varClientes.modificar_clientes(dic_clientes)
                id_ref = self.clave
        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Insertar/Modificar clientes", str(e))
            return
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        # Terminacion y habilitaciones
        self.filtro_activo = "ORDER BY apellido, nombres ASC"
        self.limpiar_text()
        self.habilitar_btn_B("disabled")
        self.habilitar_btn_A("normal")
        self.llena_grilla(id_ref)
        self.grid_clientes.focus()
        self.habilitar_text("disabled")
        self.alta_modif = 0

    # --------------------------------------------------------------------------
    # VARIAS -*-
    # --------------------------------------------------------------------------

    def doble_click_grid(self, event):
        self.feditar()

    def limitador(self, entry_text, caract):
        entry_text.set(entry_text.get()[:caract])

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        # Ejecuto funcion validar_fecha en funcion_new
        retorno_validacion = self.varFuncion_new.validar_fecha(self.sv_fecha_ingreso, self.entry_fecha_ingreso)

        una_fecha = date.today()

        match retorno_validacion:

            case "break":
                self.entry_fecha_ingreso.focus()
                return
            case "S":
                self.entry_fecha_ingreso.focus()
            case "N" | "BLANCO":
                pass
            case "":
                self.sv_fecha_ingreso.set(una_fecha.strftime('%d/%m/%Y'))
                self.entry_fecha_ingreso.focus()
            case _:
                return

    # --------------------------------------------------------------------------
    # PUNTEROS Y ORDEN -*-
    # --------------------------------------------------------------------------

    def forden_codigo(self):
        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY codigo ASC"
        self.llena_grilla(self.clave)

    def forden_apellido(self):
        # guardo los focos e items donde estamos posicionados en el TV
        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY apellido, nombres ASC"
        self.llena_grilla(self.clave)

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_clientes, 'TOP')

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_clientes, 'END')

    def fbuscar_en_tabla(self):

        # Buscar en el Grid
        if len(self.entry_buscar_cliente.get()) <= 0:
            self.status.set_status("⚠ No ingreso busqueda", "warn")
            return

        # Obtengo string a buscar
        se_busca = self.entry_buscar_cliente.get()

        # con GPT ||||||||||||||||||||||||||||||||||||||||||||||||||
        # Retorno las coincidencias
        try:
            datos = self.varClientes.buscar_clientes(se_busca)
        except Exception:
            self.varFuncion_new.mostrar_error()
            return

        # Limpio el grid
        for item in self.grid_clientes.get_children():
            self.grid_clientes.delete(item)

        # carga la grilla con los registros seleccionados
        for row in datos:
            self.grid_clientes.insert("", "end", text=row[0], values=row[1:])
            # 👉 row[1:] significa:desde el segundo elemento en adelante o sea: row[1], row[2], row[3]...

        items = self.grid_clientes.get_children()

        # selecciono el primero de la tabla y pongo foco y visibilidad
        if items:
            primero = items[0]
            self.grid_clientes.selection_set(primero)
            self.grid_clientes.focus(primero)
            self.grid_clientes.see(primero)
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    def fshowall(self):
        self.selected = self.grid_clientes.focus()
        self.clave = self.grid_clientes.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY apellido, nombres ASC"
        self.llena_grilla(self.clave)

    def cuadro_botones_grid(self):

        for c in range(1):
            self.botones1.grid_columnconfigure(c, weight=1, minsize=140)

        # Nuevo cliente
        icono = self.cargar_icono("archivo-nuevo.png")
        self.btn_nuevo=tk.Button(self.botones1, text=" Nuevo", command=self.fnuevo, bg="blue", fg="white", compound="left")
        self.btn_nuevo.image = icono
        self.btn_nuevo.config(image=icono)
        self.btn_nuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_nuevo, msg="Ingresar un nuevo cliente")

        # Modificar un cliente
        icono = self.cargar_icono("editar.png")
        self.btn_editar=tk.Button(self.botones1, text=" Editar", command=self.feditar, bg="blue", fg="white",
                               compound="left")
        self.btn_editar.image = icono
        self.btn_editar.config(image=icono)
        self.btn_editar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_editar, msg="Modificar datos de un cliente")

        # Eliminar un cliente
        icono = self.cargar_icono("eliminar.png")
        self.btn_eliminar=tk.Button(self.botones1, text=" Eliminar", command=self.feliminar, bg="red", fg="white",
                                 compound="left")
        self.btn_eliminar.image = icono
        self.btn_eliminar.config(image=icono)
        self.btn_eliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_eliminar, msg="Elimina un cliente")

        # Guardar datos del cliente
        icono = self.cargar_icono("guardar.png")
        self.btn_guardar=tk.Button(self.botones1, text=" Guardar", command=self.fguardar, bg="green", fg="white",
                                compound="left")
        self.btn_guardar.image = icono
        self.btn_guardar.config(image=icono)
        self.btn_guardar.grid(row=3, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_guardar, msg="Guarda los datos del cliente")

        # Guardar datos del cliente
        icono = self.cargar_icono("cancelar.png")
        self.btn_cancelar=tk.Button(self.botones1, text=" Cancelar", command=self.fcancelar, bg="black", fg="white",
                                 compound="left")
        self.btn_cancelar.image = icono
        self.btn_cancelar.config(image=icono)
        self.btn_cancelar.grid(row=4, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_cancelar, msg="Cancela lo que se este realizando")

        # reordenamiento de self.frame_botones_grid
        for widg in self.botones1.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def cuadro_botones_movimiento(self):

        for c in range(3):
            self.botones2.grid_rowconfigure(c, weight=1, minsize=30)

        # Ordena datos por codigo de cliente
        icono = self.cargar_icono("ordenar.png")
        self.btn_orden_codigo = tk.Button(self.botones2, text=" Orden Codigo", command=self.forden_codigo,
                                       bg="grey", fg="white", compound="left")
        self.btn_orden_codigo.image = icono
        self.btn_orden_codigo.config(image=icono)
        self.btn_orden_codigo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_orden_codigo, msg="Ordena la informacion por codigo de cliente")

        # Ordenar los datos ppor apellido y nombre
        icono = self.cargar_icono("ordenar.png")
        self.btn_orden_apellido = tk.Button(self.botones2, text=" Orden Apellido", command=self.forden_apellido,
                                         bg="grey", fg="white", compound="left")
        self.btn_orden_apellido.image = icono
        self.btn_orden_apellido.config(image=icono)
        self.btn_orden_apellido.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_orden_apellido, msg="Ordena la informacion por Apellido y nombre de cliente")

        # Guardar datos del cliente
        icono = self.cargar_icono("reset.png")
        self.btn_reset = tk.Button(self.botones2, text=" Reset", command=self.freset, bg="black", fg="white",
                                compound="left")
        self.btn_reset.image = icono
        self.btn_reset.config(image=icono)
        self.btn_reset.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_reset, msg="Vuelve al estado inicial")

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.botones2, text="", image=self.photo4, command=self.ftoparch, bg="grey", fg="white")
        self.btnToparch.grid(row=3, column=0, padx=5, sticky="nsew", pady=3)

        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.botones2, text="", image=self.photo5, command=self.ffinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=4, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # reordenamiento de self.frame_botones_grid
        for widg in self.botones2.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def cuadro_boton_salida(self):
        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=tk.Button(self.botones3, text="Salir", image=self.photo3, command=self.fsalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")

    def cuadro_cartel_clientes(self):
        fff = tkfont.Font(family="Arial", size=9, weight="bold")
        self.lbl_cant_clientes = tk.Label(self.botones4, text="Clientes", font=fff)
        self.lbl_cant_clientes1= tk.Label(self.botones4, textvariable=self.sv_cant_clientes, font=fff)
        self.lbl_cant_clientes.grid(row=0, column=0, padx=5, pady=3, columnspan=2, sticky='nsew')
        self.lbl_cant_clientes1.grid(row=1, column=0, padx=5, pady=3, columnspan=2, sticky='nsew')

    def cuadro_entrys(self):
        # CODIGO
        self.lbl_codigo = tk.Label(self.sector_entry, text="Codigo: ")
        self.lbl_codigo.grid(row=0, column=0, padx=10, pady=3, sticky="w")
        self.entry_codigo = tk.Entry(self.sector_entry, textvariable=self.sv_codigo, justify="right", width=10)
        self.sv_codigo.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_codigo, 10))
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=3, sticky="w")
        # APELLIDO
        self.lbl_apellido = tk.Label(self.sector_entry, text="Apellido: ")
        self.lbl_apellido.grid(row=1, column=0, padx=10, pady=3, sticky="w")
        self.entry_apellido=tk.Entry(self.sector_entry, textvariable=self.sv_apellido, justify="left", width=40)
        self.sv_apellido.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_apellido, 40))
        self.entry_apellido.grid(row=1, column=1, padx=10, pady=3, sticky="w")
        # NOMBRES
        self.lbl_nombres = tk.Label(self.sector_entry, text="Nombres: ")
        self.lbl_nombres.grid(row=2, column=0, padx=10, pady=3, sticky="w")
        self.entry_nombres = tk.Entry(self.sector_entry, textvariable=self.sv_nombres, justify="left", width=40)
        self.sv_nombres.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_nombres, 40))
        self.entry_nombres.grid(row=2, column=1, padx=10, pady=3, sticky="w")
        # DIRECCION
        self.lbl_direccion = tk.Label(self.sector_entry, text="Direccion: ")
        self.lbl_direccion.grid(row=3, column=0, padx=10, pady=3, sticky="w")
        self.entry_direccion=tk.Entry(self.sector_entry, textvariable=self.sv_direccion, justify="left", width=40)
        self.sv_direccion.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_direccion, 30))
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=3, sticky="w")
        # LOCALIDAD
        self.lbl_localidad = tk.Label(self.sector_entry, text="Localidad: ")
        self.lbl_localidad.grid(row=4, column=0, padx=10, pady=3, sticky="w")
        self.entry_localidad=tk.Entry(self.sector_entry, textvariable=self.sv_localidad, justify="left", width=40)
        self.sv_localidad.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_localidad, 30))
        self.entry_localidad.grid(row=4, column=1, padx=10, pady=3, sticky="w")
        # PROVINCIA
        self.lbl_provincia = tk.Label(self.sector_entry, text="Provincia: ")
        self.lbl_provincia.grid(row=5, column=0, padx=10, pady=3, sticky="w")
        self.entry_provincia=tk.Entry(self.sector_entry, textvariable=self.sv_provincia, justify="left", width=40)
        self.sv_provincia.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_provincia, 30))
        self.entry_provincia.grid(row=5, column=1, padx=10, pady=3, sticky="w")
        # POSTAL
        self.lbl_postal = tk.Label(self.sector_entry, text="Cod. Postal: ")
        self.lbl_postal.grid(row=6, column=0, padx=10, pady=3, sticky="w")
        self.entry_postal=tk.Entry(self.sector_entry, textvariable=self.sv_postal, justify="left", width=40)
        self.sv_postal.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_postal, 30))
        self.entry_postal.grid(row=6, column=1, padx=10, pady=3, sticky="w")
        # TELEFONO PERSONAL
        self.lbl_telefono_pers = tk.Label(self.sector_entry, text="Telefono Personal: ")
        self.lbl_telefono_pers.grid(row=0, column=2, padx=10, pady=3, sticky="w")
        self.entry_telefono_pers=tk.Entry(self.sector_entry, textvariable=self.sv_telef_pers, justify="left", width=40)
        self.sv_telef_pers.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_telef_pers, 30))
        self.entry_telefono_pers.grid(row=0, column=3, padx=10, pady=3, sticky="w")
        # TELEFONO TRABAJO
        self.lbl_telefono_trab = tk.Label(self.sector_entry, text="Telefono Trabajo: ")
        self.lbl_telefono_trab.grid(row=1, column=2, padx=10, pady=3, sticky="w")
        self.entry_telefono_trab=tk.Entry(self.sector_entry, textvariable=self.sv_telef_trab, justify="left", width=40)
        self.sv_telef_trab.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_telef_trab, 30))
        self.entry_telefono_trab.grid(row=1, column=3, padx=10, pady=3, sticky="w")
        # CORREO ELECTRONICO
        self.lbl_mail = tk.Label(self.sector_entry, text="Correo Electronico: ")
        self.lbl_mail.grid(row=2, column=2, padx=10, pady=3, sticky="w")
        self.entry_mail=tk.Entry(self.sector_entry, textvariable=self.sv_mail, justify="left", width=40)
        self.sv_mail.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_mail, 30))
        self.entry_mail.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        # SITUACION FISCAL - COMBOBOX
        self.lbl_sit_fiscal = tk.Label(self.sector_entry, text="Situacion Fiscal: ")
        self.lbl_sit_fiscal.grid(row=3, column=2, padx=10, pady=3, sticky="w")
        self.combo_sit_fiscal = ttk.Combobox(self.sector_entry, textvariable=self.sv_sit_fis, state='readonly',
                                             width=40)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                           "RM - Responsable Monotributo", "EX - Exento",
                                           "RN - Responsable no inscripto"]
        self.combo_sit_fiscal.grid(row=3, column=3, padx=10, pady=5, sticky="w")
        # CUIT
        self.lbl_cuit = tk.Label(self.sector_entry, text="CUIT - CUIL: ")
        self.lbl_cuit.grid(row=4, column=2, padx=10, pady=3, sticky="w")
        self.entry_cuit=tk.Entry(self.sector_entry, textvariable= self.sv_cuit, justify="left", width=40)
        self.sv_cuit.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_cuit, 11))
        self.entry_cuit.grid(row=4, column=3, padx=10, pady=3, sticky="w")
        # FECHA DE INGRESO
        self.lbl_fecha_ingreso = tk.Label(self.sector_entry, text="Fecha Ingreso: ")
        self.lbl_fecha_ingreso.grid(row=5, column=2, padx=10, pady=3, sticky="w")
        self.entry_fecha_ingreso=tk.Entry(self.sector_entry, textvariable=self.sv_fecha_ingreso, justify="left",
                                       width=40)
        self.entry_fecha_ingreso.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_ingreso.grid(row=5, column=3, padx=10, pady=3, sticky="w")
        # Label y entry OBSERVACIONES
        self.lbl_observaciones = tk.Label(self.sector_entry, text="Observaciones: ")
        self.lbl_observaciones.grid(row=6, column=2, padx=10, pady=3, sticky="w")
        self.entry_observaciones = tk.Entry(self.sector_entry, textvariable=self.sv_observaciones, justify="left",
                                         width=40)
        self.sv_observaciones.trace_add("write", lambda _name, _index, _mode: self.limitador(self.sv_observaciones, 100))
        self.entry_observaciones.grid(row=6, column=3, padx=10, pady=3, sticky="w")

    def cuadro_buscar(self):

        for c in range(4):
            self.frame_buscar.grid_columnconfigure(c, weight=2, minsize=50)

        # COLUMNAS MAS CORTAS
        self.frame_buscar.grid_columnconfigure(0, weight=1, minsize=50)
        # self.frame_buscar.grid_columnconfigure(3, weight=1, minsize=50)
        # self.frame_buscar.grid_columnconfigure(2, weight=3, minsize=50)
        # self.frame_botones_grid.grid_columnconfigure(8, weight=1, minsize=50)

        # BUSCAR UN CLIENTE
        img = Image.open("buscar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.lbl_buscar_cliente = tk.Label(self.frame_buscar, text="Buscar: ", compound="left")
        self.lbl_buscar_cliente.image = icono
        self.lbl_buscar_cliente.config(image=icono)
        self.lbl_buscar_cliente.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")

        # ENTRY BUSCAR CLIENTE
        self.entry_buscar_cliente=tk.Entry(self.frame_buscar)
        self.entry_buscar_cliente.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        ToolTip(self.entry_buscar_cliente, msg="Escriba el nombre o apellido del cliente buscado")

        # BOTON BUSCAR UN CLIENTE
 #       img = Image.open("filtrar.png").resize((18, 18))
        icono = self.cargar_icono("filtrar.png")
#        icono = ImageTk.PhotoImage(img)
        self.btn_buscar_cliente = tk.Button(self.frame_buscar, text=" Buscar", command=self.fbuscar_en_tabla,
                                         bg="CadetBlue", fg="white", width=30, compound="left")
        self.btn_buscar_cliente.image = icono
        self.btn_buscar_cliente.config(image=icono)
        self.btn_buscar_cliente.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")
        ToolTip(self.btn_buscar_cliente, msg="Presenta los clientes que coinciden con la busqueda")

        # BOTON MOSTRAR TODOS LOS CLIENTES
        icono = self.cargar_icono("ver_todo.png")
        self.btn_mostrar_todo = tk.Button(self.frame_buscar, text=" Mostrar todo", command=self.fshowall, bg="CadetBlue",
                                       width=30, fg="white", compound="left")
        self.btn_mostrar_todo.image = icono
        self.btn_mostrar_todo.config(image=icono)
        self.btn_mostrar_todo.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")
        ToolTip(self.btn_mostrar_todo, msg="Muestra todos los clientes")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_buscar.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_grid_clientes(self):

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.frame_principal)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_clientes = ttk.Treeview(self.frame_principal, height=10, columns=("col1", "col2", "col3", "col4", "col5",
                                                                             "col6", "col7", "col8", "col9", "col10",
                                                                             "col11", "col12", "col13", "col14"))

        self.grid_clientes.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_clientes.column("#0", width=60, anchor="center")
        self.grid_clientes.column("col1", width=60, anchor="center")
        self.grid_clientes.column("col2", width=180, anchor="w")
        self.grid_clientes.column("col3", width=220, anchor="w")
        self.grid_clientes.column("col4", width=220, anchor="w")
        self.grid_clientes.column("col5", width=120, anchor="center")
        self.grid_clientes.column("col6", width=90, anchor="center")
        self.grid_clientes.column("col7", width=60, anchor="center")
        self.grid_clientes.column("col8", width=200, anchor="center")
        self.grid_clientes.column("col9", width=200, anchor="center")
        self.grid_clientes.column("col10", width=200, anchor="center")
        self.grid_clientes.column("col11", width=150, anchor="center")
        self.grid_clientes.column("col12", width=100, anchor="center")
        self.grid_clientes.column("col13", width=100, anchor="center")
        self.grid_clientes.column("col14", width=200, anchor="center")

        self.grid_clientes.heading("#0", text="Id", anchor="center")
        self.grid_clientes.heading("col1", text="Codigo", anchor="center")
        self.grid_clientes.heading("col2", text="Apellido", anchor="center")
        self.grid_clientes.heading("col3", text="Nombres", anchor="center")
        self.grid_clientes.heading("col4", text="Direccion", anchor="center")
        self.grid_clientes.heading("col5", text="Localidad", anchor="center")
        self.grid_clientes.heading("col6", text="Provincia", anchor="center")
        self.grid_clientes.heading("col7", text="Postal", anchor="center")
        self.grid_clientes.heading("col8", text="Telf.Personal", anchor="center")
        self.grid_clientes.heading("col9", text="Telf.Trabajo", anchor="center")
        self.grid_clientes.heading("col10", text="E-mail", anchor="center")
        self.grid_clientes.heading("col11", text="Sit.Fiscal", anchor="center")
        self.grid_clientes.heading("col12", text="CUIT", anchor="center")
        self.grid_clientes.heading("col13", text="Fec.Ingreso", anchor="center")
        self.grid_clientes.heading("col14", text="Observaciones", anchor="center")

        self.grid_clientes.tag_configure('oddrow', background='light grey')
        self.grid_clientes.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_principal, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_principal, orient="vertical")
        self.grid_clientes.config(xscrollcommand=scroll_x.set)
        self.grid_clientes.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_clientes.xview)
        scroll_y.config(command=self.grid_clientes.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        # -------------------------------------------------------------------------
        # PACK - GENERALES
        self.grid_clientes.pack(side= "top", fill="both", expand=1, padx=1, pady=5)

    def cuadro_titulos(self):

        # LOGO<
        self.photo3 = Image.open('clientes4.png')
        self.photo3 = self.photo3.resize((105, 75), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_clientes = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_clientes = tk.Label(self.frame_titulo_top, image=self.png_clientes, bg="red", relief="ridge", bd=5, padx=5)
        # TITULO
        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=25, text="Clientes", bg="black", fg="gold",
                                font=("Arial bold", 38, "bold"), bd=5, relief="ridge")

        # COLOCO EL LOGO A LA IZQUIERDA Y EL TITULO AL LADO
        self.lbl_png_clientes.grid(row=0, column=0, sticky="w", padx=5, ipadx=20)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew", padx=12)

    def barra_lateral_botones(self):

        # BOTONES GRID - BOTONES 1
        self.botones1 = tk.LabelFrame(self.barra_botones, bd=5, relief="ridge")
        self.cuadro_botones_grid()
        self.botones1.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES ORDEN - TOPE Y FIN DE ARCHIVO - BOTONES 2
        self.botones2 = tk.LabelFrame(self.barra_botones, bd=5, relief="ridge")
        self.cuadro_botones_movimiento()
        self.botones2.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES SALIDA - BOTONES 3
        self.botones3 = tk.LabelFrame(self.barra_botones)
        self.cuadro_boton_salida()
        self.botones3.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES ROTULO CANT DE CLIENTES - BOTONES 4
        self.botones4 = tk.LabelFrame(self.barra_botones)
        self.cuadro_cartel_clientes()
        self.botones4.pack(side="top", padx=3, pady=3, fill="y")

    def cargar_icono(self, path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def get_clientes_dic(self, fecha_aux):

        return {
            "Id": self.clave,
            "codigo": self.sv_codigo.get(),
            "apellido": self.sv_apellido.get(),
            "nombres": self.sv_nombres.get(),
            "direccion": self.sv_direccion.get(),
            "localidad": self.sv_localidad.get(),
            "provincia": self.sv_provincia.get(),
            "postal": self.sv_postal.get(),
            "telef_pers": self.sv_telef_pers.get(),
            "telef_trab": self.sv_telef_trab.get(),
            "mail": self.sv_mail.get(),
            "fecha_ingreso": fecha_aux,
            "sit_fis": self.sv_sit_fis.get(),
            "cuit": self.sv_cuit.get(),
            "observaciones": self.sv_observaciones.get(),
            "apenombre": self.sv_apellido.get() + ' ' + self.sv_nombres.get()
        }


"""
🔥 CÓMO USAR SET_STATUS
✔ Guardar
self.set_status("✔ Registro guardado correctamente", "ok")
🗑 Eliminar
self.set_status("🗑 Cliente eliminado", "ok")
⚠ Validación
self.set_status("⚠ CUIT incorrecto", "warn")
❌ Error
self.set_status("❌ Error al guardar", "error")
ℹInfo
self.set_status("ℹ Buscando clientes...", "info")
"""
