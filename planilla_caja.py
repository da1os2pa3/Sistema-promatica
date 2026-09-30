import random
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk

from PIL import Image, ImageTk
from tktooltip import ToolTip

from funcion_new import ClaseFuncionNew
from funciones import *
from planilla_caja_ABM import DatosPlanilla
from status_bar import StatusBar


class ClasePlaniCaja(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()
        self.status = StatusBar(self.master)

        # ---------------------------------------------------------------------------------
        """ Creo una instancia de la clase en _ABM que le corresponde. Le paso la pantalla para poder usar los parent 
        en los messagebox. A varFuncion_new, le paso tambien la pantalla por el mismo motivo y ademas debo pasarle 
        la variable instanciada con el _ABM, de esa manera tambien le paso a funcion la instanciacion de clase del 
        _ABM y asi puede usar los metods que estan en el _ABM """

        # Instanciaciones
        self.varPlanilla = DatosPlanilla(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # PANTALLA
        # ---------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # master.geometry("880x510")
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 660
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        """ PROCEDIMIENTO PARA QUE QUEDE MOSTRANDO LA ULTIMA PLANILLA CARGADA - Obtengo la fecha de la ultima 
        planilla cargada y la filtro  (viene  como date asi YYY-mm-dd). Aca defino por primera vez filtro_activo.
        self.filtro_activo =  'planicaja WHERE CAST(pl_fecha AS date) = CAST('" + self.ultima_fecha + "' AS date)' """

        self.obtener_fecha_inicial()
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # Bloque de inicializacion
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")
        # ------------------------------------------------------------------------------

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_planilla.identify_row(0)
        # self.grid_planilla.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_planilla.focus(item)

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        Otras funciones para manejar los elementos seleccionados incluyen:
        selection_add(): añade elementos a la selección.
        selection_remove(): remueve elementos de la selección.
        selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        selection_toggle(): cambia la selección de un elemento. """

    # ---------------------------------------------------------------------------
    #  WIDGETS
    # ---------------------------------------------------------------------------

    def create_widgets(self):

        # ---------------------------------------------------------------------------------
        # TITULOS
        # ---------------------------------------------------------------------------------
        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = tk.Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('planilla.png')
        self.photo3 = self.photo3.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ventas = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_ventas = tk.Label(self.frame_titulo_top, image=self.png_ventas, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=52, text="Planilla de Caja", bg="black", fg="gold",
                                   font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ventas.grid(row=0, column=0, sticky=tk.W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # VARIABLES GENERALES
        # ---------------------------------------------------------------------------------
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------------------
        self.sv_valor_dolar_hoy = tk.StringVar(value="0.00")

        self.traer_dolarhoy()

        # la obtengo en el metodo -obtener_fecha_inicial-
        self.sv_fecha_planilla = tk.StringVar(value=self.fecha_aux)
        # esta fecha es para recuperar la fecha que estaba activa antes de cometer algun error
        # de ingreso de fecha (en blanco, etc), y asi poder recuperar la anterior que se estaba trabajando
        self.sv_fecha_error = tk.StringVar(value=self.fecha_aux)

        self.sv_tipomov = tk.StringVar(value="")
        self.sv_detalle_movim = tk.StringVar(value="")
        self.sv_cliente = tk.StringVar(value="")
        self.sv_codcli = tk.StringVar(value="0")
        self.sv_proved = tk.StringVar(value="")
        self.sv_forma_pago = tk.StringVar(value="")
        self.sv_detalle_pago = tk.StringVar(value="")
        self.sv_garantia = tk.StringVar(value="")
        self.sv_observaciones = tk.StringVar(value="")

        self.sv_buscostring = tk.StringVar(value="")

        self.sv_ingreso = tk.StringVar(value="0.00")
        self.sv_costo = tk.StringVar(value="0.00")
        self.sv_egreso = tk.StringVar(value="0.00")
        self.sv_cantidad = tk.StringVar(value="1.00")
        self.sv_pagos_ctacte = tk.StringVar(value="0.00")
        self.sv_compras = tk.StringVar(value="0.00")

        # totales que surgen de multiplicar por la cantidad
        self.sv_totingresos = tk.StringVar(value="0.00")
        self.sv_totcosto = tk.StringVar(value="0.00")
        self.sv_total_egresos = tk.StringVar(value="0.00")

        # totales de pie de pantalla
        self.sv_total_ingresos = tk.StringVar(value="0.00")
        self.sv_total_costos = tk.StringVar(value="0.00")
        self.sv_total_utilidad = tk.StringVar(value="0.00")
        self.sv_total_pagos = tk.StringVar(value="0.00")
        self.sv_total_compras = tk.StringVar(value="0.00")
        self.sv_total_util_menos_egr = tk.StringVar(value="0.00")
        self.sv_total_limpio_artic = tk.StringVar(value="0.00")
        self.sv_total_limpio_serv = tk.StringVar(value="0.00")

        # del checkbox
        self.sv_check1 = tk.StringVar(value="0")

        # para mostrar datos del articulo
        self.sv_marca_mostrar = tk.StringVar(value="")
        self.sv_rubro_mostrar = tk.StringVar(value="")
        self.sv_precio_mostrar = tk.StringVar(value="0.00")

        # para datos en tabla cuenta corriente
        self.sv_clavemov = tk.StringVar(value="0")
        self.sv_clavemov_ant = tk.StringVar(value="0")
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # TREEVIEW - GRID
        # ---------------------------------------------------------------------------------
        self.frame_tvw_planilla = tk.LabelFrame(self.master, text="Movimientos", foreground="#CF09BD")
        self.cuadro_grid_planilla()
        self.frame_tvw_planilla.pack(side="top", fill="both", padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # BUSCAR UN MOVIMIENTO
        # ---------------------------------------------------------------------------------
        self.frame_buscar_movimiento = tk.LabelFrame(self.master, text="", foreground="red")
        self.buscar_movimientos()
        self.frame_buscar_movimiento.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------
        # BOTONES
        # ---------------------------------------------------------------------------------
        self.frame_botones_grid = tk.LabelFrame(self.master, text="", foreground="red")
        self.botones_grid()
        self.frame_botones_grid.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # ---------------------------------------------------------------------------------
        # ENTRYS
        # ---------------------------------------------------------------------------------
        # DATOS GENERALES DEL MOVIMIENTO
        self.frame_entrys_planilla = tk.LabelFrame(self.master, text="", foreground="red")
        self.entrys_generales()
        self.frame_entrys_planilla.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # DETALLE DE MOVIMIENTOS
        self.frame_entrys_planilla2 = tk.LabelFrame(self.master, text="", foreground="red")
        self.entrys_detalle_movimientos()
        self.frame_entrys_planilla2.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # IMPORTES DEL MOVIMIENTO
        self.frame_entrys_planilla3 = tk.LabelFrame(self.master, text="", foreground="red")
        self.entrys_importes_del_movimiento()
        self.frame_entrys_planilla3.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # COMBOS FORMA DE PAGO
        self.frame_entrys_planilla4 = tk.LabelFrame(self.master, text="", foreground="red")
        self.entrys_combo_forma_pago()
        self.frame_entrys_planilla4.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ENTRY GARANTIAS
        self.frame_entrys_planilla5 = tk.LabelFrame(self.master, text="", foreground="red")
        self.entrys_garantias()
        self.frame_entrys_planilla5.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # ---------------------------------------------------------------------------------
        # TOTALES MOVIMIENTOS DE PLANILLA
        # ---------------------------------------------------------------------------------
        self.frame_totales = tk.LabelFrame(self.master, text="", foreground="red")
        self.calculo_totales()
        self.frame_totales.pack(side="top", fill="both", expand=0, padx=5, pady=2)

    # ---------------------------------------------------------------------------------
    # GRID
    # ---------------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        # Limpieza grid
        for item in self.grid_planilla.get_children():
            self.grid_planilla.delete(item)

        # Controles grid
        if len(self.filtro_activo) > 0:
            datos = self.varPlanilla.consultar_planilla(self.filtro_activo)
        else:
            datos = self.varPlanilla.consultar_planilla("ORDER BY pl_fecha ASC")

        # acumuladores
        acum_ingresos_ventas = 0
        acum_costos_ventas = 0
        acum_egresos = 0
        acum_pagos_ctacte = 0
        acum_compras = 0
        acum_utilidad = 0
        acum_util_egre = 0
        acum_neto_articulos = 0
        acum_neto_servicios = 0

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'), False)

            # cargo la grilla
            self.grid_planilla.insert("", "end", tags=color, text=row[0], values=(forma_normal, row[2],
                                                            row[3], row[4], row[5], round((row[4] * row[5]), 2),
                                                            row[6], row[7], row[8], row[9], row[10], row[11], row[12],
                                                            row[13], row[14], row[15], row[16], row[17], row[18]))

            # Simplifico calculos -------------------------------------------------------
            importe_venta = row[5] * row[4]
            importe_costo = row[7] * row[4]

            # Sumarizo los campos de importes totales por planilla ----------------------
            acum_ingresos_ventas += importe_venta
            acum_costos_ventas += importe_costo
            acum_utilidad += importe_venta - importe_costo
            acum_egresos += row[6]
            acum_pagos_ctacte += row[8]
            acum_compras += row[9]
            acum_util_egre += importe_venta - importe_costo - row[6]

            if row[2] == "Venta_articulos":
                acum_neto_articulos += importe_venta - importe_costo
            elif row[2] == "Venta_servicios":
                acum_neto_servicios += importe_venta - importe_costo

        # Totales planilla -------------------------------------------------------------
        self.sv_total_ingresos.set(value=str(round(acum_ingresos_ventas, 2)))
        self.sv_total_costos.set(value=str(round(acum_costos_ventas, 2)))
        self.sv_total_utilidad.set(value=str(round(acum_utilidad, 2)))
        self.sv_total_egresos.set(value=str(round(acum_egresos, 2)))
        self.sv_total_pagos.set(value=str(round(acum_pagos_ctacte, 2)))
        self.sv_total_compras.set(value=str(round(acum_compras, 2)))
        self.sv_total_util_menos_egr.set(value=str(round(acum_util_egre, 2)))
        self.sv_total_limpio_artic.set(value=str(round(acum_neto_articulos, 2)))
        self.sv_total_limpio_serv.set(value=str(round(acum_neto_servicios, 2)))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_planilla.get_children()
        # Si no hay filas (grid vacio), salgo sin intentar seleccionar
        if not children:
            self.status.set_status("ℹ Grid vacio...", "info")
            return

        # Si el parametro set_foco esta vacío (no hay foco), voy al ultimo de la grilla,
        # caso contrario, voy a la clave que se haya enviado en set_foco para dejar el puntero.
        if not set_foco:
            # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
            posicion = children[-1]       # ultimo
            # posicion = children[0]      # primero
            self.grid_planilla.focus_set()
            self.grid_planilla.focus(posicion)
            self.grid_planilla.selection_set(posicion)
            self.grid_planilla.see(posicion)
        else:
            for item in children:
                texto = self.grid_planilla.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_planilla.update_idletasks()
                    self.grid_planilla.focus_set()
                    self.grid_planilla.selection_set(item)
                    self.grid_planilla.focus(item)
                    self.grid_planilla.see(item)
                    break

    def filtrar_grilla(self, fecha_filtrar):

        # tiene que venir en str formato(05/06/2024) por ejemplo la paso a DATE en formato dd/mm/YYYY
        paso_a_date = datetime.strptime(fecha_filtrar, "%d/%m/%Y")
        # la paso a STR formato YYYY-mm-dd - este formato es el que acepta el filtro en el CAST
        fecha1 = datetime.strftime(paso_a_date, "%Y-%m-%d")

        self.filtro_activo = "WHERE CAST(pl_fecha AS date) = CAST('" + fecha1 + "' AS date)"
        self.llena_grilla("")

    # ---------------------------------------------------------------------------------
    # ESTADOS
    # ---------------------------------------------------------------------------------

    def fcancelar(self):
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return
        self.reset_stringvars()
        self.estado_inicial()
        self.habilitar_text()
        self.btn_nuevoitem.focus()

    def freset(self):
        r = messagebox.askquestion("Reset", "Confirma -reset- operacion actual?", parent=self)
        if r == messagebox.NO:
            return
        self.reset_stringvars()
        self.estado_inicial()
        self.obtener_fecha_inicial()
        # coloco en la variable fecha de planilla la fecha de la ultima planilla cargada
        self.sv_fecha_planilla.set(value=self.fecha_aux)
        self.llena_grilla("")
        self.habilitar_text()
        self.btn_nuevoitem.focus()

    def estado_inicial(self):
        self.habilitar_text()
        self.alta_modif = 0
        self.retorno = ""

    def habilitar_text(self):

        # Widgets a habilitar
        habilitar = [
            self.entry_buscar_movim,
            self.btn_buscar_movim,
            self.btn_mostrar_todo,
            self.btn_nuevoitem,
            self.btn_editaitem,
            self.btn_borraitem,
            self.btn_Cancelar,
            self.btn_Resumen,
            self.btnToparch,
            self.btnFinarch,
            self.entry_fecha_planilla,
            self.btnDerecha,
            self.btnIzquierda
        ]

        # Widgets a deshabilitar
        deshabilitar = [
            self.btn_guardaritem,
            self.combo_tipomov,
            self.entry_cliente,
            self.entry_detalle_movim,
            self.entry_ingresos,
            self.entry_cantidad,
            self.entry_costo,
            self.entry_egreso,
            self.entry_pagoscta,
            self.entry_compras,
            self.entry_proved,
            self.combo_forma_pago,
            self.entry_detalle_pago,
            self.entry_garantia,
            self.entry_observaciones,
            self.btn_bus_art,
            self.btn_bus_prov,
            self.btn_bus_cli
        ]

        # Aplicar estados
        for w in habilitar:
            w.configure(state="normal")

        for w in deshabilitar:
            w.configure(state="disabled")

        # Configuración especial
        self.grid_planilla['selectmode'] = 'browse'
        self.grid_planilla.bind("<Double-Button-1>", self.doble_click_grid_pla)

    def estado_boton_nuevo(self):

        # 1 - Desactivo los botones Nuevo - Editar - Eliminar - Resumen mes
        self.btn_nuevoitem.configure(state="disabled")
        self.btn_editaitem.configure(state="disabled")
        self.btn_borraitem.configure(state="disabled")
        self.btn_Resumen.configure(state="disabled")

        # Habilitar boton -Guardar-
        self.btn_guardaritem.configure(state="normal")

        # Desactivar Entry buscar - Boton Buscar - boton - Mostrar all-
        self.entry_buscar_movim.configure(state="disabled")
        self.btn_buscar_movim.configure(state="disabled")
        self.btn_mostrar_todo.configure(state="disabled")

        # Activar Entrys y combos
        self.combo_tipomov.configure(state="normal")

        self.btn_bus_cli.configure(state="normal")
        self.btn_bus_art.configure(state="normal")
        self.btn_bus_prov.configure(state="normal")
        self.entry_cliente.configure(state="normal")
        self.entry_detalle_movim.configure(state="normal")
        self.entry_proved.configure(state="normal")

        # Importes - cantidades - formas de pago - garantia y observaciones
        self.entry_cantidad.configure(state="normal")
        self.entry_ingresos.configure(state="normal")
        self.entry_costo.configure(state="normal")
        self.entry_egreso.configure(state="normal")
        self.entry_pagoscta.configure(state="normal")
        self.entry_compras.configure(state="normal")
        self.entry_detalle_pago.configure(state="normal")
        self.combo_forma_pago.configure(state="normal")
        self.entry_garantia.configure(state="normal")
        self.entry_observaciones.configure(state="normal")

        self.check_ctacte.configure(state="normal")

        self.divido_tipomov()

    # ---------------------------------------------------------
    # Grupo de funciones combinadas
    # ---------------------------------------------------------

    # Auxiliar usada por divido_tipomov
    @staticmethod
    def set_state(state, *widgets):
        for w in widgets:
            w.configure(state=state)

    # Auxiliar usada por divido_tipomov
    @staticmethod
    def reset_vars(*vars):
        for var in vars:
            var.set("0.00")

    def divido_tipomov(self):

        # Habilito todo primero
        self.set_state("normal",
                       self.entry_egreso,
                       self.entry_compras,
                       self.entry_ingresos,
                       self.entry_pagoscta,
                       self.entry_costo,
                       self.entry_cantidad,
                       self.entry_proved,
                       self.entry_cliente)
        self.check_ctacte.configure(onvalue=1, state="normal")

        tipo = self.combo_tipomov.get()

        match tipo:

            case "Venta_articulos" | "Venta_servicios" | "Ingresos_varios":

                self.reset_vars(self.sv_egreso, self.sv_compras)
                self.sv_proved.set("")
                self.set_state("disabled",
                               self.entry_egreso,
                               self.entry_compras,
                               self.entry_proved)

            case "Pagos_ctacte":

                self.reset_vars(self.sv_compras, self.sv_totingresos)
                self.sv_proved.set("")
                self.set_state("disabled",
                               self.entry_compras,
                               self.entry_proved)

            case "Compras":

                self.reset_vars(
                    self.sv_ingreso,
                    self.sv_pagos_ctacte,
                    self.sv_costo,
                    self.sv_egreso,
                    self.sv_totingresos)

                self.sv_cantidad.set("1.00")

                self.set_state("disabled",
                               self.entry_ingresos,
                               self.entry_pagoscta,
                               self.entry_costo,
                               self.entry_cantidad,
                               self.entry_egreso)

                self.check_ctacte.configure(state="disabled")
                self.btn_bus_prov.configure(state="normal")

            case "Egresos_varios":

                self.reset_vars(
                    self.sv_ingreso,
                    self.sv_costo,
                    self.sv_compras,
                    self.sv_totingresos)

                self.sv_cantidad.set("1.00")

                self.set_state("disabled",
                               self.entry_ingresos,
                               self.entry_costo,
                               self.entry_compras,
                               self.entry_cantidad)
            case _:
                pass

    # ---------------------------------------------------------
    # FIN Grupo de funciones combinadas
    # ---------------------------------------------------------

    def estado_resumen(self):

        # 0 - Desactivar Browse
        self.grid_planilla['selectmode'] = 'none'
        self.grid_planilla.bind("<Double-Button-1>", self.fno_modifique)

        # 1 - "Entry busqueda" y botones "Buscar" y "Mostrar all" =>activos
        self.entry_buscar_movim.configure(state="disabled")
        self.btn_buscar_movim.configure(state="disabled")
        self.btn_mostrar_todo.configure(state="disabled")

        # 2 - Botones "Nuevo" "Editar" "Eliminar" activos
        self.btn_nuevoitem.configure(state="disabled")
        self.btn_editaitem.configure(state="disabled")
        self.btn_borraitem.configure(state="disabled")

        # 3 - Guardar  => disabled
        self.btn_guardaritem.configure(state="disabled")

        # 4 - Cancelar - Reset - Resumen del mes - TOP - END
        self.btn_Cancelar.configure(state="disabled")
        self.btn_Resumen.configure(state="normal")
        self.btnToparch.configure(state="normal")
        self.btnFinarch.configure(state="normal")

        # 5 - Entrys
        self.entry_fecha_planilla.configure(state="normal")
        self.combo_tipomov.configure(state="disabled")
        self.entry_cliente.configure(state="disabled")
        self.entry_detalle_movim.configure(state="disabled")
        self.entry_ingresos.configure(state="disabled")
        self.entry_costo.configure(state="disabled")
        self.entry_cantidad.configure(state="disabled")

        self.entry_egreso.configure(state="disabled")
        self.entry_pagoscta.configure(state="disabled")
        self.entry_compras.configure(state="disabled")
        self.entry_proved.configure(state="disabled")
        self.entry_ingresos.configure(state="disabled")
        self.combo_forma_pago.configure(state="disabled")
        self.entry_detalle_pago.configure(state="disabled")
        self.entry_garantia.configure(state="disabled")
        self.entry_observaciones.configure(state="disabled")

        self.btnDerecha.configure(state="disabled")
        self.btnIzquierda.configure(state="disabled")
        self.btn_bus_art.configure(state="disabled")
        self.btn_bus_prov.configure(state="disabled")
        self.btn_bus_cli.configure(state="disabled")

    @staticmethod
    def fno_modifique(_event):
        return "break"

    def reset_stringvars(self):

        self.sv_tipomov.set(value="")
        self.combo_tipomov.current(0)
        self.sv_detalle_movim.set(value="")
        self.sv_proved.set(value="")
        self.sv_cliente.set(value="")
        self.sv_codcli.set(value="0")
        self.sv_forma_pago.set(value="")
        self.combo_forma_pago.current(0)
        self.sv_detalle_pago.set(value="")
        self.sv_garantia.set(value="")
        self.sv_observaciones.set(value="")

        self.sv_ingreso.set(value="0.00")
        self.sv_costo.set(value="0.00")
        self.sv_egreso.set(value="0.00")
        self.sv_cantidad.set(value="1.00")
        self.sv_compras.set(value="0.00")
        self.sv_totingresos.set(value="0.00")
        self.sv_totcosto.set(value="0.00")
        self.sv_pagos_ctacte.set(value="0.00")

        self.sv_check1.set(value="0")

    # ----------------------------------------------------------------------
    # CRUD
    # ----------------------------------------------------------------------

    def fnuevoitem(self):

        self.alta_modif = 1
        self.grid_planilla.bind("<Double-Button-1>", self.fno_modifique)
        self.grid_planilla['selectmode'] = 'none'
        self.estado_boton_nuevo()
        self.entry_fecha_planilla.focus_set()

    def feditaitem(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_planilla.focus()
        # Asi obtengo la clave de la Tabla campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta)
        self.clave = self.grid_planilla.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        self.estado_boton_nuevo()

        """ Traigo los valores directamente de la Tabla, para no cargar tanto de columnas el Grid.
        Tener en cuenta que solo traigo un registro (el que necesito)"""

        valores = self.varPlanilla.consultar_planilla("WHERE Id = " + str(self.clave))

        """ Esto ya no lo hago, traigo directamente de la tabla
        En la lista valores cargo el registro completo con todos los campos desde el Grid
        valores = self.grid_planilla.item(self.selected, 'values') """

        self.reset_stringvars()

        for row in valores:  # Como viene un solo registro, esto NO deberia hacerlo

            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[1], "%Y-%m-%d"), False)
            self.sv_fecha_planilla.set(value=fecha_convertida)
            self.sv_tipomov.set(value=row[2])
            self.sv_detalle_movim.set(value=row[3])
            self.sv_cantidad.set(value=row[4])
            self.sv_ingreso.set(value=row[5])
            self.sv_egreso.set(value=row[6])
            self.sv_costo.set(value=row[7])
            self.sv_pagos_ctacte.set(value=row[8])
            self.sv_compras.set(value=row[9])
            self.sv_cliente.set(value=row[10])
            self.sv_codcli.set(value=row[18])
            self.sv_forma_pago.set(value=row[11])
            self.sv_detalle_pago.set(value=row[12])
            self.sv_garantia.set(value=row[13])
            self.sv_observaciones.set(value=row[14])
            self.sv_proved.set(value=row[15])
            self.sv_check1.set(value=row[16])
            self.sv_clavemov_ant.set(value=row[17])

        self.estado_boton_nuevo()

        self.calcular("general")
        self.entry_cliente.focus()

    def fborraitem(self):

        # -----------------------------------------------------------
        """ Guardo en self.selected, el Id del item del grid o treeview (I010, IB14.... """
        self.selected = self.grid_planilla.focus()
        self.selected_ant = self.grid_planilla.prev(self.selected)
        """ Guardo en self.clave, el Id del treeview de la primer columna (12 . 23 . 25.....) """
        self.clave = self.grid_planilla.item(self.selected, 'text')
        self.clave_ant = self.grid_planilla.item(self.selected_ant, 'text')
        # -----------------------------------------------------------

        if self.clave == "" or self.selected == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_planilla.item(self.selected, 'values')

        # guardo clave de movimiento anterior para control de cuenta corriente
        self.clavemov_ant = valores[17]
        # data es para mostrar el movimiento que voy a borrar

        data = str(self.clave) + " " + valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            self.status.set_status("ℹ Cancelado...", "info")
            self.clavemov_ant = 0
            return

        # Elimino de tabla planicaja y opcionalmente de cuenta corriente
        n = self.varPlanilla.eliminar_item_planilla(self.clave)
        if n == 1:

            # Elimino de tabla ctacte si existe clave de movimiento
            if int(self.clavemov_ant) > 0:
                # Aqui lo elimino de la tabla de ctacte
                self.varPlanilla.eliminar_item_ctacte_xmodif(self.clavemov_ant)
                # messagebox.showinfo("Eliminar", "Registro eliminado EN PLANILLA Y CUENTA CORRIENTE", parent=self)
                self.status.set_status("🗑 Registro eliminado EN PLANILLA Y CUENTA CORRIENTE", "ok")
            else:
                # messagebox.showinfo("Eliminar", "Registro eliminado en PLANILLA", parent=self)
                self.status.set_status("🗑 Registro eliminado solo EN PLANILLA", "ok")

            self.llena_grilla(self.clave_ant)

        else:  # nunca puede pasar, pero por las dudas pongo mensaje

            messagebox.showinfo("Eliminar", "Hubo un error en [Eliminar item planilla de ABM] Revise el "
                                            "movimiento por favor", parent=self)

        self.clavemov_ant = 0

    def fguardar(self):

        # VALIDACIONES PREVIAS --------------------------------------------------
        # FECHA
        if not self.sv_fecha_planilla.get():
            self.status.set_status("⚠ La fecha es requerida", "warn")
            self.fecha_blanco = date.today().strftime('%d/%m/%Y')
            self.sv_fecha_planilla.set(value=self.fecha_blanco)
            self.entry_fecha_planilla.focus()
            return
        # DETALLE
        if self.sv_detalle_movim.get() == "":
            self.status.set_status("⚠ Agregue un detalle", "warn")
            self.entry_detalle_movim.focus()
            return

        # Defino variables para simplificar calculos ----------------------------
        ingreso = float(self.sv_ingreso.get() or 0)
        cantidad = float(self.sv_cantidad.get() or 0)
        egreso = float(self.sv_egreso.get() or 0)
        compras = float(self.sv_compras.get() or 0)
        pagos = float(self.sv_pagos_ctacte.get() or 0)

        # Validaciones campos numericos segun el tipo de movimiento -------------

        tipo = self.combo_tipomov.get()

        if tipo in ("Venta_articulos", "Venta_servicios", "Ingresos_varios"):

            # debe haber un valor en ingreso , puede haber pagos a ctacte , no puede haber egreso ni compras
            if self.validar_campos(ingreso == 0, "Importe de ingreso en cero", self.entry_ingresos): return
            # debe haber una cantidad
            if self.validar_campos(cantidad == 0, "Coloque cantidad", self.entry_cantidad): return
            # no debe haber importe de egreso
            if self.validar_campos(egreso != 0, "No puede haber egreso", self.entry_egreso): return
            # # no debe haber importe de compras
            if self.validar_campos(compras != 0, "No puede haber compras", self.entry_compras): return

        elif tipo == "Compras":  # Es un valor de egreso

            #  # SI debe haber importe de compra
            if self.validar_campos(compras == 0, "Importe de compras en cero", self.entry_compras): return
            # NO puede haber importe de ingreso
            if self.validar_campos(ingreso != 0, "No puede haber ingreso", self.entry_ingresos): return
            # NO puede haber imoprte en pagos a ctacte
            if self.validar_campos(pagos != 0, "No puede haber pagos ctacte", self.entry_pagoscta): return
            # NO puede haber importe de agreso
            if self.validar_campos(egreso != 0, "No puede haber egreso", self.entry_egreso): return

        elif tipo == "Egresos_varios":  # Es un valor de egreso

            # SI debe haber importe de egreso
            if self.validar_campos(egreso == 0, "Importe de egresos en cero", self.entry_egreso): return
            # NO puede haber importe de ingreso
            if self.validar_campos(ingreso != 0, "No puede haber ingreso", self.entry_ingresos): return
            # NO puede haber importe de compra
            if self.validar_campos(compras != 0, "No puede haber compras", self.entry_compras): return

        # ----------------------------------------------------------------------------
        # guardo el Id del Grid en selected para ubicacion del foco a posteriori I001, IB003
        self.selected = self.grid_planilla.focus()
        # Guardo el Id del registro de la Tabla (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_planilla.item(self.selected, 'text')

        if self.clave == "":
            pass
            # ver aca , porque sef.clave en el caso de que modifique la fecha (por una sin movimientos) y haga un Tab, el
            # Grid se me pone en blanco porque pasa a filtrarse con una fecha sin movimientosy dejo de tener el valor "text"
            # print("la clave es blanco, seguro no entran las modificaciones o es un ALTA")

        # ----------------------------------------------------------------------------

        # Identifica movimiento a cuenta corriente - debe ser cero si es un alta de nuevo movimiento
        self.sv_clavemov.set(value="0")
        self.movim_a_cta = 'N'

        # ALTA ===============================================================================
        if self.alta_modif == 1:

            # Si pagos a cuenta cte es "" le meto un "0" por las dudas
            if self.sv_pagos_ctacte.get() == "":
                self.sv_pagos_ctacte.set(value="0")

            self.movim_a_cta = 'S' if (self.sv_check1.get() == "1" or float(self.sv_pagos_ctacte.get()) != 0) else 'N'

            if self.movim_a_cta == 'S':

                # CODIGO CLIENTE
                if not float(self.sv_codcli.get()):
                    messagebox.showerror("Error", "Cuenta corriente debe tener codigo cliente - "
                                                  "falta codigo", parent=self)
                    self.entry_cliente.focus()
                    return
                # NOMBRE DE CLIENTE
                if not self.sv_cliente.get():
                    messagebox.showerror("Error", "Cuenta corriente debe tener nombre cliente - "
                                                  "falta nombre", parent=self)
                    self.entry_cliente.focus()
                    return

                # Si la cosa es correcto, genero nueva clave aleatoria para identificar el movimiento en ctacte
                self.sv_clavemov.set(value=str(random.randint(1, 1000000)))

            # Preparo Diccionarios -------------------------------------------------------
            fecha_aux = datetime.strptime(self.sv_fecha_planilla.get(), '%d/%m/%Y')
            planilla = self.get_planilla_dict(fecha_aux)
            data_ctacte = self.get_ctacte_dict(fecha_aux)
            # ----------------------------------------------------------------------------

            # Inserto datos en Planilla --------------------------------------------------
            try:
                self.id_nuevo = self.varPlanilla.insertar_planilla(planilla)
                self.id_ref = self.id_nuevo
            except ValueError as e:
                messagebox.showwarning("Datos inválidos",str(e), parent=self)
                return
            except Exception:
                self.varFuncion_new.mostrar_error()
                return
            # ----------------------------------------------------------------------------

            # 3- Si se ha generado clave de movimiento a cta. y ademas la variable movimiento a cta esta en "S"
            # Corresponde guardar el movimiento en la tabla de ctacte
            if float(self.sv_clavemov.get()) != 0 and self.movim_a_cta == 'S':
                self.varPlanilla.insertar_ctacte(data_ctacte)
                self.status.set_status("✔ Registracion correcta en Planillas y cuenta corriente", "ok")
            else:
                self.status.set_status("✔ Registracion correcta solo Planillas", "ok")

        # MODIFICACION ===================================================================================
        if self.alta_modif == 2:

            # Si pagos a cuenta cte es "" le meto un "0" por las dudas
            if self.sv_pagos_ctacte.get() == "":
                self.sv_pagos_ctacte.set(value="0")

            self.movim_a_cta = 'S' if (self.sv_check1.get() == "1" or float(self.sv_pagos_ctacte.get()) != 0) else 'N'

            if self.movim_a_cta == 'S':

                # Si codigo de cliente es "" le meto un "0" pora luego validar
                if self.sv_codcli.get() == "":
                    self.sv_codcli.set(value="0")

                # Requiero codigo de cliente
                if not float(self.sv_codcli.get() or 0):
                    #messagebox.showerror("Error", "Es necesario codigo de cliente - falta codigo", parent=self)
                    self.status.set_status("ℹ Es necesario codigo de cliente - falta codigo", "info")
                    self.entry_cliente.focus()
                    return
                # Requiero nombre de cliente
                if not self.sv_cliente.get():
                    self.status.set_status("ℹ Es necesario nombre de cliente - falta codigo", "info")
                    # messagebox.showerror("Error", "Es necesario nombre de clientee - falta nombre", parent=self)
                    self.entry_cliente.focus()
                    return

                # genero nueva clave aleatoria ------------------------------------------------
                self.sv_clavemov.set(value=str(random.randint(1, 1000000)))

            # Preparo Diccionarios -------------------------------------------------------------
            fecha_aux = datetime.strptime(self.sv_fecha_planilla.get(), '%d/%m/%Y')
            planilla = self.get_planilla_dict(fecha_aux)
            data_ctacte = self.get_ctacte_dict(fecha_aux)
            # ----------------------------------------------------------------------------------
            # Borrado previo de los movimientos de ctacte - Al ser modificacion, borrar todos los movimientos
            # en tabla de ctacte con clavemov  = sv_clavemov_ant
            if float(self.sv_clavemov_ant.get()) != 0 and self.movim_a_cta == 'S':
                self.varPlanilla.eliminar_item_ctacte_xmodif(self.sv_clavemov_ant.get())
            # ----------------------------------------------------------------------------------

            # Ingreso datos a tabla ------------------------------------------------------------
            try:
                self.varPlanilla.modificar_planilla(planilla)
                self.id_ref = self.clave
            except ValueError as e:
                messagebox.showwarning("Datos inválidos", str(e), parent=self)
                return
            except Exception:
                self.varFuncion_new.mostrar_error()
                return
            # ----------------------------------------------------------------------------------

            # Guardo de movimiento en cta cte si corresponde -----------------------------------
            if float(self.sv_clavemov.get()) != 0 and self.movim_a_cta == 'S':
                # guardo (como ALTA) movimiento modificado en ctacte con clave nueva, porque el que existia
                # anteriormente fue borrado previamente.
                self.varPlanilla.insertar_ctacte(data_ctacte)
                self.status.set_status("✔ Modificacion correcta en Planillas y cuenta corriente", "ok")
            else:
                self.status.set_status("✔ Modificacion correcta solo Planillas", "ok")
            # -----------------------------------------------------------------------------------

        self.movim_a_cta = 'N'
        self.reset_stringvars()
        self.habilitar_text()

        if self.alta_modif == 1:
            # el id nuevo
            self.llena_grilla(self.id_ref)
        elif self.alta_modif == 2:
            # el id existente
            # self.llena_grilla(self.id_ref)
            self.llena_grilla(self.clave)

        self.alta_modif = 0
        self.btn_nuevoitem.focus()

    # ---------------------------------------------------------------------------------
    # VARIAS
    # ---------------------------------------------------------------------------------

    def fsalir(self):
        self.master.destroy()

    def traer_dolarhoy(self):
        dev_informa = self.varPlanilla.consultar_informa()
        for row in dev_informa:
            self.sv_valor_dolar_hoy.set(value=row[21])

    def tildo_cuenta(self, cposa):
        # Pone el checkbox en 1 si es movimiento a cuenta corriente o el valor del campo pago es distinto de cero

        valor = self.sv_pagos_ctacte.get()
        fpago = self.combo_forma_pago.get()

        try:
            monto = float(valor) if valor else 0.0
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)
            self.entry_pagoscta.focus()
            return

        # Seteo checkbox
        self.sv_check1.set("1" if monto != 0 else "0")
        self.sv_check1.set("1" if fpago == "Cuenta Corriente" else "0")

    def obtener_fecha_inicial(self):

        # El parametro 1 trae la primer columna de la tabla (fecha en este caso), ojo la columna 0 es el Id
        self.ultima_fecha = self.varPlanilla.traer_ultimo(1)

        if self.ultima_fecha != 0:
            # Esta funcion la pasa a formato str pero al derecho normal de 2024-12-19 a 19/12/2024 esta en funciones
            self.fecha_aux = fecha_str_reves_normal(self, self.ultima_fecha, False)
        else:
            # paso la fecha de hoy a string y la asigno a ultima fecha porque no hay otra
            self.fecha_aux = date.today().strftime('%d/%m/%Y')
            self.ultima_fecha = self.fecha_aux

        """ En este filtro pongo la fecha que viene de la tabla, la cual viene con el formato (YYYY-mm-dd) y las 
        instrucciones SQL que utilizo en el filtro solo aceptan la fecha con este formato """

        self.filtro_activo = "WHERE CAST(pl_fecha AS date) = CAST('" + self.ultima_fecha + "' AS date)"

    # ---------------------------------------------------------------------------------
    # BUSQUEDAS
    # ---------------------------------------------------------------------------------

    def fbuscar_en_tabla(self):

        texto = self.sv_buscostring.get().strip()

        if not texto:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        # Sanitizar básico (evitar romper SQL) por si viene un nombre O''connor jode las comillas
        texto = texto.replace("'", "''")

        self.filtro_anterior = self.filtro_activo

        # Hago una lista con las cuatro condiciones
        campos = ["pl_detalle", "pl_cliente", "pl_proved", "pl_tipopago"]
        # esto lo hace para cada campo - muy buena instruccion
        condiciones = [f"INSTR({campo}, '{texto}') > 0" for campo in campos]

        # unir las condiciones
        self.filtro_activo = "WHERE " + " OR ".join(condiciones)

        self.varPlanilla.buscar_entabla(self.filtro_activo)
        self.llena_grilla("")

        # Mantener foco
        items = self.grid_planilla.selection()
        if items:
            self.grid_planilla.focus(items[0])

    def fshowall(self):
        self.selected = self.grid_planilla.focus()
        self.clave = self.grid_planilla.item(self.selected, 'text')
        self.filtrar_grilla(self.sv_fecha_planilla.get())
        self.llena_grilla(self.clave)

    # ---------------------------------------------------------------------------------
    # CALCULOS
    # ---------------------------------------------------------------------------------

    def fresumen(self):

        # debo tomar mes y año para realizar el filtrado de la fecha actual
        mes_filtro = str(datetime.strptime(self.sv_fecha_planilla.get(), "%d/%m/%Y").month)
        ano_filtro = str(datetime.strptime(self.sv_fecha_planilla.get(), "%d/%m/%Y").year)

        self.filtro_activo = ("WHERE MONTH(pl_fecha) = '" + mes_filtro + "' AND YEAR(pl_fecha) = '"
                              + ano_filtro + "' ORDER BY pl_fecha")

        self.llena_grilla("")

        self.estado_resumen()

    def calcular(self, que_campo):

        # --- CORRECCIÓN de 2do nivel: forzar formato válido en todos los entrys
        # variables no entry.. calculadas
        self.varFuncion_new.corregir_valor(self.sv_ingreso.get())
        self.varFuncion_new.corregir_valor(self.sv_costo.get())
        self.varFuncion_new.corregir_valor(self.sv_cantidad.get())
        self.varFuncion_new.corregir_valor(self.sv_egreso.get())
        self.varFuncion_new.corregir_valor(self.sv_pagos_ctacte.get())
        self.varFuncion_new.corregir_valor(self.sv_compras.get())
        # ---------------------------------------------------------------------------------

        try:
            # Controla allsobre los "-" y "."
            self.control_valores()

            # Evaluo segun el parametro de calculo que asigno en el Entry
            if que_campo == "general":
                x_ingreso = float(self.sv_ingreso.get())
                x_costo = float(self.sv_costo.get())
                x_cantidad = float(self.sv_cantidad.get())

                self.sv_totingresos.set(value=str(round(x_ingreso * x_cantidad, 2)))
                self.sv_totcosto.set(value=str(round(x_costo * x_cantidad, 2)))
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)
            self.entry_detalle_movim.focus()
            return

    def control_valores(self):

        """ Controla los valores en blanco o cero y los pone con dos decimales automaticamente"""

        variables = [
            self.sv_ingreso,
            self.sv_costo,
            self.sv_cantidad,
            self.sv_egreso,
            self.sv_pagos_ctacte,
            self.sv_compras
        ]

        for var in variables:
            self.formatear_sv(var)

    @staticmethod
    def formatear_sv(var):
        try:
            var.set(f"{float(var.get()):.2f}")
        except ValueError:
            var.set("0.00")


    # ---------------------------------------------------------------------------------
    # SEL
    # ---------------------------------------------------------------------------------

    def fbuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en que
        campos debe hacerse """

        texto = self.sv_cliente.get()
        que_busco = (
            f"clientes WHERE INSTR(apellido, '{texto}') > 0 "
            f"OR INSTR(nombres, '{texto}') > 0 "
            f"OR INSTR(apenombre, '{texto}') > 0 "
            f"ORDER BY apenombre"
        )

        """ Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de 
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec(
            "clientes",
            "apenombre",
            "codigo",
            "direccion",
            "Apellido y nombre",
            "Codigo",
            "Direccion",
            que_busco,
            "Orden: Alfabetico cliente", "N"
        )

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes. """

        for item in valores_new:
            self.sv_cliente.set(value=item[15])
            self.sv_codcli.set(value=item[1])

        self.entry_cliente.focus()
        self.entry_cliente.icursor(tk.END)

    def fbusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        texto = self.sv_detalle_movim.get().strip().replace("'", "''")

        campos = ["descripcion", "marca", "rubro", "codbar", "codigo"]
        condiciones = [f"INSTR({campo}, '{texto}') > 0" for campo in campos]

        que_busco = (
                "articulos WHERE "
                + " OR ".join(condiciones)
                + " ORDER BY rubro, marca, descripcion"
        )

        valores_new = self.varFuncion_new.ventana_selec(
            "articulos",
            "descripcion",
            "marca",
            "costodolar",
            "Descripcion",
            "Marca",
            "Precio dolar neto",
            que_busco,
            "Orden: Rubro+Marca+Descripcion",
            "S"
        )

        masiva = 0
        masganancia = 0

        for item in valores_new:
            self.sv_detalle_movim.set(value=item[2])  # descripcion del articulo

            costopesos_neto = round((float(self.sv_valor_dolar_hoy.get()) * float(item[6])), 2)
            masiva = round((float(costopesos_neto) * (1 + (float(item[7]) / 100))), 2)
            masganancia = round((float(masiva) * (1 + (float(item[9]) / 100))), 2)

        self.sv_ingreso.set(value=str(masganancia))
        self.sv_costo.set(value=str(masiva))

        self.entry_detalle_movim.focus()
        self.entry_detalle_movim.icursor(tk.END)

    def fbusprov(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en
        que campos debe hacerse """

        texto = self.sv_proved.get().strip().replace("'", "''")
        campos = ["denominacion", "direccion"]
        condiciones = [f"INSTR({campo}, '{texto}') > 0" for campo in campos]
        que_busco = (
                "proved WHERE "
                + " OR ".join(condiciones)
                + " ORDER BY denominacion"
        )

        """  Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de 
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec(
            "proved",
            "denominacion",
            "codigo",
            "direccion",
            "Nombre Empresa",
            "Codigo",
            "Direccion",
            que_busco,
            "Orden: Nombre de Proveedor",
            "N"
        )

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:
            self.sv_proved.set(value=item[2])
            # self.sv_codcli.set(value=item[1])

        self.entry_proved.focus()
        self.entry_proved.icursor(tk.END)

    def doble_click_grid_pla(self, _event):
        self.feditaitem()

    def fver_blanco(self):
        print("popopoppopo")
        self.sv_fecha_error.set(value=self.sv_fecha_planilla.get())

    def fantes(self):

        # Controlo que la fecha no este vacia
        if self.sv_fecha_planilla.get() == "":
            messagebox.showerror("Error", "La fecha es requerida", parent=self)
            self.sv_fecha_planilla.set(value=self.sv_fecha_error.get())
            self.entry_fecha_planilla.focus()
            return

        # primero paso la fecha a formato date
        paso_a_date = datetime.strptime(self.sv_fecha_planilla.get(), "%d/%m/%Y")
        # le resto uno con timedelta - deben estar en formato date
        resto_a_date = paso_a_date - timedelta(days=1)
        # y ahora la paso a string
        fecha1 = datetime.strftime(resto_a_date, "%Y-%m-%d")
        # asigno la fecha nuevamente al stringvar pero lo vuelvo a convertir a string
        self.sv_fecha_planilla.set(value=resto_a_date.strftime('%d/%m/%Y'))

        self.filtro_activo = "WHERE CAST(pl_fecha AS date) = CAST('" + fecha1 + "' AS date)"

        self.llena_grilla("")

    def fdespues(self):

        # Controlo que la fecha no este vacia
        if self.sv_fecha_planilla.get() == "":
            messagebox.showerror("Error", "La fecha es requerida", parent=self)
            self.sv_fecha_planilla.set(value=self.sv_fecha_error.get())
            self.entry_fecha_planilla.focus()
            return

        # primero paso la fecha a formato date
        paso_a_date = datetime.strptime(self.sv_fecha_planilla.get(), "%d/%m/%Y")
        # le resto uno con timedelta - deben estar en formato date
        resto_a_date = paso_a_date + timedelta(days=1)
        # y ahora la paso a string
        fecha1 = datetime.strftime(resto_a_date, "%Y-%m-%d")
        # asigno la fecha nuevamente al stringvar pero lo vuelvo a convertir a string
        self.sv_fecha_planilla.set(value=resto_a_date.strftime('%d/%m/%Y'))

        self.filtro_activo = "WHERE CAST(pl_fecha AS date) = CAST('" + fecha1 + "' AS date)"
        self.llena_grilla("")

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_planilla, 'TOP')

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_planilla, 'END')

    def botones_grid(self):

        for c in range(7):
            self.frame_botones_grid.grid_columnconfigure(c, weight=1, minsize=130)

        # Columnas mas cortas
        # self.frame_botones_grid.grid_columnconfigure(5, weight=1, minsize=50)
        # self.frame_botones_grid.grid_columnconfigure(6, weight=1, minsize=50)
        # self.frame_botones_grid.grid_columnconfigure(7, weight=1, minsize=50)
        # self.frame_botones_grid.grid_columnconfigure(8, weight=1, minsize=50)

        # BOTONES DEL TREEVIEW

        # Nuevo item
        icono = self.cargar_icono("archivo-nuevo.png")
        self.btn_nuevoitem = tk.Button(self.frame_botones_grid, text=" Nuevo Item", command=self.fnuevoitem, width=16,
                                       bg="blue", fg="white", compound="left")
        self.btn_nuevoitem.image = icono
        self.btn_nuevoitem.config(image=icono)
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)
        ToolTip(self.btn_nuevoitem, msg="Ingresar un nuevo item a la planilla")

        # Editar item
        icono = self.cargar_icono("editar.png")
        self.btn_editaitem = tk.Button(self.frame_botones_grid, text=" Edita Item", command=self.feditaitem, width=16,
                                       bg="blue", fg="white", compound="left")
        self.btn_editaitem.image = icono
        self.btn_editaitem.config(image=icono)
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)
        ToolTip(self.btn_editaitem, msg="Editar para modificar un item de planilla")

        # Eliminar un item
        icono = self.cargar_icono("eliminar.png")
        self.btn_borraitem = tk.Button(self.frame_botones_grid, text=" Elimina Item", command=self.fborraitem, width=16,
                                       bg="blue", fg="white", compound="left")
        self.btn_borraitem.image = icono
        self.btn_borraitem.config(image=icono)
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)
        ToolTip(self.btn_borraitem, msg="Borrar un item de planilla")

        # Guardar un item
        icono = self.cargar_icono("guardar.png")
        self.btn_guardaritem = tk.Button(self.frame_botones_grid, text=" Guardar item", command=self.fguardar, width=16,
                                         bg="green", fg="white", compound="left")
        self.btn_guardaritem.image = icono
        self.btn_guardaritem.config(image=icono)
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)
        ToolTip(self.btn_guardaritem, msg="Guardar un item nuevo en la planilla")

        # Cancelar
        icono = self.cargar_icono("cancelar.png")
        self.btn_Cancelar = tk.Button(self.frame_botones_grid, text=" Cancelar", command=self.fcancelar, width=16,
                                      bg="black", fg="white", compound="left")
        self.btn_Cancelar.image = icono
        self.btn_Cancelar.config(image=icono)
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)
        ToolTip(self.btn_Cancelar, msg="Cancela lo que se esta haciendo")

        # Reset
        icono = self.cargar_icono("reset.png")
        self.btn_Reset = tk.Button(self.frame_botones_grid, text=" Reset", command=self.freset, width=16, bg="black",
                                   fg="white", compound="left")
        self.btn_Reset.image = icono
        self.btn_Reset.config(image=icono)
        self.btn_Reset.grid(row=0, column=5, padx=5, pady=2)
        ToolTip(self.btn_Reset, msg="Vuelve el proceso a estado inicial")

        # Resumen del mes
        icono = self.cargar_icono("resumen.png")
        self.btn_Resumen = tk.Button(self.frame_botones_grid, text=" Resumen mes", command=self.fresumen, width=18,
                                     bg="light blue", fg="black", compound="left")
        self.btn_Resumen.image = icono
        self.btn_Resumen.config(image=icono)
        self.btn_Resumen.grid(row=0, column=6, padx=5, pady=2)
        ToolTip(self.btn_Resumen, msg="Informe con totales del mes acumulados")

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_botones_grid, text="", image=self.photo4, command=self.ftoparch,
                                    bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=7, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_botones_grid, text="", image=self.photo5, command=self.ffinarch,
                                    bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=8, padx=5, sticky="nsew", pady=2)

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def entrys_generales(self):

        # FECHA ---------------------------------------------------------------------------
        self.lbl_fecha_planilla = tk.Label(self.frame_entrys_planilla, text="Fecha: ", justify="left")
        self.lbl_fecha_planilla.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)
        self.entry_fecha_planilla = tk.Entry(self.frame_entrys_planilla, textvariable=self.sv_fecha_planilla,
                                             width=10, justify="right")
        # self.entry_fecha_planilla.bind("<FocusIn>", self.fver_blanco)
        self.entry_fecha_planilla.bind("<FocusIn>", lambda event: self.fver_blanco())
        self.entry_fecha_planilla.bind("<FocusOut>",
                                       lambda event: self.varFuncion_new.validar_fecha(self.sv_fecha_planilla,
                                                                                       self.entry_fecha_planilla))
        self.entry_fecha_planilla.grid(row=0, column=1, padx=3, pady=2, sticky=tk.E)

        # ATRAS EN LA FECHA ---------------------------------------------------------------
        self.photo6 = Image.open('atras.png')
        self.photo6 = self.photo6.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo6 = ImageTk.PhotoImage(self.photo6)
        self.btnIzquierda = tk.Button(self.frame_entrys_planilla, text="", image=self.photo6, command=self.fantes,
                                      bg="grey", fg="white")
        self.btnIzquierda.grid(row=0, column=2, padx=5, sticky="nsew", pady=2)

        # ADELANTE EN LA FECHA -------------------------------------------------------------
        self.photo7 = Image.open('avance.png')
        self.photo7 = self.photo7.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo7 = ImageTk.PhotoImage(self.photo7)
        self.btnDerecha = tk.Button(self.frame_entrys_planilla, text="", image=self.photo7, command=self.fdespues,
                                    bg="grey", fg="white")
        self.btnDerecha.grid(row=0, column=3, padx=5, sticky="nsew", pady=2)

        # COMBO TIPO DE MOVIMIENTO ----------------------------------------------------------
        self.lbl_tipomov = tk.Label(self.frame_entrys_planilla, text="Tipo de movimiento: ", justify="left")
        self.lbl_tipomov.grid(row=0, column=4, padx=3, pady=2, sticky=tk.W)
        self.combo_tipomov = ttk.Combobox(self.frame_entrys_planilla, textvariable=self.sv_tipomov,
                                          state='readonly', width=23)
        self.combo_tipomov['value'] = self.varPlanilla.combo_input("tm_descripcion", "tipo_movim",
                                                                   "tm_ingegr")
        self.combo_tipomov.current(0)
        self.combo_tipomov.bind('<Tab>', lambda e: self.divido_tipomov())
        self.combo_tipomov.grid(row=0, column=5, padx=5, pady=2, sticky=tk.W)

        # BOTON BUSQUEDA CLIENTE -------------------------------------------------------------
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = tk.Button(self.frame_entrys_planilla, text="", image=self.photo_bus_cli, command=self.fbuscli,
                                     bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=6, padx=5, pady=2, sticky=tk.E)

        # ENTRY CLIENTE -----------------------------------------------------------------------
        self.lbl_cliente = tk.Label(self.frame_entrys_planilla, text="Cliente: ", justify="left")
        self.lbl_cliente.grid(row=0, column=7, padx=3, pady=2, sticky=tk.W)
        self.entry_cliente = tk.Entry(self.frame_entrys_planilla, textvariable=self.sv_cliente, width=60, justify="left")
        self.entry_cliente.grid(row=0, column=8, padx=3, pady=2, sticky=tk.E)
        self.lbl_codigo_cliente = tk.Label(self.frame_entrys_planilla, textvariable=self.sv_codcli, justify="left")
        self.lbl_codigo_cliente.grid(row=0, column=9, padx=3, pady=2, sticky=tk.E)

    def entrys_detalle_movimientos(self):

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE -----------------------------
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = tk.Button(self.frame_entrys_planilla2, text="", image=self.photo_bus_art,
                                     command=self.fbusart, bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=5, pady=2, sticky=tk.E)

        # ENTRY DETALLE DEL MOVIMIENTO ----------------------------------------------------------
        self.lbl_detalle_movim = tk.Label(self.frame_entrys_planilla2, text="Detalle/Articulo: ", justify="left")
        self.lbl_detalle_movim.grid(row=0, column=1, padx=2, pady=2, sticky=tk.W)
        self.entry_detalle_movim = tk.Entry(self.frame_entrys_planilla2, textvariable=self.sv_detalle_movim, width=144,
                                            justify="left")
        self.entry_detalle_movim.grid(row=0, column=2, padx=3, pady=2, sticky=tk.E)

    def entrys_importes_del_movimiento(self):

        # IMPORTE DEL INGRESO -------------------------------------------------------------------
        self.lbl_ingresos1 = tk.Label(self.frame_entrys_planilla3, text="Ingresos: ", justify="left")
        self.lbl_ingresos1.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.entry_ingresos = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_ingreso, width=10,
                                       justify="right")
        self.entry_ingresos.config(validate="key", validatecommand=self.vcmd)
        self.entry_ingresos.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_ingresos.grid(row=0, column=1, padx=2, pady=2, sticky=tk.E)

        # IMPORTE COSTO -------------------------------------------------------------------------
        self.lbl_costo = tk.Label(self.frame_entrys_planilla3, text="Costos: ", justify="left")
        self.lbl_costo.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
        self.entry_costo = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_costo, width=10, justify="right")
        self.entry_costo.config(validate="key", validatecommand=self.vcmd)
        self.entry_costo.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_costo.grid(row=0, column=3, padx=2, pady=2, sticky=tk.E)

        # CANTIDAD -------------------------------------------------------------------------------
        self.lbl_cantidad = tk.Label(self.frame_entrys_planilla3, text="Cantidad: ", justify="left")
        self.lbl_cantidad.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)
        self.entry_cantidad = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_cantidad, width=6, justify="right")
        self.entry_cantidad.config(validate="key", validatecommand=self.vcmd)
        self.entry_cantidad.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_cantidad.grid(row=0, column=5, padx=2, pady=2, sticky=tk.E)

        # TOTAL CALCULADO INGRESO POR CANTIDAD ---------------------------------------------------
        self.lbl_totventart1 = tk.Label(self.frame_entrys_planilla3, text="Total Ing.: ", justify="left")
        self.lbl_totventart1.grid(row=0, column=6, padx=2, pady=2, sticky=tk.W)
        self.lbl_totventart2 = tk.Label(self.frame_entrys_planilla3, textvariable=self.sv_totingresos, width=10,
                                        justify="right")
        self.lbl_totventart2.grid(row=0, column=7, padx=2, pady=2, sticky=tk.E)

        # TOTAL CALCULADO COSTO POR CANTIDAD ------------------------------------------------------
        self.lbl_totcosto1 = tk.Label(self.frame_entrys_planilla3, text="Total Costo: ", justify="left")
        self.lbl_totcosto1.grid(row=0, column=8, padx=2, pady=2, sticky=tk.W)
        self.lbl_totcosto2 = tk.Label(self.frame_entrys_planilla3, textvariable=self.sv_totcosto, width=10,
                                      justify="right")
        self.lbl_totcosto2.grid(row=0, column=9, padx=2, pady=2, sticky=tk.E)

        # IMPORTE DE EGRESO -----------------------------------------------------------------------
        self.lbl_egreso = tk.Label(self.frame_entrys_planilla3, text="Egreso: ", justify="left")
        self.lbl_egreso.grid(row=0, column=10, padx=2, pady=2, sticky=tk.W)
        self.entry_egreso = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_egreso, width=10, justify="right")
        self.entry_egreso.config(validate="key", validatecommand=self.vcmd)
        self.entry_egreso.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_egreso.grid(row=0, column=11, padx=2, pady=2, sticky=tk.E)

        # IMPORTE PAGOS A CUENTA CORRIENTE ---------------------------------------------------------
        self.lbl_pagoscta = tk.Label(self.frame_entrys_planilla3, text="Pagos cta.cte.: ", justify="left")
        self.lbl_pagoscta.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        self.entry_pagoscta = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_pagos_ctacte, width=10,
                                       justify="right")
        self.entry_pagoscta.config(validate="key", validatecommand=self.vcmd)
        self.entry_pagoscta.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_pagoscta.bind("<FocusOut>", self.tildo_cuenta)
        self.entry_pagoscta.grid(row=1, column=1, padx=2, pady=2, sticky=tk.E)

        # IMPORTE DE COMPRAS A PROVEEDORES U OTRAS --------------------------------------------------
        self.lbl_compras = tk.Label(self.frame_entrys_planilla3, text="Compras: ", justify="left")
        self.lbl_compras.grid(row=1, column=2, padx=2, pady=2, sticky=tk.W)
        self.entry_compras = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_compras, width=10,
                                      justify="right")
        self.entry_compras.bind('<Tab>', lambda e: self.calcular("general"))
        self.entry_compras.config(validate="key", validatecommand=self.vcmd)
        self.entry_compras.grid(row=1, column=3, padx=2, pady=2, sticky=tk.E)

        # BOTON BUSQUEDA PROVEEDOR SI CORRESPPONDE --------------------------------------------------
        self.photo_bus_prov = Image.open('buscar.png')
        self.photo_bus_prov = self.photo_bus_prov.resize((25, 25),
                                                         Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_prov = ImageTk.PhotoImage(self.photo_bus_prov)
        self.btn_bus_prov = tk.Button(self.frame_entrys_planilla3, text="", image=self.photo_bus_prov,
                                      command=self.fbusprov, bg="grey", fg="white")
        self.btn_bus_prov.grid(row=1, column=4, padx=5, pady=2, sticky=tk.E)

        # ENTRY PROVEEDOR ----------------------------------------------------------------------------
        self.lbl_proved = tk.Label(self.frame_entrys_planilla3, text="Proveedor: ", justify="left")
        self.lbl_proved.grid(row=1, column=5, padx=3, pady=2, sticky=tk.W)
        self.entry_proved = tk.Entry(self.frame_entrys_planilla3, textvariable=self.sv_proved, width=93, justify="left")
        self.entry_proved.grid(row=1, column=6, columnspan=8, padx=8, pady=2, sticky=tk.E)

        # CHECKBOX SI ES MOVIMIENTO A CUENTA CORRIENTE -----------------------------------------------
        self.check_ctacte = tk.Checkbutton(self.frame_entrys_planilla3, text='CC', variable=self.sv_check1,
                                           onvalue=1, offvalue=0)
        self.check_ctacte.grid(row=1, column=13, padx=3, pady=2, sticky=tk.E)

    def entrys_combo_forma_pago(self):

        # Forma de pago ------------------------------------------------------------------------------
        self.lbl_forma_pago = tk.Label(self.frame_entrys_planilla4, text="Pago: ", justify="left")
        self.lbl_forma_pago.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)
        self.combo_forma_pago = ttk.Combobox(self.frame_entrys_planilla4, textvariable=self.sv_forma_pago,
                                             state='readonly', width=20)
        self.combo_forma_pago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                          "Cheques", "Otros"]
        self.combo_forma_pago.current(0)
        self.combo_forma_pago.bind("<FocusOut>", self.tildo_cuenta)
        self.combo_forma_pago.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        # DETALLE DEL PAGO ---------------------------------------------------------------------------
        self.entry_detalle_pago = tk.Entry(self.frame_entrys_planilla4, textvariable=self.sv_detalle_pago, width=135,
                                           justify="left")
        self.entry_detalle_pago.grid(row=0, column=2, padx=3, pady=2, sticky=tk.E)

    def entrys_garantias(self):

        # Garantia -----------------------------------------------------------------------------------
        self.lbl_garantia = tk.Label(self.frame_entrys_planilla5, text="Garantias: ", justify="left")
        self.lbl_garantia.grid(row=0, column=0, padx=3, pady=2, sticky=tk.W)
        self.entry_garantia = tk.Entry(self.frame_entrys_planilla5, textvariable=self.sv_garantia, width=152,
                                       justify="left")
        self.entry_garantia.grid(row=0, column=1, padx=3, pady=2, sticky=tk.E)

        # Observaciones ------------------------------------------------------------------------------
        self.lbl_observaciones = tk.Label(self.frame_entrys_planilla5, text="Observaciones: ", justify="left")
        self.lbl_observaciones.grid(row=1, column=0, padx=3, pady=2, sticky=tk.W)
        self.entry_observaciones = tk.Entry(self.frame_entrys_planilla5, textvariable=self.sv_observaciones, width=152,
                                            justify="left")
        self.entry_observaciones.grid(row=1, column=1, padx=3, pady=2, sticky=tk.E)

    def buscar_movimientos(self):

        for c in range(4):
            self.frame_buscar_movimiento.grid_columnconfigure(c, weight=1, minsize=130)

        self.lbl_buscar_movim = tk.Label(self.frame_buscar_movimiento, text="Buscar en todas las planillas: ")
        self.lbl_buscar_movim.grid(row=0, column=0, padx=5, pady=2)
        self.entry_buscar_movim = tk.Entry(self.frame_buscar_movimiento, textvariable=self.sv_buscostring, width=50)
        self.entry_buscar_movim.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.btn_buscar_movim = tk.Button(self.frame_buscar_movimiento, text="Buscar", command=self.fbuscar_en_tabla,
                                          bg="CadetBlue", fg="white", width=35)
        self.btn_buscar_movim.grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.btn_mostrar_todo = tk.Button(self.frame_buscar_movimiento, text="Mostrar todo", command=self.fshowall,
                                          bg="CadetBlue", fg="white", width=35)
        self.btn_mostrar_todo.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)

        for widg in self.frame_buscar_movimiento.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def calculo_totales(self):

        #        fff = tkFont.Font(family="Arial", size=8, weight="bold")

        # TOTAL INGRESOS DE LA FECHA ------------------------------------------------------
        self.lbl_total_ventart1 = tk.Label(self.frame_totales, text="Total ingresos: ", fg="green", justify="left")
        self.lbl_total_ventart1.grid(row=0, column=0, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_ventart2 = tk.Label(self.frame_totales, textvariable=self.sv_total_ingresos, width=12,
                                           justify="left")
        self.lbl_total_ventart2.grid(row=0, column=1, padx=2, pady=2, sticky=tk.E)

        # TOTAL COSTOS DE LA FECHA --------------------------------------------------------
        self.lbl_total_costos1 = tk.Label(self.frame_totales, text="Total costos: ", fg="red", justify="left")
        self.lbl_total_costos1.grid(row=1, column=0, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_costos2 = tk.Label(self.frame_totales, textvariable=self.sv_total_costos, width=12,
                                          justify="left")
        self.lbl_total_costos2.grid(row=1, column=1, padx=2, pady=2, sticky=tk.E)

        # TOTAL UTILIDAD DE LA FECHA ( VENTAS MENOS COSTOS) --------------------------------
        self.lbl_total_utilidad1 = tk.Label(self.frame_totales, text="Utilidad: ", fg="blue", justify="left")
        self.lbl_total_utilidad1.grid(row=0, column=2, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_utilidad2 = tk.Label(self.frame_totales, textvariable=self.sv_total_utilidad, width=12,
                                            justify="left")
        self.lbl_total_utilidad2.grid(row=0, column=3, padx=2, pady=2, sticky=tk.E)

        # TOTAL EGRESOS DE LA FECHA --------------------------------------------------------
        self.lbl_total_egresos1 = tk.Label(self.frame_totales, text="Total Egresos: ", fg="red", justify="left")
        self.lbl_total_egresos1.grid(row=1, column=2, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_egresos2 = tk.Label(self.frame_totales, textvariable=self.sv_total_egresos, width=12,
                                           justify="left")
        self.lbl_total_egresos2.grid(row=1, column=3, padx=2, pady=2, sticky=tk.E)

        # TOTAL UTILIDAD PERO AHORA MENOS LOS EGRESOS ---------------------------------------
        self.lbl_total_util_menos_egre1 = tk.Label(self.frame_totales, text="Total Util.-Egr.: ", fg="blue",
                                                   justify="left")
        self.lbl_total_util_menos_egre1.grid(row=0, column=4, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_util_menos_egre2 = tk.Label(self.frame_totales, textvariable=self.sv_total_util_menos_egr,
                                                   width=12, justify="left")
        self.lbl_total_util_menos_egre2.grid(row=0, column=5, padx=2, pady=2, sticky=tk.E)

        # TOTAL PAGOS DE LA FECHA -----------------------------------------------------------
        self.lbl_total_pagos1 = tk.Label(self.frame_totales, text="Total Pagos: ", fg="green", justify="left")
        self.lbl_total_pagos1.grid(row=1, column=4, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_pagos2 = tk.Label(self.frame_totales, textvariable=self.sv_total_pagos, width=12,
                                         justify="left")
        self.lbl_total_pagos2.grid(row=1, column=5, padx=2, pady=2, sticky=tk.E)

        # TOTAL COMPRAS DE LA FECHA ---------------------------------------------------------
        self.lbl_total_compras1 = tk.Label(self.frame_totales, text="Total Compras: ", fg="red", justify="left")
        self.lbl_total_compras1.grid(row=0, column=8, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_compras2 = tk.Label(self.frame_totales, textvariable=self.sv_total_compras, width=12,
                                           justify="left")
        self.lbl_total_compras2.grid(row=0, column=9, padx=2, pady=2, sticky=tk.E)

        # TOTAL GANANCIA LIMPIA POR VENTA DE ARTICULOS ---------------------------------------
        self.lbl_total_limpio_artic1 = tk.Label(self.frame_totales, text="Ganancia Artic.: ", fg="green",
                                                justify="left")
        self.lbl_total_limpio_artic1.grid(row=0, column=6, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_limpio_artic2 = tk.Label(self.frame_totales, textvariable=self.sv_total_limpio_artic, width=12,
                                                justify="left")
        self.lbl_total_limpio_artic2.grid(row=0, column=7, padx=2, pady=2, sticky=tk.E)

        # TOTAL GANANCIA LIMPIA POR SERVICIOS -------------------------------------------------
        self.lbl_total_limpio_serv1 = tk.Label(self.frame_totales, text="Ganancia Serv.: ", fg="green", justify="left")
        self.lbl_total_limpio_serv1.grid(row=1, column=6, padx=2, pady=2, sticky=tk.W)
        self.lbl_total_limpio_serv2 = tk.Label(self.frame_totales, textvariable=self.sv_total_limpio_serv, width=12,
                                               justify="left")
        self.lbl_total_limpio_serv2.grid(row=1, column=7, padx=2, pady=2, sticky=tk.E)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.frame_totales, text="Salir", image=self.photo3, width=45, command=self.fsalir,
                                  bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=10, rowspan=2, padx=3, pady=3, sticky="nsew")

        for widg in self.frame_totales.winfo_children():
            widg.grid_configure(padx=4, pady=1, sticky='nsew')

    def cuadro_grid_planilla(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_planilla)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_planilla = ttk.Treeview(self.frame_tvw_planilla, height=6, columns=("col1", "col2", "col3", "col4",
                                                                        "col5", "col6", "col7", "col8", "col9", "col10",
                                                                        "col11", "col12", "col13", "col14", "col15",
                                                                        "col16", "col17", "col18", "col19"))

        self.grid_planilla.bind("<Double-Button-1>", self.doble_click_grid_pla)

        self.grid_planilla.column("#0", width=30, anchor="center", minwidth=30)
        self.grid_planilla.column("col1", width=80, anchor="center", minwidth=70)
        self.grid_planilla.column("col2", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col3", width=350, anchor="center", minwidth=250)
        self.grid_planilla.column("col4", width=30, anchor="center", minwidth=60)
        self.grid_planilla.column("col5", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col6", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col7", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col8", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col9", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col10", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col11", width=170, anchor="center", minwidth=170)
        self.grid_planilla.column("col12", width=150, anchor="center", minwidth=100)
        self.grid_planilla.column("col13", width=150, anchor="center", minwidth=250)
        self.grid_planilla.column("col14", width=100, anchor="center", minwidth=250)
        self.grid_planilla.column("col15", width=100, anchor="center", minwidth=250)
        self.grid_planilla.column("col16", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col17", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col18", width=100, anchor="center", minwidth=80)
        self.grid_planilla.column("col10", width=100, anchor="center", minwidth=80)

        self.grid_planilla.heading("#0", text="Id", anchor="center")
        self.grid_planilla.heading("col1", text="Fecha", anchor="center")
        self.grid_planilla.heading("col2", text="Tipo Mov.", anchor="center")
        self.grid_planilla.heading("col3", text="Detalle", anchor="center")
        self.grid_planilla.heading("col4", text="Cant.", anchor="center")
        self.grid_planilla.heading("col5", text="Ingresos(I)", anchor="center")
        self.grid_planilla.heading("col6", text="Total Ingresos", anchor="center")
        self.grid_planilla.heading("col7", text="Egresos(E)", anchor="center")
        self.grid_planilla.heading("col8", text="Costos", anchor="center")
        self.grid_planilla.heading("col9", text="Pagos CtaCte(I)", anchor="center")
        self.grid_planilla.heading("col10", text="Compras(E)", anchor="center")
        self.grid_planilla.heading("col11", text="Cliente", anchor="center")
        self.grid_planilla.heading("col12", text="Tipo pago", anchor="center")
        self.grid_planilla.heading("col13", text="Detalle pago", anchor="center")
        self.grid_planilla.heading("col14", text="Garantia", anchor="center")
        self.grid_planilla.heading("col15", text="Observaciones", anchor="center")
        self.grid_planilla.heading("col16", text="Proveedor", anchor="center")
        self.grid_planilla.heading("col17", text="CtaCte", anchor="center")
        self.grid_planilla.heading("col18", text="ClaveMov", anchor="center")
        self.grid_planilla.heading("col19", text="Codigo Cliente", anchor="center")

        self.grid_planilla.tag_configure('oddrow', background='light grey')
        self.grid_planilla.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_tvw_planilla, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_tvw_planilla, orient="vertical")
        self.grid_planilla.config(xscrollcommand=scroll_x.set)
        self.grid_planilla.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_planilla.xview)
        scroll_y.config(command=self.grid_planilla.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_planilla['selectmode'] = 'browse'

        self.grid_planilla.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    # Trabajan con fguardar
    def validar_campos(self, condicion, mensaje, widget_focus):
        if condicion:
            messagebox.showerror("Error", mensaje, parent=self)
            widget_focus.focus()
            return True
        return False

    def get_planilla_dict(self, fecha_aux):
        return {
            "Id": self.clave,
            "pl_fecha": fecha_aux,
            "pl_tipomov": self.sv_tipomov.get(),
            "pl_detalle": self.sv_detalle_movim.get(),
            "pl_cantidad": self.sv_cantidad.get(),
            "pl_ingresos": self.sv_ingreso.get(),
            "pl_egreso": self.sv_egreso.get(),
            "pl_costo": self.sv_costo.get(),
            "pl_pagoscta": self.sv_pagos_ctacte.get(),
            "pl_compras": self.sv_compras.get(),
            "pl_cliente": self.sv_cliente.get(),
            "pl_tipopago": self.sv_forma_pago.get(),
            "pl_detapago": self.sv_detalle_pago.get(),
            "pl_garantia": self.sv_garantia.get(),
            "pl_observacion": self.sv_observaciones.get(),
            "pl_proved": self.sv_proved.get(),
            "pl_ctacte": self.sv_check1.get(),
            "pl_clavemov": self.sv_clavemov.get(),
            "pl_codcli": self.sv_codcli.get(),
        }

    def get_ctacte_dict(self, fecha_aux):
        return {
            "Id": self.clave,
            "cc_fecha": fecha_aux,
            "cc_detalle": self.sv_detalle_movim.get(),
            "cc_ingreso": (float(self.sv_ingreso.get()) * float(self.sv_cantidad.get())),
            "cc_egreso": self.sv_pagos_ctacte.get(),
            "cc_codcli": self.sv_codcli.get(),
            "cc_nomcli": self.sv_cliente.get(),
            "cc_clavemov": self.sv_clavemov.get(),
        }

    @staticmethod
    def cargar_icono(path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

"""
    # 🔥 CÓMO USARLO
    # ✔ Guardar
    # self.set_status("✔ Registro guardado correctamente", "ok")
    # 🗑 Eliminar
    # self.set_status("🗑 Cliente eliminado", "ok")
    # ⚠ Validación
    # self.set_status("⚠ CUIT incorrecto", "warn")
    # ❌ Error
    # self.set_status("❌ Error al guardar", "error")
    # ℹInfo
    # self.set_status("ℹ Buscando clientes...", "info")
"""
