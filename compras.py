from compras_ABM import *
from funciones import *
from funcion_new import *
#----------------------------
#from tkinter import *
#from tkinter import ttk
from tkinter import messagebox
#import tkinter as tk
import tkinter.font as tkFont
#from tkinter.scrolledtext import *     # para campos text
#----------------------------
import os
from PDF_clase import *
from datetime import date, datetime
from PIL import Image, ImageTk

class clase_compras(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ---------------------------------------------------------------------------------
        # Instanciaciones -*-
        self.varCompras = datosCompras(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)

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
        hventana = 380
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 100
        pheight = round(htotal / 2 - hventana / 2) - 50
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # ------------------------------------------------------------------------------

        # # guarda en item el Id del elemento fila en este caso fila 0 del grid principal
        # item = self.grid_art_faltantes.identify_row(0)
        # self.grid_art_faltantes.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_art_faltantes.focus(item)

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        Otras funciones para manejar los elementos seleccionados incluyen:
        selection_add(): añade elementos a la selección.
        selection_remove(): remueve elementos de la selección.
        selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        selection_toggle(): cambia la selección de un elemento. """

    # --------------------------------------------------------------------
    #  WIDGETS
    # --------------------------------------------------------------------

    def create_widgets(self):

        # -------------------------------------------------------------------
        # TITULOS
        # -------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('comprasmay.png')
        self.photo3 = self.photo3.resize((60, 60), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_compras = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_compras = Label(self.frame_titulo_top, image=self.png_compras, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=49, text="Articulos faltantes", bg="black", fg="gold",
                                                       font=("Arial bold", 22, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_compras.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill=X, padx=5, pady=2)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # VARIABLES
        # ---------------------------------------------------------------------

        # para validar ingresos de numeros en gets numericos
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------

        una_fecha= date.today()
        self.strvar_fecha_anotado = tk.StringVar(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_articulo = tk.StringVar(value="")
        self.strvar_estado = tk.StringVar(value="")
        self.strvar_buscostring = tk.StringVar(value="")
        self.strvar_combo_estado = tk.StringVar(value="")
        self.strvar_combo_filtro = tk.StringVar(value="")

        # ---------------------------------------------------------------------
        # GRID
        # ---------------------------------------------------------------------

        self.frame_art_faltantes = LabelFrame(self.master, text="Articulos faltantes", foreground="#CD5C5C")
        self.frame_art_faltantes_uno = LabelFrame(self.frame_art_faltantes, text="", foreground="#CD5C5C")
        self.frame_art_faltantes_dos=LabelFrame(self.frame_art_faltantes, text="", foreground="#CD5C5C")
        self.frame_busqueda_art_faltantes=LabelFrame(self.frame_art_faltantes, text="", border=5, foreground="black",
                                                     background="light blue")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_art_faltantes_dos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_art_faltantes = ttk.Treeview(self.frame_art_faltantes_dos, height=4, columns=("col1", "col2", "col3"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_art_faltantes.column("#0", width=50, anchor="center", minwidth=50)
        self.grid_art_faltantes.column("col1", width=60, anchor="w", minwidth=60)
        self.grid_art_faltantes.column("col2", width=250, anchor="w", minwidth=250)
        self.grid_art_faltantes.column("col3", width=40, anchor="center", minwidth=40)

        self.grid_art_faltantes.heading("#0", text="Id", anchor="center")
        self.grid_art_faltantes.heading("col1", text="Fecha", anchor="w")
        self.grid_art_faltantes.heading("col2", text="Articulo", anchor="w")
        self.grid_art_faltantes.heading("col3", text="Estado", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_art_faltantes_dos, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_art_faltantes_dos, orient=VERTICAL)
        self.grid_art_faltantes.config(xscrollcommand=scroll_x.set)
        self.grid_art_faltantes.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_art_faltantes.xview)
        scroll_y.config(command=self.grid_art_faltantes.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_art_faltantes['selectmode'] = 'browse'
        self.grid_art_faltantes.pack(side="top", fill=BOTH, expand=1, padx=5, pady=2)

        # Botones CRUD
        self.btn_nuevo_articulo=Button(self.frame_art_faltantes_uno, text="Nuevo articulo",
                                       command=self.fNuevo_articulo, width=17, bg='blue', fg='white')
        self.btn_nuevo_articulo.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.btn_edito_articulo=Button(self.frame_art_faltantes_uno, text="Editar articulo",
                                       command=self.fEdito_articulo, width=17, bg='blue', fg='white')
        self.btn_edito_articulo.grid(row=1, column=0, padx=3, pady=3, sticky=W)
        self.btn_borro_articulo=Button(self.frame_art_faltantes_uno, text="Borrar articulo",
                                       command=self.fBorro_articulo, width=17, bg='blue', fg='white')
        self.btn_borro_articulo.grid(row=2, column=0, padx=3, pady=3, sticky=W)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_art_faltantes_uno, text="", image=self.photo4, command=self.fToparch,
                                 bg="grey", fg="white")
        self.btnToparch.grid(row=3, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_art_faltantes_uno, text="", image=self.photo5, command=self.fFinarch,
                                 bg="grey", fg="white")
        self.btnFinarch.grid(row=4, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # Buscar un articulo en Grid
        self.lbl_busqueda_compra = Label(self.frame_busqueda_art_faltantes, text="Texto a buscar: ", justify="left",
                                         bg="light blue")
        self.lbl_busqueda_compra.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_busqueda_compra = Entry(self.frame_busqueda_art_faltantes, textvariable=self.strvar_buscostring,
                                                  state='normal', width=25, justify=LEFT, bg="light blue")
        self.entry_busqueda_compra.grid(row=0, column=1, padx=5, pady=2, sticky='nsew')

        self.btn_buscar=Button(self.frame_busqueda_art_faltantes, text="Buscar", command=self.fBuscar_articulo,
                               width=11, bg='#5F9EA0', fg='white')
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_showall=Button(self.frame_busqueda_art_faltantes, text="Mostrar todo", command=self.fShowall,
                                width=11, bg='#5F9EA0', fg='white')
        self.btn_showall.grid(row=0, column=3, padx=5, pady=2, sticky=W)
        self.btn_imprime_presup=Button(self.frame_busqueda_art_faltantes, text="Imprime Compras", command=self.creopdf,
                                       width=17, bg='#5F9EF5', fg='white')
        self.btn_imprime_presup.grid(row=0, column=4, padx=2, pady=2, sticky=W)

        self.lbl_filtrar_compra = Label(self.frame_busqueda_art_faltantes, text="Filtro: ", justify="left",
                                        bg="light blue")
        self.lbl_filtrar_compra.grid(row=0, column=5, padx=5, pady=2, sticky=W)

        # Combo estado filtrado
        self.combo_filtro = ttk.Combobox(self.frame_busqueda_art_faltantes, textvariable=self.strvar_combo_filtro,
                                         state='readonly', width=15)
        self.combo_filtro['value'] = ["Pendiente", "Comprado", "Finalizado"]
        self.combo_filtro.current(0)
        self.combo_filtro.grid(row=0, column=6, padx=3, pady=3, sticky=E)
        #self.combo_estado.bind('<Tab>', lambda e: self.calcular("completo"))

        self.btn_filtro=Button(self.frame_busqueda_art_faltantes, text="Filtrar", command=self.fFiltrar,
                               width=11, bg='#5F9EA0', fg='white')
        self.btn_filtro.grid(row=0, column=7, padx=5, pady=2, sticky=W)

        # PACKS ------------------------------------------------------------------------------
        self.frame_art_faltantes_uno.pack(side=LEFT, fill=BOTH, padx=5, pady=2)
        self.frame_art_faltantes_dos.pack(side=TOP, fill=BOTH, padx=5, pady=2)
        self.frame_busqueda_art_faltantes.pack(expand=0, side="top", fill=BOTH, padx=5, pady=2)
        self.frame_art_faltantes.pack(side="top", fill=BOTH, padx=5, pady=2)
        # ------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # ENTRYS
        # ---------------------------------------------------------------------

        self.frame_ingreso_datos = LabelFrame(self.master, text="", foreground="black")

        # Fecha de Anotacion
        self.lbl_fecha = Label(self.frame_ingreso_datos, text="Fecha: ", justify=LEFT)
        self.lbl_fecha.grid(row=0, column=0, padx=3, pady=3, sticky=W)
        self.entry_fecha = Entry(self.frame_ingreso_datos, textvariable=self.strvar_fecha_anotado, width=13)
        self.entry_fecha.grid(row=0, column=1, padx=3, pady=3, sticky=E)
        self.entry_fecha.bind("<FocusOut>", self.formato_fecha)

        # Entry articulo faltante
        self.lbl_articulo = Label(self.frame_ingreso_datos, text="Articulo: ", justify=LEFT)
        self.lbl_articulo.grid(row=0, column=2, padx=3, pady=3, sticky=W)
        self.entry_articulo = Entry(self.frame_ingreso_datos, textvariable=self.strvar_articulo, width=107, justify="left")
        self.entry_articulo.grid(row=0, column=3, padx=3, pady=3, sticky=W)
        self.strvar_articulo.trace("w", lambda *args: limitador(self.strvar_articulo, 100))

        # Combo estado
        self.lbl_combo_estado = Label(self.frame_ingreso_datos, justify=LEFT, foreground="black", text="Estado")
        self.lbl_combo_estado.grid(row=0, column=4, padx=3, pady=3, sticky=W)
        self.combo_estado = ttk.Combobox(self.frame_ingreso_datos, textvariable=self.strvar_combo_estado,
                                         state='readonly', width=15)
        self.combo_estado['value'] = ["Pendiente", "Comprado", "Finalizado"]
        self.combo_estado.current(0)
        self.combo_estado.grid(row=0, column=5, padx=3, pady=3, sticky=E)

        self.frame_ingreso_datos.pack(side="top", fill=BOTH, expand=0, padx=5, pady=5)
        # ------------------------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # BOTONES
        # ---------------------------------------------------------------------

        self.frame_botones2 = LabelFrame(self.master)

        self.btn_guardar=Button(self.frame_botones2, text="Guardar articulo", command=self.fGuardar, width=60,
                                bg='Green', fg='white')
        self.btn_guardar.grid(row=0, column=0, padx=5, pady=3, sticky='nsew')

        self.btn_cancelar=Button(self.frame_botones2, text="Cancelar", command=self.fCancelar, width=60, bg='Red',
                                 fg='white')
        self.btn_cancelar.grid(row=0, column=1, padx=5, pady=3, sticky='nsew')

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((60, 40), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_botones2, text="Salir", image=self.photo3, width=130, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=2, padx=2, pady=3)

        # for widg in self.frame_botones2.winfo_children():
        #     widg.grid_configure(padx=5, pady=3, sticky='nsew')

        self.frame_botones2.pack(expand=0, side="top", fill=BOTH, pady=2, padx=5)

    # ---------------------------------------------------------------------
    # ESTADOS
    # ---------------------------------------------------------------------

    def estado_inicial(self):

        # Activo filtro inicial en resu_presup
        self.filtro_activo = "faltantes WHERE fa_estado='Pendiente' ORDER BY fa_fecha"
        self.var_Id = -1
        self.alta_modif = 0

        una_fecha = date.today()
        self.strvar_fecha_anotado.set(value=una_fecha.strftime('%d/%m/%Y'))

        self.limpiar_entrys()
        self.estado_entrys("disabled")
        self.estado_botones_dos("disabled")
        self.estado_botones_uno("normal")

    def limpiar_entrys(self):

        una_fecha = date.today()
        self.strvar_fecha_anotado.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_articulo.set(value="")
        self.combo_estado.current(0)
        self.strvar_buscostring.set(value="")

    def estado_entrys(self, estado):

        self.entry_fecha.configure(state=estado)
        self.entry_articulo.configure(state=estado)
        self.combo_estado.configure(state=estado)
        self.entry_busqueda_compra.configure(state=estado)

    def estado_botones_uno(self, estado):

        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.btn_nuevo_articulo.configure(state=estado)
        self.btn_edito_articulo.configure(state=estado)
        self.btn_borro_articulo.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_buscar.configure(state=estado)
        self.entry_busqueda_compra.configure(state=estado)

    def estado_botones_dos(self, estado):

        self.btn_guardar.configure(state=estado)

    # ---------------------------------------------------------------------
    # GRID
    # ---------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_art_faltantes.get_children():
            self.grid_art_faltantes.delete(item)

    def llena_grilla(self, ult_tabla_id):

        datos = self.varCompras.consultar_compras(self.filtro_activo)

        for row in datos:
            self.grid_art_faltantes.insert("", END, text=row[0], values=(row[1], row[2], row[3]))

        if len(self.grid_art_faltantes.get_children()) > 0:
               self.grid_art_faltantes.selection_set(self.grid_art_faltantes.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_art_faltantes.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_art_faltantes.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
                de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

            self.grid_art_faltantes.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_art_faltantes.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_art_faltantes.yview(self.grid_art_faltantes.index(rg))
        else:
            # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
            self.mover_puntero_topend("END")

    # ---------------------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------------------

    def fNuevo_articulo(self):

        self.alta_modif = 1
        self.estado_entrys("normal")
        self.estado_botones_dos("normal")
        self.estado_botones_uno("disabled")
        self.entry_fecha.focus()

    def fEdito_articulo(self):

        self.selected = self.grid_art_faltantes.focus()
        self.clave = self.grid_art_faltantes.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.estado_entrys("normal")
        self.estado_botones_dos("normal")
        self.estado_botones_uno("disabled")

        self.entry_articulo.focus()

        self.var_Id = self.clave  #puede traer -1 , en ese caso seria un alta
        self.alta_modif = 2

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_art_faltantes.item(self.selected, 'values')

        una_fecha = datetime.strptime(valores[0], '%Y-%m-%d')
        self.strvar_fecha_anotado.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_articulo.set(value=valores[1])
        self.strvar_combo_estado.set(value=valores[2])

    def fBorro_articulo(self):

        # -----------------------------------------------------------------------------
        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_art_faltantes.focus()
        self.selected_ant = self.grid_art_faltantes.prev(self.selected)
        # guardo en clave el Id pero de la tabla (no son el mismo con el treeview)
        self.clave = self.grid_art_faltantes.item(self.selected, 'text')
        self.clave_ant = self.grid_art_faltantes.item(self.selected_ant, 'text')
        # -----------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_art_faltantes.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar articulo?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        # Metodo que ellimina el registro
        self.varCompras.eliminar_articulo(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # VALIDACIONES

        # 1- que articulo no este vacio
        if len(self.strvar_articulo.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de articulo", parent=self)
            self.entry_articulo.focus()
            return

        # Asi obtengo el Id del Grid (Treeview) de donde esta el foco (I006...I002...)
        self.selected = self.grid_art_faltantes.focus()
        # Asi obtengo la clave de la tabla (campo Id de la tabla - numero secuencial) que no es lo mismo que el del Treeview
        self.clave = self.grid_art_faltantes.item(self.selected, 'text')

        if self.alta_modif == 1:

            self.varCompras.insertar_registro(self.strvar_fecha_anotado.get(), self.strvar_articulo.get(),
            self.strvar_combo_estado.get())

            messagebox.showinfo("Guardar", "Nuevo registro creado correctamente", parent=self)

        elif self.alta_modif == 2:

            self.varCompras.modificar_registro(self.var_Id, self.strvar_fecha_anotado.get(),
            self.strvar_articulo.get(), self.strvar_combo_estado.get())

            self.var_Id == -1
            messagebox.showinfo("Modificacion", "Modificacion de registro exitosa", parent=self)

        self.limpiar_Grid()
        #self.llena_grilla(self.clave)
        self.limpiar_entrys()
        self.estado_entrys("disabled")
        self.estado_botones_uno("normal")
        self.estado_botones_dos("disabled")

        if self.alta_modif == 1:
            ultimo_tabla_id = self.varCompras.traer_ultimo(0)
            self.llena_grilla(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla(self.clave)

        self.alta_modif = 0

    # ---------------------------------------------------------------------
    # BOTONES DE ACCIONES
    # ---------------------------------------------------------------------

    def fSalir(self):

        r = messagebox.askquestion("Salir", "Confirma salir del modulo?", parent=self)
        if r == messagebox.NO:
            return
        self.master.destroy()

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys()
        self.estado_inicial()

    # ---------------------------------------------------------------------
    # PUNTEROS MANEJO
    # ---------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_art_faltantes.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return

            # selecciono el Id primero de la lista en este caso
            self.grid_art_faltantes.selection_set(rg)
            # pone el primero Id
            self.grid_art_faltantes.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_art_faltantes.yview(self.grid_art_faltantes.index(self.grid_art_faltantes.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_art_faltantes.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_art_faltantes.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_art_faltantes.focus(rg)
            # lleva el foco al final del treeview
            self.grid_art_faltantes.yview(self.grid_art_faltantes.index(self.grid_art_faltantes.get_children()[-1]))

    def fShowall(self):

        self.selected = self.grid_art_faltantes.focus()
        self.clave = self.grid_art_faltantes.item(self.selected, 'text')
        self.filtro_activo = "faltantes ORDER BY fa_fecha"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    def fBuscar_articulo(self):

        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()
            self.filtro_activo = "faltantes WHERE INSTR(fa_articulo, '" + se_busca + "') ORDER BY fa_fecha ASC"

            # self.filtro_activo = "resu_ventas WHERE INSTR(rv_cliente, '" + se_busca + "') > 0" \
            #                      + " OR " + "INSTR(nombres, '" + se_busca + "') > 0" \
            #                      + " ORDER BY apellido ASC"

            self.varCompras.buscar_entabla(self.filtro_activo)
            self.limpiar_Grid()
            self.llena_grilla("")

            """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
            item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
            item = self.grid_art_faltantes.selection()
            self.grid_art_faltantes.focus(item)

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_anotado.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_anotado.get())

        if retorno_VerFal == "":
            self.strvar_fecha_anotado.set(value=estado_antes)
            self.entry_fecha.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_anotado.set(value=estado_antes)
            self.entry_fecha.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_anotado.set(value=retorno_VerFal)
        return ("bien")

