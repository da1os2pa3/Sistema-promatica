import tkinter as tk
from datetime import date
from tkinter import ttk
# from tkinter import messagebox
from tkinter.scrolledtext import *
# ------------------------------------------------
from PIL import Image, ImageTk
from dateutil.relativedelta import relativedelta
# ------------------------------------------------
from funcion_new import ClaseFuncionNew
from funciones import *
from garantias_ABM import DatosGarantias
from status_bar import StatusBar

class ClaseGarantias(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master
        self.status = StatusBar(self.master)

        self.master.grab_set()
        self.master.focus_set()

        # Instanciaciones -----------------------------------------------------------
        """ Creo una instancia de clase varGarantia. Le paso la pantalla para poder usar los parent 
            en los mensajes de messagebox. """
        self.varGarantia = DatosGarantias(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # ---------------------------------------------------------------------------

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
        alto_ventana = 645
        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
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
        # ...................................................................
        # # guarda en item el Id del elemento fila en este caso fila 0      .
        # item = self.grid_garantias.identify_row(0)                        .
        # self.grid_garantias.selection_set(item)                           .
        # # pone el foco en el item seleccionado                            .
        # self.grid_garantias.focus(item)                                   .
        # ...................................................................

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        # ---------------------------------------------------------------------------
        # TITULOS - Encabezado logo y titulo con PACK
        # --------------------------------------------------------------------------
        self.frame_titulo_top = tk.Frame(self.master)
        self.cuadro_titulos()
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # VARIABLES GENERALES
        # --------------------------------------------------------------------------
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # --------------------------------------------------------------------------
        # STRINGVARS
        # --------------------------------------------------------------------------
        self.sv_valor_dolar_hoy = tk.StringVar(value="0.00")

        self.traer_dolarhoy()

        self.sv_buscostring =tk.StringVar(value="")
        self.sv_nombre_cliente = tk.StringVar(value="")
        self.sv_codigo_cliente = tk.StringVar(value="0")
        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.sv_fecha_movim = tk.StringVar(value=una_fecha)
        self.sv_fecha_vto = tk.StringVar(value=una_fecha)
        self.sv_detalle_articulo = tk.StringVar(value="")
        self.sv_total_oper = tk.StringVar(value="0")
        self.sv_meses = tk.StringVar(value="1")
        self.sv_numero_factura = tk.StringVar(value="")
        self.sv_observaciones = tk.StringVar(value="")

        # ------------------------------------------------------------------------
        # TREVIEEW - GRID
        # ------------------------------------------------------------------------
        self.frame_tvw_garantias=tk.LabelFrame(self.master, text="Garantias: ", foreground="#CF09BD")
        self.cuadro_grid()
        self.frame_tvw_garantias.pack(side="top", fill="both", padx=5, pady=2)

        # --------------------------------------------------------------------------
        # BUSQUEDA DE UNA GARANTIA
        # --------------------------------------------------------------------------
        self.frame_busco_garantia=tk.LabelFrame(self.master, text="", background="light blue", foreground="red")
        self.cuadro_buscar()
        self.frame_busco_garantia.pack(side="top", fill="both", expand=0, padx=5, pady=3)

        # --------------------------------------------------------------------------
        # BOTONES DEL TREEVIEW
        # --------------------------------------------------------------------------
        self.frame_primero=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_botones_crud()
        self.frame_primero.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # --------------------------------------------------------------------------
        # ENTRYS - PEDIDO DE DATOS
        # --------------------------------------------------------------------------
        self.frame_segundo=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys()
        self.frame_segundo.pack(side="top", fill="both",expand=0, padx=5, pady=3)

        # --------------------------------------------------------------------------
        # ENTRYS - DETALLES
        # --------------------------------------------------------------------------
        self.frame_tercero=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys_detalles()
        self.frame_tercero.pack(side="top", fill="both",expand=0, padx=5, pady=3)

        # --------------------------------------------------------------------------
        # ENTRYS - DATOS FACTURA Y OBSERVACIONES
        # --------------------------------------------------------------------------
        self.frame_cuarto=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys_factobs()
        self.frame_cuarto.pack(side="top", fill="both",expand=0, padx=5, pady=3)

        # --------------------------------------------------------------------------
        # ENTRYS - TEXTO DETALLE
        # --------------------------------------------------------------------------
        self.frame_quinto=tk.LabelFrame(self.master, text="Observaciones", foreground="blue")
        self.cuadro_entrys_texto_detalles()
        self.frame_quinto.pack(side="top", fill="both", expand=0, padx=5, pady=3)

    # ------------------------------------------------------------------------------
    # GRID
    # ------------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        # limpiar la grilla
        for item in self.grid_garantias.get_children():
            self.grid_garantias.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varGarantia.consultar_garantia(self.filtro_activo)
        else:
            datos = self.varGarantia.consultar_garantia("ORDER BY gt_fechavto ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024 y le digo si va con la hora tambien o no
            # forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'), False)
            # forma_normal2 = fecha_str_reves_normal(self, datetime.strftime(row[3], '%Y-%m-%d'), False)
            forma_normal = self.varFuncion_new.fecha_es(datetime.strftime(row[1], '%Y-%m-%d'), False)
            forma_normal2 = self.varFuncion_new.fecha_es(datetime.strftime(row[3], '%Y-%m-%d'), False)

            self.grid_garantias.insert("", "end", tags=color, text=row[0], values=(forma_normal, row[2],
                                                    forma_normal2, row[4], row[5], row[6], row[7], row[8], row[9]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_garantias.get_children()
        # Si no hay filas (grid vacio), salgo sin intentar seleccionar
        if not children:
            self.status.set_status("ℹ Grid vacio...", "info")
            return

        # Si el parametro set_foco esta vacío (no hay foco), voy al ultimo de la grilla,
        # caso contrario, voy a la clave que se haya enviado en set_foco para dejar el puntero.
        if not set_foco:
            # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
            posicion = children[-1]                      # ultimo
            # posicion = children[0]                     # primero
            self.grid_garantias.focus_set()
            self.grid_garantias.focus(posicion)
            self.grid_garantias.selection_set(posicion)
            self.grid_garantias.see(posicion)
        else:
            for item in children:
                texto = self.grid_garantias.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_garantias.update_idletasks()
                    self.grid_garantias.focus_set()
                    self.grid_garantias.selection_set(item)
                    self.grid_garantias.focus(item)
                    self.grid_garantias.see(item)
                    break

    # -----------------------------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------------------------

    def estado_inicial(self):

        # Variables
        self.alta_modif = 0
        self.dato_seleccion = ""
        self.filtro_activo = "ORDER BY gt_fechavto ASC"
        # Grilla
        self.selected = self.grid_garantias.focus()
        self.clave = self.grid_garantias.item(self.selected, 'text')
        # Estado inicial del Gui
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_A("normal")
        self.habilitar_btn_B("disabled")
        self.habilitar_btn_busquedas("normal")

    def limpiar_text(self):

        # Limpio los entrys y asigno valores iniciales en algunos campos necesarios
        if self.alta_modif == 1:
            una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
            self.sv_fecha_movim.set(value=una_fecha)
            self.sv_fecha_vto.set(value=una_fecha)
        elif self.alta_modif == 2 or self.alta_modif == 0:
            self.sv_fecha_movim.set(value="")
            self.sv_fecha_vto.set(value="")

        self.sv_meses.set(value="1")
        self.sv_total_oper.set(value="0")
        self.sv_detalle_articulo.set(value="")
        self.sv_nombre_cliente.set(value="")
        self.sv_codigo_cliente.set(value="0")
        self.sv_numero_factura.set(value="")
        self.sv_observaciones.set(value="")
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

    def habilitar_btn_busquedas(self, estado):
        self.btn_filtrar_movim.configure(state=estado)
        self.btn_showall_movim.configure(state=estado)
        self.entry_buscar_movim.configure(state=estado)

    # -------------------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------------------

    def fnuevo(self):

        self.alta_modif = 1
        self.habilitar_text("normal")
        self.limpiar_text()
        self.habilitar_btn_busquedas("disabled")
        self.habilitar_btn_A("disabled")
        self.habilitar_btn_B("normal")
        self.entry_fecha_movim.focus()

    def feditar(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_garantias.focus()
        # Asi obtengo la clave de la tabla (campo Id) que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_garantias.item(self.selected, 'text')

        if self.clave == "":
            self.status.set_status("❌ No hay nada seleccionado", "error")
            return

        self.alta_modif = 2

        self.habilitar_text('normal')
        self.limpiar_text()

        self.filtro_activo = "WHERE Id = " + str(self.clave)

        valores = self.varGarantia.consultar_garantia(self.filtro_activo)

        for row in valores:

            if row[1] == "None":
                messagebox.showerror("Error", "Error de fechas en Tabla, elimine el item y "
                                              "vuelva a cargarlo ", parent=self)
                self.estado_inicial()
                return

            # Convierto fechas a dd/mm/aaa
            forma_normal = self.varFuncion_new.fecha_es(datetime.strftime(row[1], '%Y-%m-%d'), False)
            forma_normal2 = self.varFuncion_new.fecha_es(datetime.strftime(row[3], '%Y-%m-%d'), False)

            self.entry_fecha_movim.insert(0, forma_normal)
            self.sv_fecha_vto.set(value=forma_normal2)
            self.entry_meses.insert(0, row[2])
            self.sv_codigo_cliente.set(value=row[4])
            self.entry_nombre_cliente.insert(0, row[5])
            self.entry_detalle_articulo.insert(0, row[6])
            self.entry_total_oper.insert(0, row[7])
            self.entry_numero_factura.insert(0, row[8])
            self.entry_observaciones.insert(0, row[9])
            self.text_detalle.insert("end", row[10])

        self.habilitar_btn_busquedas("disabled")
        self.habilitar_btn_A("disabled")
        self.habilitar_btn_B("normal")
        self.entry_nombre_cliente.focus()

    def fborrar(self):

        # ------------------------------------------------------------------------------
        # guardo item seleccionado en el grid
        self.selected = self.grid_garantias.focus()
        self.selected_ant = self.grid_garantias.prev(self.selected)
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_garantias.item(self.selected, 'text')
        self.clave_ant = self.grid_garantias.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "" or self.selected == "":
            self.status.set_status("❌ No hay nada seleccionado", "error")
            return

        valores = self.grid_garantias.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[4]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        try:
            self.varGarantia.eliminar_item_garantia(self.clave)
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("🗑 Registro eliminado correctamente", "ok")

        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # -------------------------------------------------------------------
        # VALIDACIONES
        # -------------------------------------------------------------------

        # FECHA
        if not self.sv_fecha_movim.get() or not self.sv_fecha_vto.get():
            messagebox.showerror("Error", "Fecha en blanco", parent=self)
            self.entry_fecha_movim.focus()
            return
        # DETALLE
        if not self.sv_nombre_cliente.get():
            messagebox.showerror("Error", "Agregue un cliente", parent=self)
            self.entry_nombre_cliente.focus()
            return

        # guardo el Id del Treeview en selected para ubicacion del foco a posterior (i001, i002....
        self.selected = self.grid_garantias.focus()
        # Guardo Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en TABLA 1,2,3)
        self.clave = self.grid_garantias.item(self.selected, 'text')

        # -----------------------------------------------------------------
        # PASO DICCIONARIO PARA INSERTAR O MODIFICAR
        """ Debo poner los nombres de los campos de la tabla y asignarles las variables """

        dic_garantias = {
            "Id": self.clave,
            "gt_fechaventa": self.sv_fecha_movim.get(),
            "gt_meses": self.sv_meses.get(),
            "gt_fechavto": self.sv_fecha_vto.get(),
            "gt_codcli": self.sv_codigo_cliente.get(),
            "gt_nomcli": self.sv_nombre_cliente.get(),
            "gt_articulo": self.sv_detalle_articulo.get(),
            "gt_impventa": self.sv_total_oper.get(),
            "gt_factura": self.sv_numero_factura.get(),
            "gt_observaciones": self.sv_observaciones.get(),
            "gt_detalle": self.text_detalle.get(1.0, 'end-1c')
        }
        # -----------------------------------------------------------------

        id_ref = ""

        try:
        # a = 00
        # if a == 00:
            if self.alta_modif == 1:
                self.id_nuevo = self.varGarantia.insertar_garantias(dic_garantias)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                self.varGarantia.modificar_garantias(dic_garantias)
                id_ref = self.clave
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        self.filtro_activo = "garantias ORDER BY gt_fechavto ASC"
        self.limpiar_text()
        self.llena_grilla(id_ref)
        self.estado_inicial()
        self.grid_garantias.focus()

    def fcancelar(self):
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_inicial()

    def fSalir(self):
        self.master.destroy()

    def fNo_modifique(self, event):
        return

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.sv_buscostring.get()) > 0:
            se_busca = self.sv_buscostring.get()
            self.filtro_anterior = self.filtro_activo
            self.filtro_activo = ("WHERE INSTR(gt_nomcli, '" + se_busca + "') > 0")
            self.varGarantia.buscar_entabla(self.filtro_activo)
            self.llena_grilla("")

            """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
                item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
            item = self.grid_garantias.selection()
            self.grid_garantias.focus(item)
        else:
            self.status.set_status("❌ No ingreso busqueda", "error")

    def fshowall(self):
        self.selected = self.grid_garantias.focus()
        self.clave = self.grid_garantias.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY gt_fechavto ASC"
        self.llena_grilla(self.clave)

    # -------------------------------------------------------------------------
    # PUNTEROS
    # -------------------------------------------------------------------------

    def fToparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_garantias, 'TOP')

    def fFinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_garantias, 'END')

    # ------------------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------------------

    def traer_dolarhoy(self):
        dev_informa = self.varGarantia.consultar_informa()
        for row in dev_informa:
            self.sv_valor_dolar_hoy.set(value=row[21])

    def limitador(self, entry_text, caract):
        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def DobleClickGrid(self, event):
        self.feditar()

    def calcular_fechas(self):

        fecha1 = self.varFuncion_new.validar_fecha(self.sv_fecha_movim, self.entry_fecha_movim)

        if fecha1 == "break":
            self.entry_fecha_movim.focus_set()
            return "break"

        # Convertir el texto a datetime
        fecha1 = datetime.strptime(fecha1, '%d/%m/%Y')

        # Sumar los meses
        meses = int(self.sv_meses.get())
        fecha2 = fecha1 + relativedelta(months=meses)

        # Volver a texto para mostrarlo en el StringVar
        self.sv_fecha_vto.set(fecha2.strftime('%d/%m/%Y'))
        return None


    # ------------------------------------------------------------------------------
    # BUSQUEDA POR CLIENTE
    # ------------------------------------------------------------------------------

    def fbusclii(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda
        y en que campos debe hacerse. """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de como 
            quiero verlos.-Titulos para cada columna de esos campos y String de busqueda definido arriba(que_busco)."""

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                                                        "Orden: Alfabetico cliente", "N")

        """  Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes. """

        for item in valores_new:
            self.sv_nombre_cliente.set(value=item[15])
            self.sv_codigo_cliente.set(value=item[1])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # ------------------------------------------------------------------------------
    # BUSQUEDA POR ARTICULO ARTICULO
    # ------------------------------------------------------------------------------

    def fBusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse. """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.sv_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.sv_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.sv_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(codbar, '" + self.sv_detalle_articulo.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.sv_detalle_articulo.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.varFuncion_new.ventana_selec("articulos", "descripcion", "rubro",
                                                "marca", "Descripcion", "Rubro","Marca",
                                                        que_busco, "Orden: Rubro+Marca+Descripcion","N")

        for item in valores_new:
            self.sv_detalle_articulo.set(value=item[2]) # d<escripcion del articulo
            #self.sv__codigo_cliente.set(value=item[1])

        self.entry_detalle_articulo.focus()
        self.entry_detalle_articulo.icursor(tk.END)

    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # CUADROS FRAMES
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def cuadro_titulos(self):

        # Armo el logo y el titulo
        self.photocc = Image.open('garantia.png')
        self.photocc = self.photocc.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_garantia = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_garantia = tk.Label(self.frame_titulo_top, image=self.png_garantia, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=52, text="Garantias",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_garantia.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")

    def cuadro_grid(self):

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
        self.grid_garantias.column("col5", width=300, anchor="w", minwidth=280)
        self.grid_garantias.column("col6", width=600, anchor="w", minwidth=600)
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
        scroll_x = tk.Scrollbar(self.frame_tvw_garantias, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_tvw_garantias, orient="vertical")
        self.grid_garantias.config(xscrollcommand=scroll_x.set)
        self.grid_garantias.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_garantias.xview)
        scroll_y.config(command=self.grid_garantias.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_garantias['selectmode'] = 'browse'

        self.grid_garantias.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def cuadro_buscar(self):

        for c in range(4):
            self.frame_busco_garantia.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.cargar_icono("buscar.png")
        self.lbl_buscar_titulo = tk.Label(self.frame_busco_garantia, text=" Buscar garantia (nombre cliente): ",
                                       background="light blue", compound="left")
        self.lbl_buscar_titulo.image = icono
        self.lbl_buscar_titulo.config(image=icono)
        self.lbl_buscar_titulo.grid(row=0, column=0, padx=5, pady=3, sticky='nsew')

        # ENTRY BUSCAR
        self.entry_buscar_movim=tk.Entry(self.frame_busco_garantia,textvariable=self.sv_buscostring, width=50)
        self.entry_buscar_movim.grid(row=0, column=1, padx=5, pady=3, sticky='nsew')

        # BOTON FILTRAR
        icono = self.cargar_icono("filtrar.png")
        self.btn_filtrar_movim = tk.Button(self.frame_busco_garantia, text=" Buscar", command=self.fBuscar_en_tabla,
                                       bg="blue", fg="white", width=34, compound="left")
        self.btn_filtrar_movim.image = icono
        self.btn_filtrar_movim.config(image=icono)
        self.btn_filtrar_movim.grid(row=0, column=2, padx=5, pady=3, sticky='nsew')

        # BOTON SHOW ALL
        icono = self.cargar_icono("ver_todo.png")
        self.btn_showall_movim = tk.Button(self.frame_busco_garantia, text=" Mostrar todo", command=self.fshowall,
                                 bg="blue", fg="white", width=34, compound="left")
        self.btn_showall_movim.image = icono
        self.btn_showall_movim.config(image=icono)
        self.btn_showall_movim.grid(row=0, column=3, padx=5, pady=3, sticky='nsew')

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_busco_garantia.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_botones_crud(self):

        for c in range(5):
            self.frame_primero.grid_columnconfigure(c, weight=1, minsize=140)

        # BOTON NUEVO
        icono = self.cargar_icono("archivo-nuevo.png")
        self.btn_nuevoitem = tk.Button(self.frame_primero, text=" Nuevo Garantia", command=self.fnuevo, width=22,
                                       bg="blue", fg="white", compound="left")
        self.btn_nuevoitem.image = icono
        self.btn_nuevoitem.config(image=icono)
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)

        # BOTON EDITAR
        icono = self.cargar_icono("editar.png")
        self.btn_editaitem = tk.Button(self.frame_primero, text=" Editar Garantia", command=self.feditar, width=22,
                                    bg="blue", fg="white", compound="left")
        self.btn_editaitem.image = icono
        self.btn_editaitem.config(image=icono)
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)

        # BOTON BORRAR
        icono = self.cargar_icono("eliminar.png")
        self.btn_borraitem = tk.Button(self.frame_primero, text=" Eliminar Garantia", command=self.fborrar, width=22,
                                    bg="red", fg="white", compound="left")
        self.btn_borraitem.image = icono
        self.btn_borraitem.config(image=icono)
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)

        # BOTON GUARDAR
        icono = self.cargar_icono("guardar.png")
        self.btn_guardaritem = tk.Button(self.frame_primero, text=" Guardar Garantia", command=self.fguardar, width=21,
                                      bg="green", fg="white", compound="left")
        self.btn_guardaritem.image = icono
        self.btn_guardaritem.config(image=icono)
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)

        # BOTON CANCELAR
        icono = self.cargar_icono("cancelar.png")
        self.btn_cancelar = tk.Button(self.frame_primero, text=" Cancelar", command=self.fcancelar, width=21, bg="black",
                                   fg="white", compound="left")
        self.btn_cancelar.image = icono
        self.btn_cancelar.config(image=icono)
        self.btn_cancelar.grid(row=0, column=4, padx=5, pady=2)

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_primero.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

        # FIN y TOP ARCHIVO
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_primero, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=5, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_primero, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=6, padx=5, sticky="nsew", pady=2)

        # SALIDA
        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=tk.Button(self.frame_primero, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")

    def cuadro_entrys(self):

        # Fecha del movimiento
        self.lbl_fecha_movim = tk.Label(self.frame_segundo, text="Fecha Ingreso: ", justify="left")
        self.lbl_fecha_movim.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_fecha_movim = tk.Entry(self.frame_segundo, textvariable=self.sv_fecha_movim, width=10,
                                       justify="right")
        self.entry_fecha_movim.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        # Importe Debito
        self.lbl_meses = tk.Label(self.frame_segundo, text="Meses garantia: ", justify="left")
        self.lbl_meses.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_meses = tk.Entry(self.frame_segundo, textvariable=self.sv_meses, width=5, justify="right")
        self.entry_meses.config(validate="key", validatecommand=self.vcmd)
        self.entry_meses.bind("<FocusOut>", lambda e: self.varFuncion_new.corregir_al_salir(self.entry_meses))
        self.entry_meses.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.sv_meses.trace("w", lambda *args: self.limitador(self.sv_meses, 2))
        self.entry_meses.bind('<Tab>', lambda e: self.calcular_fechas())

        # Fecha vencimiento de garantia
        self.lbl_fecha_vto = tk.Label(self.frame_segundo, text="Fecha Vencimiento: ", justify="left")
        self.lbl_fecha_vto.grid(row=0, column=4, padx=5, pady=2, sticky="w")
        self.lbl_fecha_vto_sv = tk.Label(self.frame_segundo, textvariable=self.sv_fecha_vto, width=10,
                                          justify="right")
        #self.lbl_fecha_vto_sv.bind("<FocusOut>", self.formato_fecha)
        self.lbl_fecha_vto_sv.grid(row=0, column=5, padx=5, pady=2, sticky="w")

        # Importe venta articulo
        self.lbl_total_oper = tk.Label(self.frame_segundo, text="Total operacion: ", justify="left")
        self.lbl_total_oper.grid(row=0, column=6, padx=5, pady=2, sticky="w")
        self.entry_total_oper = tk.Entry(self.frame_segundo, textvariable=self.sv_total_oper, width=15, justify="right")
        self.entry_total_oper.config(validate="key", validatecommand=self.vcmd)
        self.entry_total_oper.bind("<FocusOut>", lambda e: self.varFuncion_new.corregir_al_salir(self.entry_total_oper))
        self.entry_total_oper.grid(row=0, column=7, padx=5, pady=2, sticky="w")
        self.sv_total_oper.trace("w", lambda *args: self.limitador(self.sv_total_oper, 15))

    def cuadro_entrys_detalles(self):

        # Detalle del articulo
        self.lbl_detalle_articulo = tk.Label(self.frame_tercero, text="Detalle articulo: ", justify="left")
        self.lbl_detalle_articulo.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.photo_bus_art = Image.open('buscar.png')
        self.photo_bus_art = self.photo_bus_art.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = tk.Button(self.frame_tercero, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=1, padx=5, pady=3)
        self.entry_detalle_articulo = tk.Entry(self.frame_tercero, textvariable=self.sv_detalle_articulo, width=143,
                                            justify="left")
        self.sv_detalle_articulo.trace("w", lambda *args: limitador(self.sv_detalle_articulo, 150))
        self.entry_detalle_articulo.grid(row=0, column=2, columnspan=6, padx=5, pady=2, sticky="w")

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = tk.Label(self.frame_tercero, text="Cliente garantia: ", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        # BOTON BUSCAR CLIENTE EN LISTBOX
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = tk.Button(self.frame_tercero, text="", image=self.photo_bus_cli, command=self.fbusclii,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=1, column=1, padx=5, pady=3)
        self.entry_nombre_cliente = tk.Entry(self.frame_tercero, textvariable=self.sv_nombre_cliente, width=52)
        self.entry_nombre_cliente.grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.lbl_texto_codigo_cliente = tk.Label(self.frame_tercero, textvariable=self.sv_codigo_cliente, width=10 )
        self.lbl_texto_codigo_cliente.grid(row=1, column=3, padx=5, pady=2, sticky="w")

    def cuadro_entrys_factobs(self):

        self.lbl_numero_factura = tk.Label(self.frame_cuarto, text="Factura Nº: ", justify="left")
        self.lbl_numero_factura.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_numero_factura = tk.Entry(self.frame_cuarto, textvariable=self.sv_numero_factura, width=15, justify="right")
        self.entry_numero_factura.bind("<FocusOut>", lambda e: self.varFuncion_new.corregir_al_salir(self.entry_numero_factura))
        self.entry_numero_factura.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.sv_numero_factura.trace("w", lambda *args: self.limitador(self.sv_numero_factura, 15))

        self.lbl_observaciones = tk.Label(self.frame_cuarto, text="Observaciones: ", justify="left")
        self.lbl_observaciones.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_observaciones = tk.Entry(self.frame_cuarto, textvariable=self.sv_observaciones, width=120, justify="left")
        self.entry_observaciones.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.sv_observaciones.trace("w", lambda *args: self.limitador(self.sv_observaciones, 150))

    def cuadro_entrys_texto_detalles(self):

        self.text_detalle = ScrolledText(self.frame_quinto)
        self.text_detalle.config(width=115, height=6, wrap="word", padx=4, pady=3)
        self.text_detalle.grid(row=1, column=1, padx=4, pady=5, sticky="nsew")

    def cargar_icono(self, path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)



"""
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
🔥 CÓMO USARLO
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
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
"""