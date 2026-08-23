import os
import tkinter as tk
import tkinter.font as tkfont
from datetime import date
from tkinter import ttk

from PIL import Image, ImageTk

from PDF_clase import PDF
from cotiz_ABM import datosCotiz
from funcion_new import ClaseFuncionNew
from funciones import *
from status_bar import StatusBar


class VentasPrincipal(tk.Frame):  # <--- Sin (tk.Tk) ni (tk.Tk, master=None)
    """Clase para la ventana de Cotizaciones - Ventas con pestañas."""

    def __init__(self, master=None):  # <--- Asegúrate de agregar 'master' aquí

        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)

        # ------------------------------------------------------------------------
        # Variables compartidas de la venta - nro de venta, fecha venta y modo del CRUD(alta o edicion o NADA)
        self.sv_venta_numero = tk.StringVar()
        self.sv_venta_fecha = tk.StringVar()
        self.sv_modo = tk.StringVar(value="NADA")
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # CONFIGURACIÓN Y CENTRADO DE PANTALLA
        self.master.resizable(0, 0)
        # Forzamos a Tkinter a procesar tareas pendientes antes de medir la pantalla
        self.master.update_idletasks()
        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()
        # Asigno fijo un ancho y un alto
        ancho_ventana = 1030
        alto_ventana = 550
        # Coordenadas para centrar la ventana
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # Otros ajuste para las pestañas
        style = ttk.Style()
        style.theme_use('clam')
        # Bajamos de 230 a 216 para darles el tamaño justo sin que se corten
        style.configure('TNotebook.Tab', padding=[216, 8, 216, 8], font=('Arial', 10, 'bold'))
        # Mantenemos el bloqueo del estado seleccionado con el nuevo número
        style.map('TNotebook.Tab', padding=[('selected', [216, 8, 216, 8])])
        # -----------------------------------------------------------------------

        # CONFIGURACIÓN DE COLOR SEGURA -------------------------------------
        # Usamos el gris claro estándar directamente para no romper el layout
        style.configure('TNotebook.Tab', background='#a0a0a0')
        style.map('TNotebook.Tab', background=[('selected', '#f0f0f0'), ('active', '#f0f0f0')])
        # -----------------------------------------------------------------------

        # Instanciaciones -------------------------------------------------------
        self.varCotiz = datosCotiz(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # -----------------------------------------------------------------------

        # Pestañas --------------------------------------------------------------
        # 1. Crear el contenedor de pestañas (Notebook) usando self.master
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")

        # 2. Instanciar las pestañas --------------------------------------------
        #self.pestana_1 = PestanaUno(self.notebook, funciones=self.varFuncion_new, datos=self.varCotiz)
        """ Paso en "self" la clase "VentasPrincipal", asi puedo definir en esta clase todas las funciones y
            variables Que quiera compartir en las dos pestañas"""
        self.pestana_1 = PestanaUno(self.notebook, self) # self seria "clase ventas principal"
        self.pestana_2 = PestanaDos(self.notebook, self)

        # -----------------------------------------------------------------------
        # 3. Añadir las pestañas al contenedor
        self.notebook.add(self.pestana_1, text="Ventas")
        self.notebook.add(self.pestana_2, text="Detalle de ventas")
        # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # Funciones definidas en la clase principal
    # -----------------------------------------------------------------------

    def freiniciar_todo(self):

        # limpiar los Entrys que puedan tener datos cargados
        self.pestana_1.limpiar_entrys_1()
        self.pestana_2.limpiar_entrys_2()

        # - Desactivar entrys en las dos pestañas
        self.pestana_1.habilitar_text_1("disabled")
        self.pestana_2.habilitar_text_2("disabled")

        # - Desactivar botones en las dos pestañas
        self.pestana_1.habilitar_botones_1("disabled", "normal")
        self.pestana_2.habilitar_botones_2("disabled")

        # Vaciar auxvenas y  hacer memoria que mas tambien
        self.varCotiz.vaciar_auxventas("aux_ventas") # Vacio tabla auxiliar de ventas

        # Refrescar grilla auxiliar
        self.pestana_2.llena_grilla_auxiliar()

        # Recoloco la fecha del dia
        una_fecha = date.today()
        self.sv_venta_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))

        # 3 - Poner en cero totales grupales
        self.pestana_2.sv_global_final_venta_neto.set(value="0.00")
        self.pestana_2.sv_global_final_venta_iva21.set(value="0.00")
        self.pestana_2.sv_global_final_venta_iva105.set(value="0.00")
        self.pestana_2.sv_global_final_venta.set(value="0.00")

    def cargar_icono(self, path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def fsalir(self):
        self.winfo_toplevel().destroy()

# =========================================================================================
# PESTAÑA UNO
# =========================================================================================

class PestanaUno(tk.Frame):

    #def __init__(self, master=None, funciones=None, datos=None):
    def __init__(self, parent, principal):

        super().__init__(parent)

        # instancia directamente toda la clase principal y comparto variables y funciones de<finidas en ella
        self.principal = principal

        # ---------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------
        # DATOS DE LA VENTA Y DATOS CLIENTE
        self.principal.sv_venta_fecha = tk.StringVar(self, value="")
        self.sv_codigo_cliente = tk.StringVar(self, value="0")
        self.sv_nombre_cliente = tk.StringVar(self, value="Consumidor Final")
        self.sv_sit_fiscal = tk.StringVar(self, value="")
        self.sv_cuit = tk.StringVar(self, value="")

        # TIPOS DE PAGO
        self.sv_combo_formas_pago = tk.StringVar()
        self.sv_detalle_pago = tk.StringVar(value="")

        # VALOR DEL DOLAR HOY
        self.sv_valor_dolar_hoy = tk.StringVar(self, value="0.00")
        self.sv_tasa_recargo_precio = tk.StringVar(self, value="0")
        self.traer_dolarhoy()  # trae dolar y tasa recargo precio con tarjeta

        self.sv_buscostring = tk.StringVar(self, value="")

        # Ejecutamos tu secuencia de inicialización adaptada a la Pestaña 1
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla_ventas() # foco vacio - sin datos de busqueda

    def create_widgets(self):

        # IMPORTANTE: Todos tus widgets de esta pestaña deben tener como padre a 'self'
        # Ejemplo: self.boton = ttk.Button(self, text="Guardar Cotización")

        # VARIABLES GENERALES -------------------------------------------------
        # para validar ingresos de numeros en gets numericos
        # self.vcmd = (self.register(self.principal.varFuncion_new.validar), "%P")

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
        self.cuadro_botones_grid_ventas()
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
    # Configuracion inicial
    # ---------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo_resuventas = "ORDER BY rv_fecha"
        self.principal.varCotiz.vaciar_auxventas("aux_ventas") # Vacio tabla auxiliar de ventas
        self.habilitar_botones_1("disabled", "normal")
        self.limpiar_entrys_1()
        self.habilitar_text_1("disabled")

    def habilitar_text_1(self, estado):

        self.entry_nombre_cliente.configure(state=estado)
        self.entry_fecha_venta.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)

    def limpiar_entrys_1(self):

        self.sv_codigo_cliente.set(value="0")
        self.sv_nombre_cliente.set(value="Consumidor Final")
        self.combo_sit_fiscal_cliente.current(0)
        self.sv_cuit.set(value="")

    def fshowall(self):

        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')
        self.filtro_activo_resuventas = "ORDER BY rv_fecha"
        self.llena_grilla_ventas(self.clave) # paso solo el foco sin datos de busqueda

    def habilitar_botones_1(self, estado1, estado2):

        self.btn_bus_cli.configure(state=estado1)
        self.btn_showall.configure(state=estado2)
        self.btn_buscar.configure(state=estado2)
        self.entry_busqueda_venta.configure(state=estado2)

        self.btn_nueva_venta.configure(state=estado2)
        self.btn_edito_venta.configure(state=estado2)
        self.btn_borro_venta.configure(state=estado2)

        self.btn_imprime_venta.configure(state=estado1)

    def freset_venta(self):
        # Boton CANCELAR
        r = messagebox.askquestion("Cancelar", "Confirma cancelar venta actual?", parent=self)
        if r == messagebox.YES:
            self.principal.freiniciar_todo()
            # Debo reiniciar tambien lo que se haya hecho en la pestaña dos

    def traer_dolarhoy(self):
        dev_informa = self.principal.varCotiz.consultar_informa()
        for row in dev_informa:
            self.sv_valor_dolar_hoy.set(value=row[21])
            self.sv_tasa_recargo_precio.set(value=row[23])




    # ---------------------------------------------------------------------
    # GRIDS
    # ---------------------------------------------------------------------

    def llena_grilla_ventas(self, set_foco="", datos=None):

        """
        :param set_foco: viene el item del grid donde quiero que se ponga el foco
        :param datos: Me lo pasa directamente la funncion buscar en tabla
        """

        # limpia al GRID de las ventas ya realizadas o historicas (principal)
        for item in self.grid_tvw_todaslasventas.get_children():
            self.grid_tvw_todaslasventas.delete(item)

        # Si no me pasaron datos, consulto la base
        if datos is None:
            datos = self.principal.varCotiz.consultar_tablas("resu", self.filtro_activo_resuventas)

        #datos = self.principal.varCotiz.consultar_tablas("resu", self.filtro_activo_resuventas)

        cont = 0
        for row in datos:

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'), False)

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)
            self.grid_tvw_todaslasventas.insert("", "end", tags=color, text=row[0], values=(row[1], forma_normal,
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
            self.grid_tvw_todaslasventas.focus_set()
            self.grid_tvw_todaslasventas.focus(posicion)
            self.grid_tvw_todaslasventas.selection_set(posicion)
            self.grid_tvw_todaslasventas.see(posicion)
        else:
            for item in children:
                texto = self.grid_tvw_todaslasventas.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_tvw_todaslasventas.update_idletasks()
                    self.grid_tvw_todaslasventas.focus_set()
                    self.grid_tvw_todaslasventas.selection_set(item)
                    self.grid_tvw_todaslasventas.focus(item)
                    self.grid_tvw_todaslasventas.see(item)
                    break




    # ---------------------------------------------------------------------
    # BUSQUEDAS y movimientos en el grid
    # ---------------------------------------------------------------------

    def fbuscar_en_resuventa(self):

        if len(self.sv_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.sv_buscostring.get()

        datos = self.principal.varCotiz.buscar_entabla(se_busca)

        self.llena_grilla_ventas(datos=datos) #sin ninguno de los dos param

    def doble_click_grid(self, _event):
        self.fedito_venta()

    def fbuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
            en que campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a Funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de como
            quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.principal.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo", "direccion",
                                                                  "Apellido y nombre", "Codigo", "Direccion",
                                                                   que_busco, "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a
            los Entrys correspondientes """

        for item in valores_new:
            self.sv_nombre_cliente.set(value=item[15])
            self.sv_codigo_cliente.set(value=item[1])
            # self.sv_cli_datosmas.set(value=str(item[4] + ' - tel: ' + item[8] + ' / ' + item[9]))

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    def ftoparch(self):
        self.principal.varFuncion_new.mover_puntero_topend(self.grid_tvw_todaslasventas, 'TOP')

    def ffinarch(self):
        self.principal.varFuncion_new.mover_puntero_topend(self.grid_tvw_todaslasventas, 'END')




    # ---------------------------------------------------------------------
    # CRUD en resu_venta
    # ---------------------------------------------------------------------

    # Desde el boton "Nueva venta" de la pestaña uno
    def fnueva_venta(self):

        self.principal.sv_modo.set(value="ALTA")
        self.principal.varCotiz.vaciar_auxventas("aux_ventas")
        self.habilitar_text_1("normal")
        self.habilitar_botones_1("normal", "disabled")
        self.principal.sv_venta_numero.set(value=str(int(self.principal.varCotiz.traer_ultimo(1)) + 1))   # sumo uno a nueva venta
        self.entry_nombre_cliente.focus()
        # Activo botones en pestaña 2
        self.principal.pestana_2.habilitar_botones_2("normal")

    # Desde el boton de "Editar venta" de la pestaña 1
    def fedito_venta(self):

        # ---------------------------------------------------------------------
        # Defino variables
        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')
        if not self.clave:
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # Inicializo
        self.principal.sv_modo.set(value="EDICION")
        # Vacio tabla auxiliar
        self.principal.varCotiz.vaciar_auxventas("aux_ventas")
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # preparacion de pantalla de entrada
        self.habilitar_text_1("normal")
        self.habilitar_botones_1("normal", "disabled")
        self.entry_nombre_cliente.focus()
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # En la "lista" valores cargo todos los campos de la venta desde el GRID
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')
        # ---------------------------------------------------------------------

        # Asigno el numero de venta
        self.principal.sv_venta_numero.set(value=valores[0])

        # ---------------------------------------------------------------------
        # Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta en las variables
        datos_resuventa = self.principal.varCotiz.traer_resu_venta(self.principal.sv_venta_numero.get())

        fechapaso = datos_resuventa[2].strftime('%d/%m/%Y')
        self.principal.sv_venta_fecha.set(fechapaso)
        self.sv_codigo_cliente.set(value=datos_resuventa[3])
        self.sv_nombre_cliente.set(value=datos_resuventa[4])
        self.sv_sit_fiscal.set(value=datos_resuventa[5])
        self.sv_cuit.set(value=datos_resuventa[6])
        self.sv_combo_formas_pago.set(value=datos_resuventa[7])
        self.sv_detalle_pago.set(value=datos_resuventa[8])
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # Cargar los articulos que componen la venta de (deta_venta) - items en la "tabla auxventas"
        # Los traigo desde la TABLA detaventas a la TABLA auxventas para poder mostrarlos en el GRID auxiliar

        datos_detaventa = self.principal.varCotiz.traer_deta_venta(self.principal.sv_venta_numero.get())

        # Creamos el diccionario para insertar los datos en deta_ventas (detalle de los articulos vendido)
        for row in datos_detaventa:             # INSERTO ARTICULO EN AUXILIAR DE VENTA (aux_ventas)

            dic_detaventas = {
                #"Id": self.clave,
                #"dv_numero": self.sv_venta_numero.get(),
                "av_codigo_art": row[2],
                "av_desc_art": row[3],
                "av_marca_art": row[4],
                "av_cantidad": row[5],
                "av_tot_uni_conta": row[6],
                "av_tot_uni_lista": row[7],
                "av_neto_unidad": row[8],
                "av_impor_iva21": row[9],
                "av_impor_iva105": row[10],
                "av_impor_ganancia": row[11],
                "av_costo_dolar": row[12],
                "av_costo_bruto": row[13],
                "av_tasaiva": row[14]
            }

            #total_ventas += row[5] * row[7]  # precio de lista unitario por cantidad

            self.id_nuevo = self.principal.varCotiz.insertar_auxventa(dic_detaventas)
        # ---------------------------------------------------------------------------------------

        self.principal.pestana_2.calcular("totalventa")

        # Le digo a clase principal que le avise a pestaña_2 que me refresque el grid aux_ventas de la otra pestaña
        self.principal.pestana_2.refrescar_auxventas()

        # Habilitar los botones de ventas en Pestaña dos
        self.principal.pestana_2.habilitar_botones_2("normal")

    # Desde el boton de "Borrar Venta" de la pestaña 1 - Se borra la venta total - RESU_VENTAS y DETA_VENTAS
    def fborro_venta(self):

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
            self.principal.status.set_status("❌ No hay nada seleccionado", "error")
            return

        # guardo todos los valores en una lista desde el Tv ----------------------------
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')
        # ------------------------------------------------------------------------------
        data = str(self.clave) + " " + valores[0] + " " + valores[2]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar Venta?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        try:
            # Elimino todos los items de resu_vents y deta_ventas
            self.principal.varCotiz.eliminar_resuventa(self.clave)
            self.principal.varCotiz.eliminar_detaventa(valores[0])
        except Exception:
            self.principal.varFuncion_new.mostrar_error()
            return
        else:
            self.principal.status.set_status("🗑 Venta eliminada correctamente", "ok")

        self.llena_grilla_ventas(self.clave_ant)




    # ---------------------------------------------------------------------
    # CUADROS
    # ---------------------------------------------------------------------

    # GRID RESU_VENTAS
    def cuadro_grid_ventas(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_ventas_realizadas)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_todaslasventas = ttk.Treeview(self.frame_grid_ventas_realizadas, height=10,
                                                    columns=("col1", "col2", "col3", "col4", "col5", "col6"))

        self.grid_tvw_todaslasventas.bind("<Double-Button-1>", self.doble_click_grid)

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

    def cuadro_botones_grid_ventas(self):

        for c in range(4):
            self.frame_botones_grid_principal.grid_columnconfigure(c, weight=1, minsize=120)

        icono = self.principal.cargar_icono("buscar2.png")
        self.lbl_busqueda_venta = tk.Label(self.frame_botones_grid_principal, text=" Venta a buscar: ", justify="left",
                                           bg="light blue", compound="left")
        self.lbl_busqueda_venta.image = icono
        self.lbl_busqueda_venta.config(image=icono)
        self.lbl_busqueda_venta.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.entry_busqueda_venta = tk.Entry(self.frame_botones_grid_principal, textvariable=self.sv_buscostring,
                                             state='normal', width=50, justify="left", bg="light blue")
        self.entry_busqueda_venta.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        icono = self.principal.cargar_icono("buscar2.png")
        self.btn_buscar = tk.Button(self.frame_botones_grid_principal, text=" Buscar", command=self.fbuscar_en_resuventa,
                                    width=31, bg='#5F9EA0', fg='white', compound="left")
        self.btn_buscar.image = icono
        self.btn_buscar.config(image=icono)
        self.btn_buscar.grid(row=0, column=2, padx=3, pady=2, sticky=tk.W)

        icono = self.principal.cargar_icono("ver_todo.png")
        self.btn_showall = tk.Button(self.frame_botones_grid_principal, text=" Mostrar todo", command=self.fshowall,
                                     width=31, bg='#5F9EA0', fg='white', compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=3, pady=2, sticky=tk.W)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_botones_grid_principal, text="", image=self.photo4,
                                    command=self.ftoparch, bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=4, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_botones_grid_principal, text="", image=self.photo5,
                                    command=self.ffinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=5, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid_principal.winfo_children():
            widg.grid_configure(padx=3, pady=2, sticky='nsew')

    def cuadro_botones_grid_crudresu(self):

        for c in range(6):
            self.frame_botones_grid_crudresu.grid_columnconfigure(c, weight=1, minsize=120)

        icono = self.principal.cargar_icono("archivo-nuevo.png")
        self.btn_nueva_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Nueva Venta",
                                         command=self.fnueva_venta, width=12, bg='blue', fg='white', compound="left")
        self.btn_nueva_venta.image = icono
        self.btn_nueva_venta.config(image=icono)
        self.btn_nueva_venta.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)

        icono = self.principal.cargar_icono("editar.png")
        self.btn_edito_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Editar Venta",
                                         command=self.fedito_venta, width=12, bg='blue', fg='white', compound="left")
        self.btn_edito_venta.image = icono
        self.btn_edito_venta.config(image=icono)
        self.btn_edito_venta.grid(row=0, column=1, padx=3, pady=2, sticky=tk.W)

        icono = self.principal.cargar_icono("eliminar.png")
        self.btn_borro_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Borrar Venta",
                                         command=self.fborro_venta, width=12, bg='blue', fg='white', compound="left")
        self.btn_borro_venta.image = icono
        self.btn_borro_venta.config(image=icono)
        self.btn_borro_venta.grid(row=0, column=2, padx=3, pady=2, sticky=tk.W)

        icono = self.principal.cargar_icono("cancelar.png")
        self.btn_reset_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Cancelar Venta", command=self.freset_venta,
                                         width=19, bg='black', fg='white', compound="left")
        self.btn_reset_venta.image = icono
        self.btn_reset_venta.config(image=icono)
        self.btn_reset_venta.grid(row=0, column=3, padx=3, pady=2, sticky=tk.W)

        icono = self.principal.cargar_icono("impresora.png")
        self.btn_imprime_venta = tk.Button(self.frame_botones_grid_crudresu, text=" Imprime Venta", width=19,
                                           command=self.creopdf, bg='#5F9EF5', fg='white', compound="left")
        self.btn_imprime_venta.image = icono
        self.btn_imprime_venta.config(image=icono)
        self.btn_imprime_venta.grid(row=0, column=4, padx=5, pady=2, sticky=tk.W)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.frame_botones_grid_crudresu, text="Salir", image=self.photo3, width=85,
                                  command=self.principal.fsalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid_crudresu.winfo_children():
            widg.grid_configure(padx=3, pady=2, sticky='nsew')

    def cuadro_entrys_cliente(self):

        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        #www = tkfont.Font(family="Arial", size=10, weight="bold")

        for c in range(10):
            self.frame_entrys_ventas.grid_columnconfigure(c, weight=1, minsize=75)

        # NUMERO DE VENTA
        self.principal.sv_venta_numero.set(value=str(int(self.principal.varCotiz.traer_ultimo(1)) + 1))
        self.lbl_texto_nro_venta = tk.Label(self.frame_entrys_ventas, text="Nº Vta: ", font=fff, fg="black", justify="left")
        self.lbl_texto_nro_venta.grid(row=0, column=0, padx=1, pady=2, sticky='nsew')
        self.lbl_nro_venta = tk.Label(self.frame_entrys_ventas, textvariable=self.principal.sv_venta_numero, font=fff, fg="black", width=4)
        self.lbl_nro_venta.grid(row=0, column=1, padx=2, pady=2, sticky='nsew')

        # FECHA DE VENTA
        una_fecha = date.today()
        self.principal.sv_venta_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.lbl_texto_fecha_venta = tk.Label(self.frame_entrys_ventas, text="Fecha: ", justify="left")
        self.lbl_texto_fecha_venta.grid(row=0, column=2, padx=2, pady=2, sticky='nsew')
        self.entry_fecha_venta = tk.Entry(self.frame_entrys_ventas, textvariable=self.principal.sv_venta_fecha, width=10,
                                          justify="right")
        self.entry_fecha_venta.grid(row=0, column=3, padx=3, pady=2, sticky='nsew')
        #self.entry_fecha_venta.bind("<FocusOut>", self.formato_fecha)

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((20, 20), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = tk.Button(self.frame_entrys_ventas, text="", image=self.photo_bus_cli, command=self.fbuscli,
                                     bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=2, pady=2, sticky='nsew')

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = tk.Label(self.frame_entrys_ventas, text="Cliente: ", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky='nsew')
        self.entry_nombre_cliente = tk.Entry(self.frame_entrys_ventas, textvariable=self.sv_nombre_cliente, width=40)
        self.entry_nombre_cliente.grid(row=0, column=6, padx=2, pady=2, sticky='nsew')

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = tk.Label(self.frame_entrys_ventas, text="")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=2, pady=2, sticky='nsew')
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_entrys_ventas, textvariable=self.sv_sit_fiscal,
                                                     justify="left", state='readonly', width=30)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky='nsew')

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = tk.Label(self.frame_entrys_ventas, text="CUIT:", justify="left")
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=2, pady=2, sticky=tk.W)
        self.entry_cuit_cliente = tk.Entry(self.frame_entrys_ventas, textvariable=self.sv_cuit, justify="right", width=12)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=2, pady=2, sticky='nsew')

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_entrys_ventas.winfo_children():
            widg.grid_configure(padx=5, pady=2, sticky='nsew')

    def cuadro_valor_dolarhoy(self):

        for c in range(2):
            self.frame_valor_dolarhoy.grid_columnconfigure(c, weight=1, minsize=70)

        # COTIZACION DEL DOLAR DEL DIA
        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        self.lbl_dolarhoy1 = tk.Label(self.frame_valor_dolarhoy, text="Dolar hoy:", justify="left", font=fff, foreground="green")
        self.lbl_dolarhoy1.grid(row=0, column=0, padx=4, pady=2, sticky='nsew')
        self.lbl_dolarhoy2 = tk.Label(self.frame_valor_dolarhoy, textvariable=self.sv_valor_dolar_hoy, width=10,
                                      justify="right", font=fff, foreground="green")
        self.lbl_dolarhoy2.grid(row=0, column=1, padx=4, pady=2, sticky='nsew')

        for widg in self.frame_valor_dolarhoy.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')

    # ---------------------------------------------------------------------
    # IMPRESION
    # ---------------------------------------------------------------------

    def creopdf(self):

        # Guardo clave del item del Grid el cual quiero imprimir
        self.selected = self.grid_tvw_todaslasventas.focus()
        # Obtengo la clave de la "base de datos campo Id" que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta)
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')

        if not self.clave:
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """

        # esto siempre debe estar
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 12)
        # -----------------------------------------------------------------------------------

        # armado de encabezado
        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
        self.pdf_numero_venta = self.principal.sv_venta_numero.get()
        self.pdf_codigo_cliente = self.sv_codigo_cliente.get()
        self.pdf_nombre_cliente = self.sv_nombre_cliente.get()

        self.pdf_datos_encabezado_orden = self.pdf_numero_venta + ' - ' + self.pdf_nombre_cliente + ' ( ' + self.pdf_codigo_cliente + ' )'

        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Presupuesto / Nota de Venta ', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Fecha y Hora: ' + feac + '  -  Numero de Venta ' + self.pdf_datos_encabezado_orden,
                 border=1, align='C', fill=0, ln=1)
        # -----------------------------------------------------------------------

        # Espaciado entre cuerpos ------------------------------------
        pdf.cell(w=0, h=4, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Arial', '', 5)

        # Traer todos los registros de la tabla de articulos vendidos deta_ventas
        # self.datos_articulos_vendidos = self.varCotiz.consultar_detalle_auxventas("aux", "")
        self.datos_articulos_vendidos = self.principal.varCotiz.consultar_tablas("deta", "WHERE dv_numero = "+str(self.principal.sv_venta_numero.get()))

        sumotot = 0
        for row in self.datos_articulos_vendidos:
            # Descripcion articulo
            pdf.cell(w=70, h=4, txt=row[3], border=0, align='L', fill=0, ln=0)
            # Marca
            pdf.cell(w=30, h=4, txt=row[4], border=0, align='L', fill=0, ln=0)
            # cantidad
            pdf.cell(w=5, h=4, txt=str(float(row[5])), border=0, align='R', fill=0, ln=0)
            # Precio unidad lista
            pdf.cell(w=10, h=4, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
            # precio unidad lista x cantidad
            pdf.cell(w=10, h=4, txt=str(float(row[7])*float(row[5])), border=0, align='R', fill=0, ln=0)
            sumotot += float(row[7])*float(row[5])
            pdf.cell(w=0, h=4, txt='', align='L', fill=0, ln=1)

        # Total
        pdf.cell(w=0, h=4, txt="Total: " + str(sumotot), border=0, align='R', fill=0, ln=1)

        # mostrar = row[4]
        # cadena = (mostrar[:100])
        # pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0)

        pdf.output('hoja.pdf')

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)






# =========================================================================================
# PESTAÑA DOS
# =========================================================================================

class PestanaDos(tk.Frame):

    def __init__(self, parent, principal):

        super().__init__(parent)
        # Creo una instancia de la clase principal
        self.principal = principal

        #self.configure(bg=self.master.master.cget('bg'))
        # # Contenido de la pestaña 2
        # label = ttk.Label(self, text="Detalle Venta", font=("Arial", 14), background=self.master.master.cget('bg'))
        # label.pack(pady=7)

        # ---------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------

        # Valor del dolar hoy
        self.sv_valor_dolar_hoy = tk.StringVar(value="0.00")
        self.sv_tasa_recargo_precio = tk.StringVar(value="0")

        # Detalles del articulo a vender
        self.sv_it_codigo_articulo = tk.StringVar(value="")
        self.sv_it_descripcion_articulo = tk.StringVar(value="")
        self.sv_it_marca_articulo = tk.StringVar(value="")
        self.sv_it_rubro_articulo = tk.StringVar(value="")
        self.sv_it_ultima_actual = tk.StringVar(value="")

        # cantidad a comprar
        self.sv_cantidad_venta = tk.StringVar(value="1")

        # costo dolares neto articulo unidad
        self.sv_unidad_costo_dolar = tk.StringVar()
        # costo dolares bruto articulo unidad
        self.sv_unidad_costo_dolar_bruto = tk.StringVar(value="0.00")
        # costo pesos bruto articulo unidad
        self.sv_unidad_costo_bruto_pesos = tk.StringVar(value="0.00")
        # Costo pesos NETO articulo unidad
        self.sv_unidad_neto_pesos = tk.StringVar(value="0.00")
        # Costo pesos NETO articulo X cantidad
        # self.sv_xcanti_neto_total = tk.StringVar(value="0.00")

        # Venta pesos final articulo unidad
        self.sv_unidad_precio_venta_contado = tk.StringVar(value="0.00")
        self.sv_unidad_precio_venta_lista = tk.StringVar(value="0.00")
        # Venta pesos final articulo por cantidad
        self.sv_xcanti_total_precio_venta_lista = tk.StringVar(value="0.00")

        # Tasa del iva %
        self.sv_combo_tasa_iva = tk.StringVar()
        # Importe iva articulo (21 o 10.5) unidad
        self.sv_unidad_total_iva = tk.StringVar(value="0.00")
        # Importe iva articulo por la cantidad
        # self.sv_xcanti_total_iva = tk.StringVar(value="0.00")
        # Importe iva del articulo 21% (separo para guardar)
        self.sv_unidad_total_iva_21 = tk.StringVar(value="0.00")
        # Importe iva del articulo 10,5% (separo para guardar)
        self.sv_unidad_total_iva_105 = tk.StringVar(value="0.00")

        # Tasa Ganancia por articulo
        self.sv_unidad_tasa_ganancia = tk.StringVar(value="0.00")
        # Importe ganancia del articulo unidad
        self.sv_unidad_total_ganancia = tk.StringVar(value="0.00")
        # Importe ganancia del articulo X cantidad
        self.sv_xcanti_total_ganancia = tk.StringVar(value="0.00")

        # # TIPOS DE PAGO
        # self.sv_combo_formas_pago = tk.StringVar()
        # self.sv_detalle_pago = tk.StringVar(value="")

        # TOTALES FINALES GLOBALES TODA LA VENTA
        # 1 pago
        self.sv_global_final_venta = tk.StringVar(value="0")
        self.sv_global_final_venta_iva21 = tk.StringVar(value="0")
        self.sv_global_final_venta_iva105 = tk.StringVar(value="0")
        self.sv_global_final_venta_neto = tk.StringVar(value="0")
        # ---------------------------------------------------------------------

        # Ejecutamos tu secuencia de inicialización adaptada a la Pestaña 1
        self.create_widgets()
        self.estado_inicial()

    def create_widgets(self):

        # MUY IMPORTANTE: Todos tus widgets de esta pestaña deben tener como padre a 'self'
        # Ejemplo: self.boton = ttk.Button(self, text="Guardar Cotización")

        # VARIABLES GENERALES -------------------------------------------------
        # para validar ingresos de numeros en gets numericos
        self.vcmd = (self.register(self.principal.varFuncion_new.validar), "%P")

        # Contenedores BOTONES - ENTRYS - GRID --------------------------------

        # Contenedor principal
        self.frame_principal = tk.LabelFrame(self, text="", foreground="#CD5C5C")
        self.frame_principal.pack(expand=True, fill="both", padx=5, pady=5)  # O el empaquetado que uses (.grid o .pack)

        # Contenedor GRID Tabla aux_ventas (auxiliar) para los detalles de articulos vendidos
        self.frame_grid_ventas_articulos = tk.LabelFrame(self.frame_principal, text="Articulos vendidos", foreground="#CD5C5C")
        self.cuadro_grid_articulos()
        self.frame_grid_ventas_articulos.pack(side="top", fill="both", padx=5, pady=2)

        # Contenedor GRID Tabla aux_ventas (auxiliar) para los detalles de articulos vendidos
        self.frame_botones_articulos = tk.LabelFrame(self.frame_principal, text="", border=5, foreground="#CD5C5C")
        self.cuadro_botones_articulos()
        self.frame_botones_articulos.pack(side="top", fill="both", padx=5, pady=10)

        # Contenedor entrys de informacion descriptiva del articulo
        self.frame_entrys_articulos = tk.LabelFrame(self.frame_principal, text="", foreground="#CD5C5C")
        self.cuadro_entrys_articulos()
        self.frame_entrys_articulos.pack(side="top", fill="both", padx=5, pady=3)

        # Contenedor I mportes y cantidades de los articulos vendidos
        self.frame_entrys_importes_articulos = tk.LabelFrame(self.frame_principal, text="", foreground="#CD5C5C")
        self.cuadro_entrys_importes_articulos()
        self.frame_entrys_importes_articulos.pack(side="top", fill="both", padx=5, pady=3)

        # Contenedor Totales y formas de pago
        self.frame_totales_venta = tk.LabelFrame(self.frame_principal, text="Total Venta", border=5, foreground="black")
        self.cuadro_totales_venta()
        self.frame_totales_venta.pack(expand=0, side="top", fill="both", pady=10, padx=5)

        # Contenedor botones de Cierre venta
        self.frame_botones_aux_ventas = tk.LabelFrame(self.frame_principal)
        self.cuadro_botones_aux_ventas()
        self.frame_botones_aux_ventas.pack(expand=0, side="top", fill="both", pady=2, padx=5)
        # ---------------------------------------------------------------------




    # -------------------------------------------------------------------------
    # Inicializacion Pantalla
    # -------------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo_auxventa = "ORDER BY av_desc_art"
        self.alta_modif_p2 = 0

        # traen valor dolar y tasa recargo del precio por tarjeta para los calculos que tenga que hacer en esta pestaña
        self.sv_valor_dolar_hoy.set(value=self.principal.pestana_1.sv_valor_dolar_hoy.get())
        self.sv_tasa_recargo_precio.set(value=self.principal.pestana_1.sv_tasa_recargo_precio.get())

        self.habilitar_botones_2("disabled")
        self.limpiar_entrys_2()
        self.habilitar_text_2("disabled")

    def habilitar_text_2(self, estado):

        self.entry_detalle_movim.configure(state=estado)
        self.entry_cantidad_venta.configure(state=estado)
        self.entry_precio_lista_unidad.configure(state=estado)
        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)
        self.btn_bus_art.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)

    def habilitar_botones_2(self, estado):

        self.btn_ingresar_itemventa.configure(state=estado)
        self.btn_guardar_venta.configure(state=estado)
        self.btn_editar_itemventa.configure(state=estado)
        self.btn_eliminar_itemventa.configure(state=estado)
        self.btn_cerrar_venta.configure(state=estado)
        self.btn_reset_art.config(state=estado)
        self.btn_cancela_art.config(state=estado)

    def limpiar_entrys_2(self):

        # datos del articulo
        self.sv_it_codigo_articulo.set(value="")
        self.sv_it_descripcion_articulo.set(value="")
        self.sv_it_marca_articulo.set(value="")
        self.sv_it_rubro_articulo.set(value="")
        self.sv_it_ultima_actual.set(value="")

        # # Forma de pago
        # self.combo_formapago.current(0)
        # #self.combo_formapago.configure(state="")
        # self.principal.pestana_1.sv_detalle_pago.set(value="")

        # cantidad a comprar
        self.sv_cantidad_venta.set(value="1")

        # costo dolares neto articulo unidad
        self.sv_unidad_costo_dolar.set(value="0.00")
        # costo dolares bruto articulo unidad
        self.sv_unidad_costo_dolar_bruto.set(value="0.00")
        # costo pesos bruto articulo unidad
        self.sv_unidad_costo_bruto_pesos.set(value="0.00")
        # Costo pesos NETO articulo unidad
        self.sv_unidad_neto_pesos.set(value="0.00")
        # Costo pesos NETO articulo X cantidad
        # self.sv_xcanti_neto_total.set(value="0.00")
        # Venta pesos final articulo unidad
        self.sv_unidad_precio_venta_contado.set(value="0.00")
        self.sv_unidad_precio_venta_lista.set(value="0.00")
        # Venta pesos final articulo por cantidad
        self.sv_xcanti_total_precio_venta_lista.set(value="0.00")
        # Tasa del iva %
        #        self.sv_combo_tasa_iva = tk.StringVar()
        self.combo_tasa_iva.current(0)
        # Importe iva articulo (21 o 10.5) unidad
        self.sv_unidad_total_iva.set(value="0.00")
        # Importe iva articulo por la cantidad
        # self.sv_xcanti_total_iva.set(value="0.00")
        # Importe iva del articulo 21% (separo para guardar)
        self.sv_unidad_total_iva_21.set(value="0.00")
        # Importe iva del articulo 10,5% (separo para guardar)
        self.sv_unidad_total_iva_105.set(value="0.00")
        # Tasa Ganancia por articulo
        self.sv_unidad_tasa_ganancia.set(value="0.00")
        # Importe ganancia del articulo unidad
        self.sv_unidad_total_ganancia.set(value="0.00")
        # Importe ganancia del articulo X cantidad
        self.sv_xcanti_total_ganancia.set(value="0.00")

    # Vuelvo a cero lo que se este haciendo en la carga de un articulo actualmente
    def freset_venta_activa(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar carga de articulo actual?", parent=self)
        if r == messagebox.NO:
            return

        #self.fReiniciar_carga_articulo()

    def freset_articulo_activo(self):
        # limpiar los Entrys que puedan tener datos cargados
        self.limpiar_entrys_2()

    def cancelar_articulo(self):
        # limpiar los Entrys que puedan tener datos cargados
        self.limpiar_entrys_2()
        # - Desactivar entrys
        self.habilitar_text_2("disabled")
        self.principal.status.set_status("❌ articulo cancelado", "error")





    # -------------------------------------------------------------------------
    # GRIDS
    # -------------------------------------------------------------------------
    def refrescar_auxventas(self):
        self.llena_grilla_auxiliar()

    def llena_grilla_auxiliar(self, set_foco="", datos=None):

        """
        :param set_foco: viene la clave del item donde quiero poner el foco
        :param datos:  Lo manda la funcion busqueda ya armado el fetchall
        """

        # Limpia grid tabla auxiliar
        for item in self.grid_tvw_auxiliar_venta.get_children():
            self.grid_tvw_auxiliar_venta.delete(item)

        if datos is None:
            datos = self.principal.varCotiz.consultar_tablas("aux", self.filtro_activo_auxventa)

        cont = 0
        totalventa = 0
        for row in datos:
            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)
            self.grid_tvw_auxiliar_venta.insert("", "end", tags=color, text=row[0], values=(row[1], row[2],
                                                            row[3], row[4], row[5], row[6], row[11], row[12], row[13]))

            # Sumariza la columna total por unidad precio lista * cantidad
            totalventa += (row[6] * row[4])
            self.sv_global_final_venta.set(value=str(totalventa))

        # Controles -----------------------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_tvw_auxiliar_venta.get_children()

        # Si no hay filas, salgo sin intentar seleccionar
        if not children:
            return

        # Si hay filas y foco vacío, voy al ultimo de la grilla
        if not set_foco:
            # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
            posicion = children[-1]  # ultimo
            # posicion = children[0] # primero
            # ---------------------------------------
            # esto hace que el item ya quede seleccionado luego del filtrado y presentacion en grilla
            self.grid_tvw_auxiliar_venta.focus_set()
            self.grid_tvw_auxiliar_venta.focus(posicion)
            self.grid_tvw_auxiliar_venta.selection_set(posicion)
            self.grid_tvw_auxiliar_venta.see(posicion)
            # ----------------------------------------
        else:
            for item in children:
                texto = self.grid_tvw_auxiliar_venta.item(item, "text")
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_tvw_auxiliar_venta.update_idletasks()
                    self.grid_tvw_auxiliar_venta.focus_set()
                    self.grid_tvw_auxiliar_venta.selection_set(item)
                    self.grid_tvw_auxiliar_venta.focus(item)
                    self.grid_tvw_auxiliar_venta.see(item)
                    break




    # ---------------------------------------------------------------------
    # Busquedas y movimientos en el Grid
    # ---------------------------------------------------------------------

    def ftoparch(self):
        self.principal.varFuncion_new.mover_puntero_topend(self.grid_tvw_auxiliar_venta, 'TOP')

    def ffinarch(self):
        self.principal.varFuncion_new.mover_puntero_topend(self.grid_tvw_auxiliar_venta, 'END')




    # ----------------------------------------------------------------------------
    # CRUD  -  TODOS
    # ----------------------------------------------------------------------------

    # Bt Guardar Venta - Cerrado de la venta - Guardado definitivo de la nueva venta en las dos tablas(resu_ventas y deta_ventas)
    def fcerrar_venta(self):

        modo = self.principal.sv_modo.get()

        match modo:
            case "NADA":
                return

            case "ALTA":
                self.cerrar_venta_alta_resumen()
                self.cerrar_venta_alta_detalle()

            case "EDICION":
                self.cerrar_venta_edicion_detalle()
                self.cerrar_venta_edicion_resumen()

            case _:
                return

        self.principal.status.set_status("✔ Venta guardada correctamente", "ok")

        # Código común
        self.principal.freiniciar_todo()
        self.principal.notebook.select(self.principal.pestana_1)
        self.principal.pestana_1.btn_nueva_venta.focus_set()

    # Insertar RESU_VENTAS - RESUMEN DE VENTAS (resu_ventas) encabezados de las ventas
    def cerrar_venta_alta_resumen(self):

        # Hago consulta a aux_ventas y sumarizo el total de la venta -----------------
        self.total_ventas = 0
        datos = self.principal.varCotiz.consultar_tablas("aux", "")
        for row in datos:
            self.total_ventas += row[4] * row[6]  # precio de lista unitario por cantidad
        # ----------------------------------------------------------------------------

        # Creamos el diccionario para insertar los datos en resu_ventas (encabezado de las ventas)
        dic_resuventas = {
            #"Id": self.clave,
            "rv_numero": self.principal.sv_venta_numero.get(),
            "rv_fecha": self.principal.sv_venta_fecha.get(),
            "rv_cod_cliente": self.principal.pestana_1.sv_codigo_cliente.get(),
            "rv_cliente": self.principal.pestana_1.sv_nombre_cliente.get(),
            "rv_sitfis": self.principal.pestana_1.sv_sit_fiscal.get(),
            "rv_cuit": self.principal.pestana_1.sv_cuit.get(),
            "rv_tipo_pago": self.principal.pestana_1.sv_combo_formas_pago.get(),
            "rv_detalle_pago": self.principal.pestana_1.sv_detalle_pago.get(),
            "rv_dolarhoy": self.sv_valor_dolar_hoy.get(),
            "rv_total": self.total_ventas
        }

        try:
            id_ref = self.principal.varCotiz.insertar_resuventa(dic_resuventas)
        except Exception:
            self.principal.varFuncion_new.mostrar_error()
            return
        else:
            self.principal.pestana_1.llena_grilla_ventas(id_ref)  # paso solo el foco, sin datos de busqueda

    # Guarda modificaciones en los datos encabezado (resu_ventas)
    def cerrar_venta_edicion_resumen(self):

        #-----------------------------------------------------------------
        # GUARDO ID Y CLAVE PARA GRID Y POOSICIONAR PUNTERO
        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
        self.selected = self.principal.pestana_1.grid_tvw_todaslasventas.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo
        # verlo en la base 1, 2, 3, 4......)
        self.clave = self.principal.pestana_1.grid_tvw_todaslasventas.item(self.selected, 'text')
        #-----------------------------------------------------------------

        # Hago consulta a aux_ventas y sumarizo el total de la venta -----
        self.total_ventas = 0
        datos = self.principal.varCotiz.consultar_tablas("aux", "")
        for row in datos:
            self.total_ventas += row[4] * row[6]  # precio de lista unitario por cantidad
        # ----------------------------------------------------------------

        # Creamos el diccionario para insertar los datos en resu_ventas (encabezado de las ventas)
        dic_resuventas = {
            "Id": self.clave,
            "rv_numero": self.principal.sv_venta_numero.get(),
            "rv_fecha": self.principal.sv_venta_fecha.get(),
            "rv_cod_cliente": self.principal.pestana_1.sv_codigo_cliente.get(),
            "rv_cliente": self.principal.pestana_1.sv_nombre_cliente.get(),
            "rv_sitfis": self.principal.pestana_1.sv_sit_fiscal.get(),
            "rv_cuit": self.principal.pestana_1.sv_cuit.get(),
            "rv_tipo_pago": self.principal.pestana_1.sv_combo_formas_pago.get(),
            "rv_detalle_pago": self.principal.pestana_1.sv_detalle_pago.get(),
            "rv_dolarhoy": self.sv_valor_dolar_hoy.get(),
            "rv_total": self.total_ventas
        }

        try:
            self.principal.varCotiz.modificar_resuventa(dic_resuventas)
            id_ref = self.clave
        except Exception:
            self.principal.varFuncion_new.mostrar_error()
            return
        else:
            self.principal.pestana_1.llena_grilla_ventas(id_ref)  # paso solo el foco, sin datos de busqueda

    # Insertar en tabla detalle de las ventas (deta_ventas) articulos de la venta
    def cerrar_venta_alta_detalle(self):

        datos = self.principal.varCotiz.consultar_tablas("aux", "")
        for row in datos:

            dic_detaventas = {
#                "Id": self.clave,
                "dv_numero": self.principal.sv_venta_numero.get(),
                "dv_codigo_art": row[1],
                "dv_desc_art": row[2],
                "dv_marca_art": row[3],
                "dv_cantidad": row[4],
                "dv_tot_uni_conta": row[5],
                "dv_tot_uni_lista": row[6],
                "dv_neto_venta": row[7],
                "dv_impor_iva21": row[8],
                "dv_impor_iva105": row[9],
                "dv_impor_ganancia": row[10],
                "dv_costo_dolar": row[11],
                "dv_costo_bruto": row[12],
                "dv_tasaiva": row[13]
            }

            try:
                self.principal.varCotiz.insertar_detaventa(dic_detaventas)
            except Exception:
                self.principal.varFuncion_new.mostrar_error()
                return

    # Guardo modificaciones en el detalle de venta (se agrego, quito, modifico algyun articulo)
    def cerrar_venta_edicion_detalle(self):

        # Aqui si borro venta anterior para ingresar la misma pero modificada -----------
        self.principal.varCotiz.eliminar_detaventa(self.principal.sv_venta_numero.get())
        # -------------------------------------------------------------------------------

        datos = self.principal.varCotiz.consultar_tablas("aux", "")
        for row in datos:

            dic_detaventas = {
                # "Id": self.clave,
                "dv_numero": self.principal.sv_venta_numero.get(),
                "dv_codigo_art": row[1],
                "dv_desc_art": row[2],
                "dv_marca_art": row[3],
                "dv_cantidad": row[4],
                "dv_tot_uni_conta": row[5],
                "dv_tot_uni_lista": row[6],
                "dv_neto_venta": row[7],
                "dv_impor_iva21": row[8],
                "dv_impor_iva105": row[9],
                "dv_impor_ganancia": row[10],
                "dv_costo_dolar": row[12],
                "dv_costo_bruto": row[11],
                "dv_tasaiva": row[13]
            }

            try:
                self.principal.varCotiz.insertar_detaventa(dic_detaventas)
            except Exception:
                self.principal.varFuncion_new.mostrar_error()
                return


    # --------------------------------------------------------------------
    # CRUD sobre aux_ventas cuando ingreso, edito o borro articulos que se venden
    # --------------------------------------------------------------------

    # Inserta un articulo en aux_ventas
    def ingresar_nuevo_item_venta(self):

        #-----------------------------------------------------------------
        # Validar los items ingresados
        # 1- que articulo no este vacio
        if len(self.sv_it_descripcion_articulo.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de articulo", parent=self)
            return
        # 2- que exista una cantidad
        if not self.sv_cantidad_venta.get():
            messagebox.showerror("Error", "Falta cantidad de articulo", parent=self)
            self.entry_cantidad_venta.focus()
            return
        #-----------------------------------------------------------------

        #-----------------------------------------------------------------
        # GUARDO ID Y CLAVE PARA GRID Y POOSICIONAR PUNTERO
        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
        self.selected = self.grid_tvw_auxiliar_venta.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo
        # verlo en la base 1, 2, 3, 4......)
        self.clave = self.grid_tvw_auxiliar_venta.item(self.selected, 'text')
        #-----------------------------------------------------------------

        #-----------------------------------------------------------------
        # Genero diccionario
        dic_auxventas = {
            "Id": self.clave,
            "av_codigo_art": self.sv_it_codigo_articulo.get(),
            "av_desc_art": self.sv_it_descripcion_articulo.get(),
            "av_marca_art": self.sv_it_marca_articulo.get(),
            "av_cantidad": self.sv_cantidad_venta.get(),
            "av_tot_uni_conta": self.sv_unidad_precio_venta_contado.get(),
            "av_tot_uni_lista": self.sv_unidad_precio_venta_lista.get(),
            "av_neto_unidad": self.sv_unidad_neto_pesos.get(),
            "av_impor_iva21": self.sv_unidad_total_iva_21.get(),
            "av_impor_iva105": self.sv_unidad_total_iva_105.get(),
            "av_impor_ganancia": self.sv_unidad_total_ganancia.get(),
            "av_costo_dolar": self.sv_unidad_costo_dolar.get(),   # este es en neto
            "av_costo_bruto": self.sv_unidad_costo_bruto_pesos.get(),
            #"av_costo_dolar": self.sv_unidad_costo_dolar_bruto.get(),
            "av_tasaiva": self.sv_combo_tasa_iva.get()
        }
        #-----------------------------------------------------------------

        # Ingresar datos a la tabla y evaluacion del procedimiento
        try:
            id_ref = ""
            if self.alta_modif_p2 == 1:
                self.id_nuevo = self.principal.varCotiz.insertar_auxventa(dic_auxventas)
                id_ref = self.id_nuevo
            elif self.alta_modif_p2 == 2:
                self.id_nuevo = self.principal.varCotiz.modificar_auxventa(dic_auxventas)
                id_ref = self.id_nuevo
        except Exception:
            self.principal.varFuncion_new.mostrar_error()
            return
        else:
            self.principal.status.set_status("✔ Nuevo articulo ingresado correctamente", "ok")

        # Refresco grid auxiliar
        # self.llena_grilla_auxiliar(set_foco=self.clave)
        self.llena_grilla_auxiliar(set_foco=id_ref)
        # dejar en blanco todos los entrys del articulo
        self.limpiar_entrys_2()
        # Desactivar los entrys
        self.habilitar_text_2("disabled")
        self.entry_detalle_movim.focus()
        self.principal.status.set_status("✔ Modificacion de articulo correcta", "ok")

    # Bt. "Editar articulo" pestaña 2 - Edita los articulos de la tabla auxiliar de ventas (aux_ventas)
    def feditar_item_venta_auxiliar(self):

        # claves del Grid
        self.selected = self.grid_tvw_auxiliar_venta.focus()
        self.clave = self.grid_tvw_auxiliar_venta.item(self.selected, 'text')

        if self.clave == "":
            self.principal.status.set_status("✔ No hay nada seleccionado", "ok")
            return

        self.alta_modif_p2 = 2
        self.habilitar_text_2("normal")
        self.limpiar_entrys_2()

        valores = self.grid_tvw_auxiliar_venta.item(self.selected, 'values')

        self.sv_it_codigo_articulo.set(value=valores[0]),
        self.sv_it_descripcion_articulo.set(value=valores[1])
        self.sv_it_marca_articulo.set(value=valores[2]),
        self.sv_cantidad_venta.set(value=valores[3]),
        self.sv_unidad_precio_venta_contado.set(value=valores[4]),
        self.sv_unidad_precio_venta_lista.set(value=valores[5]),
        self.sv_unidad_neto_pesos.set(value=valores[6]),
        self.sv_unidad_total_iva_21.set(value=valores[7])

        # self.sv_unidad_total_iva_105.get(),
        # self.sv_unidad_total_ganancia.get(),
        # self.sv_unidad_costo_bruto_pesos.get(),
        # self.sv_unidad_costo_dolar_bruto.get(),
        # self.sv_combo_tasa_iva.get()

        self.principal.pestana_2.calcular("totalventa")

    # Bt. "Quitar articulo" pestaña 2 - Quita un articulo de la tabla auxiliar de ventas (aux_ventas)
    def fquitar_item_venta_auxiliar(self):

        # ------------------------------------------------------------------------------
        # selecciono el Id del GRID para su uso posterior
        self.selected = self.grid_tvw_auxiliar_venta.focus()
        self.selected_ant = self.grid_tvw_auxiliar_venta.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no son el mismo que el grid)
        self.clave = self.grid_tvw_auxiliar_venta.item(self.selected, 'text')
        self.clave_ant = self.grid_tvw_auxiliar_venta.item(self.selected_ant, 'text')
        # ------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_tvw_auxiliar_venta.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar articulo?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Cancelada por usuario", parent=self)
            return

        try:
            self.principal.varCotiz.eliminar_auxventa(self.clave)
        except Exception:
            self.principal.varFuncion_new.mostrar_error()
            return
        else:
            messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.llena_grilla_auxiliar(self.clave_ant)

        self.calcular("totalventa")

    # Bt Agregar articulo - Prepara all para que pueda cargar un nuevo articulo a la venta actual
    def agrego_articulo(self):

        self.alta_modif_p2 = 1
        self.habilitar_text_2("normal")
        self.entry_detalle_movim.focus_set()

    def doble_click_grid2(self, _event):
        self.feditar_item_venta_auxiliar()


    # ----------------------------------------------------------------------------
    # CUADROS DE PANTALLA
    # ----------------------------------------------------------------------------

    # Contenedor GRID auxiliar (aux_ventas) para ingresar los articulos vendidos
    # GRID AUXVENTAS
    def cuadro_grid_articulos(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_ventas_articulos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_auxiliar_venta = ttk.Treeview(self.frame_grid_ventas_articulos, height=7, columns=("col1", "col2",
                                                                     "col3", "col4", "col5", "col6", "col7", "col8", "col9"))

        self.grid_tvw_auxiliar_venta.bind("<Double-Button-1>", self.doble_click_grid2)
        #("<Double-Button-1>", self.doble_click_grid)
        self.grid_tvw_auxiliar_venta.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_tvw_auxiliar_venta.column("col1", width=80, anchor="w", minwidth=80)
        self.grid_tvw_auxiliar_venta.column("col2", width=430, anchor="w", minwidth=430)
        self.grid_tvw_auxiliar_venta.column("col3", width=110, anchor="center", minwidth=110)
        self.grid_tvw_auxiliar_venta.column("col4", width=60, anchor="center", minwidth=60)
        self.grid_tvw_auxiliar_venta.column("col5", width=130, anchor="center", minwidth=130)
        self.grid_tvw_auxiliar_venta.column("col6", width=70, anchor="center", minwidth=70)
        self.grid_tvw_auxiliar_venta.column("col7", width=70, anchor="center", minwidth=70)
        self.grid_tvw_auxiliar_venta.column("col8", width=70, anchor="center", minwidth=70)
        self.grid_tvw_auxiliar_venta.column("col9", width=70, anchor="center", minwidth=70)

        self.grid_tvw_auxiliar_venta.heading("#0", text="Id", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col1", text="Codigo", anchor="w")
        self.grid_tvw_auxiliar_venta.heading("col2", text="Descripcion", anchor="w")
        self.grid_tvw_auxiliar_venta.heading("col3", text="Marca", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col4", text="Cant", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col5", text="Precio contado unidad", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col6", text="Precio lista unidad", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col7", text="Costo dolar", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col8", text="Costo bruto", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col9", text="Tasa IVA", anchor="center")

        self.grid_tvw_auxiliar_venta.tag_configure('oddrow', background='light grey')
        self.grid_tvw_auxiliar_venta.tag_configure('evenrow', background='light blue')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_grid_ventas_articulos, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_grid_ventas_articulos, orient="vertical")
        self.grid_tvw_auxiliar_venta.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_auxiliar_venta.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_auxiliar_venta.xview)
        scroll_y.config(command=self.grid_tvw_auxiliar_venta.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_tvw_auxiliar_venta['selectmode'] = 'browse'
        self.grid_tvw_auxiliar_venta.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    # Contenedor de los botones CRUD para auxiliar de< venta con articulos vendidos
    def cuadro_botones_articulos(self):

        for c in range(5):
            self.frame_botones_articulos.grid_columnconfigure(c, weight=1, minsize=120)

        # Agregar articulo a la venta
        icono = self.principal.cargar_icono("agregar-producto.png")
        self.btn_guardar_venta = tk.Button(self.frame_botones_articulos, text=" Agregar articulo", width=19,
                                           command=self.agrego_articulo, bg='blue', fg='white', compound="left")
        self.btn_guardar_venta.image = icono
        self.btn_guardar_venta.config(image=icono)
        self.btn_guardar_venta.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)

        # Editar articulo en la venta
        icono = self.principal.cargar_icono("editar.png")
        self.btn_editar_itemventa = tk.Button(self.frame_botones_articulos, text=" Editar articulo", width=19,
                                              command=self.feditar_item_venta_auxiliar, bg='blue', fg='white', compound="left")
        self.btn_editar_itemventa.image = icono
        self.btn_editar_itemventa.config(image=icono)
        self.btn_editar_itemventa.grid(row=0, column=1, padx=3, pady=2, sticky=tk.W)

        # Eliminar articulo de la venta
        icono = self.principal.cargar_icono("eliminar.png")
        self.btn_eliminar_itemventa = tk.Button(self.frame_botones_articulos, text=" Quitar articulo", width=19,
                                                command=self.fquitar_item_venta_auxiliar, bg='blue', fg='white',
                                                compound="left")
        self.btn_eliminar_itemventa.image = icono
        self.btn_eliminar_itemventa.config(image=icono)
        self.btn_eliminar_itemventa.grid(row=0, column=2, padx=3, pady=2, sticky=tk.W)

        # Reset cargar articulo operaacion actual
        icono = self.principal.cargar_icono("reset.png")
        self.btn_reset_art = tk.Button(self.frame_botones_articulos, text=" Reset Articulo activo",
                                       command=self.freset_articulo_activo, width=19, bg='black', fg='white', compound="left")
        self.btn_reset_art.image = icono
        self.btn_reset_art.config(image=icono)
        self.btn_reset_art.grid(row=0, column=3, padx=3, pady=2, sticky=tk.W)

        # Cancelar operaciones en articulos
        icono = self.principal.cargar_icono("cancelar.png")
        self.btn_cancela_art = tk.Button(self.frame_botones_articulos, text=" Cancelar carga articulos", command=self.cancelar_articulo,
                                       width=19, bg='black', fg='white', compound="left")
        self.btn_cancela_art.image = icono
        self.btn_cancela_art.config(image=icono)
        self.btn_cancela_art.grid(row=0, column=4, padx=3, pady=2, sticky=tk.W)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_botones_articulos, text="", image=self.photo4, command=self.ftoparch,
                                    bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=5, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_botones_articulos, text="", image=self.photo5, command=self.ffinarch,
                                    bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=6, padx=3, sticky="nsew", pady=3)

        for widg in self.frame_botones_articulos.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_entrys_articulos(self):

        for c in range(8):
            self.frame_entrys_articulos.grid_columnconfigure(c, weight=1, minsize=80)

        # COTIZACION DEL DOLAR DEL DIA
        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        self.lbl_dolarhoy1 = tk.Label(self.frame_entrys_articulos, text="Dolar hoy:", justify="left", font=fff,
                                      foreground="red")
        self.lbl_dolarhoy1.grid(row=0, column=0, padx=4, pady=2, sticky=tk.W)
        self.lbl_dolarhoy2 = tk.Label(self.frame_entrys_articulos, textvariable=self.sv_valor_dolar_hoy, width=10,
                                      justify="right", font=fff, foreground="red")
        self.lbl_dolarhoy2.grid(row=0, column=1, padx=4, pady=2, sticky='nsew')

        # Numero de venta
        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        self.lbl_ventanro = tk.Label(self.frame_entrys_articulos, text="Venta Nro.:", justify="left", font=fff, foreground="black")
        self.lbl_ventanro.grid(row=0, column=2, padx=4, pady=2, sticky=tk.W)
        self.lbl_ventanro_valor = tk.Label(self.frame_entrys_articulos, textvariable=self.principal.sv_venta_numero, width=10,
                                      justify="right", font=fff, foreground="black")
        self.lbl_ventanro_valor.grid(row=0, column=3, padx=4, pady=2, sticky='nsew')

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((18, 18), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = tk.Button(self.frame_entrys_articulos, text="", image=self.photo_bus_art,
                                     command=self.fbusart, bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=4, padx=4, pady=2, sticky="nsew")

        # ENTRY ARTICULO
        self.lbl_detalle_movim = tk.Label(self.frame_entrys_articulos, text="Articulo: ", justify="left")
        self.lbl_detalle_movim.grid(row=0, column=5, padx=4, pady=2, sticky=tk.W)
        self.entry_detalle_movim = tk.Entry(self.frame_entrys_articulos, textvariable=self.sv_it_descripcion_articulo,
                                            width=90, justify="left")
        self.entry_detalle_movim.grid(row=0, column=6, padx=4, pady=2, sticky=tk.E)

        # COMBO TASA IVA
        self.lbl_combo_tasa_iva = tk.Label(self.frame_entrys_articulos, justify="left", foreground="black", text="IVA %")
        self.lbl_combo_tasa_iva.grid(row=0, column=7, padx=4, pady=2, sticky=tk.W)
        self.combo_tasa_iva = ttk.Combobox(self.frame_entrys_articulos, textvariable=self.sv_combo_tasa_iva, state='readonly', width=8)
        self.combo_tasa_iva['value'] = ["21.00", "10.50"]
        self.combo_tasa_iva.current(0)
        self.combo_tasa_iva.grid(row=0, column=8, padx=4, pady=2, sticky=tk.W)
        #     self.combo_tasa_iva.bind('<Tab>', lambda e: self.calcular("totales_por_item"))

        for widg in self.frame_entrys_articulos.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')

    def cuadro_entrys_importes_articulos(self):

        for c in range(13):
            self.frame_entrys_importes_articulos.grid_columnconfigure(c, weight=1, minsize=50)

        # Precios y cantidades del articulo

        fff = tkfont.Font(family="Arial", size=10, weight="bold")

        # PRECIO VENTA FINAL UNIDAD LISTA + % recargo tarjeta
        self.lbl_precio_lista_unidad1 = tk.Label(self.frame_entrys_importes_articulos, text=f"Precio LISTA (c/"
                                                 f"{self.sv_tasa_recargo_precio.get()}% rec.)$:", font=fff, justify="left", fg="green")
        self.lbl_precio_lista_unidad1.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)

        self.entry_precio_lista_unidad = tk.Entry(self.frame_entrys_importes_articulos, font=fff, width=10,
                                                  textvariable=self.sv_unidad_precio_venta_lista, justify="right")
        self.entry_precio_lista_unidad.grid(row=0, column=1, padx=2, pady=2, sticky='nsew')
        self.entry_precio_lista_unidad.config(validate="key", validatecommand=self.vcmd)
        self.entry_precio_lista_unidad.bind('<Tab>', lambda e: self.calcular("precio_lista_unidad"))

        # PRECIO VENTA FINAL UNIDAD CONTADO
        self.lbl_precio_contado_unidad1 = tk.Label(self.frame_entrys_importes_articulos, text="Contado $:", font=fff, justify="left")
        self.lbl_precio_contado_unidad1.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
        self.entry_precio_contado_unidad = tk.Label(self.frame_entrys_importes_articulos, font=fff, width=10,
                                                    textvariable=self.sv_unidad_precio_venta_contado, justify="right")
        self.entry_precio_contado_unidad.grid(row=0, column=3, padx=2, pady=2, sticky='nsew')
        # self.entry_precio_venta_unidad.config(validate="key", validatecommand=self.vcmd)
        # self.entry_precio_venta_unidad.bind('<Tab>', lambda e: self.calcular("precio_venta_unidad"))

        # CANTIDAD A COMPRAR DEL ARTICULO
        self.lbl_cantidad_venta = tk.Label(self.frame_entrys_importes_articulos, justify="left", text="Cant.: ",
                                           font=fff)
        self.lbl_cantidad_venta.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)
        self.entry_cantidad_venta = tk.Entry(self.frame_entrys_importes_articulos, textvariable=self.sv_cantidad_venta,
                                             width=4, justify="right", font=fff)
        self.entry_cantidad_venta.grid(row=0, column=5, padx=2, pady=2, sticky=tk.W)
        self.entry_cantidad_venta.config(validate="key", validatecommand=self.vcmd)
        self.entry_cantidad_venta.bind('<Tab>', lambda e: self.calcular("cantidad"))

        # CARTEL PRECIO TOTAL
        self.lbl_cartel_total_artiulo = tk.Label(self.frame_entrys_importes_articulos, text="TOTAL $:", justify="left",
                                                 font=fff, fg="green")
        self.lbl_cartel_total_artiulo.grid(row=0, column=6, padx=2, pady=2, sticky=tk.W)
        self.lbl_cartel_total_artiulo_xcanti = tk.Label(self.frame_entrys_importes_articulos, font=fff,
                                                        textvariable=self.sv_xcanti_total_precio_venta_lista,
                                                        width=10, fg="green", justify="right")
        self.lbl_cartel_total_artiulo_xcanti.grid(row=0, column=7, padx=2, pady=2, sticky='nsew')

        # COSTO UNIDAD BRUTO PESOS
        self.lbl_cartel_total_artiulo = tk.Label(self.frame_entrys_importes_articulos, text="Costo bruto $:",
                                                 justify="left", font=fff)
        self.lbl_cartel_total_artiulo.grid(row=0, column=8, padx=2, pady=2, sticky=tk.W)
        self.lbl_cartel_total_artiulo_xcanti = tk.Label(self.frame_entrys_importes_articulos, font=fff, width=10,
                                                        textvariable=self.sv_unidad_costo_bruto_pesos, justify="right")
        self.lbl_cartel_total_artiulo_xcanti.grid(row=0, column=9, padx=2, pady=2, sticky='nsew')

        # GANANCIA UNIDAD PESOS
        self.lbl_cartel_total_artiulo = tk.Label(self.frame_entrys_importes_articulos, text="Gan. $:",
                                                 justify="left", font=fff)
        self.lbl_cartel_total_artiulo.grid(row=0, column=10, padx=2, pady=2, sticky=tk.W)
        self.lbl_cartel_total_artiulo_xcanti = tk.Label(self.frame_entrys_importes_articulos, font=fff, width=10,
                                                        textvariable=self.sv_unidad_total_ganancia, justify="right")
        self.lbl_cartel_total_artiulo_xcanti.grid(row=0, column=11, padx=2, pady=2, sticky='nsew')

        # Ingresar articulo a gris de ventas
        # img = Image.open("guardar.png").resize((18, 18))
        # icono = ImageTk.PhotoImage(img)
        self.btn_ingresar_itemventa = tk.Button(self.frame_entrys_importes_articulos, text="✓ OK ↑", width=10,
                                                command=self.ingresar_nuevo_item_venta, bg='green', fg='white')
        # self.btn_ingresar_itemventa.image = icono
        # self.btn_ingresar_itemventa.config(image=icono)
        self.btn_ingresar_itemventa.grid(row=0, column=12, padx=3, pady=2, sticky=tk.W)

        for widg in self.frame_entrys_importes_articulos.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')

        # # TASA GANANCIA
        # self.lbl_tasa_ganancia_unidad1 = tk.Label(self.frame_entrys_importes_articulo, text="% Ganancia unidad : ", justify="left")
        # self.lbl_tasa_ganancia_unidad1.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
        # self.entry_tasa_ganancia_unidad2 = Entry(self.frame_entrys_importes_articulo,
        #                                          textvariable=self.sv_unidad_tasa_ganancia, width=5, justify="right")
        # self.entry_tasa_ganancia_unidad2.grid(row=0, column=3, padx=3, pady=2, sticky='w')
        # self.entry_tasa_ganancia_unidad2.config(validate="key", validatecommand=self.vcmd)
        # self.entry_tasa_ganancia_unidad2.bind('<Tab>', lambda e: self.calcular("tasa_ganancia_unidad"))
        #
        # # GANANCIA
        # self.lbl_ganancia_pesos_unidad1 = tk.Label(self.frame_entrys_importes_articulo, text="Ganancia unidad $: ", justify="left")
        # self.lbl_ganancia_pesos_unidad1.grid(row=1, column=2, padx=2, pady=2, sticky=tk.W)
        # self.entry_ganancia_pesos_unidad2 = Entry(self.frame_entrys_importes_articulo,
        #                                           textvariable=self.sv_unidad_total_ganancia, width=10,
        #                                           justify="right")
        # self.entry_ganancia_pesos_unidad2.grid(row=1, column=3, padx=3, pady=2, sticky='nsew')
        # self.entry_ganancia_pesos_unidad2.config(validate="key", validatecommand=self.vcmd)
        # self.entry_ganancia_pesos_unidad2.bind('<Tab>', lambda e: self.calcular("importe_ganancia_unidad"))
        #
        # # COSTO PESOS BRUTO UNIDAD
        # self.lbl_costo_pesos_bruto_unidad1 = tk.Label(self.frame_entrys_importes_articulo, text="Costo Bruto $: ", justify="left")
        # self.lbl_costo_pesos_bruto_unidad1.grid(row=2, column=0, padx=2, pady=2, sticky=tk.W)
        # self.lbl_costo_pesos_bruto_unidad2 = tk.Label(self.frame_entrys_importes_articulo,
        #                                            textvariable=self.sv_unidad_costo_bruto_pesos, state='normal',
        #                                            width=15, justify="right")
        # self.lbl_costo_pesos_bruto_unidad2.grid(row=2, column=1, padx=3, pady=2, sticky='nsew')
        # #self.entry_costo_pesos_bruto_unidad2.config(validate="key", validatecommand=self.vcmd)
        # #self.entry_costo_pesos_bruto_unidad2.bind('<Tab>', lambda e: self.calcular("costo_pesos_bruto"))
        #
        # # COSTO DOLAR UNIDAD
        # self.lbl_total_costodolar_unidad1 = tk.Label(self.frame_entrys_importes_articulo, text="Costo Dolar Bruto U$: ",
        #                                           justify="left")
        # self.lbl_total_costodolar_unidad1.grid(row=2, column=2, padx=2, pady=2, sticky=tk.W)
        # self.lbl_total_costodolar_unidad2 = tk.Label(self.frame_entrys_importes_articulo,
        #                                           textvariable=self.sv_unidad_costo_dolar_bruto, width=15,
        #                                           justify="right")
        # self.lbl_total_costodolar_unidad2.grid(row=2, column=3, padx=3, pady=2, sticky='nsew')
        #
        # # NETO VENTA UNIDAD
        # self.lbl_total_netoventa_unidad1 = tk.Label(self.frame_entrys_importes_articulo, text="Neto Venta unidad $: ",
        #                                          justify="left")
        # self.lbl_total_netoventa_unidad1.grid(row=0, column=5, padx=2, pady=2, sticky=tk.W)
        # self.lbl_total_netoventa_unidad2 = tk.Label(self.frame_entrys_importes_articulo,
        #                                          textvariable=self.sv_unidad_neto_pesos, width=15, justify="right")
        # self.lbl_total_netoventa_unidad2.grid(row=0, column=6, padx=3, pady=2, sticky='nsew')
        #
        # # TOTAL IVA
        # self.lbl_totaliva_unidad1 = tk.Label(self.frame_entrys_importes_articulo, text="IVA unidad $: ", justify="left")
        # self.lbl_totaliva_unidad1.grid(row=1, column=5, padx=2, pady=2, sticky=tk.W)
        # self.lbl_totaliva_unidad2 = tk.Label(self.frame_entrys_importes_articulo, textvariable=self.sv_unidad_total_iva,
        #                                   width=15, justify="right")
        # self.lbl_totaliva_unidad2.grid(row=1, column=6, padx=3, pady=2, sticky='nsew')

    def cuadro_totales_venta(self):

        for c in range(5):
            self.frame_totales_venta.grid_columnconfigure(c, weight=1, minsize=90)

        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        self.lbl_acumulado_neto_venta1 = tk.Label(self.frame_totales_venta, text="Total Venta $: ", font=fff, fg="blue",
                                                  justify="left")
        self.lbl_acumulado_neto_venta1.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.lbl_acumulado_neto_venta2 = tk.Label(self.frame_totales_venta, textvariable=self.sv_global_final_venta,
                                                  state='normal', font=fff, fg="blue", width=12, justify="right")
        self.lbl_acumulado_neto_venta2.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # forma de pago y detalle
        self.lbl_combo_formapago = tk.Label(self.frame_totales_venta, text="Forma de Pago: ", justify="left")
        self.lbl_combo_formapago.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
        self.combo_formapago = ttk.Combobox(self.frame_totales_venta, textvariable=self.principal.pestana_1.sv_combo_formas_pago,
                                            state='readonly', width=15)
        self.combo_formapago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                         "Tarjeta Credito", "Cheque"]
        self.combo_formapago.current(0)
        self.combo_formapago.grid(row=0, column=3, padx=4, pady=2, sticky=tk.W)

        self.lbl_deta_formapago = tk.Label(self.frame_totales_venta, text="Detalle: ", justify="left")
        self.lbl_deta_formapago.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)
        self.entry_deta_formapago = tk.Entry(self.frame_totales_venta, textvariable=self.principal.pestana_1.sv_detalle_pago, width=75)
        self.entry_deta_formapago.grid(row=0, column=5, padx=4, pady=2, sticky=tk.W)

        for widg in self.frame_totales_venta.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_botones_aux_ventas(self):

        for c in range(1):
            self.frame_botones_aux_ventas.grid_columnconfigure(c, weight=1, minsize=120)

        icono = self.principal.cargar_icono("guardar.png")
        self.btn_cerrar_venta = tk.Button(self.frame_botones_aux_ventas, text=" Guardar venta", width=19,
                                          command=self.fcerrar_venta, bg='green', fg='white', compound="left")
        self.btn_cerrar_venta.image = icono
        self.btn_cerrar_venta.config(image=icono)
        self.btn_cerrar_venta.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.frame_botones_aux_ventas, text="Salir", image=self.photo3, width=85,
                                  command=self.principal.fsalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")

        for widg in self.frame_botones_aux_ventas.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')



    # -------------------------------------------------------------------------
    # VALIDACION ENTRADA DE DATOS NUEMERICOS Y FECHAS
    # -------------------------------------------------------------------------

    def control_valores(self):

        # Hago Control (control_forma) de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
        # Tambien todos los demas controles numericos que hacen falta

        self.sv_unidad_precio_venta_contado.set(
            value=self.principal.varFuncion_new.corregir_valor(self.sv_unidad_precio_venta_contado.get()))
        self.sv_unidad_precio_venta_lista.set(
            value=self.principal.varFuncion_new.corregir_valor(self.sv_unidad_precio_venta_lista.get()))
        self.sv_unidad_costo_bruto_pesos.set(
            value=self.principal.varFuncion_new.corregir_valor(self.sv_unidad_costo_bruto_pesos.get()))
        self.sv_cantidad_venta.set(value=self.principal.varFuncion_new.corregir_valor(self.sv_cantidad_venta.get()))
        self.sv_unidad_tasa_ganancia.set(value=self.principal.varFuncion_new.corregir_valor(self.sv_unidad_tasa_ganancia.get()))


    # -------------------------------------------------------------------------
    # PRECIOS Y TOTALES - Calculos y obtencion de precios - Busqueda de articulos
    # -------------------------------------------------------------------------

    # Busqueda del articulo - obtencion de precios y tasas - calculos de totales
    def fbusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.sv_it_descripcion_articulo.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.sv_it_descripcion_articulo.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.sv_it_descripcion_articulo.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.sv_it_descripcion_articulo.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.principal.varFuncion_new.ventana_selec("articulos", "descripcion", "marca",
                                                        "costodolar", "Descripcion", "Marca",
                                                        "Precio dolar neto", que_busco,
                                                        "Orden: Rubro+Marca+Descripcion", "S")

        #masiva = 0
        #masganancia = 0

        for item in valores_new:
            # -------------------------------------------------------------
            # PROPIEDADES ARTICULO - descripcion del articulo - %IVA
            self.sv_it_codigo_articulo.set(value=item[1])       #CODIGO ARTICULO
            self.sv_it_descripcion_articulo.set(value=item[2])  #DESCRIPCION ATICULO
            self.sv_it_marca_articulo.set(value=item[3])        #MARCA ARTICULOS
            self.sv_unidad_costo_dolar.set(value=item[6])       #COSTO POR UNIDAD EN DOLARES
            self.sv_combo_tasa_iva.set(value=item[7])           #TASA IVA ARTICULO
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # CACULOS - calculo neto_pesos : neto mas el iva : neta ma iva mas ganancia = precio de venta por unidad
            # costo neto
            costopesos_neto = round((float(self.sv_valor_dolar_hoy.get()) * float(item[6])), 2)
            # costo bruto
            costo_neto_masiva = round((float(costopesos_neto) * (1 + (float(item[7]) / 100))), 2)
            # precio de venta contado
            costo_masiva_masganancia = round((float(costo_neto_masiva) * (1 + (float(item[9]) / 100))), 2)
            # precio de venta lista (mas el % de recargo con tarjeta activo
            precio_venta_lista = costo_masiva_masganancia * (1 + (float(self.sv_tasa_recargo_precio.get()) / 100))
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # Precio de venta x unidad de lista (tiene el recargo del 10%)
            self.sv_unidad_precio_venta_lista.set(value=str(round(precio_venta_lista)))
            # Precio de venta x unidad contado (sin el 10% de recargo)
            self.sv_unidad_precio_venta_contado.set(value=str(round(costo_masiva_masganancia)))
            # Precio de venta de lista ya multiplicado por la cantidad (TOTAL FINAL DEL ARTICULO)
            self.sv_xcanti_total_precio_venta_lista.set(value=self.principal.varFuncion_new.formatear_cifra(
                                            round(precio_venta_lista * float(self.sv_cantidad_venta.get()))))
            # Costo x unidad del articulo en pesos y bruto(con iva)
            self.sv_unidad_costo_bruto_pesos.set(value=str(round(costo_neto_masiva)))
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # % de ganancia x unidad para el articulo (% ganancia)
            self.sv_unidad_tasa_ganancia.set(value=item[9])
            # Importe que gano x unidad de articulo tomado desde el precio de lista
            self.sv_unidad_total_ganancia.set(value=str(round(precio_venta_lista - costo_neto_masiva)))
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # Precio de costo x unidad neto en pesos
            self.sv_unidad_neto_pesos.set(value=str(costopesos_neto))
            # -------------------------------------------------------------

            self.entry_precio_lista_unidad.focus_set()
            self.entry_precio_lista_unidad.selection_range(0, tk.END)  # selecciona el texto

    def calcular(self, que_campo):

        # Esta funcion solo controla todos los Entrys numericos que no contengan el valor "" o mas de un "-" o un "."
        self.control_valores()

        #ii = 1
        try:
        #if ii == 1:
            if que_campo == "cantidad":  # Cuando se modifica la cantidad de un articulo

                # 1 - Precio de venta por unidad de lista(+10%) x cantidad comprada
                self.sv_xcanti_total_precio_venta_lista.set(value=str(round(float(self.sv_unidad_precio_venta_lista.get()) *
                                                                      float(self.sv_cantidad_venta.get()), 2)))
                # 2 - Ganancia por cantidad
                # self.sv_xcanti_total_ganancia.set(value=str(round(float(self.sv_unidad_total_ganancia.get()) *
                #                                                   float(self.sv_cantidad_venta.get()), 2)))

            if que_campo == "precio_lista_unidad":  # Se modifico el precio de venta de lista(+10%) para el articulo

                # 1 - Calculo nueva ganancia unidad
                self.sv_unidad_total_ganancia.set(value=str(round(float(self.sv_unidad_precio_venta_lista.get()) -
                                                            float(self.sv_unidad_costo_bruto_pesos.get()), 2)))

                # calculo nuevo neto unidad
                calcu_nuevo_neto = (float(self.sv_unidad_precio_venta_lista.get()) /
                                    float((1 + (float(self.sv_combo_tasa_iva.get()) / 100))))
                self.sv_unidad_neto_pesos.set(value=str(round(calcu_nuevo_neto, 2)))

                # Importe del IVA unidad Global (para el 21 o el 10,5) segun cual venga es lo mismo
                self.sv_unidad_total_iva.set(value=str(round(float(self.sv_unidad_neto_pesos.get()) *
                                                      (float(self.sv_combo_tasa_iva.get()) / 100), 2)))

                # Asigno el importe del IVA segun la TASA
                if self.sv_combo_tasa_iva.get() == "21.00":
                    self.sv_unidad_total_iva_21.set(value=str(round((float(self.sv_unidad_neto_pesos.get()) *
                                                              (float(self.sv_combo_tasa_iva.get()) / 100)), 2)))
                else:
                    self.sv_unidad_total_iva_105.set(value=str(round((float(self.sv_unidad_neto_pesos.get()) *
                                                                          (float(self.sv_combo_tasa_iva.get()) / 100)), 2)))

            # 3 - Multiplico nuevos importes por cantidad

            # - Precio final venta por cantidad comprada para un articulo
            self.sv_xcanti_total_precio_venta_lista.set(value=str(round(float(self.sv_unidad_precio_venta_lista.get()) *
                                                                            float(self.sv_cantidad_venta.get()), 2)))
            # - Ganancia por cantidad
            # self.sv_xcanti_total_ganancia.set(value=str(round(float(self.sv_unidad_total_ganancia.get()) *
            #                                                   float(self.sv_cantidad_venta.get()), 2)))

            if que_campo == "totalventa":  # Sumariza todos los articulos que estan en auxiliar de ventas

                datos = self.principal.varCotiz.consultar_tablas("aux")

                sumatot = 0
                # sumaiva21 = 0
                # sumaiva105 = 0
                # sumanetos = 0

                for row in datos:
                    sumatot += (row[6] * row[4])  # precio de lista * cantidad
                    # sumaiva21 = sumaiva21 + (row[7] * row[4])
                    # sumaiva105 = sumaiva105 + (row[8] * row[4])
                    # sumanetos = sumanetos + ((row[6]) * row[4])

                self.sv_global_final_venta.set(value=str(round(sumatot)))
                # self.sv_global_final_venta_iva21.set(value=round(sumaiva21, 2))
                # self.sv_global_final_venta_iva105.set(value=round(sumaiva105, 2))
                # self.sv_global_final_venta_neto.set(value=str(float(sumanetos)))

        except ValueError as e:

            messagebox.showerror("Error", str(e), parent=self)
            return




# # Punto de entrada para ejecutar la aplicación
# if __name__ == "__main__":
#     app = VentasPrincipal()
#     app.mainloop()
