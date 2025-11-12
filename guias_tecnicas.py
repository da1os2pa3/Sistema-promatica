import os
from tkinter import *
from tkinter import ttk
from guias_tecnicas_ABM import *
from tkinter import messagebox
import tkinter as tk
from tkinter.scrolledtext import *     # para campos text
from PIL import Image, ImageTk
from tkVideoPlayer import TkinterVideo

class clase_GuiasTecnicas(Frame):

    # Creo una instancia de la clase - clase definida en guias_tecnicas_ABM.py
    varGuiaTecnica = datosGuiasTecnicas()

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # ------ Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # ------ Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 725
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) - 0
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # Se usa para saber que filtro esta activo y mantenerlo - a continuacion se setea a un valor inicial
        self.filtro_activo = "guias_tecnicas ORDER BY gt_clave ASC"

        self.carpeta_principal = os.path.dirname(__file__)

        # Debe existir la carpeta "tecnica" en la carpeta donde este el sistema
        self.carpeta_guias = os.path.join(self.carpeta_principal, "tecnica")
        self.carpeta_fotos = os.path.join(self.carpeta_principal, "fotos")

        # Verifico que existan las carpetas
        if os.path.isfile(self.carpeta_guias):
            messagebox.showerror("Error", "No existe la carpeta")
            return
        if os.path.isfile(self.carpeta_fotos):
            messagebox.showerror("Error", "No existe la carpeta")
            return

        # self.photoa = Image.open("C:\Proyectos_Python\ABM_Clientes\foto\rubro.png")
        # self.imagen_defa = "logo1.jpg"

        self.imagen_defa = "tapiz.jpg"

        self.cual_foto = 0

        self.create_widgets()
        self.llena_grilla()

        # guarda en item el Id del elemento fila en este caso fila 0
        item = self.grid_guias_tecnicas.identify_row(0)

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. """

        self.grid_guias_tecnicas.selection_set(item)
        # pone el foco en el item seleccionado
        self.grid_guias_tecnicas.focus(item)
        self.habilitar_Btn_busquedas("normal")
        self.habilitar_text("disabled")
        self.habilitar_Btn_ABM("normal")
        self.habilitar_Btn_guardar_cancelar("disabled")

    # ==================================================================================================
    # ========================================== WIDGETS ===============================================
    # ==================================================================================================

    def create_widgets(self):

        # TITULOS =============================================================================

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('tecnica.png')

        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ctacte = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_ctacte = Label(self.frame_titulo_top, image=self.png_ctacte, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Guias Tecnicas",
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

        # =====================================================================================
        # ============================ STRINGVARS =============================================
        # =====================================================================================

        self.strvar_buscostring = tk.StringVar(value="")
        self.strvar_palabra_clave = tk.StringVar(value="")
        self.strvar_descripcion = tk.StringVar(value="")
        self.strvar_ruta = tk.StringVar(value="")
        self.strvar_imagen_Art = tk.StringVar(value="")

        self.strvar_foto_uno = tk.StringVar(value="")
        self.strvar_foto_dos = tk.StringVar(value="")
        self.strvar_foto_tres = tk.StringVar(value="")

        self.strvar_video_uno = tk.StringVar(value="")
        self.strvar_video_dos = tk.StringVar(value="")

        self.strvar_otros_docu = tk.StringVar(value="")

        # ========================================================================================
        # ====================================== TREVIEEW  =======================================
        # ========================================================================================

        # LABELFRAME DEL TREEVIEW ---------------------------------------------------------------------------
        self.frame_grid_guias=LabelFrame(self.master, text="Guias Tecnicas: ", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_guias)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_guias_tecnicas = ttk.Treeview(self.frame_grid_guias, height=6, columns=("col1", "col2", "col3",
                                                                                          "col4", "col5", "col6",
                                                                                          "col7", "col8", "col9",
                                                                                          "col10"))

        self.grid_guias_tecnicas.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_guias_tecnicas.column("#0", width=50, anchor=CENTER, minwidth=50)
        self.grid_guias_tecnicas.column("col1", width=200, anchor=CENTER, minwidth=200)
        self.grid_guias_tecnicas.column("col2", width=350, anchor=CENTER, minwidth=350)
        self.grid_guias_tecnicas.column("col3", width=300, anchor=CENTER, minwidth=300)
        self.grid_guias_tecnicas.column("col4", width=150, anchor=CENTER, minwidth=150)
        self.grid_guias_tecnicas.column("col5", width=150, anchor=CENTER, minwidth=150)
        self.grid_guias_tecnicas.column("col6", width=150, anchor=CENTER, minwidth=150)
        self.grid_guias_tecnicas.column("col7", width=150, anchor=CENTER, minwidth=150)
        self.grid_guias_tecnicas.column("col8", width=150, anchor=CENTER, minwidth=150)
        self.grid_guias_tecnicas.column("col9", width=150, anchor=CENTER, minwidth=150)
        self.grid_guias_tecnicas.column("col10", width=150, anchor=CENTER, minwidth=150)

        self.grid_guias_tecnicas.heading("#0", text="Id", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col1", text="Clave", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col2", text="Descripcion", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col3", text="Ruta", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col4", text="Texto", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col5", text="foto_1", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col6", text="foto_2", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col7", text="foto_3", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col8", text="video_1", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col9", text="video_2", anchor=CENTER)
        self.grid_guias_tecnicas.heading("col10", text="otros", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_grid_guias, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_grid_guias, orient=VERTICAL)
        self.grid_guias_tecnicas.config(xscrollcommand=scroll_x.set)
        self.grid_guias_tecnicas.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_guias_tecnicas.xview)
        scroll_y.config(command=self.grid_guias_tecnicas.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_guias_tecnicas['selectmode'] = 'browse'

        self.grid_guias_tecnicas.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_grid_guias.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        # ---------------------------------------------------------------------------------------------------

        # Primer frame botones -------------------------------------------------------------------------------
        self.frame_primero=LabelFrame(self.master, text="", foreground="red")

        # BUSCAR MOVIMIENTOS
        self.lbl_buscar_clave = Label(self.frame_primero, text="Buscar: ", justify=LEFT)
        self.lbl_buscar_clave.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.entry_buscar_clave = Entry(self.frame_primero, textvariable=self.strvar_buscostring, width=50)
        self.entry_buscar_clave.grid(row=0, column=1, padx=5, pady=3, sticky=W)

        self.btn_buscar_movim = Button(self.frame_primero, text="Filtrar", command=self.fBuscar_en_tabla,
                                       bg="cadetblue", fg="white", width=22)
        self.btn_buscar_movim.grid(row=0, column=2, padx=5, pady=3, sticky=W)

        self.btn_showall = Button(self.frame_primero, text="Mostrar todo", command=self.fShowall,
                                  bg="cadetblue", fg="white", width=22)
        self.btn_showall.grid(row=0, column=3, padx=5, pady=3, sticky=W)

        self.btn_reset_buscar = Button(self.frame_primero, text="Reset busqueda", command=self.fReset_buscar,
                                  bg="red", fg="white", width=22)
        self.btn_reset_buscar.grid(row=0, column=4, padx=5, pady=3, sticky=W)

        # botones fin y principio archivo ---------------------------------------------------------------------
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_primero, text="", image=self.photo4, command=self.fToparch, bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=5, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_primero, text="", image=self.photo5, command=self.fFinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=6, padx=5, sticky="nsew", pady=2)

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = Button(self.frame_primero, image=self.photo_imp, pady=3, command=self.fImprime, border=3)
        self.btn_imprime.grid(row=0, column=7, padx=4, pady=2)
        #self.btnPlaniCaja.place(x=555, y=10, width=100, height=100)

        self.frame_primero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # -------------------------------------------------------------------------------------------------

        # Segundo Frame Entrys ----------------------------------------------------------------------------
        self.frame_segundo = LabelFrame(self.master, text="", foreground="red")

        # Palabra Clave
        self.lbl_palabra_clave = Label(self.frame_segundo, text="Palabra Clave: ", justify=LEFT)
        self.lbl_palabra_clave.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.entry_palabra_clave = Entry(self.frame_segundo, textvariable=self.strvar_palabra_clave, width=40)
        self.entry_palabra_clave.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        # Breve descripcion
        self.lbl_descripcion = Label(self.frame_segundo, text="Descripcion: ", justify=LEFT)
        self.lbl_descripcion.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_descripcion = Entry(self.frame_segundo, textvariable=self.strvar_descripcion, width=99)
        self.entry_descripcion.grid(row=0, column=3, padx=2, pady=2, sticky=W)

        self.frame_segundo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # --------------------------------------------------------------------------------------------------

        # frame para ingreso solo de la ruta
        self.frame_octavo = LabelFrame(self.master, text="", foreground="red")

        self.lbl_ruta = Label(self.frame_octavo, text="Ruta: ", justify=LEFT)
        self.lbl_ruta.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.entry_ruta = Entry(self.frame_octavo, textvariable=self.strvar_ruta, width=161)
        self.entry_ruta.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        self.frame_octavo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # --------------------------------------------------------------------------------------------------

        # Segundo Frame Videos y fotos ---------------------------------------------------------------------
        self.frame_septimo = LabelFrame(self.master, text="", foreground="red")

        # Rutas fotos
        self.lbl_foto_uno = Label(self.frame_septimo, text="Foto 1: ", justify=LEFT)
        self.lbl_foto_uno.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.entry_foto_uno = Entry(self.frame_septimo, textvariable=self.strvar_foto_uno, width=35)
        self.entry_foto_uno.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.entry_foto_uno.bind('<Tab>', lambda e: self.validar_imagen(self.strvar_foto_uno.get()))
        self.btn_foto_uno = Button(self.frame_septimo, text="Ver", width=7, command=self.fVer_foto_uno, bg="grey", fg="white")
        self.btn_foto_uno.grid(row=0, column=2, padx=5, sticky="nsew", pady=2)

        self.lbl_foto_dos = Label(self.frame_septimo, text="Foto 2: ", justify=LEFT)
        self.lbl_foto_dos.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.entry_foto_dos = Entry(self.frame_septimo, textvariable=self.strvar_foto_dos, width=35)
        self.entry_foto_dos.bind('<Tab>', lambda e: self.validar_imagen(self.strvar_foto_dos.get()))
        self.entry_foto_dos.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.btn_foto_dos = Button(self.frame_septimo, text="Ver", width=7, command=self.fVer_foto_dos, bg="grey", fg="white")
        self.btn_foto_dos.grid(row=0, column=5, padx=5, sticky="nsew", pady=2)

        self.lbl_foto_tres = Label(self.frame_septimo, text="Foto 3: ", justify=LEFT)
        self.lbl_foto_tres.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        self.entry_foto_tres = Entry(self.frame_septimo, textvariable=self.strvar_foto_tres, width=34)
        self.entry_foto_tres.bind('<Tab>', lambda e: self.validar_imagen(self.strvar_foto_tres.get()))
        self.entry_foto_tres.grid(row=0, column=7, padx=2, pady=2, sticky=W)
        self.btn_foto_tres = Button(self.frame_septimo, text="Ver", width=7, command=self.fVer_foto_tres, bg="grey", fg="white")
        self.btn_foto_tres.grid(row=0, column=8, padx=5, sticky="nsew", pady=2)

        # Rutas videos
        self.lbl_video_uno = Label(self.frame_septimo, text="Video 1: ", justify=LEFT)
        self.lbl_video_uno.grid(row=1, column=0, padx=2, pady=2, sticky=W)
        self.entry_video_uno = Entry(self.frame_septimo, textvariable=self.strvar_video_uno, width=35)
        self.entry_video_uno.grid(row=1, column=1, padx=2, pady=2, sticky=W)
        self.btn_video_uno = Button(self.frame_septimo, text="Ver", width=7, command=self.fVer_video_uno, bg="grey", fg="white")
        self.btn_video_uno.grid(row=1, column=2, padx=5, sticky="nsew", pady=2)

        self.lbl_video_dos = Label(self.frame_septimo, text="Video 2: ", justify=LEFT)
        self.lbl_video_dos.grid(row=1, column=3, padx=2, pady=2, sticky=W)
        self.entry_video_dos = Entry(self.frame_septimo, textvariable=self.strvar_video_dos, width=35)
        self.entry_video_dos.grid(row=1, column=4, padx=2, pady=2, sticky=W)
        self.btn_video_dos = Button(self.frame_septimo, text="Ver", width=7, command=self.fVer_video_dos, bg="grey", fg="white")
        self.btn_video_dos.grid(row=1, column=5, padx=5, sticky="nsew", pady=2)

        self.lbl_otros_docu = Label(self.frame_septimo, text="Otros: ", justify=LEFT)
        self.lbl_otros_docu.grid(row=1, column=6, padx=2, pady=2, sticky=W)
        self.entry_otros_docu = Entry(self.frame_septimo, textvariable=self.strvar_otros_docu, width=34)
        self.entry_otros_docu.grid(row=1, column=7, padx=2, pady=2, sticky=W)
        self.btn_otros_docu = Button(self.frame_septimo, text="Ver", width=7, command=self.fVer_otros, bg="grey", fg="white")
        self.btn_otros_docu.grid(row=1, column=8, padx=5, sticky="nsew", pady=2)

        self.frame_septimo.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # --------------------------------------------------------------------------------------------------

        # Tercero Frame tercero (contenedor) cuarto (texto) y quinto (fotos) -------------------------------
        self.frame_tercero = Frame(self.master)
        self.frame_cuarto = LabelFrame(self.frame_tercero, text="", foreground="red")
        self.frame_quinto = LabelFrame(self.frame_tercero, text="", foreground="red")

        # Ingreso de texto
        self.text_guia = ScrolledText(self.frame_cuarto)
        self.text_guia.config(width=80, height=12, wrap="word", padx=5, pady=5)
        self.text_guia.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Ingreso de imagen
        #self.entry_imagen_art = Entry(self.frame_quinto, textvariable=self.strvar_imagen_Art, width=25)
        #self.entry_imagen_art.bind('<Tab>', lambda e: self.validar_imagen())

        # Viene en self.imagen.defa - "tapiz.jpg" por default definida en variables generales arriba
        self.photoa = Image.open(os.path.join(self.carpeta_guias, self.imagen_defa))
        self.photoa = self.photoa.resize((300, 200), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.imagen_art = ImageTk.PhotoImage(self.photoa)
        # muestro la imagen en el frame
        self.lbl_imagen_art = Label(self.frame_quinto, image=self.imagen_art, bg="white", relief=RIDGE, bd=5, padx=5)

        # self.lbl_foto = Label(self.frame_quinto, text="Foto: ", justify=LEFT)
        # #self.lbl_descripcion.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        # self.entry_foto = Entry(self.frame_quinto, textvariable=self.strvar_descripcion, width=130)
        # #self.entry_descripcion.grid(row=0, column=3, padx=2, pady=2, sticky=W)

        self.lbl_imagen_art.pack(expand=0, side=TOP, pady=2, padx=2)
        #self.lbl_foto.pack(expand=0, side=TOP, pady=2, padx=2)
        #self.entry_foto.pack(expand=0, side=TOP, pady=2, padx=2)
        self.frame_cuarto.pack(side=LEFT, fill=BOTH, expand=0, padx=5, pady=2)
        self.frame_quinto.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tercero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # -------------------------------------------------------------------------------------------------

        # Cuarto frame de botones -------------------------------------------------------------------------
        self.frame_sexto = LabelFrame(self.master, text="", foreground="red")

        # BOTONES DEL TREEVIEW ----------------------------------------------------------------------------
        self.btn_nuevoitem = Button(self.frame_sexto, text="Nuevo", command=self.fNuevo, width=24, bg="blue", fg="white")
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)
        self.btn_editaitem = Button(self.frame_sexto, text="Editar", command=self.fEditar, width=24, bg="blue", fg="white")
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)
        self.btn_borraitem = Button(self.frame_sexto, text="Eliminar", command=self.fBorrar, width=24, bg="blue", fg="white")
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)
        self.btn_guardaritem = Button(self.frame_sexto, text="Guardar", command=self.fGuardar, width=24, bg="green", fg="white")
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)
        self.btn_Cancelar = Button(self.frame_sexto, text="Cancelar", command=self.fCancelar, width=24, bg="red", fg="white")
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_sexto, text="Salir", image=self.photo3, width=65, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        self.frame_sexto.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)
        # --------------------------------------------------------------------------------------------------

    # =====================================================================================
    # ================================= GRILLA ============================================
    # =====================================================================================

    def llena_grilla(self):

        if len(self.filtro_activo) < 0:
            messagebox.showerror("Error", "Filtro activo erroneo", parent=self)
            return

        datos = self.varGuiaTecnica.consultar_guia(self.filtro_activo)
        for row in datos:

            self.grid_guias_tecnicas.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[5],
                                                                          row[6], row[7], row[8], row[9], row[10]))

        """ get_children() es que obtiene todos los datos. El [0] indica que obtiene el elemento
        # correspondiente a ese indice o sea el Id I001, si no le pongo nada, trae todos los Id)
        # Esto parece hacer que el treeview se posicione en el primero """

        if len(self.grid_guias_tecnicas.get_children()) > 0:
            self.grid_guias_tecnicas.selection_set(self.grid_guias_tecnicas.get_children()[0])

    def limpiar_Grid(self):

        for item in self.grid_guias_tecnicas.get_children():
            self.grid_guias_tecnicas.delete(item)

    # ==================================================================================
    # ============================== ACTIVACIONES ======================================
    # ==================================================================================

    def habilitar_Btn_busquedas(self, estado):

        self.btn_buscar_movim.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_reset_buscar.configure(state=estado)
        self.entry_buscar_clave.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.btn_imprime.configure(state=estado)

    def habilitar_Btn_ABM(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)

    def habilitar_Btn_guardar_cancelar(self, estado):

        self.btn_guardaritem.configure(state=estado)
        self.btn_Cancelar.configure(state=estado)
        self.btn_foto_uno.configure(state=estado)
        self.btn_foto_dos.configure(state=estado)
        self.btn_foto_tres.configure(state=estado)
        self.btn_video_uno.configure(state=estado)
        self.btn_video_dos.configure(state=estado)
        self.btn_otros_docu.configure(state=estado)

    def habilitar_text(self, estado):

        self.entry_palabra_clave.configure(state=estado)
        self.entry_descripcion.configure(state=estado)
        self.entry_ruta.configure(state=estado)
        self.entry_foto_uno.configure(state=estado)
        self.entry_foto_dos.configure(state=estado)
        self.entry_foto_tres.configure(state=estado)
        self.entry_video_uno.configure(state=estado)
        self.entry_video_dos.configure(state=estado)
        self.entry_otros_docu.configure(state=estado)
        self.text_guia.configure(state=estado)

    def limpiar_text(self):

        self.entry_buscar_clave.delete(0, END)
        self.entry_palabra_clave.delete(0, END)
        self.entry_descripcion.delete(0, END)
        self.entry_ruta.delete(0, END)
        self.entry_foto_uno.delete(0, END)
        self.entry_foto_dos.delete(0, END)
        self.entry_foto_tres.delete(0, END)
        self.entry_video_uno.delete(0, END)
        self.entry_video_dos.delete(0, END)
        self.entry_otros_docu.delete(0, END)
        self.text_guia.delete('1.0', 'end')

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.fShowall()
            self.limpiar_text()
            self.habilitar_text("disabled")
            self.habilitar_Btn_ABM("normal")
            self.habilitar_Btn_guardar_cancelar("disabled")
            self.habilitar_Btn_busquedas("normal")
            self.grid_guias_tecnicas.focus()

            # ----------------------------------------------
            # reestablezco la imagen de videos/fotos
            self.imagen_defa = "tapiz.jpg"
            self.photoa = Image.open(os.path.join(self.carpeta_guias, self.imagen_defa))
            self.photoa = self.photoa.resize((300, 200), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)

            self.frame_quinto.forget()

            self.frame_quinto = LabelFrame(self.frame_tercero, text="", foreground="red")

            self.lbl_imagen_art = Label(self.frame_quinto, image=self.imagen_art, bg="white", relief=RIDGE, bd=5, padx=5)

            self.frame_quinto.pack(side=LEFT, fill=BOTH, expand=1, padx=5, pady=2)
            self.lbl_imagen_art.pack(expand=1, side=TOP, pady=2, padx=2)
            # ----------------------------------------------

    def fSalir(self):
        self.master.destroy()

    # =============================================================================================
    # ==================================== CRUD ===================================================
    # =============================================================================================

    def fNuevo(self):

        self.alta_modif = 1
        self.habilitar_text("normal")
        self.habilitar_Btn_ABM("disabled")
        self.habilitar_Btn_guardar_cancelar("normal")
        self.habilitar_Btn_busquedas("disabled")
        self.entry_palabra_clave.focus()

    def fEditar(self):

        self.alta_modif = 2
        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_guias_tecnicas.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_guias_tecnicas.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta
        self.habilitar_text('normal')
        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_Btn_ABM("disabled")
        self.habilitar_Btn_guardar_cancelar("normal")

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_guias_tecnicas.item(self.selected, 'values')

        self.strvar_palabra_clave.set(value=valores[0])
        self.strvar_descripcion.set(value=valores[1])
        self.strvar_ruta.set(value=valores[2])
        self.text_guia.insert(END, valores[3])
        self.strvar_foto_uno.set(value=valores[4])
        self.strvar_foto_dos.set(value=valores[5])
        self.strvar_foto_tres.set(value=valores[6])
        self.strvar_video_uno.set(value=valores[7])
        self.strvar_video_dos.set(value=valores[8])
        self.strvar_otros_docu.set(value=valores[9])
        self.entry_descripcion.focus()

    def fBorrar(self):

        # guardo item seleccionado en el grid
        self.selected = self.grid_guias_tecnicas.focus()
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_guias_tecnicas.item(self.selected, 'text')

        que_paso = self.puntabla(self.selected, "E")

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_guias_tecnicas.item(self.selected, 'values')
        # guardo clave de movimietno anterior
        data = str(self.clave) + " " + valores[2]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)

        if r == messagebox.YES:
            # Elimino de tabla planicaja
            n = self.varGuiaTecnica.eliminar_item_guia(self.clave)
            if n == 1:
                messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
                self.limpiar_Grid()
                self.llena_grilla()
            else:
                messagebox.showinfo("Eliminar", "No fue posible eliminar el Registro", parent=self)

        que_paso = self.puntabla(self.selected, "F")

    def fGuardar(self):

        if self.strvar_descripcion.get() == "" and self.strvar_palabra_clave.get() == "":
            messagebox.showerror("Error", "No hay datos", parent=self)
            self.entry_palabra_clave.focus()
            return

        aaa = 0

        if aaa == 0:

        # #try:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori --------------------------
            self.selected = self.grid_guias_tecnicas.focus()
            # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
            self.clave = self.grid_guias_tecnicas.item(self.selected, 'text')
            self.nuevo_guia = ""

            if self.alta_modif == 1:

                # INGRESO - ALTA
                self.varGuiaTecnica.insertar_guia(self.strvar_palabra_clave.get(), self.strvar_descripcion.get(),
                                                  self.strvar_ruta.get(), self.text_guia.get(1.0, 'end-1c'),
                                                  self.strvar_foto_uno.get(), self.strvar_foto_dos.get(),
                                                  self.strvar_foto_tres.get(), self.strvar_video_uno.get(),
                                                  self.strvar_video_dos.get(), self.strvar_otros_docu.get())

                messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)


            if self.alta_modif == 2:

                # MODIFICACION
                self.varGuiaTecnica.modificar_guia(self.var_Id, self.strvar_palabra_clave.get(),
                                                   self.strvar_descripcion.get(), self.strvar_ruta.get(),
                                                   self.text_guia.get(1.0, 'end-1c'),
                                                   self.strvar_foto_uno.get(), self.strvar_foto_dos.get(),
                                                   self.strvar_foto_tres.get(), self.strvar_video_uno.get(),
                                                   self.strvar_video_dos.get(), self.strvar_otros_docu.get())

                self.var_Id == -1

                messagebox.showinfo("Modificacion", "La modificacion fue exitosa", parent=self)

            # cierre de las novedades y reseteando pantalla para nuevo movimiento - actualizando grilla -------
            self.limpiar_Grid()
            self.llena_grilla()

            # ordenamiento puntero en treeview
            if self.alta_modif == 1:
                # ALTA
                self.puntabla(self.nuevo_guia, "A")
            elif self.alta_modif == 2:
                # MODIFICACION
                que_paso = self.puntabla(self.clave, "B")
            elif self.alta_modif == 0:
                messagebox.showerror("Error", "codigo de Alta_modif cero", parent=self)
                return

    # #except:

    #     messagebox.showerror("Error", "Revise Fechas", parent=self)
    #     self.entry_fecha_planilla.focus()
    #     return

        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_Btn_guardar_cancelar("disabled")
        self.habilitar_Btn_ABM("normal")
        self.habilitar_Btn_busquedas("normal")
        self.grid_guias_tecnicas.focus()

    # ================================================================================================
    # ================================= MOVIMIENTO EN TREEVIEW =======================================
    # ================================================================================================

    def fToparch(self):
        self.mover_puntero('TOP')

    def fFinarch(self):
         self.mover_puntero('END')

    def mover_puntero(self, param_topend):

        # Para ir a tope o fin de archivo -----------------------------------------------------------
        if param_topend == "":
            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_guias_tecnicas.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            clave = self.grid_guias_tecnicas.item(self.selected, 'text')

        # Si es tope de archivo ----------------------------------------------------------------------
        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_guias_tecnicas.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_guias_tecnicas.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_guias_tecnicas.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_guias_tecnicas.yview(self.grid_guias_tecnicas.index(self.grid_guias_tecnicas.get_children()[0]))

        # Si es fin de archivo -----------------------------------------------------------------------
        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_guias_tecnicas.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_guias_tecnicas.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_guias_tecnicas.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_guias_tecnicas.yview(self.grid_guias_tecnicas.index(self.grid_guias_tecnicas.get_children()[-1]))

    def puntabla(self, registro, tipo_mov):

        # metodo para posicionar el puntero en el TV luego de las distintas acciones sobre los datos

        # trae el indice de la tabla "I001"
        regis = self.grid_guias_tecnicas.get_children()
        rg = ""
        contador = 0
        # --------------------------------------------------------------------------------

        # aca traigo el codigo del registr0 (cod.cliente, cod. art.... que estoy dando de alta porque aun no tengo ID)
        # ALTA
        if tipo_mov == "A":
            for rg in regis:
                buscado = self.grid_guias_tecnicas.item(rg)['values']
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
                buscado = self.grid_guias_tecnicas.item(rg)['text']
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
                    buscado = self.grid_guias_tecnicas.item(rg)['values']
                    self.buscado2 = str(buscado[2])
                    break
                if rg == registro:  # registro seria self.selected o sea el Id de la BD
                    control = 0
        # -------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id del que obtuve antes
        # que es el que sigue al que borre
        if tipo_mov == 'F':
            for rg in regis:
                buscado = self.grid_guias_tecnicas.item(rg)['values']
                if self.buscado2 == str(buscado[2]):
                    break
        # ------------------------------------------------------------------------------------------

        # BUSCAR EN TABLA - Viene de la funcion que busca en la tabla lo que se requiere
        if tipo_mov == 'S':
            if regis != ():
                for rg in regis:
                    break
                if rg == "":
                    #self.btn_buscar_planilla.configure(state="disabled")
                    return
        # ----------------------------------------------------------------------------------------

        self.grid_guias_tecnicas.selection_set(rg)
        self.grid_guias_tecnicas.focus(rg)
        self.grid_guias_tecnicas.yview(self.grid_guias_tecnicas.index(rg))

        if rg == "":
            return False
        return True

    def fShowall(self):

        self.filtro_activo = "guias_tecnicas ORDER BY gt_clave ASC"
        self.limpiar_Grid()
        self.llena_grilla()

    def fReset_buscar(self):

        self.strvar_buscostring.set(value="")
        self.fShowall()

    # ============================================================================================
    # =================================== BUSQUEDAS ==============================================
    # ============================================================================================

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()

            self.filtro_anterior = self.filtro_activo

            self.filtro_activo = "guias_tecnicas WHERE INSTR(gt_clave, '" + se_busca + "') > 0" \
                               + " OR " + "INSTR(gt_brevedesc, '" + se_busca + "') > 0"

            self.varGuiaTecnica.buscar_entabla(self.filtro_activo)
            self.limpiar_Grid()
            self.llena_grilla()

            # funcion que acomoda el puntero en el TV
            que_paso = self.puntabla("", "S")

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

    # ===================================================================
    # ========================= FOTOS ===================================
    # ===================================================================

    def fVer_foto_uno(self):
        self.fVer_fotos("uno")

    def fVer_foto_dos(self):
        self.fVer_fotos("dos")

    def fVer_foto_tres(self):
        self.fVer_fotos("tres")

    def fVer_fotos(self, xcual):

        if xcual == "uno":
            if len(self.strvar_foto_uno.get()) == 0:
                return
            self.imagen_defa = self.strvar_foto_uno.get()
        elif xcual == "dos":
            if len(self.strvar_foto_dos.get()) == 0:
                return
            self.imagen_defa = self.strvar_foto_dos.get()
        elif xcual == "tres":
            if len(self.strvar_foto_tres.get()) == 0:
                return
            self.imagen_defa = self.strvar_foto_tres.get()

        # Verifico que exista el archivo
        if not os.path.isfile(os.path.join(self.carpeta_guias, self.imagen_defa)):
            messagebox.showerror("Error", "Archivo no existe", parent=self)
            return

        # Borro u olvido el label anterior
        self.lbl_imagen_art.forget()

        self.photoa = Image.open(os.path.join(self.carpeta_guias, self.imagen_defa))
        self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.imagen_art = ImageTk.PhotoImage(self.photoa)

        self.lbl_imagen_art = Label(self.frame_quinto, image=self.imagen_art, bg="white", relief=RIDGE, bd=5)
        self.lbl_imagen_art.pack(expand=1, side=TOP, fill=BOTH, pady=2, padx=2)
        self.lbl_imagen_art.bind("<Double-Button-1>", self.amplia_img)

    # ===================================================================
    # ========================= VIDEOS ==================================
    # ===================================================================

    def fVer_video_uno(self):
        self.fVer_Videos("uno")
    def fVer_video_dos(self):
        self.fVer_Videos("dos")
    def fVer_otros(self):
        self.fVer_otros_docu()



    def fVer_Videos(self, xcual):

        if xcual == "uno":
            if len(self.strvar_video_uno.get()) == 0:
                return
            self.imagen_defa = self.strvar_video_uno.get()
        elif xcual == "dos":
            if len(self.strvar_video_dos.get()) == 0:
                return
            self.imagen_defa = self.strvar_video_dos.get()

        control_video = (os.path.join(self.carpeta_guias, self.imagen_defa))

        self.strvar_ruta.set(value=(os.path.join(self.carpeta_guias, self.imagen_defa)))

        # print((os.path.join(self.carpeta_guias, self.imagen_defa)))

        # Verifico que exista el archivo
        if not os.path.isfile(os.path.join(self.carpeta_guias, self.imagen_defa)):
            messagebox.showerror("Error", "Archivo no existe", parent=self)
            return

        self.lbl_imagen_art.forget()

        videoplayer = TkinterVideo(self.frame_quinto, scaled=True)
        self.repro = os.path.join(self.carpeta_guias, self.imagen_defa)

        videoplayer.load(self.repro)
        videoplayer.pack(expand=True, fill="both")

        videoplayer.bind("<Double-Button-1>", self.amplia_video)
        videoplayer.play()  # play the video
