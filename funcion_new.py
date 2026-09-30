import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from tkinter import ttk
import traceback
import mysql.connector


class ClaseFuncionNew:

    #def __init__(self, root, objeto):
    def __init__(self, root):

        self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")

        """ Por aca recibe primero la pantalla para que me funcione bien el parent en los messagebox. Luego tambien
        recibo el objeto instanciado  en el programa que llama la funcion (clientes, proveedores, articulos ... )
        y de esta manera poder usar su correspondiente ABM (clientes_ABM, proved_ABM ... ) """

        self.master = root

    @staticmethod
    def get_connection():

        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")


    """
    ------------------------------------------------------------------------------
    # 1 - formatear_cifra - Toma una cifra y le pone los puntos de los miles y las 
          comas decimales - cifra debe venir tipo numerico
    ------------------------------------------------------------------------------
    """
    @staticmethod
    def formatear_cifra(cifra):
        numero = cifra
        salida1 = "{:,.2f}".format(numero)
        salida2 = salida1.replace(',', 'n')
        salida3 = salida2.replace('.', ',')
        salida4 = salida3.replace('n', '.')
        return salida4
   # ------------------------------------------------------------------------------


    """
    --------------------------------------------------------------------------
    2 - FECHA_ES Toma una fecha en formato 2025-12-26 (tabla) y la devuelve 26/12/2026 (string-uso en sistema)
        Ya tanmbien la tengo hecha en funciones como 'fecha_str_reves_normal(self, par, con_hora=False):' 
    --------------------------------------------------------------------------
    """
    @staticmethod
    def fecha_es(par, con_hora=False):

        try:
            if con_hora:
                formato_entrada = '%Y-%m-%d %H:%M'
                formato_salida = '%d/%m/%Y %H:%M'
            else:
                formato_entrada = '%Y-%m-%d'
                formato_salida = '%d/%m/%Y'

            fecha_dt = datetime.strptime(par, formato_entrada)
            return fecha_dt.strftime(formato_salida)
        except ValueError:
            return ""  # o podrías devolver None o lanzar error
    # ------------------------------------------------------------------------------


    """
    --------------------------------------------------------------------------
    1 - FECHA_A_TABLA - Toma una fecha en formato normal 2025/12/26 (tabla) y la devuelve 2026-12-26 (uso en tablas)
    --------------------------------------------------------------------------
    """
    @staticmethod
    def fecha_a_tabla(fecha_str):
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M:%S")
            return fecha.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None  # o podés lanzar error si preferís
    # ---------------------------------------------------------------------------



    # ---------------------------------------------------------------------------
    # BLOQUE DE TRES FUNCIONES JUNTAS
    # Las proximas tres trabajan combinadas validando una fecha de entrada
    # ---------------------------------------------------------------------------
    """
    --------------------------------------------------------------------------
    1 - VALIDAR_FECHA - Valida formato de las fechas y su logica
    --------------------------------------------------------------------------
    """
    def validar_fecha(self, sv_fecha, widget=None):

        fecha = sv_fecha.get()

        retorno = self.valida_fechas(fecha, widget)

        if retorno in ("", "N", "BLANCO"):
            widget.focus_set()
            return "break"

        sv_fecha.set(retorno)
        return retorno

    # Es llamada por la anterior
    def valida_fechas(self, fecha_string, widget=None):

        if not fecha_string:
            self.mensajes_error_fechas("A", widget)
            return ""

        fecha_string = fecha_string.strip()

        # ✅ Caso 1: viene sin barras (ddmmaaaa)
        if len(fecha_string) == 8 and fecha_string.isdigit():
            fecha_string = f"{fecha_string[0:2]}/{fecha_string[2:4]}/{fecha_string[4:8]}"

        # ✅ Caso 2: formato con barras
        elif len(fecha_string) == 10:
            if fecha_string[2] != "/" or fecha_string[5] != "/":
                self.mensajes_error_fechas("C", widget)
                return ""
        else:
            self.mensajes_error_fechas("B", widget)
            return ""

        # ✅ Validación REAL de fecha (incluye bisiestos)
        try:
            fecha = datetime.strptime(fecha_string, "%d/%m/%Y")
        except ValueError:
            self.mensajes_error_fechas("E", widget)
            return ""

        # ✅ Control de año
        ano_actual = datetime.today().year

        if abs(fecha.year - ano_actual) > 5:
            sigue = self.mensajes_error_fechas("F", widget)
            if sigue != "S":
                return "N"
        return fecha.strftime("%d/%m/%Y")

    @staticmethod
    def mensajes_error_fechas(tipo_error, widget):

        mensajes = {
            "A": "La fecha no puede ser vacía",
            "B": "Cantidad de caracteres de fecha erróneos",
            "C": "Separadores incorrectos - use (dd/mm/aaaa)",
            "D": "Caracteres inválidos - use solo números",
            "E": "Fecha inválida - verifique día/mes/año",
        }

        if tipo_error in mensajes:
            messagebox.showerror("Error", mensajes[tipo_error], parent=widget.winfo_toplevel())
            return "N"

        if tipo_error == "F":
            return "S" if messagebox.askyesno(
                "Verifique",
                "Diferencia grande con el año actual. ¿Continuar?",
                parent=widget.winfo_toplevel()
            ) else "N"
    # ---------------------------------------------------------------------------
    # CIERRA BLOQUE DE TRES FUNCIONES
    # ---------------------------------------------------------------------------


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
    @staticmethod
    def mostrar_toast(pantalla_padre, mensaje, pa_color, duracion=3000, tipo="info"):

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
    # ---------------------------------------------------------------------------


    """
    ------------------------------------------------------------------------------
    1 - MOVER PUNTERO top end
    ------------------------------------------------------------------------------
    """
    @staticmethod
    def mover_puntero_topend(tree, posicion):

        items = tree.get_children()
        if not items:
            return
        item = items[0] if posicion == 'TOP' else items[-1]
        tree.focus_set()
        tree.selection_set(item)
        tree.focus(item)
        tree.see(item)
    # ---------------------------------------------------------------------------


    """
    --------------------------------------------------------------------------
    1 - MOSTRAR_ERROR - Captura los errores y me los muestra con detalle para que pueda entender 
        el error y saber donde esta
    --------------------------------------------------------------------------
    """
    def mostrar_error(self, titulo="Error del sistema"):
        tipo, valor, tb = sys.exc_info()

        # Ir hasta la última llamada del traceback
        while tb.tb_next:
            tb = tb.tb_next

        archivo = os.path.basename(tb.tb_frame.f_code.co_filename)
        ruta = tb.tb_frame.f_code.co_filename
        funcion = tb.tb_frame.f_code.co_name
        linea = tb.tb_lineno

        texto_traceback = traceback.format_exc()

        mensaje = (
            f"Tipo de error : {tipo.__name__}\n\n"
            f"Archivo       : {archivo}\n"
            f"Función       : {funcion}\n"
            f"Línea         : {linea}\n\n"
            f"Descripción:\n{valor}\n\n"
            f"{'-' * 50}\n"
            f"Traceback completo:\n{texto_traceback}"
        )

        print("\n" + "=" * 70)
        print(titulo)
        print("=" * 70)
        print(f"Ruta      : {ruta}")
        print(f"Archivo   : {archivo}")
        print(f"Función   : {funcion}")
        print(f"Línea     : {linea}")
        print(f"Tipo      : {tipo.__name__}")
        print(f"Error     : {valor}")
        print(texto_traceback)
        print("=" * 70)

        messagebox.showerror(titulo, mensaje, parent=self.master)
    # ---------------------------------------------------------------------------


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
        self.sel_item.protocol("WM_DELETE_WINDOW", self.fcerrar)
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

        self.grid_funcsel.bind("<Double-Button-1>", lambda e: self.doble_click_grid(e, xtabla))

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
                  command=lambda: self.fselec_sel_item(xtabla)).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Volver", width=20, command=self.fvuelvo_nada).grid(row=0, column=1, padx=5)

        # ESPERA (reemplaza mainloop) ------------------------------------------------
        self.master.wait_window(self.sel_item)

        return self.todo_el_registro

    def doble_click_grid(self, _event, la_tabla):
        self.fselec_sel_item(la_tabla)

    def fvuelvo_nada(self):
        # Boton de opcion volver
        self.todo_el_registro = ""
        self.fcerrar()

    def fselec_sel_item(self, ztabla):

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

        self.fcerrar()

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

    def limpiar_grid_sel(self):
        for item in self.grid_funcsel.get_children():
            self.grid_funcsel.delete(item)

    def fcerrar(self):

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

    # ---------------------------------------------------------------------------
    # FIN METODO SEL
    # ---------------------------------------------------------------------------



    """
    --------------------------------------------------------------------------
    1 - VALIDAR - Valida los Entrys numericos 
        No se llaman entre si pero funcionan juntas. Una controla los caracteres que se ingresan 
        y la otra pone cero si queda un punto o un guion solos
    --------------------------------------------------------------------------
    """
    @staticmethod
    def validar(value):
        if value == "":
            return True
        for c in value:
            if c not in "0123456789.-":
                return False
        if value.count("-") > 1 or ("-" in value and not value.startswith("-")):
            return False
        if value.count(".") > 1:
            return False
        return True
    # ------------------------------------------------------------------------------
    """
        Función original: se usa específicamente con un widget Entry.
        Lee el valor del Entry, lo corrige usando corregir_valor(),
        y vuelve a escribir el resultado en el Entry.
        # funcionan juntas para los entrys y solo corregir_valor para los stringvars
    """
    def corregir_al_salir(self, entry):
        valor = entry.get()
        texto_final = self.corregir_valor(valor)
        entry.delete(0, tk.END)
        entry.insert(0, texto_final)

    @staticmethod
    def corregir_valor(valor):
        """
        Función 'pura': recibe un valor (string, o lo que devuelva un StringVar/Entry),
        y devuelve el string ya corregido y formateado a 2 decimales.
        No toca ningún widget — se puede usar con Entry, StringVar, o un cálculo suelto.
        """
        if valor in ("", "-", ".", "-.", None):
            return "0.00"
        try:
            numero = float(valor)
            return f"{numero:.2f}"
        except (ValueError, TypeError):
            return "0.00"
    # -----------------------------------------------------------------------------


    # def control_numerico(self, value, quepongo):
    #
    #     Intenta convertir value a float. Si no puede, o si el resultado es 0,
    #     devuelve quepongo. Si puede y es distinto de 0, devuelve el valor
    #     absoluto redondeado a 2 decimales.
    #
    #     try:
    #         num = float(value)
    #     except ValueError:
    #         return quepongo
    #     if num == 0:
    #         return quepongo
    #     return round(abs(num), 2)
