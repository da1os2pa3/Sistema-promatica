import os
from funciones import *
from inf_tecnicos_ABM import *
#import tkinter as tk
from datetime import date, datetime
#from tkinter import messagebox
from tkinter.scrolledtext import *
from tktooltip import ToolTip
from PIL import Image, ImageTk
from PDF_clase import *

class clase_inf_tecnicos(Frame):


    def __init__(self, master=None):
        super().__init__(master, width=880, height=810)
        self.master = master

        # Instanciaciones -----------------------------------------------------------------
        # Creo instancia de la clase ABM y la paso pantalla master
        self.var_inf_tecnicos = clase_inf_tecnicos_ABM(self.master)
        # ---------------------------------------------------------------------------------

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
        hventana = 560
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.filtro_activo = ""

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_informes_tecnicos.identify_row(0)
        # self.grid_informes_tecnicos.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_informes_tecnicos.focus(item)
        # self.estado_inicial("disabled")

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. """

    # ==================================================================================================
    # ========================================== WIDGETS ===============================================
    # ==================================================================================================

    def create_widgets(self):

        # En este modulo no se usa
        # # validar: funcion en funciones.py que valida que lo ingresado sea un numeo o "-" o "."
        # self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ---------------------------------------------------------------
        # TITULOS

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('inf_tecnico.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ctacte = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_ctacte = Label(self.frame_titulo_top, image=self.png_ctacte, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Informes tècnicos",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ctacte.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)
        # --------------------------------------------------------------------------

        # --------------------------------------------------------------------------
        # STRINGVARS
        # --------------------------------------------------------------------------

        self.strvar_fecha = tk.StringVar(value="")
        self.strvar_usuario = tk.StringVar(value="")
        self.strvar_dni = tk.StringVar(value="")
        self.strvar_numdoc = tk.StringVar(value="")
        self.strvar_equipo = tk.StringVar(value="")
        self.strvar_modelo = tk.StringVar(value="")
        self.strvar_serie = tk.StringVar(value="")
        self.strvar_diagnostico = tk.StringVar(value="")
        self.strvar_provocado = tk.StringVar(value="")

        # --------------------------------------------------------------------------
        # BUSCAR
        # --------------------------------------------------------------------------

        # LABELFRAME DEL TREEVIEW
        self.frame_treeview=LabelFrame(self.master, text="", foreground="#CF09BD")

        # FRAME dentro del frame principal para poner la linea de busqueda
        self.frame_buscar = LabelFrame(self.frame_treeview)

        # BUSCAR Linea de label y entry de busqueda
        self.lbl_buscar_informe = Label(self.frame_buscar, text="Buscar informe (cliente): ")
        self.lbl_buscar_informe.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_informe=Entry(self.frame_buscar, width=50)
        self.entry_buscar_informe.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.btn_buscar_informe = Button(self.frame_buscar, text="Buscar", command=self.fBuscar_en_tabla,
                                         bg="CadetBlue", fg="white", width=27)
        self.btn_buscar_informe.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.btn_mostrar_todo = Button(self.frame_buscar, text="Mostrar todo", command=self.fShowall, bg="CadetBlue",
                                       fg="white", width=27)
        self.btn_mostrar_todo.grid(row=0, column=3, padx=5, pady=2, sticky=W)

        # --------------------------------------------------------------------------
        # TREVIEEW
        # --------------------------------------------------------------------------

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_treeview)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_informes_tecnicos = ttk.Treeview(self.frame_treeview, height=5, columns=("col1", "col2", "col3",
                                                                            "col4", "col5", "col6", "col7", "col8"))

        self.grid_informes_tecnicos.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_informes_tecnicos.column("#0", width=50, anchor="center", minwidth=50)
        self.grid_informes_tecnicos.column("col1", width=80, anchor="center", minwidth=50)
        self.grid_informes_tecnicos.column("col2", width=250, anchor="center", minwidth=200)
        self.grid_informes_tecnicos.column("col3", width=100, anchor="center", minwidth=80)
        self.grid_informes_tecnicos.column("col4", width=80, anchor="center", minwidth=80)
        self.grid_informes_tecnicos.column("col5", width=250, anchor="center", minwidth=80)
        self.grid_informes_tecnicos.column("col6", width=200, anchor="center", minwidth=80)
        self.grid_informes_tecnicos.column("col7", width=100, anchor="center", minwidth=80)

        self.grid_informes_tecnicos.heading("#0", text="Id", anchor="center")
        self.grid_informes_tecnicos.heading("col1", text="Fecha", anchor="center")
        self.grid_informes_tecnicos.heading("col2", text="Cliente", anchor="center")
        self.grid_informes_tecnicos.heading("col3", text="Tipo Doc.", anchor="center")
        self.grid_informes_tecnicos.heading("col4", text="Nº Doc.", anchor="center")
        self.grid_informes_tecnicos.heading("col5", text="Equipo", anchor="center")
        self.grid_informes_tecnicos.heading("col6", text="Modelo", anchor="center")
        self.grid_informes_tecnicos.heading("col7", text="Serie", anchor="center")

        self.grid_informes_tecnicos.tag_configure('oddrow', background='light grey')
        self.grid_informes_tecnicos.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_treeview, orient="horizontal")
        scroll_y = Scrollbar(self.frame_treeview, orient="vertical")
        self.grid_informes_tecnicos.config(xscrollcommand=scroll_x.set)
        self.grid_informes_tecnicos.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_informes_tecnicos.xview)
        scroll_y.config(command=self.grid_informes_tecnicos.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_informes_tecnicos['selectmode'] = 'browse'

        self.frame_buscar.pack(side="top", fill="both", expand=1, padx=1, pady=3)
        self.grid_informes_tecnicos.pack(side="top", fill="both", expand=1, padx=5, pady=2)
        self.frame_treeview.pack(side="top", fill="both", padx=5, pady=2)

        # --------------------------------------------------------------------------
        # BOTONES DEL TREEVIEW
        # --------------------------------------------------------------------------
        self.frame_botones_grid=LabelFrame(self.master, text="", foreground="red")
        self.botones_tv()
        self.frame_botones_grid.pack(side="top", fill="both", expand=0, padx=2, pady=2)

        # --------------------------------------------------------------------------
        # ENTRYS
        # --------------------------------------------------------------------------
        self.frame_dos=LabelFrame(self.master, text="", foreground="red")
        self.entrys()
        self.frame_tres.pack(side="top", fill="both", expand=0, padx=5, pady=5)

    # --------------------------------------------------------------------------
    # METODOS
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ESTADOS
    # --------------------------------------------------------------------------

    def estado_inicial(self):

        self.var_Id = -1
        self.alta_modif = 0
        self.filtro_activo = "inf_tecnicos ORDER BY it_fecha ASC"

        self.limpiar_text()
        self.estado_botones("normal")
        self.habilitar_text("disabled")

    def habilitar_text(self, estado):

        self.entry_fecha.configure(state=estado)
        self.entry_usuario.configure(state=estado)
        self.entry_numdoc.configure(state=estado)
        self.combo_tipo_dni.configure(state=estado)
        self.entry_equipo.configure(state=estado)
        self.entry_modelo.configure(state=estado)
        self.entry_serie.configure(state=estado)
        self.entry_diagnostico.configure(state=estado)
        self.entry_provocado.configure(state=estado)
        self.text_descripcion.configure(state=estado)

        self.btn_guardar.configure(state=estado)
        self.btn_genero_informe.configure(state=estado)
        self.grid_informes_tecnicos['selectmode'] = 'browse'

    def estado_botones(self, estado):

        self.btn_nuevo.configure(state=estado)
        self.btn_borrar.configure(state=estado)
        self.btn_editar.configure(state=estado)
        self.btn_imprime.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)

        self.grid_informes_tecnicos['selectmode'] = 'none'

    def limpiar_text(self):

        self.strvar_fecha.set(value="")
        self.strvar_usuario.set(value="")
        self.combo_tipo_dni.set("")
        self.strvar_numdoc.set(value="")
        self.strvar_equipo.set(value="")
        self.strvar_modelo.set(value="")
        self.strvar_serie.set(value="")
        self.strvar_diagnostico.set(value="")
        self.strvar_provocado.set(value="")
        self.text_descripcion.delete('1.0', 'end')

    # --------------------------------------------------------------------------
    # GRILLA
    # --------------------------------------------------------------------------

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) <= 0:
            messagebox.showwarning("Aviso", "No hay un Orden para la tabla - filtro_activo - "
                                            "El programa continua", parent=self)

        datos = self.var_inf_tecnicos.consultar_inf_tecnicos(self.filtro_activo)

        cont=0
        for row in datos:

            cont+=1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_informes_tecnicos.insert("", "end", tags=color, text=row[0], values=(row[1], row[2],
                                                                                        row[3], row[4], row[5], row[6],
                                                                                        row[7], row[8]))

        if len(self.grid_informes_tecnicos.get_children()) > 0:
            self.grid_informes_tecnicos.selection_set(self.grid_informes_tecnicos.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)"""

        if ult_tabla_id:

            """ Si NO es blanco - 
                regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_informes_tecnicos.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_informes_tecnicos.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_informes_tecnicos.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_informes_tecnicos.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_informes_tecnicos.yview(self.grid_informes_tecnicos.index(rg))
        else:
            # En caso de que el parametro sea "" muevo el puntero al final del GRID
            self.muevo_puntero_topend("END")

    def limpiar_Grid(self):

        for item in self.grid_informes_tecnicos.get_children():
            self.grid_informes_tecnicos.delete(item)

    # --------------------------------------------------------------------------
    # PUNTEROS
    # --------------------------------------------------------------------------

    def fToparch(self):
        self.muevo_puntero_topend('TOP')

    def fFinarch(self):
        self.muevo_puntero_topend('END')

    def muevo_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_informes_tecnicos.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_informes_tecnicos.selection_set(rg)
            # pone el primero Id
            self.grid_informes_tecnicos.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_informes_tecnicos.yview(self.grid_informes_tecnicos.index(self.grid_informes_tecnicos.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_informes_tecnicos.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_informes_tecnicos.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_informes_tecnicos.focus(rg)
            # lleva el foco al final del treeview
            self.grid_informes_tecnicos.yview(self.grid_informes_tecnicos.index(self.grid_informes_tecnicos.get_children()[-1]))

    # --------------------------------------------------------------------------
    # CRUD
    # --------------------------------------------------------------------------

    def fSalir(self):
        self.master.destroy()

    def fCancelar(self):
        self.limpiar_text()
        self.estado_botones("normal")
        self.habilitar_text("disabled")

    def DobleClickGrid(self, event):
        self.fEditar()

    def fNuevo(self):

        self.estado_botones("disabled")
        self.habilitar_text("normal")
        self.limpiar_text()
        self.alta_modif = 1

        # Fecha y hora de ingreso
        una_fecha = datetime.now()
        self.fecha = una_fecha.strftime("%d/%m/%Y")
        self.strvar_fecha.set(self.fecha)
        self.entry_usuario.focus()

    def fEditar(self):

        self.selected = self.grid_informes_tecnicos.focus()
        self.clave = self.grid_informes_tecnicos.item(self.selected, 'text')

        if not self.clave:
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self.master)
            return

        self.alta_modif = 2
        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        self.habilitar_text("normal")
        self.limpiar_text()
        self.estado_botones("disabled")

        # aplico el filtro sobre el registro que quiero
        self.filtro_activo = "inf_tecnicos WHERE Id = " + str(self.clave)

        #self.grid_informes_tecnicos.configure(selectmode="none")

        # traigo los valores directamente desde la tabla y no del treeview - solo el registro requerido
        campos = self.var_inf_tecnicos.consultar_edicion(self.filtro_activo)

        # convierto fecha de date a string y cambio a visualizacion español
        fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(campos[1], "%Y-%m-%d"), "hora_no")
        self.entry_fecha.delete(0, END)
        self.entry_fecha.insert(0, fecha_convertida)
        self.strvar_usuario.set(value=campos[2])
        self.combo_tipo_dni.insert(0, campos[3])
        self.strvar_numdoc.set(value=campos[4])
        self.strvar_equipo.set(value=campos[5])
        self.strvar_modelo.set(value=campos[6])
        self.strvar_serie.set(value=campos[7])
        self.strvar_diagnostico.set(value=campos[8])
        self.strvar_provocado.set(value=campos[9])
        self.text_descripcion.insert(END, campos[10])

        self.entry_usuario.focus()

    def fBorrar(self):

        self.selected = self.grid_informes_tecnicos.focus()
        self.selected_ant = self.grid_informes_tecnicos.prev(self.selected)
        self.clave = self.grid_informes_tecnicos.item(self.selected, 'text')
        self.clave_ant = self.grid_informes_tecnicos.item(self.selected_ant, 'text')

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_informes_tecnicos.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[1]+" "+valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar registro?\n " + data, parent=self)

        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        self.var_inf_tecnicos.eliminar_informe(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # VALIDACION QUE EXISTA Cliente y equipo declarado
        if self.strvar_usuario.get() == "":
            messagebox.showwarning("Alerta", "Ingrese nombre/s", parent=self)
            self.entry_usuario.focus()
            self.filtro_activo = "inf_tecnicos ORDER BY it_fecha"
            return

        if self.strvar_equipo.get() == "":
            messagebox.showwarning("Alerta", "Ingrese equipo", parent=self)
            self.entry_equipo.focus()
            self.filtro_activo = "inf_tecnicos ORDER BY it_fecha"
            return

        #try:
        aaa = 0
        if aaa==0:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori
            self.selected = self.grid_informes_tecnicos.focus()
            # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
            self.clave = self.grid_informes_tecnicos.item(self.selected, 'text')

            if self.alta_modif == 1:

                self.var_inf_tecnicos.insertar_informe(self.strvar_fecha.get(), self.strvar_usuario.get(),
                self.strvar_dni.get(), self.strvar_numdoc.get(), self.strvar_equipo.get(), self.strvar_modelo.get(),
                self.strvar_serie.get(), self.strvar_diagnostico.get(), self.strvar_provocado.get(),
                self.text_descripcion.get(1.0, 'end-1c'))

                messagebox.showinfo("Guardar", "Nuevo registro creado correctamente", parent=self)

            elif self.alta_modif == 2:

                self.var_inf_tecnicos.modificar_informe(self.var_Id, self.strvar_fecha.get(),
                self.strvar_usuario.get(), self.strvar_dni.get(), self.strvar_numdoc.get(),
                self.strvar_equipo.get(), self.strvar_modelo.get(), self.strvar_serie.get(),
                self.strvar_diagnostico.get(), self.strvar_provocado.get(),
                self.text_descripcion.get(1.0, 'end-1c'))

                self.var_Id == -1
                messagebox.showinfo("Modificacion", "La modificacion del registro fue exitosa", parent=self)

            self.limpiar_Grid()
            self.limpiar_text()
            self.estado_botones("normal")
            self.habilitar_text("disabled")

            self.filtro_activo = "inf_tecnicos ORDER BY it_fecha"

            if self.alta_modif == 1:
                ultimo_tabla_id = self.var_inf_tecnicos.traer_ultimo(0)
                self.llena_grilla(ultimo_tabla_id)
            elif self.alta_modif == 2:
                self.llena_grilla(self.clave)

            self.alta_modif = 0

        #except:
        else:

            messagebox.showerror("Error", "Revise datos ingresados por favor", parent=self)
            self.entry_usuario.focus()
            return

    # --------------------------------------------------------------------------
    # BUSCAR - MOSTRAR
    # --------------------------------------------------------------------------

    def fBuscar_en_tabla(self):

        # Buscar en el TREVIEW
        if len(self.entry_buscar_informe.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.entry_buscar_informe.get()

        self.filtro_activo = "inf_tecnicos WHERE INSTR(it_usuario, '" + se_busca + "') > 0"  + " ORDER BY it_usuario"

        self.var_inf_tecnicos.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_informes_tecnicos.selection()
        self.grid_informes_tecnicos.focus(item)

    def fShowall(self):

        self.selected = self.grid_informes_tecnicos.focus()
        self.clave = self.grid_informes_tecnicos.item(self.selected, 'text')
        self.filtro_activo = "inf_tecnicos ORDER BY it_usuario"
        self.limpiar_Grid()
        self.llena_grilla(self.clave)

    # --------------------------------------------------------------------------
    # INFORMES
    # --------------------------------------------------------------------------

    def fGenero_informe(self):

        self.text_descripcion.delete('1.0', 'end')

        self.text_descripcion.insert(END,f"De acuerdo a lo solicitado por el señor/a {self.strvar_usuario.get()} "
                                     f"{self.strvar_dni.get()} - Nº: {self.strvar_numdoc.get()}, "
                                     f"se extiende el presente informe tècnico sobre la revisiòn del siguiente "
                                     f"equipo: {self.strvar_equipo.get()} Modelo {self.strvar_modelo.get()} Nº de "
                                     f"serie{self.strvar_serie.get()} Una vez revisado/a, se constata que el mismo "
                                     f"presenta las siguientes fallas: {self.strvar_diagnostico.get()}. Se estima que "
                                     f"los daños fueron provocados por {self.strvar_provocado.get()}. Se extiende este "
                                     f"informe para ser presentado ante quien corresponda.")

    def fImprime(self):

        self.selected = self.grid_informes_tecnicos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_informes_tecnicos.item(self.selected, 'text')

        # traigo el registro que quiero imprimir - aplico el filtro sobre el registro que quiero (UNO SOLO)
        self.filtro_activo = "inf_tecnicos WHERE Id = " + str(self.clave)

        # traigo los valores directamente desde la tabla y no del treeview - solo el registro requerido
        campos = self.var_inf_tecnicos.consultar_edicion(self.filtro_activo)
        feac = campos[1].strftime("%d-%m-%Y")

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

        self.pdf_fecha = feac
        self.pdf_usuario = campos[2]
        self.pdf_tipodoc = campos[3]
        self.pdf_numdoc = campos[4]
        self.pdf_equipo = campos[5]
        self.pdf_modelo = campos[6]
        self.pdf_serie = campos[7]
        self.pdf_diagnostico = campos[8]
        self.pdf_provocado = campos[9]
        self.pdf_informe = campos[10]

        # Imprimo el encabezado de pagina ---------------------------------------------------
        pdf.set_font('Arial', 'b', 14)
        pdf.cell(w=0, h=5, txt='Informe Tecnico', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0, h=5, txt='Villa Carlos Paz, ' + feac , border=0, align='L', fill=0, ln=1)
        # -----------------------------------------------------------------------------------

        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Informe: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_informe, align='L', fill=0)
        pdf.cell(w=0, h=15, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Promatica computaciòn', border=0, align='R', fill=0, ln=1)

        self.filtro_activo = "inf_tecnicos ORDER BY it_fecha"

        pdf.output('hoja.pdf')
        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    # --------------------------------------------------------------------------
    # VARIAS
    # --------------------------------------------------------------------------

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha.get())

        una_fecha = date.today()

        if retorno_VerFal == "":
            # Retorno con error
            self.strvar_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.entry_fecha.focus()
            return "error"
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.entry_fecha.focus()
            return "bien"
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.entry_fecha.focus()
            return "error"
        elif retorno_VerFal == "BLANCO":
            return "bien"
        else:
            self.strvar_fecha.set(retorno_VerFal)
            return "bien"

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta el :5 limitas la cantidad d caracteres
            entry_text.set(entry_text.get()[:caract])

    # --------------------------------------------------------------------------
    # BLOQUES BOTONES - ENTRYS
    # --------------------------------------------------------------------------

    def botones_tv(self):

        # plantilla de columnas
        for c in range(5):
            self.frame_botones_grid.grid_columnconfigure(c, weight=5, minsize=110)

        # Columnas 7 y 8 (más chicas)
        self.frame_botones_grid.grid_columnconfigure(5, weight=1, minsize=50)
        self.frame_botones_grid.grid_columnconfigure(6, weight=1, minsize=50)
        self.frame_botones_grid.grid_columnconfigure(7, weight=1, minsize=50)
        self.frame_botones_grid.grid_columnconfigure(8, weight=1, minsize=50)

        # Nuevo informe
        img = Image.open("archivo-nuevo.png").resize((20, 20))
        icono = ImageTk.PhotoImage(img)
        self.btn_nuevo = Button(self.frame_botones_grid, text="Nuevo Informe", command=self.fNuevo, width=16, bg="blue",
                                fg="white", compound="left")
        self.btn_nuevo.grid(row=0, column=0, padx=4, pady=2, sticky="nsew")
        self.btn_nuevo.image = icono
        self.btn_nuevo.config(image=icono)
        ToolTip(self.btn_nuevo, msg="Ingresar un nuevo Informe")

        # Editar un informe
        img = Image.open("editar.png").resize((20, 20))
        icono = ImageTk.PhotoImage(img)
        self.btn_editar = Button(self.frame_botones_grid, text="Edita Informe", command=self.fEditar, width=16,
                                 bg="blue", fg="white", compound="left")
        self.btn_editar.grid(row=0, column=1, padx=4, pady=2, sticky="nsew")
        self.btn_editar.image = icono
        self.btn_editar.config(image=icono)
        ToolTip(self.btn_editar, msg="Modificar un Informe")

        # Eliminar un informe
        img = Image.open("eliminar.png").resize((20, 20))
        icono = ImageTk.PhotoImage(img)
        self.btn_borrar = Button(self.frame_botones_grid, text="Eliminar Informe", command=self.fBorrar, width=16,
                                 bg="red", fg="white", compound="left")
        self.btn_borrar.grid(row=0, column=2, padx=4, pady=2, sticky="nsew")
        self.btn_borrar.image = icono
        self.btn_borrar.config(image=icono)
        ToolTip(self.btn_borrar, msg="Elimina un Informe")

        # Guardar Informe
        img = Image.open("guardar.png").resize((20, 20))
        icono = ImageTk.PhotoImage(img)
        self.btn_guardar = Button(self.frame_botones_grid, text="Guardar Informe", command=self.fGuardar, width=16,
                                  bg="green", fg="white", compound="left")
        self.btn_guardar.grid(row=0, column=3, padx=4, pady=2, sticky="nsew")
        self.btn_guardar.image = icono
        self.btn_guardar.config(image=icono)
        ToolTip(self.btn_guardar, msg="Guarda el informe")

        # Cancelar
        img = Image.open("cancelar.png").resize((20, 20))
        icono = ImageTk.PhotoImage(img)
        self.btn_Cancelar = Button(self.frame_botones_grid, text="Cancelar", command=self.fCancelar, width=16,
                                   bg="black", fg="white", compound="left")
        self.btn_Cancelar.grid(row=0, column=4, padx=4, pady=2, sticky="nsew")
        self.btn_Cancelar.image = icono
        self.btn_Cancelar.config(image=icono)
        ToolTip(self.btn_Cancelar, msg="Cancela lo que se esta haciendo")

        # SALIR
        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_botones_grid, text="Salir", image=self.photo3, width=25, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=8, padx=4, pady=2, sticky="nsew")

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = Button(self.frame_botones_grid, image=self.photo_imp, pady=3, command=self.fImprime, border=3)
        self.btn_imprime.grid(row=0, column=5, padx=4, pady=2, sticky="nsew")

        self.photo1 = Image.open('toparch.png')
        self.photo1 = self.photo1.resize((25, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo1 = ImageTk.PhotoImage(self.photo1)
        self.btnToparch = Button(self.frame_botones_grid, text="", image=self.photo1, command=self.fToparch, bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=6, padx=4, pady=2, sticky="nsew")
        self.photo2 = Image.open('finarch.png')
        self.photo2 = self.photo2.resize((25, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo2 = ImageTk.PhotoImage(self.photo2)
        self.btnFinarch = Button(self.frame_botones_grid, text="", image=self.photo2, command=self.fFinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=7, padx=4, pady=2, sticky="nsew")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid.winfo_children():
            widg.grid_configure(padx=2, pady=3, sticky='nsew')

    def entrys(self):

        # FECHA
        self.lbl_fecha = Label(self.frame_dos, text="Fecha emision: ")
        self.lbl_fecha.grid(row=0, column=0, padx=4, pady=3, sticky=W)
        self.entry_fecha = Entry(self.frame_dos, textvariable=self.strvar_fecha, justify="left", width=10)
        self.entry_fecha.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha.grid(row=0, column=1, padx=4, pady=3, sticky=W)

        # NOMBRE
        self.lbl_usuario = Label(self.frame_dos, text="Cliente: ")
        self.lbl_usuario.grid(row=0, column=2, padx=4, pady=3, sticky=W)
        self.entry_usuario = Entry(self.frame_dos, textvariable=self.strvar_usuario, justify="left", width=47)
        self.strvar_usuario.trace("w", lambda *args: self.limitador(self.strvar_usuario, 50))
        self.entry_usuario.grid(row=0, column=3, padx=4, pady=3, sticky=W)

        # TIPO DOCUMENTO - COMBOBOX
        self.lbl_tipo_dni = Label(self.frame_dos, text="Tipo Documento: ")
        self.lbl_tipo_dni.grid(row=0, column=4, padx=4, pady=3, sticky=W)
        self.combo_tipo_dni = ttk.Combobox(self.frame_dos, textvariable=self.strvar_dni, state='readonly', width=46)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_tipo_dni["values"] = ["DNI-Documento Nacional de Identidad", "CI-Cedula de Identidad",
                                         "CUIT-Clave unica de identificacion tributaria", "LC-Libreta Civica",
                                         "LE-Libreta de Enrolamiento", "LEM-Libreta de Embarque", "PAS-Pasaporte"]
        self.combo_tipo_dni.grid(row=0, column=5, padx=4, pady=5, sticky=W)

        # NUMERO DOCUMENTO
        self.lbl_numdoc = Label(self.frame_dos, text="Nº Documento: ")
        self.lbl_numdoc.grid(row=1, column=0, padx=4, pady=3, sticky=W)
        self.entry_numdoc = Entry(self.frame_dos, textvariable=self.strvar_numdoc, justify="left", width=13)
        self.strvar_numdoc.trace("w", lambda *args: self.limitador(self.strvar_numdoc, 13))
        self.entry_numdoc.grid(row=1, column=1, padx=4, pady=3, sticky=W)

        # EQUIPO
        self.lbl_equipo = Label(self.frame_dos, text="Equipo: ")
        self.lbl_equipo.grid(row=1, column=2, padx=4, pady=3, sticky=W)
        self.entry_equipo = Entry(self.frame_dos, textvariable=self.strvar_equipo, justify="left", width=118)
        self.strvar_equipo.trace("w", lambda *args: self.limitador(self.strvar_equipo, 100))
        self.entry_equipo.grid(row=1, column=3, columnspan=3, padx=4, pady=3, sticky=W)

        # MODELO
        self.lbl_modelo = Label(self.frame_dos, text="Modelo: ")
        self.lbl_modelo.grid(row=2, column=0, padx=4, pady=3, sticky=W)
        self.entry_modelo = Entry(self.frame_dos, textvariable=self.strvar_modelo, justify="left", width=80)
        self.strvar_modelo.trace("w", lambda *args: self.limitador(self.strvar_modelo, 100))
        self.entry_modelo.grid(row=2, column=1, columnspan=3, padx=4, pady=3, sticky=W)

        # NUMERO DE SERIE
        self.lbl_serie = Label(self.frame_dos, text="Numero de Serie: ")
        self.lbl_serie.grid(row=2, column=4, padx=4, pady=3, sticky=W)
        self.entry_serie = Entry(self.frame_dos, textvariable=self.strvar_serie, justify="left", width=40)
        self.strvar_serie.trace("w", lambda *args: self.limitador(self.strvar_serie, 30))
        self.entry_serie.grid(row=2, column=5, padx=4, pady=3, sticky=W)

        # FALLOS
        self.lbl_diagnostico = Label(self.frame_dos, text="Diagnostico: ")
        self.lbl_diagnostico.grid(row=3, column=0, padx=4, pady=3, sticky=W)
        self.entry_diagnostico = Entry(self.frame_dos, textvariable=self.strvar_diagnostico, justify="left", width=150)
        self.strvar_diagnostico.trace("w", lambda *args: self.limitador(self.strvar_diagnostico, 250))
        self.entry_diagnostico.grid(row=3, column=1, columnspan=5, padx=4, pady=3, sticky=W)

        # PROVOCADO
        self.lbl_provocado = Label(self.frame_dos, text="Provocado: ")
        self.lbl_provocado.grid(row=4, column=0, padx=4, pady=3, sticky=W)
        self.entry_provocado = Entry(self.frame_dos, textvariable=self.strvar_provocado, justify="left", width=150)
        self.strvar_provocado.trace("w", lambda *args: self.limitador(self.strvar_provocado, 250))
        self.entry_provocado.grid(row=4, column=1, columnspan=5, padx=4, pady=3, sticky=W)

        self.frame_dos.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        self.frame_tres=LabelFrame(self.master, text="", foreground="red")

        # DESCRIPCION
        self.text_descripcion = ScrolledText(self.frame_tres)
        self.text_descripcion.config(width=105, height=4, wrap="word", padx=4, pady=2)
        self.text_descripcion.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # BOTON GENERAR TEXTO INFORME
        self.btn_genero_informe = Button(self.frame_tres, text="Generar\nInforme", command=self.fGenero_informe,
                                         width=16, height=4, bg="blue", fg="white")
        self.btn_genero_informe.grid(row=0, column=1, padx=5, pady=2)
