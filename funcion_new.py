from tkinter import messagebox
from tkinter import *
from tkinter import ttk
# --------------------------------------
import mysql.connector
from mysql.connector import Error
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

    # --------------------------------------------------------------------------
    # FUNCION SEL
    # --------------------------------------------------------------------------

    def ventana_selec(self, xtabla, campo1, campo2, campo3, titu1, titu2, titu3, filtro, titulo, pesos):

        # ----------------------------------------------------------------------
        # VALIDO LA CANTIDAD DE CAMPOS PASADDOS
        if not campo1 or not campo2 or not campo3:
            messagebox("Error Sistema", "Debe pasar tres campos a ventana de seleccion", parent=self.master)
            return None

        # ----------------------------------------------------------------------
        # CREO LA PANTALLA

        self.sel_item = Toplevel()
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

        self.strvar_dolar_hoy = StringVar(value=self.traer_dolarhoy())
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        # DEFINO EL TREEVIEW

        self.frame_select=LabelFrame(self.sel_item, text="", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_select)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_funcsel = ttk.Treeview(self.frame_select, height=10, columns=("col1", "col2", "col3"))

        #self.grid_funcsel.bind("<Double-Button-1>", self.DobleClickGrid)
        # use lambda para asi poder pasar parametro con la tabla
        self.grid_funcsel.bind("<Double-Button-1>", lambda e: self.DobleClickGrid(e, xtabla))

        self.grid_funcsel.column("#0", width=20, anchor=CENTER, minwidth=20)
        self.grid_funcsel.column("col1", width=300, anchor=CENTER, minwidth=270)
        self.grid_funcsel.column("col2", width=150, anchor=CENTER, minwidth=120)
        self.grid_funcsel.column("col3", width=150, anchor=CENTER, minwidth=120)

        self.grid_funcsel.heading("#0", text="Id", anchor=CENTER)
        self.grid_funcsel.heading("col1", text=titu1, anchor=CENTER)
        self.grid_funcsel.heading("col2", text=titu2, anchor=CENTER)
        self.grid_funcsel.heading("col3", text=titu3, anchor=CENTER)

        self.grid_funcsel.tag_configure('oddrow', background='light green')
        self.grid_funcsel.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_select, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_select, orient=VERTICAL)
        self.grid_funcsel.config(xscrollcommand=scroll_x.set)
        self.grid_funcsel.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_funcsel.xview)
        scroll_y.config(command=self.grid_funcsel.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_funcsel['selectmode'] = 'browse'

        self.grid_funcsel.pack(side=TOP, fill=BOTH, expand=1, padx=0, pady=0)
        self.frame_select.pack(side=TOP, fill=BOTH, padx=0, pady=0)

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
        retorno = self.buscar_entabla(que_busco) # el primero delretorno es el Id

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

                self.grid_funcsel.insert("", END, tags=color, text=reto[0], values=(reto[valor1], reto[valor2],
                                                                                        round(precio_venta, 2)))
            else:
                self.grid_funcsel.insert("", END, tags=color, text=reto[0], values=(reto[valor1], reto[valor2],
                                                                                        reto[valor3]))

        if len(self.grid_funcsel.get_children()) > 0:
            self.grid_funcsel.selection_set(self.grid_funcsel.get_children()[0])

        # --------------------------------------------------------------------------
        # BOTONES

        self.frame_botones_select=LabelFrame(self.sel_item, text="", foreground="#CF09BD")

        # Aca llamo a la funcion que me devuelve el registro completo
        self.btn_seleccion_sel = Button(self.frame_botones_select, text="Seleccionar",
                                        command=lambda:self.fSelec_sel_item(xtabla), width=22, bg="grey", fg="white")
        self.btn_seleccion_sel.grid(row=0, column=0, padx=5, pady=2)

        # self.btn_cancelar_sel = Button(self.frame_botones_select, text="Volver", command=self.fCerrar, width=22,
        # bg="grey", fg="white")
        self.btn_cancelar_sel = Button(self.frame_botones_select, text="Volver", command=lambda :self.fVuelvo_nada(),
                                       width=22, bg="grey", fg="white")
        self.btn_cancelar_sel.grid(row=0, column=1, padx=5, pady=2)

        self.frame_botones_select.pack(side=TOP, padx=0, pady=0)

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

    #------------------------------------------------------------------------------
    # VALIDACIONES
    #------------------------------------------------------------------------------

    """ Valida los caracteres que ingresan en los campos numericos - solo numeros, punto y guion. """

    def validar(self, value):
        codigo = value
        for i in codigo:
            if i not in '0123456789.-':
                return  False
        return True
