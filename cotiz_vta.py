import os
import tkinter.font as tkFont
from datetime import date
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from fontTools.ttLib.tables.S__i_l_f import Pass
from PDF_clase import *
from cotiz_ABM import datosCotiz
from funcion_new import ClaseFuncion_new
from funciones import *

# =========================================================================================
# CLASE PRINCIPAL
# =========================================================================================

class VentasPrincipal(tk.Frame):  # <--- Sin (tk.Tk) ni (tk.Tk, master=None)
    """Clase para la ventana de Cotizaciones - Ventas con pestañas."""

    def __init__(self, master=None):  # <--- Asegúrate de agregar 'master' aquí

        super().__init__(master)
        self.master = master

        # ------------------------------------------------------------------------
        # CONFIGURACIÓN Y CENTRADO DE PANTALLA
        # ------------------------------------------------------------------------
        self.master.resizable(0, 0)

        # Forzamos a Tkinter a procesar tareas pendientes antes de medir la pantalla
        self.master.update_idletasks()

        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()

        # Asigno fijo un ancho y un alto
        ancho_ventana = 1030
        alto_ventana = 650

        # Coordenadas para centrar la ventana
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # CORRECCIÓN: Ajustamos el número a 210 para que entre "Ventas" completa
        # -----------------------------------------------------------------------
        style = ttk.Style()
        style.theme_use('clam')

        # Bajamos de 230 a 216 para darles el tamaño justo sin que se corten
        style.configure('TNotebook.Tab', padding=[216, 8, 216, 8], font=('Arial', 10, 'bold'))

        # Mantenemos el bloqueo del estado seleccionado con el nuevo número
        style.map('TNotebook.Tab', padding=[('selected', [216, 8, 216, 8])])

        # --- CONFIGURACIÓN DE COLOR SEGURA -------------------------------------
        # Usamos el gris claro estándar directamente para no romper el layout
        style.configure('TNotebook.Tab', background='#a0a0a0')
        style.map('TNotebook.Tab', background=[('selected', '#f0f0f0'), ('active', '#f0f0f0')])
        # -----------------------------------------------------------------------

        # Instanciaciones -------------------------------------------------------
        self.varCotiz = datosCotiz(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # -----------------------------------------------------------------------

        # Pestañas --------------------------------------------------------------
        # 1. Crear el contenedor de pestañas (Notebook) usando self.master
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        # 2. Instanciar las pestañas
        self.pestana_1 = PestanaUno(self.notebook, funciones=self.varFuncion_new, datos=self.varCotiz)
        self.pestana_2 = PestanaDos(self.notebook)

        # 3. Añadir las pestañas al contenedor
        self.notebook.add(self.pestana_1, text="Ventas")
        self.notebook.add(self.pestana_2, text="Detalle de ventas")
        # -----------------------------------------------------------------------


# =========================================================================================
# PESTAÑA UNO
# =========================================================================================

class PestanaUno(tk.Frame):

    def __init__(self, master=None, funciones=None, datos=None):

        super().__init__(master)

        # Para que sean visibles dentro de esta clase Pestana1
        self.varFuncion_new = funciones
        self.varCotiz = datos

        # Es una línea automatizada para mimetizar colores. En lugar de escribir vos a mano #f0f0f0 o el color
        # que sea, dejas que Python viaje hacia la ventana principal, mire qué color tiene, regrese y pinte
        # la pestaña con ese mismo tono exacto para que toda la pantalla quede perfectamente uniforme.
        # self.configure(bg=self.master.master.cget('bg'))
        # Contenido de la pestaña 1
        #label = ttk.Label(self, text="", font=("Arial", 14), background=self.master.master.cget('bg'))
        # label.pack(pady=2)

        # ---------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------
        # DATOS DE LA VENTA Y DATOS CLIENTE
        self.strvar_nro_venta = tk.StringVar(self, value="0")
        self.strvar_fecha_venta = tk.StringVar(self, value="")
        self.strvar_codigo_cliente = tk.StringVar(self, value="0")
        self.strvar_nombre_cliente = tk.StringVar(self, value="Consumidor Final")
        self.strvar_sit_fiscal = tk.StringVar(self, value="")
        self.strvar_cuit = tk.StringVar(self, value="")

        # TIPOS DE PAGO
        self.strvar_combo_formas_pago = tk.StringVar()
        self.strvar_detalle_pago = tk.StringVar(value="")

        # VALOR DEL DOLAR HOY
        self.strvar_valor_dolar_hoy = tk.StringVar(self, value="0.00")
        self.strvar_tasa_recargo_precio = tk.StringVar(self, value="0")
        self.traer_dolarhoy()  # trae dolar y tasa recargo precio con tarjeta

        self.strvar_buscostring = tk.StringVar(self, value="")

        # Ejecutamos tu secuencia de inicialización adaptada a la Pestaña 1
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla_ventas("") # foco vacio

    def create_widgets(self):

        # MUY IMPORTANTE: Todos tus widgets de esta pestaña deben tener como padre a 'self'
        # Ejemplo: self.boton = ttk.Button(self, text="Guardar Cotización")

        # VARIABLES GENERALES -------------------------------------------------
        # para validar ingresos de numeros en gets numericos
        #self.vcmd = (self.register(self.varFuncion_new.validar), "%P")
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")


        # ---------------------------------------------------------------------
        # CUADROS BOTONES - ENTRYS - GRID
        
        # Contenedor principal
        self.frame_principal = tk.LabelFrame(self, text="", foreground="#CD5C5C")
        self.frame_principal.pack(expand=True, fill="both", padx=5, pady=5)  # O el empaquetado que uses (.grid o .pack)

        # Contenedor GRID Tabla ventas (resuventa)
        self.frame_grid_ventas_realizadas = tk.LabelFrame(self.frame_principal, text="Ventas realizadas", foreground="#CD5C5C")
        self.cuadro_grid_ventas()
        self.frame_grid_ventas_realizadas.pack(side="top", fill="both", padx=5, pady=2)

        # contenedor Botones de busquedas en tabla resuventas GRID encabezado de Ventas
        self.frame_botones_grid_principal = tk.LabelFrame(self.frame_principal, text="", border=5, foreground="black", background="light blue")
        self.cuadro_botones_grid_ventaS()
        self.frame_botones_grid_principal.pack(side="top", fill="both", padx=5, pady=2)

        # Contenedor Botones Crud 
        self.frame_botones_grid_crudresu = tk.LabelFrame(self.frame_principal, text="", border=5, foreground="black", background="light blue")
        self.cuadro_botones_grid_crudresu()
        self.frame_botones_grid_crudresu.pack(side="top", fill="both", padx=5, pady=2)

        # Contenedor ENTRYS del encabezado de la venta TABLA resuventas
        self.frame_entrys_ventas = tk.LabelFrame(self.frame_principal, text="Encabezado de la venta", foreground="blue")
        self.cuadro_entrys_cliente()
        self.frame_entrys_ventas.pack(side="top", fill="both", expand=0, padx=5, pady=3)

        # Contenedor que muestra el Valor del dolar para hoy
        self.frame_valor_dolarhoy = tk.LabelFrame(self.frame_principal, text="", border=5, foreground="black", background="light blue")
        self.cuadro_valor_dolarhoy()
        self.frame_valor_dolarhoy.pack(side="top", fill="both", padx=5, pady=2)
        # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # FUNCIONES CONFIGURACION
    # ---------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo_resuventas = "ORDER BY rv_fecha"
        self.alta_modif = 0
        self.varCotiz.vaciar_auxventas("aux_ventas") # Vacio tabla auxiliar de ventas
        self.habilitar_botones("disabled", "normal", "disabled")
        self.limpiar_entrys("todo")
        self.habilitar_text("disabled")

    def habilitar_text(self, estado):

        self.entry_nombre_cliente.configure(state=estado)
        self.entry_fecha_venta.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)

    def limpiar_entrys(self, parte):

        self.strvar_codigo_cliente.set(value="0")
        self.strvar_nombre_cliente.set(value="Consumidor Final")
        self.combo_sit_fiscal_cliente.current(0)
        self.strvar_cuit.set(value="")

    def fShowall(self):

        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')
        self.filtro_activo_resuventas = "ORDER BY rv_fecha"
        self.llena_grilla_ventas(self.clave)

    def habilitar_botones(self, estado1, estado2, estado3):

        self.btn_bus_cli.configure(state=estado1)
        self.btn_showall.configure(state=estado2)
        self.btn_buscar.configure(state=estado2)
        self.entry_busqueda_venta.configure(state=estado2)

        self.btn_nueva_venta.configure(state=estado2)
        self.btn_edito_venta.configure(state=estado2)
        self.btn_borro_venta.configure(state=estado2)

    def fReset_venta(self):
        # Boton CANCELAR
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.fReiniciar_todo()
            # Debo reiniciar tambien lo que se haya hecho en la pestaña dos

    def fReiniciar_todo(self):

        # 2 - Desactivar campos y botones
        self.habilitar_text("disabled")
        self.habilitar_botones("disabled", "normal", "browse")

        # Debo reiniciar tambien lo que se haya hecho en la pestaña dos

        # Vaciar auxvenas y  hacer memoria que mas tambien

        # 3 - Poner en cero totales grupales
        # self.strvar_global_final_venta_neto.set(value="0.00")
        # self.strvar_global_final_venta_iva21.set(value="0.00")
        # self.strvar_global_final_venta_iva105.set(value="0.00")
        # self.strvar_global_final_venta.set(value="0.00")

        self.limpiar_entrys("todo")

        una_fecha = date.today()
        self.strvar_fecha_venta.set(value=una_fecha.strftime('%d/%m/%Y'))

        # buscar numero de venta
        self.strvar_nro_venta.set(value=str(int(self.varCotiz.traer_ultimo(1)) + 1))

    def traer_dolarhoy(self):
        dev_informa = self.varCotiz.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])
            self.strvar_tasa_recargo_precio.set(value=row[23])

    # ---------------------------------------------------------------------
    # GRIDS
    # ---------------------------------------------------------------------

    def llena_grilla_ventas(self, set_foco):

        # limpia al GRID de las ventas ya realizadas o historicas (principal)
        for item in self.grid_tvw_todaslasventas.get_children():
            self.grid_tvw_todaslasventas.delete(item)

        datos = self.varCotiz.consultar_tablas("resu", self.filtro_activo_resuventas)

        cont = 0
        for row in datos:
            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_tvw_todaslasventas.insert("", "end", tags=color, text=row[0], values=(row[1], row[2],
                                                                                            row[4], row[10], row[7], row[8]))

        # Controles --------------------------------------------------------
        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_tvw_todaslasventas.get_children()
        # Si no hay filas (grid vacio), salgo sin intentar seleccionar
        if not children:
            return

        # Si foco vacío (no hay foco), voy al ultimo de la grilla - caso contrario, voy a la clave que se haya enviado
        # en set_foco para dejar el puntero
        if not set_foco:
            # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
            posicion = children[-1]  # ultimo
            # posicion = children[0] # primero
            self.grid_tvw_todaslasventas.selection_set(posicion)
            self.grid_tvw_todaslasventas.see(posicion)
        else:
            for item in children:
                texto = self.grid_tvw_todaslasventas.item(item, "text")
                print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    print("aca entro")
                    self.grid_tvw_todaslasventas.update_idletasks()
                    self.grid_tvw_todaslasventas.focus_set()
                    self.grid_tvw_todaslasventas.selection_set(item)
                    self.grid_tvw_todaslasventas.focus(item)
                    self.grid_tvw_todaslasventas.see(item)
                    break

    # ---------------------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------------------

    def fNueva_venta(self):

        self.varCotiz.vaciar_auxventas("aux_ventas")
        self.habilitar_text("normal")
        self.habilitar_botones("normal", "disabled", "none")
        self.strvar_nro_venta.set(value=str(int(self.varCotiz.traer_ultimo(1)) + 1))      # sumo uno a nueva venta
        self.entry_nombre_cliente.focus()

    def fEdito_venta(self):

        # Defino variables
        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')
        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        # Vacio tabla auxiliar
        self.varCotiz.vaciar_auxventas("aux_ventas")

        # preparacion de pantalla de entrada
        self.habilitar_text("normal")
        self.habilitar_botones("normal", "disabled", "none")
        self.entry_nombre_cliente.focus()

        # En la "lista" valores cargo todos los campos de la venta desde el GRID
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')

        # Asigno el numero de venta
        self.strvar_nro_venta.set(value=valores[0])

        # Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta en las variables
        datos_resuventa = self.varCotiz.traer_resu_venta(self.strvar_nro_venta.get())

        fechapaso = datos_resuventa[2].strftime('%d/%m/%Y')
        self.strvar_fecha_venta.set(fechapaso)
        self.strvar_codigo_cliente.set(value=datos_resuventa[3])
        self.strvar_nombre_cliente.set(value=datos_resuventa[4])
        self.strvar_sit_fiscal.set(value=datos_resuventa[5])
        self.strvar_cuit.set(value=datos_resuventa[6])
        self.strvar_combo_formas_pago.set(value=datos_resuventa[7])
        self.strvar_detalle_pago.set(value=datos_resuventa[8])

        # Cargar los articulos que componen la venta de (deta_venta) - items en la "tabla auxventas"
        # Los traigo desde la TABLA detaventas a la TABLA auxventas para poder mostrarlos en el GRID auxiliar
        datos_detaventa = self.varCotiz.traer_deta_venta(self.strvar_nro_venta.get())

        for row in datos_detaventa:             # INSERTO ARTICULO EN AUXILIAR DE VENTA (aux_ventas)

            self.varCotiz.insertar_auxventa(row[2],  # codigo de articulo
                                            row[3],  # descripcion de articulo
                                            row[4],  # marca
                                            row[5],  # cantidad vendida
                                            row[6],  # total pesos unidad de contado
                                            row[7],  # total pesos unidad precio de lista
                                            row[8],  # pesos neto por unidad
                                            row[9],  # pesos iva 21 %
                                            row[10],  # pesos iva 10.5
                                            row[11],  # ganancia por unidad
                                            row[12],  # costo bruto por unidad
                                            row[13],  # costo dolar unidad neto
                                            row[14])  # tasa del IVA 21 / 10.5




        # Tengo que hacer porque aui estaria llenando datos de la pestaña dos

        #    self.calcular("totalventa")

        # self.llena_grilla_ventas(self.clave)
        print("llena_grilla_auxiliar" + " " + str(self.clave))
        # self.llena_grilla_auxiliar(self.clave)





    def fBorro_venta(self):

        # Se borra la venta total - RESU_VENTAS y DETA_VENTAS

        # ------------------------------------------------------------------------------
        # Obtengo valores a las variables
        # selecciono el Id del GRID para su uso posterior
        self.selected = self.grid_tvw_todaslasventas.focus()
        self.selected_ant = self.grid_tvw_todaslasventas.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no son el mismo que el grid)
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')
        self.clave_ant = self.grid_tvw_todaslasventas.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[2]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar Venta?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        # Elimino de resu_vents y deta_ventas
        # self.varCotiz.eliminar_resuventa(self.clave)
        # self.varCotiz.eliminar_detaventa(valores[0])

        # messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        # self.llena_grilla_ventas(self.clave_ant)

    # ---------------------------------------------------------------------
    # BUSQUEDAS Y MOVIMIENTOS EN EL GRID
    # ---------------------------------------------------------------------

    def DobleClickGrid(self, event):
        self.fEdito_venta()

    def fBuscar_resuventa(self):

        if len(self.strvar_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        # se_busca = self.strvar_buscostring.get()
        # self.filtro_activo_resuventas = "WHERE INSTR(rv_cliente, '" + se_busca + "') ORDER BY rv_fecha ASC"
        #
        # self.varCotiz.buscar_entabla(self.filtro_activo)
        # self.llena_grilla_ventas("")
        #
        # """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el
        # item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        # item = self.grid_tvw_todaslasventas.selection()
        # self.grid_tvw_todaslasventas.focus(item)

    def fBuscli(self):

        Pass

        # """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
        #     en que campos debe hacerse """
        #
        # que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
        #             + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
        #             + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
        #             + " ORDER BY apenombre"
        #
        # """ Llamo a Funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de como
        #     quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """
        #
        # valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
        #                                                 "direccion", "Apellido y nombre", "Codigo", "Direccion",
        #                                                 que_busco,
        #                                                 "Orden: Alfabetico cliente", "N")
        #
        # """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a
        #     los Entrys correspondientes """
        #
        # for item in valores_new:
        #     self.strvar_nombre_cliente.set(value=item[15])
        #     self.strvar_codigo_cliente.set(value=item[1])
        #     # self.strvar_cli_datosmas.set(value=str(item[4] + ' - tel: ' + item[8] + ' / ' + item[9]))
        #
        # self.entry_nombre_cliente.focus()
        # self.entry_nombre_cliente.icursor(tk.END)

    def fToparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_tvw_todaslasventas, 'TOP')

    def fFinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_tvw_todaslasventas, 'END')

    # ---------------------------------------------------------------------
    # CUADROS
    # ---------------------------------------------------------------------

    def cuadro_grid_ventas(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_ventas_realizadas)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_todaslasventas = ttk.Treeview(self.frame_grid_ventas_realizadas, height=6,
                                                    columns=("col1", "col2", "col3", "col4", "col5", "col6"))

        self.grid_tvw_todaslasventas.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_tvw_todaslasventas.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_tvw_todaslasventas.column("col1", width=100, anchor="w", minwidth=100)
        self.grid_tvw_todaslasventas.column("col2", width=80, anchor="w", minwidth=80)
        self.grid_tvw_todaslasventas.column("col3", width=350, anchor="center", minwidth=350)
        self.grid_tvw_todaslasventas.column("col4", width=100, anchor="center", minwidth=100)
        self.grid_tvw_todaslasventas.column("col5", width=100, anchor="center", minwidth=100)
        self.grid_tvw_todaslasventas.column("col6", width=130, anchor="center", minwidth=130)

        self.grid_tvw_todaslasventas.heading("#0", text="Id", anchor="center")
        self.grid_tvw_todaslasventas.heading("col1", text="Nº Venta", anchor="w")
        self.grid_tvw_todaslasventas.heading("col2", text="Fecha", anchor="w")
        self.grid_tvw_todaslasventas.heading("col3", text="Cliente", anchor="center")
        self.grid_tvw_todaslasventas.heading("col4", text="Total venta", anchor="center")
        self.grid_tvw_todaslasventas.heading("col5", text="Forma pago", anchor="center")
        self.grid_tvw_todaslasventas.heading("col6", text="Detalle pago", anchor="center")

        self.grid_tvw_todaslasventas.tag_configure('oddrow', background='light grey')
        self.grid_tvw_todaslasventas.tag_configure('evenrow', background='light blue')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_grid_ventas_realizadas, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_grid_ventas_realizadas, orient="vertical")
        self.grid_tvw_todaslasventas.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_todaslasventas.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_todaslasventas.xview)
        scroll_y.config(command=self.grid_tvw_todaslasventas.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_tvw_todaslasventas['selectmode'] = 'browse'

        self.grid_tvw_todaslasventas.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def cuadro_botones_grid_ventaS(self):

        for c in range(4):
            self.frame_botones_grid_principal.grid_columnconfigure(c, weight=1, minsize=120)

        img = Image.open("buscar2.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.lbl_busqueda_venta = tk.Label(self.frame_botones_grid_principal, text=" Venta a buscar: ", justify="left",
                                           bg="light blue", compound="left")
        self.lbl_busqueda_venta.image = icono
        self.lbl_busqueda_venta.config(image=icono)
        self.lbl_busqueda_venta.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_busqueda_venta = tk.Entry(self.frame_botones_grid_principal, textvariable=self.strvar_buscostring,
                                             state='normal', width=50, justify="left", bg="light blue")
        self.entry_busqueda_venta.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        img = Image.open("buscar2.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_buscar = tk.Button(self.frame_botones_grid_principal, text=" Buscar", command=self.fBuscar_resuventa,
                                    width=31, bg='#5F9EA0', fg='white', compound="left")
        self.btn_buscar.image = icono
        self.btn_buscar.config(image=icono)
        self.btn_buscar.grid(row=0, column=2, padx=3, pady=2, sticky=tk.W)

        img = Image.open("ver_todo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_showall = tk.Button(self.frame_botones_grid_principal, text=" Mostrar todo", command=self.fShowall,
                                     width=31, bg='#5F9EA0', fg='white', compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=3, pady=2, sticky=tk.W)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_botones_grid_principal, text="", image=self.photo4,
                                    command=self.fToparch, bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=4, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_botones_grid_principal, text="", image=self.photo5,
                                    command=self.fFinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=5, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid_principal.winfo_children():
            widg.grid_configure(padx=3, pady=2, sticky='nsew')

    def cuadro_botones_grid_crudresu(self):

        for c in range(4):
            self.frame_botones_grid_crudresu.grid_columnconfigure(c, weight=1, minsize=120)

        img = Image.open("archivo-nuevo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_nueva_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Nueva Venta",
                                         command=self.fNueva_venta, width=12, bg='blue', fg='white', compound="left")
        self.btn_nueva_venta.image = icono
        self.btn_nueva_venta.config(image=icono)
        self.btn_nueva_venta.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)

        img = Image.open("editar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_edito_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Editar Venta",
                                         command=self.fEdito_venta, width=12, bg='blue', fg='white', compound="left")
        self.btn_edito_venta.image = icono
        self.btn_edito_venta.config(image=icono)
        self.btn_edito_venta.grid(row=0, column=1, padx=3, pady=2, sticky=tk.W)

        img = Image.open("eliminar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_borro_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Borrar Venta",
                                         command=self.fBorro_venta, width=12, bg='blue', fg='white', compound="left")
        self.btn_borro_venta.image = icono
        self.btn_borro_venta.config(image=icono)
        self.btn_borro_venta.grid(row=0, column=2, padx=3, pady=2, sticky=tk.W)

        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_reset_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Cancelar Venta", command=self.fReset_venta,
                                         width=19, bg='black', fg='white', compound="left")
        self.btn_reset_venta.image = icono
        self.btn_reset_venta.config(image=icono)
        self.btn_reset_venta.grid(row=0, column=3, padx=3, pady=2, sticky=tk.W)

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid_crudresu.winfo_children():
            widg.grid_configure(padx=3, pady=2, sticky='nsew')

    def cuadro_entrys_cliente(self):

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        www = tkFont.Font(family="Arial", size=10, weight="bold")

        for c in range(10):
            self.frame_entrys_ventas.grid_columnconfigure(c, weight=1, minsize=70)

        # NUMERO DE VENTA
        self.strvar_nro_venta.set(value=str(int(self.varCotiz.traer_ultimo(1)) + 1))
        self.lbl_texto_nro_venta = tk.Label(self.frame_entrys_ventas, text="Nº Vta: ", font=fff, fg="black", justify="left")
        self.lbl_texto_nro_venta.grid(row=0, column=0, padx=1, pady=2, sticky='nsew')
        self.lbl_nro_venta = tk.Label(self.frame_entrys_ventas, textvariable=self.strvar_nro_venta, font=fff, fg="black", width=4)
        self.lbl_nro_venta.grid(row=0, column=1, padx=2, pady=2, sticky='nsew')

        # FECHA DE VENTA
        una_fecha = date.today()
        self.strvar_fecha_venta.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.lbl_texto_fecha_venta = tk.Label(self.frame_entrys_ventas, text="Fecha: ", justify="left")
        self.lbl_texto_fecha_venta.grid(row=0, column=2, padx=2, pady=2, sticky='nsew')
        self.entry_fecha_venta = tk.Entry(self.frame_entrys_ventas, textvariable=self.strvar_fecha_venta, width=7,
                                          justify="right")
        self.entry_fecha_venta.grid(row=0, column=3, padx=2, pady=2, sticky='nsew')
        #self.entry_fecha_venta.bind("<FocusOut>", self.formato_fecha)

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = tk.Label(self.frame_entrys_ventas, text="Cliente: ", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=4, padx=2, pady=2, sticky='nsew')
        self.entry_nombre_cliente = tk.Entry(self.frame_entrys_ventas, textvariable=self.strvar_nombre_cliente,
                                             width=30)
        self.entry_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky='nsew')

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = tk.Button(self.frame_entrys_ventas, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                     bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=6, padx=2, pady=2, sticky='nsew')

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = tk.Label(self.frame_entrys_ventas, text="")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=2, pady=2, sticky='nsew')
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_entrys_ventas, textvariable=self.strvar_sit_fiscal,
                                                     justify="left", state='readonly', width=25)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky='nsew')

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = tk.Label(self.frame_entrys_ventas, text="CUIT:", justify="left")
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=2, pady=2, sticky=tk.W)
        self.entry_cuit_cliente = tk.Entry(self.frame_entrys_ventas, textvariable=self.strvar_cuit, justify="right",
                                           width=12)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=2, pady=2, sticky='nsew')

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_entrys_ventas.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')

    def cuadro_valor_dolarhoy(self):

        for c in range(2):
            self.frame_valor_dolarhoy.grid_columnconfigure(c, weight=1, minsize=70)

        # COTIZACION DEL DOLAR DEL DIA
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_dolarhoy1 = tk.Label(self.frame_valor_dolarhoy, text="Dolar hoy:", justify="left", font=fff,
                                      foreground="green")
        self.lbl_dolarhoy1.grid(row=0, column=0, padx=4, pady=2, sticky='nsew')
        self.lbl_dolarhoy2 = tk.Label(self.frame_valor_dolarhoy, textvariable=self.strvar_valor_dolar_hoy, width=10,
                                      justify="right", font=fff, foreground="green")
        self.lbl_dolarhoy2.grid(row=0, column=1, padx=4, pady=2, sticky='nsew')

        for widg in self.frame_valor_dolarhoy.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')











# =========================================================================================
# PESTAÑA DOS
# =========================================================================================

class PestanaDos(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.configure(bg=self.master.master.cget('bg'))

        # Contenido de la pestaña 2
        label = ttk.Label(self, text="Detalle Venta", font=("Arial", 14), background=self.master.master.cget('bg'))
        label.pack(pady=7)



        # Ejecutamos tu secuencia de inicialización adaptada a la Pestaña 1
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla_auxiliar("")
        self.llena_grilla_ventas("")

    def create_widgets(self):
        # MUY IMPORTANTE: Todos tus widgets de esta pestaña deben tener como padre a 'self'
        # Ejemplo: self.boton = ttk.Button(self, text="Guardar Cotización")
        pass

    def estado_inicial(self):
        pass

    def llena_grilla_auxiliar(self, condicion):
        pass

    def llena_grilla_ventas(self, condicion):
        pass





# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    app = VentasPrincipal()
    app.mainloop()
