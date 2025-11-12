from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
# ------------------------------------
from configuracion_ABM import *
# ------------------------------------
from datetime import date, datetime
from PIL import Image, ImageTk

class Ventconfig(Frame):

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)

        self.varConfig = datosConfig()

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        master.geometry("880x510")
        master.resizable(0, 0)

        """
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        """

        wtotal = master.winfo_screenwidth()
        htotal = master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1040
        hventana = 440
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.llena_grilla()

        item = self.grid_config.identify_row(0)
        self.grid_config.selection_set(item)
        self.grid_config.focus(item)

        self.habilitar_text("disabled")
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")
        self.var_Id = -1

    def create_widgets(self):

        # -------------------------------------------------------------------------
        # TITULOS

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('configuraciones.png')
        self.photo3 = self.photo3.resize((75, 75), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_configuracion = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_configuracion = Label(self.frame_titulo_top, image=self.png_configuracion, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=28, text="Configuracion",
                                bg="black", fg="gold", font=("Arial bold", 38, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_configuracion.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=5)
        # --------------------------------------------------------------------------

        # VARIABLES GENERALES
        self.filtro_activo = "informa"
        self.var_Id = -1
        self.alta_modif = 0
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # BOTONES

        barra_botones = LabelFrame(self.master)

        # Instalacion botones
        # self.btnNuevo=Button(barra_botones, text="Nuevo", command=self.fNuevo, bg="blue", fg="white", width=10)
        # self.btnNuevo.grid(row=0, column=0, padx=5, pady=5, ipadx=10)
        self.btnModificar=Button(barra_botones, text="Modificar", command=self.fModificar, bg="blue", fg="white", width=10)
        self.btnModificar.grid(row=1, column=0, padx=5, pady=5, ipadx=10)
        # self.btnEliminar=Button(barra_botones, text="Eliminar", command=self.fEliminar, bg="blue", fg="white", width=10)
        # self.btnEliminar.grid(row=2, column=0, padx=5, pady=5, ipadx=10)
        self.btnGuardar=Button(barra_botones, text="Guardar", command=self.fGuardar, bg="green", fg="white", width=10)
        self.btnGuardar.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.btnCancelar=Button(barra_botones, text="Cancelar", command=self.fCancelar, bg="black", fg="white", width=10)
        self.btnCancelar.grid(row=4, column=0, padx=5, pady=5, columnspan=2)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(barra_botones, text="Salir", image=self.photo3, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")

        # PACK - frame de botones
        barra_botones.pack(side=LEFT, padx=15, pady=5, ipady=5, fill=Y)
        # ----------------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------------
        # TREEVIEW
        self.frame_tv = Frame(self.master)

        # STYLE TREEVIEW - un chiche para formas y colores
        style = ttk.Style(self.frame_tv)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        # TREEVIEW
        self.grid_config = ttk.Treeview(self.frame_tv, height=2, columns=("col1", "col2", "col3", "col4", "col5",
                                                                          "col6", "col7", "col8", "col9", "col10",
                                                                          "col11", "col12","col13", "col14", "col15",
                                                                          "col16", "col17", "col18", "col19", "col20",
                                                                          "col21", "col22", "col23"))

        self.grid_config.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_config.column("#0", width=60, anchor=CENTER)
        self.grid_config.column("col1", width=60, anchor=CENTER)
        self.grid_config.column("col2", width=180, anchor=CENTER)
        self.grid_config.column("col3", width=220, anchor=CENTER)
        self.grid_config.column("col4", width=220, anchor=CENTER)
        self.grid_config.column("col5", width=120, anchor=CENTER)
        self.grid_config.column("col6", width=90, anchor=CENTER)
        self.grid_config.column("col7", width=60, anchor=CENTER)
        self.grid_config.column("col8", width=200, anchor=CENTER)
        self.grid_config.column("col9", width=200, anchor=CENTER)
        self.grid_config.column("col10", width=200, anchor=CENTER)
        self.grid_config.column("col11", width=150, anchor=CENTER)
        self.grid_config.column("col12", width=100, anchor=CENTER)
        self.grid_config.column("col13", width=100, anchor=CENTER)
        self.grid_config.column("col14", width=200, anchor=CENTER)
        self.grid_config.column("col15", width=200, anchor=CENTER)
        self.grid_config.column("col16", width=200, anchor=CENTER)
        self.grid_config.column("col17", width=200, anchor=CENTER)
        self.grid_config.column("col18", width=200, anchor=CENTER)
        self.grid_config.column("col19", width=200, anchor=CENTER)
        self.grid_config.column("col20", width=200, anchor=CENTER)
        self.grid_config.column("col21", width=200, anchor=CENTER)
        self.grid_config.column("col22", width=200, anchor=CENTER)
        self.grid_config.column("col23", width=100, anchor=CENTER)

        self.grid_config.heading("#0", text="Id", anchor=CENTER)
        self.grid_config.heading("col1", text="Empresa", anchor=CENTER)
        self.grid_config.heading("col2", text="Direccion", anchor=CENTER)
        self.grid_config.heading("col3", text="Localidad", anchor=CENTER)
        self.grid_config.heading("col4", text="Provincia", anchor=CENTER)
        self.grid_config.heading("col5", text="Postal", anchor=CENTER)
        self.grid_config.heading("col6", text="Correo Electronico", anchor=CENTER)
        self.grid_config.heading("col7", text="Telefono 1", anchor=CENTER)
        self.grid_config.heading("col8", text="Telefono 2", anchor=CENTER)
        self.grid_config.heading("col9", text="Titular", anchor=CENTER)
        self.grid_config.heading("col10", text="Contacto", anchor=CENTER)
        self.grid_config.heading("col11", text="Sit.Fiscal", anchor=CENTER)
        self.grid_config.heading("col12", text="CUIT", anchor=CENTER)
        self.grid_config.heading("col13", text="Rentas", anchor=CENTER)
        self.grid_config.heading("col14", text="Municipal", anchor=CENTER)
        self.grid_config.heading("col15", text="Tasa IVA 1", anchor=CENTER)
        self.grid_config.heading("col16", text="Tasa IVA 2", anchor=CENTER)
        self.grid_config.heading("col17", text="Tasa IVA 3", anchor=CENTER)
        self.grid_config.heading("col18", text="Tasa Imp.Int.", anchor=CENTER)
        self.grid_config.heading("col19", text="Tasa Percepcion", anchor=CENTER)
        self.grid_config.heading("col20", text="Tasa Retencion", anchor=CENTER)
        self.grid_config.heading("col21", text="Dolar 1", anchor=CENTER)
        self.grid_config.heading("col22", text="Dolar 2", anchor=CENTER)
        self.grid_config.heading("col23", text="Ultimo saldo", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tv, orient=HORIZONTAL)
        self.grid_config.config(xscrollcommand=scroll_x.set)
        scroll_x.config(command=self.grid_config.xview)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_config['selectmode'] = 'browse'

        # PACK - de el treeview y el FRAME tv
        self. grid_config.pack(side = TOP, fill=BOTH, expand=1, padx=5, pady=5)
        self.frame_tv.pack(side=TOP, fill=BOTH, padx=5, pady=5)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS

        self.sector_entry = LabelFrame(self.master)

        # Stringsvar
        self.strvar_empresa = tk.StringVar(self.sector_entry)
        self.strvar_direccion = tk.StringVar(self.sector_entry)
        self.strvar_localidad = tk.StringVar(self.sector_entry)
        self.strvar_provincia = tk.StringVar(self.sector_entry)
        self.strvar_postal = tk.StringVar(self.sector_entry)
        self.strvar_correo = tk.StringVar(self.sector_entry)
        self.strvar_telef1 = tk.StringVar(self.sector_entry)
        self.strvar_telef2 = tk.StringVar(self.sector_entry)
        self.strvar_titular = tk.StringVar(self.sector_entry)
        self.strvar_contacto = tk.StringVar(self.sector_entry)
        self.strvar_sit_fis = tk.StringVar(self.sector_entry)
        self.strvar_cuit = tk.StringVar(self.sector_entry)
        self.strvar_rentas = tk.StringVar(self.sector_entry)
        self.strvar_municipal = tk.StringVar(self.sector_entry)
        self.strvar_tasa_iva1 = tk.StringVar(self.sector_entry)
        self.strvar_tasa_iva2 = tk.StringVar(self.sector_entry)
        self.strvar_tasa_iva3 = tk.StringVar(self.sector_entry)
        self.strvar_tasa_impint = tk.StringVar(self.sector_entry)
        self.strvar_tasa_reten = tk.StringVar(self.sector_entry)
        self.strvar_tasa_percep = tk.StringVar(self.sector_entry)
        self.strvar_dolar1 = tk.StringVar(self.sector_entry)
        self.strvar_dolar2 = tk.StringVar(self.sector_entry)
        self.strvar_ultimo_saldo = tk.StringVar(value="0")

        # ----------------------------------------------------------------------------------------
        # ENTRYS

        # EMPRESA
        self.lbl_empresa = Label(self.sector_entry, text="[*] Empresa: ")
        self.lbl_empresa.grid(row=0, column=0, padx=10, pady=3, sticky=W)
        self.entry_empresa = Entry(self.sector_entry, textvariable=self.strvar_empresa, justify="left", width=30)
        self.strvar_empresa.trace("w", lambda *args: self.limitador(self.strvar_empresa, 30))
        self.entry_empresa.grid(row=0, column=1, padx=10, pady=3, sticky=W)
        # DIRECCION
        self.lbl_direccion = Label(self.sector_entry, text="Direccion: ")
        self.lbl_direccion.grid(row=1, column=0, padx=10, pady=3, sticky=W)
        self.entry_direccion=Entry(self.sector_entry, textvariable=self.strvar_direccion, justify="left", width=30)
        self.strvar_direccion.trace("w", lambda *args: self.limitador(self.strvar_direccion, 30))
        self.entry_direccion.grid(row=1, column=1, padx=10, pady=3, sticky=W)
        # LOCALIDAD
        self.lbl_localidad = Label(self.sector_entry, text="Localidad: ")
        self.lbl_localidad.grid(row=2, column=0, padx=10, pady=3, sticky=W)
        self.entry_localidad = Entry(self.sector_entry, textvariable=self.strvar_localidad, justify="left", width=20)
        self.strvar_localidad.trace("w", lambda *args: self.limitador(self.strvar_localidad, 20))
        self.entry_localidad.grid(row=2, column=1, padx=10, pady=3, sticky=W)
        # PROVINCIA
        self.lbl_provincia = Label(self.sector_entry, text="Provincia: ")
        self.lbl_provincia.grid(row=3, column=0, padx=10, pady=3, sticky=W)
        self.entry_provincia=Entry(self.sector_entry, textvariable=self.strvar_provincia, justify="left", width=15)
        self.strvar_provincia.trace("w", lambda *args: self.limitador(self.strvar_provincia, 15))
        self.entry_provincia.grid(row=3, column=1, padx=10, pady=3, sticky=W)
        # POSTAL
        self.lbl_postal = Label(self.sector_entry, text="Cod.Postal: ")
        self.lbl_postal.grid(row=4, column=0, padx=10, pady=3, sticky=W)
        self.entry_postal=Entry(self.sector_entry, textvariable=self.strvar_postal, justify="left", width=5)
        self.strvar_postal.trace("w", lambda *args: self.limitador(self.strvar_postal, 5))
        self.entry_postal.grid(row=4, column=1, padx=10, pady=3, sticky=W)
        # CORREO ELECTRONICO
        self.lbl_correo = Label(self.sector_entry, text="Correo electronico: ")
        self.lbl_correo.grid(row=5, column=0, padx=10, pady=3, sticky=W)
        self.entry_correo=Entry(self.sector_entry, textvariable=self.strvar_correo, justify="left", width=35)
        self.strvar_correo.trace("w", lambda *args: self.limitador(self.strvar_correo, 30))
        self.entry_correo.grid(row=5, column=1, padx=10, pady=3, sticky=W)
        # TELEFONO 1
        self.lbl_telef1 = Label(self.sector_entry, text="Telefono 1: ")
        self.lbl_telef1.grid(row=6, column=0, padx=10, pady=3, sticky=W)
        self.entry_telef1=Entry(self.sector_entry, textvariable=self.strvar_telef1, justify="left", width=15)
        self.strvar_telef1.trace("w", lambda *args: self.limitador(self.strvar_telef1, 15))
        self.entry_telef1.grid(row=6, column=1, padx=10, pady=3, sticky=W)
        # TELEFONO 2
        self.lbl_telef2 = Label(self.sector_entry, text="Telefono 2: ")
        self.lbl_telef2.grid(row=7, column=0, padx=10, pady=3, sticky=W)
        self.entry_telef2=Entry(self.sector_entry, textvariable=self.strvar_telef2, justify="left", width=15)
        self.strvar_telef2.trace("w", lambda *args: self.limitador(self.strvar_telef2, 15))
        self.entry_telef2.grid(row=7, column=1, padx=10, pady=3, sticky=W)
        # TITULAR
        self.lbl_titular = Label(self.sector_entry, text="Titular: ")
        self.lbl_titular.grid(row=0, column=2, padx=10, pady=3, sticky=W)
        self.entry_titular=Entry(self.sector_entry, textvariable=self.strvar_titular, justify="left", width=30)
        self.strvar_titular.trace("w", lambda *args: self.limitador(self.strvar_titular, 30))
        self.entry_titular.grid(row=0, column=3, padx=10, pady=3, sticky=W)
        # CONTACTO
        self.lbl_contacto = Label(self.sector_entry, text="Contacto: ")
        self.lbl_contacto.grid(row=1, column=2, padx=10, pady=3, sticky=W)
        self.entry_contacto=Entry(self.sector_entry, textvariable=self.strvar_titular, justify="left", width=30)
        self.strvar_contacto.trace("w", lambda *args: self.limitador(self.strvar_contacto, 30))
        self.entry_contacto.grid(row=1, column=3, padx=10, pady=3, sticky=W)
        # SITUACION FISCAL - COMBOBOX
        self.lbl_sit_fis = Label(self.sector_entry, text="[*] Sit. Fiscal: ")
        self.lbl_sit_fis.grid(row=2, column=2, padx=10, pady=3, sticky=W)
        self.combo_sit_fis = ttk.Combobox(self.sector_entry, textvariable=self.strvar_sit_fis, state='readonly',
                                          width=28)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fis["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                        "RM - Responsable Monotributo", "EX - Exento",
                                        "RN - Responsable no inscripto"]
        self.combo_sit_fis.grid(row=2, column=3, padx=10, pady=5, sticky=W)
        # CUIT
        self.lbl_cuit = Label(self.sector_entry, text="CUIT [sin -]: ")
        self.lbl_cuit.grid(row=3, column=2, padx=10, pady=3, sticky=W)
        # self.entry_cuit=Entry(self.sector_entry, validate="key",
        #                       validatecommand=(self.sector_entry.register(self.val_entcuit), "%S", "%P"),
        #                       textvariable=self.strvar_cuit, justify="left", width=40)
        self.entry_cuit=Entry(self.sector_entry, textvariable= self.strvar_cuit, justify="left", width=11)
#        self.entry_cuit.bind('<KeyRelease>', lambda e: self.verifcuit(self.strvar_cuit.get()))
        self.strvar_cuit.trace("w", lambda *args: self.limitador(self.strvar_cuit, 11))
        self.entry_cuit.grid(row=3, column=3, padx=10, pady=3, sticky=W)
        # RENTAS
        self.lbl_rentas = Label(self.sector_entry, text="Rentas: ")
        self.lbl_rentas.grid(row=4, column=2, padx=10, pady=3, sticky=W)
        self.entry_rentas=Entry(self.sector_entry, textvariable=self.strvar_rentas, justify="left", width=20)
        self.strvar_rentas.trace("w", lambda *args: self.limitador(self.strvar_rentas, 20))
        self.entry_rentas.grid(row=4, column=3, padx=10, pady=3, sticky=W)
        # MUNICIPAL
        self.lbl_municipal = Label(self.sector_entry, text="Municipal: ")
        self.lbl_municipal.grid(row=5, column=2, padx=10, pady=3, sticky=W)
        self.entry_municipal = Entry(self.sector_entry, textvariable=self.strvar_municipal, justify="left", width=20)
        self.strvar_municipal.trace("w", lambda *args: self.limitador(self.strvar_municipal, 20))
        self.entry_municipal.grid(row=5, column=3, padx=10, pady=3, sticky=W)
        # TASA IVA1 - COMBOBOX
        self.lbl_tasa_iva1 = Label(self.sector_entry, text="[*] Tasa IVA 1: ")
        self.lbl_tasa_iva1.grid(row=6, column=2, padx=10, pady=3, sticky=W)
        self.entry_tasa_iva1=Entry(self.sector_entry, textvariable=self.strvar_tasa_iva1, justify="right", width=5)
        self.strvar_tasa_iva1.trace("w", lambda *args: self.limitador(self.strvar_tasa_iva1, 5))
        self.entry_tasa_iva1.grid(row=6, column=3, padx=10, pady=3, sticky=W)
        # TASA IVA2 - COMBOBOX
        self.lbl_tasa_iva2 = Label(self.sector_entry, text="[*] Tasa IVA 2: ")
        self.lbl_tasa_iva2.grid(row=7, column=2, padx=10, pady=3, sticky=W)
        self.entry_tasa_iva2=Entry(self.sector_entry, textvariable=self.strvar_tasa_iva2, justify="right", width=5)
        self.strvar_tasa_iva2.trace("w", lambda *args: self.limitador(self.strvar_tasa_iva2, 5))
        self.entry_tasa_iva2.grid(row=7, column=3, padx=10, pady=3, sticky=W)
        # TASA IVA3 - COMBOBOX
        self.lbl_tasa_iva3 = Label(self.sector_entry, text="Tasa IVA 3: ")
        self.lbl_tasa_iva3.grid(row=0, column=4, padx=10, pady=3, sticky=W)
        self.entry_tasa_iva3=Entry(self.sector_entry, textvariable=self.strvar_tasa_iva3, justify="right", width=5)
        self.strvar_tasa_iva3.trace("w", lambda *args: self.limitador(self.strvar_tasa_iva3, 5))
        self.entry_tasa_iva3.grid(row=0, column=5, padx=10, pady=3, sticky=W)
        # TASA IMPINT
        self.lbl_tasa_impint = Label(self.sector_entry, text="Tasa Imp.Interno: ")
        self.lbl_tasa_impint.grid(row=1, column=4, padx=10, pady=3, sticky=W)
        self.entry_tasa_impint=Entry(self.sector_entry, textvariable=self.strvar_tasa_impint, justify="right", width=5)
        self.strvar_tasa_impint.trace("w", lambda *args: self.limitador(self.strvar_tasa_impint, 5))
        self.entry_tasa_impint.grid(row=1, column=5, padx=10, pady=3, sticky=W)
        # TASA RETENCIONES
        self.lbl_tasa_reten = Label(self.sector_entry, text="Tasa Retenciones: ")
        self.lbl_tasa_reten.grid(row=2, column=4, padx=10, pady=3, sticky=W)
        self.entry_tasa_reten=Entry(self.sector_entry, textvariable=self.strvar_tasa_reten, justify="right", width=5)
        self.strvar_tasa_reten.trace("w", lambda *args: self.limitador(self.strvar_tasa_reten, 5))
        self.entry_tasa_reten.grid(row=2, column=5, padx=10, pady=3, sticky=W)
        # TASA PERCEPCIONES
        self.lbl_tasa_percep = Label(self.sector_entry, text="Tasa Percepciones: ")
        self.lbl_tasa_percep.grid(row=3, column=4, padx=10, pady=3, sticky=W)
        self.entry_tasa_percep=Entry(self.sector_entry, textvariable=self.strvar_tasa_percep, justify="right", width=5)
        self.strvar_tasa_percep.trace("w", lambda *args: self.limitador(self.strvar_tasa_percep, 5))
        self.entry_tasa_percep.grid(row=3, column=5, padx=10, pady=3, sticky=W)
        # DOLAR 1
        self.lbl_dolar1 = Label(self.sector_entry, text="[*] Dolar 1: ")
        self.lbl_dolar1.grid(row=4, column=4, padx=10, pady=3, sticky=W)
        self.entry_dolar1=Entry(self.sector_entry, textvariable=self.strvar_dolar1, justify="right", width=10)
        self.strvar_dolar1.trace("w", lambda *args: self.limitador(self.strvar_dolar1, 15))
        self.entry_dolar1.grid(row=4, column=5, padx=10, pady=3, sticky=W)
        # DOLAR 2
        self.lbl_dolar2 = Label(self.sector_entry, text="Dolar 2: ")
        self.lbl_dolar2.grid(row=5, column=4, padx=10, pady=3, sticky=W)
        self.entry_dolar2=Entry(self.sector_entry, textvariable=self.strvar_dolar2, justify="right", width=10)
        self.strvar_dolar2.trace("w", lambda *args: self.limitador(self.strvar_dolar2, 15))
        self.entry_dolar2.grid(row=5, column=5, padx=10, pady=3, sticky=W)
        # ULTIMO SALDO
        self.lbl_ultsal = Label(self.sector_entry, text="Ultimo saldo: ")
        self.lbl_ultsal.grid(row=6, column=4, padx=10, pady=3, sticky=W)
        self.entry_ultimo_saldo=Entry(self.sector_entry, textvariable=self.strvar_ultimo_saldo, justify="right",
                                      width=10)
        self.strvar_ultimo_saldo.trace("w", lambda *args: self.limitador(self.strvar_ultimo_saldo, 15))
        self.entry_ultimo_saldo.grid(row=6, column=5, padx=10, pady=3, sticky=W)

        # PACK del frame "sector_entry"
        self.sector_entry.pack(expand=1, fill=BOTH, pady=5, padx=5)

    # ----------------------------------------------------------------------------------------
    # FUNCIONES GRILLA Y CAMPOS

    def llena_grilla(self):

        if len(self.filtro_activo) > 0:
            datos = self.varConfig.consultar_setting(self.filtro_activo)
        else:
            datos = self.varConfig.consultar_setting("informa")

        #for row in datos:
        self.grid_config.insert("", END, text=datos[0], values=(datos[1], datos[2], datos[3], datos[4], datos[5],
                                                                datos[6], datos[7], datos[8], datos[9], datos[10],
                                                                datos[11], datos[12], datos[13], datos[14], datos[15],
                                                                datos[16], datos[17], datos[18], datos[19], datos[20],
                                                                datos[21], datos[22], datos[26]))

        if len(self.grid_config.get_children()) > 0:
            self.grid_config.selection_set(self.grid_config.get_children()[0])

    def limpiar_text(self):

        self.entry_empresa.delete(0, END)
        self.entry_direccion.delete(0, END)
        self.entry_localidad.delete(0, END)
        self.entry_provincia.delete(0, END)
        self.entry_postal.delete(0, END)
        self.entry_correo.delete(0, END)
        self.entry_telef1.delete(0, END)
        self.entry_telef2.delete(0, END)
        self.entry_titular.delete(0, END)
        self.entry_contacto.delete(0,END)
        self.combo_sit_fis.delete(0, END)
        self.entry_cuit.delete(0, END)
        self.entry_rentas.delete(0, END)
        self.entry_municipal.delete(0, END)
        self.entry_tasa_iva1.delete(0, END)
        self.entry_tasa_iva2.delete(0, END)
        self.entry_tasa_iva3.delete(0, END)
        self.entry_tasa_impint.delete(0, END)
        self.entry_tasa_reten.delete(0, END)
        self.entry_tasa_percep.delete(0, END)
        self.entry_dolar1.delete(0, END)
        self.entry_dolar2.delete(0, END)
        self.entry_ultimo_saldo.delete(0, END)

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

    def limpiar_Grid(self):
        for item in self.grid_config.get_children():
            self.grid_config.delete(item)

    def habilitar_Btn_Oper(self, estado):

        self.btnModificar.configure(state=estado)

    def habilitar_Btn_Final(self, estado):

        self.btnGuardar.configure(state=estado)
        self.btnCancelar.configure(state=estado)

    # ----------------------------------------------------------------------------------------
    # CRUD

    def fModificar(self):

        self.selected = self.grid_config.focus()
        self.clave = self.grid_config.item(self.selected, 'text')

        self.alta_modif = 2

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
        else:
            self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta
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

            self.habilitar_Btn_Final("normal")
            self.habilitar_Btn_Oper("disabled")
            self.entry_empresa.focus()

    def fGuardar(self):

        # VALIDACION QUE EXISTA APELLIDO
        if self.strvar_empresa.get() == "" or self.strvar_sit_fis == "" or self.strvar_dolar1 == "" or \
           self.strvar_tasa_iva1 == 0 or self.strvar_tasa_iva2 == 0:

            messagebox.showwarning("Alerta", "Campos requeridos [*]", parent=self)
            self.entry_empresa.focus()
            return

        # VALIDAR CUIT
        if not self.validar_cuit(self.strvar_cuit.get()):   # not True
            messagebox.showwarning("Alerta", "CUIT incorrecto", parent=self)
            self.entry_cuit.focus()
            return
        # -------------------------------------------------------------------------------------------

        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori
        self.selected = self.grid_config.focus()
        # # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_config.item(self.selected, 'text')
        self.nuevo_conf = ""

        if self.alta_modif == 1:
            pass

        elif self.alta_modif == 2:

            self.varConfig.modificar_setting(self.var_Id, self.strvar_empresa.get(),
            self.strvar_direccion.get(), self.strvar_localidad.get(), self.strvar_provincia.get(),
            self.strvar_postal.get(), self.strvar_correo.get(), self.strvar_telef1.get(),
            self.strvar_telef2.get(), self.strvar_titular.get(), self.strvar_contacto.get(),
            self.strvar_sit_fis.get(), self.strvar_cuit.get(), self.strvar_rentas.get(),
            self.strvar_municipal.get(), self.strvar_tasa_iva1.get(), self.strvar_tasa_iva2.get(),
            self.strvar_tasa_iva3.get(), self.strvar_tasa_impint.get(), self.strvar_tasa_reten.get(),
            self.strvar_tasa_percep.get(), self.strvar_dolar1.get(), self.strvar_dolar2.get(),
            self.strvar_ultimo_saldo.get())

            self.var_Id == -1
            messagebox.showinfo("Modificacion", "La modificacion del registro fue exitosa", parent=self)

        self.limpiar_Grid()
        self.llena_grilla()
        self.limpiar_text()
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")
        self.habilitar_text("disabled")

        if self.alta_modif == 1:
            pass
        elif self.alta_modif == 2:
            self.puntabla(self.clave, "B")

        self.alta_modif = 0

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.limpiar_text()
            self.habilitar_Btn_Final("disabled")
            self.habilitar_Btn_Oper("normal")
            self.habilitar_text("disabled")

    def fSalir(self):
        self.master.destroy()

    # ----------------------------------------------------------------------------------------
    # OTROS FUNCIONES

    def DobleClickGrid(self, event):
        self.fModificar()

    def limitador(self, entry_text, caract):
        # Metodo que limita la cantidad de caracteres que ingresan en Entry -OBSERVACIONES - Tiempo de Ingeso
        if len(entry_text.get()) > 0:
            # donde esta el :5 limitas la cantidad d caracteres
            entry_text.set(entry_text.get()[:caract])

    def validar_cuit(self, cuit):
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

    def puntabla(self, registro, tipo_mov):

        # metodo para posicionar el puntero en el TV luego de las distintas acciones sobre los datos

        # trae el indice de la tabla "I001"
        regis = self.grid_config.get_children()
        rg = ""
        contador = 0
        # --------------------------------------------------------------------------------

        # Aca es para acomodar el puntero cuando el registro si existe en la tabla, entonces puedo usar el ID
        # MODIFICACION
        if tipo_mov == "B":
            for rg in regis:
                # En buscado guardo el Id de la tabla (base datos) del que estoy posicionado
                buscado = self.grid_config.item(rg)['text']
                # en registro viene "clave" que es el Id del que estoy parado y lo paso a la funcion como parametro
                contador += 1
                # busco el ID de la tabla con el que guarde antes en "clave" - aca busco un Id de la tabla
                # a registro se le paso el Id de la tabla (es distinto la busqueda a ALTA)
                if buscado == registro:  # 72
                    break

        self.grid_config.selection_set(rg)
        self.grid_config.focus(rg)
        self.grid_config.yview(self.grid_config.index(rg))

        if rg == "":
            return False
        return True
