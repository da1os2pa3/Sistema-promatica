import os
import tkinter as tk
import tkinter.font as tkfont
from datetime import date
from tkinter import ttk
from tkinter.scrolledtext import *  # para campos text
from PIL import Image, ImageTk
from PDF_clase import PDF
from articulos import ClaseArticulos
from funcion_new import ClaseFuncionNew
from funciones import *
from presup_nuevo_ABM import DatosPresupuestos
from status_bar import StatusBar


class ClasePresupuestos(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=520)
        self.master = master
        self.status = StatusBar(self.master)

        # --------------------------------------------------------------------------
        # PANTALLA
        # --------------------------------------------------------------------------
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """

        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()
        # Asigno fijo un ancho y un alto
        ancho_ventana = 1045
        alto_ventana = 670
        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # -------------------------------------------------------------------------

        # Otros ajuste para las pestañas ------------------------------------------
        style = ttk.Style()
        style.theme_use('clam')
        # Bajamos de 230 a 216 para darles el tamaño justo sin que se corten
        style.configure('TNotebook.Tab', padding=[227, 8, 227, 8], font=('Arial', 10, 'bold'))
        # Mantenemos el bloqueo del estado seleccionado con el nuevo número
        style.map('TNotebook.Tab', padding=[('selected', [227, 8, 227, 8])])
        # -----------------------------------------------------------------------

        # CONFIGURACIÓN DE COLOR SEGURA -----------------------------------------
        # Usamos el gris claro estándar directamente para no romper el layout
        style.configure('TNotebook.Tab', background='#a0a0a0')
        style.map('TNotebook.Tab', background=[('selected', '#f0f0f0'), ('active', '#f0f0f0')])
        # -----------------------------------------------------------------------

        # Instanciaciones -------------------------------------------------------
        self.var_obj_presup = DatosPresupuestos(self.master)
        self.var_obj_funcionnew = ClaseFuncionNew(self.master)
        # -----------------------------------------------------------------------

        # Variables uso compartido en pestanas ----------------------------------
        self.sv_nro_presup = tk.StringVar(value="0")
        self.sv_fecha_presup = tk.StringVar(value="")
        self.sv_valor_dolar_presup = tk.StringVar(value="0.00")
        self.sv_valor_dolar_oficial_hoy = tk.StringVar(value="0.00")
        self.sv_tasa_ganancia = tk.StringVar(value="0.00")
        # variables de totales generales
        self.sv_total_presup = tk.StringVar(value="0.00")
        self.sv_total_item_redondo = tk.StringVar(value="0.00")
        self.sv_total_ganancia = tk.StringVar(value="0.00")
        self.sv_total_costos = tk.StringVar(value="0.00")
        self.sv_total_presup_redondo = tk.StringVar(value="0.00")
        # ----------------------------------------------------------------------

        # Pestañas --------------------------------------------------------------
        # 1. Crear el contenedor de pestañas (Notebook) usando self.master
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both")
        # -----------------------------------------------------------------------

        # 2. Instanciar las pestañas --------------------------------------------
        #self.pestana_1 = PestanaUno(self.notebook, funciones=self.var_obj_funcionnew, datos=self.varCotiz)
        """ Paso en "self" la clase "VentasPrincipal", asi puedo definir en esta clase todas las funciones y
            variables Que quiera compartir en las dos pestañas"""
        self.pestana_1 = ClasePestanaUno(self.notebook, self) # self seria "clase ventas principal"
        self.pestana_2 = ClasePestanaDos(self.notebook, self)
        # -----------------------------------------------------------------------ººº

        # 3. Añadir las pestañas al contenedor ----------------------------------
        self.notebook.add(self.pestana_1, text="Encabezado")
        self.notebook.add(self.pestana_2, text="Detalle")
        # -----------------------------------------------------------------------

        # Funciones compartidas -------------------------------------------------
        self.traer_dolarhoy()
        self.estado_inicial_general()

    # -----------------------------------------------------------------------
    # Funciones definidas en la clase principal
    # -----------------------------------------------------------------------

    def estado_inicial_general(self):

        self.pestana_1.festado_inicial_uno()
        self.pestana_2.festado_inicial_dos()

    def traer_dolarhoy(self):

        # ----------------------------------------------------------
        try:
            dev_informa = self.var_obj_presup.consultar_informa()
        except Exception:
            self.var_obj_funcionnew.mostrar_error()
            return
        # ----------------------------------------------------------

        for row in dev_informa:
            self.sv_valor_dolar_presup.set(value=row[21])
            self.sv_valor_dolar_oficial_hoy.set(value=row[21])
            # self.sv_tasa_recargo_precio.set(value=row[23])

    def fcancela_presup(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return
        self.estado_inicial_general()

    def cargar_icono(self, path, size=(18, 18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    def fsalir(self):
        self.winfo_toplevel().destroy()





# =========================================================================================
# PESTAÑA UNO
# =========================================================================================

class ClasePestanaUno(tk.Frame):

    # def __init__(self, master=None, funciones=None, datos=None):
    def __init__(self, parent, principal):
        super().__init__(parent)

        # Creo instancia de clase principal - Instancio directamente toda la clase principal
        # y comparto variables y funciones definidas en ella
        self.principal = principal

        # =STRINGVARS= usadas en la pestaña uno -------------------------------
        # Datos de la venta y datos del cliente
        self.sv_codigo_cliente = tk.StringVar(value="0")
        self.sv_nombre_cliente = tk.StringVar(value="Consumidor Final")
        self.sv_sit_fiscal = tk.StringVar(value="")
        self.sv_cuit = tk.StringVar(value="")
        # Tipos de pago
        self.sv_combo_formas_pago = tk.StringVar()
        self.sv_detalle_pago = tk.StringVar(value="")
        self.sv_aceptado = tk.StringVar(value="0")
        # Busquedas
        self.sv_buscostring = tk.StringVar(value="")
        # ---------------------------------------------------------------------

        # Ejecutamos tu secuencia de inicialización adaptada a la Pestaña 1 ---
        self.create_widgets()
        self.festado_inicial_uno()
        # self.fllena_grilla_presupuestos("")
        # ---------------------------------------------------------------------

    def create_widgets(self):

        # VARIABLES GENERALES -------------------------------------------------
        # para validar ingresos de numeros en gets numericos
        # "Tkinter, registrame esta función porque después
        # quiero que vos la llames."
        self.vcmd = (self.register(self.principal.var_obj_funcionnew.validar), "%P")
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # CUADROS
        # ---------------------------------------------------------------------
        self.frame_principal = tk.LabelFrame(self, text="", foreground="#CD5C5C")
        self.frame_principal.pack(expand=True, fill="both", padx=5, pady=5)

        # CUADRO GRID DE PRESUPUESTOS ENTREGADOS  ------------------------------
        # Grid donde se ven los resumenes de los persupuestos entregados
        self.frame_grid_presupuestos=tk.LabelFrame(self.frame_principal, text="Presupuesto entregados",
                                                   foreground="#CD5C5C")
        self.fcuadro_grid_presupuestos()
        self.frame_grid_presupuestos.pack(side="top", fill="both", padx=5, pady=5)
        # ----------------------------------------------------------------------

        # CUADRO BUSQUEDA_PRESUPUESTOS -----------------------------------------
        self.frame_busqueda_presupuestos=tk.LabelFrame(self.frame_principal, text="", border=5, foreground="black",
                                                       background="light blue")
        self.fcuadro_buscar_presupuestos()
        self.frame_busqueda_presupuestos.pack(expand=0, side="top", fill="both", padx=5, pady=10)
        # ----------------------------------------------------------------------

        # CUADRO ENTRYS tasa ganancia y valor dolar para operacion actual ------
        self.frame_ganancia = tk.LabelFrame(self.frame_principal, text="", bg="#81EBCD", borderwidth=2, relief="solid",
                                            highlightbackground="blue")
        self.entry_ganancia()
        self.frame_ganancia.pack(side="top", fill="both", expand=0, padx=5, pady=3)
        # ----------------------------------------------------------------------

        # CUADRO ENTRYS DATOS DEL CLIENTE --------------------------------------
        self.frame_cliente = tk.LabelFrame(self.frame_principal, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                           highlightbackground="blue" )
        self.fcuadro_entrys_datos_cliente()
        self.frame_cliente.pack(side="top", fill="both", expand=0, padx=5, pady=3)
        # ----------------------------------------------------------------------

        # CUADRO ENTRYS FORMA DE PAGO ------------------------------------------
        self.frame_forma_pago = tk.LabelFrame(self.frame_principal, text="", bg="#CEF2EF", borderwidth=2, relief="solid",
                                              highlightbackground="blue")
        self.fentrys_formas_pago()
        self.frame_forma_pago.pack(side="top", fill="both", expand=0, padx=5, pady=3)
        # ----------------------------------------------------------------------

        # CUADRO BOTONES CRUD Y MOV GRIDPRESUPUESTOS ---------------------------
        self.frame_botones_uno_grid_presupuestos = tk.LabelFrame(self.frame_principal, text="", bg="#CD5C5C")
        self.fcuadro_botones__uno_grid_presupuestos()
        self.frame_botones_uno_grid_presupuestos.pack(side="top", fill="both", padx=5, pady=10)
        # ----------------------------------------------------------------------

        # CUADRO TOTALES GENERALES ---------------------------------------------
        self.frame_totales_generales = tk.LabelFrame(self.frame_principal, text="", foreground="black", border=5,
                                                     relief="ridge")
        self.fcuadro_totales_generales()
        self.frame_totales_generales.pack(side="top", fill="both", expand=0, padx=5, pady=3)
        # ----------------------------------------------------------------------

        # CUADRO BOTONES CERRAR PRESUPUESTO O CANCELAR -------------------------
        self.frame_cerrar_cancelar = tk.LabelFrame(self.frame_principal, text="", foreground="black", border=5,
                                                   relief="ridge")
        self.fcuadro_cerrar_cancelar()
        self.frame_cerrar_cancelar.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------


    # ---------------------------------------------------------------------
    # Configuracion inicial
    # ---------------------------------------------------------------------

    def festado_inicial_uno(self):

        self.filtro_activo_presupuestos = "ORDER BY rp_fecha, rp_numero ASC"
        # self.alta_modif_presup = 0      # tabla resu_presu

        # limpia todos los entrys - borro los datos que puedan tener
        self.flimpiar_entrys_uno()
        # preparo fecha del presupuesto - paso a string
        una_fecha = date.today()
        self.principal.sv_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))
        # desactivo todos los entrys
        self.estado_entrys_crud_uno("disabled")
        # Limpiamos los totales globales del presupuesto
        self.flimpiar_totales_finales()
        # Activo los botones del CRUD principal - Nuevo-Edito_Borro presupuesto
        self.estado_botones_uno("normal")

        # --------------------------------------------------------
        try:
            # Vacio el GRID auxiliar (auxpresup) - donde cargo los componentes
            self.principal.var_obj_presup.vaciar_auxpresup()
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # --------------------------------------------------------

        self.fllena_grilla_presupuestos("")

    def estado_entrys_crud_uno(self, estado):

        """ Estado inicial de los entrys - cliente y componentes - solo se ejecuta una vez al entrar al modulo """

        self.entry_fecha_presup.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.combo_sit_fiscal_cliente.configure(state=estado)
        self.entry_cuit_cliente.configure(state=estado)

        self.entry_dolarhoy2.configure(state=estado)
        self.entry_tasa_ganancia.configure(state=estado)

        self.combo_formapago.configure(state=estado)
        self.entry_deta_formapago.configure(state=estado)
        self.btn_busco_cliente.configure(state=estado)

    def flimpiar_entrys_uno(self):

        """ Limpia totdos los e Entrys - se usa en inicial y para cancelar """

        una_fecha = date.today()
        self.principal.sv_fecha_presup.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.sv_nombre_cliente.set(value="Consumidor Final")
        self.sv_codigo_cliente.set(value="0")
        self.combo_sit_fiscal_cliente.current(0)
        self.sv_cuit.set(value="")
        self.combo_formapago.current(0)
        self.sv_detalle_pago.set(value="")
        self.principal.sv_tasa_ganancia.set(value="0.00")
        self.principal.traer_dolarhoy()
        self.sv_aceptado.set(value="0")
        # self.principal.sv_valor_dolar_presup.set(value="0.00")

    def flimpiar_totales_finales(self):

        self.principal.sv_total_presup.set(value="0.00")
        self.principal.sv_total_item_redondo.set(value="0.00")
        self.principal.sv_total_ganancia.set(value="0.00")
        self.principal.sv_total_costos.set(value="0.00")
        self.principal.sv_total_presup_redondo.set(value="0.00")

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
        self.btn_imprime_presup.configure(state=estado)
        #self.btn_imprime_presup_ext.configure(state=estado)
        self.entry_busqueda_presup.configure(state=estado)

    def fllena_grilla_presupuestos(self, set_foco):

        # Limpio el grid
        for item in self.grid_presupuestos.get_children():
            self.grid_presupuestos.delete(item)

        try:

            datos = self.principal.var_obj_presup.consultar_presupuestos("resu_presup", self.filtro_activo_presupuestos)

            cont = 0
            for row in datos:

                cont += 1
                color = ('evenrow',) if cont % 2 else ('oddrow',)

                # Para cambiar el color si el presupuesto es aceptado
                if row[14] == "1":
                    color = ("error",)

                """ Este es el ejemplo por si quiero destacar alguna linea segun alguna condicion especial, por
                    ejemplo 'presupuesto realizado - Si un columna coincide con un valor buscado, cambie el color'
                    if row[1] == 2324:
                        color = ("error",)
                    Va combinado con la siguiente linea, que hay que ponerla en el llena_grilla
                    self.grid_clientes.tag_configure('error', background='green')
                    va debajo de los otros dos configure de odorow y everrow """

                # convierto fecha de 2024-12-19 a 19/12/2024
                # fecha_forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'), False)
                fecha_forma_normal = self.principal.var_obj_funcionnew.fecha_es(datetime.strftime(row[2], '%Y-%m-%d'))

                self.grid_presupuestos.insert("", "end", tags=color, text=row[0], values=(row[1],
                                                    fecha_forma_normal, row[4], row[7], row[8], row[9], row[10]))

            # Controles --------------------------------------------------------
            # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
            children = self.grid_presupuestos.get_children()
            # Si no hay filas (grid vacio), salgo sin intentar seleccionar
            if not children:
                self.principal.status.set_status("ℹ Grid vacio...", "info")
                return

            # Si el parametro set_foco esta vacío (no hay foco), voy al ultimo de la grilla,
            # caso contrario, voy a la clave que se haya enviado en set_foco para dejar el puntero.
            if not set_foco:
                # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
                posicion = children[-1]                      # ultimo
                # posicion = children[0]                     # primero
                self.grid_presupuestos.focus_set()
                self.grid_presupuestos.focus(posicion)
                self.grid_presupuestos.selection_set(posicion)
                self.grid_presupuestos.see(posicion)
            else:
                for item in children:
                    texto = self.grid_presupuestos.item(item, "text")
                    # print(str(set_foco) + " " + str(texto))
                    if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                        self.grid_presupuestos.update_idletasks()
                        self.grid_presupuestos.focus_set()
                        self.grid_presupuestos.selection_set(item)
                        self.grid_presupuestos.focus(item)
                        self.grid_presupuestos.see(item)
                        break

        except Exception:

            self.principal.var_obj_funcionnew.mostrar_error("Fallo en carga de GRID resu_presup")
            return


    # ----------------------------------------------------------------------------
    # BOTONES CRUD - NUEVOS PRESUPUESTOS
    # ----------------------------------------------------------------------------

    def fnuevo_presupuesto(self):

        # self.alta_modif_presup = 1
        self.estado_entrys_crud_uno("normal")
        self.estado_botones_uno("disabled")
        self.principal.pestana_2.estado_botones_dos("normal")
        self.flimpiar_entrys_uno()
        self.principal.sv_nro_presup.set(value=str(int(self.principal.var_obj_presup.traer_ultimo(1)) + 1))
        self.entry_fecha_presup.focus()

    def fedito_presupuesto(self):

        # -------------------------------------------------------------------
        self.selected = self.grid_presupuestos.focus()
        self.clave = self.grid_presupuestos.item(self.selected, 'text')
        # -------------------------------------------------------------------

        if not self.clave:
            self.principal.status.set_status("ℹ No hay nada seleccionado...", "info")
            return

        self.estado_entrys_crud_uno("normal")
        self.estado_botones_uno("disabled")
        self.flimpiar_entrys_uno()
        self.principal.pestana_2.estado_botones_dos("normal")
        self.entry_fecha_presup.focus()

        # Vacio tabla auxilliar ---------------------------------------------
        try:
            self.principal.var_obj_presup.vaciar_auxpresup()
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -------------------------------------------------------------------

        #self.alta_modif_presup = 2

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_presupuestos.item(self.selected, 'values')
        self.principal.sv_nro_presup.set(value=valores[0])

        # -------------------------------------------------------------------
        try:
            # 2 - Cargar los datos encabezado de la venta (cliente, fecha....) de Resu_Venta
            datos_presu_entregado = self.principal.var_obj_presup.traer_resu_presup(self.principal.sv_nro_presup.get())
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -------------------------------------------------------------------

        fechapaso = datos_presu_entregado[2].strftime('%d/%m/%Y')
        self.principal.sv_fecha_presup.set(fechapaso)
        self.sv_codigo_cliente.set(value=datos_presu_entregado[3])
        self.sv_nombre_cliente.set(value=datos_presu_entregado[4])
        self.sv_sit_fiscal.set(value=datos_presu_entregado[5])
        self.sv_cuit.set(value=datos_presu_entregado[6])
        self.principal.sv_valor_dolar_presup.set(value=datos_presu_entregado[7])
        self.principal.sv_tasa_ganancia.set(value=datos_presu_entregado[8])
        self.principal.sv_total_presup_redondo.set(value=datos_presu_entregado[10])
        self.sv_combo_formas_pago.set(value=datos_presu_entregado[11])
        self.sv_detalle_pago.set(value=datos_presu_entregado[12])
        self.sv_aceptado.set(value=datos_presu_entregado[14])
        self.principal.pestana_2.text_especificaciones.configure(state="normal")
        self.principal.pestana_2.text_especificaciones.insert("end", datos_presu_entregado[13])
        self.principal.pestana_2.text_especificaciones.configure(state="disabled")
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        try:
            # 3 - Cargar los componentes del presupuesto de deta_presup
            datos_detapresup = self.principal.var_obj_presup.traer_deta_presup(self.principal.sv_nro_presup.get())
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

        for row in datos_detapresup:

            # -----------------------------------------------------------------
            dolar_a_pesos = float(row[8]) * float(self.principal.sv_valor_dolar_presup.get())
            iva_a_cargar = dolar_a_pesos * (float(row[6]) / 100)
            ganancia_a_cargar = (dolar_a_pesos + iva_a_cargar) * (float(self.principal.sv_tasa_ganancia.get()) / 100)
            total_presupuesto = dolar_a_pesos + iva_a_cargar + ganancia_a_cargar
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            dic_deta_auxpresup = {
                "Id": row[0],                              # Id
                "ax_orden": row[1],                        # orden elemento
                "ax_proved": row[3],                       # nombre del proveedor
                "ax_codcomp": row[4],                      # codigo componente del proveedor
                "ax_componente": row[5],                   # descripcion del componente
                "ax_iva": row[6],                          # tasa iva del componente
                "ax_cantidad": row[7],                     # cantidad del componente
                "ax_neto_dolar": row[8],                   # costo neto componente en dolares
                "ax_total_presup": total_presupuesto,      # total del presupuesto real
                "ax_total_redondo": row[9],                # total en pesos redondeo
                "ax_total_ganancia": ganancia_a_cargar,    # total ganancia
                "ax_total_costos": dolar_a_pesos           # total costos
            }
            # -----------------------------------------------------------------

            # -----------------------------------------------------------------
            try:
                # Insertar registro en aux_presup
                self.principal.var_obj_presup.insertar_auxpresup(dic_deta_auxpresup)
            except Exception:
                self.principal.var_obj_funcionnew.mostrar_error()
                return
            # -----------------------------------------------------------------

        self.principal.pestana_2.calcular("totalpresupuesto")
        self.principal.pestana_2.llena_grilla_auxiliar("")

    def fborro_presupuesto(self):

        # ----------------------------------------------------------------------
        # selecciono el Id del grid para su uso posterior
        self.selected = self.grid_presupuestos.focus()
        self.selected_ant = self.grid_presupuestos.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no son el mismo)
        self.clave = self.grid_presupuestos.item(self.selected, 'text')
        self.clave_ant = self.grid_presupuestos.item(self.selected_ant, 'text')
        # ----------------------------------------------------------------------

        if self.clave == "":
            self.principal.status.set_status("❌ No hay nada seleccionador", "error")
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_presupuestos.item(self.selected, 'values')
        data = " Presupuesto Nº " + valores[0] + " de " + valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar presupuesto?\n " + data, parent=self)
        if r == messagebox.NO:
            self.principal.status.set_status("🗑 operacion cancelada", "")
            return

        # Elimino de resu_ventas y deta_ventas ----------------------------------------
        try:
            self.principal.var_obj_presup.eliminar_presu_entregado1(self.clave)
            self.principal.var_obj_presup.eliminar_detapresup(valores[0])  # por numero de venta
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -----------------------------------------------------------------------------

        self.principal.status.set_status("✔ Registro eliminado correctamente", "ok")
        self.fllena_grilla_presupuestos(self.clave_ant)

    def fpresupuesto_aceptado(self):

        # ----------------------------------------------------------------------
        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_presupuestos.focus()
        # guardo en clave el Id pero de la tabla (no son el mismo)
        self.clave = self.grid_presupuestos.item(self.selected, 'text')
        # ----------------------------------------------------------------------

        if self.clave == "":
            self.principal.status.set_status("❌ No hay nada seleccionador", "error")
            return

        # -----------------------------------------------------------------------
        try:
            # consulto registro en la tabla para saber el estado de la marca de aceptado (si esta ya aceptadoo o no)
            datos = self.principal.var_obj_presup.consultar_presupuestos("resu_presup",
                                                                         f"resu_presup WHERE id={self.clave}")
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ------------------------------------------------------------------------

        # si esta marcado como aceptado lo cambio a no aceptado y a la inversa
        marca_aceptado = "0"
        for i in datos:
            if i[14] == "0":
                marca_aceptado = "1"

        # guardo todos los valores en una lista desde el Grid
        valores = self.grid_presupuestos.item(self.selected, 'values')
        #        data = str(self.clave)+" "+valores[0]+" " + valores[2]
        data = " Presupuesto Nº " + valores[0] + " de " + valores[2]

        r = messagebox.askquestion("", "Confirma cambio de estado presupuesto?\n " + data, parent=self)
        if r == messagebox.NO:
            self.principal.status.set_status("ℹ Cancelado por usuario", "info")
            return

        # -------------------------------------------------------------------------
        try:
            # paso self.clave que es el Id de la tabla y la marca para aceptar o des_aceptar
            self.principal.var_obj_presup.marcar_presup_aceptado(self.clave, marca_aceptado)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # --------------------------------------------------------------------------

        if marca_aceptado == "1":
            self.principal.status.set_status("✔ Presupuesto aceptado", "ok")
        else:
            self.principal.status.set_status("✔ Presupuesto NO aceptado", "ok")

        self.fllena_grilla_presupuestos(self.clave)

    # -----------------------------------------------------------------------------
    # GUARDAR PRESUPUESTOS
    # -----------------------------------------------------------------------------

    def fguardar(self):
        self.fcerrar_presupuesto("normal")

    def fguardar_como(self):
        pass
    #     self.fcerrar_presupuesto("como")

    def fcerrar_presupuesto(self, parametro):

        # VALIDACIONES  ------------------------------------------------------------------
        # valido que haya items en venta - Grid vacio
        if len(self.principal.pestana_2.grid_componentes.get_children()) <= 0:
            messagebox.showerror("Error", "No hay componentes cargados", parent=self)
            return
        # valido nro venta - no hay numero de venta
        if self.principal.sv_nro_presup.get() == 0:
            messagebox.showerror("Error", "Verifique numero de venta", parent=self)
            return
        # valido fecha venta - no hay feca de venta
        if self.principal.sv_fecha_presup.get() == "":
            messagebox.showerror("Error", "Verifique fecha de venta", parent=self)
            return
        # valido nombre de cliente - no hay cliente asignado
        if self.sv_nombre_cliente.get() == "":
            messagebox.showerror("Error", "Ingrese nombre de cliente", parent=self)
            return
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        if parametro == "normal":
            # Es una carga normal
            r = messagebox.askquestion("Cerrar presupuesto", "Guardamos el presupuesto? ", parent=self)
            if r == messagebox.NO:
                return

            # -------------------------------------------------------------------
            try:
                # Borro el presupuesto en las dos tablas (resu_presup y deta_presup) por las dudas sea modificacion
                self.principal.var_obj_presup.eliminar_detapresup(self.principal.sv_nro_presup.get())
                # Borro en deta_presup - por las dudas sea modificacion
                self.principal.var_obj_presup.eliminar_presu_entregado2(self.principal.sv_nro_presup.get())
            except Exception:
                self.principal.var_obj_funcionnew.mostrar_error()
                return
            # -------------------------------------------------------------------

        # --------------------------------------------------------------------
        if parametro == "como":
            # Es guardar como para generar un presupuesto igual pero con otro numero

            r = messagebox.askquestion("Presupuesto", "Duplicar presupuesto... asignando numero siguiente ", parent=self)
            if r == messagebox.NO:
                return

            # Si es -guardar_como- busco solamente asignar un numero mas de presupuesto como si fuera uno nuevo
            self.principal.sv_nro_presup.set(value=str(int(self.principal.var_obj_presup.traer_ultimo(1)) + 1))
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        try:
            # Antes de insertar los presupuestos en las tablas principales, borro todo aux_presup y
            #  lo vuelvo a cargar desde el GRID con los datos actualizados
            self.principal.var_obj_presup.actualizar_auxpresup(self.principal.pestana_2.grid_componentes)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # CARGA DE LAS TABLAS - CIERRE DE PRESUPUESTO
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        try:
            # Inserto en tabla DETA_PRESU
            datos = self.principal.var_obj_presup.consultar_detalle_auxpresup()
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -------------------------------------------------------------------

        for row in datos:

            # -----------------------------------------------------------------
            dic_deta_presup = {
                "Id": row[0],                                          # Id
                "dp_orden": row[1],                                    # orden elemento
                "dp_numero": self.principal.sv_nro_presup.get(),       # numero de presupuesto
                "dp_proved": row[2],                                   # nombre proveedor
                "dp_codcomp": row[3],                                  # codigo componente del proveedor
                "dp_componente": row[4],                               # descripcion del componente
                "dp_iva": row[5],                                      # tasa iva del componente
                "dp_cantidad": row[6],                                 # cantidad del componente
                "dp_neto_dolar": row[7],                               # costo neto componente en dolares
                "dp_redondo": row[9]                                   # total en pesos redondeo
            }

            # -----------------------------------------------------------------
            try:
                self.principal.var_obj_presup.insertar_detapresup(dic_deta_presup)
            except Exception:
                self.principal.var_obj_funcionnew.mostrar_error()
                return
            # -----------------------------------------------------------------

        # Insertar en tabla resu_presup ------------------------------------------------
        self.nuevo_presupuesto = self.principal.sv_nro_presup.get()
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        dic_resu_presup = {
            "Id": "",                                                                  # Id
            "rp_numero": self.principal.sv_nro_presup.get(),                           # numero de presupuesto
            "rp_fecha": self.principal.sv_fecha_presup.get(),                          # fecha de presupuesto
            "rp_codcli": self.sv_codigo_cliente.get(),                                 # codigo de cliente
            "rp_nomcli": self.sv_nombre_cliente.get(),                                 # nombre del cliente
            "rp_sitfiscal": self.sv_sit_fiscal.get(),                                  # situacion fiscal del cliente
            "rp_cuit": self.sv_cuit.get(),                                             # cuit del cliente
            "rp_valor_dolar": self.principal.sv_valor_dolar_presup.get(),              # valor asignado del dolar hoy
            "rp_tasa_gan": self.principal.sv_tasa_ganancia.get(),                      # tasa de ganancia
            "rp_total_real": self.principal.sv_total_presup.get(),                     # total en pesos redondeo
            "rp_total_redondo": self.principal.sv_total_presup_redondo.get(),          # total en pesos redondeo
            "rp_forma_pago": self.sv_combo_formas_pago.get(),                          # forma de pago
            "rp_detalle_pago": self.sv_detalle_pago.get(),                             # detalle del pago
            "rp_detalle": self.principal.pestana_2.text_especificaciones.get(1.0, 'end-1c'),  # texto especificaciones
            "rp_aceptado": self.sv_aceptado.get()                            # codigo 0/1 de presupuesto aceptado o no
        }

        # --------------------------------------------------------------------------
        try:
            self.principal.var_obj_presup.insertar_presu_entregado(dic_resu_presup)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -----------------------------------------------------------------

        # pongo all en blanco como si recien iniciara para que se pueda pedir un nuevo presupuesto
        self.principal.estado_inicial_general()

        self.principal.status.set_status("🗑 Ingreso correcto detalle y resumen", "ok")

        # ---------------------------------------------------------------------
        try:
            ultimo_tabla_id = self.principal.var_obj_presup.traer_ultimo(0)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

        self.fllena_grilla_presupuestos(ultimo_tabla_id)

        # ---------------------------------------------------------------------
        try:
            # Vacio GRID aux_presup
            self.principal.var_obj_presup.vaciar_auxpresup()
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

    def doble_click_grid(self, _event):

        self.flimpiar_entrys_uno()
        self.estado_entrys_crud_uno("disabled")
        self.fedito_presupuesto()



    # ----------------------------------------------------------------------
    # CUADROS
    # ----------------------------------------------------------------------

    # GRID presupuestos - Creacion GRID de presupuestos (historico)
    def fcuadro_grid_presupuestos(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_presupuestos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_presupuestos = ttk.Treeview(self.frame_grid_presupuestos, height=8, columns=("col1",
                                                    "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9"))

        self.grid_presupuestos.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_presupuestos.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_presupuestos.column("col1", width=100, anchor="w", minwidth=100)
        self.grid_presupuestos.column("col2", width=80, anchor="w", minwidth=80)
        self.grid_presupuestos.column("col3", width=350, anchor="center", minwidth=350)
        self.grid_presupuestos.column("col4", width=100, anchor="center", minwidth=100)
        self.grid_presupuestos.column("col5", width=100, anchor="center", minwidth=100)
        self.grid_presupuestos.column("col6", width=130, anchor="center", minwidth=130)
        self.grid_presupuestos.column("col7", width=130, anchor="center", minwidth=130)
        self.grid_presupuestos.column("col8", width=130, anchor="center", minwidth=130)
        self.grid_presupuestos.column("col9", width=130, anchor="center", minwidth=130)

        self.grid_presupuestos.heading("#0", text="Id", anchor="center")
        self.grid_presupuestos.heading("col1", text="Nº Venta", anchor="w")
        self.grid_presupuestos.heading("col2", text="Fecha", anchor="w")
        self.grid_presupuestos.heading("col3", text="Cliente", anchor="center")
        self.grid_presupuestos.heading("col4", text="Dolar", anchor="center")
        self.grid_presupuestos.heading("col5", text="% Ganancia", anchor="center")
        self.grid_presupuestos.heading("col6", text="Total venta", anchor="center")
        self.grid_presupuestos.heading("col7", text="Redondeo", anchor="center")
        self.grid_presupuestos.heading("col8", text="Forma pago", anchor="center")
        self.grid_presupuestos.heading("col9", text="Detalle pago", anchor="center")

        self.grid_presupuestos.tag_configure('oddrow', background='light grey')
        self.grid_presupuestos.tag_configure('evenrow', background='white')
        self.grid_presupuestos.tag_configure('error', background='#AADE64')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_grid_presupuestos, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_grid_presupuestos, orient="vertical")
        self.grid_presupuestos.config(xscrollcommand=scroll_x.set)
        self.grid_presupuestos.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_presupuestos.xview)
        scroll_y.config(command=self.grid_presupuestos.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_presupuestos['selectmode'] = 'browse'

        self.grid_presupuestos.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    # Buscar un presupuesto
    def fcuadro_buscar_presupuestos(self):

        for c in range(5):
            self.frame_busqueda_presupuestos.grid_columnconfigure(c, weight=1, minsize=10)

        icono = self.principal.cargar_icono("buscar.png")
        self.lbl_busqueda_presup = tk.Label(self.frame_busqueda_presupuestos, text=" Buscar presupuesto por cliente: ",
                                            justify="left", bg="light blue", compound="left")
        self.lbl_busqueda_presup.image = icono
        self.lbl_busqueda_presup.config(image=icono)
        self.lbl_busqueda_presup.grid(row=0, column=0, padx=3, pady=2, sticky="nsew")

        # ENTRY BUSCAR PRESUPUESTO REALIZADO
        self.entry_busqueda_presup = tk.Entry(self.frame_busqueda_presupuestos, textvariable=self.sv_buscostring,
                                              state='normal', width=40, justify="left")
        self.entry_busqueda_presup.grid(row=0, column=1, padx=3, pady=2, sticky='nsew')

        # BOTON BUSCAR PRESUPUESTO
        icono = self.principal.cargar_icono("filtrar.png")
        self.btn_buscar=tk.Button(self.frame_busqueda_presupuestos, text=" Buscar", command=self.fbuscar_presupuesto,
                                  bg='Blue', fg='white', width=95, compound="left")
        self.btn_buscar.image = icono
        self.btn_buscar.config(image=icono)
        self.btn_buscar.grid(row=0, column=2, padx=3, pady=2, sticky="nsew")

        # BOTON SHOWALL
        icono = self.principal.cargar_icono("ver_todo.png")
        self.btn_showall=tk.Button(self.frame_busqueda_presupuestos, text=" Mostrar todo", command=self.fshowall,
                                   bg='Blue', fg='white', width=95, compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=3, pady=2, sticky="nsew")

        # IMPRIMIR PRESUPUESTO INTERNO
        icono = self.principal.cargar_icono("impresora.png")
        self.btn_showall.grid(row=0, column=3, padx=4, pady=2, sticky="w")
        self.btn_imprime_presup=tk.Button(self.frame_busqueda_presupuestos, text=" Presupuesto",
                                          command=self.fmenu_listados, width=105, bg='#5F9EF5', fg='white', compound="left")
        self.btn_imprime_presup.image = icono
        self.btn_imprime_presup.config(image=icono)
        self.btn_imprime_presup.grid(row=0, column=4, padx=4, pady=2, sticky="nsew")
        # ----------------------------------------------------------------------

        # Salir del modulo
        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.frame_busqueda_presupuestos, text="Salir", image=self.photo3, width=85,
                                  command=self.principal.fsalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # BOTONES FIN PRINCIPIO ARCHIVO

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((18, 18), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_busqueda_presupuestos, text="", image=self.photo4, command=self.ftoparch,
                                    bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=6, padx=4, sticky="nsew", pady=2)

        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((18, 18), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_busqueda_presupuestos, text="", image=self.photo5, command=self.ffinarch,
                                    bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=7, padx=4, sticky="nsew", pady=2)

        # reordenamiento del frame
        for widg in self.frame_busqueda_presupuestos.winfo_children():
            widg.grid_configure(padx=4, pady=3, sticky='nsew')

    # Ingresar ganancia y dolar para el presupuesto que se esta preparando
    def entry_ganancia(self):

        for c in range(6):
            self.frame_ganancia.grid_columnconfigure(c, weight=1, minsize=100)

        # % GANANCIA
        self.lbl_tasa_ganancia = tk.Label(self.frame_ganancia, text="Ganancia %: ", bg="#CEF2EF", justify="left")
        self.lbl_tasa_ganancia.grid(row=0, column=0, padx=3, pady=2, sticky="w")
        self.entry_tasa_ganancia = tk.Entry(self.frame_ganancia, textvariable=self.principal.sv_tasa_ganancia, width=6,
                                            justify="right")
        self.entry_tasa_ganancia.grid(row=0, column=1, padx=3, pady=2, sticky="e")
        self.entry_tasa_ganancia.config(validate="key", validatecommand=self.vcmd)
        self.entry_tasa_ganancia.bind("<FocusOut>", lambda e: self.principal.var_obj_funcionnew.corregir_al_salir(self.entry_tasa_ganancia))
        self.entry_tasa_ganancia.bind('<Tab>', lambda e: self.principal.pestana_2.calcular("completo"))

        # COTIZACION DEL DOLAR A APLICAR EN ESTE PRESUPUESTO
        self.lbl_dolarhoy1 = tk.Label(self.frame_ganancia, text="Dolar este presupuesto:", justify="left", bg="#CEF2EF",
                                      foreground="red")
        self.lbl_dolarhoy1.grid(row=0, column=2, padx=3, pady=2, sticky="w")
        self.entry_dolarhoy2 = tk.Entry(
            self.frame_ganancia, textvariable=self.principal.sv_valor_dolar_presup, width=10, justify="right",
            foreground="red"
        )
        self.entry_dolarhoy2.grid(row=0, column=3, padx=3, pady=2, sticky="e")

        # COTIZACION DEL DOLAR DEL DIA
        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        self.lbl_dolarhoy1 = tk.Label(self.frame_ganancia, text="Dolar oficial hoy:", justify="left", font=fff,
                                      foreground="black")
        self.lbl_dolarhoy1.grid(row=0, column=4, padx=4, pady=2, sticky=tk.W)
        self.lbl_dolarhoy2 = tk.Label(self.frame_ganancia, textvariable=self.principal.sv_valor_dolar_oficial_hoy,
                                      width=10, justify="right", font=fff, foreground="black")
        self.lbl_dolarhoy2.grid(row=0, column=5, padx=4, pady=2, sticky='nsew')

        for widg in self.frame_ganancia.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    # Definicion de los Entrys del encabezado
    def fcuadro_entrys_datos_cliente(self):

        #fff = tkfont.Font(family="Arial", size=8, weight="bold")
        www = tkfont.Font(family="Arial", size=10, weight="bold")

        for c in range(11):
            self.frame_cliente.grid_columnconfigure(c, weight=1, minsize=30)

        # NUMERO DE PRESUPUESTO
        self.lbl_nro_presup = tk.Label(self.frame_cliente, text="Nº: ", width=2, font=www, fg="red", bg="#CEF2EF",
                                       justify="right")
        self.lbl_nro_presup.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.lbl_nro_presup2 = tk.Label(self.frame_cliente, textvariable=self.principal.sv_nro_presup, font=www,
                                        width=2, bg="#CEF2EF", fg="red")
        self.lbl_nro_presup2.grid(row=0, column=1, padx=2, pady=2, sticky="w")

        # FECHA DE VENTA
        self.lbl_fecha_presup = tk.Label(self.frame_cliente, text="Fecha: ", bg="#CEF2EF", justify="right")
        self.lbl_fecha_presup.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        self.entry_fecha_presup = tk.Entry(self.frame_cliente, textvariable=self.principal.sv_fecha_presup, width=8,
                                           justify="right")
        self.entry_fecha_presup.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        #self.entry_fecha_presup.bind("<FocusOut>", self.formato_fecha)
        #self.entry_fecha_presup.bind("<FocusOut>", lambda event: self.principal.var_obj_funcionnew.validar_fecha(self.principal.sv_fecha_presup, self.entry_fecha_presup))
        self.entry_fecha_presup.bind("<FocusOut>", lambda event: self.principal.var_obj_funcionnew.validar_fecha(
                self.principal.sv_fecha_presup, self.entry_fecha_presup))

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((18, 18), Image.Resampling.LANCZOS)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_busco_cliente = tk.Button(self.frame_cliente, text="", image=self.photo_bus_cli,
                                           command=self.fbuscli, fg="white")
        self.btn_busco_cliente.grid(row=0, column=4, padx=3, pady=2, sticky='nsew')

        # NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = tk.Label(self.frame_cliente, text="Cliente: ", bg="#CEF2EF", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=5, padx=3, pady=2, sticky="w")
        self.entry_nombre_cliente = tk.Entry(self.frame_cliente, textvariable=self.sv_nombre_cliente, width=40)
        self.entry_nombre_cliente.grid(row=0, column=6, padx=3, pady=2, sticky="w")
        self.sv_nombre_cliente.trace("w", lambda *args: limitador(self.sv_nombre_cliente, 50))

        # SITUACION FISCAL DEL CLIENTE
        self.lbl_sit_fiscal_cliente = tk.Label(self.frame_cliente, text="SF", bg="#CEF2EF")
        self.lbl_sit_fiscal_cliente.grid(row=0, column=7, padx=3, pady=2, sticky="w")
        self.combo_sit_fiscal_cliente = ttk.Combobox(self.frame_cliente, textvariable=self.sv_sit_fiscal, justify="left",
                                                     state='readonly', width=22)
        # self.cargar_combo = self.varClientes.llenar_combo_rubro()
        self.combo_sit_fiscal_cliente["values"] = ["CF - Consumidor Final", "RI - Responsable Inscripto",
                                                   "RM - Responsable Monotributo", "EX - Exento",
                                                   "RN - Responsable no inscripto"]
        self.combo_sit_fiscal_cliente.current(0)
        self.combo_sit_fiscal_cliente.grid(row=0, column=8, padx=2, pady=2, sticky="w")

        # CUIT CLIENTE
        self.lbl_texto_cuit_cliente = tk.Label(self.frame_cliente, text="CUIT:", bg="#CEF2EF", justify="left")
        self.lbl_texto_cuit_cliente.grid(row=0, column=9, padx=3, pady=2, sticky="w")
        self.entry_cuit_cliente = tk.Entry(self.frame_cliente, textvariable=self.sv_cuit, justify="right", width=13)
        self.entry_cuit_cliente.grid(row=0, column=10, padx=3, pady=2, sticky="w")

        for widg in self.frame_cliente.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    # Botones CRUD grid presupuestos entregados
    def fcuadro_botones__uno_grid_presupuestos(self):

        for c in range(4):
            self.frame_botones_uno_grid_presupuestos.grid_columnconfigure(c, weight=1, minsize=140)

        icono = self.principal.cargar_icono("archivo-nuevo.png")
        self.btn_nuevo_presup=tk.Button(self.frame_botones_uno_grid_presupuestos, text=" Nuevo Presupuesto",
                                        command=self.fnuevo_presupuesto, bg='blue', fg='white', compound="left")
        self.btn_nuevo_presup.image = icono
        self.btn_nuevo_presup.config(image=icono)
        self.btn_nuevo_presup.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        icono = self.principal.cargar_icono("editar.png")
        self.btn_edito_presup=tk.Button(self.frame_botones_uno_grid_presupuestos, text=" Editar Presupuesto",
                                        command=self.fedito_presupuesto, width=17, bg='blue', fg='white', compound="left")
        self.btn_edito_presup.image = icono
        self.btn_edito_presup.config(image=icono)
        self.btn_edito_presup.grid(row=0, column=1, padx=3, pady=3, sticky="w")

        icono = self.principal.cargar_icono("eliminar.png")
        self.btn_borro_presup=tk.Button(self.frame_botones_uno_grid_presupuestos, text=" Borrar Presupuesto",
                                        command=self.fborro_presupuesto, width=17, bg='red', fg='white', compound="left")
        self.btn_borro_presup.image = icono
        self.btn_borro_presup.config(image=icono)
        self.btn_borro_presup.grid(row=0, column=2, padx=3, pady=3, sticky="w")

        icono = self.principal.cargar_icono("ordenar.png")
        self.btn_aceptado_presup=tk.Button(self.frame_botones_uno_grid_presupuestos, text=" Marcar presupuesto aceptado",
                                           command=self.fpresupuesto_aceptado, width=17, bg='#75E342', fg='black', compound="left")
        self.btn_aceptado_presup.image = icono
        self.btn_aceptado_presup.config(image=icono)
        self.btn_aceptado_presup.grid(row=0, column=3, padx=3, pady=3, sticky="w")

        # reordenamiento del frame
        for widg in self.frame_botones_uno_grid_presupuestos.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def fentrys_formas_pago(self):

        for c in range(4):
            self.frame_forma_pago.grid_columnconfigure(c, weight=1, minsize=30)

        # forma de pago y detalle
        self.lbl_combo_formapago = tk.Label(self.frame_forma_pago, text="Forma de Pago: ", bg="#CEF2EF", justify="left")
        self.lbl_combo_formapago.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.combo_formapago = ttk.Combobox(self.frame_forma_pago, textvariable=self.sv_combo_formas_pago,
                                            state='readonly', width=15)
        self.combo_formapago['value'] = ["Efectivo", "Transferencia", "Cuenta Corriente", "Tarjeta Debito",
                                         "Tarjeta Credito", "Cheque"]
        self.combo_formapago.current(0)
        self.combo_formapago.grid(row=0, column=1, padx=4, pady=2, sticky="w")

        # Detalle de pago
        self.lbl_deta_formapago = tk.Label(self.frame_forma_pago, text="Detalle: ", bg="#CEF2EF", justify="left")
        self.lbl_deta_formapago.grid(row=0, column=2, padx=2, pady=2, sticky="w")
        self.entry_deta_formapago = tk.Entry(self.frame_forma_pago, textvariable=self.sv_detalle_pago, width=123)
        self.entry_deta_formapago.grid(row=0, column=3, padx=4, pady=2, sticky="w")

        for widg in self.frame_forma_pago.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def fcuadro_totales_generales(self):

        fff = tkfont.Font(family="Arial", size=9, weight="bold")

        for c in range(8):
            self.frame_totales_generales.grid_columnconfigure(c, weight=1, minsize=30)

        # TOTAL COSTO BRUTO
        self.lbl_total_costos = tk.Label(self.frame_totales_generales, text="Total Costos: ", justify="left", font=fff,
                                         foreground="#ff33f6")
        self.lbl_total_costos.grid(row=0, column=0, padx=8, pady=2, sticky="w")
        self.lbl_total_costos2 = tk.Label(self.frame_totales_generales, textvariable=self.principal.sv_total_costos,
                                          width=15, justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_costos2.grid(row=0, column=1, padx=8, pady=2, sticky="e")

        # TOTAL GANANCIA
        self.lbl_total_ganancia = tk.Label(self.frame_totales_generales, text="Total ganancia: ", justify="left",
                                           font=fff, foreground="#ff33f6")
        self.lbl_total_ganancia.grid(row=0, column=2, padx=8, pady=2, sticky="w")
        self.lbl_total_ganancia2 = tk.Label(self.frame_totales_generales, textvariable=self.principal.sv_total_ganancia,
                                            width=15, justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_ganancia2.grid(row=0, column=3, padx=8, pady=2, sticky="e")

        # TOTAL PRESUPUESTO GLOBAL
        self.lbl_total_presupuesto = tk.Label(self.frame_totales_generales, text="Total presupuesto: ", justify="left",
                                              font=fff, foreground="#ff33f6")
        self.lbl_total_presupuesto.grid(row=0, column=4, padx=8, pady=2, sticky="w")
        self.lbl_total_presupuesto2 = tk.Label(self.frame_totales_generales, textvariable=self.principal.sv_total_presup,
                                               width=15, justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_presupuesto2.grid(row=0, column=5, padx=8, pady=2, sticky="e")

        # TOTAL PRESUPUESTO REDONDEADO
        self.lbl_total_presup_redondo = tk.Label(self.frame_totales_generales, text="Total redondeado: ",
                                                 justify="left", font=fff, foreground="#ff33f6")
        self.lbl_total_presup_redondo.grid(row=0, column=6, padx=8, pady=2, sticky="w")
        self.lbl_total_presup_redondo2 = tk.Label(self.frame_totales_generales,
                                                  textvariable=self.principal.sv_total_presup_redondo, width=15,
                                                  justify="right", font=fff, foreground="#ff33f6")
        self.lbl_total_presup_redondo2.grid(row=0, column=7, padx=8, pady=2, sticky="e")

        for widg in self.frame_totales_generales.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def fcuadro_cerrar_cancelar(self):

        for c in range(3):
            self.frame_cerrar_cancelar.grid_columnconfigure(c, weight=1, minsize=30)

        icono = self.principal.cargar_icono("guardar.png")
        self.btn_cerrar_presupuesto=tk.Button(self.frame_cerrar_cancelar, text=" Actualizar/Guardar\n presupuesto",
                                           command=self.fguardar, width=17, bg='green', fg='white', compound="left")
        self.btn_cerrar_presupuesto.image = icono
        self.btn_cerrar_presupuesto.config(image=icono)
        self.btn_cerrar_presupuesto.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        icono = self.principal.cargar_icono("guardar.png")
        self.btn_guardar_como=tk.Button(self.frame_cerrar_cancelar, text=" Guardar como...", command=self.fguardar_como,
                                     width=17, bg='light green', fg='black', compound="left")
        self.btn_guardar_como.image = icono
        self.btn_guardar_como.config(image=icono)
        self.btn_guardar_como.grid(row=0, column=1, padx=3, pady=3, sticky="w")

        icono = self.principal.cargar_icono("cancelar.png")
        self.btn_cancelar_presupuesto = tk.Button(self.frame_cerrar_cancelar, text=" Cancelar",
                                                  command=self.principal.fcancela_presup,
                                                  width=17, bg='black', fg='white', compound="left")
        self.btn_cancelar_presupuesto.image = icono
        self.btn_cancelar_presupuesto.config(image=icono)
        self.btn_cancelar_presupuesto.grid(row=0, column=2, padx=3, pady=3, sticky="w")

        for widg in self.frame_cerrar_cancelar.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')


    # ----------------------------------------------------------------------------
    # BUSQUEDAS EN GRID PRESUPUESTOS Y FUNCIONES SEL
    # ----------------------------------------------------------------------------

    def fbuscar_presupuesto(self):

        if len(self.sv_buscostring.get()) > 0:

            se_busca = self.sv_buscostring.get()

            # ---------------------------------------------------------------------
            try:
                datos = self.principal.var_obj_presup.buscar_entabla(se_busca)
            except Exception:
                self.principal.var_obj_funcionnew.mostrar_error()
                return
            # ---------------------------------------------------------------------

            # Limpio el grid
            for item in self.grid_presupuestos.get_children():
                self.grid_presupuestos.delete(item)

            # carga la grilla con los registros seleccionados
            for row in datos:
                self.grid_presupuestos.insert("", "end", text=row[0], values=row[1:])
                # 👉 row[1:] significa:desde el segundo elemento en adelante o sea: row[1], row[2], row[3]...

            items = self.grid_presupuestos.get_children()

            # selecciono el primero de la tabla y pongo foco y visibilidad
            if items:
                primero = items[0]
                self.grid_presupuestos.selection_set(primero)
                self.grid_presupuestos.focus(primero)
                self.grid_presupuestos.see(primero)

    # SEL CLIENTE
    def fbuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y
        en que campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """  Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden de
        como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco) """

        valores_new = self.principal.var_obj_funcionnew.ventana_selec("clientes", "apenombre", "codigo", "direccion",
                                                                  "Apellido y nombre", "Codigo", "Direccion",
                                                                  que_busco, "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a
        los Entrys correspondientes """

        for item in valores_new:

            self.sv_nombre_cliente.set(value=item[15])
            self.sv_codigo_cliente.set(value=item[1])
            self.sv_sit_fiscal.set(value=item[11])
            self.sv_cuit.set(value=item[12])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # ----------------------------------------------------------------------------
    # MOVIMIENTOS EN EL GRID
    # ----------------------------------------------------------------------------

    def ftoparch(self):
        self.principal.var_obj_funcionnew.mover_puntero_topend(self.grid_presupuestos, 'TOP')

    def ffinarch(self):
        self.principal.var_obj_funcionnew.mover_puntero_topend(self.grid_presupuestos, 'END')

    def fshowall(self):
        self.selected = self.grid_presupuestos.focus()
        self.clave = self.grid_presupuestos.item(self.selected, 'text')
        self.filtro_activo_presupuestos = "ORDER BY rp_fecha"
        self.fllena_grilla_presupuestos(self.clave)




    # ----------------------------------------------------------------------------
    # IMPRESION
    # ----------------------------------------------------------------------------

    def fmenu_listados(self):

        # ---------------------------------------------------------------------------
        # DEFINO PANTALLA FLOTANTE

        self.pantalla_imprimir = tk.Toplevel()
        self.pantalla_imprimir.geometry('630x260+660+380')
        self.pantalla_imprimir.transient(master=self.master)
        self.pantalla_imprimir.config(bg='light green', padx=5, pady=5)
        self.pantalla_imprimir.resizable(False, False)
        self.pantalla_imprimir.title("Seleccion formato Informe")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # TITULOS

        self.frame_titulo_impresion = tk.Frame(self.pantalla_imprimir, bg="light green")

        # Armo el logo y el titulo
        self.photo = Image.open('impresora.png')
        self.photo = self.photo.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_select = ImageTk.PhotoImage(self.photo)
        self.lbl_png_select = tk.Label(self.frame_titulo_impresion, image=self.png_select, bg="red", relief="ridge", bd=5)

        self.lbl_tit = tk.Label(self.frame_titulo_impresion, width=29, text="Seleccion formato Informe",
                             bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_select.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
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

        # ----------------------------------------------------------------------------------
        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_presupuestos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_presupuestos.item(self.selected, 'text')
        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return
        # ----------------------------------------------------------------------------------

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
        valores = self.grid_presupuestos.item(self.selected, 'values')

        # armado de encabezado
        fecha_presup = valores[1]
        self.pdf_numero_presupuesto   = valores[0]
        self.pdf_nombre_cliente       = valores[2]
        self.pdf_dolar_presupuesto    = valores[3]
        self.pdf_tasa_ganancia        = valores[4]
        self.pdf_total_presup_redondo = valores[6]

        # ---------------------------------------------------------------------
        try:
            # Traigo, si es que hay, el detalle extenso del producto presupuestado de la tabla resu_presup
            datos_presu_entregado = self.principal.var_obj_presup.traer_resu_presup(self.pdf_numero_presupuesto)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

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

        # ---------------------------------------------------------------------
        try:
            # Traer todos los registros de la tabla deta_presup ---------------------
            self.items_presupuesto = self.principal.var_obj_presup.traer_deta_presup(self.pdf_numero_presupuesto)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 8)
        total_presupuesto = 0

        for row in self.items_presupuesto:

            # calculos ----------------------------------------------------------
            bruto_dolar = round((row[7] * float(row[8])) * (1+(float(row[6])/100)), 2)
            sumo_precio_final_conganancia = round((bruto_dolar * float(self.principal.sv_valor_dolar_presup.get())) *
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
        #total_presupuesto = formatear_cifra(total_presupuesto)
        total_redondo = formatear_cifra(round(float(self.pdf_total_presup_redondo), 2))
        #pdf.cell(w=0, h=5, txt="Total: " + str(total_presupuesto), border=0, align='R', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt="Total: " + str(total_redondo), border=0, align='R', fill=0, ln=1)

        # Espaciado -----------------------------------------------------------------------
        pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        try:
            pdf.output('hoja.pdf')
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error("Verifique listados abiertos en otras terminales")
            return

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    def creopdfint(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_presupuestos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_presupuestos.item(self.selected, 'text')

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
        valores = self.grid_presupuestos.item(self.selected, 'values')

        # # armado de encabezado ------------------------------------------------------------
        # fecha_forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'))

        # sdf = datetime.strptime(valores[1], '%Y-%m-%d')
        # fecha_presup = sdf.strftime('%d-%m-%Y')
        fecha_presup = valores[1]
        self.pdf_numero_presupuesto =   valores[0]
        self.pdf_nombre_cliente =       valores[2]
        self.pdf_dolar_presupuesto =    valores[3]
        self.pdf_tasa_ganancia =        valores[4]
        self.pdf_total_presup_redondo = valores[6]

        # ---------------------------------------------------------------------
        try:
            # Traigo, si es que hay, el detalle extenso del producto presupuestado de la tabla resu_presup
            datos_presu_entregado = self.principal.var_obj_presup.traer_resu_presup(self.pdf_numero_presupuesto)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

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

        # ---------------------------------------------------------------------
        try:
            # Traer todos los registros de la tabla deta_presup
            self.items_presupuesto = self.principal.var_obj_presup.traer_deta_presup(self.pdf_numero_presupuesto)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # ---------------------------------------------------------------------

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
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error("Verifique listados abiertos en otras terminales")
            return

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)









# =========================================================================================
# PESTAÑA DOS
# =========================================================================================

class ClasePestanaDos(tk.Frame):

    def __init__(self, parent, principal):
        super().__init__(parent)

        # Creo instancia de clase principal - instancia directamente toda la clase principal
        # y comparto variables y funciones definidas en ella
        self.principal = principal

        # ---------------------------------------------------------------------
        # STRINGVARS
        # ---------------------------------------------------------------------
        self.sv_buscostring = tk.StringVar(value="")

        self.sv_componente = tk.StringVar(value="")
        self.sv_combo_tasa_iva = tk.StringVar(value="")
        self.sv_cantidad_vendida = tk.StringVar(value="0.00")
        self.sv_neto_dolar = tk.StringVar(value="0.00")
        self.sv_proveedor = tk.StringVar(value="")
        self.sv_codigo_componente = tk.StringVar(value="")

        self.sv_neto_dolar = tk.StringVar(value="0.00")
        self.sv_costo_neto_pesos_unidad = tk.StringVar(value="0.00")
        self.sv_costo_neto_pesos_xcanti = tk.StringVar(value="0.00")
        self.sv_costo_bruto_pesos_unidad = tk.StringVar(value="0.00")
        self.sv_costo_bruto_pesos_xcanti = tk.StringVar(value="0.00")
        self.sv_importe_iva_unidad = tk.StringVar(value="0.00")
        self.sv_importe_iva_xcanti = tk.StringVar(value="0.00")
        self.sv_importe_ganancia_unidad = tk.StringVar(value="0.00")
        self.sv_importe_ganancia_xcanti = tk.StringVar(value="0.00")
        self.sv_precio_final_unidad = tk.StringVar(value="0.00")
        self.sv_precio_final_xcanti = tk.StringVar(value="0.00")

        self.sv_combo_tasa_iva = tk.StringVar()
        # ----------------------------------------------------------------------

        # Ejecutamos tu secuencia de inicialización adaptada a la Pestaña 2
        self.create_widgets()


    def create_widgets(self):

        # MUY IMPORTANTE: Todos tus widgets de esta pestaña deben tener como padre a 'self'
        # Ejemplo: self.boton = ttk.Button(self, text="Guardar Cotización")

        # VARIABLES GENERALES -------------------------------------------------
        # para validar ingresos de numeros en gets numericos
        self.vcmd = (self.register(self.principal.var_obj_funcionnew.validar), "%P")

        # CUADROS - CONTENEDORES ----------------------------------------------

        # Contenedor principal
        self.frame_principal = tk.LabelFrame(self, text="", foreground="#CD5C5C")
        self.frame_principal.pack(expand=True, fill="both", padx=5, pady=5)  # O el empaquetado que uses (.grid o .pack)

        # Contenedor GRID Tabla aux_ventas (auxiliar) para los detalles de articulos vendidos
        self.frame_grid_componentes=tk.LabelFrame(self.frame_principal, text="Componentes presupuesto actual",
                                                  foreground="#CD5C5C")
        self.cuadro_grid_componentes()
        self.frame_grid_componentes.pack(side="top", fill="both", padx=5, pady=2)

        # Botones CRUD GRID auxiliar de< componentes
        self.frame_cuadro3 = tk.LabelFrame(self.frame_principal, text="", bg="#27F5E4")
        self.cuadro_botones_grid_componentes()
        self.frame_cuadro3.pack(side="top", fill="both", padx=5, pady=5)
        # ---------------------------------------------------------------------

        # ENTRYS ARTICULO/COMPONENTE A VENDER
        self.frame_componentes = tk.LabelFrame(self.frame_principal, text="", bg="#81EBCD", borderwidth=2,
                                               relief="solid", highlightbackground="blue")
        self.entrys_componentes()
        self.frame_componentes.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ENTRYS IMPORTES ARTICULO - Linea de precios del item a cargar
        self.frame_precios_articulo = tk.LabelFrame(self.frame_principal, text="", bg="#81EBCD", foreground="black",
                                                    relief="solid")
        self.entrys_precios_componentes()
        self.frame_precios_articulo.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # -----------------------------------------------------------------------

        # CUADRO FRAME_CAJADETEXTO
        self.frame_cajatexto = tk.LabelFrame(self.frame_principal, text="Descripcion adicional", fg="red")
        self.cuadro_caja_texto_detalles_extensos()
        self.frame_cajatexto.pack(expand=0, side="top", fill="both", pady=5, padx=5)
        # ----------------------------------------------------------------------

    def festado_inicial_dos(self):

        self.alta_modif_aux = 0  # tabla aux_presu
        # self.filtro_activo_presupuestos = "ORDER BY rp_fecha, rp_numero ASC"
        self.filtro_activo_auxiliar = "ORDER BY ax_orden ASC"

        # Limpiar los entrys de la pestaña dos
        self.limpiar_entrys_parcial()
        self.flimpiar_importes_componente()

        # Aseguro que esten desactivados los entrys de la pestaña dos
        self.estado_entrys_crud_dos("disabled")
        # Desactivo los botones de la parte de los componentes
        self.estado_botones_dos("disabled")
        # Refresco el GRID auxiliar de componentes
        self.llena_grilla_auxiliar("")

    def estado_botones_dos(self, estado):

        """ Activo/desactivo los botones de la parte de los componentes - + componente - componente Cierre etc... """

        self.btn_mas_componente.configure(state=estado)
        self.btn_menos_componente.configure(state=estado)
        self.btn_editar_componente.configure(state=estado)
        self.btn_ingresar_componente.configure(state=estado)
        self.btn_reset_componente.configure(state=estado)

        # self.btn_cancelar_presupuesto.configure(state=estado)

        # self.btn_cerrar_presupuesto.configure(state=estado)
        # self.btn_guardar_como.configure(state=estado)
        # self.btn_busco_cliente.configure(state=estado)
        # self.btn_bus_art.configure(state=estado)


    # ---------------------------------------------------------------------
    # GRID AUXILIAR - El de los componentes
    # ---------------------------------------------------------------------

    # GRID presupuesto actual o el que estamos recien creando en auxcomp tabla auxilliar
    def cuadro_grid_componentes(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_componentes)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_componentes = ttk.Treeview(self.frame_grid_componentes, height=9, columns=("col1", "col2", "col3",
                                                 "col4", "col5", "col6", "col7", "col8", "col9", "col10", "col11"))

        #self.grid_venta_articulos.bind("<Double-Button-1>", self.doble_click_grid)
        self.grid_componentes.column("#0", width=40, anchor="center", minwidth=40)
        self.grid_componentes.column("col1", width=50, anchor="w", minwidth=50)
        self.grid_componentes.column("col2", width=50, anchor="w", minwidth=60)
        self.grid_componentes.column("col3", width=90, anchor="center", minwidth=90)
        self.grid_componentes.column("col4", width=300, anchor="center", minwidth=250)
        self.grid_componentes.column("col5", width=50, anchor="center", minwidth=50)
        self.grid_componentes.column("col6", width=40, anchor="center", minwidth=40)
        self.grid_componentes.column("col7", width=100, anchor="center", minwidth=100)
        self.grid_componentes.column("col8", width=100, anchor="center", minwidth=100)
        self.grid_componentes.column("col9", width=100, anchor="center", minwidth=100)
        self.grid_componentes.column("col10", width=100, anchor="center", minwidth=100)
        self.grid_componentes.column("col11", width=100, anchor="center", minwidth=100)
        #self.grid_componentes.column("col12", width=100, anchor="center", minwidth=80)

        self.grid_componentes.heading("#0", text="Id", anchor="center")
        self.grid_componentes.heading("col1", text="Orden", anchor="w")
        self.grid_componentes.heading("col2", text="Proveedor", anchor="w")
        self.grid_componentes.heading("col3", text="Codigo Compn.", anchor="w")
        self.grid_componentes.heading("col4", text="Componente", anchor="center")
        self.grid_componentes.heading("col5", text="%IVA", anchor="center")
        self.grid_componentes.heading("col6", text="Cant.", anchor="center")
        self.grid_componentes.heading("col7", text="CostoNeto U$S", anchor="center")
        self.grid_componentes.heading("col8", text="Tot.Presupuesto", anchor="center")
        self.grid_componentes.heading("col9", text="Tot.Redondeo", anchor="center")
        self.grid_componentes.heading("col10", text="Tot.Ganancia", anchor="center")
        self.grid_componentes.heading("col11", text="Tot.Costo", anchor="center")
        #self.grid_componentes.heading("col12", text="Total Costo", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_grid_componentes, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_grid_componentes, orient="vertical")
        self.grid_componentes.config(xscrollcommand=scroll_x.set)
        self.grid_componentes.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_componentes.xview)
        scroll_y.config(command=self.grid_componentes.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_componentes['selectmode'] = 'browse'
        self.grid_componentes.pack(side="top", fill="both", expand=1, padx=5, pady=2)


    # ---------------------------------------------------------------------
    # BOTONES CRUD GRID AUXILIAR - El de los componentes
    # ---------------------------------------------------------------------

    def cuadro_botones_grid_componentes(self):

        # Botones +componente -com ponente Ingresar componente al presupuesto
        for c in range(7):
            self.frame_cuadro3.grid_columnconfigure(c, weight=1, minsize=100)

        # AGREGAR UN COMPONENTE
        icono = self.principal.cargar_icono("signo_mas.png")
        self.btn_mas_componente=tk.Button(self.frame_cuadro3, text=" Componente", command=self.fmas_componente,
                                          width=18, bg='blue', fg='white', compound="left")
        self.btn_mas_componente.image = icono
        self.btn_mas_componente.config(image=icono)
        self.btn_mas_componente.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

        # QUITAR UN COMPONENTE
        icono = self.principal.cargar_icono("signo_menos.png")
        self.btn_menos_componente=tk.Button(self.frame_cuadro3, text=" Componente", command=self.fmenos_componente,
                                            width=18, bg='blue', fg='white', compound="left")
        self.btn_menos_componente.image = icono
        self.btn_menos_componente.config(image=icono)
        self.btn_menos_componente.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")

        # EDITAR COMPONENTE
        icono = self.principal.cargar_icono("editar.png")
        self.btn_editar_componente = tk.Button(self.frame_cuadro3, text=" Editar\ncomponente",
                                               command=self.feditar_item_auxpresup, width=18, bg='blue', fg='white',
                                               compound="left")
        self.btn_editar_componente.image = icono
        self.btn_editar_componente.config(image=icono)
        self.btn_editar_componente.grid(row=0, column=2, padx=3, pady=3, sticky="nsew")

        # INGRESAR COMPONENTE AL GRID DE PRESUPUESTO ACTUAL
        icono = self.principal.cargar_icono("agregar-producto.png")
        self.btn_ingresar_componente = tk.Button(self.frame_cuadro3, text=" Ingresa\ncomponente",
                                                 command=self.finsertar_item_auxpresup, width=18, bg='blue', fg='white',
                                                 compound="left")
        self.btn_ingresar_componente.image = icono
        self.btn_ingresar_componente.config(image=icono)
        self.btn_ingresar_componente.grid(row=0, column=3, padx=3, pady=3, sticky="nsew")

        # CANCELAR LA CARGA DEL COMPONENTE AL GRID DE PRESUPUESTO ACTUAL
        icono = self.principal.cargar_icono("cancelar.png")
        self.btn_reset_componente = tk.Button(self.frame_cuadro3, text=" Cancela\ncomponente",
                                              command=self.freset_articulo, width=18, bg='grey', fg='white',
                                              compound="left")
        self.btn_reset_componente.image = icono
        self.btn_reset_componente.config(image=icono)
        self.btn_reset_componente.grid(row=0, column=4, padx=2, pady=2, sticky="nsew")

        # CANCELAR presupuesto total
        icono = self.principal.cargar_icono("cancelar.png")
        self.btn_cancelar_presupuesto = tk.Button(self.frame_cuadro3, text=" Cancelar\npresupuesto",
                                                  command=self.principal.fcancela_presup, width=18, bg='black',
                                                  fg='white', compound="left")
        self.btn_cancelar_presupuesto.image = icono
        self.btn_cancelar_presupuesto.config(image=icono)
        self.btn_cancelar_presupuesto.grid(row=0, column=5, padx=3, pady=3, sticky="w")
        # ----------------------------------------------------------------------

        # Salir del modulo
        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir = tk.Button(self.frame_cuadro3, text="Salir", image=self.photo3, width=18,
                                  command=self.principal.fsalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=6, padx=3, pady=2, sticky="nsew")
        # ----------------------------------------------------------------------

        # Flechas de movimiento en el GRID
        icono = self.principal.cargar_icono("flecha_arriba.png")
        self.btn_flecha_sube=tk.Button(self.frame_cuadro3, text="", command=self.fsubir_uno, width=20, bg='white', fg='black')
        self.btn_flecha_sube.image = icono
        self.btn_flecha_sube.config(image=icono)
        self.btn_flecha_sube.grid(row=0, column=7, padx=2, pady=2, sticky="nsew")

        icono = self.principal.cargar_icono("flecha_abajo.png")
        self.btn_flecha_baja=tk.Button(self.frame_cuadro3, text="", command=self.fbajar_uno, width=20, bg='white', fg='black')
        self.btn_flecha_baja.image = icono
        self.btn_flecha_baja.config(image=icono)
        self.btn_flecha_baja.grid(row=0, column=8, padx=2, pady=2, sticky="nsew")

        # reordenamiento del frame
        for widg in self.frame_cuadro3.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    # Caja de texto para detalle extenso
    def cuadro_caja_texto_detalles_extensos(self):

        self.frame_cajatexto.grid_rowconfigure(0, weight=1)
        self.frame_cajatexto.grid_columnconfigure(0, weight=1)
        self.text_especificaciones = ScrolledText(self.frame_cajatexto)
        self.text_especificaciones.config(width=100, height=8, wrap="word", padx=5, pady=5)
        self.text_especificaciones.grid(row=0, column=0, padx=5, pady=15)


    # ---------------------------------------------------------------------
    # FUNCIONES CRUD DE BOTONES CRUD GRID AUXILIAR - El de los componentes
    # ---------------------------------------------------------------------

    def fmas_componente(self):

        """ Agrega un componente al presupuesto - activa el sistema para ingresar componentes """

        # Los Entrys propios del componente
        self.estado_entrys_crud_dos("normal")
        # deshabilito los botones del crud 2
        self.estado_botones_dos("disabled")
        self.btn_ingresar_componente.configure(state="normal")
        self.btn_reset_componente.configure(state="normal")
        self.entry_componente.focus()
        # self.btn_mas_componente.configure(state="disabled")
        # self.btn_menos_componente.configure(state="disabled")
        # self.btn_editar_componente.configure(state="disabled")

    def feditar_item_auxpresup(self):

        # ---------------------------------------------------------------------------------
        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_componentes.focus()
        # Asi obtengo la clave de la Tabla campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_componentes.item(self.selected, 'text')
        # ---------------------------------------------------------------------------------

        if self.clave == "":
            self.principal.status.set_status("❌ No hay nada seleccionador", "error")
            return

        self.estado_entrys_crud_dos("normal")
        # Desactivo botones de novel 2 excepto "Cancelar, ingresar componente
        self.estado_botones_dos("disabled")
        self.btn_ingresar_componente.configure(state="normal")
        self.btn_reset_componente.configure(state="normal")
        self.entry_componente.focus()

        # activo bandera de modificacion de tabla auxpresup
        self.alta_modif_aux = 1

        # En la lista valores cargo toda la liena del GRID completa
        valores = self.grid_componentes.item(self.selected, 'values')

        self.sv_proveedor.set(value=valores[1])
        self.sv_codigo_componente.set(value=valores[2])
        self.sv_componente.set(value=valores[3])
        self.sv_combo_tasa_iva.set(value=valores[4])
        self.sv_cantidad_vendida.set(value=valores[5])
        self.sv_neto_dolar.set(value=valores[6])
        self.principal.sv_total_item_redondo.set(value=valores[8])

        self.calcular("completo")

        self.entry_componente.focus()

    def fmenos_componente(self):

        """ Elimina un coponente previamente cargado del presupuesto """

        # ---------------------------------------------------------------------------------
        self.selected = self.grid_componentes.focus()
        self.selected_ant = self.grid_componentes.prev(self.selected)
        self.clave = self.grid_componentes.item(self.selected, 'text')
        self.clave_ant = self.grid_componentes.item(self.selected_ant, 'text')
        # ---------------------------------------------------------------------------------

        if self.clave == "":
            self.principal.status.set_status("❌ No hay nada seleccionador", "error")
            return

        valores = self.grid_componentes.item(self.selected, 'values')
        data = str(self.clave) + " " + valores[0] + " " + valores[1]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar componente?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        # -------------------------------------------------------------------
        try:
            # Elimino item de aux_presup (solo el item seleccionado
            self.principal.var_obj_presup.eliminar_auxpresup(self.clave)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -------------------------------------------------------------------

        self.llena_grilla_auxiliar(self.clave_ant)

        # -------------------------------------------------------------------
        # reordenar numeros de orden para que se acomoden los numeros de orden
        self.freordenar(self.grid_componentes)
        # -------------------------------------------------------------------

        self.principal.status.set_status("🗑 Componente eliminado", "ok")

        self.calcular("totalventa")
        self.calcular("totalpresupuesto")

    def finsertar_item_auxpresup(self):

        """ Inserto el componente en tabla auxiliar (aux_presup) """

        # VALIDACIONES
        # 1- que articulo no este vacio y que haya cantidad
        if len(self.sv_componente.get()) == 0:
            self.principal.status.set_status("⚠ Faltan datos del componente", "warn")
            self.entry_componente.focus()
            return
        if float(self.sv_cantidad_vendida.get()) == 0:
            self.principal.status.set_status("⚠ No ingreso cantidad vendida", "warn")
            self.entry_cantidad.focus()
            return

        # controlo que no sea una modificacion para borrar el componente anterior
        if self.alta_modif_aux == 1:

            #MODIFICACION

            # ----------------------------------------------------------------
            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_componentes.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            self.clave = self.grid_componentes.item(self.selected, 'text')
            # ----------------------------------------------------------------

            # ----------------------------------------------------------------
            # Si es una modificacion, guardo el numero de orden que tenia
            # ----------------------------------------------------------------
            # primer elemento de la seleccion (I001 ò I002..), NO del grid no siempre coincide con el que tiene el foco
            item = self.grid_componentes.selection()[0]
            # Obtener todos los valores de la fila
            valores = self.grid_componentes.item(item, "values")
            # "Orden" está en la columna 0 guardo el orden que tenia
            orden_item = valores[0]
            # ----------------------------------------------------------------

            # ----------------------------------------------------------------
            try:
                # Elimino el item anterior en la tabla aux_presup
                self.principal.var_obj_presupuestos.eliminar_auxpresup(self.clave)
            except Exception:
                self.principal.var_obj_funcionnew.mostrar_error()
                return
            # ----------------------------------------------------------------

        else:

            # ALTA

            # Creo el nuevo numero de orden para el item ingresado
            total = len(self.grid_componentes.get_children())
            orden_item = total + 1

        # vuelvo a cero la bandera de modificacion
        self.alta_modif_aux = 0

        # -----------------------------------------------------------------
        dic_deta_auxpresup = {
            "Id": "",                                                          # Id
            "ax_orden": orden_item,                                            # orden elemento
            "ax_proved": self.sv_proveedor.get(),                              # nombre del proveedor
            "ax_codcomp": self.sv_codigo_componente.get(),                     # codigo componente del proveedor
            "ax_componente": self.sv_componente.get(),                         # descripcion del componente
            "ax_iva": self.sv_combo_tasa_iva.get(),                            # tasa iva del componente
            "ax_cantidad": self.sv_cantidad_vendida.get(),                     # cantidad del componente
            "ax_neto_dolar": self.sv_neto_dolar.get(),                         # costo neto componente en dolares
            "ax_total_presup": self.sv_precio_final_xcanti.get(),              # total del presupuesto real
            "ax_total_redondo": self.principal.sv_total_item_redondo.get(),    # total en pesos redondeo
            "ax_total_ganancia": self.sv_importe_ganancia_xcanti.get(),        # total ganancia
            "ax_total_costos": self.sv_costo_bruto_pesos_xcanti.get()          # total costos
        }
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        try:
            # Insertamos el componente en el auxilliar de presupuesto (aux_presup)
            self.principal.var_obj_presup.insertar_auxpresup(dic_deta_auxpresup)
            ultimo_tabla_id = self.principal.var_obj_presup.traer_ultimo(0)
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error()
            return
        # -----------------------------------------------------------------

        self.llena_grilla_auxiliar(ultimo_tabla_id)

        # -------------------------------------------------------------------
        # dejar en blanco todos los entrys del articulo
        self.limpiar_entrys_parcial()

        # Limpia los totales que se calculan a partir de que estoy cargando un nuevo componente
        self.flimpiar_importes_componente()

        # desactivar los entrys de la parte dos (componentes)
        self.estado_entrys_crud_dos("disabled")
        # limpiar los totales del componente
        self.principal.pestana_1.flimpiar_totales_finales()
        # -------------------------------------------------------------------

        self.calcular("totalpresupuesto")

        self.principal.status.set_status("✔ Item ingresado correctamente", "ok")

        # Botones de la parte componentes vuelven a estado inicial (+ compon... - compon...
        self.estado_botones_dos("normal")
        self.entry_componente.focus()

    def estado_entrys_crud_dos(self, estado):

        """ Activo entrys de la parte de (componentes) cuando presiono boton (+ componente) """

        self.entry_componente.configure(state=estado)
        self.combo_tasa_iva.configure(state=estado)
        self.entry_cantidad.configure(state=estado)
        self.entry_neto_dolar.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_codigo_componente.configure(state=estado)
        self.entry_total_item_redondo.configure(state=estado)
        self.btn_bus_art.configure(state=estado)
        self.text_especificaciones.configure(state=estado)

        # self.btn_detalle_precio_articulo.configure(state=estado)
        # self.btn_reset_componente.configure(state=estado)

    def freset_articulo(self):

        if self.entry_componente["state"] == "disabled":
            self.principal.status.set_status("⚠ Ingreso componentes esta inactivo", "warn")
            return
        r = messagebox.askquestion("Reset", "Confirma cancelar componente?", parent=self)
        if r == messagebox.NO:
            return

        self.limpiar_entrys_parcial()
        self.flimpiar_importes_componente()
        self.estado_entrys_crud_dos("disabled")
        self.estado_botones_dos("normal")

        # self.alta_modif_aux = 0
        # self.alta_modif_presup = 0
        # self.entry_componente.focus()

    def fsubir_uno(self):

        # Obtengo Id del item actual en el grid I001....
        actual = self.grid_componentes.focus()
        if not actual:
            messagebox.showwarning("Aviso", "No hay nada seleccionado", parent=self)
            return

        # 👉 (posicion del item - arranca en cero) índice del ítem dentro de su contenedor(posición) (1, 2, 3....
        #     orden de posicion o renglon
        index = self.grid_componentes.index(actual)
        if index == 0:
            self.principal.status.set_status("ℹ Llegamos al principio...", "info")

            self.grid_componentes.focus(actual)
            self.grid_componentes.selection_set(actual)
            return

        if index > 0:
            # muevo toda la inea actual a un index menor, o sea para arriba
            # Las ' ' son el parámetro el parent(padre) del ítem dentro del Treeview - vacio es raiz
            self.grid_componentes.move(actual, '', index - 1)
            self.grid_componentes.see(actual)  # 👈 también acá

        # me posiciono en el que estaba pero un renglon mas arriba
        self.grid_componentes.focus(actual)
        self.grid_componentes.selection_set(actual)

        self.freordenar(self.grid_componentes)

    def fbajar_uno(self):

        # Obtengo Id del item actual en el grid I001....
        actual = self.grid_componentes.focus()
        if not actual:
            messagebox.showwarning("Aviso", "No hay nada seleccionado", parent=self)
            return

        # 👉 (posicion del item - arranca en cero) índice del ítem dentro de su contenedor(posición) (1, 2, 3....
        #     orden de posicion o renglon
        index = self.grid_componentes.index(actual)
        total = len(self.grid_componentes.get_children())

        if index >= total - 1:
            self.principal.status.set_status("ℹ Llegamos al final", "info")
            self.grid_componentes.focus(actual)
            self.grid_componentes.selection_set(actual)
            return

        if index < total - 1:
            # muevo toda la inea actual a un index mayor, o sea para abajo
            # Las ' ' son el parámetro el parent(padre) del ítem dentro del Treeview - vacio es raiz
            # .see lo hace visible dentro del grid or si os vamos muy para abajo fuera del area visible
            self.grid_componentes.move(actual, '', index + 1)
            self.grid_componentes.see(actual)  # 👈 clave

        # me posiciono en el que estaba pero un renglon mas abajo
        self.grid_componentes.focus(actual)
        self.grid_componentes.selection_set(actual)

        self.freordenar(self.grid_componentes)

    def freordenar(self, tree):

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


    # -----------------------------------------------------------------------------
    # ENTRYS DE COMPONENTES
    # ------------------------------------------------------------------------------

    def entrys_componentes(self):

        for c in range(13):
            self.frame_componentes.grid_columnconfigure(c, weight=1, minsize=30)

        # BOTON DE BUSQUEDA DE ARTICULO SI CORRESPONDE AL DETALLE
        self.photo_bus_art = Image.open('ver.png')
        self.photo_bus_art = self.photo_bus_art.resize((18, 18), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_art = ImageTk.PhotoImage(self.photo_bus_art)
        self.btn_bus_art = tk.Button(self.frame_componentes, text="", image=self.photo_bus_art, command=self.fbusart,
                                     bg="grey", fg="white")
        self.btn_bus_art.grid(row=0, column=0, padx=2, pady=2, sticky="e")

        # ENTRY ARTICULO
        self.lbl_componente = tk.Label(self.frame_componentes, text="Componente: ", bg="#81EBCD", justify="left")
        self.lbl_componente.grid(row=0, column=1, padx=2, pady=2, sticky="w")
        self.entry_componente = tk.Entry(self.frame_componentes, textvariable=self.sv_componente, width=40, justify="left")
        self.entry_componente.grid(row=0, column=2, padx=2, pady=2, sticky="e")
        self.sv_componente.trace("w", lambda *args: limitador(self.sv_componente, 95))

        # COMBO TASA IVA
        self.lbl_combo_tasa_iva = tk.Label(self.frame_componentes, justify="left", foreground="black", bg="#81EBCD", text="IVA %")
        self.lbl_combo_tasa_iva.grid(row=0, column=3, padx=2, pady=2, sticky="w")
        self.combo_tasa_iva = ttk.Combobox(self.frame_componentes, textvariable=self.sv_combo_tasa_iva, state='readonly', width=6)
        self.combo_tasa_iva['value'] = ["21.00", "10.50"]
        self.combo_tasa_iva.current(0)
        self.combo_tasa_iva.grid(row=0, column=4, padx=2, pady=2, sticky="w")
        self.combo_tasa_iva.bind('<Tab>', lambda e: self.calcular("completo"))

        # ENTRY CANTIDAD
        self.lbl_cantidad = tk.Label(self.frame_componentes, text="Cant.: ", bg="#81EBCD", justify="left")
        self.lbl_cantidad.grid(row=0, column=7, padx=2, pady=2, sticky="w")
        self.entry_cantidad = tk.Entry(self.frame_componentes, textvariable=self.sv_cantidad_vendida, width=4, justify="right")
        self.entry_cantidad.grid(row=0, column=8, padx=2, pady=2, sticky="e")
        self.entry_cantidad.config(validate="key", validatecommand=self.vcmd)
        self.entry_cantidad.bind("<FocusOut>", lambda e: self.principal.var_obj_funcionnew.corregir_al_salir(self.entry_cantidad))
        self.entry_cantidad.bind('<Tab>', lambda e: self.calcular("completo"))

        # ENTRY NETO DOLAR
        self.lbl_neto_dolar = tk.Label(self.frame_componentes, text="Neto dolar: ", bg="#81EBCD", justify="left")
        self.lbl_neto_dolar.grid(row=0, column=9, padx=2, pady=2, sticky="w")
        self.entry_neto_dolar = tk.Entry(self.frame_componentes, textvariable=self.sv_neto_dolar, width=8, justify="right")
        self.entry_neto_dolar.grid(row=0, column=10, padx=2, pady=2, sticky="e")
        self.entry_neto_dolar.config(validate="key", validatecommand=self.vcmd)
        self.entry_neto_dolar.bind("<FocusOut>", lambda e: self.principal.var_obj_funcionnew.corregir_al_salir(self.entry_neto_dolar))
        self.entry_neto_dolar.bind('<Tab>', lambda e: self.calcular("completo"))

        self.lbl_proved = tk.Label(self.frame_componentes, text="Prov.: ", bg="#81EBCD", justify="left")
        self.lbl_proved.grid(row=0, column=11, padx=2, pady=2, sticky="w")
        self.entry_proved = tk.Entry(self.frame_componentes, textvariable=self.sv_proveedor, width=15, justify="left")
        self.entry_proved.grid(row=0, column=12, padx=2, pady=2, sticky="w")

        self.lbl_codigo_componente = tk.Label(self.frame_componentes, text="Cod.: ", bg="#81EBCD", justify="left")
        self.lbl_codigo_componente.grid(row=0, column=13, padx=2, pady=2, sticky="w")
        self.entry_codigo_componente = tk.Entry(self.frame_componentes, textvariable=self.sv_codigo_componente,
                                                width=15, justify="left")
        self.entry_codigo_componente.grid(row=0, column=14, padx=2, pady=2, sticky="w")

        for widg in self.frame_componentes.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')

    def entrys_precios_componentes(self):

        fff = tkfont.Font(family="Arial", size=9, weight="bold")

        for c in range(12):
            self.frame_precios_articulo.grid_columnconfigure(c, weight=1, minsize=30)

        # COSTO PESOS CON IVA
        self.lbl_costo_pesos_bruto_unidad = tk.Label(self.frame_precios_articulo, text="Costo Unidad: ", bg="#81EBCD", justify="left")
        self.lbl_costo_pesos_bruto_unidad.grid(row=2, column=0, padx=1, pady=2, sticky="w")
        self.lbl_costo_pesos_bruto_unidad2 = tk.Label(self.frame_precios_articulo,
                                                      textvariable=self.sv_costo_bruto_pesos_unidad, width=10, font=fff,
                                                      fg="blue", justify="right")
        self.lbl_costo_pesos_bruto_unidad2.grid(row=2, column=1, padx=1, pady=2, sticky="e")

        # COSTO PESOS CON IVA * CANTIDAD
        self.lbl_costo_bruto_pesos_xcanti = tk.Label(self.frame_precios_articulo, text="Costo total: ", bg="#81EBCD", justify="left")
        self.lbl_costo_bruto_pesos_xcanti.grid(row=2, column=2, padx=1, pady=2, sticky="w")
        self.lbl_costo_bruto_pesos_xcanti2 = tk.Label(self.frame_precios_articulo,
                                                      textvariable=self.sv_costo_bruto_pesos_xcanti, width=10, font=fff,
                                                      fg="blue", justify="right")
        self.lbl_costo_bruto_pesos_xcanti2.grid(row=2, column=3, padx=1, pady=2, sticky="e")

        # IMPORTE PESOS GANANCIA * CANTIDAD
        self.lbl_importe_ganancia_xcanti = tk.Label(self.frame_precios_articulo, text="Ganancia: ", bg="#81EBCD", justify="left")
        self.lbl_importe_ganancia_xcanti.grid(row=2, column=4, padx=1, pady=2, sticky="w")
        self.lbl_importe_ganancia_xcanti2 = tk.Label(self.frame_precios_articulo,
                                                     textvariable=self.sv_importe_ganancia_xcanti, width=10, fg="blue",
                                                     font=fff, justify="right")
        self.lbl_importe_ganancia_xcanti2.grid(row=2, column=5, padx=1, pady=2, sticky="e")

        # PRECIO DE VENTA
        self.lbl_precio_final_xcanti = tk.Label(self.frame_precios_articulo, text="Precio venta: ", bg="#81EBCD", justify="left")
        self.lbl_precio_final_xcanti.grid(row=2, column=6, padx=1, pady=2, sticky="w")
        self.lbl_precio_final_xcanti2 = tk.Label(self.frame_precios_articulo, textvariable=self.sv_precio_final_xcanti,
                                                 width=10, fg="blue", font=fff, justify="right")
        self.lbl_precio_final_xcanti2.grid(row=2, column=7, padx=1, pady=2, sticky="e")

        # Redondeo del total del Item
        self.lbl_total_item_redondo = tk.Label(self.frame_precios_articulo, text="Redondeo: ", bg="#81EBCD", justify="left")
        self.lbl_total_item_redondo.grid(row=2, column=8, padx=1, pady=2, sticky="w")
        self.entry_total_item_redondo = tk.Entry(self.frame_precios_articulo,
                                                 textvariable=self.principal.sv_total_item_redondo, width=15,
                                                 justify="right")
        self.entry_total_item_redondo.grid(row=2, column=9, padx=1, pady=2, sticky="e")
        self.entry_total_item_redondo.config(validate="key", validatecommand=self.vcmd)
        self.entry_total_item_redondo.bind("<FocusOut>", lambda e: self.principal.var_obj_funcionnew.corregir_al_salir(self.entry_total_item_redondo))
        self.entry_total_item_redondo.bind('<Tab>', lambda e: self.calcular("precio_venta_unidad"))

        self.btn_detalle_precio_articulo = tk.Button(self.frame_precios_articulo, text="Detalle precio",
                                                     command=self.fdetalle_precio_articulo, width=15, bg='blue',
                                                     fg='white')
        self.btn_detalle_precio_articulo.grid(row=2, column=10, padx=5, pady=2, sticky="w")

        self.btn_articulo = tk.Button(self.frame_precios_articulo, text="Articulos", command=self.fver_articulos,
                                      width=16, bg='blue', fg='white')
        self.btn_articulo.grid(row=2, column=11, padx=5, pady=2, sticky="w")

        for widg in self.frame_precios_articulo.winfo_children():
            widg.grid_configure(padx=3, pady=3, sticky='nsew')


    def fbusart(self):

        """ Paso los parametros de busqueda - Tabla, el string de busqueda y en que campos debe hacerse """

        que_busco = "articulos WHERE INSTR(descripcion, '" + self.sv_componente.get() + "') > 0" \
                    + " OR INSTR(marca, '" + self.sv_componente.get() + "') > 0" \
                    + " OR INSTR(rubro, '" + self.sv_componente.get() + "') > 0" \
                    + " OR INSTR(codbar, '" + self.sv_componente.get() + "') > 0" \
                    + " OR INSTR(codigo, '" + self.sv_componente.get() + "') > 0" \
                    + " ORDER BY rubro, marca, descripcion"

        valores_new = self.principal.var_obj_funcionnew.ventana_selec("articulos", "descripcion", "codigo","costodolar",
                                                            "Descripcion", "Codigo", "Precio dolar neto", que_busco,
                                                            "Orden: Rubro+Marca+Descripcion", "S")

        for item in valores_new:

            self.sv_componente.set(value=item[2]) # d<escripcion del articulo
            self.sv_combo_tasa_iva.set(value=item[7])
            self.sv_neto_dolar.set(value=item[6])

        self.entry_componente.focus()
        self.entry_componente.icursor(tk.END)


    # # -----------------------------------------------------------
    # # VALIDACION ENTRADAS
    # # -----------------------------------------------------------

    def limpiar_entrys_parcial(self):

        """ Vacio los entrys relacionados con la carga del componente y totales """

        self.sv_componente.set(value="")
        self.combo_tasa_iva.current(0)
        self.sv_cantidad_vendida.set(value="0")
        self.sv_neto_dolar.set(value="0.00")
        self.sv_proveedor.set(value="")
        self.sv_codigo_componente.set(value="")
        self.sv_costo_neto_pesos_unidad.set(value="0.00")
        self.sv_costo_neto_pesos_xcanti.set(value="0.00")
        # self.sv_total_item_redondo.set(value="0.00")
        self.text_especificaciones.delete('1.0', 'end')


    # # -----------------------------------------------------------------
    # # GRIDS
    # # -----------------------------------------------------------------

    def llena_grilla_auxiliar(self, set_foco):

        # Limpio el Grid
        for item in self.grid_componentes.get_children():
            self.grid_componentes.delete(item)

        try:
        # aa = 0
        # if aa== 0:

            datos = self.principal.var_obj_presup.consultar_presupuestos("aux_presup", self.filtro_activo_auxiliar)
            orden = 1

            for row in datos:
                self.grid_componentes.insert("", "end", text=row[0], values=(orden, row[2], row[3], row[4],
                                                             row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
                orden += 1
            if len(self.grid_componentes.get_children()) > 0:
                   self.grid_componentes.selection_set(self.grid_componentes.get_children()[0])

            # Controles --------------------------------------------------------
            # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
            children = self.grid_componentes.get_children()
            # Si no hay filas (grid vacio), salgo sin intentar seleccionar
            if not children:
                self.principal.status.set_status("ℹ Grid vacio...", "info")
                return

            # Si foco vacío (no hay foco), voy al ultimo de la grilla - caso contrario, voy a la clave
            # que se haya enviado en set_foco para dejar el puntero
            if not set_foco:
                # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
                posicion = children[-1]  # ultimo
                # posicion = children[0] # primero
                self.grid_componentes.focus_set()
                self.grid_componentes.focus(posicion)
                self.grid_componentes.selection_set(posicion)
                self.grid_componentes.see(posicion)
            else:
                for item in children:
                    texto = self.grid_componentes.item(item, "text")
                    # print(str(set_foco) + " " + str(texto))
                    if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                        self.grid_componentes.update_idletasks()
                        self.grid_componentes.focus_set()
                        self.grid_componentes.selection_set(item)
                        self.grid_componentes.focus(item)
                        self.grid_componentes.see(item)
                        break

        except Exception:

            self.principal.var_obj_funcionnew.mostrar_error("Fallo en carga de GRID auxiliar")
            return


    # ----------------------------------------------------------
    # CALCULOS
    # ----------------------------------------------------------

    def calcular(self, que_campo):

        # --- CORRECCIÓN de 2do nivel: forzar formato válido en todos los entrys
        # que se van a usar y verificar variables calculadas en los stringvars
        self.principal.var_obj_funcionnew.corregir_al_salir(self.entry_neto_dolar)
        self.principal.var_obj_funcionnew.corregir_al_salir(self.entry_cantidad)
        self.principal.var_obj_funcionnew.corregir_al_salir(self.combo_tasa_iva)
        self.principal.var_obj_funcionnew.corregir_al_salir(self.principal.pestana_1.entry_tasa_ganancia)
        # variables no entry.. calculadas
        self.principal.var_obj_funcionnew.corregir_valor(self.principal.sv_valor_dolar_presup.get())
        # ---------------------------------------------------------------------------------

        ii = 1
        #try:
        if ii == 1:

            if que_campo == "completo":
                print(self.sv_cantidad_vendida.get())
                # -------------------------------------------------------------
                # 1 - Costo neto unidad pesos y cantidad
                self.sv_costo_neto_pesos_unidad.set(value=str(round(float(self.sv_neto_dolar.get()) *
                                                                    float(self.principal.sv_valor_dolar_presup.get()), 2)))
                self.sv_costo_neto_pesos_xcanti.set(value=str(round(float(self.sv_neto_dolar.get()) *
                                                                    float(self.principal.sv_valor_dolar_presup.get()) *
                                                                    float(self.sv_cantidad_vendida.get()), 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 2 - Importe IVA unidad y cantidad
                importe_iva = (((float(self.sv_neto_dolar.get()) * float(self.principal.sv_valor_dolar_presup.get())) *
                              float(self.sv_combo_tasa_iva.get())) / 100)

                importe_ivaxcanti = ((((float(self.sv_neto_dolar.get()) *
                                        float(self.principal.sv_valor_dolar_presup.get())) *
                                        float(self.sv_combo_tasa_iva.get())) / 100) *
                                        float(self.sv_cantidad_vendida.get()))

                self.sv_importe_iva_unidad.set(value=str(round(importe_iva, 2)))
                self.sv_importe_iva_xcanti.set(value=str(round(importe_ivaxcanti, 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 3 - Costo BRUTO pesos unidad y cantidad

                # Costo en Pesos mas IVA * unidad
                self.sv_costo_bruto_pesos_unidad.set(value= str(round(float(self.sv_costo_neto_pesos_unidad.get()) +
                                                            float(self.sv_importe_iva_unidad.get()), 2)))
                # Costo en Pesos  ms IVA * unidad * la cantidad vendida
                self.sv_costo_bruto_pesos_xcanti.set(value= str(round((float(self.sv_costo_neto_pesos_unidad.get()) +
                                                            float(self.sv_importe_iva_unidad.get())) *
                                                            float(self.sv_cantidad_vendida.get()), 2)))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 4 - Importe ganancia por unidad y por cantidad

                ganancia_unidad = round(((float(self.sv_costo_bruto_pesos_unidad.get()) *
                                          float(self.principal.sv_tasa_ganancia.get())) / 100), 2)

                ganancia_xcanti = round((((float(self.sv_costo_bruto_pesos_unidad.get()) *
                                           float(self.principal.sv_tasa_ganancia.get())) / 100) *
                                           float(self.sv_cantidad_vendida.get())), 2)

                self.sv_importe_ganancia_unidad.set(value=str(ganancia_unidad))
                self.sv_importe_ganancia_xcanti.set(value=str(ganancia_xcanti))
                # -------------------------------------------------------------

                # -------------------------------------------------------------
                # 4 - Total final del componente por unidad y cantidad

                total_final_unidad = (float(self.sv_importe_ganancia_unidad.get()) +
                                      float(self.sv_costo_bruto_pesos_unidad.get()))
                total_final_xcanti = total_final_unidad *  float(self.sv_cantidad_vendida.get())

                self.sv_precio_final_unidad.set(value=str(round(total_final_unidad, 2)))
                self.sv_precio_final_xcanti.set(value=str(round(total_final_xcanti, 2)))
                # -------------------------------------------------------------

            if que_campo == "totalpresupuesto":

                """ Guardo todos los items que compnen el presupuesto """
                try:
                    datos = self.principal.var_obj_presup.consultar_presupuestos("aux_presup", "aux_presup")
                except Exception:
                    self.principal.var_obj_funcionnew.mostrar_error()
                    return

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
                self.principal.sv_total_ganancia.set(value=str(round(sumatot_ganancia, 2)))
                # total costos con IVA incluido
                self.principal.sv_total_costos.set(value=str(round(sumatot_costos, 2)))
                # Total del presupuesto real - sin redondeo
                self.principal.sv_total_presup.set(value=str(round(sumatot_presu)))
                # total presupuesto redondeado
                self.principal.sv_total_presup_redondo.set(value=str(round(sumatot_redondo, 2)))

        else:
        #except:

            messagebox.showerror("Error", "Error en funcion de Calculos - revise entradas numericas", parent=self)
            return

    # Esta limpia los totales que se calculan cuando cargo un componente nuevo a la tabla auxiliar
    def flimpiar_importes_componente(self):

        self.sv_precio_final_unidad.set(value="0.00")
        self.sv_precio_final_xcanti.set(value="0.00")
        self.sv_importe_ganancia_unidad.set(value="0.00")
        self.sv_importe_ganancia_xcanti.set(value="0.00")
        self.sv_costo_bruto_pesos_unidad.set(value="0.00")
        self.sv_costo_bruto_pesos_xcanti.set(value="0.00")
        self.text_especificaciones.delete('1.0', 'end')


    # -------------------------------------------------------------
    # VARIAS
    # -------------------------------------------------------------

    # Accede directamente al modulo de articulos completo
    def fver_articulos(self):

        vent = tk.Toplevel()
        vent.title("ABM Articulos")
        # Asigno la clase Ventart que esta en articulos.py a la variable app
        app = ClaseArticulos(vent)
        app.mainloop()

    # Muestra en una pantalla flotante, el detalle minucioso de los componentes del precio del articulo
    def fdetalle_precio_articulo(self):

        # PANTALLA FLOTANTE DETALLE PRECIO DEL ARTICULO

        self.pantalla_detalle = tk.Toplevel()

        self.pantalla_detalle.protocol("WM_DELETE_WINDOW", self.fcerrar5)
        self.pantalla_detalle.geometry('580x260+600+400')
        self.pantalla_detalle.config(bg='#27BEF5', padx=5, pady=5)
        self.pantalla_detalle.resizable(1, 1)
        self.pantalla_detalle.title("Detalle precio del articulo")
        self.pantalla_detalle.focus_set()
        self.pantalla_detalle.grab_set()
        self.pantalla_detalle.transient(master=self.master)

        self.frame_detalle_articulo=tk.LabelFrame(self.pantalla_detalle, text="", foreground="#CF09BD")

        # -------------------------------------------------------------------
        # DOLARES

        # DOLARES Precio neto
        lbl_neto_dolar_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"DOLARES - Costo neto x unidad: U$S {self.sv_neto_dolar.get()} - "
             f"Total costo neto: U$S"
             f" {float(self.sv_neto_dolar.get())*float(self.sv_cantidad_vendida.get())}")
        lbl_neto_dolar_articulo.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        # DOLARES Importe del IVA
        self.iva_en_dolares = round(float(self.sv_neto_dolar.get()) * (float(self.sv_combo_tasa_iva.get()) / 100), 2)

        lbl_iva_dolar_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"DOLARES - Importe IVA x unidad: U$S {self.iva_en_dolares} - "
             f"Total IVA: U$S {self.iva_en_dolares * float(self.sv_cantidad_vendida.get())}")
        lbl_iva_dolar_articulo.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # DOLARES Precio Bruto (con VIA)
        lbl_bruto_dolar_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"DOLARES - Costo bruto x unidad: U$S {self.iva_en_dolares+float(self.sv_neto_dolar.get())} - "
             f"Total costo bruto: U$S "
             f"{float(self.sv_cantidad_vendida.get()) * (self.iva_en_dolares+float(self.sv_neto_dolar.get()))}")
        lbl_bruto_dolar_articulo.grid(row=2, column=0, padx=5, pady=2, sticky="w")

        # ------------------------------------------------------------------
        # PESOS

        # PESOS Precio neto
        lbl_neto_pesos_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"PESOS -      Costo neto x unidad: $ {self.sv_costo_neto_pesos_unidad.get()} - "
             f"Total costo neto: $ {self.sv_costo_neto_pesos_xcanti.get()}")
        lbl_neto_pesos_articulo.grid(row=3, column=0, padx=5, pady=2, sticky="w")

        # PESOS Importe del IVA
        self.iva_en_pesos = round(float(self.sv_costo_neto_pesos_unidad.get()) * (float(self.sv_combo_tasa_iva.get()) / 100), 2)

        lbl_iva_pesos_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"PESOS -      Importe IVA x unidad: $ {self.iva_en_pesos} - "
             f"Total IVA: $ {self.iva_en_pesos * float(self.sv_cantidad_vendida.get())}")
        lbl_iva_pesos_articulo.grid(row=4, column=0, padx=5, pady=2, sticky="w")

        # PESOS Precio Bruto (con VIA)
        lbl_bruto_pesos_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"PESOS -      Costo bruto x unidad: $ {self.iva_en_pesos+float(self.sv_costo_neto_pesos_unidad.get())} - "
             f"Total costo bruto: $ "
             f"{float(self.sv_cantidad_vendida.get()) * (self.iva_en_pesos+float(self.sv_costo_neto_pesos_unidad.get()))}")
        lbl_bruto_pesos_articulo.grid(row=5, column=0, padx=5, pady=2, sticky="w")

        # GANANCIA PESOS
        importe_ganancia_unidad =round(float(self.sv_costo_bruto_pesos_unidad.get()) *
                                       (float(self.principal.sv_tasa_ganancia.get()) / 100), 2)
        importe_ganancia_total = importe_ganancia_unidad * float(self.sv_cantidad_vendida.get())
        lbl_ganancia_pesos_articulo=tk.Label(self.frame_detalle_articulo,
        text=f"PESOS -      Ganancia: % {self.principal.sv_tasa_ganancia.get()} - "
             f"Importe ganancia x unidad: "
             f"{importe_ganancia_unidad} - "
             f"Total Importe ganancia: "
             f"{importe_ganancia_total}")
        lbl_ganancia_pesos_articulo.grid(row=6, column=0, padx=5, pady=2, sticky="w")

        # PRECIO VENTA FINAL EN PESOS
        precio_venta_final_unidad = round(float(self.sv_costo_bruto_pesos_unidad.get()) *
                                          (1 + (float(self.principal.sv_tasa_ganancia.get()) / 100)), 2)
        precio_venta_final_total = round(precio_venta_final_unidad * float(self.sv_cantidad_vendida.get()), 2)

        lbl_precio_pesos_venta_final=tk.Label(self.frame_detalle_articulo,
        text=f"PESOS -      Precio venta final x unidad: {precio_venta_final_unidad} - "
             f"Precio venta final: {precio_venta_final_total} - Redondeo: {self.principal.sv_total_item_redondo.get()}")
        lbl_precio_pesos_venta_final.grid(row=7, column=0, padx=5, pady=2, sticky="w")

        self.frame_detalle_articulo.pack(side="top", fill="both", expand=1, padx=5, pady=5)

        self.btn_volver_pantalla = tk.Button(self.frame_detalle_articulo, text="Volver", command=self.fcerrar5, width=22,
                                    bg="blue", fg="white")
        self.btn_volver_pantalla.grid(row=8, column=0, padx=10, pady=2, sticky="nsew")

        self.pantalla_detalle.mainloop()

    def fcerrar5(self):
        self.pantalla_detalle.destroy()
        self.master.grab_set()
        self.master.focus_set()






"""
    ejemplo de uso funcion mostrar error
    
        try:
            id_ref = self.principal.varCotiz.insertar_resuventa(dic_resuventas)
        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Cerrar_Venta_alta_resumen - ValueError", str(e))
            return
        except Exception:
            self.principal.var_obj_funcionnew.mostrar_error("Error Cerrar_Venta_alta_resumen")
            return
        else:
            self.principal.status.set_status("✔ Ingreso nueva venta guardada correctamente", "Ok")
            # Refresco el GRID - voy al foco del nuevo
            self.principal.pestana_1.llena_grilla_ventas(id_ref)  # paso solo el foco, sin datos de busqueda


        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        self.set_status("✔ Registro guardado correctamente", "ok")
        self.set_status("🗑 Cliente eliminado", "ok")
        self.set_status("⚠ CUIT incorrecto", "warn")
        self.set_status("❌ Error al guardar", "error")
        self.set_status("ℹ Buscando clientes...", "info")
"""


