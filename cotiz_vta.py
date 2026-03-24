from cotiz_ABM import *
from funcion_new import *
from funciones import *
import os
import tkinter.font as tkFont
from datetime import datetime, date
from tkinter import *
from PIL import Image, ImageTk
from PDF_clase import *
class VentCotiz(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # Instanciaciones -------------------------------------------------------
        self.varCotiz = datosCotiz()
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # -----------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # PANTALLA
        # ------------------------------------------------------------------------
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """

        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()

        # Asigno fijo un ancho y un alto
        ancho_ventana = 1030
        alto_ventana = 650

        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla_auxiliar("")
        self.llena_grilla_principal("")

        # ---------------------------------------------------------------------
        # """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. """
        #
        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_tvw_auxiliar_venta.identify_row(0)
        # # Grid de auxventas
        # self.grid_tvw_auxiliar_venta.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_tvw_auxiliar_venta.focus(item)
        # # vacio tabla auxiliar de ventas
        # self.habilitar_text("disabled")
        # # habilitar botones
        # self.habilitar_botones("disabled", "normal", "browse")
        # ---------------------------------------------------------------------

    # ---------------------------------------------------------------------
    # WIDGETS
    # ---------------------------------------------------------------------

    def create_widgets(self):

        # ---------------------------------------------------------------------
        # TITULOS
        # ---------------------------------------------------------------------
        # Encabezado logo y titulo con PACK
        # self.frame_titulo_top = Frame(self.master)
        #
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
        # --------------------------------------------------------------------------

        # VARIABLES GENERALES ----------------------------------------------------------------
        # para validar ingresos de numeros en gets numericos
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ---------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------
        # DATOS DE LA VENTA Y DATOS CLIENTE
        self.strvar_nro_venta = tk.StringVar(value="0")
        self.strvar_fecha_venta = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_nombre_cliente = tk.StringVar(value="Consumidor Final")
        self.strvar_sit_fiscal = tk.StringVar(value="")
        self.strvar_cuit = tk.StringVar(value="")

        # VALOR DEL DOLAR HOY
        self.strvar_valor_dolar_hoy = tk.StringVar(value="0.00")
        self.strvar_tasa_recargo_precio = tk.StringVar(value="0")
        self.traer_dolarhoy() # trae dolar y tasa recargo precio con tarjeta

        # ARTICULO ITEM INGRESADO A AUX_VENTAS
        self.strvar_it_codigo_articulo = tk.StringVar(value="")
        self.strvar_it_descripcion_articulo = tk.StringVar(value="")
        self.strvar_it_marca_articulo = tk.StringVar(value="")
        self.strvar_it_rubro_articulo = tk.StringVar(value="")
        self.strvar_it_ultima_actual = tk.StringVar(value="")

        # TOTALES REFERIDOS A CARGA DEL ITEM DE VENTA
        # cantidad a comprar
        self.strvar_cantidad_venta = tk.StringVar(value="1")

        # costo dolares neto articulo unidad
        self.strvar_unidad_costo_dolar = tk.StringVar()
        # costo dolares bruto articulo unidad
        self.strvar_unidad_costo_dolar_bruto = tk.StringVar(value="0.00")

        # costo pesos bruto articulo unidad
        self.strvar_unidad_costo_bruto_pesos = tk.StringVar(value="0.00")
        # Costo pesos NETO articulo unidad
        self.strvar_unidad_neto_pesos = tk.StringVar(value="0.00")
        # Costo pesos NETO articulo X cantidad
        # self.strvar_xcanti_neto_total = tk.StringVar(value="0.00")

        # Venta pesos final articulo unidad
        self.strvar_unidad_precio_venta_contado = tk.StringVar(value="0.00")
        self.strvar_unidad_precio_venta_lista = tk.StringVar(value="0.00")
        # Venta pesos final articulo por cantidad
        self.strvar_xcanti_total_precio_venta_lista = tk.StringVar(value="0.00")

        # Tasa del iva %
        self.strvar_combo_tasa_iva = tk.StringVar()
        # Importe iva articulo (21 o 10.5) unidad
        self.strvar_unidad_total_iva = tk.StringVar(value="0.00")
        # Importe iva articulo por la cantidad
        # self.strvar_xcanti_total_iva = tk.StringVar(value="0.00")
        # Importe iva del articulo 21% (separo para guardar)
        self.strvar_unidad_total_iva_21 = tk.StringVar(value="0.00")
        # Importe iva del articulo 10,5% (separo para guardar)
        self.strvar_unidad_total_iva_105 = tk.StringVar(value="0.00")

        # Tasa Ganancia por articulo
        self.strvar_unidad_tasa_ganancia = tk.StringVar(value="0.00")
        # Importe ganancia del articulo unidad
        self.strvar_unidad_total_ganancia = tk.StringVar(value="0.00")
        # Importe ganancia del articulo X cantidad
        self.strvar_xcanti_total_ganancia = tk.StringVar(value="0.00")

        # TIPOS DE PAGO
        self.strvar_combo_formas_pago = tk.StringVar()
        self.strvar_detalle_pago = tk.StringVar(value="")

        # TOTALES FINALES GLOBALES TODA LA VENTA
        # 1 pago
        self.strvar_global_final_venta = tk.StringVar(value="0")
        #self.strvar_global_final_venta_iva21 = tk.StringVar(value="0")
        #self.strvar_global_final_venta_iva105 = tk.StringVar(value="0")
        #self.strvar_global_final_venta_neto = tk.StringVar(value="0")

        self.strvar_buscostring = tk.StringVar(value="")

        # ---------------------------------------------------------------------
        # Abro frame principal
        self.frame_principal=LabelFrame(self.master, text="", foreground="#CD5C5C")

        # ---------------------------------------------------------------------
        # GRID TABLA VENTAS YA REALIZADAS
        # ---------------------------------------------------------------------
        self.frame_grid_ventas_realizadas=LabelFrame(self.frame_principal, text="Ventas realizadas",
                                                     foreground="#CD5C5C")
        self.cuadro_grid_ventas_realizadas()
        self.frame_grid_ventas_realizadas.pack(side="top", fill="both", padx=5, pady=2)

        # ---------------------------------------------------------------------
        # BOTONES BUSQUEDA Y CRUD VENTAS GRID PRINCIPAL
        # ---------------------------------------------------------------------
        self.frame_botones_grid_principal=LabelFrame(self.frame_principal, text="", border=5, foreground="black",
                                             background="light blue")
        self.cuadro_botones_grid_principal()
        self.frame_botones_grid_principal.pack(side="top", fill="both", padx=5, pady=2)
        
        # ---------------------------------------------------------------------
        # Cierro fame principal
        self.frame_principal.pack(side="top", fill="both", padx=5, pady=2)

        # ---------------------------------------------------------------------
        # ENTRYS UNO CLIENTE Y VENTA
        # ---------------------------------------------------------------------
        self.frame_entrys_cliente = LabelFrame(self.master, text="", foreground="blue")
        self.cuadro_entrys_cliente()
        self.frame_entrys_cliente.pack(side="top", fill="both", expand=0, padx=5, pady=3)

        # ---------------------------------------------------------------------
        # ENTRYS DOS ARTICULO
        # ---------------------------------------------------------------------
        self.frame_entrys_articulo = LabelFrame(self.master, text="Articulo", foreground="black")
        self.cuadro_entrys_articulo()
        self.frame_entrys_articulo.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # ---------------------------------------------------------------------
        # ENTRYS TRES ARTICULO PRECIOS Y CANTIDADES
        # ---------------------------------------------------------------------
        # frame particular - Precios y cantidades
        self.frame_entrys_importes_articulo = LabelFrame(self.master)
        self.cuadro_entrys_importes_articulo()
        self.frame_entrys_importes_articulo.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # ---------------------------------------------------------------------
        # BOTONES CRUD ARTICULO ACTUAL
        # ---------------------------------------------------------------------
        self.frame_botones_articulo = LabelFrame(self.master)
        self.cuadro_botones_articulo()
        self.frame_botones_articulo.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # ---------------------------------------------------------------------
        # GRID AUXILIAR PARA VENTA
        # ---------------------------------------------------------------------
        self.frame_grid_auxiliar_venta=LabelFrame(self.master, text="Articulos venta actual ", foreground="#CD5C5C")
        self.cuadro_grid_auxiliar_venta()
        self.frame_grid_auxiliar_venta.pack(side="top", fill="both", padx=5, pady=2)

        # ---------------------------------------------------------------------
        # TOTALES DE VENTA
        # ---------------------------------------------------------------------
        self.frame_totales_todo=LabelFrame(self.master, text="Total Venta", border=5, foreground="black")
        self.cuadro_totales_venta()
        self.frame_totales_todo.pack(expand=0, side="top", fill="both", pady=2, padx=5)

        # ---------------------------------------------------------------------
        # BOTONES GRID AUXILIAR PARA VENTA
        # ---------------------------------------------------------------------
        self.frame_botones_aux_ventas = LabelFrame(self.master)
        self.cuadro_botones_aux_ventas()
        self.frame_botones_aux_ventas.pack(expand=0, side="top", fill="both", pady=2, padx=5)

    # ---------------------------------------------------------------------
    # ESTADOS
    # ---------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo = "aux_ventas ORDER BY av_desc_art ASC"
        self.filtro_activo_resuventa = "resu_ventas ORDER BY rv_fecha"
        self.alta_modif = 0
        # Vacio tabla auxiliar de ventas
        self.varCotiz.vaciar_auxventas("aux_ventas")
        self. habilitar_botones("disabled","normal", "disabled")
        self.limpiar_entrys("todo")
        self.habilitar_text("disabled")

    def habilitar_botones(self, estado1, estado2, estado3):

        self.btn_ingresar_itemventa.configure(state=estado1)
        self.btn_eliminar_itemventa.configure(state=estado1)
        self.btn_cerrar_venta.configure(state=estado1)
        self.btn_reset_art.config(state=estado1)
        #self.btn_imprime_venta.configure(state=estado1)
        self.btn_bus_art.configure(state=estado1)
        self.btn_bus_cli.configure(state=estado1)
        self.btn_showall.configure(state=estado2)
        self.btn_buscar.configure(state=estado2)
        self.entry_busqueda_venta.configure(state=estado2)

        self.btn_nueva_venta.configure(state=estado2)
        self.btn_edito_venta.configure(state=estado2)
        self.btn_borro_venta.configure(state=estado2)

        #self.grid_tvw_todaslasventas.configure(selectmode=estado3)
        if estado3 == "none":
            self.btnFinarch.configure(state="disabled")
            self.btnToparch.configure(state="disabled")
        else:
            self.btnFinarch.configure(state="normal")
            self.btnToparch.configure(state="normal")

    def habilitar_text(self, estado):

        self.entry_nombre_cliente.configure(state=estado)
        self.entry_detalle_movim.configure(state=estado)
        self.entry_fecha_venta.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cantidad_venta.configure(state=estado)
        self.entry_precio_lista_unidad.configure(state=estado)
        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)

        # self.entry_tasa_ganancia_unidad2.configure(state=estado)
        # self.entry_ganancia_pesos_unidad2.configure(state=estado)
        # self.entry_precio_venta_unidad.configure(state=estado)

        self.combo_tasa_iva.configure(state=estado)

    def limpiar_entrys(self, parte):

        if parte == "todo":
            # datos del cliente
            self.strvar_codigo_cliente.set(value="0")
            self.strvar_nombre_cliente.set(value="Consumidor Final")
            self.combo_sit_fiscal_cliente.current(0)
            self.strvar_cuit.set(value="")

        # datos del articulo
        self.strvar_it_codigo_articulo.set(value="")
        self.strvar_it_descripcion_articulo.set(value="")
        self.strvar_it_marca_articulo.set(value="")
        self.strvar_it_rubro_articulo.set(value="")
        self.strvar_it_ultima_actual.set(value="")

        # cantidad a comprar
        self.strvar_cantidad_venta.set(value="1")

        # costo dolares neto articulo unidad
        self.strvar_unidad_costo_dolar.set(value="0.00")
        # costo dolares bruto articulo unidad
        self.strvar_unidad_costo_dolar_bruto.set(value="0.00")
        # costo pesos bruto articulo unidad
        self.strvar_unidad_costo_bruto_pesos.set(value="0.00")
        # Costo pesos NETO articulo unidad
        self.strvar_unidad_neto_pesos.set(value="0.00")
        # Costo pesos NETO articulo X cantidad
        # self.strvar_xcanti_neto_total.set(value="0.00")
        # Venta pesos final articulo unidad
        self.strvar_unidad_precio_venta_contado.set(value="0.00")
        self.strvar_unidad_precio_venta_lista.set(value="0.00")
        # Venta pesos final articulo por cantidad
        self.strvar_xcanti_total_precio_venta_lista.set(value="0.00")
        # Tasa del iva %
        #        self.strvar_combo_tasa_iva = tk.StringVar()
        self.combo_tasa_iva.current(0)
        # Importe iva articulo (21 o 10.5) unidad
        self.strvar_unidad_total_iva.set(value="0.00")
        # Importe iva articulo por la cantidad
        #self.strvar_xcanti_total_iva.set(value="0.00")
        # Importe iva del articulo 21% (separo para guardar)
        self.strvar_unidad_total_iva_21.set(value="0.00")
        # Importe iva del articulo 10,5% (separo para guardar)
        self.strvar_unidad_total_iva_105.set(value="0.00")
        # Tasa Ganancia por articulo
        self.strvar_unidad_tasa_ganancia.set(value="0.00")
        # Importe ganancia del articulo unidad
        self.strvar_unidad_total_ganancia.set(value="0.00")
        # Importe ganancia del articulo X cantidad
        self.strvar_xcanti_total_ganancia.set(value="0.00")

    def traer_dolarhoy(self):
        dev_informa = self.varCotiz.consultar_informa()
        for row in dev_informa:
            self.strvar_valor_dolar_hoy.set(value=row[21])
            self.strvar_tasa_recargo_precio.set(value=row[23])

    # ---------------------------------------------------------------------
    # GRID AUXILIAR
    # ---------------------------------------------------------------------

    def limpiar_grid_auxiliar(self):
        # Limpia grid tabla auxiliar

        for item in self.grid_tvw_auxiliar_venta.get_children():
            self.grid_tvw_auxiliar_venta.delete(item)

    def llena_grilla_auxiliar(self, ult_tabla_id):
        # GRid auxiliar de articulos a vender

        datos = self.varCotiz.consultar_articulo_item_vta(self.filtro_activo)

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_tvw_auxiliar_venta.insert("", "end", tags=color, text=row[0], values=(row[1], row[2],
                                                                     row[3], row[4], row[5], row[6], row[12], row[13]))
        if len(self.grid_tvw_auxiliar_venta.get_children()) > 0:
               self.grid_tvw_auxiliar_venta.selection_set(self.grid_tvw_auxiliar_venta.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:
            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_tvw_auxiliar_venta.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_tvw_auxiliar_venta.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
                de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

            self.grid_tvw_auxiliar_venta.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_tvw_auxiliar_venta.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_tvw_auxiliar_venta.yview(self.grid_tvw_auxiliar_venta.index(rg))
        else:
            # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
            self.mover_puntero_topend("END")

    # ---------------------------------------------------------------------
    # GRID PRINCIPAL
    # ---------------------------------------------------------------------

    def limpiar_grid_principal(self):

        # limpia al GRID de las ventas ya realizadas o historicas (principal)
        for item in self.grid_tvw_todaslasventas.get_children():
            self.grid_tvw_todaslasventas.delete(item)

    def llena_grilla_principal(self, ult_tabla_id):
        # Llena el GRID de las ventas realizadas - historicas

        datos = self.varCotiz.consultar_articulo_item_vta(self.filtro_activo_resuventa)

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            self.grid_tvw_todaslasventas.insert("", "end", tags=color, text=row[0], values=(row[1], row[2],
                                                                                      row[4], row[10], row[7], row[8]))

        if len(self.grid_tvw_todaslasventas.get_children()) > 0:
               self.grid_tvw_todaslasventas.selection_set(self.grid_tvw_todaslasventas.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:
            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_tvw_todaslasventas.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_tvw_todaslasventas.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
                de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

            self.grid_tvw_todaslasventas.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_tvw_todaslasventas.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_tvw_todaslasventas.yview(self.grid_tvw_todaslasventas.index(rg))
        else:
            # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
            self.mover_puntero_topend("END")

    # ---------------------------------------------------------------------
    # reset - cancelacion - salida
    # ---------------------------------------------------------------------

    def fReset_articulo(self):

        self.strvar_it_descripcion_articulo.set(value="")
        self.strvar_unidad_costo_bruto_pesos.set(value="0.00")
        self.strvar_unidad_total_ganancia.set(value="0.00")
        self.strvar_unidad_tasa_ganancia.set(value="0.00")
        self.strvar_unidad_precio_venta_contado.set(value="0.00")
        self.strvar_unidad_precio_venta_lista.set(value="0.00")
        self.strvar_unidad_neto_pesos.set(value="0.00")
        self.strvar_unidad_costo_dolar_bruto.set(value="0.00")
        self.strvar_xcanti_total_precio_venta_lista.set(value="0.00")
        self.strvar_xcanti_total_ganancia.set(value="0.00")
        self.strvar_cantidad_venta.set(value="1")
        self.strvar_unidad_total_iva.set(value="0.00")
        self.entry_detalle_movim.focus()

    def fReset_venta(self):
        # Boton CANCELAR

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.fReiniciar_todo()

    def fReiniciar_todo(self):

        self. limpiar_grid_auxiliar()

        # 2 - Desactivar campos y botones
        self.habilitar_text("disabled")
        self.habilitar_botones("disabled", "normal", "browse")

        # 3 - Poner en cero totales grupales
        #self.strvar_global_final_venta_neto.set(value="0.00")
        #self.strvar_global_final_venta_iva21.set(value="0.00")
        #self.strvar_global_final_venta_iva105.set(value="0.00")
        self.strvar_global_final_venta.set(value="0.00")

        self.limpiar_entrys("todo")

        una_fecha = date.today()
        self.strvar_fecha_venta.set(value=una_fecha.strftime('%d/%m/%Y'))

        # buscar numero de venta
        self.strvar_nro_venta.set(value=str(int(self.varCotiz.traer_ultimo(1)) + 1))

    def fSalir(self):
        self.master.destroy()

    # ---------------------------------------------------------------------
    # CRUD sobre Grid auxiliar -
    # ---------------------------------------------------------------------

    def fInsertar_item_venta_auxiliar(self):

        # Ingresa el articulo a la grilla de venta parcial - auxiliar

        # Validar los items ingresados
        # 1- que articulo no este vacio
        if len(self.strvar_it_descripcion_articulo.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de articulo", parent=self)
            return
        # 2- que exista una cantidad
        if float(self.strvar_cantidad_venta.get()) == 0:
            messagebox.showerror("Error", "Falta cantidad de articulo", parent=self)
            self.entry_cantidad_venta.focus()
            return

        # INSERTO ARTICULO EN AUXILIAR DE VENTA (aux_ventas)
        # if self.strvar_combo_tasa_iva.get() == "21.00":
        #     self.strvar_unidad_total_iva_21.set(value=self.strvar_unidad_total_iva.get())
        # elif self.strvar_combo_tasa_iva.get() == "10.50":
        #     self.strvar_unidad_total_iva_105.set(value=self.strvar_unidad_total_iva.get())

        self.varCotiz.insertar_auxventa(self.strvar_it_codigo_articulo.get(),
                                        self.strvar_it_descripcion_articulo.get(),
                                        self.strvar_it_marca_articulo.get(),
                                        self.strvar_cantidad_venta.get(),
                                        self.strvar_unidad_precio_venta_contado.get(),
                                        self.strvar_unidad_precio_venta_lista.get(),
                                        self.strvar_unidad_neto_pesos.get(),
                                        self.strvar_unidad_total_iva_21.get(),
                                        self.strvar_unidad_total_iva_105.get(),
                                        self.strvar_unidad_total_ganancia.get(),
                                        self.strvar_unidad_costo_bruto_pesos.get(),
                                        self.strvar_unidad_costo_dolar.get(),
                                        self.strvar_combo_tasa_iva.get())

        # Calculos de totales finales de la venta
        self.calcular("totalventa")

        # Refresco grid auxiliar
        self.limpiar_grid_auxiliar()
        self.llena_grilla_auxiliar("")

        # dejar en blanco todos los entrys del articulo
        self.limpiar_entrys("articulo")

        # poner disabled datos del cliente -la fecha QUEDA EDITADA
        self.entry_nombre_cliente.configure(state="disabled")
        self.combo_sit_fiscal_cliente.configure(state="disabled")
        self.entry_cuit_cliente.configure(state="disabled")
        self.btn_bus_cli.configure(state="disabled")

        messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)
        
        """
        # En esta insercion, no trabajo movimiento del puntero, dado que no son muchos articulos que se 
        # cargan y es solo un movimiento auxiliar
        """

        self.entry_detalle_movim.focus()

    def fQuitar_item_venta_auxiliar(self):
        # Boton QUITAR ITEM DE VENTA en tabla auxiliar

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

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        self.varCotiz.eliminar_auxventa(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_grid_auxiliar()
        self.llena_grilla_auxiliar(self.clave_ant)

        self.calcular("totalventa")

    # ---------------------------------------------------------------------
    # CRUD sobre Grid Principal
    # ---------------------------------------------------------------------

    def fCerrarVenta(self):
        # iNGRESA LA VENTA A VENTAS REALIZADAS - HISTORICO

        # valido que haya items en venta
        if len(self.grid_tvw_auxiliar_venta.get_children()) <= 0:
            messagebox.showerror("Error", "No hay items en ventas", parent=self)
            return
        # velido nro venta
        if self.strvar_nro_venta.get() == 0:
            messagebox.showerror("Error", "Verifique numero de venta", parent=self)
            return
        # valido fecha venta
        if self.strvar_fecha_venta.get() == "":
            messagebox.showerror("Error", "Verifique fecha de venta", parent=self)
            return

        # borrar este numero de venta si existiera como en el caso de una modificacion en resuventas y en detaventas
        self.varCotiz.eliminar_detaventa(self.strvar_nro_venta.get())
        self.varCotiz.eliminar_resuventa2(self.strvar_nro_venta.get())

        # ---------------------------------------------------------------------------------------
        # DETALLE DE VENTAS

        # Inserto en deta_ventas Tabla que contiene el detalle de articulos de la venta
        datos = self.varCotiz.consultar_detalle_auxventas("aux_ventas")

        total_ventas = 0
        self.alta_modif = 1

        for row in datos:

            # inserto en tabla DETA_VENTAS (ventas detalladas por articulo)

            self.varCotiz.insertar_detaventa(self.strvar_nro_venta.get(),
                                             row[1],  # codigo articulo
                                             row[2],  # desc.articulo
                                             row[3],  # marca articulo
                                             row[4],  # cantidad vendida
                                             row[5],  # precio final venta contado unidad
                                             row[6],  # precio final venta lista unidad
                                             row[7],  # neto venta unidad
                                             row[8],  # iva 21 unidad
                                             row[9],  # iva 10.5 unidad
                                             row[10], # importe ganancia unidad
                                             row[12], # costo dolar unidad
                                             row[11], # costo pesos bruto unidad
                                             row[13]) # tasa iva

            total_ventas += row[4] * row[6]  # precio de lista unitario por cantidad
        # --------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------
        # RESUMEN DE VENTAS

        # inserto en RESU_VENTAS - Resumen de la venta - datos del cliente y pago

        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
        self.selected = self.grid_tvw_todaslasventas.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo
        # verlo en la base 1, 2, 3, 4......)
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')

        fecha_aux = datetime.strptime(self.strvar_fecha_venta.get(), '%d/%m/%Y')
        self.varCotiz.insertar_resuventa(self.strvar_nro_venta.get(), fecha_aux,
                                         self.strvar_codigo_cliente.get(),
                                         self.strvar_nombre_cliente.get(),
                                         self.strvar_sit_fiscal.get(),
                                         self.strvar_cuit.get(),
                                         self.strvar_combo_formas_pago.get(),
                                         self.strvar_detalle_pago.get(),
                                         self.strvar_valor_dolar_hoy.get(),
                                         total_ventas)

        messagebox.showinfo("Guardar", "Ingreso correcto detalle y resumen", parent=self)

        # refresco grid de resuventas para que se me actualie la grilla de resuventas
        self.limpiar_grid_principal()

        if self.alta_modif == 1:
            ultimo_tabla_id = self.varCotiz.traer_ultimo(0)
            print(ultimo_tabla_id)
            print("nada")
            self.llena_grilla_principal(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla_principal(self.clave)

        self.alta_modif = 0

        # pongo all en blanco como si recien iniciara para que se pueda pedir una nueva venta
        self.fReiniciar_todo()

    # ---------------------------------------------------------------------
    # CRUD VENTAS sobre tabla principal RESU_VENTAS
    # ---------------------------------------------------------------------

    def fNueva_venta(self):

        self.varCotiz.vaciar_auxventas("aux_ventas")
        self.habilitar_text("normal")
        self.habilitar_botones("normal", "disabled", "none")
        # sumo uno a nueva venta
        self.strvar_nro_venta.set(value=str(int(self.varCotiz.traer_ultimo(1)) + 1))
        # mando foco al artiulo
        self.entry_detalle_movim.focus()

    def fEdito_venta(self):

        # 1 - Obtener el numero de ventas_interno
        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        # Vacio tabla auxiliar
        self.varCotiz.vaciar_auxventas("aux_ventas")

        # preparacion
        self.habilitar_text("normal")
        self.habilitar_botones("normal", "disabled", "none")
        self.entry_detalle_movim.focus()

        # -------------------------------------------------------------------------------
        # En lista valores cargo todos los campos de la venta
        valores = self.grid_tvw_todaslasventas.item(self.selected, 'values')

        self.strvar_nro_venta.set(value=valores[0])

        # 2 - Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta
        datos_resuventa = self.varCotiz.traer_resu_venta(self.strvar_nro_venta.get())

        fechapaso = datos_resuventa[2].strftime('%d/%m/%Y')
        self.strvar_fecha_venta.set(fechapaso)
        self.strvar_codigo_cliente.set(value=datos_resuventa[3])
        self.strvar_nombre_cliente.set(value=datos_resuventa[4])
        self.strvar_sit_fiscal.set(value=datos_resuventa[5])
        self.strvar_cuit.set(value=datos_resuventa[6])
        self.strvar_combo_formas_pago.set(value=datos_resuventa[7])
        self.strvar_detalle_pago.set(value=datos_resuventa[8])

        # -------------------------------------------------------------------------------
        # 3 - Cargar los articulos que componen la venta de (deta_venta) - items
        datos_detaventa = self.varCotiz.traer_deta_venta(self.strvar_nro_venta.get())

        for row in datos_detaventa:

            # INSERTO ARTICULO EN AUXILIAR DE VENTA (aux_ventas)

            # if self.strvar_combo_tasa_iva.get() == "21.00":
            #     self.strvar_unidad_total_iva_21.set(value=self.strvar_unidad_total_iva.get())
            # elif self.strvar_combo_tasa_iva.get() == "10.50":
            #     self.strvar_unidad_total_iva_105.set(value=self.strvar_unidad_total_iva.get())

            # self.strvar_unidad_costo_bruto_pesos.set(value="0")

            self.varCotiz.insertar_auxventa(row[2],    # codigo de articulo
                                            row[3],    # descripcion de articulo
                                            row[4],    # marca
                                            row[5],    # cantidad vendida
                                            row[6],    # total pesos unidad de contado
                                            row[7],    # total pesos unidad precio de lista
                                            row[8],    # pesos neto por unidad
                                            row[9],    # pesos iva 21 %
                                            row[10],   # pesos iva 10.5
                                            row[11],   # ganancia por unidad
                                            row[12],   # costo bruto por unidad
                                            row[13],   # costo dolar unidad neto
                                            row[14])   # tasa del IVA 21 / 10.5

            self.calcular("totalventa")

        self.limpiar_grid_auxiliar()
        self.llena_grilla_auxiliar(self.clave)

    def fBorro_venta(self):

        # Se borra la venta total - RESU_VENTAS y DETA_VENTAS

        # ------------------------------------------------------------------------------
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
        data = str(self.clave)+" "+valores[0]+" " + valores[2]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar Venta?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        # Elimino de resu_vents y deta_ventas
        self.varCotiz.eliminar_resuventa(self.clave)
        self.varCotiz.eliminar_detaventa(valores[0])

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
        self.limpiar_grid_principal()
        self.llena_grilla_principal(self.clave_ant)

    # ---------------------------------------------------------------------
    # BUSQUEDAS en tabla principal RESU_VENTAS - buscamos una venta ya realizada
    # ---------------------------------------------------------------------

    def fBuscar_resuventa(self):

        if len(self.strvar_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.strvar_buscostring.get()
        self.filtro_activo_resuventa = "resu_ventas WHERE INSTR(rv_cliente, '" + se_busca + "') ORDER BY rv_fecha ASC"

        self.varCotiz.buscar_entabla(self.filtro_activo)
        self.limpiar_grid_principal()
        self.llena_grilla_principal("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_tvw_todaslasventas.selection()
        self.grid_tvw_todaslasventas.focus(item)

    # --------------------------------------------------------------------
    # CALCULOS  Y CONTROL DE VARIABLES
    # --------------------------------------------------------------------

    def calcular(self, que_campo):

        #Esta funcion solo controla todos los Entrys numericos que no contengan el valor "" o mas de un "-" o un "."
        self.control_valores()

        ii = 1
        #try:
        if ii == 1:

            if que_campo == "cantidad":  # Cuando se modifica la cantidad

                # 1 - Precio de lista final venta por cantidad comprada
                self.strvar_xcanti_total_precio_venta_lista.set(
                    value=str(round(float(self.strvar_unidad_precio_venta_lista.get()) *
                    float(self.strvar_cantidad_venta.get()), 2)))
                # 2 - Ganancia por cantidad
                # self.strvar_xcanti_total_ganancia.set(value=str(round(float(self.strvar_unidad_total_ganancia.get()) *
                #                                                   float(self.strvar_cantidad_venta.get()), 2)))

            if que_campo == "precio_lista_unidad":     # Se modifico el precio de venta de lista

                # 1 - Calculo nueva ganancia unidad
                self.strvar_unidad_total_ganancia.set(value=str(round(float(self.strvar_unidad_precio_venta_lista.get()) -
                                                                      float(self.strvar_unidad_costo_bruto_pesos.get()), 2)))

                # calculo nuevo neto unidad
                calcu_nuevo_neto = (float(self.strvar_unidad_precio_venta_lista.get()) /
                                    float((1 + (float(self.strvar_combo_tasa_iva.get()) / 100))))
                self.strvar_unidad_neto_pesos.set(value=str(round(calcu_nuevo_neto, 2)))

                # Importe del IVA unidad Global (para el 21 o el 10,5) segun cual venga es lo mismo
                self.strvar_unidad_total_iva.set(value=str(round(float(self.strvar_unidad_neto_pesos.get()) *
                                                            (float(self.strvar_combo_tasa_iva.get()) / 100), 2)))

                # Asigno el impoprte del IVA segun la TASA
                if self.strvar_combo_tasa_iva.get() == "21.00":
                    self.strvar_unidad_total_iva_21.set(value=str(round((float(self.strvar_unidad_neto_pesos.get()) *
                                                               ((float(self.strvar_combo_tasa_iva.get()) / 100))), 2)))
                else:
                    self.strvar_unidad_total_iva_105.set(value=str(round((float(self.strvar_unidad_neto_pesos.get()) *
                                                               ((float(self.strvar_combo_tasa_iva.get()) / 100))), 2)))

            # 3 - Multiplico nuevos importes por cantidad
            # - Precio final venta por cantidad comprada
            self.strvar_xcanti_total_precio_venta_lista.set(value=str(round(float(
                                                                self.strvar_unidad_precio_venta_lista.get()) *
                                                                float(self.strvar_cantidad_venta.get()), 2)))
            # - Ganancia por cantidad
            # self.strvar_xcanti_total_ganancia.set(value=str(round(float(self.strvar_unidad_total_ganancia.get()) *
            #                                                   float(self.strvar_cantidad_venta.get()), 2)))

            if que_campo == "totalventa":    # Sumariza todos los articulos que estan en auxiliar de ventas

                datos = self.varCotiz.consultar_articulo_item_vta("aux_ventas")

                sumatot = 0
                # sumaiva21 = 0
                # sumaiva105 = 0
                # sumanetos = 0

                for row in datos:

                    sumatot += (row[6] * row[4])   # precio de lista * cantidad
                    # sumaiva21 = sumaiva21 + (row[7] * row[4])
                    # sumaiva105 = sumaiva105 + (row[8] * row[4])
                    # sumanetos = sumanetos + ((row[6]) * row[4])

                self.strvar_global_final_venta.set(value=str(round(sumatot)))
                # self.strvar_global_final_venta_iva21.set(value=round(sumaiva21, 2))
                # self.strvar_global_final_venta_iva105.set(value=round(sumaiva105, 2))
                # self.strvar_global_final_venta_neto.set(value=str(float(sumanetos)))

        else:
        #except:

            messagebox.showerror("Error", "Revise entradas numericas", parent=self)
            return

    # -------------------------------------------------------------------------
    # VALIDACION ENTRADA DE DATOS NUEMRICOS Y FECHAS
    # -------------------------------------------------------------------------

    def control_valores(self):

        # Hago Control (control_forma) de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
        # Tambien todos los demas controles numericos que hacen falta

        self.strvar_unidad_precio_venta_contado.set(value=control_numerico(self.strvar_unidad_precio_venta_contado.get(), "0"))
        self.strvar_unidad_precio_venta_lista.set(value=control_numerico(self.strvar_unidad_precio_venta_lista.get(), "0"))
        self.strvar_unidad_costo_bruto_pesos.set(value=control_numerico(self.strvar_unidad_costo_bruto_pesos.get(), "1"))
        self.strvar_cantidad_venta.set(value=control_numerico(self.strvar_cantidad_venta.get(), "1"))
        self.strvar_unidad_tasa_ganancia.set(value=control_numerico(self.strvar_unidad_tasa_ganancia.get(), "0"))

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_venta.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_venta.get())

        if retorno_VerFal == "":
            self.strvar_fecha_venta.set(value=estado_antes)
            self.entry_fecha_venta.focus()
            return ("error")
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_venta.set(value=estado_antes)
            self.entry_fecha_venta.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_venta.set(value=retorno_VerFal)
        return ("bien")

    # -------------------------------------------------------------------------
    # MOVIMIENTOS EN EL GRID
    # -------------------------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend('TOP')

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview (I001, I002.....
            regis = self.grid_tvw_todaslasventas.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_tvw_todaslasventas.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_tvw_todaslasventas.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_clientes.yview(self.grid_tvw_todaslasventas.index(self.grid_tvw_todaslasventas.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview (I001, I002, ..........
            regis = self.grid_tvw_todaslasventas.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            # barro hasta el ultimo
            for rg in regis:
                continue
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_tvw_todaslasventas.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_tvw_todaslasventas.focus(rg)
            # lleva el foco al final del treeview
            self.grid_tvw_todaslasventas.yview(self.grid_tvw_todaslasventas.index(self.grid_tvw_todaslasventas.get_children()[-1]))

    def fShowall(self):

        self.selected = self.grid_tvw_todaslasventas.focus()
        self.clave = self.grid_tvw_todaslasventas.item(self.selected, 'text')
        self.filtro_activo_resuventa = "resu_ventas ORDER BY rv_fecha"
        self.limpiar_grid_principal()
        self.llena_grilla_principal(self.clave)

    # -------------------------------------------------------------------------
    # CUADROS FRAMES DE PANTALLA
    # -------------------------------------------------------------------------

    def cuadro_botones_grid_principal(self):

        for c in range(7):
            self.frame_botones_grid_principal.grid_columnconfigure(c, weight=1, minsize=120)

        img = Image.open("buscar2.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.lbl_busqueda_venta = Label(self.frame_botones_grid_principal, text=" Venta a buscar: ", justify="left",
                                        bg="light blue", compound="left")
        self.lbl_busqueda_venta.image = icono
        self.lbl_busqueda_venta.config(image=icono)
        self.lbl_busqueda_venta.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_busqueda_venta = Entry(self.frame_botones_grid_principal, textvariable=self.strvar_buscostring,
                                                  state='normal', width=50, justify="left", bg="light blue")
        self.entry_busqueda_venta.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        img = Image.open("buscar2.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_buscar=Button(self.frame_botones_grid_principal, text=" Buscar", command=self.fBuscar_resuventa, width=31,
                               bg='#5F9EA0', fg='white', compound="left")
        self.btn_buscar.image = icono
        self.btn_buscar.config(image=icono)
        self.btn_buscar.grid(row=0, column=2, padx=3, pady=2, sticky=W)

        img = Image.open("ver_todo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_showall=Button(self.frame_botones_grid_principal, text=" Mostrar todo", command=self.fShowall, width=31,
                                bg='#5F9EA0', fg='white', compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=3, pady=2, sticky=W)

        img = Image.open("archivo-nuevo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_nueva_venta=Button(self.frame_botones_grid_principal, text=" Nueva Venta", command=self.fNueva_venta,
                                    width=12, bg='blue', fg='white', compound="left")
        self.btn_nueva_venta.image = icono
        self.btn_nueva_venta.config(image=icono)
        self.btn_nueva_venta.grid(row=0, column=4, padx=3, pady=2, sticky=W)

        img = Image.open("editar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_edito_venta=Button(self.frame_botones_grid_principal, text=" Editar Venta", command=self.fEdito_venta,
                                    width=12, bg='blue', fg='white', compound="left")
        self.btn_edito_venta.image = icono
        self.btn_edito_venta.config(image=icono)
        self.btn_edito_venta.grid(row=0, column=5, padx=3, pady=2, sticky=W)

        img = Image.open("eliminar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_borro_venta=Button(self.frame_botones_grid_principal, text=" Borrar Venta", command=self.fBorro_venta,
                                    width=12, bg='blue', fg='white', compound="left")
        self.btn_borro_venta.image = icono
        self.btn_borro_venta.config(image=icono)
        self.btn_borro_venta.grid(row=0, column=6, padx=3, pady=2, sticky=W)

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_botones_grid_principal, text="", image=self.photo4, command=self.fToparch,
                                 bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=7, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_botones_grid_principal, text="", image=self.photo5, command=self.fFinarch,
                                 bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=8, padx=3, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid_principal.winfo_children():
            widg.grid_configure(padx=3, pady=2, sticky='nsew')

    def cuadro_entrys_cliente(self):

        fff = tkFont.Font(family="Arial", size=8, weight="bold")
        www = tkFont.Font(family="Arial", size=10, weight="bold")

        # NUMERO DE VENTA
        self.strvar_nro_venta.set(value=str(int(self.varCotiz.traer_ultimo(1)) + 1))
        self.lbl_texto_nro_venta = Label(self.frame_entrys_cliente, text="Nº venta: ", font=www, fg="red",
                                         justify="left")
        self.lbl_texto_nro_venta.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_nro_venta = Label(self.frame_entrys_cliente, textvariable=self.strvar_nro_venta, font=www, fg="red",
                                   width=6)
        self.lbl_nro_venta.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        # FECHA DE VENTA
        una_fecha = date.today()
        self.strvar_fecha_venta.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.lbl_texto_fecha_venta = Label(self.frame_entrys_cliente, text="Fecha venta: ", justify="left")
        self.lbl_texto_fecha_venta.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_fecha_venta = Entry(self.frame_entrys_cliente, textvariable=self.strvar_fecha_venta, width=10)
        self.entry_fecha_venta.grid(row=0, column=3, padx=2, pady=2, sticky=W)
        self.entry_fecha_venta.bind("<FocusOut>", self.formato_fecha)

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_entrys_cliente, text="Cliente: ", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_entrys_cliente, textvariable=self.strvar_nombre_cliente, width=52)
        self.entry_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky=W)

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_entrys_cliente, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=6, padx=5, pady=2, sticky='nsew')

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = Label(self.frame_entrys_cliente, text="")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=3, pady=2, sticky=W)
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_entrys_cliente, textvariable=self.strvar_sit_fiscal,
                                                     justify="left", state='readonly', width=25)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky=W)

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = Label(self.frame_entrys_cliente, text="CUIT:", justify="left")
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=2, pady=2, sticky=W)
        self.entry_cuit_cliente = Entry(self.frame_entrys_cliente, textvariable=self.strvar_cuit, justify="right",
                                        width=15)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=2, pady=2, sticky=W)

    def cuadro_entrys_articulo(self):

        for c in range(6):
            self.frame_entrys_articulo.grid_columnconfigure(c, weight=1, minsize=80)

        # Articulo

        # BOTON DE  BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((18, 18), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = Button(self.frame_entrys_articulo, text="", image=self.photo_bus_art, command=self.fBusart,
                                  bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=4, pady=2, sticky=E)

        # ENTRY ARTICULO
        self.lbl_detalle_movim = Label(self.frame_entrys_articulo, text="Articulo: ", justify="left")
        self.lbl_detalle_movim.grid(row=0, column=1, padx=4, pady=2, sticky=W)
        self.entry_detalle_movim = Entry(self.frame_entrys_articulo, textvariable=self.strvar_it_descripcion_articulo,
                                         width=90, justify="left")
        self.entry_detalle_movim.grid(row=0, column=2, padx=4, pady=2, sticky=E)

        # COMBO TASA IVA
        self.lbl_combo_tasa_iva = Label(self.frame_entrys_articulo, justify="left", foreground="black", text="IVA %")
        self.lbl_combo_tasa_iva.grid(row=0, column=3, padx=4, pady=2, sticky=W)
        self.combo_tasa_iva = ttk.Combobox(self.frame_entrys_articulo, textvariable=self.strvar_combo_tasa_iva,
                                           state='readonly', width=8)
        self.combo_tasa_iva['value'] = ["21.00", "10.50"]
        self.combo_tasa_iva.current(0)
        self.combo_tasa_iva.grid(row=0, column=4, padx=4, pady=2, sticky=W)
        #     self.combo_tasa_iva.bind('<Tab>', lambda e: self.calcular("totales_por_item"))

        # COTIZACION DEL DOLAR DEL DIA
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_dolarhoy1 = Label(self.frame_entrys_articulo, text="Dolar hoy:", justify="left", font=fff,
                                   foreground="red")
        self.lbl_dolarhoy1.grid(row=0, column=5, padx=4, pady=2, sticky=W)
        self.lbl_dolarhoy2 = Label(self.frame_entrys_articulo, textvariable=self.strvar_valor_dolar_hoy, width=10,
                                   justify="right", font=fff, foreground="red")
        self.lbl_dolarhoy2.grid(row=0, column=6, padx=4, pady=2, sticky='nsew')

        for widg in self.frame_entrys_articulo.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')

    def cuadro_entrys_importes_articulo(self):

        for c in range(12):
            self.frame_entrys_importes_articulo.grid_columnconfigure(c, weight=1, minsize=50)

        # Precios y cantiodades del articulo

        fff = tkFont.Font(family="Arial", size=10, weight="bold")

        # PRECIO VENTA FINAL UNIDAD LISTA + % recargo tarjeta
        self.lbl_precio_lista_unidad1 = Label(self.frame_entrys_importes_articulo, text=f"Precio LISTA (c/"
                                               f"{self.strvar_tasa_recargo_precio.get()}% rec.)$:", font=fff,
                                              justify="left", fg="green")
        self.lbl_precio_lista_unidad1.grid(row=0, column=0, padx=2, pady=2, sticky=W)

        self.entry_precio_lista_unidad = Entry(self.frame_entrys_importes_articulo, font=fff, width=10,
                                               textvariable=self.strvar_unidad_precio_venta_lista, justify="right")
        self.entry_precio_lista_unidad.grid(row=0, column=1, padx=2, pady=2, sticky='nsew')
        self.entry_precio_lista_unidad.config(validate="key", validatecommand=self.vcmd)
        self.entry_precio_lista_unidad.bind('<Tab>', lambda e: self.calcular("precio_lista_unidad"))

        # PRECIO VENTA FINAL UNIDAD CONTADO
        self.lbl_precio_contado_unidad1 = Label(self.frame_entrys_importes_articulo, text="Contado $:", font=fff,
                                              justify="left")
        self.lbl_precio_contado_unidad1.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.entry_precio_contado_unidad = Label(self.frame_entrys_importes_articulo, font = fff, width=10,
                                               textvariable=self.strvar_unidad_precio_venta_contado, justify="right")
        self.entry_precio_contado_unidad.grid(row=0, column=3, padx=2, pady=2, sticky='nsew')
        # self.entry_precio_venta_unidad.config(validate="key", validatecommand=self.vcmd)
        # self.entry_precio_venta_unidad.bind('<Tab>', lambda e: self.calcular("precio_venta_unidad"))

        # CANTIDAD A COMPRAR DEL ARTICULO
        self.lbl_cantidad_venta = Label(self.frame_entrys_importes_articulo, justify="left", text="Cant.: ", font=fff)
        self.lbl_cantidad_venta.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.entry_cantidad_venta = Entry(self.frame_entrys_importes_articulo, textvariable=self.strvar_cantidad_venta,
                                          width=4, justify="right", font=fff)
        self.entry_cantidad_venta.grid(row=0, column=5, padx=2, pady=2, sticky=W)
        self.entry_cantidad_venta.config(validate="key", validatecommand=self.vcmd)
        self.entry_cantidad_venta.bind('<Tab>', lambda e: self.calcular("cantidad"))

        # CARTEL PRECIO TOTAL
        self.lbl_cartel_total_artiulo = Label(self.frame_entrys_importes_articulo, text="TOTAL $:", justify="left",
                                              font=fff, fg="green")
        self.lbl_cartel_total_artiulo.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        self.lbl_cartel_total_artiulo_xcanti = Label(self.frame_entrys_importes_articulo, font=fff,
                                               textvariable=self.strvar_xcanti_total_precio_venta_lista, width=10,
                                               fg="green", justify="right")
        self.lbl_cartel_total_artiulo_xcanti.grid(row=0, column=7, padx=2, pady=2, sticky='nsew')

        # COSTO UNIDAD BRUTO PESOS
        self.lbl_cartel_total_artiulo = Label(self.frame_entrys_importes_articulo, text="Costo bruto $:",
                                              justify="left", font=fff)
        self.lbl_cartel_total_artiulo.grid(row=0, column=8, padx=2, pady=2, sticky=W)
        self.lbl_cartel_total_artiulo_xcanti = Label(self.frame_entrys_importes_articulo, font=fff, width=10,
                                                textvariable=self.strvar_unidad_costo_bruto_pesos, justify="right")
        self.lbl_cartel_total_artiulo_xcanti.grid(row=0, column=9, padx=2, pady=2, sticky='nsew')

        # GANANCIA UNIDAD PESOS
        self.lbl_cartel_total_artiulo = Label(self.frame_entrys_importes_articulo, text="Ganancia $:", justify="left",
                                              font=fff)
        self.lbl_cartel_total_artiulo.grid(row=0, column=10, padx=2, pady=2, sticky=W)
        self.lbl_cartel_total_artiulo_xcanti = Label(self.frame_entrys_importes_articulo, font =fff, width=10,
                                                textvariable=self.strvar_unidad_total_ganancia, justify="right")
        self.lbl_cartel_total_artiulo_xcanti.grid(row=0, column=11, padx=2, pady=2, sticky='nsew')

        for widg in self.frame_entrys_importes_articulo.winfo_children():
            widg.grid_configure(padx=2, pady=2, sticky='nsew')


        # # TASA GANANCIA
        # self.lbl_tasa_ganancia_unidad1 = Label(self.frame_entrys_importes_articulo, text="% Ganancia unidad : ", justify="left")
        # self.lbl_tasa_ganancia_unidad1.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        # self.entry_tasa_ganancia_unidad2 = Entry(self.frame_entrys_importes_articulo,
        #                                          textvariable=self.strvar_unidad_tasa_ganancia, width=5, justify="right")
        # self.entry_tasa_ganancia_unidad2.grid(row=0, column=3, padx=3, pady=2, sticky='w')
        # self.entry_tasa_ganancia_unidad2.config(validate="key", validatecommand=self.vcmd)
        # self.entry_tasa_ganancia_unidad2.bind('<Tab>', lambda e: self.calcular("tasa_ganancia_unidad"))
        #
        # # GANANCIA
        # self.lbl_ganancia_pesos_unidad1 = Label(self.frame_entrys_importes_articulo, text="Ganancia unidad $: ", justify="left")
        # self.lbl_ganancia_pesos_unidad1.grid(row=1, column=2, padx=2, pady=2, sticky=W)
        # self.entry_ganancia_pesos_unidad2 = Entry(self.frame_entrys_importes_articulo,
        #                                           textvariable=self.strvar_unidad_total_ganancia, width=10,
        #                                           justify="right")
        # self.entry_ganancia_pesos_unidad2.grid(row=1, column=3, padx=3, pady=2, sticky='nsew')
        # self.entry_ganancia_pesos_unidad2.config(validate="key", validatecommand=self.vcmd)
        # self.entry_ganancia_pesos_unidad2.bind('<Tab>', lambda e: self.calcular("importe_ganancia_unidad"))
        #
        # # COSTO PESOS BRUTO UNIDAD
        # self.lbl_costo_pesos_bruto_unidad1 = Label(self.frame_entrys_importes_articulo, text="Costo Bruto $: ", justify="left")
        # self.lbl_costo_pesos_bruto_unidad1.grid(row=2, column=0, padx=2, pady=2, sticky=W)
        # self.lbl_costo_pesos_bruto_unidad2 = Label(self.frame_entrys_importes_articulo,
        #                                            textvariable=self.strvar_unidad_costo_bruto_pesos, state='normal',
        #                                            width=15, justify="right")
        # self.lbl_costo_pesos_bruto_unidad2.grid(row=2, column=1, padx=3, pady=2, sticky='nsew')
        # #self.entry_costo_pesos_bruto_unidad2.config(validate="key", validatecommand=self.vcmd)
        # #self.entry_costo_pesos_bruto_unidad2.bind('<Tab>', lambda e: self.calcular("costo_pesos_bruto"))
        #
        # # COSTO DOLAR UNIDAD
        # self.lbl_total_costodolar_unidad1 = Label(self.frame_entrys_importes_articulo, text="Costo Dolar Bruto U$: ",
        #                                           justify="left")
        # self.lbl_total_costodolar_unidad1.grid(row=2, column=2, padx=2, pady=2, sticky=W)
        # self.lbl_total_costodolar_unidad2 = Label(self.frame_entrys_importes_articulo,
        #                                           textvariable=self.strvar_unidad_costo_dolar_bruto, width=15,
        #                                           justify="right")
        # self.lbl_total_costodolar_unidad2.grid(row=2, column=3, padx=3, pady=2, sticky='nsew')
        #
        # # NETO VENTA UNIDAD
        # self.lbl_total_netoventa_unidad1 = Label(self.frame_entrys_importes_articulo, text="Neto Venta unidad $: ",
        #                                          justify="left")
        # self.lbl_total_netoventa_unidad1.grid(row=0, column=5, padx=2, pady=2, sticky=W)
        # self.lbl_total_netoventa_unidad2 = Label(self.frame_entrys_importes_articulo,
        #                                          textvariable=self.strvar_unidad_neto_pesos, width=15, justify="right")
        # self.lbl_total_netoventa_unidad2.grid(row=0, column=6, padx=3, pady=2, sticky='nsew')
        #
        # # TOTAL IVA
        # self.lbl_totaliva_unidad1 = Label(self.frame_entrys_importes_articulo, text="IVA unidad $: ", justify="left")
        # self.lbl_totaliva_unidad1.grid(row=1, column=5, padx=2, pady=2, sticky=W)
        # self.lbl_totaliva_unidad2 = Label(self.frame_entrys_importes_articulo, textvariable=self.strvar_unidad_total_iva,
        #                                   width=15, justify="right")
        # self.lbl_totaliva_unidad2.grid(row=1, column=6, padx=3, pady=2, sticky='nsew')

    def cuadro_entrys_cuatro(self):

        # Mas datos de venta articulo

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        # TOTAL GANANCIA X CANTIDAD
        self.lbl_ganancia_xcanti1 = Label(self.frame_importes_articulo_dos, text="Total General Ganancia: ", font=fff,
                                          fg="orange",justify="left")
        self.lbl_ganancia_xcanti1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_ganancia_xcanti2 = Label(self.frame_importes_articulo_dos,
                                          textvariable=self.strvar_xcanti_total_ganancia, font=fff, fg="orange",
                                          width=15, justify="right")
        self.lbl_ganancia_xcanti2.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # TOTAL VENTA X CANTIDAD
        self.lbl_total_venta_xcanti1 = Label(self.frame_importes_articulo_dos, text="Total General Venta: ", font=fff,
                                             fg="red", justify="left")
        self.lbl_total_venta_xcanti1.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.lbl_total_venta_xcanti2 = Label(self.frame_importes_articulo_dos,
                                             textvariable=self.strvar_xcanti_total_precio_venta_lista,
                                             font = fff, fg="red", width=15, justify="right")
        self.lbl_total_venta_xcanti2.grid(row=0, column=3, padx=3, pady=2, sticky='nsew')

    def cuadro_botones_aux_ventas(self):

        for c in range(3):
            self.frame_botones_aux_ventas.grid_columnconfigure(c, weight=1, minsize=120)

        img = Image.open("guardar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_cerrar_venta=Button(self.frame_botones_aux_ventas, text=" Cerrar venta actual", width=19,
                                     command=self.fCerrarVenta, bg='green', fg='white', compound="left")
        self.btn_cerrar_venta.image = icono
        self.btn_cerrar_venta.config(image=icono)
        self.btn_cerrar_venta.grid(row=0, column=0, padx=3, pady=2, sticky=W)

        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_reset_venta=Button(self.frame_botones_aux_ventas, text=" Reset Venta", command=self.fReset_venta,
                                    width=19, bg='black', fg='white', compound="left")
        self.btn_reset_venta.image = icono
        self.btn_reset_venta.config(image=icono)
        self.btn_reset_venta.grid(row=0, column=1, padx=3, pady=2, sticky=W)

        img = Image.open("impresora.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_imprime_venta=Button(self.frame_botones_aux_ventas, text=" Imprime Venta", width=19,
                                      command=self.creopdf, bg='#5F9EF5', fg='white', compound="left")
        self.btn_imprime_venta.image = icono
        self.btn_imprime_venta.config(image=icono)
        self.btn_imprime_venta.grid(row=0, column=2, padx=5, pady=2, sticky=W)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_botones_aux_ventas, text="Salir", image=self.photo3, width=85,
                             command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")

        for widg in self.frame_botones_aux_ventas.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_totales_venta(self):

        # TOTAL NETO VENTA ACUMULADO

        for c in range(5):
            self.frame_totales_todo.grid_columnconfigure(c, weight=1, minsize=90)

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_acumulado_neto_venta1 = Label(self.frame_totales_todo, text="Total Venta $: ", font=fff, fg="blue",
                                               justify="left")
        self.lbl_acumulado_neto_venta1.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        self.lbl_acumulado_neto_venta2 = Label(self.frame_totales_todo, textvariable=self.strvar_global_final_venta,
                                                  state='normal', font=fff, fg="blue", width=12, justify="right")
        self.lbl_acumulado_neto_venta2.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # forma de pago y detalle
        self.lbl_combo_formapago = Label(self.frame_totales_todo, text="Forma de Pago: ", justify="left")
        self.lbl_combo_formapago.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        self.combo_formapago = ttk.Combobox(self.frame_totales_todo, textvariable=self.strvar_combo_formas_pago,
                                            state='readonly', width=15)
        self.combo_formapago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                         "Tarjeta Credito", "Cheque"]
        self.combo_formapago.current(0)
        self.combo_formapago.grid(row=0, column=3, padx=4, pady=2, sticky=W)

        self.lbl_deta_formapago = Label(self.frame_totales_todo, text="Detalle: ", justify="left")
        self.lbl_deta_formapago.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        self.entry_deta_formapago = Entry(self.frame_totales_todo, textvariable=self.strvar_detalle_pago, width=75)
        self.entry_deta_formapago.grid(row=0, column=5, padx=4, pady=2, sticky=W)

        for widg in self.frame_totales_todo.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')


        # # TOTAL IVA PESOS ACUMULADO
        # # iva 21%
        # self.lbl_acumulado_totaliva211 = Label(self.frame_totales_todo, text="Total IVA 21%: ", justify="left")
        # self.lbl_acumulado_totaliva211.grid(row=0, column=2, padx=2, pady=2, sticky=W)
        # self.lbl_acumulado_totaliva212 = Label(self.frame_totales_todo, textvariable=self.strvar_global_final_venta_iva21,
        #                                       width=15, justify="right")
        # self.lbl_acumulado_totaliva212.grid(row=0, column=3, padx=3, pady=2, sticky='nsew')
        # # iva 10.5%
        # self.lbl_acumulado_totaliva1051 = Label(self.frame_totales_todo, text="Total IVA 10.5%: ", justify="left")
        # self.lbl_acumulado_totaliva1051.grid(row=0, column=4, padx=2, pady=2, sticky=W)
        # self.lbl_acumulado_totaliva1052 = Label(self.frame_totales_todo,
        #                                         textvariable=self.strvar_global_final_venta_iva105, width=15,
        #                                         justify="right")
        # self.lbl_acumulado_totaliva1052.grid(row=0, column=5, padx=3, pady=2, sticky='nsew')
        #
        # # TOTAL VENTA PESOS ACUMULADO
        # self.lbl_acumulado_totalventa1 = Label(self.frame_totales_todo, text="Total Venta: ", justify="left")
        # self.lbl_acumulado_totalventa1.grid(row=0, column=6, padx=2, pady=2, sticky=W)
        # self.lbl_acumulado_totalventa2 = Label(self.frame_totales_todo, textvariable=self.strvar_global_final_venta,
        #                                       width=15, justify="right")
        # self.lbl_acumulado_totalventa2.grid(row=0, column=7, padx=3, pady=2, sticky='nsew')

        # for widg in self.frame_totales_todo.winfo_children():
        #     widg.grid_configure(padx=10, pady=3, sticky='nsew')

    def cuadro_botones_articulo(self):

        for c in range(3):
            self.frame_botones_articulo.grid_columnconfigure(c, weight=1, minsize=120)

        img = Image.open("guardar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_ingresar_itemventa=Button(self.frame_botones_articulo, text=" Ingresar articulo a venta", width=19,
                                 command=self.fInsertar_item_venta_auxiliar, bg='#5F9EA0', fg='white', compound="left")
        self.btn_ingresar_itemventa.image = icono
        self.btn_ingresar_itemventa.config(image=icono)
        self.btn_ingresar_itemventa.grid(row=0, column=0, padx=3, pady=2, sticky=W)

        img = Image.open("eliminar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_eliminar_itemventa=Button(self.frame_botones_articulo, text=" Quitar articulo de venta", width=19,
                                 command=self.fQuitar_item_venta_auxiliar, bg='#5F9EA0', fg='white', compound="left")
        self.btn_eliminar_itemventa.image = icono
        self.btn_eliminar_itemventa.config(image=icono)
        self.btn_eliminar_itemventa.grid(row=0, column=1, padx=3, pady=2, sticky=W)

        img = Image.open("reset.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_reset_art=Button(self.frame_botones_articulo, text=" Reset Articulo", command=self.fReset_articulo,
                                  width=19, bg='black', fg='white', compound="left")
        self.btn_reset_art.image = icono
        self.btn_reset_art.config(image=icono)
        self.btn_reset_art.grid(row=0, column=2, padx=3, pady=2, sticky=W)

        for widg in self.frame_botones_articulo.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    # --------------------------------------------------------------------------
    # CUADRO SELECCION DE ITEMS - SEL
    # --------------------------------------------------------------------------

    def fBuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
            en que campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a Funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de como 
            quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                        "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
            los Entrys correspondientes """

        for item in valores_new:
            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])
            #self.strvar_cli_datosmas.set(value=str(item[4] + ' - tel: ' + item[8] + ' / ' + item[9]))

        #self.strvar_cli_deuda.set(value=str(self.fTraedeuda(self.strvar_codigo_cliente.get())))
        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    def fBusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.strvar_it_descripcion_articulo.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.strvar_it_descripcion_articulo.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.strvar_it_descripcion_articulo.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.strvar_it_descripcion_articulo.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.varFuncion_new.ventana_selec("articulos", "descripcion", "marca",
                                                        "costodolar", "Descripcion", "Marca",
                                                        "Precio dolar neto", que_busco,
                                                        "Orden: Rubro+Marca+Descripcion", "S")

        masiva = 0
        masganancia = 0

        for item in valores_new:

            # -------------------------------------------------------------
            # PROPIEDADES ARTICULO - descripcion del articulo - %IVA
            self.strvar_it_codigo_articulo.set(value=item[1])
            self.strvar_it_descripcion_articulo.set(value=item[2])
            self.strvar_it_marca_articulo.set(value=item[3])
            self.strvar_unidad_costo_dolar.set(value=item[6])
            self.strvar_combo_tasa_iva.set(value=item[7])
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # CACULOS - calculo neto_pesos : neto mas el iva : neta ma iva mas ganancia = precio de venta por unidad
            # costo neto
            costopesos_neto = round((float(self.strvar_valor_dolar_hoy.get()) * float(item[6])), 2)
            # costo bruto
            costo_neto_masiva = round((float(costopesos_neto) * (1 + ((float(item[7]) / 100)))), 2)
            # precio de venta contado
            costo_masiva_masganancia = round((float(costo_neto_masiva) * (1 + ((float(item[9]) / 100)))), 2)
            # precio de venta lista (mas el % de recargo con tarjeta activo
            precio_venta_lista = costo_masiva_masganancia * (1 + (float(self.strvar_tasa_recargo_precio.get()) / 100))
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # PRECIO VENTA x unidad Y x cantidad Lista y contado - redondeados
            self.strvar_unidad_precio_venta_lista.set(value=str(round(precio_venta_lista)))
            self.strvar_unidad_precio_venta_contado.set(value=str(round(costo_masiva_masganancia)))
            self.strvar_xcanti_total_precio_venta_lista.set(value=self.varFuncion_new.formatear_cifra(round(precio_venta_lista *
                                                                            float(self.strvar_cantidad_venta.get()))))
            self.strvar_unidad_costo_bruto_pesos.set(value=str(round(costo_neto_masiva)))
            # -------------------------------------------------------------

            # -------------------------------------------------------------
            # GANANCIA - (% ganancia) y (ganancia por unidad y  por cantidad)
            self.strvar_unidad_tasa_ganancia.set(value=item[9])
            self.strvar_unidad_total_ganancia.set(value=str(round(precio_venta_lista - costo_neto_masiva)))
            # -------------------------------------------------------------

            #self.strvar_xcanti_total_ganancia.set(value=str(float(self.strvar_unidad_total_ganancia.get()) *
            #                                                float(self.strvar_cantidad_venta.get())))

            # -------------------------------------------------------------
            # costos - costo en pesos por unidad
            self.strvar_unidad_neto_pesos.set(value=str(costopesos_neto))
            # -------------------------------------------------------------

            self.entry_precio_lista_unidad.focus_set()
            self.entry_precio_lista_unidad.selection_range(0, tk.END)  # selecciona el texto

            # # -------------------------------------------------------------------
            # # costo en pesos sin impuesto NETO unidad -
            # # (costo neto en dolares del articulo * valor dolar pesos del dia)
            # var_calculo = round(float(item[6]) * float(self.strvar_valor_dolar_hoy.get()), 2)
            # self.strvar_it_costo_pesos_neto.set(value=var_calculo)
            # # -------------------------------------------------------------------


        #self.strvar_it_costo_pesos_neto.set(value=costopesos_neto)
        #self.strvar_costo.set(value=masiva)

        # self.entry_detalle_movim.focus()
        # self.entry_detalle_movim.icursor(tk.END)

        # if len(self.strvar_detalle_articulo.get()) < 3:
        #     messagebox.showwarning("Aviso", "Falta argumento de busqueda minimo tres caracteres", parent=self)
        #     self.entry_detalle_articulo.focus()
        #     return


    # -----------------------------------------------------------------------------------
    # GRIDS
    # -----------------------------------------------------------------------------------

    def cuadro_grid_auxiliar_venta(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_auxiliar_venta)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_auxiliar_venta = ttk.Treeview(self.frame_grid_auxiliar_venta, height=4, columns=("col1", "col2",
                                            "col3", "col4", "col5", "col6", "col7", "col8"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        self.grid_tvw_auxiliar_venta.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_tvw_auxiliar_venta.column("col1", width=80, anchor="w", minwidth=80)
        self.grid_tvw_auxiliar_venta.column("col2", width=430, anchor="w", minwidth=430)
        self.grid_tvw_auxiliar_venta.column("col3", width=110, anchor="center", minwidth=110)
        self.grid_tvw_auxiliar_venta.column("col4", width=60, anchor="center", minwidth=60)
        self.grid_tvw_auxiliar_venta.column("col5", width=130, anchor="center", minwidth=130)
        self.grid_tvw_auxiliar_venta.column("col6", width=70, anchor="center", minwidth=70)
        self.grid_tvw_auxiliar_venta.column("col7", width=70, anchor="center", minwidth=70)
        self.grid_tvw_auxiliar_venta.column("col8", width=70, anchor="center", minwidth=70)

        self.grid_tvw_auxiliar_venta.heading("#0", text="Id", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col1", text="Codigo", anchor="w")
        self.grid_tvw_auxiliar_venta.heading("col2", text="Descripcion", anchor="w")
        self.grid_tvw_auxiliar_venta.heading("col3", text="Marca", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col4", text="Cant", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col5", text="Precio contado unidad", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col6", text="Precio lista unidad", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col7", text="Costo dolar", anchor="center")
        self.grid_tvw_auxiliar_venta.heading("col8", text="Tasa IVA", anchor="center")

        self.grid_tvw_auxiliar_venta.tag_configure('oddrow', background='light grey')
        self.grid_tvw_auxiliar_venta.tag_configure('evenrow', background='light blue')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_grid_auxiliar_venta, orient="horizontal")
        scroll_y = Scrollbar(self.frame_grid_auxiliar_venta, orient="vertical")
        self.grid_tvw_auxiliar_venta.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_auxiliar_venta.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_auxiliar_venta.xview)
        scroll_y.config(command=self.grid_tvw_auxiliar_venta.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_tvw_auxiliar_venta['selectmode'] = 'browse'
        self.grid_tvw_auxiliar_venta.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def cuadro_grid_ventas_realizadas(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_ventas_realizadas)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_tvw_todaslasventas = ttk.Treeview(self.frame_grid_ventas_realizadas, height=4, columns=("col1", "col2",
                                                                                    "col3", "col4", "col5","col6"))

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
        scroll_x = Scrollbar(self.frame_grid_ventas_realizadas, orient="horizontal")
        scroll_y = Scrollbar(self.frame_grid_ventas_realizadas, orient="vertical")
        self.grid_tvw_todaslasventas.config(xscrollcommand=scroll_x.set)
        self.grid_tvw_todaslasventas.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_tvw_todaslasventas.xview)
        scroll_y.config(command=self.grid_tvw_todaslasventas.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_tvw_todaslasventas['selectmode'] = 'browse'

        self.grid_tvw_todaslasventas.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def DobleClickGrid(self, event):
        self.fEdito_venta()

    # -------------------------------------------------------------------------
    # INFORMES
    # -------------------------------------------------------------------------

    def creopdf(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_tvw_auxiliar_venta.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_tvw_auxiliar_venta.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # Traer todos los registros de la tabla de articulos vendidos
        self.datos_articulos_vendidos = self.varCotiz.consultar_detalle_auxventas("aux_ventas")

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
        self.pdf_numero_venta = self.strvar_nro_venta.get()
        self.pdf_codigo_cliente = self.strvar_codigo_cliente.get()
        self.pdf_nombre_cliente = self.strvar_nombre_cliente.get()

        #str(self.datos_articulos_vendidos[1])
        # self.pdf_nombre_cliente = datos_registro_selec[5]
        self.pdf_datos_encabezado_orden = self.pdf_numero_venta+' - '+self.pdf_nombre_cliente+' ( '+self.pdf_codigo_cliente+' )'
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
        # retorno una lista con los registros
        # datos = self.varOrdenes.consultar_orden("")
        sumotot = 0
        for row in self.datos_articulos_vendidos:
            # Descripcion articulo
            pdf.cell(w=120, h=5, txt=row[2], border=0, align='L', fill=0, ln=0)
            # Marca
            pdf.cell(w=20, h=5, txt=row[3], border=0, align='L', fill=0, ln=0)
            # Total pesos del articulo
            pdf.cell(w=0, h=5, txt=str(row[4]), border=0, align='R', fill=0, ln=1)
            sumotot += row[4]

        # Total
        pdf.cell(w=0, h=5, txt="Total: " + str(sumotot), border=0, align='R', fill=0, ln=1)

            # mostrar = row[4]
            # cadena = (mostrar[:100])
            # pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0)

        pdf.output('hoja.pdf')

        # # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

