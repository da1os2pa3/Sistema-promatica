import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from configuracion_ABM import DatosConfig
from funcion_new import ClaseFuncionNew
from funciones import *
from status_bar import StatusBar


class ClaseConfiguracion(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)

        self.varConfig = DatosConfig()
        self.varFuncion_new = ClaseFuncionNew(self.master)

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        master.geometry("880x510")
        master.resizable(0, 0)
        # ----------------------------------------------------------------------------------

        self.pantalla()
        self.create_widgets()
        self.llena_grilla("")

        item = self.grid_config.identify_row(0)
        self.grid_config.selection_set(item)
        self.grid_config.focus(item)

        self.habilitar_text("disabled")
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")

    def create_widgets(self):

        # --------------------------------------------------------------------------
        # TITULOS Y LOGO -----------------------------------------------------------
        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = tk.Frame(self.master)
        self.titulo_logo()
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=5)

        # VARIABLES GENERALES ------------------------------------------------------
        self.filtro_activo = ""
        self.alta_modif = 0

        # BOTONES ------------------------------------------------------------------
        self.cuadro_botones_crud = tk.LabelFrame(self.master)
        self.botones_crud()
        self.cuadro_botones_crud.pack(side="left", padx=15, pady=5, ipady=5, fill="y")

        # GRID ----------------------------------------------------------------------
        self.cuadro_grid = tk.Frame(self.master)
        self.armado_grid()
        self.cuadro_grid.pack(side="top", fill="both", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # STRINGVARS ----------------------------------------------------------------
        self.cuadro_sector_entry = tk.LabelFrame(self.master)

        self.sv_empresa      = tk.StringVar(self.cuadro_sector_entry)
        self.sv_direccion    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_localidad    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_provincia    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_postal       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_correo       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_telef1       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_telef2       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_titular      = tk.StringVar(self.cuadro_sector_entry)
        self.sv_contacto     = tk.StringVar(self.cuadro_sector_entry)
        self.sv_sit_fis      = tk.StringVar(self.cuadro_sector_entry)
        self.sv_cuit         = tk.StringVar(self.cuadro_sector_entry)
        self.sv_rentas       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_municipal    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_tasa_iva1    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_tasa_iva2    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_tasa_iva3    = tk.StringVar(self.cuadro_sector_entry)
        self.sv_tasa_impint  = tk.StringVar(self.cuadro_sector_entry)
        self.sv_tasa_reten   = tk.StringVar(self.cuadro_sector_entry)
        self.sv_tasa_percep  = tk.StringVar(self.cuadro_sector_entry)
        self.sv_dolar1       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_dolar2       = tk.StringVar(self.cuadro_sector_entry)
        self.sv_ultimo_saldo = tk.StringVar(value="0")

        # ENTRYS  -------------------------------------------------------------------
        self.entrada_entrys()

        self.cuadro_sector_entry.pack(expand=1, fill="both", pady=5, padx=5)

    # ---------------------------------------------------------------------------------
    # FUNCIONES GRILLA Y CAMPOS
    # ---------------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_config.get_children():
            self.grid_config.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varConfig.consultar_setting(self.filtro_activo)
        else:
            datos = self.varConfig.consultar_setting("")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_config.insert("", "end", tags=color, text=row[0], values=(row[1], row[2], row[3], row[4], row[5],
                                                                    row[6], row[7], row[8], row[9], row[10],
                                                                    row[11], row[12], row[13], row[14], row[15],
                                                                    row[16], row[17], row[18], row[19], row[20],
                                                                    row[21], row[22], row[26]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_config.get_children()
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
            self.grid_config.focus_set()
            self.grid_config.focus(posicion)
            self.grid_config.selection_set(posicion)
            self.grid_config.see(posicion)
        else:
            for item in children:
                texto = self.grid_config.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_config.update_idletasks()
                    self.grid_config.focus_set()
                    self.grid_config.selection_set(item)
                    self.grid_config.focus(item)
                    self.grid_config.see(item)
                    break

    def limpiar_text(self):

        self.entry_empresa.delete(0, "end")
        self.entry_direccion.delete(0, "end")
        self.entry_localidad.delete(0, "end")
        self.entry_provincia.delete(0, "end")
        self.entry_postal.delete(0, "end")
        self.entry_correo.delete(0, "end")
        self.entry_telef1.delete(0, "end")
        self.entry_telef2.delete(0, "end")
        self.entry_titular.delete(0, "end")
        self.entry_contacto.delete(0,"end")
        self.combo_sit_fis.delete(0, "end")
        self.entry_cuit.delete(0, "end")
        self.entry_rentas.delete(0, "end")
        self.entry_municipal.delete(0, "end")
        self.entry_tasa_iva1.delete(0, "end")
        self.entry_tasa_iva2.delete(0, "end")
        self.entry_tasa_iva3.delete(0, "end")
        self.entry_tasa_impint.delete(0, "end")
        self.entry_tasa_reten.delete(0, "end")
        self.entry_tasa_percep.delete(0, "end")
        self.entry_dolar1.delete(0, "end")
        self.entry_dolar2.delete(0, "end")
        self.entry_ultimo_saldo.delete(0, "end")

    def habilitar_text(self, estado):

        self.entry_empresa.configure(state=estado)
        self.entry_direccion.configure(state=estado)
        self.entry_localidad.configure(state=estado)
        self.entry_provincia.configure(state=estado)
        self.entry_postal.configure(state=estado)
        self.entry_correo.configure(state=estado)
        self.entry_telef1.configure(state=estado)
        self.entry_telef2.configure(state=estado)
        self.entry_titular.configure(state=estado)
        self.entry_contacto.configure(state=estado)
        self.combo_sit_fis.configure(state=estado)
        self.entry_cuit.configure(state=estado)
        self.entry_rentas.configure(state=estado)
        self.entry_municipal.configure(state=estado)
        self.entry_tasa_iva1.configure(state=estado)
        self.entry_tasa_iva2.configure(state=estado)
        self.entry_tasa_iva3.configure(state=estado)
        self.entry_tasa_impint.configure(state=estado)
        self.entry_tasa_reten.configure(state=estado)
        self.entry_tasa_percep.configure(state=estado)
        self.entry_dolar1.configure(state=estado)
        self.entry_dolar2.configure(state=estado)
        self.entry_ultimo_saldo.configure(state=estado)

    def habilitar_btn_oper(self, estado):

        self.btnModificar.configure(state=estado)

    def habilitar_btn_final(self, estado):

        self.btnGuardar.configure(state=estado)
        self.btnCancelar.configure(state=estado)

    # ----------------------------------------------------------------------------------------
    # CRUD

    def fmodificar(self):

        # --------------------------------------------------------------------------
        self.selected = self.grid_config.focus()
        self.clave = self.grid_config.item(self.selected, 'text')
        # --------------------------------------------------------------------------

        self.alta_modif = 2

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
        else:
            self.habilitar_text('normal')
            valores = self.grid_config.item(self.selected, 'values')

            self.limpiar_text()
            self.entry_empresa.insert(0, valores[0])
            self.entry_direccion.insert(0, valores[1])
            self.entry_localidad.insert(0, valores[2])
            self.entry_provincia.insert(0, valores[3])
            self.entry_postal.insert(0, valores[4])
            self.entry_correo.insert(0, valores[5])
            self.entry_telef1.insert(0, valores[6])
            self.entry_telef2.insert(0, valores[7])
            self.entry_titular.insert(0, valores[8])
            self.entry_contacto.insert(0, valores[9])
            self.combo_sit_fis.insert(0, valores[10])
            self.entry_cuit.insert(0, valores[11])
            self.entry_rentas.insert(0, valores[12])
            self.entry_municipal.insert(0, valores[13])
            self.entry_tasa_iva1.insert(0, valores[14])
            self.entry_tasa_iva2.insert(0, valores[15])
            self.entry_tasa_iva3.insert(0, valores[16])
            self.entry_tasa_impint.insert(0, valores[17])
            self.entry_tasa_reten.insert(0, valores[18])
            self.entry_tasa_percep.insert(0, valores[19])
            self.entry_dolar1.insert(0, valores[20])
            self.entry_dolar2.insert(0, valores[21])
            self.entry_ultimo_saldo.insert(0, valores[22])

            self.habilitar_btn_final("normal")
            self.habilitar_btn_oper("disabled")
            self.entry_empresa.focus()

    def fguardar(self):

        # VALIDACION QUE EXISTA APELLIDO
        if self.sv_empresa.get() == "" or self.sv_sit_fis == "" or self.sv_dolar1 == "" or \
           self.sv_tasa_iva1 == 0 or self.sv_tasa_iva2 == 0:

            messagebox.showwarning("Alerta", "Campos requeridos [*]", parent=self)
            self.entry_empresa.focus()
            return
        # VALIDAR CUIT
        if not self.validar_cuit(self.sv_cuit.get()):   # not True
            messagebox.showwarning("Alerta", "CUIT incorrecto", parent=self)
            self.entry_cuit.focus()
            return

        # -------------------------------------------------------------------------------------------
        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori ----------------
        self.selected = self.grid_config.focus()
        # # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_config.item(self.selected, 'text')
        # -------------------------------------------------------------------------------------------

        # fecha_aux = datetime.strptime(self.sv_fecha_ingreso.get(), '%d/%m/%Y')
        dic_configuracion = self.get_configuracion_dic()         # funcion que genera el diccionario

        #-----------------------------------------------------------------
        # GUARDADO DATOS Y EVALUACION DEL PROCEDIMIENTO
        #-----------------------------------------------------------------

        id_ref = ""
        try:
            if self.alta_modif == 1:
                pass
                # self.id_nuevo = self.varConfig.insertar_clientes(dic_configuracion)
                # id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                self.varConfig.modificar_setting(dic_configuracion)
                id_ref = self.clave
        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Insertar/Modificar", str(e))
            return
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

            # self.clave, self.sv_empresa.get(),
            # self.sv_direccion.get(), self.sv_localidad.get(), self.sv_provincia.get(),
            # self.sv_postal.get(), self.sv_correo.get(), self.sv_telef1.get(),
            # self.sv_telef2.get(), self.sv_titular.get(), self.sv_contacto.get(),
            # self.sv_sit_fis.get(), self.sv_cuit.get(), self.sv_rentas.get(),
            # self.sv_municipal.get(), self.sv_tasa_iva1.get(), self.sv_tasa_iva2.get(),
            # self.sv_tasa_iva3.get(), self.sv_tasa_impint.get(), self.sv_tasa_reten.get(),
            # self.sv_tasa_percep.get(), self.sv_dolar1.get(), self.sv_dolar2.get(),
            # self.sv_ultimo_saldo.get())

        self.llena_grilla(id_ref)
        self.limpiar_text()
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_oper("normal")
        self.habilitar_text("disabled")
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

    # ----------------------------------------------------------------------------------------
    # OTROS FUNCIONES

    def doble_click_grid(self, _event):
        self.fmodificar()

    @staticmethod
    def limitador(entry_text, caract):
        # Metodo que limita la cantidad de caracteres que ingresan en Entry -OBSERVACIONES - Tiempo de Ingeso
        if len(entry_text.get()) > 0:
            # donde esta el :5 limitas la cantidad d caracteres
            entry_text.set(entry_text.get()[:caract])

    @staticmethod
    def validar_cuit(cuit):
        # Metodo que valida el Numero de CUIT - Se ejecuta antes de guardar

        if len(cuit) == 0:
            return True

        base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

        cuit = cuit.replace("-", "")  # remuevo las barras

        if len(cuit) != 11:
            return False

        # calculo el digito verificador
        aux = 0
        for i in range(10):
            aux += int(cuit[i]) * base[i]

        aux = 11 - (aux - (int(aux / 11) * 11))

        if aux == 11:
            aux = 0
        if aux == 10:
            aux = 9

        return aux == int(cuit[10])

    def pantalla(self):
        """
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        """
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1040
        hventana = 460
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

    def titulo_logo(self):

        # Armo el logo y el titulo
        self.photo3 = Image.open('configuraciones.png')
        self.photo3 = self.photo3.resize((75, 75), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_configuracion = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_configuracion = tk.Label(self.frame_titulo_top, image=self.png_configuracion, bg="red", relief="ridge", bd=5)

        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=28, text="Configuracion",
                                bg="black", fg="gold", font=("Arial bold", 38, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_configuracion.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")

    def botones_crud(self):

        self.btnModificar=tk.Button(self.cuadro_botones_crud, text="Modificar", command=self.fmodificar, bg="blue", fg="white", width=10)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=5, ipadx=10)
        self.btnGuardar=tk.Button(self.cuadro_botones_crud, text="Guardar", command=self.fguardar, bg="green", fg="white", width=10)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.btnCancelar=tk.Button(self.cuadro_botones_crud, text="Cancelar", command=self.fcancelar, bg="black", fg="white", width=10)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=tk.Button(self.cuadro_botones_crud, text="Salir", image=self.photo3, command=self.fsalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

    def armado_grid(self):

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.cuadro_grid)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        # TREEVIEW
        self.grid_config = ttk.Treeview(self.cuadro_grid, height=2, columns=("col1", "col2", "col3", "col4", "col5",
                                                                          "col6", "col7", "col8", "col9", "col10",
                                                                          "col11", "col12","col13", "col14", "col15",
                                                                          "col16", "col17", "col18", "col19", "col20",
                                                                          "col21", "col22", "col23"))

        self.grid_config.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_config.column("#0", width=60, anchor="center")
        self.grid_config.column("col1", width=60, anchor="center")
        self.grid_config.column("col2", width=180, anchor="center")
        self.grid_config.column("col3", width=220, anchor="center")
        self.grid_config.column("col4", width=220, anchor="center")
        self.grid_config.column("col5", width=120, anchor="center")
        self.grid_config.column("col6", width=90, anchor="center")
        self.grid_config.column("col7", width=60, anchor="center")
        self.grid_config.column("col8", width=200, anchor="center")
        self.grid_config.column("col9", width=200, anchor="center")
        self.grid_config.column("col10", width=200, anchor="center")
        self.grid_config.column("col11", width=150, anchor="center")
        self.grid_config.column("col12", width=100, anchor="center")
        self.grid_config.column("col13", width=100, anchor="center")
        self.grid_config.column("col14", width=200, anchor="center")
        self.grid_config.column("col15", width=200, anchor="center")
        self.grid_config.column("col16", width=200, anchor="center")
        self.grid_config.column("col17", width=200, anchor="center")
        self.grid_config.column("col18", width=200, anchor="center")
        self.grid_config.column("col19", width=200, anchor="center")
        self.grid_config.column("col20", width=200, anchor="center")
        self.grid_config.column("col21", width=200, anchor="center")
        self.grid_config.column("col22", width=200, anchor="center")
        self.grid_config.column("col23", width=100, anchor="center")

        self.grid_config.heading("#0", text="Id", anchor="center")
        self.grid_config.heading("col1", text="Empresa", anchor="center")
        self.grid_config.heading("col2", text="Direccion", anchor="center")
        self.grid_config.heading("col3", text="Localidad", anchor="center")
        self.grid_config.heading("col4", text="Provincia", anchor="center")
        self.grid_config.heading("col5", text="Postal", anchor="center")
        self.grid_config.heading("col6", text="Correo Electronico", anchor="center")
        self.grid_config.heading("col7", text="Telefono 1", anchor="center")
        self.grid_config.heading("col8", text="Telefono 2", anchor="center")
        self.grid_config.heading("col9", text="Titular", anchor="center")
        self.grid_config.heading("col10", text="Contacto", anchor="center")
        self.grid_config.heading("col11", text="Sit.Fiscal", anchor="center")
        self.grid_config.heading("col12", text="CUIT", anchor="center")
        self.grid_config.heading("col13", text="Rentas", anchor="center")
        self.grid_config.heading("col14", text="Municipal", anchor="center")
        self.grid_config.heading("col15", text="Tasa IVA 1", anchor="center")
        self.grid_config.heading("col16", text="Tasa IVA 2", anchor="center")
        self.grid_config.heading("col17", text="Tasa IVA 3", anchor="center")
        self.grid_config.heading("col18", text="Tasa Imp.Int.", anchor="center")
        self.grid_config.heading("col19", text="Tasa Percepcion", anchor="center")
        self.grid_config.heading("col20", text="Tasa Retencion", anchor="center")
        self.grid_config.heading("col21", text="Dolar 1", anchor="center")
        self.grid_config.heading("col22", text="Dolar 2", anchor="center")
        self.grid_config.heading("col23", text="Ultimo saldo", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.cuadro_grid, orient="horizontal")
        self.grid_config.config(xscrollcommand=scroll_x.set)
        scroll_x.config(command=self.grid_config.xview)
        scroll_x.pack(side="bottom", fill="x")
        self.grid_config['selectmode'] = 'browse'

        self.grid_config.pack(side = "top", fill="both", expand=1, padx=5, pady=5)

    def entrada_entrys(self):

        # EMPRESA
        self.lbl_empresa = tk.Label(self.cuadro_sector_entry, text="[*] Empresa: ")
        self.lbl_empresa.grid(row=0, column=0, padx=10, pady=3, sticky="w")
        self.entry_empresa = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_empresa, justify="left", width=30)
        self.sv_empresa.trace("w", lambda *args: self.limitador(self.sv_empresa, 30))
        self.entry_empresa.grid(row=0, column=1, padx=10, pady=3, sticky="w")
        # DIRECCION
        self.lbl_direccion = tk.Label(self.cuadro_sector_entry, text="Direccion: ")
        self.lbl_direccion.grid(row=1, column=0, padx=10, pady=3, sticky="w")
        self.entry_direccion = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_direccion, justify="left", width=30)
        self.sv_direccion.trace("w", lambda *args: self.limitador(self.sv_direccion, 30))
        self.entry_direccion.grid(row=1, column=1, padx=10, pady=3, sticky="w")
        # LOCALIDAD
        self.lbl_localidad = tk.Label(self.cuadro_sector_entry, text="Localidad: ")
        self.lbl_localidad.grid(row=2, column=0, padx=10, pady=3, sticky="w")
        self.entry_localidad = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_localidad, justify="left", width=20)
        self.sv_localidad.trace("w", lambda *args: self.limitador(self.sv_localidad, 20))
        self.entry_localidad.grid(row=2, column=1, padx=10, pady=3, sticky="w")
        # PROVINCIA
        self.lbl_provincia = tk.Label(self.cuadro_sector_entry, text="Provincia: ")
        self.lbl_provincia.grid(row=3, column=0, padx=10, pady=3, sticky="w")
        self.entry_provincia = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_provincia, justify="left", width=15)
        self.sv_provincia.trace("w", lambda *args: self.limitador(self.sv_provincia, 15))
        self.entry_provincia.grid(row=3, column=1, padx=10, pady=3, sticky="w")
        # POSTAL
        self.lbl_postal = tk.Label(self.cuadro_sector_entry, text="Cod.Postal: ")
        self.lbl_postal.grid(row=4, column=0, padx=10, pady=3, sticky="w")
        self.entry_postal = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_postal, justify="left", width=5)
        self.sv_postal.trace("w", lambda *args: self.limitador(self.sv_postal, 5))
        self.entry_postal.grid(row=4, column=1, padx=10, pady=3, sticky="w")
        # CORREO ELECTRONICO
        self.lbl_correo = tk.Label(self.cuadro_sector_entry, text="Correo electronico: ")
        self.lbl_correo.grid(row=5, column=0, padx=10, pady=3, sticky="w")
        self.entry_correo = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_correo, justify="left", width=35)
        self.sv_correo.trace("w", lambda *args: self.limitador(self.sv_correo, 30))
        self.entry_correo.grid(row=5, column=1, padx=10, pady=3, sticky="w")
        # TELEFONO 1
        self.lbl_telef1 = tk.Label(self.cuadro_sector_entry, text="Telefono 1: ")
        self.lbl_telef1.grid(row=6, column=0, padx=10, pady=3, sticky="w")
        self.entry_telef1 = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_telef1, justify="left", width=15)
        self.sv_telef1.trace("w", lambda *args: self.limitador(self.sv_telef1, 15))
        self.entry_telef1.grid(row=6, column=1, padx=10, pady=3, sticky="w")
        # TELEFONO 2
        self.lbl_telef2 = tk.Label(self.cuadro_sector_entry, text="Telefono 2: ")
        self.lbl_telef2.grid(row=7, column=0, padx=10, pady=3, sticky="w")
        self.entry_telef2 = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_telef2, justify="left", width=15)
        self.sv_telef2.trace("w", lambda *args: self.limitador(self.sv_telef2, 15))
        self.entry_telef2.grid(row=7, column=1, padx=10, pady=3, sticky="w")
        # TITULAR
        self.lbl_titular = tk.Label(self.cuadro_sector_entry, text="Titular: ")
        self.lbl_titular.grid(row=0, column=2, padx=10, pady=3, sticky="w")
        self.entry_titular = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_titular, justify="left", width=30)
        self.sv_titular.trace("w", lambda *args: self.limitador(self.sv_titular, 30))
        self.entry_titular.grid(row=0, column=3, padx=10, pady=3, sticky="w")
        # CONTACTO
        self.lbl_contacto = tk.Label(self.cuadro_sector_entry, text="Contacto: ")
        self.lbl_contacto.grid(row=1, column=2, padx=10, pady=3, sticky="w")
        self.entry_contacto = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_titular, justify="left", width=30)
        self.sv_contacto.trace("w", lambda *args: self.limitador(self.sv_contacto, 30))
        self.entry_contacto.grid(row=1, column=3, padx=10, pady=3, sticky="w")
        # SITUACION FISCAL - COMBOBOX
        self.lbl_sit_fis = tk.Label(self.cuadro_sector_entry, text="[*] Sit. Fiscal: ")
        self.lbl_sit_fis.grid(row=2, column=2, padx=10, pady=3, sticky="w")
        self.combo_sit_fis = ttk.Combobox(self.cuadro_sector_entry, textvariable=self.sv_sit_fis, state='readonly',
                                          width=28)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fis["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                        "RM - Responsable Monotributo", "EX - Exento",
                                        "RN - Responsable no inscripto"]
        self.combo_sit_fis.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        # CUIT
        self.lbl_cuit = tk.Label(self.cuadro_sector_entry, text="CUIT [sin -]: ")
        self.lbl_cuit.grid(row=3, column=2, padx=10, pady=3, sticky="w")
        self.entry_cuit = tk.Entry(self.cuadro_sector_entry, textvariable= self.sv_cuit, justify="left", width=11)
        self.sv_cuit.trace("w", lambda *args: self.limitador(self.sv_cuit, 11))
        self.entry_cuit.grid(row=3, column=3, padx=10, pady=3, sticky="w")
        # RENTAS
        self.lbl_rentas = tk.Label(self.cuadro_sector_entry, text="Rentas: ")
        self.lbl_rentas.grid(row=4, column=2, padx=10, pady=3, sticky="w")
        self.entry_rentas = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_rentas, justify="left", width=20)
        self.sv_rentas.trace("w", lambda *args: self.limitador(self.sv_rentas, 20))
        self.entry_rentas.grid(row=4, column=3, padx=10, pady=3, sticky="w")
        # MUNICIPAL
        self.lbl_municipal = tk.Label(self.cuadro_sector_entry, text="Municipal: ")
        self.lbl_municipal.grid(row=5, column=2, padx=10, pady=3, sticky="w")
        self.entry_municipal = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_municipal, justify="left", width=20)
        self.sv_municipal.trace("w", lambda *args: self.limitador(self.sv_municipal, 20))
        self.entry_municipal.grid(row=5, column=3, padx=10, pady=3, sticky="w")
        # TASA IVA1 - COMBOBOX
        self.lbl_tasa_iva1 = tk.Label(self.cuadro_sector_entry, text="[*] Tasa IVA 1: ")
        self.lbl_tasa_iva1.grid(row=6, column=2, padx=10, pady=3, sticky="w")
        self.entry_tasa_iva1 = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_tasa_iva1, justify="right", width=5)
        self.sv_tasa_iva1.trace("w", lambda *args: self.limitador(self.sv_tasa_iva1, 5))
        self.entry_tasa_iva1.grid(row=6, column=3, padx=10, pady=3, sticky="w")
        # TASA IVA2 - COMBOBOX
        self.lbl_tasa_iva2 = tk.Label(self.cuadro_sector_entry, text="[*] Tasa IVA 2: ")
        self.lbl_tasa_iva2.grid(row=7, column=2, padx=10, pady=3, sticky="w")
        self.entry_tasa_iva2=tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_tasa_iva2, justify="right", width=5)
        self.sv_tasa_iva2.trace("w", lambda *args: self.limitador(self.sv_tasa_iva2, 5))
        self.entry_tasa_iva2.grid(row=7, column=3, padx=10, pady=3, sticky="w")
        # TASA IVA3 - COMBOBOX
        self.lbl_tasa_iva3 = tk.Label(self.cuadro_sector_entry, text="Tasa IVA 3: ")
        self.lbl_tasa_iva3.grid(row=0, column=4, padx=10, pady=3, sticky="w")
        self.entry_tasa_iva3 = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_tasa_iva3, justify="right", width=5)
        self.sv_tasa_iva3.trace("w", lambda *args: self.limitador(self.sv_tasa_iva3, 5))
        self.entry_tasa_iva3.grid(row=0, column=5, padx=10, pady=3, sticky="w")
        # TASA IMPINT
        self.lbl_tasa_impint = tk.Label(self.cuadro_sector_entry, text="Tasa Imp.Interno: ")
        self.lbl_tasa_impint.grid(row=1, column=4, padx=10, pady=3, sticky="w")
        self.entry_tasa_impint = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_tasa_impint, justify="right", width=5)
        self.sv_tasa_impint.trace("w", lambda *args: self.limitador(self.sv_tasa_impint, 5))
        self.entry_tasa_impint.grid(row=1, column=5, padx=10, pady=3, sticky="w")
        # TASA RETENCIONES
        self.lbl_tasa_reten = tk.Label(self.cuadro_sector_entry, text="Tasa Retenciones: ")
        self.lbl_tasa_reten.grid(row=2, column=4, padx=10, pady=3, sticky="w")
        self.entry_tasa_reten = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_tasa_reten, justify="right", width=5)
        self.sv_tasa_reten.trace("w", lambda *args: self.limitador(self.sv_tasa_reten, 5))
        self.entry_tasa_reten.grid(row=2, column=5, padx=10, pady=3, sticky="w")
        # TASA PERCEPCIONES
        self.lbl_tasa_percep = tk.Label(self.cuadro_sector_entry, text="Tasa Percepciones: ")
        self.lbl_tasa_percep.grid(row=3, column=4, padx=10, pady=3, sticky="w")
        self.entry_tasa_percep = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_tasa_percep, justify="right", width=5)
        self.sv_tasa_percep.trace("w", lambda *args: self.limitador(self.sv_tasa_percep, 5))
        self.entry_tasa_percep.grid(row=3, column=5, padx=10, pady=3, sticky="w")
        # DOLAR 1
        self.lbl_dolar1 = tk.Label(self.cuadro_sector_entry, text="[*] Dolar 1: ")
        self.lbl_dolar1.grid(row=4, column=4, padx=10, pady=3, sticky="w")
        self.entry_dolar1 = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_dolar1, justify="right", width=10)
        self.sv_dolar1.trace("w", lambda *args: self.limitador(self.sv_dolar1, 15))
        self.entry_dolar1.grid(row=4, column=5, padx=10, pady=3, sticky="w")
        # DOLAR 2
        self.lbl_dolar2 = tk.Label(self.cuadro_sector_entry, text="Dolar 2: ")
        self.lbl_dolar2.grid(row=5, column=4, padx=10, pady=3, sticky="w")
        self.entry_dolar2 = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_dolar2, justify="right", width=10)
        self.sv_dolar2.trace("w", lambda *args: self.limitador(self.sv_dolar2, 15))
        self.entry_dolar2.grid(row=5, column=5, padx=10, pady=3, sticky="w")
        # ULTIMO SALDO
        self.lbl_ultsal = tk.Label(self.cuadro_sector_entry, text="Ultimo saldo: ")
        self.lbl_ultsal.grid(row=6, column=4, padx=10, pady=3, sticky="w")
        self.entry_ultimo_saldo = tk.Entry(self.cuadro_sector_entry, textvariable=self.sv_ultimo_saldo, justify="right",
                                      width=10)
        self.sv_ultimo_saldo.trace("w", lambda *args: self.limitador(self.sv_ultimo_saldo, 15))
        self.entry_ultimo_saldo.grid(row=6, column=5, padx=10, pady=3, sticky="w")

    def get_configuracion_dic(self):

        return {
            "Id":             self.clave,
            "i_empresa":      self.sv_empresa.get(),
            "i_direccion":    self.sv_direccion.get(),
            "i_localidad":    self.sv_localidad.get(),
            "i_provincia":    self.sv_provincia.get(),
            "i_postal":       self.sv_postal.get(),
            "i_correo":       self.sv_correo.get(),
            "i_telef1":       self.sv_telef1.get(),
            "i_telef2":       self.sv_telef2.get(),
            "i_titular":      self.sv_titular.get(),
            "i_contacto":     self.sv_contacto.get(),
            "i_sit_fis":      self.sv_sit_fis.get(),
            "i_cuit":         self.sv_cuit.get(),
            "i_rentas":       self.sv_rentas.get(),
            "i_municip":      self.sv_municipal.get(),
            "i_iva1":         self.sv_tasa_iva1.get(),
            "i_iva2":         self.sv_tasa_iva2.get(),
            "i_iva3":         self.sv_tasa_iva3.get(),
            "i_impint":       self.sv_tasa_impint.get(),
            "i_reten":        self.sv_tasa_reten.get(),
            "i_percep":       self.sv_tasa_percep.get(),
            "i_dolar1":       self.sv_dolar1.get(),
            "i_dolar2":       self.sv_dolar2.get(),
            "i_ultimo_saldo": self.sv_ultimo_saldo.get()
        }
