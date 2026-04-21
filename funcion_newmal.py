import sys
from tkinter import messagebox
#from tkinter import *
from tkinter import ttk
import tkinter as tk

# --------------------------------------
import mysql.connector
#from mysql.connector import Error
# --------------------------------------
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
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom"
        )


    """
    ===================================================================================
    FORMATOS DE DATOS 
    ===================================================================================
    """

    """
    -----------------------------------------------------------------------------------
    1 - formatear_cifra
        - Toma una cifra y le pone los puntos de los miles y las comas decimales
        - cifra debe venir tipo numerico
    -----------------------------------------------------------------------------------
    """
    def formatear_cifra(self, cifra):
        numero = cifra
        salida1 = "{:,.2f}".format(numero)
        salida2 = salida1.replace(',', 'n')
        salida3 = salida2.replace('.', ',')
        salida4 = salida3.replace('n', '.')
        return salida4
    """
    -----------------------------------------------------------------------------------
    """


    """
    ===================================================================================
    VALIDACIONES 
    ===================================================================================
    """

    """
    -----------------------------------------------------------------------------------
    1 - validar 2-4-26
        - Toma una cifra y le pone los puntos de los miles y las comas decimales
        - cifra debe venir tipo numerico
        Valida los caracteres que ingresan en los campos numericos - solo numeros, punto y guion. 
    -----------------------------------------------------------------------------------
    """
    def validar(self, value):
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
    -----------------------------------------------------------------------------------
    """


    """
    ===================================================================================
    COSAS DE PANTALLAS Y MENSAJES 
    ===================================================================================
    """

    """ 1 - METODO mostrar_toast - 10-2-26
            Por ahora la uso desde ctacte con los siguientes llamados:
            self.varFuncion_new.mostrar_toast(self.pantalla_estad, "🧹 Iniciando borrado de registros..", "green", 2500, "")
            --- proceso real ---
            self.pantalla_estad.after(3000, lambda: self.varFuncion_new.mostrar_toast(self.pantalla_estad, "✅ Proceso 
            finalizado", "green", 2500, ""))
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
    -----------------------------------------------------------------------------------
    """



    """
    ===================================================================================
    CONVERSIONES DE FORMATOS 
    ===================================================================================
    """

    """
    -----------------------------------------------------------------------------------
    1 -  Toma una fecha en formato 2025-12-26 y  la devuelve 26/12/2026
    -----------------------------------------------------------------------------------
    """
    def fecha_es(self, fecha_mysql):
        fecha = datetime.strptime(fecha_mysql, "%Y-%m-%d")
        return fecha.strftime("%d/%m/%Y")
    """
    -----------------------------------------------------------------------------------
    """



    """
    ===================================================================================
    PUNTEROS Y MOVIMIENTOS DENTRO DE LOS GRIDS 
    ===================================================================================
    """

    """
    -----------------------------------------------------------------------------------
    1 -  Mueve al final o tope de aqrchivo el puntero
    -----------------------------------------------------------------------------------
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
    -----------------------------------------------------------------------------------
    """







    """
    ===================================================================================
    FUNCION SEL
    ===================================================================================
    """

    def ventana_selec(self, xtabla, campo1, campo2, campo3, titu1, titu2, titu3, filtro, titulo, pesos):

        # ----------------------------------------------------------------------
        # VALIDO LA CANTIDAD DE CAMPOS PASADDOS
        if not campo1 or not campo2 or not campo3:
            messagebox.showerror("Error Sistema", "Debe pasar tres campos a ventana de seleccion", parent=self.master)
            return None

        # ----------------------------------------------------------------------
        # CREO LA PANTALLA

        self.sel_item = tk.Toplevel()
        self.sel_item.protocol("WM_DELETE_WINDOW", self.fCerrar)
        self.sel_item.geometry('820x300+600+250')
        self.sel_item.config(bg='light grey', padx=5, pady=5)
        self.sel_item.resizable(1, 1)
        self.sel_item.title(f"Seleccione => {titulo}")
        self.sel_item.focus_set()
        self.sel_item.grab_set()
        self.sel_item.transient(master=self.master)

        # -----------------------------------------------------------------
        # STRINGVARS LOCALES

        # TRAIGO EL DOLAR ACTUAL
        self.strvar_dolar_hoy = tk.StringVar(value=self.traer_dolarhoy())
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        # DEFINO EL TREEVIEW

        self.frame_select=tk.LabelFrame(self.sel_item, text="", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_select)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_funcsel = ttk.Treeview(self.frame_select, height=10, columns=("col1", "col2", "col3"))

        #self.grid_funcsel.bind("<Double-Button-1>", self.DobleClickGrid)
        # use lambda para asi poder pasar parametro con la tabla
        self.grid_funcsel.bind("<Double-Button-1>", lambda e: self.DobleClickGrid(e, xtabla))

        self.grid_funcsel.column("#0", width=20, anchor="center", minwidth=20)
        self.grid_funcsel.column("col1", width=300, anchor="center", minwidth=270)
        self.grid_funcsel.column("col2", width=150, anchor="center", minwidth=120)
        self.grid_funcsel.column("col3", width=150, anchor="center", minwidth=120)

        self.grid_funcsel.heading("#0", text="Id", anchor="center")
        self.grid_funcsel.heading("col1", text=titu1, anchor="center")
        self.grid_funcsel.heading("col2", text=titu2, anchor="center")
        self.grid_funcsel.heading("col3", text=titu3, anchor="center")

        self.grid_funcsel.tag_configure('oddrow', background='light green')
        self.grid_funcsel.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_select, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_select, orient="vertical")
        self.grid_funcsel.config(xscrollcommand=scroll_x.set)
        self.grid_funcsel.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_funcsel.xview)
        scroll_y.config(command=self.grid_funcsel.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_funcsel['selectmode'] = 'browse'

        self.grid_funcsel.pack(side="top", fill="both", expand=1, padx=0, pady=0)
        self.frame_select.pack(side="top", fill="both", padx=0, pady=0)

        # --------------------------------------------------------------------------
        # LIMPIAR EL GRID

        self.limpiar_Grid_sel()

        # --------------------------------------------------------------------------
        # DEFINO VARIABLES

        """ En que busco pongo el parametro que viene (filtro) donde esta definido que buscar y en que campos """
        que_busco = filtro

        """ La defino en blanco porque esta es la que se usa para ir a la tabla a buscar el registro completo una vez 
        que el usuario selecciono en la grilla el registro que queria. En el caso de que el usuario cierre la ventana 
        desde la X antes de seleccionar, esta variable vuelve en BLANCO y si no la tengo definida aqui da error al 
        retornar los valores. Es la variable que se retorna al programa principal que llamo la ventana de seleccion """
        self.todo_el_registro = ""

        """ Aqui solicitamos a la funcion que nos devuelva todos los registros de la tabla especificada que 
        cumplan con la condicion de busqueda, puede que ninguno la cumpla o varios la tengan. Es lo que 
        presentaria (mostrar) el Grid para que yo elija el que quiero """
        retorno = self.buscar_entabla(que_busco) # el primero del retorno es el Id

        # --------------------------------------------------------------------------
        # CARGO EL GRID

        """  Este metodo, me devuelve una lista compuesta por tuplas con la posicion y nombre de cada campo.. 
        por ejemplo (15, nomape)... de la tabla que le haya pasado. Esto lo hace para todos los campos.
        Usa esta sentencia SQL tomando como ejemplo la tabla clientes:
        #SELECT ORDINAL_POSITION, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'sist_prom' 
        AND TABLE_NAME = 'clientes' ORDER BY ORDINAL_POSITION """

        # Traigo una lista con tuplas de posicion y nombre del campo de la tabla
        self.nombre_campos = self.pasar_nombres_campos(xtabla)

        """ Creo un diccionario que contendra los pares (edad: 25, nombre: Daniel....) En este caso contendra la 
        posicion del campo y el nombre. """
        lista_posic_campos = {}

        """ En este -for-, hago una iteracion y cargo el diccionario con los campos que quiero que se muestren 
        en el Grid segun le pedi en campo1, campo2, campo3.. pero no van a estar ordenados como quiero que 
        aparezcan en las columnas del grid:
        antes => {'2': 1, '3': 4, '1': 15} luego de ordenar =>{'1': 15, '2': 1, '3': 4} """

        for index, item in enumerate(self.nombre_campos):

            if self.nombre_campos[index][1] == campo1:
                lista_posic_campos["1"]=index
            if self.nombre_campos[index][1] == campo2:
                lista_posic_campos["2"]=index
            if self.nombre_campos[index][1] == campo3:
                lista_posic_campos["3"]=index

        """ Aqui ya creo el diccionario ordenado segun el orden en que pase los campos en los parametros 
        de la funcion (campo1, campo2 ...) """
        ordenado = dict(sorted(lista_posic_campos.items()))

        """  Ahora guardo el valor que me interesa que es el segundo del diccionario que es donde esta la posicion 
        en la tabla del campo y los guardo en tres variables. """

        valor1 = list(ordenado.values())[0]
        valor2 = list(ordenado.values())[1]
        valor3 = list(ordenado.values())[2]

        """ Ahora si hago la iteracion en todo -retorno- que contiene todos los registros que cuplen con la condicion 
        y asi puedo seleccionar mediante el subindice los que quiero que se muestren en el grid. Como se ve, aca 
        hago la insercion en el treeview de los items que me va a mostrar la ventana para que podamos seleccionar. """

        cont = 0
        for index, reto in enumerate(retorno):

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            if pesos == "S":
                precio_venta = ((float(reto[valor3]) * float(self.strvar_dolar_hoy.get())) * (1 + (float(reto[7]/100)))
                                * (1 + (float(reto[9]/100))))

                self.grid_funcsel.insert("", "end", tags=color, text=reto[0], values=(reto[valor1], reto[valor2],
                                                                                        round(precio_venta, 2)))
            else:
                self.grid_funcsel.insert("", "end", tags=color, text=reto[0], values=(reto[valor1], reto[valor2],
                                                                                        reto[valor3]))

        if len(self.grid_funcsel.get_children()) > 0:
            self.grid_funcsel.selection_set(self.grid_funcsel.get_children()[0])

        # --------------------------------------------------------------------------
        # BOTONES

        self.frame_botones_select=tk.LabelFrame(self.sel_item, text="", foreground="#CF09BD")

        # Aca llamo a la funcion que me devuelve el registro completo
        self.btn_seleccion_sel = tk.Button(self.frame_botones_select, text="Seleccionar",
                                        command=lambda:self.fSelec_sel_item(xtabla), width=22, bg="grey", fg="white")
        self.btn_seleccion_sel.grid(row=0, column=0, padx=5, pady=2)

        # self.btn_cancelar_sel = Button(self.frame_botones_select, text="Volver", command=self.fCerrar, width=22,
        # bg="grey", fg="white")
        self.btn_cancelar_sel = tk.Button(self.frame_botones_select, text="Volver", command=lambda :self.fVuelvo_nada(),
                                       width=22, bg="grey", fg="white")
        self.btn_cancelar_sel.grid(row=0, column=1, padx=5, pady=2)

        self.frame_botones_select.pack(side="top", padx=0, pady=0)

        self.sel_item.mainloop()

        """ Retorno el registro -completo- del cliente que necesito. Ojo, no es el item del Grid el que vuelve, porque 
        este solo tiene tres datos del registro (solo los que quise visualizar) y puede que el programa al que 
        se devuelven necesite mas datos. """

        # --------------------------------------------------------------------------
        #DEVOLUCION REGISTRO SELECCIONADO => => => =>
        return self.todo_el_registro
        # --------------------------------------------------------------------------

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

    def limpiar_Grid_sel(self):
        for item in self.grid_funcsel.get_children():
            self.grid_funcsel.delete(item)

    def fCerrar(self):

        """ El quit hace que el sistema salga fuera del mainloop, esto sale pero no destruye la pantalla, la misma
        queda congelada, para eso luego hay que hacer el destroy. """

        self.sel_item.quit()
        self.sel_item.destroy()
        self.master.grab_set()
        self.master.focus_set()

    def buscar_entabla(self, argumento):

        """ Aqui nos llega un string de busqueda y en que campos debemos buscarlo. Devolvemos todos
        los registros que cumplan con la condicion especificada """

        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM " + argumento)
        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def pasar_nombres_campos(self, xtabla):

        cur = self.cnn.cursor()
        expresion=(f"SELECT ORDINAL_POSITION, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                   f"WHERE TABLE_NAME = '{xtabla}' ORDER BY ORDINAL_POSITION")
        #cur.execute("SELECT ORDINAL_POSITION, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'clientes'
        # ORDER BY ORDINAL_POSITION")
        cur.execute(expresion)
        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def pasar_item_seleccionado(self, Id, is_ztabla):

        """
        Esta funcion fue creada para asistir a la ventana de seleccion de items (famosa SEL). Va a devolver
        el registro seleccionado (a traves del Id que nos viene coo parametro), de la tabla que se nos proporciona
        tambien como parametrole
        """

        cur = self.cnn.cursor()
        #expresion=(f"'''SELECT * FROM {ztabla} WHERE Id = {}'''.format(Id)")
        #sql = '''SELECT * FROM clientes WHERE Id = {}'''.format(Id)
        sql = '''SELECT * FROM '''+is_ztabla+''' WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        datos_inf = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos_inf

    def consultar_informa(self):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos_inf
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-consultar informa-",
                                 parent=self.master)
            exit()

    def traer_dolarhoy(self):
        dev_informa = self.consultar_informa()
        for row in dev_informa:
            return row[21]