#        videoplayer.forget()

    def fVer_otros_docu(self):

        if len(self.strvar_otros_docu.get()) == 0:
            return
        self.imagen_defa = self.strvar_otros_docu.get()

        self.leer = os.path.join(self.carpeta_guias, self.imagen_defa)
        os.system(self.leer)

    # =================================================================================
    # ========================= VARIACIONES IMAGENES ==================================
    # =================================================================================

    def amplia_img(self,koko):

#        if len(self.strvar_foto_uno.get()) != 0:

        # crear toplevel con imagen grande
        self.vent_img = Toplevel()
        self.vent_img.geometry('1020x900+600+50')
        self.vent_img.config(bg='white', padx=5, pady=5)
        # ayuda_top.resizable(0,0)
        self.vent_img.resizable(1, 1)
        self.vent_img.title("Imagen ampliada")
        self.photo_b = Image.open(os.path.join(self.carpeta_guias, self.imagen_defa))
        self.photo_b = self.photo_b.resize((900, 700), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.imagen_art_b = ImageTk.PhotoImage(self.photo_b)
        # muestro la imagen en el frame
        self.lbl_im_art_b = Label(self.vent_img, image=self.imagen_art_b, bg="white", relief=RIDGE, bd=5)
        self.lbl_im_art_b.pack(expand=1, side=TOP, fill=BOTH, pady=2, padx=2)
        self.vent_img.grab_set()
        self.vent_img.focus_set()
        mainloop()

    def amplia_video(self,koko):
        os.system(self.repro)

    def validar_imagen(self, verruta):

        """
        Cuando doy un alta y coloco el nombre de la imagen jpg, valido que exista en la carpeta fotos
        y ya la cargo y la muestro
        """

        # Borro u olvido el label anterior
        self.lbl_imagen_art.forget()

        if len(verruta) != 0:
            self.imagen_defa = verruta
        else:
            # self.imagen_defa = "logo1.jpg"
            return

        try:

            self.photoa = Image.open(os.path.join(self.carpeta_guias, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)

        except:

            messagebox.showerror("Error", "No existe la imagen", parent=self)

            self.imagen_defa = "logo1.jpg"

            self.photoa = Image.open(os.path.join(self.carpeta_guias, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)

            self.strvar_foto_uno.set(value="")
            self.entry_foto_uno.focus()

        # muestro la imagen en el frame
        self.lbl_imagen_art = Label(self.frame_quinto, image=self.imagen_art, bg="white", relief=RIDGE, bd=5)
        self.lbl_imagen_art.pack(expand=1, side=TOP, fill=BOTH, pady=2, padx=2)

    # =================================================================================================
    # ======================================= IMPRESION ===============================================
    # =================================================================================================

    def fImprime(self):
        pass

    #     # traigo el registro que quiero imprimir
    #     self.selected = self.grid_saldos_ctacte.focus()
    #     # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
    #     # que pone la BD automaticamente al dar el alta
    #     self.clave = self.grid_saldos_ctacte.item(self.selected, 'text')
    #
    #     # if self.clave == "":
    #     #     messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
    #     #     return
    #
    #     # Definir parametros listado
    #     """
    #     P : portrait (vertical)
    #     L : landscape (horizontal)
    #     A4 : 210x297mm
    #     """
    #
    #     # esto siempre debe estar ------------------------------------------------------------
    #     pdf = PDF(orientation='P', unit='mm', format='A4')
    #     # numero de paginas para luego usar en numeracion de pie de pagina
    #     pdf.alias_nb_pages()
    #     # Esto fuerza agregar una pagina al PDF
    #     pdf.add_page()
    #     # set de letra, tipo y tamaño
    #     pdf.set_font('Times', '', 12)
    #     # -----------------------------------------------------------------------------------
    #
    #     # armado de encabezado --------------------------------------------------------------
    #     feactual = datetime.now()
    #     feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
    #
    #     # Imprimo el encabezado de pagina ---------------------------------------------------
    #     pdf.set_font('Arial', '', 8)
    #     pdf.cell(w=0, h=5, txt='Saldos en Cuenta Corriente - Fecha y Hora: ' + feac , border=1, align='C', fill=0, ln=1)
    #     # -----------------------------------------------------------------------------------
    #
    #     # para listar una base de datos forma simple basica ---------------------------------
    #     # lista_de_datos = retorno de la base de datos
    #     # al ultimo le ponemos w=0 y abarca completo el resto del renglon hasta el final
    #
    #     pdf.cell(w=15, h=8, txt='Cliente', border=1, align='C', fill=0)
    #     pdf.cell(w=150, h=8, txt='Cliente', border=1, align='C', fill=0)
    #     pdf.multi_cell(w=0, h=8, txt='Saldo', border=1, align='C', fill=0)
    #     # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)
    #     pdf.set_font('Arial', '', 5)
    #
    #     # retorno una lista con los registros ----------------------------------------------------
    #     datos = self.varSaldoscc.consultar_saldosctacte("saldosctacte")
    #
    #     pdf.set_font('Arial', '', 11)
    #
    #     for row in datos:
    #         pdf.cell(w=15, h=6, txt=str(row[1]), border=1, align='C', fill=0)
    #         pdf.cell(w=150, h=6, txt=row[2], border=1, align='C', fill=0)
    #         #pdf.cell(w=20, h=5, txt=row[3], border=1, align='C', fill=0)
    #         #mostrar = row[4]
    #         #cadena = (mostrar[:100])
    #         pdf.multi_cell(w=0, h=6, txt=str(row[3]), border=1, align='R', fill=0)
    #
    #     pdf.output('hoja.pdf')
    #     # Abre el archivo PDF para luego, si quiero, poder imprimirlo
    #     path = 'hoja.pdf'
    #     os.system(path)

    def DobleClickGrid(self, event):
        self.fEditar()
