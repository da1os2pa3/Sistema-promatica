from tkinter import messagebox
#from tkinter import *
from tkinter import ttk
import tkinter as tk
import mysql.connector
from datetime import datetime

class ClaseFuncion_new:

    #def __init__(self, root, objeto):
    def __init__(self, root):

        self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")

        """ Por aca recibe primero la pantalla para que me funcione bien el parent en los messagebox. Luego tambien
        recibo el objeto instanciado  en el programa que llama la funcion (clientes, proveedores, articulos ... )
        y de esta manera poder usar su correspondiente ABM (clientes_ABM, proved_ABM ... ) """

        self.master = root

    def get_connection(self):
        print("OK= Escuchando.....")
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    """
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    METODOS - FORMATO DATOS
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """

    """
    ------------------------------------------------------------------------------
    # 1 - formatear_cifra - Toma una cifra y le pone los puntos de los miles y las 
          comas decimales - cifra debe venir tipo numerico
    ------------------------------------------------------------------------------
    """
    def formatear_cifra(self, cifra):
        numero = cifra
        salida1 = "{:,.2f}".format(numero)
        salida2 = salida1.replace(',', 'n')
        salida3 = salida2.replace('.', ',')
        salida4 = salida3.replace('n', '.')
        return salida4
    """
    ------------------------------------------------------------------------------
    """


    """
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    METODOS TRATAMIENTO DE FECHAS
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """

    """
    --------------------------------------------------------------------------
    1 - Toma una fecha en formato 2025-12-26 (tabla) y la devuelve 26/12/2026 (string-uso en sistema)
        Ya tanmbien la tengo hecha en funciones como 'fecha_str_reves_normal(self, par, con_hora=False):' 
    --------------------------------------------------------------------------
    """
    def fecha_es(self, fecha_mysql):
        fecha = datetime.strptime(fecha_mysql, "%Y-%m-%d")
        return fecha.strftime("%d/%m/%Y")
    """
    ------------------------------------------------------------------------------
    """

    def fecha_a_tabla(self, fecha_str):
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M:%S")
            return fecha.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None  # o podés lanzar error si preferís




    """
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    METODOS PANTALLAS - MENSAJES - ESTETICA
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """

    """
    --------------------------------------------------------------------------
    1 - METODO mostrar_toast
        Por ahora la uso desde ctacte con los siguientes llamados:
        self.varFuncion_new.mostrar_toast(self.pantalla_estad, "🧹 Iniciando borrado de registros...", "green", 2500, "")
        --- proceso real ---
        self.pantalla_estad.after(3000, lambda: self.varFuncion_new.mostrar_toast(self.pantalla_estad, "✅ Proceso 
        finalizado", "green", 2500, ""))
    --------------------------------------------------------------------------
    """
    def mostrar_toast(self, pantalla_padre, mensaje, pa_color, duracion=3000, tipo="info"):

        tipo = str(tipo).strip().lower()

        colores = {
            "success": "#1e7e34",  # verde
            "error": "#c82333",  # rojo
            "info": "#222222"  # gris
        }

        bg_color = colores.get(tipo, "#222222")

        """ toast.overrideredirect(True)        # sin bordes
            toast.attributes("-topmost", True)  # siempre arriba
            toast = tk.Toplevel(self.pantalla_estad) # asignamos la clase a variable toast"""

        toast = tk.Toplevel(pantalla_padre)
        toast.overrideredirect(True)  # sin bordes
        toast.attributes("-topmost", True)
        toast.configure(bg=bg_color)

        # Estilo
        frame = tk.Frame(toast, bg=pa_color, padx=20, pady=10)
        frame.pack()

        tk.Label(
            frame,
            text=mensaje,
            fg="white",
            bg=pa_color,
            font=("Segoe UI", 10)
        ).pack()

        # 🔔 sonido solo para error (Windows)
        if tipo == "error":
            try:
                import winsound
                winsound.MessageBeep(winsound.MB_ICONHAND)
            except Exception:
                pass

        # Posición (abajo a la derecha)
        pantalla_padre.update_idletasks()
        toast.update_idletasks()

        ventana_x = pantalla_padre.winfo_rootx()
        ventana_y = pantalla_padre.winfo_rooty()
        ventana_ancho = pantalla_padre.winfo_width()
        ventana_alto = pantalla_padre.winfo_height()

        toast_ancho = toast.winfo_width()
        toast_alto = toast.winfo_height()

        x = ventana_x + ventana_ancho - toast_ancho - 20
        y = ventana_y + ventana_alto - toast_alto - 50

        toast.geometry(f"+{x}+{y}")

        # Auto cerrar
        toast.after(duracion, toast.destroy)
    """
    ------------------------------------------------------------------------------
    """


    """
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    METODOS - PUNTEROS - MOVIMIENTOS EN EL GRID
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """

    """
    ------------------------------------------------------------------------------
    1 - MOVER PUNTERO top end
    ------------------------------------------------------------------------------
    """
    def mover_puntero_topend(self, tree, posicion):

        items = tree.get_children()
        if not items:
            return
        item = items[0] if posicion == 'TOP' else items[-1]
        tree.focus_set()
        tree.selection_set(item)
        tree.focus(item)
        tree.see(item)
    """
    ------------------------------------------------------------------------------
    """


    """
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    METODOS - VALIDACIONES
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """

    """
    ------------------------------------------------------------------------------
    1 - Metodo Validar - Valida los caracteres que ingresan en los campos numericos - solo numeros, punto y guion. 
    ------------------------------------------------------------------------------
    """

    def validar(self, value):
        # codigo = value
        # for i in codigo:
        #     if i not in '0123456789.-':
        #         return  False
        # return True
        if value == "":
            return True  # permitir borrar
            # Solo caracteres válidos
        for c in value:
            if c not in "0123456789.-":
                return False
            # Solo un signo menos y al inicio
        if value.count("-") > 1 or ("-" in value and not value.startswith("-")):
            return False
            # Solo un punto decimal
        if value.count(".") > 1:
            return False
        return True
    """
    ------------------------------------------------------------------------------
    """











    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # IMPORTANT - FUNCION SEL - ventana_selec
    # Ventana SEL utilizado en todos los modulos
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    # def ventana_selec(self, xtabla, campo1, campo2, campo3, titu1, titu2, titu3, filtro, titulo, pesos):
    #
    #     # ----------------------------------------------------------------------
    #     # VALIDO LA CANTIDAD DE CAMPOS PASADDOS
    #     if not campo1 or not campo2 or not campo3:
    #         messagebox.showerror("Error Sistema", "Debe pasar tres campos a ventana de seleccion", parent=self.master)
    #         return None
    #
    #     # ----------------------------------------------------------------------
    #     # CREO LA PANTALLA
    #
    #     self.sel_item = tk.Toplevel()
    #     self.sel_item.protocol("WM_DELETE_WINDOW", self.fCerrar)
    #     self.sel_item.geometry('820x300+600+250')
    #     self.sel_item.config(bg='light grey', padx=5, pady=5)
    #     self.sel_item.resizable(1, 1)
    #     self.sel_item.title(f"Seleccione => {titulo}")
    #     self.sel_item.focus_set()
    #     self.sel_item.grab_set()
    #     self.sel_item.transient(master=self.master)
    #
    #     # -----------------------------------------------------------------
    #     # STRINGVARS LOCALES
    #
    #     # TRAIGO EL DOLAR ACTUAL
    #     self.strvar_dolar_hoy = tk.StringVar(value=self.traer_dolarhoy())
    #     # -----------------------------------------------------------------
    #
    #     # -----------------------------------------------------------------
    #     # DEFINO EL TREEVIEW
    #
    #     self.frame_select=tk.LabelFrame(self.sel_item, text="", foreground="#CF09BD")
    #
    #     # STYLE TREEVIEW
    #     style = ttk.Style(self.frame_select)
    #     style.theme_use("clam")
    #     style.configure("Treeview.Heading", background="black", foreground="white")
    #
    #     self.grid_funcsel = ttk.Treeview(self.frame_select, height=10, columns=("col1", "col2", "col3"))
    #
    #     #self.grid_funcsel.bind("<Double-Button-1>", self.DobleClickGrid)
    #     # use lambda para asi poder pasar parametro con la tabla
    #     self.grid_funcsel.bind("<Double-Button-1>", lambda e: self.DobleClickGrid(e, xtabla))
    #
    #     self.grid_funcsel.column("#0", width=20, anchor="center", minwidth=20)
    #     self.grid_funcsel.column("col1", width=300, anchor="center", minwidth=270)
    #     self.grid_funcsel.column("col2", width=150, anchor="center", minwidth=120)
    #     self.grid_funcsel.column("col3", width=150, anchor="center", minwidth=120)
    #
    #     self.grid_funcsel.heading("#0", text="Id", anchor="center")
    #     self.grid_funcsel.heading("col1", text=titu1, anchor="center")
    #     self.grid_funcsel.heading("col2", text=titu2, anchor="center")
    #     self.grid_funcsel.heading("col3", text=titu3, anchor="center")
    #
    #     self.grid_funcsel.tag_configure('oddrow', background='light green')
    #     self.grid_funcsel.tag_configure('evenrow', background='white')
    #
    #     # SCROLLBAR del Treeview
    #     scroll_x = tk.Scrollbar(self.frame_select, orient="horizontal")
    #     scroll_y = tk.Scrollbar(self.frame_select, orient="vertical")
    #     self.grid_funcsel.config(xscrollcommand=scroll_x.set)
    #     self.grid_funcsel.config(yscrollcommand=scroll_y.set)
    #     scroll_x.config(command=self.grid_funcsel.xview)
    #     scroll_y.config(command=self.grid_funcsel.yview)
    #     scroll_y.pack(side="right", fill="y")
    #     scroll_x.pack(side="bottom", fill="x")
    #     self.grid_funcsel['selectmode'] = 'browse'
    #
    #     self.grid_funcsel.pack(side="top", fill="both", expand=1, padx=0, pady=0)
    #     self.frame_select.pack(side="top", fill="both", padx=0, pady=0)
    #
    #     # --------------------------------------------------------------------------
    #     # LIMPIAR EL GRID
    #
    #     self.limpiar_Grid_sel()
    #
    #     # --------------------------------------------------------------------------
    #     # DEFINO VARIABLES
    #
    #     """ En que busco pongo el parametro que viene (filtro) donde esta definido que buscar y en que campos """
    #     que_busco = filtro
    #
    #     """ La defino en blanco porque esta es la que se usa para ir a la tabla a buscar el registro completo una vez
    #     que el usuario selecciono en la grilla el registro que queria. En el caso de que el usuario cierre la ventana
    #     desde la X antes de seleccionar, esta variable vuelve en BLANCO y si no la tengo definida aqui da error al
    #     retornar los valores. Es la variable que se retorna al programa principal que llamo la ventana de seleccion """
    #     self.todo_el_registro = ""
    #
    #     """ Aqui solicitamos a la funcion que nos devuelva todos los registros de la tabla especificada que
    #     cumplan con la condicion de busqueda, puede que ninguno la cumpla o varios la tengan. Es lo que
    #     presentaria (mostrar) el Grid para que yo elija el que quiero """
    #     retorno = self.buscar_entabla(que_busco) # el primero del retorno es el Id
    #
    #     # --------------------------------------------------------------------------
    #     # CARGO EL GRID
    #
    #     """  Este metodo, me devuelve una lista compuesta por tuplas con la posicion y nombre de cada campo..
    #     por ejemplo (15, nomape)... de la tabla que le haya pasado. Esto lo hace para todos los campos.
    #     Usa esta sentencia SQL tomando como ejemplo la tabla clientes:
    #     #SELECT ORDINAL_POSITION, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'sist_prom'
    #     AND TABLE_NAME = 'clientes' ORDER BY ORDINAL_POSITION """
    #
    #     # Traigo una lista con tuplas de posicion y nombre del campo de la tabla
    #     self.nombre_campos = self.pasar_nombres_campos(xtabla)
    #
    #     """ Creo un diccionario que contendra los pares (edad: 25, nombre: Daniel....) En este caso contendra la
    #     posicion del campo y el nombre. """
    #     lista_posic_campos = {}
    #
    #     """ En este -for-, hago una iteracion y cargo el diccionario con los campos que quiero que se muestren
    #     en el Grid segun le pedi en campo1, campo2, campo3.. pero no van a estar ordenados como quiero que
    #     aparezcan en las columnas del grid:
    #     antes => {'2': 1, '3': 4, '1': 15} luego de ordenar =>{'1': 15, '2': 1, '3': 4} """
    #
    #     # for index, item in enumerate(self.nombre_campos):
    #     #
    #     #     if self.nombre_campos[index][1] == campo1:
    #     #         lista_posic_campos["1"]=index
    #     #     if self.nombre_campos[index][1] == campo2:
    #     #         lista_posic_campos["2"]=index
    #     #     if self.nombre_campos[index][1] == campo3:
    #     #         lista_posic_campos["3"]=index
    #
    #     # for item in self.nombre_campos:
    #     #
    #     #     pos_real = item[0] - 1  # 👈 clave: ORDINAL_POSITION - 1
    #     #     nombre = item[1]
    #     #
    #     #     if nombre == campo1:
    #     #         lista_posic_campos["1"] = pos_real
    #     #     if nombre == campo2:
    #     #         lista_posic_campos["2"] = pos_real
    #     #     if nombre == campo3:
    #     #         lista_posic_campos["3"] = pos_real
    #
    #
    #     """ Aqui ya creo el diccionario ordenado segun el orden en que pase los campos en los parametros
    #     de la funcion (campo1, campo2 ...) """
    #     # ordenado = dict(sorted(lista_posic_campos.items()))
    #
    #     """  Ahora guardo el valor que me interesa que es el segundo del diccionario que es donde esta la posicion
    #     en la tabla del campo y los guardo en tres variables. """
    #
    #     # valor1 = list(ordenado.values())[0]
    #     # valor2 = list(ordenado.values())[1]
    #     # valor3 = list(ordenado.values())[2]
    #
    #     """ Ahora si hago la iteracion en todo -retorno- que contiene todos los registros que cuplen con la condicion
    #     y asi puedo seleccionar mediante el subindice los que quiero que se muestren en el grid. Como se ve, aca
    #     hago la insercion en el treeview de los items que me va a mostrar la ventana para que podamos seleccionar. """
    #
    #     campos_dict = {nombre: pos - 1 for pos, nombre in self.nombre_campos}
    #
    #     valor1 = campos_dict[campo1]
    #     valor2 = campos_dict[campo2]
    #     valor3 = campos_dict[campo3]
    #
    #
    #
    #     cont = 0
    #     for index, reto in enumerate(retorno):
    #
    #         cont += 1
    #         color = ('evenrow',) if cont % 2 else ('oddrow',)
    #
    #         if pesos == "S":
    #
    #             dolar = float(self.strvar_dolar_hoy.get())
    #             precio_base = float(reto[valor3])
    #             recargo1 = float(reto[7]) / 100
    #             recargo2 = float(reto[9]) / 100
    #             precio_venta = precio_base * dolar * (1 + recargo1) * (1 + recargo2)
    #
    #             # precio_venta = ((float(reto[valor3]) * float(self.strvar_dolar_hoy.get())) * (1 + (float(reto[7]/100)))
    #             #                 * (1 + (float(reto[9]/100))))
    #
    #             self.grid_funcsel.insert("", "end", tags=color, text=reto[0], values=(reto[valor1], reto[valor2],
    #                                                                                     round(precio_venta, 2)))
    #         else:
    #             self.grid_funcsel.insert("", "end", tags=color, text=reto[0], values=(reto[valor1], reto[valor2],
    #                                                                                     reto[valor3]))
    #
    #     if len(self.grid_funcsel.get_children()) > 0:
    #         self.grid_funcsel.selection_set(self.grid_funcsel.get_children()[0])
    #
    #     # --------------------------------------------------------------------------
    #     # BOTONES
    #
    #     self.frame_botones_select=tk.LabelFrame(self.sel_item, text="", foreground="#CF09BD")
    #
    #     # Aca llamo a la funcion que me devuelve el registro completo
    #     self.btn_seleccion_sel = tk.Button(self.frame_botones_select, text="Seleccionar",
    #                                     command=lambda:self.fSelec_sel_item(xtabla), width=22, bg="grey", fg="white")
    #     self.btn_seleccion_sel.grid(row=0, column=0, padx=5, pady=2)
    #
    #     self.btn_cancelar_sel = tk.Button(self.frame_botones_select, text="Volver", command=lambda :self.fVuelvo_nada(),
    #                                    width=22, bg="grey", fg="white")
    #     self.btn_cancelar_sel.grid(row=0, column=1, padx=5, pady=2)
    #
    #     self.frame_botones_select.pack(side="top", padx=0, pady=0)
    #
    #     # self.sel_item.mainloop()
    #     self.master.wait_window(self.sel_item)
    #
    #     """ Retorno el registro -completo- del cliente que necesito. Ojo, no es el item del Grid el que vuelve, porque
    #     este solo tiene tres datos del registro (solo los que quise visualizar) y puede que el programa al que
    #     se devuelven necesite mas datos. """
    #
    #     # --------------------------------------------------------------------------
    #     #DEVOLUCION REGISTRO SELECCIONADO => => => =>
    #     return self.todo_el_registro
    #     # --------------------------------------------------------------------------


    """
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    METODOS - SEL
    ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    """

    # funcion principal que llama a todas las otras
    def ventana_selec(self, xtabla, campo1, campo2, campo3, titu1, titu2, titu3, filtro, titulo, pesos):

        # VALIDACIÓN ---------------------------------------------------------------
        if not all([campo1, campo2, campo3]):
            messagebox.showerror("Error Sistema",
                                 "Debe pasar tres campos a ventana de seleccion",
                                 parent=self.master)
            return None

        # VENTANA ------------------------------------------------------------------
        self.sel_item = tk.Toplevel(self.master)
        self.sel_item.protocol("WM_DELETE_WINDOW", self.fCerrar)
        self.sel_item.geometry('820x300+600+250')
        self.sel_item.config(bg='light grey', padx=5, pady=5)
        self.sel_item.resizable(1, 1)
        self.sel_item.title(f"Seleccione => {titulo}")

        self.sel_item.transient(self.master)
        self.sel_item.grab_set()
        self.sel_item.focus_set()

        # VARIABLES -----------------------------------------------------------------
        self.todo_el_registro = ""
        dolar = float(self.traer_dolarhoy())

        # TREEVIEW - GRID -----------------------------------------------------------
        frame = tk.LabelFrame(self.sel_item)
        frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_funcsel = ttk.Treeview(frame, height=10, columns=("col1", "col2", "col3"), selectmode="browse")

        self.grid_funcsel.bind("<Double-Button-1>", lambda e: self.DobleClickGrid(e, xtabla))

        # COLUMNAS
        self.grid_funcsel.column("#0", width=50, anchor="center")
        self.grid_funcsel.column("col1", width=300, anchor="center")
        self.grid_funcsel.column("col2", width=150, anchor="center")
        self.grid_funcsel.column("col3", width=150, anchor="center")

        self.grid_funcsel.heading("#0", text="Id")
        self.grid_funcsel.heading("col1", text=titu1)
        self.grid_funcsel.heading("col2", text=titu2)
        self.grid_funcsel.heading("col3", text=titu3)

        self.grid_funcsel.tag_configure('oddrow', background='light green')
        self.grid_funcsel.tag_configure('evenrow', background='white')

        # SCROLL
        scroll_y = tk.Scrollbar(frame, orient="vertical", command=self.grid_funcsel.yview)
        scroll_x = tk.Scrollbar(frame, orient="horizontal", command=self.grid_funcsel.xview)

        self.grid_funcsel.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_funcsel.pack(fill="both", expand=True)

        # DATOS ---------------------------------------------------------------------
        retorno = self.buscar_entabla(filtro)

        # MAPEAR CAMPOS
        nombre_campos = self.pasar_nombres_campos(xtabla)
        campos_dict = {nombre: pos - 1 for pos, nombre in nombre_campos}

        valor1 = campos_dict[campo1]
        valor2 = campos_dict[campo2]
        valor3 = campos_dict[campo3]

        # CARGA GRID ----------------------------------------------------------------
        for i, fila in enumerate(retorno):

            color = ('evenrow',) if i % 2 else ('oddrow',)

            if pesos == "S":
                precio_base = float(fila[valor3])
                rec1 = float(fila[7]) / 100
                rec2 = float(fila[9]) / 100
                precio = precio_base * dolar * (1 + rec1) * (1 + rec2)
                valor_mostrar = round(precio, 2)
            else:
                valor_mostrar = fila[valor3]

            self.grid_funcsel.insert("","end", text=fila[0], values=(fila[valor1],
                                                                     fila[valor2], valor_mostrar), tags=color)

        # SELECCIÓN INICIAL
        items = self.grid_funcsel.get_children()
        if items:
            self.grid_funcsel.selection_set(items[0])

        # BOTONES -------------------------------------------------------------------
        frame_btn = tk.Frame(self.sel_item)
        frame_btn.pack(pady=5)

        tk.Button(frame_btn, text="Seleccionar", width=20,
                  command=lambda: self.fSelec_sel_item(xtabla)).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Volver", width=20, command=self.fVuelvo_nada).grid(row=0, column=1, padx=5)

        # ESPERA (reemplaza mainloop) ------------------------------------------------
        self.master.wait_window(self.sel_item)

        return self.todo_el_registro

    def DobleClickGrid(self, event, la_tabla):
        self.fSelec_sel_item(la_tabla)

    def fVuelvo_nada(self):
        # Boton de opcion volver
        self.todo_el_registro = ""
        self.fCerrar()

    def fSelec_sel_item(self, ztabla):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_funcsel.focus()
        # Asi obtengo la clave de la base de datos (Tabla) campo Id que no es lo mismo que el otro
        # (numero secuencial 1, 2, 3, 4.... que pone la Tabla BD automaticamente al dar el alta
        self.clave = self.grid_funcsel.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Seleccion", "No hay nada seleccionado", parent=self.master)
            return

        """ Este metodo me busca especificamente el item seleccionado a traves del Id y la tabla en la que se 
        debe buscar(las dos cosas se pasan como parametros). Lo trae completo (todo el registro), luego sera 
        devuelto al programa principal para su tratamiento. """

        #self.todo_el_registro = self.varObjeto.pasar_item_seleccionado(self.clave, ztabla)
        self.todo_el_registro = self.pasar_item_seleccionado(self.clave, ztabla)

        self.fCerrar()

    def pasar_item_seleccionado(self, Id, is_ztabla):

        """
        Esta funcion fue creada para asistir a la ventana de seleccion de items (famosa SEL). Va a devolver
        el registro seleccionado (a traves del Id que nos viene coo parametro), de la tabla que se nos proporciona
        tambien como parametrole
        """

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            #expresion=(f"'''SELECT * FROM {ztabla} WHERE Id = {}'''.format(Id)")
            #sql = '''SELECT * FROM clientes WHERE Id = {}'''.format(Id)
            sql = '''SELECT * FROM '''+is_ztabla+''' WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            datos_inf = cur.fetchall()
            return datos_inf
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        """ Aqui nos llega un string de busqueda y en que campos debemos buscarlo. Devolvemos todos
        los registros que cumplan con la condicion especificada """
        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            return datos
        finally:
            cur.close()
            cnn.close()

    def pasar_nombres_campos(self, xtabla):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            expresion=(f"SELECT ORDINAL_POSITION, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                       f"WHERE TABLE_NAME = '{xtabla}' ORDER BY ORDINAL_POSITION")
            cur.execute(expresion)
            datos = cur.fetchall()
            cnn.commit()
            return datos
        finally:
            cur.close()
            cnn.close()

    def consultar_informa(self):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            return datos_inf
        finally:
            cur.close()
            cnn.close()

    def limpiar_Grid_sel(self):
        for item in self.grid_funcsel.get_children():
            self.grid_funcsel.delete(item)

    def fCerrar(self):

        """ El quit hace que el sistema salga fuera del mainloop, esto sale pero no destruye la pantalla, la misma
        queda congelada, para eso luego hay que hacer el destroy. """

        #self.sel_item.quit()
        self.sel_item.destroy()
        self.master.grab_set()
        self.master.focus_set()

    def traer_dolarhoy(self):
        dev_informa = self.consultar_informa()
        for row in dev_informa:
            return row[21]
    """
    ------------------------------------------------------------------------------
    """
