"""
# ============================ WIDGETS
# ============================ STRINGVARS
# ============================ TREEVIEW
# ============================ ENTRYS
# ============================ PANTALLA (GRILLA - LIMPIAR - BOTONES ON OFF .....)
# ============================ CRUD (NUEVO - EDITAR - MODIF - BORRAR ...)
# ============================ MOVIMIENTOS EN TREEVIEW (NUEVO - EDITAR - MODIF - BORRAR ...)
# ============================ VALIDACIONES
# ============================ IMPRESION
# ========================================================================================================
# FUNCIONES METODOS
# ========================================================================================================
# ---------------------------------------- PANTALLA - WIDGETS - TREEVIEW
# def llena_grilla(self):
# def limpiar_text(self):
# def limpiar_Grid(self):
# def habilitar_text(self, estado):
# def habilitar_Btn_Oper(self, estado):
# def habilitar_Btn_Final(self, estado):
# def habilitar_Btn_busquedas(self, estado):
# def habilitar_Selec_cliente(self, estado):
# def reset_campos(self):
# def fReset_selcli(self):
# ---------------------------------------- STRINGVARS
# def reset_stringvars(self):
# ---------------------------------------- CRUD
# def fNuevo(self):
# def fEditar(self):
# def fBorrar(self):
# def fGuardar(self):
# def fCancelar(self):
# def fCompactar(self):
# def fSalir(self):
# --------------------------------------- MOVIMIENTOS ARCHIVO
# def fToparch(self):
# def fFinarch(self):
# def mover_puntero(self, param_topend):
# def puntabla(self, registro, tipo_mov):
# --------------------------------------- BUSQUEDAS
# def fBuscar_en_tabla(self):
# def fShowall(self):
# def fBuscli(self):
# def fSelec_cli(self):
# --------------------------------------- VALIDACIONES
# def formato_fecha(self, pollo):
# --------------------------------------- IMPRESION
# def fImprime(self):
# ========================================================================================================
"""

import os
from PDF_clase import *
from funciones import *
from ctacte_ABM import *
from tkinter import *
from tkinter import ttk
from clientes_ABM import *
from tkinter import messagebox
from datetime import date, datetime
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkFont


class CuentaCorriente(Frame):
    # Creo la clase - clase definida en
    varCtacte = datosCtacte()

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        # master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # ------ Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # ------ Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 690
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 100
        pheight = round(htotal / 2 - hventana / 2) - 50
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # Se usa para saber que filtro esta activo y mantenerlo - a continuacion se setea a un valor inicial
        self.filtro_activo = "ctacte WHERE cc_codcli = 0 ORDER BY cc_fecha ASC"

        self.create_widgets()
        self.llena_grilla()

        # guarda en item el Id del elemento fila en este caso fila 0
        item = self.grid_ctacte.identify_row(0)

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. """

        self.grid_ctacte.selection_set(item)
        # pone el foco en el item seleccionado
        self.grid_ctacte.focus(item)
        self.habilitar_text("disabled")
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_Selec_cliente("disabled")
        self.habilitar_Btn_Oper("disabled")
        self.entry_nombre_cliente.focus()

    # ==================================================================================================
    # ========================================== WIDGETS ===============================================
    # ==================================================================================================

    def create_widgets(self):

        # TITULOS =============================================================================

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('ctacte.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ctacte = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_ctacte = Label(self.frame_titulo_top, image=self.png_ctacte, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Cuentas Corrientes",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ctacte.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # --------------------------------------------------------------------------

        # VARIABLES GENERALES - =====================================================================
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.var_Id = -1
        self.alta_modif = 0
        vcmd = (self.register(validar), '%P')

        # =====================================================================================
        # ============================ STRINGVARS =============================================
        # =====================================================================================

        self.retorno = ""
        self.strvar_buscostring = tk.StringVar(value="")
        self.strvar_nombre_cliente = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value=0)
        una_fecha = date.today()
        una_fecha = datetime.strftime(una_fecha, "%d/%m/%Y")
        self.strvar_fecha_movim = tk.StringVar(value=una_fecha)
        self.strvar_detalle_movim = tk.StringVar(value="")
        self.strvar_saldo_cliente = tk.StringVar(value="0.00")
        self.strvar_debito_movim = tk.StringVar(value="0.00")
        self.strvar_credito_movim = tk.StringVar(value="0.00")
        self.strvar_clavemov = tk.StringVar(value="0")

        # ========================================================================================
        # ====================================== TREVIEEW  =======================================
        # ========================================================================================

        # LABELFRAME DEL TREEVIEW ---------------------------------------------------------------------------
        self.frame_tvw_ctacte = LabelFrame(self.master, text="Cuentas Corrientes: ", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_ctacte)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_ctacte = ttk.Treeview(self.frame_tvw_ctacte, height=5, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5"))

        # self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_ctacte.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_ctacte.column("col1", width=80, anchor=CENTER, minwidth=60)
        self.grid_ctacte.column("col2", width=300, anchor=CENTER, minwidth=200)
        self.grid_ctacte.column("col3", width=100, anchor=CENTER, minwidth=80)
        self.grid_ctacte.column("col4", width=100, anchor=CENTER, minwidth=80)
        self.grid_ctacte.column("col5", width=80, anchor=CENTER, minwidth=80)

        self.grid_ctacte.heading("#0", text="Id", anchor=CENTER)
        self.grid_ctacte.heading("col1", text="Fecha", anchor=CENTER)
        self.grid_ctacte.heading("col2", text="Detalle", anchor=CENTER)
        self.grid_ctacte.heading("col3", text="Debito", anchor=CENTER)
        self.grid_ctacte.heading("col4", text="Credito", anchor=CENTER)
        self.grid_ctacte.heading("col5", text="Clave", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_ctacte, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_ctacte, orient=VERTICAL)
        self.grid_ctacte.config(xscrollcommand=scroll_x.set)
        self.grid_ctacte.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_ctacte.xview)
        scroll_y.config(command=self.grid_ctacte.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_ctacte['selectmode'] = 'browse'

        self.grid_ctacte.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_ctacte.pack(side=TOP, fill=BOTH, padx=5, pady=2)

        # Armado de los Frames -------------------------------------------------------------------
        self.frame_primero = LabelFrame(self.master, text="", foreground="red")
        self.frame_segundo = LabelFrame(self.master, text="", foreground="red")
        self.frame_tercero = LabelFrame(self.master, text="", foreground="red")
        self.frame_cuarto = LabelFrame(self.master, text="", foreground="red")

        # ========================================================================================
        # ============================= PEDIR CLIENTE A REVISAR ==================================
        # ========================================================================================

        # FRAME primero -------------------------------------------------------------------------------------
        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_primero, text="Cliente: ", justify=LEFT)
        self.lbl_texto_nombre_cliente.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_primero, textvariable=self.strvar_nombre_cliente, width=48)
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.lbl_texto_codigo_cliente = Label(self.frame_primero, textvariable=self.strvar_codigo_cliente, width=10)
        self.lbl_texto_codigo_cliente.grid(row=0, column=2, padx=5, pady=2, sticky=W)

        # BOTON BUSCAR CLIENTE EN LISTBOX
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_primero, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=3, padx=5)

        # BOTON RESET BUSQUEDA DE CLIENTE - HABILLITO ENTRY DEL NOMBRE
        self.photo_reset_cli = Image.open('reset.png')
        self.photo_reset_cli = self.photo_reset_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_reset_cli = ImageTk.PhotoImage(self.photo_reset_cli)
        self.btn_reset_cli = Button(self.frame_primero, text="", image=self.photo_reset_cli, command=self.fReset_selcli,
                                    bg="grey", fg="white")
        self.btn_reset_cli.grid(row=0, column=4, padx=5)

        # Saldo del cliente ----------------------------------------------------------------------------------
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_saldo_cliente = Label(self.frame_primero, text="Saldo: ", font=fff, justify=LEFT)
        self.lbl_saldo_cliente.grid(row=0, column=5, padx=5, pady=2, sticky=W)
        self.lbl_importe_saldo_cliente = Label(self.frame_primero, textvariable=self.strvar_saldo_cliente, width=20,
                                               font=fff, justify=LEFT)
        self.lbl_importe_saldo_cliente.grid(row=0, column=6, padx=5, pady=2, sticky=W)

        # Boton para compactar
        self.btn_compactar = Button(self.frame_primero, text="Compactar", command=self.fCompactar, width=15,
                                    bg="medium purple", fg="white")
        self.btn_compactar.grid(row=0, column=7, padx=4, pady=2)

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = Button(self.frame_primero, image=self.photo_imp, pady=3, command=self.fImprime, border=3)
        self.btn_imprime.grid(row=0, column=8, padx=4, pady=2)
        # self.btnPlaniCaja.place(x=555, y=10, width=100, height=100)

        # botones fin y principio archivo -------------------------------------------------------------------
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_primero, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=9, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_primero, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=10, padx=5, sticky="nsew", pady=2)
        # ---------------------------------------------------------------------------------

        # FRAME Segundo ------------------------------------------------------------------------------
        # LISTBOX SELECCION DEL CLIENTE
        self.lbox_selec_cliente = Listbox(self.frame_segundo, width=50, height=3)
        self.lbox_selec_cliente.grid(row=0, column=0, rowspan=3, padx=10, pady=5, sticky='nsew')
        self.btn_seleccion_cliente = Button(self.frame_segundo, text='Seleccionar', command=self.fSelec_cli, width=19,
                                            bg="CadetBlue", fg="Black")
        self.btn_seleccion_cliente.grid(row=0, column=2, rowspan=3, padx=10, pady=5, sticky='nsew')
        scrollbar = Scrollbar(self.frame_segundo, orient=VERTICAL, width=20)
        scrollbar.grid(row=0, column=1, rowspan=3, sticky='nsew')
        self.lbox_selec_cliente.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lbox_selec_cliente.yview)

        # BUSCAR MOVIMIENTOS --------------------------------------------------------------------------------
        self.lbl_busqueda_ctacte = Label(self.frame_segundo, text="Buscar: ", justify=CENTER)
        self.lbl_busqueda_ctacte.grid(row=0, column=3, padx=3, pady=3, sticky=W)
        self.entry_buscar_ctacte = Entry(self.frame_segundo, textvariable=self.strvar_buscostring, width=30)
        self.entry_buscar_ctacte.grid(row=0, column=4, padx=5, pady=3, sticky=W)

        self.btn_buscar_movim = Button(self.frame_segundo, text="Filtrar", command=self.fBuscar_en_tabla,
                                       bg="blue", fg="white", width=16)
        self.btn_buscar_movim.grid(row=0, column=5, padx=5, pady=3, sticky=W)

        self.btn_muestra_todo_movim = Button(self.frame_segundo, text="Mostrar todo", command=self.fShowall,
                                             bg="blue", fg="white", width=16)
        self.btn_muestra_todo_movim.grid(row=0, column=6, padx=5, pady=3, sticky=W)
        # ---------------------------------------------------------------------------------------

        # FRAME Tercero -------------------------------------------------------------------------
        vcmd = (self.register(validar), '%P')

        # Fecha del movimiento ------------------------------------------------------------------
        self.lbl_fecha_movim = Label(self.frame_tercero, text="Fecha: ", justify=LEFT)
        self.lbl_fecha_movim.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_fecha_movim = Entry(self.frame_tercero, textvariable=self.strvar_fecha_movim, width=10,
                                       justify=RIGHT)
        self.entry_fecha_movim.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_movim.grid(row=0, column=1, padx=5, pady=2, sticky=W)

        # Detalle del movimiento ----------------------------------------------------------------
        self.lbl_detalle_movim = Label(self.frame_tercero, text="Detalle: ", justify=LEFT)
        self.lbl_detalle_movim.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.entry_detalle_movim = Entry(self.frame_tercero, textvariable=self.strvar_detalle_movim, width=125,
                                         justify=LEFT)
        self.strvar_detalle_movim.trace("w", lambda *args: limitador(self.strvar_detalle_movim, 200))
        self.entry_detalle_movim.grid(row=0, column=3, columnspan=30, padx=5, pady=2, sticky=W)

        # Importe Debito ----------------------------------------------------------------
        self.lbl_debito_movim = Label(self.frame_tercero, text="Debito: ", justify=LEFT)
        self.lbl_debito_movim.grid(row=1, column=0, padx=5, pady=2, sticky=W)
        self.entry_debito_movim = Entry(self.frame_tercero, textvariable=self.strvar_debito_movim, width=20,
                                        justify=RIGHT)
        self.entry_debito_movim.config(validate="key", validatecommand=vcmd)
        self.entry_debito_movim.grid(row=1, column=1, padx=5, pady=2, sticky=W)
        self.entry_debito_movim.config(validate="key", validatecommand=vcmd)
        self.strvar_debito_movim.trace("w", lambda *args: self.limitador(self.strvar_debito_movim, 15))
        self.entry_debito_movim.bind('<Tab>', lambda e: self.calcular())

        # Importe Credito ----------------------------------------------------------------
        self.lbl_credito_movim = Label(self.frame_tercero, text="Credito: ", justify=LEFT)
        self.lbl_credito_movim.grid(row=1, column=2, padx=5, pady=2, sticky=W)
        self.entry_credito_movim = Entry(self.frame_tercero, textvariable=self.strvar_credito_movim, width=20,
                                         justify=RIGHT)
        self.entry_credito_movim.config(validate="key", validatecommand=vcmd)
        self.entry_credito_movim.grid(row=1, column=3, padx=5, pady=2, sticky=W)
        self.entry_credito_movim.config(validate="key", validatecommand=vcmd)
        self.strvar_credito_movim.trace("w", lambda *args: self.limitador(self.strvar_credito_movim, 15))
        self.entry_credito_movim.bind('<Tab>', lambda e: self.calcular())
        # --------------------------------------------------------------------------------------

        # FRAME Cuarto -------------------------------------------------------------------------
        # BOTONES DEL TREEVIEW --------------------------------------------------------------------------------
        self.btn_nuevoitem = Button(self.frame_cuarto, text="Nuevo Item", command=self.fNuevo, width=24, bg="blue",
                                    fg="white")
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)
        self.btn_editaitem = Button(self.frame_cuarto, text="Edita Item", command=self.fEditar, width=24, bg="blue",
                                    fg="white")
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)
        self.btn_borraitem = Button(self.frame_cuarto, text="Elimina Item", command=self.fBorrar, width=24, bg="blue",
                                    fg="white")
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)
        self.btn_guardaritem = Button(self.frame_cuarto, text="Guardar item", command=self.fGuardar, width=24,
                                      bg="green", fg="white")
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)
        self.btn_Cancelar = Button(self.frame_cuarto, text="Cancelar", command=self.fCancelar, width=24, bg="red",
                                   fg="white")
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = Button(self.frame_cuarto, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                               bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        # Cerrado de los Frames PACKS ---------------------------------------------------------------------
        self.frame_primero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_segundo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_tercero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_cuarto.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)

        # =============================================================================================
        # ==================================== FUNCSEL ================================================
        # =============================================================================================

        # LABELFRAME DEL TREEVIEW  DE SELECCION ------------------------------------------------------------
        self.frame_tvw_funcsel = LabelFrame(self.master, text="Seleccionar: ", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_funcsel)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_funcsel = ttk.Treeview(self.frame_tvw_funcsel, height=5, columns=("col1", "col2", "col3", "col4"))

        # self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_funcsel.column("#0", width=60, anchor=CENTER, minwidth=60)
        self.grid_funcsel.column("col1", width=200, anchor=CENTER, minwidth=180)
        self.grid_funcsel.column("col2", width=40, anchor=CENTER, minwidth=40)
        self.grid_funcsel.column("col3", width=50, anchor=CENTER, minwidth=50)
        self.grid_funcsel.column("col4", width=50, anchor=CENTER, minwidth=50)

        self.grid_funcsel.heading("#0", text="Id", anchor=CENTER)
        self.grid_funcsel.heading("col1", text="Dato1", anchor=CENTER)
        self.grid_funcsel.heading("col2", text="Dato2", anchor=CENTER)
        self.grid_funcsel.heading("col3", text="Dato3", anchor=CENTER)
        self.grid_funcsel.heading("col4", text="Dato4", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_funcsel, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_funcsel, orient=VERTICAL)
        self.grid_funcsel.config(xscrollcommand=scroll_x.set)
        self.grid_funcsel.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_funcsel.xview)
        scroll_y.config(command=self.grid_funcsel.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_funcsel['selectmode'] = 'browse'

        self.grid_funcsel.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_funcsel.pack(side=TOP, fill=BOTH, padx=5, pady=2)

    # =============================================================================================
    # ==================================== PANTALLA ===============================================
    # =============================================================================================

    def llena_grilla(self):

        if len(self.filtro_activo) > 0:
            datos = self.varCtacte.consultar_ctacte(self.filtro_activo)
        else:
            datos = self.varCtacte.consultar_ctacte("ctacte ORDER BY cc_fecha ASC")

        suma_debitos = 0
        suma_creditos = 0

        for row in datos:
            self.grid_ctacte.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[7]))
            suma_debitos += row[3]
            suma_creditos += row[4]

        self.strvar_saldo_cliente.set(value=(suma_debitos - suma_creditos))

        if len(self.grid_ctacte.get_children()) > 0:
            self.grid_ctacte.selection_set(self.grid_ctacte.get_children()[0])

    def limpiar_text(self):

        una_fecha = date.today()
        una_fecha = datetime.strftime(una_fecha, "%d/%m/%Y")
        self.strvar_fecha_movim.set(value=una_fecha)
        self.entry_detalle_movim.delete(0, END)
        # self.entry_debito_movim.delete(0, END)
        # self.entry_credito_movim.delete(0, END)
        self.strvar_debito_movim.set(value="0.00")
        self.strvar_credito_movim.set(value="0.00")

    def limpiar_Grid(self):

        for item in self.grid_ctacte.get_children():
            self.grid_ctacte.delete(item)

    def habilitar_text(self, estado):

        self.entry_fecha_movim.configure(state=estado)
        self.entry_detalle_movim.configure(state=estado)
        self.entry_debito_movim.configure(state=estado)
        self.entry_credito_movim.configure(state=estado)
        # self.combo_sit_fiscal.configure(state=estado)
        # self.entry_cuit.configure(state=estado)
        # self.entry_observaciones.configure(state=estado)

    def habilitar_Btn_Oper(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)

    def habilitar_Btn_Final(self, estado):

        self.btn_guardaritem.configure(state=estado)
        self.btn_Cancelar.configure(state=estado)

    def habilitar_Btn_busquedas(self, estado):

        self.entry_buscar_ctacte.configure(state=estado)
        self.btn_buscar_movim.configure(state=estado)
        self.btn_muestra_todo_movim.configure(state=estado)
        self.btn_compactar.configure(state=estado)
        self.btn_imprime.configure(state=estado)

    def habilitar_Selec_cliente(self, estado):

        self.lbox_selec_cliente.configure(state=estado)
        self.btn_seleccion_cliente.configure(state=estado)

    def reset_stringvars(self):

        self.retorno = ""
        self.strvar_buscostring.set(value="")
        self.strvar_nombre_cliente.set(value="")
        self.strvar_codigo_cliente.set(value=0)
        una_fecha = date.today()
        una_fecha = datetime.strftime(una_fecha, "%d/%m/%Y")
        self.strvar_fecha_movim.set(value=una_fecha)
        self.strvar_detalle_movim.set(value="")
        self.strvar_saldo_cliente.set(value="0.00")
        self.strvar_debito_movim.set(value="0.00")
        self.strvar_credito_movim.set(value="0.00")

    def reset_campos(self):

        self.strvar_detalle_movim.set(value="")
        self.strvar_debito_movim.set(value="0.00")
        self.strvar_credito_movim.set(value="0.00")

    def fReset_selcli(self):

        self.entry_nombre_cliente.configure(state="normal")
        self.btn_bus_cli.configure(state="normal")
        self.strvar_nombre_cliente.set(value="")
        self.strvar_codigo_cliente.set(value=0)
        self.limpiar_text()
        self.habilitar_text("disabled")

        self.lbox_selec_cliente.configure(state="normal")
        self.lbox_selec_cliente.delete(0, END)
        self.habilitar_Selec_cliente("disabled")
        # self.lbox_selec_cliente.configure(state="disabled")
        # self.btn_seleccion_cliente.configure(state=disa"normal")

        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_Btn_Oper("disabled")
        self.habilitar_Btn_Final("disabled")
        self.limpiar_Grid()
        self.strvar_saldo_cliente.set(value=0)

        self.entry_nombre_cliente.focus()

    # =============================================================================================
    # ==================================== CRUD ===================================================
    # =============================================================================================

    def fNuevo(self):

        # Debe existir cliente se verifica nombre y codigo
        if self.strvar_nombre_cliente.get() == "" or self.strvar_codigo_cliente.get() == "0":
            messagebox.showwarning("Error", " Debe existir un cliente asignado", parent=self)
            self.entry_nombre_cliente.focus()
            return

        self.alta_modif = 1
        self.habilitar_text("normal")
        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_Selec_cliente("disabled")
        self.habilitar_Btn_Oper("disabled")
        self.habilitar_Btn_Final("normal")
        self.entry_fecha_movim.focus()

    def fEditar(self):

        self.alta_modif = 2

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_ctacte.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_ctacte.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return
        else:
            self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta
            self.habilitar_text('normal')
            # En la lista valores cargo todos los registros completos con todos los campos
            valores = self.grid_ctacte.item(self.selected, 'values')

            #    self.reset_stringvars()

            # Al modificar tambien debo convertir la fecha SQL a string dd/mm/yyyy para visualizarla
            una_fecha = datetime.strptime(valores[0], '%Y-%m-%d')
            self.strvar_fecha_movim.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.strvar_detalle_movim.set(value=valores[1])
            self.strvar_debito_movim.set(value=valores[2])
            self.strvar_credito_movim.set(value=valores[3])

        self.habilitar_text("normal")
        self.habilitar_Btn_Oper("disabled")
        self.habilitar_Btn_Final("normal")
        self.entry_nombre_cliente.focus()

    def fBorrar(self):

        # guardo item seleccionado en el grid
        self.selected = self.grid_ctacte.focus()
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_ctacte.item(self.selected, 'text')

        # guardo la clae de movimiento anterior si la hay
        self.clavemov_ant = 0

        que_paso = self.puntabla(self.selected, "E")

        if self.clave == "":

            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)

        else:

            valores = self.grid_ctacte.item(self.selected, 'values')
            # guardo clave de movimietno anterior
            #            self.clavemov_ant = valores[17]
            data = str(self.clave) + " " + valores[2]

            r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)

            if r == messagebox.YES:

                # Elimino de tabla planicaja
                n = self.varCtacte.eliminar_item_ctacte(self.clave)

                # # Elimino de tabla ctacte si existe clave de movimiento
                # if self.clavemov_ant != 0:
                #     self.varPlanilla.eliminar_item_ctacte_xmodif(self.clavemov_ant)

                if n == 1:
                    messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
                    self.limpiar_Grid()
                    self.llena_grilla()
                else:
                    messagebox.showinfo("Eliminar", "No fue posible eliminar el Registro", parent=self)

        que_paso = self.puntabla(self.selected, "F")

    def fGuardar(self):

        # 1- Validaciones que correspondan ---------------------------------------------------------------
        # FECHA ------------------------------------------------------------------------------------------
        if self.strvar_fecha_movim.get() == "":
            messagebox.showerror("Error", "Fecha en blanco", parent=self)
            self.entry_fecha_movim.focus()
            return

        # DETALLE ----------------------------------------------------------------------------------------
        if self.strvar_detalle_movim.get() == "":
            messagebox.showerror("Error", "Agregue un detalle", parent=self)
            self.entry_detalle_movim.focus()
            return

        # CAMPOS DE IMPORTE -----------------------------------------------------------------------------
        if self.strvar_debito_movim.get() == "0.00" and self.strvar_credito_movim.get() == "0.00":
            messagebox.showerror("Error", "No i mgreso importes", parent=self)
            self.entry_debito_movim.focus()
            return

        aaa = 0
        if aaa == 0:
            # #try:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori --------------------------
            self.selected = self.grid_ctacte.focus()
            # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
            self.clave = self.grid_ctacte.item(self.selected, 'text')
            self.nuevo_itempla = ""

            if self.alta_modif == 1:

                # INGRESO - ALTA

                self.nuevo_itempla = str(self.strvar_detalle_movim.get())

                # debe ser cero si es un alta de nuevo movimiento ------------------------------------------------
                self.strvar_clavemov.set(value="0")

                # guardo movimiento en ctacte ----------------------------------------------------------------
                fecha_aux = datetime.strptime(self.strvar_fecha_movim.get(), '%d/%m/%Y')
                self.varCtacte.insertar_ctacte(fecha_aux, self.strvar_detalle_movim.get(),
                                               self.strvar_debito_movim.get(), self.strvar_credito_movim.get(),
                                               self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                               self.strvar_clavemov.get())

                messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

            else:

                # MODIFICACION

                self.strvar_clavemov.set(value="0")

                self.varCtacte.modificar_ctacte(self.var_Id, self.strvar_fecha_movim.get(),
                                                self.strvar_detalle_movim.get(), self.strvar_debito_movim.get(),
                                                self.strvar_credito_movim.get(),
                                                self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                                self.strvar_clavemov.get())

                self.var_Id == -1
                messagebox.showinfo("Modificacion", "La modificacion fue exitosa", parent=self)

            # cierre de las novedades y reseteando pantalla para nuevo movimiento - actualizando grilla -------
            self.limpiar_Grid()
            self.llena_grilla()
            self.reset_campos()

            # Deshabilitar variables a estado cero
            self.habilitar_text("disabled")
            # rehabilitar botones correspondientes
            self.habilitar_Btn_Oper("normal")
            self.habilitar_Btn_Final("disabled")

            self.lbox_selec_cliente.configure(state="normal")
            self.lbox_selec_cliente.delete(0, END)
            self.btn_seleccion_cliente.configure(state="disabled")

            # ordenamiento puntero en treeview
            if self.alta_modif == 1:
                # ALTA
                self.puntabla(self.nuevo_itempla, "A")
            elif self.alta_modif == 2:
                # MODIFICACION
                que_paso = self.puntabla(self.clave, "B")
            elif self.alta_modif == 0:
                messagebox.showerror("Error", "codigo de Alta_modif cero", parent=self)
                return

            # self.alta_modif = 0

            self.btn_nuevoitem.focus()

        # #except:

        #     messagebox.showerror("Error", "Revise Fechas", parent=self)
        #     self.entry_fecha_planilla.focus()
        #     return

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.fReset_selcli()

    def fCompactar(self):
        pass

    def fSalir(self):
        self.master.destroy()

    # ===================================================================================================
    # ==================================== MOVIMIENTO EN TREEVIEW =======================================
    # ===================================================================================================

    def fToparch(self):
        self.mover_puntero('TOP')

    def fFinarch(self):
        self.mover_puntero('END')

    def mover_puntero(self, param_topend):

        # Para ir a tope o fin de archivo -----------------------------------------------------------
        if param_topend == "":
            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_ctacte.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            clave = self.grid_ctacte.item(self.selected, 'text')

        # Si es tope de archivo ----------------------------------------------------------------------
        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_ctacte.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_ctacte.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_ctacte.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_ctacte.yview(self.grid_ctacte.index(self.grid_ctacte.get_children()[0]))

        # Si es fin de archivo -----------------------------------------------------------------------
        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_ctacte.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_ctacte.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_ctacte.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_ctacte.yview(self.grid_ctacte.index(self.grid_ctacte.get_children()[-1]))

    def puntabla(self, registro, tipo_mov):

        # metodo para posicionar el puntero en el TV luego de las distintas acciones sobre los datos

        # trae el indice de la tabla "I001"
        regis = self.grid_ctacte.get_children()
        rg = ""
        contador = 0
        # --------------------------------------------------------------------------------

        # aca traigo el codigo del registr0 (cod.cliente, cod. art.... que estoy dando de alta porque aun no tengo ID)
        # ALTA
        if tipo_mov == "A":
            for rg in regis:
                buscado = self.grid_ctacte.item(rg)['values']
                # contador = contador + 1
                # busco el codigo de contrato que ingrese nuevo - Aca busco un campo de la tabla
                # a registro se le paso el nro de contrato en este caso
                if str(buscado[0]) == registro:
                    break
        # ----------------------------------------------------------------------------------------------------

        # Aca es para acomodar el puntero cuando el registro si existe en la tabla, entonces puedo usar el ID
        # MODIFICACION
        if tipo_mov == "B":
            for rg in regis:
                # En buscado guardo el Id de la tabla (base datos) del que estoy posicionado
                buscado = self.grid_ctacte.item(rg)['text']
                # en registro viene "clave" que es el Id del que estoy parado y lo paso a la funcion como parametro
                contador += 1
                # busco el ID de la tabla con el que guarde antes en "clave" - aca busco un Id de la tabla
                # a registro se le paso el Id de la tabla (es distinto la busqueda a ALTA)
                if buscado == registro:  # 72
                    break
        # -----------------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 1 -es la parte donde tomo el Id del registro que le sigue al que voy a eliminar
        if tipo_mov == 'E':
            control = 1
            self.buscado2 = ""
            for rg in regis:
                contador += 1
                if control == 0:
                    # guardo Id del que sigue
                    buscado = self.grid_ctacte.item(rg)['values']
                    self.buscado2 = str(buscado[2])
                    break
                if rg == registro:  # registro seria self.selected o sea el Id de la BD
                    control = 0
        # -------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id del que obtuve antes
        # que es el que sigue al que borre
        if tipo_mov == 'F':
            for rg in regis:
                buscado = self.grid_ctacte.item(rg)['values']
                if self.buscado2 == str(buscado[2]):
                    break
        # ------------------------------------------------------------------------------------------

        # BUSCAR EN TABLA - Viene de la funcion que busca en la tabla lo que se requiere
        if tipo_mov == 'S':
            if regis != ():
                for rg in regis:
                    break
                if rg == "":
                    self.btn_buscar_planilla.configure(state="disabled")
                    return
        # ----------------------------------------------------------------------------------------

        self.grid_ctacte.selection_set(rg)
        self.grid_ctacte.focus(rg)
        self.grid_ctacte.yview(self.grid_ctacte.index(rg))

        if rg == "":
            return False
        return True

    # ===================================================================================================
    # ========================================= BUSQUEDAS ===============================================
    # ===================================================================================================

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()

            self.filtro_anterior = self.filtro_activo

            self.filtro_activo = (
                        "ctacte WHERE cc_codcli = '" + self.strvar_codigo_cliente.get() + "' AND INSTR(cc_detalle, '" + se_busca + "') > 0")

            self.varCtacte.buscar_entabla(self.filtro_activo)
            self.limpiar_Grid()
            self.llena_grilla()

            # funcion que acomoda el puntero en el TV
            que_paso = self.puntabla("", "S")

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

    def fShowall(self):

        self.filtro_activo = "ctacte WHERE cc_codcli = '" + self.strvar_codigo_cliente.get() + "' ORDER BY cc_fecha ASC"
        self.limpiar_Grid()
        self.llena_grilla()

    # def fBuscli(self):
    #
    #     # busqueda de cliente para carga de la orden - usa listbox ----------------------------------------
    #     if len(self.strvar_nombre_cliente.get()) > 0:
    #         """
    #         2 - acceder la tabla de clientes y filtrar por el string de busqueda que se
    #         haya colocado en el entry cliente
    #         el comando INSTR de SQL nos busca la posicion de lo que busco dentro de una cadena, si no la encuentra
    #         devuelve cero
    #         """
    #         se_busca = self.strvar_nombre_cliente.get()
    #
    #         que_busco = "clientes WHERE INSTR(apellido, '" + se_busca + "') > 0"\
    #                     + " OR " + "INSTR(nombres, '" + se_busca + "') > 0"
    #
    #         self.retorno = self.varCtacte.buscar_entabla(que_busco)
    #
    #         # borro los items anteriores del listbox y habilito botones ------------------------------------------
    #         self.lbox_selec_cliente.configure(state="normal")
    #         self.lbox_selec_cliente.delete(0, END)
    #         self.btn_seleccion_cliente.configure(state="normal")
    #
    #         # llenar listbox con lo filtrado (campo apellido y nombre
    #         for index, reto in enumerate(self.retorno):
    #             if reto[2] == "":
    #                 self.lbox_selec_cliente.insert(index, reto[3])
    #             else:
    #                 self.lbox_selec_cliente.insert(index, reto[2]+' '+reto[3])
    #
    #         self.lbox_selec_cliente.focus()
    #
    #     else:
    #
    #         messagebox.showwarning("Alerta", "No ingreso busqueda", parent=self)

    def fSelec_cli(self):
        pass

    def fBuscli(self):

        se_busca = self.strvar_nombre_cliente.get()

        que_busco = "clientes WHERE INSTR(apellido, '" + se_busca + "') > 0" \
                    + " OR " + "INSTR(nombres, '" + se_busca + "') > 0"\
                    + " OR " + "INSTR(CONCAT(apellido,' ',nombres), '" + se_busca + "') > 0"

        self.retorno = self.varCtacte.buscar_entabla(que_busco)

        for index, reto in enumerate(self.retorno):
            if reto[2] == "":
                nombre_cliente = reto[3]
            else:
                nombre_cliente = (reto[2] + ' ' + reto[3])

            # for row in datos:
            #     self.grid_ctacte.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[7]))

            self.varCtacte.insertar_funcsel(nombre_cliente, reto[1], reto[4], "hola")

        # if len(self.filtro_activo) > 0:
        nuevofiltro = "funcsel ORDER BY fs_dato1 ASC"

        datos = self.varCtacte.consultar_ctacte(nuevofiltro)

        # else:
        #     datos = self.varCtacte.consultar_ctacte("ctacte ORDER BY cc_fecha ASC")

        for row in datos:
            self.grid_funcsel.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4]))

        if len(self.grid_funcsel.get_children()) > 0:
            self.grid_funcsel.selection_set(self.grid_funcsel.get_children()[0])

        # #self.habilitar_text("normal")
        # self.habilitar_Btn_busquedas("normal")
        # self.habilitar_Btn_Oper("normal")
        #
        # self.strvar_codigo_cliente.set(value=0)
        #
        # # Metodo del boton seleccionar cliente debe devolver los datos del cliente enfocado ---------------
        # for item in self.lbox_selec_cliente.curselection():
        #     self.strvar_nombre_cliente.set(value=self.lbox_selec_cliente.get(item))
        #
        # for item in self.retorno:
        #
        #     if item[2] == "":
        #         if self.strvar_nombre_cliente.get() == item[3]:
        #             self.strvar_codigo_cliente.set(value=item[1])
        #
        #     if item[2] != "":
        #         if self.strvar_nombre_cliente.get() == (item[2] + ' ' + item[3]):
        #             self.strvar_codigo_cliente.set(value=item[1])
        #
        # # si el codigo de cliente no es cero, filtro la tabla por el cliente seleccionado --------------------
        # if int(self.strvar_codigo_cliente.get()) != 0:
        #     # filtrar la cuenta corriente para este cliente
        #     self.filtro_activo = "ctacte WHERE cc_codcli = '" + self.strvar_codigo_cliente.get() +" ' ORDER BY cc_fecha ASC"
        #     self.limpiar_Grid()
        #     self.llena_grilla()
        #
        #     # inhabilito edicion de nombre de cliente para que no pueda cambiarlo
        #     self.entry_nombre_cliente.configure(state="disabled")
        #     self.btn_bus_cli.configure(state="disabled")

    # =================================================================================================
    # ======================================= VALIDACIONES ============================================
    # =================================================================================================

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_movim.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_movim.get())

        if retorno_VerFal == "":
            self.strvar_fecha_movim.set(value=estado_antes)
            self.entry_fecha_movim.focus()
            return ("error")
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.filtro_activo = "planicaja WHERE CAST(pl_fecha AS date) = CAST('" + self.strvar_fecha_movim.get() + "' AS date)"
            self.limpiar_Grid()
            self.llena_grilla()
            self.entry_fecha_movim.focus()
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_movim.set(value=estado_antes)
            self.entry_fecha_movim.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_movim.set(value=retorno_VerFal)

            # # funcion que hace las transformaciones de fecha para volver a generar el filtro activo
            # self.filtrar_grilla(self.strvar_fecha_movim.get())

        return ("bien")

    # ================================================================================================
    # ============================ CALCULOS Y VALIDACION DATOS =======================================
    # ================================================================================================

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def calcular(self):

        try:

            # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
            if not control_forma(list(self.strvar_debito_movim.get())):
                self.strvar_debito_movim.set(value=0)
                self.entry_debito_movim.focus()
                return
            if not control_forma(list(self.strvar_credito_movim.get())):
                self.strvar_credito_movim.set(value=0)
                self.entry_credito_movim.focus()
                return

            # Control de valor en blanco o solo un . o -
            if self.strvar_debito_movim.get() == "" or self.strvar_debito_movim.get() == "." or self.strvar_debito_movim.get() == "-":
                self.strvar_debito_movim.set(value=0)
            if self.strvar_credito_movim.get() == "" or self.strvar_credito_movim.get() == "." or self.strvar_credito_movim.get() == "-":
                self.strvar_credito_movim.set(value=0)

            # control de valor en cero o si tiene mas de dos decimales lo trunco a dos
            if float(self.strvar_debito_movim.get()) == 0:
                self.strvar_debito_movim.set(value=0)
            else:
                self.strvar_debito_movim.set(value=round(float(self.strvar_debito_movim.get()), 2))

            if float(self.strvar_credito_movim.get()) == 0:
                self.strvar_credito_movim.set(value=0)
            else:
                self.strvar_credito_movim.set(value=round(float(self.strvar_credito_movim.get()), 2))

        except:

            messagebox.showerror("Error", "Revise entradas numericas", parent=self)
            self.entry_total_partes.focus()
            return

    # ================================================================================================
    # ======================================= INFORMES ===============================================
    # ================================================================================================

    def fImprime(self):

        # # traigo el registro que quiero imprimir
        # self.selected = self.grid_ctacte.focus()
        # # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # # que pone la BD automaticamente al dar el alta
        # self.clave = self.grid_ctacte.item(self.selected, 'text')
        #
        # if self.clave == "":
        #     messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
        #     return

        # Debo filtrar el cliente seleccionado
        adad = self.strvar_codigo_cliente.get()
        datos_registro_selec = self.varCtacte.consultar_ctacte(
            "ctacte WHERE cc_codcli = '" + adad + "' ORDER BY cc_fecha ASC")
        print(datos_registro_selec)

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

        # armado de encabezado --------------------------------------------------------------
        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")

        # Imprimo el encabezado de pagina ---------------------------------------------------
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Saldos en Cuenta Corriente - Fecha y Hora: ' + feac, border=1, align='C', fill=0, ln=1)
        # -----------------------------------------------------------------------------------

        pdf.cell(w=15, h=8, txt='Fecha', border=1, align='C', fill=0)
        pdf.cell(w=100, h=8, txt='Detalle', border=1, align='C', fill=0)
        pdf.cell(w=20, h=8, txt='Ingreso', border=1, align='C', fill=0)
        pdf.cell(w=20, h=8, txt='Egreso', border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=8, txt='Saldo', border=1, align='C', fill=0)
        # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)
        pdf.set_font('Arial', '', 5)

        tot_saldo = 0
        for row in datos_registro_selec:
            fecha1 = datetime.strftime(row[1], "%d-%m-%Y")

            tot_saldo += row[3] - row[4]
            pdf.cell(w=15, h=6, txt=fecha1, border=1, align='C', fill=0)
            pdf.cell(w=100, h=6, txt=row[2], border=1, align='C', fill=0)
            pdf.cell(w=20, h=6, txt=str(row[3]), border=1, align='C', fill=0)
            pdf.cell(w=20, h=6, txt=str(row[4]), border=1, align='C', fill=0)
            pdf.multi_cell(w=0, h=6, txt=str(tot_saldo), border=1, align='E', fill=0)

        pdf.output('hoja.pdf')
        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)
