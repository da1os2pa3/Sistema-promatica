import tkinter

from funciones import *
from funcion_new import *
from presupuestos_ABM import *
from articulos import *
#--------------------------------------
#from tkinter import *
#from tkinter import ttk
from tkinter import messagebox
#import tkinter as tk
import tkinter.font as tkFont
from tkinter.scrolledtext import *     # para campos text
#--------------------------------------
import os
from PDF_clase import *
from PIL import Image, ImageTk
from datetime import date, datetime
# -------------------------------------

class Clase_Presupuestos(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=520)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ---------------------------------------------------------------------------------
        # Instanciaciones
        self.varPresupuestos = datosPresupuestos(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # PANTALLA
        # ----------------------------------------------------------------------------------

        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """

        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()

        # Asigno fijo un ancho y un alto
        ancho_ventana = 1045
        alto_ventana = 775

        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------
        # BLOQUE INICIAL
        #-------------------------------------------------------------------------------
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla_resu_presup("")
        # ------------------------------------------------------------------------------

        # Obtengo el numero del presupuesto siguiente al ultimo cargado
        self.strvar_nro_presup.set(value=str(int(self.varPresupuestos.traer_ultimo(1)) + 1))

        # ------------------------------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno.
        Otras funciones para manejar los elementos seleccionados incluyen:
        1 - selection_add(): añade elementos a la selección.
        2 - selection_remove(): remueve elementos de la selección.
        3 - selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        4 - selection_toggle(): cambia la selección de un elemento. """

        """ Seteos iniciales: self.limpiar_entrys_total()-
        self.strvar_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))-self.estado_entrys_inicial("disabled")-
        self.estado_botones_dos("disabled")-self.estado_botones_uno("normal")-
        self.varPresupuestos.vaciar_auxpresup("aux_presup")-self.limpiar_Grid_auxiliar()-self.alta_modif_aux = 0
        self.alta_modif_presup = 0-self.grid_tvw_resupresup['selectmode'] = 'browse'-
        self.grid_tvw_resupresup.bind("<Double-Button-1>", self.DobleClickGrid) """

        # # guarda en item el Id del elemento fila en este caso fila 0 del grid principal
        # item = self.grid_tvw_resupresup.identify_row(0)
        # # Grid de auxpresup
        # self.grid_tvw_resupresup.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_tvw_resupresup.focus(item)

        # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # WIDGETS
    # ----------------------------------------------------------------------

    def create_widgets(self):

        # ----------------------------------------------------------------------
        #  TITULOS
        # ---------------------------------------------------------------------
        # Encabezado logo y titulo con PACK
        # self.frame_titulo_top = Frame(self.master)
        # # Armo el logo y el titulo
        # self.photo3 = Image.open('productos.png')
        # self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        # self.png_ventas = ImageTk.PhotoImage(self.photo3)
        # self.lbl_png_ventas = Label(self.frame_titulo_top, image=self.png_ventas, bg="red", relief=RIDGE, bd=5)
        # self.lbl_titulo = Label(self.frame_titulo_top, width=76, text="Ventas",
        #                         bg="black", fg="gold", font=("Arial bold", 15, "bold"), bd=5, relief=RIDGE, padx=5)
        # # Coloco logo y titulo en posicion de pantalla
        # self.lbl_png_ventas.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        # self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        # self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # STRINGVARS
        # ----------------------------------------------------------------------

        # DATOS DE LA VENTA Y DATOS CLIENTE
        self.strvar_nro_presup = tk.StringVar(value="0")
        self.strvar_fecha_presup = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_nombre_cliente = tk.StringVar(value="Consumidor Final")
        self.strvar_sit_fiscal = tk.StringVar(value="")
        self.strvar_cuit = tk.StringVar(value="")

        # VALOR DEL DOLAR HOY
        self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")
        self.traer_dolarhoy()

        # ARTICULO ITEM INGRESADO A AUX_VENTAS
        self.strvar_componente = tk.StringVar(value="")
        self.strvar_combo_tasa_iva = tk.StringVar()
        self.strvar_cantidad_vendida = tk.StringVar(value="1")
        self.strvar_tasa_ganancia = tk.StringVar(value="0.00")
        self.strvar_proveedor = tk.StringVar(value="")
        self.strvar_codigo_componente = tk.StringVar(value="")

        # VALORES
        self.strvar_neto_dolar = tk.StringVar(value="0.00")

        self.strvar_costo_neto_pesos_unidad = tk.StringVar(value="0.00")
        self.strvar_costo_neto_pesos_xcanti = tk.StringVar(value="0.00")

        self.strvar_costo_bruto_pesos_unidad = tk.StringVar(value="0.00")
        self.strvar_costo_bruto_pesos_xcanti = tk.StringVar(value="0.00")

        self.strvar_importe_iva_unidad = tk.StringVar(value="0.00")
        self.strvar_importe_iva_xcanti = tk.StringVar(value="0.00")

        self.strvar_importe_ganancia_unidad = tk.StringVar(value="0.00")
        self.strvar_importe_ganancia_xcanti = tk.StringVar(value="0.00")

        self.strvar_precio_final_unidad = tk.StringVar(value="0.00")
        self.strvar_precio_final_xcanti = tk.StringVar(value="0.00")

        # sumatoria de todos los componentes
        self.strvar_total_presupuesto = tk.StringVar(value="0.00")
        self.strvar_total_item_redondo = tk.StringVar(value="0.00")
        self.strvar_total_ganancia = tk.StringVar(value="0.00")
        self.strvar_total_costos = tk.StringVar(value="0.00")
        self.strvar_total_presup_redondo = tk.StringVar(value="0.00")

        # TIPOS DE PAGO
        self.strvar_combo_formas_pago = tk.StringVar()
        self.strvar_detalle_pago = tk.StringVar(value="")

        self.strvar_buscostring = tk.StringVar(value="")
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------------------------

        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # PREPARO TABLA AUXILIAR

        # Vacio la tabla auxiliar de componentes aux_presup donde van los items que se seleccionen
        self.varPresupuestos.vaciar_auxpresup("aux_presup")
        # ----------------------------------------------------------------------

        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        # COMIENZAN LOS FRAMES :::::::::::::::::::::::::::::::::::::::::::::::::
        # ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

        # ----------------------------------------------------------------------
        # grid principal de pantalla excepto barra lateral del menu
        self.frame_grid_botones=LabelFrame(self.master, text="", foreground="#CD5C5C")
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ABRO FRAME BARRA LATERAL BOTONES IZQUIERDA :::::::::::::::::::::::::::

        # Botones Nuevo-Edito-Borro-Guardar-Guardar como-Cancelar barra de la izquierda de arriba hacia abajo
        self.frame_botones_izquierda=LabelFrame(self.frame_grid_botones, text="", foreground="#CD5C5C")

        # cuadro 1 menu de la izquierda ----------------------------------------
        self.frame_cuadro1 = LabelFrame(self.frame_botones_izquierda, text="", bg="#CD5C5C")
        self.cuadro_botones_grid_entregados_1()
        self.frame_cuadro1.pack(side="top", fill="both", padx=5, pady=5)
        # ----------------------------------------------------------------------

        # cuadro 2 menu de la izquierda ----------------------------------------
        self.frame_cuadro2 = LabelFrame(self.frame_botones_izquierda, text="", bg="#B727F5")
        self.cuadro_botones_grid_entregados_2()
        self.frame_cuadro2.pack(side="top", fill="both", padx=5, pady=5)
        # ---------------------------------------------------------------------

        # cuadro 3 menu de la izquierda ---------------------------------------
        self.frame_cuadro3 = LabelFrame(self.frame_botones_izquierda, text="", bg="#27F5E4")
        self.cuadro_botones_grid_entregados_3()
        self.frame_cuadro3.pack(side="top", fill="both", padx=5, pady=5)
        # ---------------------------------------------------------------------

        # cuadro 4  menu de la izquierda --------------------------------------
        self.frame_cuadro4 = LabelFrame(self.frame_botones_izquierda, text="")
        self.cuadro_botones_grid_entregados_4()
        self.frame_cuadro4.pack(side="top", fill="both", expand = 1, padx=5, pady=5)
        # ----------------------------------------------------------------------

        self.frame_botones_izquierda.pack(side="left", fill="both", padx=5, pady=2)

        # PACK FRAME BARRA BOTONES IZQUIERDA ::::::::::::::::::::::::::::::::::
        # ---------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ABRO FRAME_BUSQUEDA_PRESU_ENTREGADO ::::::::::::::::::::::::::::::::::

        # BUSCAR UN PRESUPUESTO - impresion TOPE Y FIN ARCHIVO - barra horizontal superior

        self.frame_busqueda_presu_entregado=LabelFrame(self.frame_grid_botones, text="", border=5, foreground="black",
                                                  background="light blue")
        self.cuadro_buscar_presup_entregado()
        self.frame_busqueda_presu_entregado.pack(expand=0, side="top", fill="both", pady=2, padx=5)

        # PACK FRAME_BUSQUEDA_PRESU_ENTREGADO ::::::::::::::::::::::::::::::::::
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # GRID DE PRESUPUESTOS ENTREGADOS
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ABRO frame_grid_presup_entregados ::::::::::::::::::::::::::::::::::::

        # Tv donde se ven los resumenes de los persupuestos entragados
        self.frame_grid_presup_entregados=LabelFrame(self.frame_grid_botones, text="Presupuesto entregados",
                                                     foreground="#CD5C5C")
        self.cuadro_tv_presup_entregados()
        self.frame_grid_presup_entregados.pack(side="top", fill="both", padx=5, pady=2)

        # PACK FRAME_GRID_PRESUP_ENTREGADOS ::::::::::::::::::::::::::::::::::::
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # CAJA DE TEXTO PARA DETALLES EXTENSOS DE DESCRIPCION
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ABRO FRAME_CAJADETEXTO :::::::::::::::::::::::::::::::::::::::::::::::

        self.frame_cajatexto = LabelFrame(self.frame_grid_botones, text="Descripcion adicional", fg="red")
        self.cuadro_caja_texto_detalles_extensos()
        self.frame_cajatexto.pack(expand=0, side="top", fill="both", pady=3, padx=5)

        # PACK FRAME_CAJADETEXTO :::::::::::::::::::::::::::::::::::::::::::::::
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # GRID - TREEVIEW CARGA PRESUPUESTO ACTUAL
        # ----------------------------------------------------------------------
        # ----------------------------------------------------------------------
        # ABRO frame_grid_presup_actual ::::::::::::::::::::::::::::::::::::::::

        self.frame_grid_presup_actual=LabelFrame(self.frame_grid_botones, text="Componentes presupuesto actual",
                                                 foreground="#CD5C5C")
        self.cuadro_tv_presup_actual()
        self.frame_grid_presup_actual.pack(side="top", fill="both", padx=5, pady=2)

        # PACK frame_grid_presup_actual ::::::::::::::::::::::::::::::::::::::::
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        self.frame_grid_botones.pack(side="top", fill="both", padx=5, pady=2)
        # ----------------------------------------------------------------------
        # FIN CUADRO DE FRAME_GRID_BOTONES :::::::::::::::::::::::::::::::::::::
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS DATOS DEL CLIENTE
        # ----------------------------------------------------------------------
        self.frame_cliente = LabelFrame(self.master, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                        highlightbackground="blue" )
        self.entrys_datos_cliente()
        self.frame_cliente.pack(side="top", fill="both", expand=0, padx=5, pady=3)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS FORMA DE PAGO
        # ----------------------------------------------------------------------
        self.frame_forma_pago = LabelFrame(self.master, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                        highlightbackground="blue")
        self.entrys_formas_pago()
        self.frame_forma_pago.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS DATOS ARTICULO/COMPONENTE A VENDER
        # ----------------------------------------------------------------------
        self.frame_componentes = LabelFrame(self.master, text="", bg="#81EBCD", borderwidth=2, relief="solid",
                                        highlightbackground="blue")
        self.entrys_componentes()
        self.frame_componentes.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ENTRYS IMPORTES DEL PRESUPUESTO - Linea de totales del item a cargar
        # ----------------------------------------------------------------------
        self.frame_importes_articulo = LabelFrame(self.master, text="", bg="#81EBCD", foreground="black", relief="solid")
        self.entrys_precios_componentes()
        #self.frame_importes_articulo_uno.pack(side="left", fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_importes_articulo.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # LABELS TOTALES GENERALES
        # ----------------------------------------------------------------------
        self.frame_totales_generales = LabelFrame(self.master, text="", foreground="black", border=5, relief="ridge")
        self.labels_totales_generales()
        self.frame_totales_generales.pack(side="top", fill="both", expand=0, padx=5, pady=2)

    # ----------------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo_resu_presup = "resu_presup ORDER BY rp_fecha, rp_numero ASC"
        self.filtro_activo_auxiliar = "aux_presup ORDER BY ax_orden ASC"
        self.dato_seleccion = ""
        self.alta_modif_aux = 0         # tabla aux_presu
        self.alta_modif_presup = 0      # tabla resu_presu

        # limpia todos los entrys - borro los datos que puedan tener
        self.limpiar_entrys_total()
        # preparo fecha del presupuesto - paso a string
        una_fecha = date.today()
        self.strvar_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))
        # desactivo todos los entrys
        self.estado_entrys_inicial("disabled")
        # Desactivo los botones de la parte de los componentes
        self.estado_botones_dos("disabled")
        # Activo los botones del CRUD principal - Nuevo-Edito_Borro presupuesto
        self.estado_botones_uno("normal")

        # Vacio el TVW auxpresup - donde cargo los componentes
        self.varPresupuestos.vaciar_auxpresup("aux_presup")
        self.limpiar_Grid_auxiliar()

        self.alta_modif_aux = 0
        self.alta_modif_presup = 0

        # Modo activo el browse del Grid  de los presupuesto
        self.grid_tvw_presu_entregado['selectmode'] = 'browse'
        self.grid_tvw_presu_entregado.bind("<Double-Button-1>", self.DobleClickGrid)

    def estado_entrys_inicial(self, estado):

        """ Estado inicial de los entrys - cliente y componentes - solo se ejecuta una vez al entrar al modulo """

        self.entry_fecha_presup.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_componente.configure(state=estado)
        self.btn_bus_art.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)
        self.entry_dolarhoy2.configure(state=estado)
        self.entry_cantidad.configure(state=estado)
        self.entry_tasa_ganancia.configure(state=estado)
        self.entry_neto_dolar.configure(state=estado)
        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_codigo_componente.configure(state=estado)
        self.entry_total_item_redondo.configure(state=estado)
        self.text_especificaciones.configure(state=estado)
        self.btn_detalle_precio_articulo.configure(state=estado)
        self.btn_articulo.configure(state=estado)
        self.btn_reset_componente.configure(state=estado)

    def estado_entrys_crud(self, estado):

        """ Cuando pido nuevo presupuesto solo activo los entrys de resumen de presupuesto  - no de los componentes """

        self.entry_fecha_presup.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.entry_dolarhoy2.configure(state=estado)
        self.entry_tasa_ganancia.configure(state=estado)
        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)
        self.text_especificaciones.configure(state=estado)

    def estado_entrys_crud_2(self, estado):

        """ Activo entrys de la parte de (componentes) cuando presiono boton (+ componente) """

        self.entry_componente.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)
        self.entry_cantidad.configure(state=estado)
        self.entry_neto_dolar.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_codigo_componente.configure(state=estado)
        self.entry_total_item_redondo.configure(state=estado)
        self.text_especificaciones.configure(state=estado)
        self.btn_detalle_precio_articulo.configure(state=estado)
        self.btn_articulo.configure(state=estado)
        self.btn_reset_componente.configure(state=estado)

    def estado_botones_uno(self, estado):

        """ Activo/desactiva los botones principales del CRUD - nuevo, borro, edito, toparch """

        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.btn_nuevo_presup.configure(state=estado)
        self.btn_edito_presup.configure(state=estado)
        self.btn_borro_presup.configure(state=estado)
        self.btn_aceptado_presup.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_buscar.configure(state=estado)
        self.btn_imprime_presupuesto.configure(state=estado)
        #self.btn_imprime_presup_ext.configure(state=estado)
        self.entry_busqueda_presup.configure(state=estado)

        if self.alta_modif_presup == 1:
            self.grid_tvw_presu_entregado['selectmode'] = 'none'
            self.grid_tvw_presu_entregado.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif_presup == 2 or self.alta_modif_presup == 0:
            self.grid_tvw_presu_entregado['selectmode'] = 'browse'
            self.grid_tvw_presu_entregado.bind("<Double-Button-1>", self.DobleClickGrid)

    def estado_botones_dos(self, estado):

        """ Activo/desactivo los botones de la parte de los componentes - + componente - componente Cierre etc... """

        self.btn_ingresar_componente.configure(state=estado)
        self.btn_editar_componente.configure(state=estado)
        self.btn_mas_componente.configure(state=estado)
        self.btn_menos_componente.configure(state=estado)
        self.btn_cerrar_presupuesto.configure(state=estado)
        self.btn_guardar_como.configure(state=estado)
        self.btn_cancelar_presupuesto.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)
        self.btn_bus_art.configure(state=estado)

    def fNo_modifique(self, event):
        return

    def limpiar_entrys_parcial(self):

        """ Vacio los entrys relaionados con la carga del componente y totales """

        self.strvar_componente.set(value="")
        self.combo_tasa_iva.current(0)
        self.strvar_cantidad_vendida.set(value="1")
        self.strvar_neto_dolar.set(value="0.00")
        self.strvar_proveedor.set(value="")
        self.strvar_codigo_componente.set(value="")
        self.strvar_costo_neto_pesos_unidad.set(value="0.00")
        self.strvar_costo_neto_pesos_xcanti.set(value="0.00")
        self.strvar_total_item_redondo.set(value="0.00")

    def limpiar_entrys_total(self):

        """ Limpia totdos los e Entrys - se usa en inicial y para cancelar """

        una_fecha = date.today()
        self.strvar_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.strvar_nombre_cliente.set(value="Consumidor Final")
        self.strvar_codigo_cliente.set(value="0")
        self.combo_sit_fiscal_cliente.current(0)
        self.strvar_cuit.set(value="")
        self.strvar_tasa_ganancia.set(value="0.00")
        self.strvar_componente.set(value="")
        self.combo_tasa_iva.current(0)
        self.strvar_valor_dolar_hoy.set(value="0.00")
        self.traer_dolarhoy()
        self.strvar_cantidad_vendida.set(value="1")
        self.strvar_neto_dolar.set(value="0.00")
        self.combo_formapago.current(0)
        self.strvar_detalle_pago.set(value="")
        self.strvar_proveedor.set(value="")
        self.strvar_codigo_componente.set(value="")
        self.strvar_costo_neto_pesos_unidad.set(value="0.00")
        self.strvar_costo_neto_pesos_xcanti.set(value="0.00")
        self.strvar_total_presupuesto.set(value="0.00")
        self.strvar_total_ganancia.set(value="0.00")
        self.strvar_total_costos.set(value="0.00")
        self.strvar_total_item_redondo.set(value="0.00")
        self.strvar_total_presup_redondo.set(value="0.00")
        self.text_especificaciones.delete('1.0', 'end')

    def limpiar_totales(self):

        """ Limpia los totales generales """

        self.strvar_costo_neto_pesos_unidad.set(value="0.00")
        self.strvar_costo_neto_pesos_xcanti.set(value="0.00")
        self.strvar_costo_bruto_pesos_unidad.set(value="0.00")
        self.strvar_costo_bruto_pesos_xcanti.set(value="0.00")
        self.strvar_importe_iva_unidad.set(value="0.00")
        self.strvar_importe_iva_xcanti.set(value="0.00")
        self.strvar_importe_ganancia_unidad.set(value="0.00")
        self.strvar_importe_ganancia_xcanti.set(value="0.00")
        self.strvar_precio_final_unidad.set(value="0.00")
        self.strvar_precio_final_xcanti.set(value="0.00")

    # -----------------------------------------------------------------
    # GRIDS
    # -----------------------------------------------------------------

    def limpiar_Grid_resu_presup(self):

        for item in self.grid_tvw_presu_entregado.get_children():
            self.grid_tvw_presu_entregado.delete(item)

    def llena_grilla_resu_presup(self, ult_tabla_id):

        try:

            datos = self.varPresupuestos.consultar_presupuestos(self.filtro_activo_resu_presup)

            cont = 0
            for row in datos:

                cont += 1
                color = ('evenrow',) if cont % 2 else ('oddrow',)

                if row[14] == "1":
                    color = ("error",)

                """ 
                Este es el ejemplo por si quiero destacar alguna linea segun alguna condicion especial, por 
                ejemplo 'presupuesto realizado - Si un columna coincide con un valor buscado, cambie el color' 
                if row[1] == 2324:
                    color = ("error",)
                Va combinado con la siguiente linea, que hay que ponerla en el llena_grilla
                self.grid_clientes.tag_configure('error', background='green')
                va debajo de los otros dos configure de odorow y everrow
                """

                # convierto fecha de 2024-12-19 a 19/12/2024
                forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'), False)

                self.grid_tvw_presu_entregado.insert("", "end", tags=color, text=row[0], values=(row[1],
                                                                forma_normal, row[4], row[7], row[8], row[9], row[10]))

            if len(self.grid_tvw_presu_entregado.get_children()) > 0:
                   self.grid_tvw_presu_entregado.selection_set(self.grid_tvw_presu_entregado.get_children()[0])

            self.mover_puntero_topend('END')

        except:

            messagebox.showinfo("Error", "Fallo carga de grilla resu_presup", parent=self)
            return

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_tvw_presu_entregado.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_tvw_presu_entregado.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """
            """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_tvw_presu_entregado.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_tvw_presu_entregado.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_tvw_presu_entregado.yview(self.grid_tvw_presu_entregado.index(rg))
        else:
            self.mover_puntero_topend("END")

    def limpiar_Grid_auxiliar(self):

        for item in self.grid_tvw_auxcomp.get_children():
            self.grid_tvw_auxcomp.delete(item)

    def llena_grilla_auxiliar(self, ult_tabla_id):

        try:

            datos = self.varPresupuestos.consultar_presupuestos(self.filtro_activo_auxiliar)
            orden = 1
            for row in datos:
                self.grid_tvw_auxcomp.insert("", "end", text=row[0], values=(orden, row[2], row[3], row[4],
                                                                                  row[5], row[6], row[7], row[8],
                                                                                  row[9], row[10], row[11]))
                orden += 1
            if len(self.grid_tvw_auxcomp.get_children()) > 0:
                   self.grid_tvw_auxcomp.selection_set(self.grid_tvw_auxcomp.get_children()[0])

        except:

            messagebox.showinfo("Error", "Fallo carga de grilla auxiliar", parent=self)
            return

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_tvw_auxcomp.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_tvw_auxcomp.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. """

            if ult_tabla_id:

                """ "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

                self.grid_tvw_auxcomp.selection_set(rg)
                # Para que no me diga que no hay nada seleccionado
                self.grid_tvw_auxcomp.focus(rg)
                # para que la linea seleccionada no me quede fuera del area visible del treeview
                self.grid_tvw_auxcomp.yview(self.grid_tvw_auxcomp.index(rg))
            else:
                self.mover_puntero_topend("END")

    # ----------------------------------------------------------------------
    # BOTONES Nuevo presupuesto - Editar - Eliminar - Cancelar
    # ----------------------------------------------------------------------

    def fNuevo_presupuesto(self):

        self.alta_modif_presup = 1

        self.estado_entrys_crud("normal")
        self.estado_botones_uno("disabled")
        self.estado_botones_dos("normal")
        self.limpiar_entrys_total()
        self.strvar_nro_presup.set(value=str(int(self.varPresupuestos.traer_ultimo(1)) + 1))
        self.entry_fecha_presup.focus()

    def fEdito_presupuesto(self):

        self.selected = self.grid_tvw_presu_entregado.focus()
        self.clave = self.grid_tvw_presu_entregado.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.estado_entrys_crud("normal")
        self.estado_botones_uno("disabled")
        self.estado_botones_dos("normal")
        self.limpiar_entrys_total()

        self.varPresupuestos.vaciar_auxpresup("aux_presup")

        self.alta_modif_presup = 2

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_tvw_presu_entregado.item(self.selected, 'values')
        self.strvar_nro_presup.set(value=valores[0])

        # 2 - Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta

        datos_presu_entregado = self.varPresupuestos.traer_resu_presup(self.strvar_nro_presup.get())

        fechapaso = datos_presu_entregado[2].strftime('%d/%m/%Y')
        self.strvar_fecha_presup.set(fechapaso)
        self.strvar_codigo_cliente.set(value=datos_presu_entregado[3])
        self.strvar_nombre_cliente.set(value=datos_presu_entregado[4])
        self.strvar_sit_fiscal.set(value=datos_presu_entregado[5])
        self.strvar_cuit.set(value=datos_presu_entregado[6])
        self.strvar_valor_dolar_hoy.set(value=datos_presu_entregado[7])
        self.strvar_tasa_ganancia.set(value=datos_presu_entregado[8])
        self.strvar_combo_formas_pago.set(value=datos_presu_entregado[11])
        self.strvar_detalle_pago.set(value=datos_presu_entregado[12])
        self.strvar_total_presup_redondo.set(value=datos_presu_entregado[10])
        self.text_especificaciones.configure(state="normal")
        self.text_especificaciones.insert(END, datos_presu_entregado[13])

        # 3 - Cargar los componentes del presupuesto de deta_presup

        datos_detapresup = self.varPresupuestos.traer_deta_presup(self.strvar_nro_presup.get())

        for row in datos_detapresup:

            dolar_a_pesos = float(row[8]) * float(self.strvar_valor_dolar_hoy.get())
            iva_a_cargar = dolar_a_pesos * (float(row[6]) / 100)
            ganancia_a_cargar = (dolar_a_pesos + iva_a_cargar) * (float(self.strvar_tasa_ganancia.get()) / 100)
            total_presupuesto = dolar_a_pesos + iva_a_cargar + ganancia_a_cargar

            self.varPresupuestos.insertar_auxpresup(row[1], row[3], row[4], row[5], row[6], row[7], row[8],
                                                    total_presupuesto, row[9], ganancia_a_cargar, dolar_a_pesos)

        self.calcular("completo")
        self.calcular("totalpresupuesto")
        self.limpiar_Grid_auxiliar()
        self.llena_grilla_auxiliar("")







    def fBorro_presupuesto(self):

        # ----------------------------------------------------------------------
        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_tvw_presu_entregado.focus()
        self.selected_ant = self.grid_tvw_presu_entregado.prev(self.selected)
        # guardo en clave el Id pero de la Bd (no son el mismo
        self.clave = self.grid_tvw_presu_entregado.item(self.selected, 'text')
        self.clave_ant = self.grid_tvw_presu_entregado.item(self.selected_ant, 'text')
        # ----------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_tvw_presu_entregado.item(self.selected, 'values')
        #        data = str(self.clave)+" "+valores[0]+" " + valores[2]
        data = " Presupuesto Nº " + valores[0] + " de " + valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar presupuesto?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion Cancelada", parent=self)
            return

        # Elimino de resu_ventas y deta_ventas
        self.varPresupuestos.eliminar_presu_entregado1(self.clave)
        self.varPresupuestos.eliminar_detapresup(valores[0])  # por numero de venta

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid_resu_presup()
        self.llena_grilla_resu_presup(self.clave_ant)

    def fCancela_presup(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys_total()
        self.limpiar_totales()
        self.estado_inicial()
        self.varPresupuestos.vaciar_auxpresup("aux_presup")
        self.entry_fecha_presup.focus()

    def DobleClickGrid(self, event):

        self.limpiar_entrys_parcial()
        self.estado_entrys_crud_2("disabled")
        self.fEdito_presupuesto()

    def fSalir(self):

        r = messagebox.askquestion("Salir", "Confirma Salir?", parent=self)
        if r == messagebox.NO:
            return
        self.master.destroy()

    # ----------------------------------------------------------------------
    # BOTONES sobre componentes - Nuevo componente - Editar - Eliminar - Cancelar
    # ----------------------------------------------------------------------

    def fMas_componente(self):

        """ Agrega un componente al presupuesto - activa el sistema para ingresar componentes """

        # Los Entrys propios del componente
        self.estado_entrys_crud_2("normal")
        # deshabilito los botones del crud 2
        self.btn_mas_componente.configure(state="disabled")
        self.btn_menos_componente.configure(state="disabled")
        self.btn_editar_componente.configure(state="disabled")
        self.entry_componente.focus()

    def fMenos_componente(self):

        # ---------------------------------------------------------------------------------
        """ Elimina un coponente previamente cargado del presupuesto """

        self.selected = self.grid_tvw_auxcomp.focus()
        self.selected_ant = self.grid_tvw_auxcomp.prev(self.selected)
        self.clave = self.grid_tvw_auxcomp.item(self.selected, 'text')
        self.clave_ant = self.grid_tvw_auxcomp.item(self.selected_ant, 'text')
        # ---------------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_tvw_auxcomp.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        self.varPresupuestos.eliminar_auxpresup(self.clave)

        self.limpiar_Grid_auxiliar()
        self.llena_grilla_auxiliar(self.clave_ant)

        # reordenar numeros de orden para que se acomoden los numeros de orden
        self.reordenar(self.grid_tvw_auxcomp)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.calcular("totalventa")
        self.calcular("totalpresupuesto")

    def fInsertar_item_auxpresup(self):

        """ Inserto el componente en tabla auxiliar (aux_presup) """

        # VALIDACIONES
        # 1- que articulo no este vacio y que haya cantidad
        if len(self.strvar_componente.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de componente", parent=self)
            self.entry_componente.focus()
            return
        if float(self.strvar_cantidad_vendida.get()) == 0:
            messagebox.showerror("Error", "Falta cantidad de articulo", parent=self)
            self.entry_cantidad.focus()
            return

        # controlo que no sea una modificacion para borrar el componente anterior
        if self.alta_modif_aux == 1:

            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_tvw_auxcomp.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            self.clave = self.grid_tvw_auxcomp.item(self.selected, 'text')

            # ----------------------------------------------------------------
            # Si es una modificacion, guardo el numero de orden que tenia
            # ----------------------------------------------------------------
            # primer elemento de la seleccion (I001 ò I002..), NO del grid no siempre coincide con el que tiene el foco
            item = self.grid_tvw_auxcomp.selection()[0]
            # Obtener todos los valores de la fila
            valores = self.grid_tvw_auxcomp.item(item, "values")
            # "Orden" está en la columna 0 guardo el orden que tenia
            orden_item = valores[0]
            # ----------------------------------------------------------------

            self.varPresupuestos.eliminar_auxpresup(self.clave)

        else:

            total = len(self.grid_tvw_auxcomp.get_children())
            orden_item = total + 1

        # vuelvo a cero la bandera de modificacion
        self.alta_modif_aux = 0

        # Insertamos el componente en el auxilliar de presupuesto (aux_presup)

        self.varPresupuestos.insertar_auxpresup(orden_item, self.strvar_proveedor.get(), self.strvar_codigo_componente.get(),
                                                self.strvar_componente.get(), self.strvar_combo_tasa_iva.get(),
                                                self.strvar_cantidad_vendida.get(), self.strvar_neto_dolar.get(),
                                                self.strvar_precio_final_xcanti.get(),
                                                self.strvar_total_item_redondo.get(),
                                                self.strvar_importe_ganancia_xcanti.get(),
                                                self.strvar_costo_bruto_pesos_xcanti.get())

        self.calcular("totalpresupuesto")

        self.limpiar_Grid_auxiliar()

        ultimo_tabla_id = self.varPresupuestos.traer_ultimo(0)
        self.llena_grilla_auxiliar(ultimo_tabla_id)

        # dejar en blanco todos los entrys del articulo
        self.limpiar_entrys_parcial()
        # desactivar los entrys de la parte dos (componentes)
        self.estado_entrys_crud_2("disabled")
        # limpiar los totales del componente
        self.limpiar_totales()

        messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

        # Botones de la parte componentes vuelven a estado inicial (+ compon... - compon...
        self.estado_botones_dos("normal")
        self.entry_componente.focus()

    def fEditar_item_auxpresup(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_tvw_auxcomp.focus()
        # Asi obtengo la clave de la Tabla campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_auxcomp.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        # activo entrys de segundo nivel (componentes)
        self.estado_entrys_crud_2("normal")

        # Desactivo botones de novel 2 excepto "Cancelar, ingresar componente y cerrar presupuesto"
        self.estado_botones_dos("disabled")
        self.btn_ingresar_componente.configure(state="normal")
        self.btn_cerrar_presupuesto.configure(state="normal")
        self.btn_guardar_como.configure(state="normal")
        self.btn_cancelar_presupuesto.configure(state="normal")
        self.btn_reset_componente.configure(state="normal")

        # activo bandera de modificacion de tabla auxpresup
        self.alta_modif_aux = 1

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        # En la lista valores cargo toda la liena del treeview completa
        valores = self.grid_tvw_auxcomp.item(self.selected, 'values')

        self.strvar_proveedor.set(value=valores[1])
        self.strvar_codigo_componente.set(value=valores[2])
        self.strvar_componente.set(value=valores[3])
        self.strvar_combo_tasa_iva.set(value=valores[4])
        self.strvar_cantidad_vendida.set(value=valores[5])
        self.strvar_neto_dolar.set(value=valores[6])
        self.strvar_total_item_redondo.set(value=valores[8])

        self.calcular("completo")

        self.entry_componente.focus()

    def fReset_articulo(self):

        r = messagebox.askquestion("Resetr", "Confirma anular componente?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys_parcial()
        self.limpiar_totales()
        self.estado_entrys_crud_2("disabled")
        self.estado_botones_dos("normal")
        self.alta_modif_aux = 0
        self.alta_modif_presup = 0
        self.entry_componente.focus()

    # -----------------------------------------------------------------------------
    # GUARDAR PRESUPUESTOS
    # -----------------------------------------------------------------------------

    def fGuardar(self):
        self.fCerrarPresupuesto("normal")

    def fGuardar_como(self):
        self.fCerrarPresupuesto("como")

    def fCerrarPresupuesto(self, parametro):

        # VALIDACIONES

        # --------------------------------------------------------------------
        # valido que haya items en venta - Grid vacio
        if len(self.grid_tvw_auxcomp.get_children()) <= 0:
            messagebox.showerror("Error", "No hay items cargados", parent=self)
            return
        # valido nro venta - no hay numero de venta
        if self.strvar_nro_presup.get() == 0:
            messagebox.showerror("Error", "Verifique numero de venta", parent=self)
            return
        # valido fecha venta - no hay feca de venta
        if self.strvar_fecha_presup.get() == "":
            messagebox.showerror("Error", "Verifique fecha de venta", parent=self)
            return
        # valido nombre de cliente - no hay cliente asignado
        if self.strvar_nombre_cliente.get() == "":
            messagebox.showerror("Error", "Ingrese nombre de cliente", parent=self)
            return
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        if parametro == "normal":
            # Es una carga normal
            r = messagebox.askquestion("Cerrar presupuesto", "Guardamos el presupuesto? ", parent=self)
            if r == messagebox.NO:
                return

        if parametro == "como":
            # Es guardar como para generar un presupuesto igual pero con otro numero
            r = messagebox.askquestion("Presupuesto", "Duplicar presupuesto... asignando numero siguiente ", parent=self)
            if r == messagebox.NO:
                return

        if parametro == "normal":

            # Borro el presupuesto en resu_presup - por las dudas sea modificacion
            self.varPresupuestos.eliminar_detapresup(self.strvar_nro_presup.get())
            # Borro en deta_presup - por las dudas sea modificacion
            self.varPresupuestos.eliminar_presu_entregado2(self.strvar_nro_presup.get())

        if parametro == "como":

            # Si es -guardar_como- busco solamente aignar un  numero mas de presupuesto como si fuera uno nuevo
            self.strvar_nro_presup.set(value=str(int(self.varPresupuestos.traer_ultimo(1)) + 1))
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # Antes de insertar los presupuestos en las tablas principales, debo actualizar desde
        # el Grid a la tabla aux_presup - Elimino all y lo vuelvo a cargar desde el Grid

        self.varPresupuestos.actualizar_auxpresup(self.grid_tvw_auxcomp)
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # CARGA DE LAS TABLAS - CIERRE DE PRESUPUESTO
        # Inserto en DETA_PRESUP
        datos = self.varPresupuestos.consultar_detalle_auxpresup("aux_presup")

        for row in datos:

            # inserto en tabla DETA_PRESUP
            self.varPresupuestos.insertar_detapresup(row[1], self.strvar_nro_presup.get(),
                                             row[2],  # nombre proveedor
                                             row[3],  # codigo componente proveedor
                                             row[4],  # descripcion del componente
                                             row[5],  # tasa IVA del componente
                                             row[6],  # cantidad presupuestada
                                             row[7],  # costo neto componente en dolares
                                             row[9])  # Total en pesos redondeado
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        self.nuevo_presupuesto = self.strvar_nro_presup.get()

        # Inserto en RESU_PRESUP
        fecha_aux = datetime.strptime(self.strvar_fecha_presup.get(), '%d/%m/%Y')
        self.varPresupuestos.insertar_presu_entregado(self.strvar_nro_presup.get(), fecha_aux,
                                         self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                         self.combo_sit_fiscal_cliente.get(), self.strvar_cuit.get(),
                                         self.strvar_valor_dolar_hoy.get(), self.strvar_tasa_ganancia.get(),
                                         self.strvar_total_presupuesto.get(), self.strvar_total_presup_redondo.get(),
                                         self.combo_formapago.get(), self.strvar_detalle_pago.get(),
                                         self.text_especificaciones.get(1.0, 'end-1c'))
        # ---------------------------------------------------------------------------------

        messagebox.showinfo("Guardar", "Ingreso correcto detalle y resumen", parent=self)

        # refresco grid de presu_entregado para que se me actualie la grilla de resu_presup
        self.limpiar_Grid_resu_presup()

        # acomodo el puntero en el presupuesto recien ingresado
        ultimo_tabla_id = self.varPresupuestos.traer_ultimo(0)
        self.llena_grilla_resu_presup(ultimo_tabla_id)

        # pongo all en blanco como si recien iniciara para que se pueda pedir un nuevo presupuesto
        self.estado_inicial()

    # -----------------------------------------------------------------------------
    # BUSQUEDAS DE PRESUPUESTOS
    # -----------------------------------------------------------------------------

    def fBuscar_presupuesto(self):

        if len(self.strvar_buscostring.get()) > 0:

            se_busca = self.strvar_buscostring.get()
            self.filtro_activo_resu_presup = "resu_presup WHERE INSTR(rp_nomcli, '" + se_busca + "') ORDER BY rp_fecha ASC"

            self.varPresupuestos.buscar_entabla(self.filtro_activo_resu_presup)

            self.limpiar_Grid_resu_presup()
            self.llena_grilla_resu_presup("")

            """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el
            item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
            item = self.grid_tvw_presu_entregado.selection()
            self.grid_tvw_presu_entregado.focus(item)

        else:

            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

    # --------------------------------------------------------------------------
    # MOVIMIENTOS PUNTERO EN EL GRID
    # --------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('"top"')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def fSubir_uno(self):

        # Obtengo Id del item actual en el grid I001....
        actual = self.grid_tvw_auxcomp.focus()
        if not actual:
            messagebox.showwarning("Aviso", "No hay nada seleccionado", parent=self)
            return

        # 👉 (posicion del item - arranca en cero) índice del ítem dentro de su contenedor(posición) (1, 2, 3....
        #     orden de posicion o renglon
        index = self.grid_tvw_auxcomp.index(actual)
        if index == 0:
            messagebox.showwarning("Aviso", "Llegamos al principio", parent=self)
            self.grid_tvw_auxcomp.focus(actual)
            self.grid_tvw_auxcomp.selection_set(actual)
            return

        if index > 0:
            # muevo toda la inea actual a un index menor, o sea para arriba
            # Las ' ' son el parámetro el parent(padre) del ítem dentro del Treeview - vacio es raiz
            self.grid_tvw_auxcomp.move(actual, '', index - 1)
            self.grid_tvw_auxcomp.see(actual)  # 👈 también acá

        # me posiciono en el que estaba pero un renglon mas arriba
        self.grid_tvw_auxcomp.focus(actual)
        self.grid_tvw_auxcomp.selection_set(actual)

        self.reordenar(self.grid_tvw_auxcomp)

    def fBajar_uno(self):

        # Obtengo Id del item actual en el grid I001....
        actual = self.grid_tvw_auxcomp.focus()
        if not actual:
            messagebox.showwarning("Aviso", "No hay nada seleccionado", parent=self)
            return

        # 👉 (posicion del item - arranca en cero) índice del ítem dentro de su contenedor(posición) (1, 2, 3....
        #     orden de posicion o renglon
        index = self.grid_tvw_auxcomp.index(actual)
        total = len(self.grid_tvw_auxcomp.get_children())

        if index >= total - 1:
            messagebox.showwarning("Aviso", "Llegamos al final", parent=self)
            self.grid_tvw_auxcomp.focus(actual)
            self.grid_tvw_auxcomp.selection_set(actual)
            return

        if index < total - 1:
            # muevo toda la inea actual a un index mayor, o sea para abajo
            # Las ' ' son el parámetro el parent(padre) del ítem dentro del Treeview - vacio es raiz
            # .see lo hace visible dentro del grid or si os vamos muy para abajo fuera del area visible
            self.grid_tvw_auxcomp.move(actual, '', index + 1)
            self.grid_tvw_auxcomp.see(actual)  # 👈 clave

        # me posiciono en el que estaba pero un renglon mas abajo
        self.grid_tvw_auxcomp.focus(actual)
        self.grid_tvw_auxcomp.selection_set(actual)

        self.reordenar(self.grid_tvw_auxcomp)

    def reordenar(self, tree):

        """
        👉  enumerate(..., start=1)
            Recorre esa lista y te da dos cosas en cada vuelta:

            i → contador(1, 2, 3, ...)
            item → el
            id('I001', etc.)

            ✔ start = 1 hace que empiece en 1(no en 0)
        """

        for i, item in enumerate(tree.get_children(), start=1):

            # (tree.item(item, "values") Devuelve una tupla con los valores de la linea del grid
            # "list" Convierte la tupla en lista para poder modificarla
            valores = list(tree.item(item, "values"))

            # Cambia el primer valor de la lista
            valores[0] = i  # 👈 columna orden (ajustá índice si no es 0)

            # Es la que actualiza el contenido completo de la fila en el Treeview de Tkinter.
            # item es el index del registro del treeview I001, I002...
            tree.item(item, values=valores)

    def mover_puntero_topend(self, param_topend):

        # Si es tope de archivo
        if param_topend == '"top"':
            # obtengo una lista con todos los Id del treeview
            regis = self.grid_tvw_presu_entregado.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return

            # pone el primero Id
            self.grid_tvw_presu_entregado.focus(rg)
            # selecciono el Id primero de la lista en este caso
            self.grid_tvw_presu_entregado.selection_set(rg)

            # le principio del treeview con esta instruccion que encontre
            self.grid_tvw_presu_entregado.yview(self.grid_tvw_presu_entregado.index(self.grid_tvw_presu_entregado.get_children()[0]))

        # self.grid_tvw_auxcomp.focus(actual)
        # self.grid_tvw_auxcomp.selection_set(actual)

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_tvw_presu_entregado.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return

            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_tvw_presu_entregado.focus(rg)
            # Selecciono el ultimo Id en este caso
            self.grid_tvw_presu_entregado.selection_set(rg)
            # lleva el foco al final del treeview
            self.grid_tvw_presu_entregado.yview(self.grid_tvw_presu_entregado.index(self.grid_tvw_presu_entregado.get_children()[-1]))

    def fShowall(self):

        self.selected = self.grid_tvw_presu_entregado.focus()
        self.clave = self.grid_tvw_presu_entregado.item(self.selected, 'text')
        self.filtro_activo_resu_presup = "resu_presup ORDER BY rp_fecha"
        self.limpiar_Grid_resu_presup()
        self.llena_grilla_resu_presup(self.clave)

    # ----------------------------------------------------------
    # CALCULOS
    # ----------------------------------------------------------

    def calcular(self, que_campo):

        #Esta funcion solo controla todos los Entrys numericos que no contengan el valor "" o mas de un "-" o un "."
        self.control_valores()

        ii = 1
        #try:
        if ii == 1:

            if que_campo == "completo":

                # -------------------------------------------------------------
                # 1 - Costo neto unidad pesos y cantidad

                self.strvar_costo_neto_pesos_unidad.set(value=str(round(float(self.strvar_neto_dolar.get()) *
                                                                    float(self.strvar_valor_dolar_hoy.get()), 2)))

                self.strvar_costo_neto_pesos_xcanti.set(value=str(round(float(self.strvar_neto_dolar.get()) *
                                                                    float(self.strvar_valor_dolar_hoy.get()) *
                                                                    float(self.strvar_cantidad_vendida.get()), 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 2 - Importe IVA unidad y cantidad

                importe_iva = (((float(self.strvar_neto_dolar.get()) * float(self.strvar_valor_dolar_hoy.get())) *
                              float(self.strvar_combo_tasa_iva.get())) / 100)

                importe_ivaxcanti = ((((float(self.strvar_neto_dolar.get()) *
                                        float(self.strvar_valor_dolar_hoy.get())) *
                                        float(self.strvar_combo_tasa_iva.get())) / 100) *
                                        float(self.strvar_cantidad_vendida.get()))

                self.strvar_importe_iva_unidad.set(value=str(round(importe_iva, 2)))
                self.strvar_importe_iva_xcanti.set(value=str(round(importe_ivaxcanti, 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 3 - Costo BRUTO pesos unidad y cantidad

                # Costo en Pesos mas IVA * unidad
                self.strvar_costo_bruto_pesos_unidad.set(value= str(round(float(self.strvar_costo_neto_pesos_unidad.get()) +
                                                                      float(self.strvar_importe_iva_unidad.get()), 2)))
                # Costo en Pesos  ms IVA * unidad * la cantidad vendida
                self.strvar_costo_bruto_pesos_xcanti.set(value= str(round((float(self.strvar_costo_neto_pesos_unidad.get()) +
                                                                       float(self.strvar_importe_iva_unidad.get())) *
                                                                       float(self.strvar_cantidad_vendida.get()), 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 4 - Importe ganancia por unidad y por cantidad

                ganancia_unidad = round(((float(self.strvar_costo_bruto_pesos_unidad.get()) *
                                          float(self.strvar_tasa_ganancia.get())) / 100), 2)

                ganancia_xcanti = round((((float(self.strvar_costo_bruto_pesos_unidad.get()) *
                                           float(self.strvar_tasa_ganancia.get())) / 100) *
                                           float(self.strvar_cantidad_vendida.get())), 2)

                self.strvar_importe_ganancia_unidad.set(value=str(ganancia_unidad))
                self.strvar_importe_ganancia_xcanti.set(value=str(ganancia_xcanti))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 4 - Total final del componente por unidad y cantidad

                total_final_unidad = (float(self.strvar_importe_ganancia_unidad.get()) +
                                      float(self.strvar_costo_bruto_pesos_unidad.get()))
                total_final_xcanti = total_final_unidad *  float(self.strvar_cantidad_vendida.get())

                self.strvar_precio_final_unidad.set(value=str(round(total_final_unidad, 2)))
                self.strvar_precio_final_xcanti.set(value=str(round(total_final_xcanti, 2)))
                # -------------------------------------------------------------

            if que_campo == "totalpresupuesto":

                """ Guardo todos los items que compnen el presupuesto """
                datos = self.varPresupuestos.consultar_presupuestos("aux_presup")
                sumatot_presu = 0
                sumatot_redondo = 0
                sumatot_costos = 0

                """ Itero dentro de los componentes y calculo los totales generales """
                for row in datos:

                    # total costos mas IVA
                    sumatot_costos += (row[11] * (1 + (row[5]/100)))
                    sumatot_presu += row[8]
                    sumatot_redondo += row[9]

                """ La ganancia la calculo entre el total redondeado y el costo total bruto para todos los 
                articulos o componentes ingresadosde los articulos """

                sumatot_ganancia = sumatot_redondo - sumatot_costos

                # ganancia calculada sobre diferencia entre el "total redondeado" y el "costo total del articulo con IVA"
                self.strvar_total_ganancia.set(value=str(round(sumatot_ganancia, 2)))
                # total costos con IVA incluido
                self.strvar_total_costos.set(value=str(round(sumatot_costos, 2)))
                # Total del presupuesto real - sin redondeo
                self.strvar_total_presupuesto.set(value=str(round(sumatot_presu)))
                # total presupuesto redondeado
                self.strvar_total_presup_redondo.set(value=str(round(sumatot_redondo, 2)))

        else:
        #except:

            messagebox.showerror("Error", "Error en funcion de Calculos - revise entradas numericas", parent=self)
            return

    # -----------------------------------------------------------
    # VALIDACION ENTRADAS
    # -----------------------------------------------------------

    def control_valores(self):

        """ Hago Control (control_forma) de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
        Tambien todos los demas controles numericos que hacen falta """

        self.strvar_neto_dolar.set(value=control_numerico(self.strvar_neto_dolar.get(), "0"))
        self.strvar_cantidad_vendida.set(value=control_numerico(self.strvar_cantidad_vendida.get(), "1"))
        self.strvar_valor_dolar_hoy.set(value=control_numerico(self.strvar_valor_dolar_hoy.get(), "1"))
        self.strvar_tasa_ganancia.set(value=control_numerico(self.strvar_tasa_ganancia.get(), "1"))
        self.strvar_total_item_redondo.set(value=control_numerico(self.strvar_total_item_redondo.get(), "0"))

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_presup.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_presup.get())

        if retorno_VerFal == "":
            self.strvar_fecha_presup.set(value=estado_antes)
            self.entry_fecha_presup.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_presup.set(value=estado_antes)
            self.entry_fecha_presup.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_presup.set(value=retorno_VerFal)
        return ("bien")

    # -------------------------------------------------------------
    # VARIAS
    # -------------------------------------------------------------

    def traer_dolarhoy(self):

        dev_informa = self.varPresupuestos.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])

    # --------------------------------------------------------------
    # SEL CLIENTE
    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
        en que campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """  Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de 
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                                          "direccion", "Apellido y nombre", "Codigo",
                                            "Direccion", que_busco, "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:

            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])
            self.strvar_sit_fiscal.set(value=item[11])
            self.strvar_cuit.set(value=item[12])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # --------------------------------------------------------------------
    # SEL ARTICULO

    def fBusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(codbar, '" + self.strvar_componente.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.strvar_componente.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.varFuncion_new.ventana_selec("articulos", "descripcion", "codigo",
                                                        "costodolar", "Descripcion", "Codigo",
                                                        "Precio dolar neto", que_busco,
                                                        "Orden: Rubro+Marca+Descripcion", "S")

        for item in valores_new:

            self.strvar_componente.set(value=item[2]) # d<escripcion del articulo
            self.strvar_combo_tasa_iva.set(value=item[7])
            self.strvar_neto_dolar.set(value=item[6])

        self.entry_componente.focus()
        self.entry_componente.icursor(tk.END)

    def fCerrar5(self):

        self.pantalla_detalle.destroy()
        self.master.grab_set()
        self.master.focus_set()

    def fVerArticulos(self):

        vent = Toplevel()
        vent.title("ABM Articulos")
        # Asigno la clase Ventart que esta en articulos.py a la variable app
        app = Clase_Articulos(vent)
        app.mainloop()

    def fDetalle_precio_articulo(self):

        # PANTALLA FLOTANTE DETALLE PRECIO DEL ARTICULO

        self.pantalla_detalle = Toplevel()

        self.pantalla_detalle.protocol("WM_DELETE_WINDOW", self.fCerrar5)
        self.pantalla_detalle.geometry('580x260+600+400')
        self.pantalla_detalle.config(bg='#27BEF5', padx=5, pady=5)
        self.pantalla_detalle.resizable(1, 1)
        self.pantalla_detalle.title("Detalle precio del articulo")
        self.pantalla_detalle.focus_set()
        self.pantalla_detalle.grab_set()
        self.pantalla_detalle.transient(master=self.master)

        self.frame_detalle_articulo=LabelFrame(self.pantalla_detalle, text="", foreground="#CF09BD")

        # -------------------------------------------------------------------
        # DOLARES

        # DOLARES Precio neto
        lbl_neto_dolar_articulo=Label(self.frame_detalle_articulo,
        text=f"DOLARES - Costo neto x unidad: U$S {self.strvar_neto_dolar.get()} - "
             f"Total costo neto: U$S"
             f" {float(self.strvar_neto_dolar.get())*float(self.strvar_cantidad_vendida.get())}")
        lbl_neto_dolar_articulo.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        # DOLARES Importe del IVA
        self.iva_en_dolares = round(float(self.strvar_neto_dolar.get()) * (float(self.strvar_combo_tasa_iva.get()) / 100), 2)

        lbl_iva_dolar_articulo=Label(self.frame_detalle_articulo,
        text=f"DOLARES - Importe IVA x unidad: U$S {self.iva_en_dolares} - "
             f"Total IVA: U$S {self.iva_en_dolares * float(self.strvar_cantidad_vendida.get())}")
        lbl_iva_dolar_articulo.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # DOLARES Precio Bruto (con VIA)
        lbl_bruto_dolar_articulo=Label(self.frame_detalle_articulo,
        text=f"DOLARES - Costo bruto x unidad: U$S {self.iva_en_dolares+float(self.strvar_neto_dolar.get())} - "
             f"Total costo bruto: U$S "
             f"{float(self.strvar_cantidad_vendida.get()) * (self.iva_en_dolares+float(self.strvar_neto_dolar.get()))}")
        lbl_bruto_dolar_articulo.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        # ------------------------------------------------------------------
        # PESOS

        # PESOS Precio neto
        lbl_neto_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Costo neto x unidad: $ {self.strvar_costo_neto_pesos_unidad.get()} - "
             f"Total costo neto: $ {self.strvar_costo_neto_pesos_xcanti.get()}")
        lbl_neto_pesos_articulo.grid(row=3, column=0, padx=5, pady=2, sticky="w")

        # PESOS Importe del IVA
        self.iva_en_pesos = round(float(self.strvar_costo_neto_pesos_unidad.get()) * (float(self.strvar_combo_tasa_iva.get()) / 100), 2)

        lbl_iva_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Importe IVA x unidad: $ {self.iva_en_pesos} - "
             f"Total IVA: $ {self.iva_en_pesos * float(self.strvar_cantidad_vendida.get())}")
        lbl_iva_pesos_articulo.grid(row=4, column=0, padx=5, pady=2, sticky="w")

        # PESOS Precio Bruto (con VIA)
        lbl_bruto_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Costo bruto x unidad: $ {self.iva_en_pesos+float(self.strvar_costo_neto_pesos_unidad.get())} - "
             f"Total costo bruto: $ "
             f"{float(self.strvar_cantidad_vendida.get()) * (self.iva_en_pesos+float(self.strvar_costo_neto_pesos_unidad.get()))}")
        lbl_bruto_pesos_articulo.grid(row=5, column=0, padx=5, pady=2, sticky="w")

        # GANANCIA PESOS
        importe_ganancia_unidad =round(float(self.strvar_costo_bruto_pesos_unidad.get()) *
                                       (float(self.strvar_tasa_ganancia.get()) / 100), 2)
        importe_ganancia_total = importe_ganancia_unidad * float(self.strvar_cantidad_vendida.get())
        lbl_ganancia_pesos_articulo=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Ganancia: % {self.strvar_tasa_ganancia.get()} - "
             f"Importe ganancia x unidad: "
             f"{importe_ganancia_unidad} - "
             f"Total Importe ganancia: "
             f"{importe_ganancia_total}")
        lbl_ganancia_pesos_articulo.grid(row=6, column=0, padx=5, pady=2, sticky="w")

        # PRECIO VENTA FINAL EN PESOS
        precio_venta_final_unidad = round(float(self.strvar_costo_bruto_pesos_unidad.get()) *
                                          (1 + (float(self.strvar_tasa_ganancia.get()) / 100)), 2)
        precio_venta_final_total = round(precio_venta_final_unidad * float(self.strvar_cantidad_vendida.get()), 2)

        lbl_precio_pesos_venta_final=Label(self.frame_detalle_articulo,
        text=f"PESOS -      Precio venta final x unidad: {precio_venta_final_unidad} - "
             f"Precio venta final: {precio_venta_final_total} - Redondeo: {self.strvar_total_item_redondo.get()}")
        lbl_precio_pesos_venta_final.grid(row=7, column=0, padx=5, pady=2, sticky="w")

        self.frame_detalle_articulo.pack(side="top", fill="both", expand=1, padx=5, pady=5)

        self.btn_volver_pantalla = Button(self.frame_detalle_articulo, text="Volver", command=self.fCerrar5, width=22,
                                    bg="blue", fg="white")
        self.btn_volver_pantalla.grid(row=8, column=0, padx=10, pady=2, sticky="nsew")

        self.pantalla_detalle.mainloop()

    def puntero_busqueda(self,registro):

        """ # registro = Viene en blanco
            # regis = Indice del registro en el treeview tabla "I00E1", "I00F".......
            # (rg) = Es el iterante dentro de regis, esta el "Index" del Treeview (I00E, I00F...) """

        regis = self.grid_tvw_presu_entregado.get_children()
        rg = ""

        if regis != ():
            for rg in regis:
                break
            if rg == "":
                self.btn_buscar.configure(state="disabled")
                return

    def cuadro_botones_grid_entregados_1(self):

        for c in range(1):
            self.frame_cuadro1.grid_columnconfigure(c, weight=1, minsize=140)

        img = Image.open("archivo-nuevo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_nuevo_presup=Button(self.frame_cuadro1, text=" Nuevo Presupuesto",
                                    command=self.fNuevo_presupuesto, bg='blue', fg='white', compound="left")
        self.btn_nuevo_presup.image = icono
        self.btn_nuevo_presup.config(image=icono)
        self.btn_nuevo_presup.grid(row=0, column=0, padx=3, pady=3, sticky=W)

        img = Image.open("editar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_edito_presup=Button(self.frame_cuadro1, text=" Editar Presupuesto",
                                    command=self.fEdito_presupuesto, width=17, bg='blue', fg='white', compound="left")
        self.btn_edito_presup.image = icono
        self.btn_edito_presup.config(image=icono)
        self.btn_edito_presup.grid(row=1, column=0, padx=3, pady=3, sticky=W)

        img = Image.open("eliminar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_borro_presup=Button(self.frame_cuadro1, text=" Borrar Presupuesto",
                                    command=self.fBorro_presupuesto, width=17, bg='red', fg='white', compound="left")
        self.btn_borro_presup.image = icono
        self.btn_borro_presup.config(image=icono)
        self.btn_borro_presup.grid(row=2, column=0, padx=3, pady=3, sticky=W)

        img = Image.open("ordenar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_aceptado_presup=Button(self.frame_cuadro1, text=" Acepta presupuesto",
                                    command=self.fPresupuesto_aceptado, width=17, bg='#75E342', fg='black', compound="left")
        self.btn_aceptado_presup.image = icono
        self.btn_aceptado_presup.config(image=icono)
        self.btn_aceptado_presup.grid(row=3, column=0, padx=3, pady=3, sticky=W)

        # reordenamiento del frame
        for widg in self.frame_cuadro1.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def cuadro_botones_grid_entregados_2(self):

        for c in range(1):
            self.frame_cuadro2.grid_columnconfigure(c, weight=1, minsize=140)

        img = Image.open("guardar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_cerrar_presupuesto=Button(self.frame_cuadro2, text=" Actualizar/Guardar\n presupuesto",
                                           command=self.fGuardar, width=17, bg='green', fg='white', compound="left")
        self.btn_cerrar_presupuesto.image = icono
        self.btn_cerrar_presupuesto.config(image=icono)
        self.btn_cerrar_presupuesto.grid(row=3, column=0, padx=3, pady=3, sticky=W)

        img = Image.open("guardar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_guardar_como=Button(self.frame_cuadro2, text=" Guardar como...", command=self.fGuardar_como,
                                     width=17, bg='light green', fg='black', compound="left")
        self.btn_guardar_como.image = icono
        self.btn_guardar_como.config(image=icono)
        self.btn_guardar_como.grid(row=4, column=0, padx=3, pady=3, sticky=W)

        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_cancelar_presupuesto=Button(self.frame_cuadro2, text=" Cancelar", command=self.fCancela_presup,
                                             width=17, bg='black', fg='white', compound="left")
        self.btn_cancelar_presupuesto.image = icono
        self.btn_cancelar_presupuesto.config(image=icono)
        self.btn_cancelar_presupuesto.grid(row=5, column=0, padx=3, pady=3, sticky=W)

        # reordenamiento del frame
        for widg in self.frame_cuadro2.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def cuadro_botones_grid_entregados_3(self):

        # Botones +componente -com ponente Ingresar componente al presupuesto

        # for c in range(1):
        #     self.frame_cuadro3.grid_columnconfigure(c, weight=1, minsize=140)

        for c in range(2):
            self.frame_cuadro3.grid_columnconfigure(c, weight=1, minsize=70)

        # AGREGAR UN COMPONENTE
        img = Image.open("signo_mas.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_mas_componente=Button(self.frame_cuadro3, text=" Componente", command=self.fMas_componente,
                                       width=17, bg='blue', fg='white', compound="left")
        self.btn_mas_componente.image = icono
        self.btn_mas_componente.config(image=icono)
        self.btn_mas_componente.grid(row=6, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

        # QUITAR UN COMPONENTE
        img = Image.open("signo_menos.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_menos_componente=Button(self.frame_cuadro3, text=" Componente", command=self.fMenos_componente,
                                         width=17, bg='blue', fg='white', compound="left")
        self.btn_menos_componente.image = icono
        self.btn_menos_componente.config(image=icono)
        self.btn_menos_componente.grid(row=7, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

        # EDITAR COMPONENTE
        img = Image.open("editar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_editar_componente=Button(self.frame_cuadro3, text=" Editar componente",
                                           command=self.fEditar_item_auxpresup, width=17, bg='blue', fg='white', compound="left")
        self.btn_editar_componente.image = icono
        self.btn_editar_componente.config(image=icono)
        self.btn_editar_componente.grid(row=8, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

        # INGRESAR COMPONENTE AL GRID DE PRESUPUESTO ACTUAL
        img = Image.open("agregar-producto.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_ingresar_componente=Button(self.frame_cuadro3, text=" Actualizar\ncomponente",
                                           command=self.fInsertar_item_auxpresup, width=17, bg='blue',
                                           fg='white', compound="left")
        self.btn_ingresar_componente.image = icono
        self.btn_ingresar_componente.config(image=icono)
        self.btn_ingresar_componente.grid(row=9, column=0, columnspan=2, padx=3, pady=3, sticky="nsew")

        # CANCELAR LA CARGA DEL COMPONENTE AL GRID DE PRESUPUESTO ACTUAL
        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_reset_componente=Button(self.frame_cuadro3, text=" Anular ingreso\nde componente",
                                         command=self.fReset_articulo, width=17, bg='black', fg='white', compound="left")
        self.btn_reset_componente.image = icono
        self.btn_reset_componente.config(image=icono)
        self.btn_reset_componente.grid(row=10, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")

        img = Image.open("flecha_arriba.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_flecha_sube=Button(self.frame_cuadro3, text="", command=self.fSubir_uno, width=5, bg='white', fg='black')
        self.btn_flecha_sube.image = icono
        self.btn_flecha_sube.config(image=icono)
        self.btn_flecha_sube.grid(row=11, column=0, padx=2, pady=2, sticky="nsew")

        img = Image.open("flecha_abajo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_flecha_baja=Button(self.frame_cuadro3, text="", command=self.fBajar_uno, width=5, bg='white', fg='black')
        self.btn_flecha_baja.image = icono
        self.btn_flecha_baja.config(image=icono)
        self.btn_flecha_baja.grid(row=11, column=1, padx=2, pady=2, sticky="nsew")

        # reordenamiento del frame
        for widg in self.frame_cuadro3.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def cuadro_botones_grid_entregados_4(self):

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_cuadro4, text="Salir", image=self.photo3, width=133, height=40, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=0, padx=3, pady=3, sticky = 'nsew')

    def cuadro_buscar_presup_entregado(self):

        # BARRA SUPERIOR

        for c in range(1):
            self.frame_busqueda_presu_entregado.grid_columnconfigure(c, weight=1, minsize=140)

        img = Image.open("buscar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.lbl_busqueda_presup = Label(self.frame_busqueda_presu_entregado, text=" Buscar presupuesto por cliente: ",
                                         justify="left", bg="light blue", compound="left")
        self.lbl_busqueda_presup.image = icono
        self.lbl_busqueda_presup.config(image=icono)
        self.lbl_busqueda_presup.grid(row=0, column=0, padx=3, pady=2, sticky="nsew")

        # ENTRY BUSCAR PRESUPUESTO REALIZADO
        self.entry_busqueda_presup = Entry(self.frame_busqueda_presu_entregado, textvariable=self.strvar_buscostring,
                                                  state='normal', width=23, justify="left")
        self.entry_busqueda_presup.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # BOTON BUSCAR PRESUPUESTO
        img = Image.open("filtrar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_buscar=Button(self.frame_busqueda_presu_entregado, text=" Buscar", command=self.fBuscar_presupuesto,
                               bg='Blue', fg='white', width=95, compound="left")
        self.btn_buscar.image = icono
        self.btn_buscar.config(image=icono)
        self.btn_buscar.grid(row=0, column=2, padx=3, pady=2, sticky="nsew")

        # BOTON MOSTRAR TODO
        img = Image.open("ver_todo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_showall=Button(self.frame_busqueda_presu_entregado, text=" Mostrar todo", command=self.fShowall,
                                bg='Blue', fg='white', width=95, compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=3, pady=2, sticky="nsew")

        # ------------------------------------------------------------------------
        # BOTONES IMPRESION

        # IMPRIMIR PRESUPUESTO INTERNO
        img = Image.open("impresora.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_showall.grid(row=0, column=3, padx=4, pady=2, sticky=W)
        self.btn_imprime_presupuesto=Button(self.frame_busqueda_presu_entregado, text=" Presupuesto",
                                           command=self.MenuListados, width=105, bg='#5F9EF5', fg='white', compound="left")
        self.btn_imprime_presupuesto.image = icono
        self.btn_imprime_presupuesto.config(image=icono)
        self.btn_imprime_presupuesto.grid(row=0, column=4, padx=4, pady=2, sticky="nsew")

        # # IMPRIMIR PRESUPUESTO INTERNO
        # img = Image.open("impresora.png").resize((18, 18))
        # icono = ImageTk.PhotoImage(img)
        # self.btn_imprime_presup_ext=Button(self.frame_busqueda_presu_entregado, text=" Presup. externo",
        #                                    command=self.creopdfext, width=105, bg='#5F9EF5', fg='white', compound="left")
        # self.btn_imprime_presup_ext.image = icono
        # self.btn_imprime_presup_ext.config(image=icono)
        # self.btn_imprime_presup_ext.grid(row=0, column=5, padx=4, pady=2, sticky="nsew")
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # BOTONES FIN PRINCIPIO ARCHIVO

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((18, 18), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_busqueda_presu_entregado, text="", image=self.photo4, command=self.fToparch,
                                 bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=6, padx=4, sticky="nsew", pady=2)

        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((18, 18), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_busqueda_presu_entregado, text="", image=self.photo5, command=self.fFinarch,
                                 bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=7, padx=4, sticky="nsew", pady=2)

        # reordenamiento del frame
        for widg in self.frame_busqueda_presu_entregado.winfo_children():
            widg.grid_configure(padx=4, pady=3, sticky='nsew')

    def cuadro_caja_texto_detalles_extensos(self):

        # CAJA DONDE SE ESCRIBE EL DETALLE EXTENSO DEL ARTICULO EJ.: NOTEBOOKS

        self.text_especificaciones = ScrolledText(self.frame_cajatexto)
        self.text_especificaciones.config(width=100, height=4, wrap="word", padx=5, pady=5)
        self.text_especificaciones.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def cuadro_tv_presup_actual(self):

        # Tv del presupuesto actual o el que estamos recien creando en auxcomp tabla auxilliar

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_presup_actual)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_auxcomp = ttk.Treeview(self.frame_grid_presup_actual, height=7, columns=("col1", "col2", "col3",
                                                                                               "col4", "col5", "col6",
                                                                                               "col7", "col8", "col9",
                                                                                               "col10", "col11"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        self.grid_tvw_auxcomp.column("#0", width=50, anchor="center", minwidth=50)
        self.grid_tvw_auxcomp.column("col1", width=30, anchor="w", minwidth=30)
        self.grid_tvw_auxcomp.column("col2", width=45, anchor="w", minwidth=45)
        self.grid_tvw_auxcomp.column("col3", width=90, anchor="center", minwidth=90)
        self.grid_tvw_auxcomp.column("col4", width=250, anchor="center", minwidth=250)
        self.grid_tvw_auxcomp.column("col5", width=50, anchor="center", minwidth=50)
        self.grid_tvw_auxcomp.column("col6", width=30, anchor="center", minwidth=30)
        self.grid_tvw_auxcomp.column("col7", width=100, anchor="center", minwidth=100)
        self.grid_tvw_auxcomp.column("col8", width=80, anchor="center", minwidth=80)
        self.grid_tvw_auxcomp.column("col9", width=90, anchor="center", minwidth=90)
        self.grid_tvw_auxcomp.column("col10", width=80, anchor="center", minwidth=80)
        self.grid_tvw_auxcomp.column("col11", width=80, anchor="center", minwidth=80)
        #self.grid_tvw_auxcomp.column("col12", width=100, anchor="center", minwidth=80)

        self.grid_tvw_auxcomp.heading("#0", text="Id", anchor="center")
        self.grid_tvw_auxcomp.heading("col1", text="Ord.", anchor="w")
        self.grid_tvw_auxcomp.heading("col2", text="Prov.", anchor="w")
        self.grid_tvw_auxcomp.heading("col3", text="Cod.Compon.", anchor="w")
        self.grid_tvw_auxcomp.heading("col4", text="Componente", anchor="center")
        self.grid_tvw_auxcomp.heading("col5", text="%IVA", anchor="center")
        self.grid_tvw_auxcomp.heading("col6", text="Cant.", anchor="center")
        self.grid_tvw_auxcomp.heading("col7", text="Costo Neto U$S", anchor="center")
        self.grid_tvw_auxcomp.heading("col8", text="Tot. Presupuesto", anchor="center")
        self.grid_tvw_auxcomp.heading("col9", text="Tot. Redondeo", anchor="center")
        self.grid_tvw_auxcomp.heading("col10", text="Tot. Ganancia", anchor="center")
        self.grid_tvw_auxcomp.heading("col11", text="Tot. Costo", anchor="center")
        #self.grid_tvw_auxcomp.heading("col12", text="Total Costo", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_grid_presup_actual, orient="horizontal")
        scroll_y = Scrollbar(self.frame_grid_presup_actual, orient="vertical")
        self.grid_tvw_auxcomp.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_auxcomp.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_auxcomp.xview)
        scroll_y.config(command=self.grid_tvw_auxcomp.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_tvw_auxcomp['selectmode'] = 'browse'
        self.grid_tvw_auxcomp.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def cuadro_tv_presup_entregados(self):

        # Tv de los presupuestos ya realizados o historicos

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_presup_entregados)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_presu_entregado = ttk.Treeview(self.frame_grid_presup_entregados, height=6, columns=("col1",
                                                                                       "col2", "col3", "col4", "col5",
                                                                                       "col6", "col7", "col8", "col9"))

        self.grid_tvw_presu_entregado.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_tvw_presu_entregado.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_tvw_presu_entregado.column("col1", width=100, anchor="w", minwidth=100)
        self.grid_tvw_presu_entregado.column("col2", width=80, anchor="w", minwidth=80)
        self.grid_tvw_presu_entregado.column("col3", width=350, anchor="center", minwidth=350)
        self.grid_tvw_presu_entregado.column("col4", width=100, anchor="center", minwidth=100)
        self.grid_tvw_presu_entregado.column("col5", width=100, anchor="center", minwidth=100)
        self.grid_tvw_presu_entregado.column("col6", width=130, anchor="center", minwidth=130)
        self.grid_tvw_presu_entregado.column("col7", width=130, anchor="center", minwidth=130)
        self.grid_tvw_presu_entregado.column("col8", width=130, anchor="center", minwidth=130)
        self.grid_tvw_presu_entregado.column("col9", width=130, anchor="center", minwidth=130)

        self.grid_tvw_presu_entregado.heading("#0", text="Id", anchor="center")
        self.grid_tvw_presu_entregado.heading("col1", text="Nº Venta", anchor="w")
        self.grid_tvw_presu_entregado.heading("col2", text="Fecha", anchor="w")
        self.grid_tvw_presu_entregado.heading("col3", text="Cliente", anchor="center")
        self.grid_tvw_presu_entregado.heading("col4", text="Dolar", anchor="center")
        self.grid_tvw_presu_entregado.heading("col5", text="% Ganancia", anchor="center")
        self.grid_tvw_presu_entregado.heading("col6", text="Total venta", anchor="center")
        self.grid_tvw_presu_entregado.heading("col7", text="Redondeo", anchor="center")
        self.grid_tvw_presu_entregado.heading("col8", text="Forma pago", anchor="center")
        self.grid_tvw_presu_entregado.heading("col9", text="Detalle pago", anchor="center")

        self.grid_tvw_presu_entregado.tag_configure('oddrow', background='light grey')
        self.grid_tvw_presu_entregado.tag_configure('evenrow', background='white')
        self.grid_tvw_presu_entregado.tag_configure('error', background='#AADE64')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_grid_presup_entregados, orient="horizontal")
        scroll_y = Scrollbar(self.frame_grid_presup_entregados, orient="vertical")
        self.grid_tvw_presu_entregado.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_presu_entregado.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_presu_entregado.xview)
        scroll_y.config(command=self.grid_tvw_presu_entregado.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_tvw_presu_entregado['selectmode'] = 'browse'

        self.grid_tvw_presu_entregado.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def entrys_datos_cliente(self):

        fff = tkFont.Font(family="Arial", size=8, weight="bold")
        www = tkFont.Font(family="Arial", size=10, weight="bold")

        for c in range(15):
            self.frame_cliente.grid_columnconfigure(c, weight=1, minsize=30)

        # NUMERO DE PRESUPUESTO
        self.lbl_nro_presup = Label(self.frame_cliente, text="Nº: ", width=2, font=www, fg="red", bg="#CEF2EF", justify="right")
        self.lbl_nro_presup.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_nro_presup2 = Label(self.frame_cliente, textvariable=self.strvar_nro_presup, font=www, width=2, bg="#CEF2EF",
                                     fg="red")
        self.lbl_nro_presup2.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        # FECHA DE VENTA
        self.lbl_fecha_presup = Label(self.frame_cliente, text="Fecha: ", bg="#CEF2EF", justify="right")
        self.lbl_fecha_presup.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_fecha_presup = Entry(self.frame_cliente, textvariable=self.strvar_fecha_presup, width=11)
        self.entry_fecha_presup.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.entry_fecha_presup.bind("<FocusOut>", self.formato_fecha)

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((18, 18), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_cliente, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=3, pady=2, sticky='nsew')

        # NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_cliente, text="Cliente: ", bg="#CEF2EF", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=5, padx=3, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_cliente, textvariable=self.strvar_nombre_cliente, width=40)
        self.entry_nombre_cliente.grid(row=0, column=6, padx=3, pady=2, sticky=W)
        self.strvar_nombre_cliente.trace("w", lambda *args: limitador(self.strvar_nombre_cliente, 50))

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = Label(self.frame_cliente, text="SF", bg="#CEF2EF")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=3, pady=2, sticky=W)
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_cliente, textvariable=self.strvar_sit_fiscal,
                                                     justify="left", state='readonly', width=22)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky=W)

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = Label(self.frame_cliente, text="CUIT:", bg="#CEF2EF", justify="left")
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=3, pady=2, sticky=W)
        self.entry_cuit_cliente = Entry(self.frame_cliente, textvariable=self.strvar_cuit, justify="right", width=13)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=3, pady=2, sticky=W)

        # % GANANCIA
        self.lbl_tasa_ganancia = Label(self.frame_cliente, text="Gan.%: ", bg="#CEF2EF", justify="left")
        self.lbl_tasa_ganancia.grid(row=0, column=11, padx=3, pady=2, sticky=W)
        self.entry_tasa_ganancia = Entry(self.frame_cliente, textvariable=self.strvar_tasa_ganancia, width=6,
                                         justify="right")
        self.entry_tasa_ganancia.grid(row=0, column=12, padx=3, pady=2, sticky=E)
        self.entry_tasa_ganancia.config(validate="key", validatecommand=self.vcmd)
        self.entry_tasa_ganancia.bind('<Tab>', lambda e: self.calcular("completo"))

        # COTIZACION DEL DOLAR DEL DIA
        #fff = tkFont.Font(family="Arial", size=8, weight="bold")
        self.lbl_dolarhoy1 = Label(self.frame_cliente, text="Dolar:", justify="left", bg="#CEF2EF", foreground="red")
        self.lbl_dolarhoy1.grid(row=0, column=13, padx=3, pady=2, sticky=W)
        self.entry_dolarhoy2 = Entry(self.frame_cliente, textvariable=self.strvar_valor_dolar_hoy, width=10,
                                     justify="right", foreground="red")
        self.entry_dolarhoy2.grid(row=0, column=14, padx=3, pady=2, sticky=E)

        for widg in self.frame_cliente.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def entrys_formas_pago(self):

        for c in range(4):
            self.frame_forma_pago.grid_columnconfigure(c, weight=1, minsize=30)

        # forma de pago y detalle
        self.lbl_combo_formapago = Label(self.frame_forma_pago, text="Forma de Pago: ", bg="#CEF2EF", justify="left")
        self.lbl_combo_formapago.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.combo_formapago = ttk.Combobox(self.frame_forma_pago, textvariable=self.strvar_combo_formas_pago,
                                            state='readonly', width=15)
        self.combo_formapago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                         "Tarjeta Credito", "Cheque"]
        self.combo_formapago.current(0)
        self.combo_formapago.grid(row=0, column=1, padx=4, pady=2, sticky=W)

        # Detalle de pago
        self.lbl_deta_formapago = Label(self.frame_forma_pago, text="Detalle: ", bg="#CEF2EF", justify="left")
        self.lbl_deta_formapago.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_deta_formapago = Entry(self.frame_forma_pago, textvariable=self.strvar_detalle_pago, width=123)
        self.entry_deta_formapago.grid(row=0, column=3, padx=4, pady=2, sticky=W)

        for widg in self.frame_forma_pago.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def entrys_componentes(self):

        for c in range(13):
            self.frame_componentes.grid_columnconfigure(c, weight=1, minsize=30)

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((18, 18), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = Button(self.frame_componentes, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=2, pady=2, sticky=E)

        # ENTRY ARTICULO
        self.lbl_componente = Label(self.frame_componentes, text="Componente: ", bg="#81EBCD", justify="left")
        self.lbl_componente.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        self.entry_componente = Entry(self.frame_componentes, textvariable=self.strvar_componente, width=51,
                                      justify="left")
        self.entry_componente.grid(row=0, column=2, padx=2, pady=2, sticky=E)
        self.strvar_componente.trace("w", lambda *args: limitador(self.strvar_componente, 95))

        # COMBO TASA IVA
        self.lbl_combo_tasa_iva = Label(self.frame_componentes, justify="left", foreground="black", bg="#81EBCD",
                                        text="IVA %")
        self.lbl_combo_tasa_iva.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.combo_tasa_iva = ttk.Combobox(self.frame_componentes, textvariable=self.strvar_combo_tasa_iva,
                                           state='readonly', width=6)
        self.combo_tasa_iva['value'] = ["21.00", "10.50"]
        self.combo_tasa_iva.current(0)
        self.combo_tasa_iva.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.combo_tasa_iva.bind('<Tab>', lambda e: self.calcular("completo"))

        # ENTRY CANTIDAD
        self.lbl_cantidad = Label(self.frame_componentes, text="Cant.: ", bg="#81EBCD", justify="left")
        self.lbl_cantidad.grid(row=0, column=7, padx=2, pady=2, sticky=W)
        self.entry_cantidad = Entry(self.frame_componentes, textvariable=self.strvar_cantidad_vendida, width=4,
                                    justify="right")
        self.entry_cantidad.grid(row=0, column=8, padx=2, pady=2, sticky=E)
        self.entry_cantidad.config(validate="key", validatecommand=self.vcmd)
        self.entry_cantidad.bind('<Tab>', lambda e: self.calcular("completo"))

        # ENTRY NETO DOLAR
        self.lbl_neto_dolar = Label(self.frame_componentes, text="Neto dolar: ", bg="#81EBCD", justify="left")
        self.lbl_neto_dolar.grid(row=0, column=9, padx=2, pady=2, sticky=W)
        self.entry_neto_dolar = Entry(self.frame_componentes, textvariable=self.strvar_neto_dolar, width=8,
                                      justify="right")
        self.entry_neto_dolar.grid(row=0, column=10, padx=2, pady=2, sticky=E)
        self.entry_neto_dolar.config(validate="key", validatecommand=self.vcmd)
        self.entry_neto_dolar.bind('<Tab>', lambda e: self.calcular("completo"))

        self.lbl_proved = Label(self.frame_componentes, text="Prov.: ", bg="#81EBCD", justify="left")
        self.lbl_proved.grid(row=0, column=11, padx=2, pady=2, sticky=W)
        self.entry_proved = Entry(self.frame_componentes, textvariable=self.strvar_proveedor, width=15, justify="left")
        self.entry_proved.grid(row=0, column=12, padx=2, pady=2, sticky=W)

        self.lbl_codigo_componente = Label(self.frame_componentes, text="Cod.: ", bg="#81EBCD", justify="left")
        self.lbl_codigo_componente.grid(row=0, column=13, padx=2, pady=2, sticky=W)
        self.entry_codigo_componente = Entry(self.frame_componentes, textvariable=self.strvar_codigo_componente,
                                             width=15, justify="left")
        self.entry_codigo_componente.grid(row=0, column=14, padx=2, pady=2, sticky=W)

        for widg in self.frame_componentes.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def entrys_precios_componentes(self):

        fff = tkFont.Font(family="Arial", size=9, weight="bold")

        for c in range(12):
            self.frame_importes_articulo.grid_columnconfigure(c, weight=1, minsize=30)

        # COSTO PESOS CON IVA
        self.lbl_costo_pesos_bruto_unidad = Label(self.frame_importes_articulo, text="Costo Unidad: ", bg="#81EBCD", justify="left")
        self.lbl_costo_pesos_bruto_unidad.grid(row=2, column=0, padx=1, pady=2, sticky=W)
        self.lbl_costo_pesos_bruto_unidad2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_costo_bruto_pesos_unidad, width=10,
                                                  font= fff, fg="blue", justify="right")
        self.lbl_costo_pesos_bruto_unidad2.grid(row=2, column=1, padx=1, pady=2, sticky=E)

        # COSTO PESOS CON IVA * CANTIDAD
        self.lbl_costo_bruto_pesos_xcanti = Label(self.frame_importes_articulo, text="Costo total: ", bg="#81EBCD", justify="left")
        self.lbl_costo_bruto_pesos_xcanti.grid(row=2, column=2, padx=1, pady=2, sticky=W)
        self.lbl_costo_bruto_pesos_xcanti2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_costo_bruto_pesos_xcanti, width=10,
                                                  font= fff, fg="blue", justify="right")
        self.lbl_costo_bruto_pesos_xcanti2.grid(row=2, column=3, padx=1, pady=2, sticky=E)

        # IMPORTE PESOS GANANCIA * CANTIDAD
        self.lbl_importe_ganancia_xcanti = Label(self.frame_importes_articulo, text="Ganancia: ", bg="#81EBCD", justify="left")
        self.lbl_importe_ganancia_xcanti.grid(row=2, column=4, padx=1, pady=2, sticky=W)
        self.lbl_importe_ganancia_xcanti2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_importe_ganancia_xcanti, width=10,
                                                  fg="blue", font= fff, justify="right")
        self.lbl_importe_ganancia_xcanti2.grid(row=2, column=5, padx=1, pady=2, sticky=E)

        # PRECIO DE VENTA
        self.lbl_precio_final_xcanti = Label(self.frame_importes_articulo, text="Precio venta: ", bg="#81EBCD", justify="left")
        self.lbl_precio_final_xcanti.grid(row=2, column=6, padx=1, pady=2, sticky=W)
        self.lbl_precio_final_xcanti2 = Label(self.frame_importes_articulo,
                                                  textvariable=self.strvar_precio_final_xcanti, width=10,
                                                  fg="blue", font= fff, justify="right")
        self.lbl_precio_final_xcanti2.grid(row=2, column=7, padx=1, pady=2, sticky=E)

        # Redondeo del total del Item
        self.lbl_total_item_redondo = Label(self.frame_importes_articulo, text="Redondeo: ", bg="#81EBCD", justify="left")
        self.lbl_total_item_redondo.grid(row=2, column=8, padx=1, pady=2, sticky=W)
        self.entry_total_item_redondo = Entry(self.frame_importes_articulo, textvariable=self.strvar_total_item_redondo,
                                              width=15, justify="right")
        self.entry_total_item_redondo.grid(row=2, column=9, padx=1, pady=2, sticky=E)
        self.entry_total_item_redondo.config(validate="key", validatecommand=self.vcmd)
        self.entry_total_item_redondo.bind('<Tab>', lambda e: self.calcular("precio_venta_unidad"))

        self.btn_detalle_precio_articulo=Button(self.frame_importes_articulo, text="Detalle precio",
                                                command=self.fDetalle_precio_articulo, width=15, bg='blue', fg='white')
        self.btn_detalle_precio_articulo.grid(row=2, column=10, padx=5, pady=2, sticky=W)

        self.btn_articulo=Button(self.frame_importes_articulo, text="Articulos",
                                                command=self.fVerArticulos, width=16, bg='blue', fg='white')
        self.btn_articulo.grid(row=2, column=11, padx=5, pady=2, sticky=W)

        for widg in self.frame_importes_articulo.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def labels_totales_generales(self):

        fff = tkFont.Font(family="Arial", size=9, weight="bold")

        for c in range(8):
            self.frame_totales_generales.grid_columnconfigure(c, weight=1, minsize=30)

        # TOTAL COSTO BRUTO
        self.lbl_total_costos = Label(self.frame_totales_generales, text="Total Costos: ", justify="left", font=fff,
                                      foreground="#ff33f6")
        self.lbl_total_costos.grid(row=0, column=0, padx=8, pady=2, sticky=W)
        self.lbl_total_costos2 = Label(self.frame_totales_generales, textvariable=self.strvar_total_costos, width=15,
                                       justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_costos2.grid(row=0, column=1, padx=8, pady=2, sticky=E)

        # TOTAL GANANCIA
        self.lbl_total_ganancia = Label(self.frame_totales_generales, text="Total ganancia: ", justify="left", font=fff,
                                        foreground="#ff33f6")
        self.lbl_total_ganancia.grid(row=0, column=2, padx=8, pady=2, sticky=W)
        self.lbl_total_ganancia2 = Label(self.frame_totales_generales, textvariable=self.strvar_total_ganancia,
                                         width=15, justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_ganancia2.grid(row=0, column=3, padx=8, pady=2, sticky=E)

        # TOTAL PRESUPUESTO GLOBAL
        self.lbl_total_presupuesto = Label(self.frame_totales_generales, text="Total presupuesto: ", justify="left",
                                           font=fff, foreground="#ff33f6")
        self.lbl_total_presupuesto.grid(row=0, column=4, padx=8, pady=2, sticky=W)
        self.lbl_total_presupuesto2 = Label(self.frame_totales_generales, textvariable=self.strvar_total_presupuesto,
                                            width=15, justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_presupuesto2.grid(row=0, column=5, padx=8, pady=2, sticky=E)

        # TOTAL PRESUPUESTO REDONDEADO
        self.lbl_total_presup_redondo = Label(self.frame_totales_generales, text="Total redondeado: ", justify="left",
                                              font=fff, foreground="#ff33f6")
        self.lbl_total_presup_redondo.grid(row=0, column=6, padx=8, pady=2, sticky=W)
        self.lbl_total_presup_redondo2 = Label(self.frame_totales_generales,
                                               textvariable=self.strvar_total_presup_redondo, width=15, justify="right",
                                               font=fff, foreground="#ff33f6")
        self.lbl_total_presup_redondo2.grid(row=0, column=7, padx=8, pady=2, sticky=E)

        for widg in self.frame_totales_generales.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def fPresupuesto_aceptado(self):

        # ----------------------------------------------------------------------
        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_tvw_presu_entregado.focus()
        # guardo en clave el Id pero de la tabla (no son el mismo)
        self.clave = self.grid_tvw_presu_entregado.item(self.selected, 'text')
        # ----------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("", "No hay nada seleccionado", parent=self)
            return

        # consulto el registro en la tabla para saber e estado de la marca de aceptado (si esta ya aceptadoo o no)
        datos = self.varPresupuestos.consultar_presupuestos(f"resu_presup WHERE id={self.clave}")

        # si esta marcado como aceptado lo cambio a no aceptado y a la inversa
        marca_aceptado = "0"
        for i in datos:
            if i[14] == "0":
                marca_aceptado = "1"

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_tvw_presu_entregado.item(self.selected, 'values')
        #        data = str(self.clave)+" "+valores[0]+" " + valores[2]
        data = " Presupuesto Nº " + valores[0] + " de " + valores[2]

        r = messagebox.askquestion("", "Confirma cambio de estado presupuesto?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("", "Cancelado", parent=self)
            return

        # paso self.clave que es el Id de la tabla y la marca para aceptar o des_aceptar
        self.varPresupuestos.marcar_presup_aceptado(self.clave, marca_aceptado)

        if marca_aceptado == "1":
            messagebox.showinfo("", "Presupuesto aceptado", parent=self)
        else:
            messagebox.showinfo("", "Presupuesto NO aceptado", parent=self)

        self.limpiar_Grid_resu_presup()
        self.llena_grilla_resu_presup(self.clave)

    # ------------------------------------------------------------------------
    # INFORMES
    # ------------------------------------------------------------------------

    def MenuListados(self):

        # ---------------------------------------------------------------------------
        # DEFINO PANTALLA FLOTANTE

        self.pantalla_imprimir = Toplevel()
        self.pantalla_imprimir.geometry('630x260+660+380')
        self.pantalla_imprimir.transient(master=self.master)
        self.pantalla_imprimir.config(bg='light green', padx=5, pady=5)
        self.pantalla_imprimir.resizable(False, False)
        self.pantalla_imprimir.title("Seleccion formato Informe")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # TITULOS

        self.frame_titulo_impresion = Frame(self.pantalla_imprimir, bg="light green")

        # Armo el logo y el titulo
        self.photo = Image.open('impresora.png')
        self.photo = self.photo.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_select = ImageTk.PhotoImage(self.photo)
        self.lbl_png_select = tk.Label(self.frame_titulo_impresion, image=self.png_select, bg="red", relief="ridge", bd=5)

        self.lbl_tit = tk.Label(self.frame_titulo_impresion, width=29, text="Seleccion formato Informe",
                             bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_select.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_tit.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_impresion.pack(side="top", fill="x", padx=5, pady=2)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # Seleccion del informe

        # Variable compartida
        opcion_listado = tk.IntVar(value=1)  # Listado 1 por defecto

        # ===== Frame de opciones =====
        frame_opciones = tk.LabelFrame(
            self.pantalla_imprimir,
            bg="light green",
            text="Seleccion de listado"
        )
        frame_opciones.pack(padx=15, pady=15, fill="x")

        tk.Radiobutton(
            frame_opciones,
            text="Impresion presupuesto Interno, con todo el detalle de precios por componente.                   ",
            variable=opcion_listado,
            bg="light green",
            value=1
        ).pack(anchor="center", padx=15, pady=5)

        tk.Radiobutton(
            frame_opciones,
            text="Impresion presupuesto externo solo con los componentes CON precio final de cada uno.   ",
            variable=opcion_listado,
            bg="light green",
            value=2
        ).pack(anchor="center", padx=15, pady=5)

        tk.Radiobutton(
            frame_opciones,
            text="Impresion presupuesto externo solo con los componentes SIN precio de cada uno de ellos.",
            variable=opcion_listado,
            bg="light green",
            value=3
        ).pack(anchor="center", padx=15, pady=5)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # ===== Funciones =====
        def continuar():

            opcion = opcion_listado.get()

            if opcion == 1:
                # Presupuesto interno con all detalle precios y ganancias
                self.creopdfint()
            elif opcion == 2:
                # Presupuesto externo con precios por componente
                self.creopdfext("S")
            elif opcion == 3:
                # Presupuesto externo SIN precios por componente
                self.creopdfext("N")

        def cancelar():
            self.pantalla_imprimir.destroy()

        # ----------------------------------------------------------------------
        # BOTONES INFORME

        # ===== Frame de botones =====
        frame_botones = tk.Frame(self.pantalla_imprimir, bg="light green")
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Continuar",
            width=20,
            command=continuar
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            frame_botones,
            text="Salir",
            width=20,
            command=cancelar
        ).grid(row=0, column=1, padx=10)
        # ----------------------------------------------------------------------

        self.pantalla_imprimir.grab_set()
        self.pantalla_imprimir.focus_set()

    def creopdfext(self, precios):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_tvw_presu_entregado.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_presu_entregado.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # ----------------------------------------------------------------------------------
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
        # ----------------------------------------------------------------------------------

        # Cargo la linea del treeview de resu_presu
        valores = self.grid_tvw_presu_entregado.item(self.selected, 'values')

        # sdf = datetime.strptime(valores[1], '%Y-%m-%d')
        # feac = sdf.strftime('%d-%m-%Y')

        # armado de encabezado
        fecha_presup = valores[1]
        self.pdf_numero_presupuesto   = valores[0]
        self.pdf_nombre_cliente       = valores[2]
        self.pdf_dolar_presupuesto    = valores[3]
        self.pdf_tasa_ganancia        = valores[4]
        self.pdf_total_presup_redondo = valores[6]

        # Traigo, si es que hay, el detalle extenso del producto presupuestado de la tabla resu_presup
        datos_presu_entregado = self.varPresupuestos.traer_resu_presup(self.pdf_numero_presupuesto)
        self.pdf_detalle = datos_presu_entregado[13]

        # Encabezado
        self.pdf_datos_encabezado_orden = '('+self.pdf_numero_presupuesto+') - '+self.pdf_nombre_cliente
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Fecha: ' + fecha_presup + '  -  Numero Presupuesto ' + self.pdf_datos_encabezado_orden,
                 border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.cell(w=100, h=5, txt="Item", border=1, align='C', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="IVA", border=1, align='R', fill=0, ln=0)
        pdf.cell(w=10, h=5, txt="Cant", border=1, align='R', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="Neto Dolar", border=1, align='R', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="Bruto pesos", border=1, align='R', fill=0, ln=0)
        #pdf.cell(w=20, h=5, txt="Final", border=1, align='R', fill=0, ln=0)
        pdf.multi_cell(w=0, h=5, txt="Total", border=1, align='R', fill=0)

        pdf.cell(w=0, h=2, txt="", border=0, align='C', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items_presupuesto = self.varPresupuestos.traer_deta_presup(self.pdf_numero_presupuesto)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 8)
        total_presupuesto = 0

        for row in self.items_presupuesto:

            # calculos ----------------------------------------------------------
            bruto_dolar = round((row[7] * float(row[8])) * (1+(float(row[6])/100)), 2)
            sumo_precio_final_conganancia = round((bruto_dolar * float(self.strvar_valor_dolar_hoy.get())) *
                                                  (1+(float(self.pdf_tasa_ganancia)/100)), 2)
            total_presupuesto += sumo_precio_final_conganancia

            # Descripcion item
            pdf.cell(w=100, h=5, txt=row[5], border=0, align='L', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(row[5]), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=10, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(bruto_dolar, 2))), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
            if precios == "S":
                # con precios de componentes
                pdf.multi_cell(w=0, h=5, txt=str(formatear_cifra(row[9])), border=0, align='R', fill=0)
            else:
                # sin precios de componentes
                pdf.multi_cell(w=0, h=5, txt="")
            #pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Impresion del detalle extenso ---------------------------------------------------
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='* Detalle: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_detalle, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        # Total final --------------------------------------------------------------------
        total_presupuesto = formatear_cifra(total_presupuesto)
        total_redondo = formatear_cifra(round(float(self.pdf_total_presup_redondo), 2))
        #pdf.cell(w=0, h=5, txt="Total: " + str(total_presupuesto), border=0, align='R', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt="Total: " + str(total_redondo), border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        try:
            pdf.output('hoja.pdf')
        except:
            messagebox.showinfo("Error", "Verifique listados abiertos en otras terminales", parent=self)
            return

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    def creopdfint(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_tvw_presu_entregado.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_presu_entregado.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # ----------------------------------------------------------------------------------
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

        # Cargo la linea del treeview de resu_presu ---------------------------------------
        valores = self.grid_tvw_presu_entregado.item(self.selected, 'values')

        # # armado de encabezado ------------------------------------------------------------
        # forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'))

        # sdf = datetime.strptime(valores[1], '%Y-%m-%d')
        # fecha_presup = sdf.strftime('%d-%m-%Y')
        fecha_presup = valores[1]
        self.pdf_numero_presupuesto =   valores[0]
        self.pdf_nombre_cliente =       valores[2]
        self.pdf_dolar_presupuesto =    valores[3]
        self.pdf_tasa_ganancia =        valores[4]
        self.pdf_total_presup_redondo = valores[6]

        # Traigo, si es que hay, el detalle extenso del producto presupuestado de la tabla resu_presup
        datos_presu_entregado = self.varPresupuestos.traer_resu_presup(self.pdf_numero_presupuesto)
        self.pdf_detalle = datos_presu_entregado[13]

        # Encabezado
        self.pdf_datos_encabezado_orden = '('+self.pdf_numero_presupuesto+') - '+self.pdf_nombre_cliente
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt='Fecha: ' + fecha_presup + '  -  Numero Presupuesto ' + self.pdf_datos_encabezado_orden,
                 border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.set_font('Arial', '', 7)
        pdf.cell(w=95, h=5, txt="Item", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=10, h=5, txt="IVA", border=1, align='R', fill=0, ln=0)
        pdf.cell(w=5, h=5, txt="Ct", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=10, h=5, txt="BDU", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=17, h=5, txt="BPT", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=17, h=5, txt="Final", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=17, h=5, txt="Ganancia", border=1, align='C', fill=0, ln=0)
        pdf.multi_cell(w=0, h=5, txt="Redondo", border=1, align='R', fill=0)
        #pdf.cell(w=20, h=5, txt="Redondeo", border=1, align='R', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items_presupuesto = self.varPresupuestos.traer_deta_presup(self.pdf_numero_presupuesto)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 7)

        # Sumatoria totales finales
        total_presupuesto = 0
        total_ganancia = 0
        total_costo_dolar = 0
        total_costo_pesos = 0

        for row in self.items_presupuesto:

            # calculos ----------------------------------------------------------

            # costo total bruto en dolar
            # cantidad * precio neto dolar * 1.105 0 1.21
            bruto_dolar = round((row[7] * float(row[8])) * (1+(float(row[6])/100)), 2)
            # sumarizo el costo en dolares bruto c/iva
            total_costo_dolar += bruto_dolar

            # costo total Bruto en pesos c/iva
            # (cantidad * neto_dolar) * dolar_presupuesto * (1+(tasa_iva/100))
            # bruto_pesos = round(((row[6] * float(row[7])) * float(self.pdf_dolar_presupuesto)) * (1+(float(row[5])/100)), 2)
            bruto_pesos = round((bruto_dolar * float(self.pdf_dolar_presupuesto)), 2)
            # sumarizo el costo bruto pesos (c/iva)
            total_costo_pesos += bruto_pesos

            # calculo y sumarizo la ganancia
            item_ganancia = round(bruto_pesos * (float(self.pdf_tasa_ganancia) / 100), 2)
            total_ganancia += item_ganancia

            # costo bruto * (1+(tasa_ganancia/100))
            sumo_precio_final_conganancia = round(bruto_pesos * (1+(float(self.pdf_tasa_ganancia)/100)), 2)
            total_presupuesto += sumo_precio_final_conganancia

            # Descripcion item
            pdf.cell(w=95, h=5, txt=row[5], border=0, align='L', fill=0, ln=0)
            pdf.cell(w=10, h=5, txt=str(row[6]), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=5, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
            #pdf.cell(w=10, h=5, txt=str(formatear_cifra(row[7] * (1+(row[5]/100)))), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=10, h=5, txt=str(formatear_cifra(bruto_dolar)), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=17, h=5, txt=str(formatear_cifra(bruto_pesos)), border=0, align='R', fill=0, ln=0)
            pdf.cell(w=17, h=5, txt=str(formatear_cifra(sumo_precio_final_conganancia)), border=0, align='R', fill=0)
            pdf.cell(w=17, h=5, txt=str(formatear_cifra(item_ganancia)), border=0, align='R', fill=0)
            pdf.multi_cell(w=0, h=5, txt=str(row[9]), border=0, align='R', fill=0)
            #pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # Impresion linea final de totales ------------------------------------------------
        total_ganancia = formatear_cifra(total_ganancia)
        total_costo_dolar = formatear_cifra(total_costo_dolar)
        total_costo_pesos = formatear_cifra(total_costo_pesos)

        pdf.set_font('Courier', 'B', 8)

        pdf.cell(w=0, h=5, txt='* Dolar: '+self.pdf_dolar_presupuesto+' - Total Ganancia: '+str(total_ganancia)+
                               ' Costo Dolar: '+str(total_costo_dolar)+' Costo pesos: '+str(total_costo_pesos),
                                align='L', border=1, fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # Impresion del detalle extenso ---------------------------------------------------
        pdf.set_font('Courier', 'B', 8)
        pdf.cell(w=0, h=5, txt='* Detalle: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 8)
        pdf.multi_cell(w=0, h=5, txt=self.pdf_detalle, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        # Total final --------------------------------------------------------------------
        total_presupuesto = formatear_cifra(round(total_presupuesto, 2))
        total_redondo = formatear_cifra(round(float(self.pdf_total_presup_redondo), 2))
        pdf.cell(w=0, h=5, txt="Total: " + str(total_presupuesto), border=0, align='R', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt="Redondo: " + str(total_redondo), border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        try:
            pdf.output('hoja.pdf')
        except:
            messagebox.showinfo("Error", "Verifique listados abiertos en otras terminales", parent=self)
            return

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)