#     def puntabla(self, registro, tipo_mov):
#
#         # metodo para posicionar el puntero en el TV luego de las distintas acciones sobre los datos
#
#         # trae el indice de la tabla "I001", "I002", ......
#         regis = self.grid_art_faltantes.get_children()
#         rg = ""
#         contador = 0
#         # -----------------------------------------------------------------------------------------------------
#
#         # ALTA ------------------------------------------------------------------------------------------------
#         # aca traigo el codigo del registr0 (cod.cliente, cod. art.... que estoy dando de alta porque aun no tengo ID)
#         # ALTA
#         if tipo_mov == "A":
#             # barro regis que son las Id de cada linea del Treeview
#             for rg in regis:
#                 # guardo en buscado cada uno de los valores de esa linea
#                 buscado = self.grid_art_faltantes.item(rg)['values']
#                 # en este caso pregunto si el valor 1 es igual al string que pase como parametro en registro
#                 if str(buscado[1]) == registro:
#                     # si son iguales salgo y devuelvo en "rg" el Id que tiene el nuevo registro del treeview
#                     break
#         # ----------------------------------------------------------------------------------------------------
#
#         # MODIFICACION ---------------------------------------------------------------------------------------
#         # Aca es para acomodar el puntero cuando el registro si existe en la tabla, entonces puedo usar el ID
#         if tipo_mov == "B":
#             for rg in regis:
#                 # En buscado guardo el Id de la tabla (base datos) del que estoy posicionado
#                 buscado = self.grid_art_faltantes.item(rg)['text']
#
#                 # en registro viene "clave" que es el Id del que estoy parado y lo paso a la funcion como parametro
#                 contador += 1
#                 # busco el ID de la tabla con el que guarde antes en "clave" - aca busco un Id de la tabla
#                 # a registro se le paso el Id de la tabla (es distinto la busqueda a ALTA)
#                 if buscado == registro:
#                     break
#         # -----------------------------------------------------------------------------------------------------
#
#         # -----------------------------------------------------------------------------------------------------
#         # BORRAR REGISTRO PARTE 1 -es la parte donde tomo el Id del registro que le sigue al que voy a eliminar
#         if tipo_mov == 'E':
#             control = 1
#             lista = [""]
#             self.buscado2 = ""
#             for rg in regis:
#                 contador += 1
#                 lista.append(rg)
#                 if control == 0:
#                     # guardo Id del que sigue
#                     buscado = self.grid_art_faltantes.item(rg)['values']
#                     self.buscado2 = str(buscado[1])
#
#                     # ---------------------------------------------------------------------------------------
#                     # esto agregue para que no se me mueva el puntero al posterior registro del treeview
#                     xxx = len(lista) - 2
#                     x_rg = lista[xxx]
#
#                     self.grid_art_faltantes.selection_set(x_rg)
#                     self.grid_art_faltantes.focus(x_rg)
#                     self.grid_art_faltantes.yview(self.grid_art_faltantes.index(x_rg))
#
#                     if rg == "":
#                         return False
#                     return True
#
# #                    break
#
#                 if rg == registro:  # registro seria self.selected o sea el Id de la BD
#                     control = 0
#         # -------------------------------------------------------------------------------------------
#
#         # -------------------------------------------------------------------------------------------
#         # BORRAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id del que obtuve antes
#         # que es el que sigue al que borre
#         if tipo_mov == 'F':
#             for rg in regis:
#                 buscado = self.grid_art_faltantes.item(rg)['values']
#                 if self.buscado2 == str(buscado[1]):
#                     break
#         # ------------------------------------------------------------------------------------------
#
#         # ------------------------------------------------------------------------------------------
#         # BUSCAR EN TABLA - Viene de la funcion que busca en la tabla lo que se requiere
#         if tipo_mov == 'S':
#             if regis != ():
#                 for rg in regis:
#                     break
#                 if rg == "":
#                     #self.btn_buscar_cliente.configure(state="disabled")
#                     return
#         # ----------------------------------------------------------------------------------------
#
#         # ----------------------------------------------------------------------------------------
#         # vuelven los punteros del treeview con el valor Id encontrado en las busquedas anteriores
#         self.grid_art_faltantes.selection_set(rg)
#         self.grid_art_faltantes.focus(rg)
#         self.grid_art_faltantes.yview(self.grid_art_faltantes.index(rg))
#
#         if rg == "":
#             return False
#         return True
#         # ---------------------------------------------------------------------------------------------

    # ===================================================
    # INFORMES
    # ===================================================

    def creopdf(self):

        # traigo el registro que quiero imprimir
        self.selected = self.grid_art_faltantes.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_art_faltantes.item(self.selected, 'text')

        # ==================================================================================
        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """
        # esto siempre debe estar ----------------------------------------------------------
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 12)
        # ----------------------------------------------------------------------------------
        # ==================================================================================

        # Cargo la linea del treeview de resu_presu ---------------------------------------
#        valores = self.grid_art_faltantes.item(self.selected, 'values')

        # armado de encabezado ------------------------------------------------------------
        sdf = date.today()          #,todatetime.strptime(valores[1], '%Y-%m-%d')
        feac = sdf.strftime('%d-%m-%Y')
        self.titulo = "Articulos pendientes de reposicion"
        # self.pdf_numero_presupuesto = valores[0]
        # self.pdf_nombre_cliente = valores[2]
        # self.pdf_dolar_presupuesto = valores[3]
        # self.pdf_tasa_ganancia = valores[4]

        self.pdf_datos_encabezado = feac+' '+self.titulo
        # Imprimo el encabezado de pagina
        pdf.set_font('Arial', '', 8)
        # pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        # pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt=self.pdf_datos_encabezado, border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.cell(w=20, h=5, txt="Fecha", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=140, h=5, txt="Articulo", border=1, align='L', fill=0, ln=0)
        # pdf.cell(w=30, h=5, txt="Estado", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Neto Dolar", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Bruto pesos", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Final", border=1, align='R', fill=0, ln=0)
        pdf.multi_cell(w=0, h=5, txt="Estado", border=1, align='L', fill=0)
        pdf.cell(w=0, h=5, txt="", border=0, align='L', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items = self.varCompras.consultar_compras(self.filtro_activo)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 8)
        for row in self.items:

            fecha_conver = datetime.strftime(row[1], '%d-%m-%Y')
            pdf.cell(w=20, h=5, txt=fecha_conver, border=0, align='R', fill=0, ln=0)
            pdf.cell(w=140, h=5, txt=row[2], border=0, align='L', fill=0, ln=0)
            # pdf.cell(w=10, h=5, txt=str(row[2]), border=0, align='R', fill=0, ln=0)
            # pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
            # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(neto_dolar_pesos, 2))), border=0, align='R', fill=0, ln=0)
            # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
            pdf.multi_cell(w=0, h=5, txt=str(row[3]), border=0, align='L', fill=0)
            #pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        pdf.output('hoja.pdf')

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    def fFiltrar(self):

        self.filtro_activo = "faltantes WHERE fa_estado = '" + self.strvar_combo_filtro.get() + "' ORDER BY fa_fecha"
        self.limpiar_Grid()
        self.llena_grilla("")
