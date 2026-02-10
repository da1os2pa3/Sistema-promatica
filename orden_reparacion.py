from funciones import *
from ordenrepar_ABM import *
from funcion_new import *
# ---------------------------------------------
import os
import tkinter.font as tkFont
from datetime import date, datetime
# ---------------------------------------------
# from tkinter import *
import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import *
# ---------------------------------------------
from PIL import Image, ImageTk
from PDF_clase import *
from fpdf import FPDF
from tktooltip import ToolTip

class OrdenesRepara(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=1100, height=730)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # -----------------------------------------------------------------------
        # Instanciaciones

        """ Creo una instancia de clientes_ABM de la clase datosClientes
        -A varGarantia le paso la pantalla para poder usar los parent en los mensajes de messagebox
        -A varFuncion_new, le paso tambien la pantalla por el mismo motivo."""

        self.varOrdenes = DatosOrdenRepar(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ------------------------------------------------------------------------

        # ------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos toddo el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Asignamos medidas a la ventana
        wventana = 1100
        hventana = 740
        # Aplicamos la siguiente formula para ubicarla en el centro
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # VARIABLES Y ORDEN INICIAL
        # ---------------------------------------------------------------------
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # ---------------------------------------------------------------------
        # Este codigo sirve para poner el foco en un item determinado
        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_orden.identify_row(0)
        # self.grid_orden.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_orden.focus(item)
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno.
        # Otras funciones para manejar los elementos seleccionados incluyen:
        1- selection_add(): añade elementos a la selección.
        2- selection_remove(): remueve elementos de la selección.
        3- selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        4- selection_toggle(): cambia la selección de un elemento. """
        # ----------------------------------------------------------------------

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        # validar: funcion en funciones.py que valida que lo ingresado sea un numeo o "-" o "."
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ------------------------------------------------------------------
        # STRINGVARS -*-
        # ------------------------------------------------------------------

        self.strvar_buscar_orden = tk.StringVar(value="")
        self.strvar_nombre_cliente = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_cli_datosmas = tk.StringVar(value="")
        self.strvar_cli_deuda = tk.StringVar(value="0")
        self.strvar_nro_orden = tk.StringVar(value="0")
        self.strvar_fecha_ingreso = tk.StringVar(value="")
        self.strvar_fecha_egreso = tk.StringVar(value="")

        self.strvar_equ_ingresa = tk.StringVar(value="")
        self.strvar_equ_grupo = tk.StringVar(value="")
        self.strvar_equipo_procesador = tk.StringVar(value="")
        self.strvar_equipo_ram = tk.StringVar(value="")
        self.strvar_equipo_discos = tk.StringVar(value="")
        self.strvar_equipo_sist_oper = tk.StringVar(value="")
        self.strvar_equipo_ing_obser = tk.StringVar(value="")
        self.strvar_equ_accesorios = tk.StringVar(value="")
        self.strvar_equ_estado = tk.StringVar(value="")

        self.strvar_cuentas = tk.StringVar(value="")
        self.strvar_requerido = tk.StringVar(value="")
        self.strvar_presupuesto = tk.StringVar(value="")
        self.strvar_partes = tk.StringVar(value="")
        self.strvar_total_partes = tk.StringVar(value="0")
        self.strvar_total_manodeobra = tk.StringVar(value="0")
        self.strvar_tot_final = tk.StringVar(value="0.00")
        self.strvar_retirado = tk.StringVar(value="N")

        self.strvar_buscostring = tk.StringVar(value="")

        # Estadisticas
        self.strvar_estad_total = tk.StringVar(value="0")
        self.strvar_estad_pendi = tk.StringVar(value="0")
        self.strvar_estad_mesact = tk.StringVar(value="0")
        self.strvar_estad_pespendi = tk.StringVar(value="0")
        self.strvar_estad_pesmesact = tk.StringVar(value="0")
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TREEVIEW -*-
        # ------------------------------------------------------------------
        self.frame_superior = Frame(self.master)
        self.frame_tvw_ordenes = LabelFrame(self.frame_superior, text="", foreground="#CF09BD")
        self.frame_treeview()
        self.grid_orden.pack(side="top", fill="both", expand=0, padx=3, pady=2)
        self.frame_tvw_ordenes.pack(side="left", fill="both", expand=1, padx=3, pady=2)
        self.frame_superior.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # BOTONES SOBRE EL GRID (CRUD - IMPRESION - MOVIMIENTOS EN LA GRILLA
        # ----------------------------------------------------------------------
        self.frame_botones_grid = LabelFrame(self.master, text="")
        self.cuadro_botones_grid()
        self.frame_botones_grid.pack(side="top", fill="both", expand=0, padx=3, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS -*-
        # ------------------------------------------------------------------
        self.frame_entrys_uno = LabelFrame(self.master, text="")
        self.cuadro_entrys()
        self.frame_entrys_dos.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS DATOS EQUIPO
        # ------------------------------------------------------------------
        self.frame_entrys_uno_bis = LabelFrame(self.master, text="", bd=3, relief="ridge")
        self.cuadro_entrys_equipo()
        self.frame_entrys_uno_bis.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS DATOS EQUIPO DOS
        # ------------------------------------------------------------------
        self.frame_entrys_tres = LabelFrame(self.master, text="", bd=3, relief="ridge")
        self.cuadro_entrys_equipo_dos()
        self.frame_entrys_tres.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS DATOS EQUIPO TRES
        # ------------------------------------------------------------------
        self.frame_entrys_cuatro = LabelFrame(self.master, text="", bd=3, relief="ridge")
        self. cuadro_entrys_equipo_tres()
        self.frame_entrys_cuatro.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS DATOS EQUIPO PIE
        # ------------------------------------------------------------------
        self.frame_entrys_cinco = LabelFrame(self.master, text="")
        self.cuadro_entrys_pie()
        self.frame_entrys_cinco.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS DATOS EQUIPO TOTALES
        # ------------------------------------------------------------------
        self.frame_entrys_seis = LabelFrame(self.master, text="")
        self.cuadro_entrys_totales()
        self.frame_entrys_seis.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # ESTADOS -*-
    # --------------------------------------------------------------------------------

    def on_write(self, *args):

        # Transforma a mayuscula la S de equipo retirado
        texto = self.strvar_retirado.get()
        self.strvar_retirado.set(texto.upper())

    def estado_inicial(self):

        self.filtro_activo = "orden_repara WHERE fin_retirada = 'N' ORDER BY fecha_ingreso ASC"
        self.var_Id = -1
        self.alta_modif = 0

        self.limpiar_text()
        self.estado_botones("normal")
        self.habilitar_text("disabled")

    def habilitar_text(self, estado):

        self.btn_guardar_orden.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_nro_orden.configure(state=estado)
        self.entry_equ_ingresa.configure(state=estado)
        self.grupo_tipo_equipo.configure(state=estado)
        self.entry_equipo_procesador.configure(state=estado)
        self.entry_equipo_ram.configure(state=estado)
        self.entry_equipo_discos.configure(state=estado)
        self.entry_equipo_sist_oper.configure(state=estado)
        self.entry_equipo_ing_obser.configure(state=estado)

        self.entry_equ_accesorios.configure(state=estado)
        self.entry_equ_estado.configure(state=estado)
        self.entry_cuentas.configure(state=estado)
        self.entry_partes.configure(state=estado)
        self.entry_requerido.configure(state=estado)
        self.text_anotaciones.configure(state=estado)
        self.text_trabajo_realizado.configure(state=estado)
        self.text_diagnostico.configure(state=estado)
        self.entry_presupuesto.configure(state=estado)
        self.entry_total_partes.configure(state=estado)
        self.entry_total_manodeobra.configure(state=estado)
        self.entry_retirado.configure(state=estado)

        # Activar Browse
        self.grid_orden['selectmode'] = 'browse'
        self.grid_orden.bind("<Double-Button-1>", self.DobleClickGrid)

    def limpiar_text(self):

        self.entry_nombre_cliente.delete(0, END)

        self.strvar_codigo_cliente.set(value="0")
        self.strvar_cli_datosmas.set(value="")

        # tratamiento de nro de orden
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.delete(0, END)
        self.entry_nro_orden.configure(state="disabled")
        self.strvar_fecha_ingreso.set(value="")
        self.strvar_fecha_egreso.set(value="")

        self.strvar_equ_ingresa.set(value="")
        self.strvar_equipo_procesador.set(value="")
        self.strvar_equipo_ram.set(value="")
        self.strvar_equipo_discos.set(value="")
        self.strvar_equipo_sist_oper.set(value="")
        self.strvar_equipo_ing_obser.set(value="")

        self.strvar_equ_accesorios.set(value="")
        self.strvar_equ_estado.set(value="")
        self.strvar_cuentas.set(value="")
        self.strvar_requerido.set(value="")
        self.strvar_partes.set(value="")
        self.text_anotaciones.delete('1.0', 'end')
        self.text_trabajo_realizado.delete('1.0', 'end')
        self.text_diagnostico.delete('1.0', 'end')
        self.strvar_presupuesto.set(value="")
        self.strvar_partes.set(value="")
        self.strvar_total_partes.set(value="0.00")
        self.strvar_total_manodeobra.set(value="0.00")
        self.strvar_retirado.set(value="N")

        self.grupo_tipo_equipo.set("")
        self.grupo_tipo_equipo.current(0)

        self.strvar_cli_deuda.set(value="0")

    def estado_botones(self, estado):

        self.btn_nueva_orden.configure(state=estado)
        self.btn_editar_orden.configure(state=estado)
        self.btn_borrar_orden.configure(state=estado)
        self.btn_ver_orden.configure(state=estado)
        self.btn_imprime_orden.configure(state=estado)
        self.btn_buscar_orden.configure(state=estado)
        self.btn_showall_orden.configure(state=estado)
        self.btn_no_retiradas.configure(state=estado)
        self.btn_estadistica.configure(state=estado)
        self.btn_inf_tecnico.configure(state=estado)
        self.entry_buscar_orden.configure(state=estado)

    def estado_botones_global(self):

        self.entry_nombre_cliente.configure(state="normal")

        self.btn_cancelar_orden.configure(state="normal")
        self.btn_guardar_orden.configure(state="normal")

        self.btn_bus_cli.configure(state="normal")

        self.entry_equ_ingresa.configure(state="normal")
        self.entry_equipo_procesador.configure(state="normal")
        self.entry_equipo_ram.configure(state="normal")
        self.entry_equipo_discos.configure(state="normal")
        self.entry_equipo_sist_oper.configure(state="normal")
        self.entry_equipo_ing_obser.configure(state="normal")

        self.entry_equ_accesorios.configure(state="normal")
        self.entry_equ_estado.configure(state="normal")
        self.entry_cuentas.configure(state="normal")
        self.entry_partes.configure(state="normal")
        self.entry_requerido.configure(state="normal")
        self.text_anotaciones.configure(state="normal")
        self.text_trabajo_realizado.configure(state="normal")
        self.text_diagnostico.configure(state="normal")
        self.entry_presupuesto.configure(state="normal")
        self.entry_total_partes.configure(state="normal")
        self.entry_total_manodeobra.configure(state="normal")
        self.entry_retirado.configure(state="normal")

        self.grupo_tipo_equipo.configure(state="normal")
        self.btn_nueva_orden.configure(state="disabled")
        self.btn_editar_orden.configure(state="disabled")
        self.btn_borrar_orden.configure(state="disabled")
        self.btn_ver_orden.configure(state="disabled")
        self.btn_imprime_orden.configure(state="disabled")
        self.btn_buscar_orden.configure(state="disabled")
        self.entry_buscar_orden.configure(state="disabled")
        self.btn_showall_orden.configure(state="disabled")
        self.btn_no_retiradas.configure(state="disabled")
        self.btn_estadistica.configure(state="disabled")
        self.btn_inf_tecnico.configure(state="disabled")

    # --------------------------------------------------------------------------------
    # GRILLA -*-
    # --------------------------------------------------------------------------------

    def llena_grilla(self, ult_tabla_id):

        datos = self.varOrdenes.consultar_ordenes(self.filtro_activo)

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal_ingreso = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d %H:%M'),
                                                          "hora_si")
            forma_normal_egreso = None

            if row[3] != None:

                forma_normal_egreso  = fecha_str_reves_normal(self, datetime.strftime(row[3], '%Y-%m-%d %H:%M'),
                                                              "hora_si")

            """ Leo en la lista datos todos los registros y los inserto en la grilla
            1- El "" nos da quien es el padre de este nodo (ninguno en este caso (nace en la raiz))
            2- "end" es en que posicion va (en este caso al final)
            3 - tags=color > color de las filas intercaladas
            4- text=row[0] - es el Id de la Tabla (21, 22, 23..."""

            self.grid_orden.insert("", "end", tags=color, text=row[0], values=(row[1], forma_normal_ingreso,
                                    forma_normal_egreso, row[4], row[5], (row[23]+row[22]), row[23], row[22]))

        """ get_children() obtiene todos los datos hijos. El [0] indica que obtiene el elemento
        correspondiente a ese indice o sea el Id I001, si no le pongo nada, trae todos los Id)
        Esto parece hacer que el treeview se posicione en el primero """

        if len(self.grid_orden.get_children()) > 0:
            self.grid_orden.selection_set(self.grid_orden.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)
        # ----------------------------------------------------------------------------------

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:

            """ Si NO es blanco - 
                regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_orden.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_orden.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
            de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
            con las siguientes instrucciones. """

            self.grid_orden.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_orden.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_orden.yview(self.grid_orden.index(rg))
        else:
            # En caso de que el parametro sea "" muevo el puntero al final del GRID
            self.muevo_puntero_topend("END")

    def llena_grilla2(self, argg2):

        datos = self.varOrdenes.consultar_ordenes(argg2)

        for row in datos:
            self.grid_orden.insert("", END, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))

        if len(self.grid_orden.get_children()) > 0:
            self.grid_orden.selection_set(self.grid_orden.get_children()[0])

    def limpiar_Grid(self):

        for item in self.grid_orden.get_children():
            self.grid_orden.delete(item)

    # --------------------------------------------------------------------------------
    # CRUD *
    # --------------------------------------------------------------------------------

    def fVer_orden(self):

        # -------------------------------------------------------------
        self.selected = self.grid_orden.focus()
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Ver", "No hay nada seleccionado", parent=self)
            return

        # self.alta_modif = 2
        # self.var_Id = self.clave  #puede traer -1 , en ese caso seria un alta

        self.habilitar_text('normal')
        self.limpiar_text()

        # Trae un solo el registro solicitado mediante su ID. Metodo de ordenrepar_ABM.
        datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)

        # Asigno el valor de la lista al campo desde la posicion 1
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.insert(0, datos_registro_selec[1])
        self.entry_nro_orden.configure(state="disabled")

        # Aqui analizo que no me llegue desde la TABLA ninguna fecha en "none" dado que ese es un error
        # en el caso que venga, la convierto datetime con la fecha actual tanto para ingreso como para egreso.
        una_fecha = (datos_registro_selec[2])
        self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
        self.strvar_fecha_ingreso.set(self.fecha_final)

        # Tratamiento de fecha de egreso porque aca puede venir None
        if (datos_registro_selec[3]) == None:
            self.strvar_fecha_egreso.set(value="")
        else:
            una_fecha = (datos_registro_selec[3])
            self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
            self.strvar_fecha_egreso.set(self.fecha_final)

        #self.filtro_activo = "orden_repara WHERE Id = " + str(self.clave)
        #valores = self.varOrdenes.consultar_ordenes(self.filtro_activo)

        # Aqui analizo que no me llegue desde la TABLA ninguna fecha en "none" dado que ese es un error
        # en el caso que venga, la convierto datetime con la fecha actual tanto para ingreso como para egreso.
        una_fecha = (datos_registro_selec[2])
        self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
        self.strvar_fecha_ingreso.set(self.fecha_final)

        # Tratamiento de fecha de egreso porque aca puede venir None
        if (datos_registro_selec[3]) == None:
            self.strvar_fecha_egreso.set(value="")
        else:
            una_fecha = (datos_registro_selec[3])
            self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
            self.strvar_fecha_egreso.set(self.fecha_final)

        self.strvar_codigo_cliente.set(datos_registro_selec[4])
        self.strvar_nombre_cliente.set(value=datos_registro_selec[5])

        self.strvar_equ_ingresa.set(value=datos_registro_selec[6])
        self.strvar_equ_grupo.set(value=datos_registro_selec[7])
        self.strvar_equipo_procesador.set(value=datos_registro_selec[8])
        self.strvar_equipo_ram.set(value=datos_registro_selec[9])
        self.strvar_equipo_discos.set(value=datos_registro_selec[10])
        self.strvar_equipo_sist_oper.set(value=datos_registro_selec[11])
        self.strvar_equipo_ing_obser.set(value=datos_registro_selec[11])
        self.strvar_equ_accesorios.set(value=datos_registro_selec[13])
        self.strvar_equ_estado.set(value=datos_registro_selec[14])

        self.strvar_cuentas.set(value=datos_registro_selec[15])
        self.strvar_requerido.set(value=datos_registro_selec[16])
        self.text_diagnostico.insert(END, datos_registro_selec[17])
        self.strvar_presupuesto.set(value=datos_registro_selec[18])
        self.text_trabajo_realizado.insert(END, datos_registro_selec[19])
        self.strvar_partes.set(value=datos_registro_selec[20])
        self.text_anotaciones.insert(END, datos_registro_selec[21])
        self.strvar_total_manodeobra.set(value=datos_registro_selec[22])
        self.strvar_total_partes.set(value=datos_registro_selec[23])
        self.strvar_retirado.set(value=datos_registro_selec[24])

        self.strvar_cli_deuda.set(value=str(self.fTraedeuda(self.strvar_codigo_cliente.get())))

        # traer los datos del cliente direccion y telefono - Datos mas -
        retorno = self.varOrdenes.buscar_entabla("clientes WHERE codigo = '" + self.strvar_codigo_cliente.get() + "'")

        for item in retorno:
            self.strvar_cli_datosmas.set(value=str(item[4] + ' - tel: ' + item[8] + ' / ' + item[9]))

        self.sumar_totalfinal()
        self.habilitar_text('disabled')

    def fNueva(self):

        self.alta_modif = 1

        #  Desactivar Browse
        self.grid_orden['selectmode'] = 'none'
        self.grid_orden.bind("<Double-Button-1>", self.fNo_modifique)

        # Preparo estado de pantalla
        self.estado_botones_global()
        self.limpiar_text()
        self.entry_nombre_cliente.focus()

        # traer ultimo numero de orden mas uno para ingresar
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.insert(0, (int(self.varOrdenes.traer_ultimo(1)) + 1))
        self.entry_nro_orden.configure(state="disabled")

        # Fecha y hora de ingreso
        una_fecha = datetime.now()
        self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
        self.strvar_fecha_ingreso.set(self.fecha_final)
        self.entry_retirado.insert(0, "N")

    def fModificar_orden(self):

        # Preparo claves de registros para puntero en el grid posterior
        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_orden.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # Preparo variables y estado pantalla
        self.alta_modif = 2

        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        self.estado_botones_global()
        self.limpiar_text()

        # Trae un solo el registro solicitado mediante su ID. Metodo de ordenrepar_ABM.
        datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)

        # Asigno el valor de la lista al campo desde la posicion 1
        self.entry_nro_orden.configure(state="normal")
        self.entry_nro_orden.insert(0, datos_registro_selec[1])
        self.entry_nro_orden.configure(state="disabled")

        # Aqui analizo que no me llegue desde la TABLA ninguna fecha en "none" dado que ese es un error
        # en el caso que venga, la convierto datetime con la fecha actual tanto para ingreso como para egreso.
        una_fecha = (datos_registro_selec[2])
        self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
        self.strvar_fecha_ingreso.set(self.fecha_final)

        # Tratamiento de fecha de egreso porque aca puede venir None
        if (datos_registro_selec[3]) == None:
            self.strvar_fecha_egreso.set(value="")
        else:
            una_fecha = (datos_registro_selec[3])
            self.fecha_final = una_fecha.strftime("%d-%m-%Y %H:%M:%S")
            self.strvar_fecha_egreso.set(self.fecha_final)

        self.strvar_codigo_cliente.set(datos_registro_selec[4])
        self.strvar_nombre_cliente.set(value=datos_registro_selec[5])

        self.strvar_equ_ingresa.set(value=datos_registro_selec[6])
        self.strvar_equ_grupo.set(value=datos_registro_selec[7])
        self.strvar_equipo_procesador.set(value=datos_registro_selec[8])
        self.strvar_equipo_ram.set(value=datos_registro_selec[9])
        self.strvar_equipo_discos.set(value=datos_registro_selec[10])
        self.strvar_equipo_sist_oper.set(value=datos_registro_selec[11])
        self.strvar_equipo_ing_obser.set(value=datos_registro_selec[11])
        self.strvar_equ_accesorios.set(value=datos_registro_selec[13])
        self.strvar_equ_estado.set(value=datos_registro_selec[14])

        self.strvar_cuentas.set(value=datos_registro_selec[15])
        self.strvar_requerido.set(value=datos_registro_selec[16])
        self.text_diagnostico.insert(END, datos_registro_selec[17])
        self.strvar_presupuesto.set(value=datos_registro_selec[18])
        self.text_trabajo_realizado.insert(END, datos_registro_selec[19])
        self.strvar_partes.set(value=datos_registro_selec[20])
        self.text_anotaciones.insert(END, datos_registro_selec[21])
        self.strvar_total_manodeobra.set(value=datos_registro_selec[22])
        self.strvar_total_partes.set(value=datos_registro_selec[23])
        self.strvar_retirado.set(value=datos_registro_selec[24])

        self.strvar_cli_deuda.set(value=str(self.fTraedeuda(self.strvar_codigo_cliente.get())))

        # traer los datos del cliente direccion y telefono - Datos mas -
        retorno = self.varOrdenes.buscar_entabla("clientes WHERE codigo = '" + self.strvar_codigo_cliente.get() +"'")

        for item in retorno:
            self.strvar_cli_datosmas.set(value=str(item[4]+' - tel: '+item[8]+' / '+item[9]))

        self.sumar_totalfinal()
        self.entry_nombre_cliente.focus()

    def fEliminar_orden(self):

        # ---------------------------------------------------------------------------
        # Preparo claves para puntero en el GRid
        # selecciono el Id del Tv grid I010, IB020
        self.selected = self.grid_orden.focus()
        self.selected_ant = self.grid_orden.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no es el mismo del Tv - 23, 12, 33, ....
        self.clave = self.grid_orden.item(self.selected, 'text')
        self.clave_ant = self.grid_orden.item(self.selected_ant, 'text')
        # ---------------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el GRID
        valores = self.grid_orden.item(self.selected, 'values')

        data = "Id: "+str(self.clave)+" Nº: "+valores[0]+" Cliente: " + valores[4]

        r = messagebox.askquestion("Cuidado", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Aviso", "Eliminacion cancelada", parent=self)
            return

        self.varOrdenes.eliminar_orden(self.clave)

        messagebox.showinfo("Aviso", "Registro eliminado correctamente", parent=self)
        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar_orden(self):

        # --------------------------------------------------------------------------------
        # VALIDAR

        # no permito codigo ni nombre de cliente en blanco
        if int(self.strvar_codigo_cliente.get()) == 0 or self.strvar_nombre_cliente.get() == "":
            messagebox.showerror("Cuidado", "Faltan datos de cliente - verifique", parent=self)
            return
        # el numero de orden no puede ser vacio
        if self.strvar_nro_orden.get() == 0:
            messagebox.showerror("Cuidado", "Faltan numero de orden - verifique", parent=self)
            return
        # el -retirada- debe ser S o N
        if self.strvar_retirado.get() != "S" and self.strvar_retirado.get() != "N":
            messagebox.showerror("Cuidado", "El informe de retirada valor no aceptado, solo S o N - "
                                            "verifique", parent = self)
            return
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # Guardo las claves para los punteros
        # guardo el Id del Tv en selected para ubicacion del foco a posteriori - I001, IB10
        self.selected = self.grid_orden.focus()
        # Guardo el Id del registro de la Tabla (no es el mismo que el otro, este puedo verlo en la TABLA - 21, 12..)
        self.clave = self.grid_orden.item(self.selected, 'text')
        # --------------------------------------------------------------------------------

        if self.alta_modif == 1:

            self.varOrdenes.insertar_orden(self.strvar_nro_orden.get(), datetime.now(),
                self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(), self.strvar_equ_ingresa.get(),
                self.strvar_equ_grupo.get(), self.strvar_equipo_procesador.get(), self.strvar_equipo_ram.get(),
                self.strvar_equipo_discos.get(), self.strvar_equipo_sist_oper.get(), self.strvar_equipo_ing_obser.get(),
                self.strvar_equ_accesorios.get(), self.strvar_equ_estado.get(), self.strvar_cuentas.get(),
                self.strvar_requerido.get(), self.text_diagnostico.get(1.0, 'end-1c'),
                self.strvar_presupuesto.get(), self.text_trabajo_realizado.get(1.0, 'end-1c'),
                self.strvar_partes.get(), self.text_anotaciones.get(1.0, 'end-1c'),
                self.strvar_total_manodeobra.get(), self.strvar_total_partes.get(), self.strvar_retirado.get())

            messagebox.showinfo("Aviso", "Nuevo registro creado correctamente", parent=self)

        else:

            transformo_fecha_ingreso = datetime
            transformo_fecha_ingreso = transformo_fecha_ingreso.strptime(self.strvar_fecha_ingreso.get(),
                                                                         "%d-%m-%Y %H:%M:%S")

            if self.strvar_retirado.get() == "S":
                transformo_fecha_egreso = datetime.now()
            else:
                transformo_fecha_egreso = ""

            self.varOrdenes.modificar_orden(self.var_Id, self.strvar_nro_orden.get(), transformo_fecha_ingreso,
                transformo_fecha_egreso, self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                self.strvar_equ_ingresa.get(), self.strvar_equ_grupo.get(), self.strvar_equipo_procesador.get(),
                self.strvar_equipo_ram.get(), self.strvar_equipo_discos.get(), self.strvar_equipo_sist_oper.get(),
                self.strvar_equipo_ing_obser.get(), self.strvar_equ_accesorios.get(), self.strvar_equ_estado.get(),
                self.strvar_cuentas.get(), self.strvar_requerido.get(),
                self.text_diagnostico.get(1.0, 'end-1c'), self.strvar_presupuesto.get(),
                self.text_trabajo_realizado.get(1.0, 'end-1c'), self.strvar_partes.get(),
                self.text_anotaciones.get(1.0, 'end-1c'), self.strvar_total_manodeobra.get(),
                self.strvar_total_partes.get(), self.strvar_retirado.get())

            messagebox.showinfo("Aviso", "La modificacion del registro fue exitosa", parent=self)

        # Ordenar estado de pantalla
        self.limpiar_Grid()
        self.habilitar_text("normal")
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.estado_botones("normal")

        # Acomodar punteros en el GRID
        if self.alta_modif == 1:
            ultimo_tabla_id = self.varOrdenes.traer_ultimo(0)
            self.llena_grilla(ultimo_tabla_id)
        elif self.alta_modif == 2:
            self.llena_grilla(self.clave)

        # Cierre
        self.alta_modif = 0
        self.btn_nueva_orden.focus()

    # --------------------------------------------------------------------------------
    # VARIAS *
    # --------------------------------------------------------------------------------

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.habilitar_text("normal")
            self.limpiar_text()
            self.habilitar_text("disabled")
            self.estado_botones("normal")

    def fSalir(self):
        self.master.destroy()

    def DobleClickGrid(self, event):
        self.fModificar_orden()

    def fNo_modifique(self, event):
        return "break"

    def fImprimir(self):
        self.creopdf()

    def fNoretiradas(self):

        self.filtro_activo = "orden_repara WHERE fin_retirada = 'N' ORDER BY fecha_ingreso ASC"
        self.limpiar_Grid()
        self.llena_grilla("")

    def fEstadistica(self):

        self.filtro_anterior = self.filtro_activo
        self.filtro_activo = "orden_repara ORDER BY fecha_ingreso"

        datos = self.varOrdenes.consultar_ordenes(self.filtro_activo)

        total_ordenes = 0
        total_orden_pendientes = 0
        total_pesos_pendientes = 0
        total_orden_mesactual = 0
        total_pesos_mesactual = 0

        for row in datos:

            fecha_orden = datetime.date(row[2])
            mes_orden = fecha_orden.month
            ano_orden = fecha_orden.year
            mes_comparacion = date.today().month
            ano_comparacion = date.today().year

            total_ordenes += 1

            if row[24] == "N":
                total_orden_pendientes += 1
                total_pesos_pendientes += (float(row[23])+float(row[22]))

            if mes_comparacion == mes_orden and ano_comparacion == ano_orden:
                total_orden_mesactual += 1
                total_pesos_mesactual += (float(row[23])+float(row[22]))

         # if len(self.grid_orden.get_children()) > 0:
         #    self.grid_orden.selection_set(self.grid_orden.get_children()[0])

        total_pesos_mesactual = formatear_cifra(total_pesos_mesactual)
        total_pesos_pendientes = formatear_cifra(total_pesos_pendientes)

        self.strvar_estad_total.set(value=str(total_ordenes))
        self.strvar_estad_pendi.set(value=str(total_orden_pendientes))
        self.strvar_estad_mesact.set(value=str(total_orden_mesactual))
        self.strvar_estad_pespendi.set(value=str(total_pesos_pendientes))
        self.strvar_estad_pesmesact.set(value=str(total_pesos_mesactual))

        self.pantalla_estad = Toplevel()
        self.pantalla_estad.geometry('220x180+1200+200')
        self.pantalla_estad.transient(master=self.master)
        self.pantalla_estad.config(bg='light green', padx=5, pady=5)
        self.pantalla_estad.resizable(False, False)
        self.pantalla_estad.title("Estadisticas")

        # muestro la imagen en el frame
        self.lbl_total_ordenes1 = Label(self.pantalla_estad, text="Total ordenes: ", bg="light blue",
                                        relief="ridge", bd=5)
        self.lbl_total_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_total, bg="plum1",
                                        relief="ridge", bd=5)
        self.lbl_pendi_ordenes1 = Label(self.pantalla_estad, text="Ordenes pendientes: ", bg="light blue",
                                        relief="ridge", bd=5)
        self.lbl_pendi_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_pendi, bg="plum1",
                                        relief="ridge", bd=5)
        self.lbl_pespendi_ordenes1 = Label(self.pantalla_estad, text="Pesos pendientes: ", bg="light blue",
                                           relief="ridge", bd=5)
        self.lbl_pespendi_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_pespendi, bg="plum1",
                                           relief="ridge", bd=5)
        self.lbl_mesact_ordenes1 = Label(self.pantalla_estad, text="Ordenes mes actual: ", bg="light blue",
                                         relief="ridge", bd=5)
        self.lbl_mesact_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_mesact, bg="plum1",
                                         relief="ridge", bd=5)
        self.lbl_pesmesact_ordenes1 = Label(self.pantalla_estad, text="Pesos mes actual: ", bg="light blue",
                                            relief="ridge", bd=5)
        self.lbl_pesmesact_ordenes2 = Label(self.pantalla_estad, textvariable=self.strvar_estad_pesmesact, bg="plum1",
                                            relief="ridge", bd=5)

        self.lbl_total_ordenes1.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_total_ordenes2.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_pendi_ordenes1.grid(row=1, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_pendi_ordenes2.grid(row=1, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_pespendi_ordenes1.grid(row=2, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_pespendi_ordenes2.grid(row=2, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_mesact_ordenes1.grid(row=3, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_mesact_ordenes2.grid(row=3, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_pesmesact_ordenes1.grid(row=4, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_pesmesact_ordenes2.grid(row=4, column=1, padx=5, pady=3, sticky="nsew")

        for widg in self.pantalla_estad.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

        self.pantalla_estad.grab_set()
        self.pantalla_estad.focus_set()

        mainloop()

        self.filtro_activo = self.filtro_anterior

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    # --------------------------------------------------------------------------------
    # PUNTEROS *
    # --------------------------------------------------------------------------------

    def muevo_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_orden.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_orden.selection_set(rg)
            # pone el primero Id
            self.grid_orden.focus(rg)
            # lle principio del treeview con esta instruccion que encontre
            self.grid_orden.yview(self.grid_orden.index(self.grid_orden.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_orden.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_orden.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_orden.focus(rg)
            # lleva el foco al final del treeview
            self.grid_orden.yview(self.grid_orden.index(self.grid_orden.get_children()[-1]))

    def fToparch(self):
        self.muevo_puntero_topend('TOP')

    def fFinarch(self):
        self.muevo_puntero_topend('END')

    def fShowall(self):

        self.filtro_activo = "orden_repara ORDER by fecha_ingreso ASC"
        self.limpiar_Grid()
        self.llena_grilla("")

    def fTraedeuda(self, codigo_cli):

        # Trae la deuda del cliente que se selecciona
        datos = self.varOrdenes.suma_deuda(codigo_cli)

        sumasaldo = 0
        for row in datos:
            sumasaldo += row[3] - row[4]

        return(sumasaldo)

    # ----------------------------------------------------------------------------
    # SEL -*-
    # ----------------------------------------------------------------------------

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
            self.strvar_cli_datosmas.set(value=str(item[4] + ' - tel: ' + item[8] + ' / ' + item[9]))

        self.strvar_cli_deuda.set(value=str(self.fTraedeuda(self.strvar_codigo_cliente.get())))
        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    # ----------------------------------------------------------------------------
    # BUSQUEDAS -*-
    # ----------------------------------------------------------------------------

    def fFiltrar_orden(self):

        if len(self.strvar_buscar_orden.get()) <= 0:
            messagebox.showwarning("Alerta", "No ingreso busqueda", parent=self)
            self.entry_buscar_orden.focus()
            return

        se_busca = self.strvar_buscar_orden.get()

        self.filtro_activo = "orden_repara WHERE INSTR(or_nombre_cliente, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(or_num_orden, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(equ_grupo, '" + se_busca + "') > 0" \
                             + " OR " + "INSTR(equ_ingresa, '" + se_busca + "') > 0"

 #       + " OR " + "INSTR(equ_descripcion, '" + se_busca + "') > 0" \

        self.retorno = self.varOrdenes.buscar_entabla(self.filtro_activo)

        self.limpiar_Grid()
        self.llena_grilla2(self.filtro_activo)

    # ----------------------------------------------------------------------------
    # CALCULOS -*-
    # ----------------------------------------------------------------------------

    def sumar_totalfinal(self):

        #try:
        aaa = 0
        if aaa == 0:

            # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
            if not control_forma(list(self.strvar_total_partes.get())):
                self.strvar_total_partes.set(value="0")
                self.entry_total_partes.focus()
                return
            if not control_forma(list(self.strvar_total_manodeobra.get())):
                self.strvar_total_manodeobra.set(value="0")
                self.entry_total_manodeobra.focus()
                return

            # Control de valor en blanco o solo un . o -
            if (self.strvar_total_partes.get() == "" or self.strvar_total_partes.get() == "."
                    or self.strvar_total_partes.get() == "-"):
                self.strvar_total_partes.set(value="0")
            if (self.strvar_total_manodeobra.get() == "" or self.strvar_total_manodeobra.get() == "."
                    or self.strvar_total_manodeobra.get() == "-"):
                self.strvar_total_manodeobra.set(value="0")

            # control de valor en cero o si tiene mas de dos decimales lo trunco a dos
            if float(self.strvar_total_partes.get()) == 0:
                self.strvar_total_partes.set(value="0")
            else:
                self.strvar_total_partes.set(value=str(round(float(self.strvar_total_partes.get()), 2)))
            if float(self.strvar_total_manodeobra.get()) == 0:
                self.strvar_total_manodeobra.set(value="0")
            else:
                self.strvar_total_manodeobra.set(value=str(round(float(self.strvar_total_manodeobra.get()), 2)))

            v1 = float(self.strvar_total_partes.get())
            v2 = float(self.strvar_total_manodeobra.get())

            self.strvar_tot_final.set(value=str(round((v1 + v2), 2)))

        else:
        #except:

            messagebox.showerror("Error", "Revise datos ingresados", parent=self)
            self.entry_total_partes.focus()
            return

    # ************************************************************************************
    # TREEVIEW
    # ************************************************************************************

    def frame_treeview(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_ordenes)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        # Este es el TV donde aparecen las ordenes de reparacion
        self.grid_orden = ttk.Treeview(self.frame_tvw_ordenes, height=6, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5", "col6", "col7", "col8"))
        self.grid_orden.bind("<Double-Button-1>", self.DobleClickGrid)
        #self.grid_orden.bind("<ButtonRelease-3>", self.muestradatos)

        self.grid_orden.column("#0", width=40, anchor="center")
        self.grid_orden.column("col1", width=70, anchor="e")
        self.grid_orden.column("col2", width=130, anchor="center")
        self.grid_orden.column("col3", width=130, anchor="center")
        self.grid_orden.column("col4", width=50, anchor="e")
        self.grid_orden.column("col5", width=300, anchor="w")
        self.grid_orden.column("col6", width=90, anchor="e")
        self.grid_orden.column("col7", width=90, anchor="e")
        self.grid_orden.column("col8", width=90, anchor="e")

        self.grid_orden.heading("#0", text="Id", anchor="center")
        self.grid_orden.heading("col1", text="Nº Orden", anchor="center")
        self.grid_orden.heading("col2", text="Fecha/Hora Ingreso", anchor="center")
        self.grid_orden.heading("col3", text="Fecha/Hora Egreso", anchor="center")
        self.grid_orden.heading("col4", text="Cod.", anchor="center")
        self.grid_orden.heading("col5", text="Cliente", anchor="center")
        self.grid_orden.heading("col6", text="Total", anchor="center")
        self.grid_orden.heading("col7", text="Partes", anchor="center")
        self.grid_orden.heading("col8", text="M.O.", anchor="center")

        self.grid_orden.tag_configure('oddrow', background='light grey')
        self.grid_orden.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_ordenes, orient="horizontal")
        scroll_y = Scrollbar(self.frame_tvw_ordenes, orient="vertical")
        self.grid_orden.config(xscrollcommand=scroll_x.set)
        self.grid_orden.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_orden.xview)
        scroll_y.config(command=self.grid_orden.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_orden['selectmode'] = 'browse'

    # ************************************************************************************
    # METODOS PARA BOTONES Y ENTRYS
    # ************************************************************************************

    def cuadro_botones_grid(self):

        """
        for c in range(7):
            self.frame_botones_grid.grid_columnconfigure(c, weight=1, minsize=140)

        Muy bueno, es como que formatea e grid de antemano y ya no necesito width, solo mle pongo la cantidad de
        columnas.

       🔹 ¿Qué significa weight en grid_columnconfigure?
           weight define cómo se reparte el espacio extra cuando el contenedor (el frame) es más grande que la
           suma mínima de sus columnas. 👉 En otras palabras: qué columnas se estiran y cuánto, cuando sobra espacio.

           ⚖️ Ejemplo con pesos distintos :
            frame.grid_columnconfigure(0, weight=2)
            frame.grid_columnconfigure(1, weight=1)
            Si sobra espacio:
            columna 0 recibe el doble que la 1Si pongo 2 """

        for c in range(7):
            self.frame_botones_grid.grid_columnconfigure(c, weight=1, minsize=140)

        # ------------------------------------------------------
        # BUSCAR
        img = Image.open("buscar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        lbl_buscar_orden = Label(self.frame_botones_grid, text=" Buscar:: ", compound="left")
        lbl_buscar_orden.image = icono
        lbl_buscar_orden.config(image=icono)
        lbl_buscar_orden.grid(row=0, column=0, padx=4, pady=2, sticky="nsew")
        self.entry_buscar_orden = Entry(self.frame_botones_grid, textvariable=self.strvar_buscar_orden, width=19)
        self.entry_buscar_orden.grid(row=0, column=1, padx=4, pady=3, sticky="nsew")
        ToolTip(self.entry_buscar_orden, msg="Ingrese un nombre a buscar")

        # ------------------------------------------------------
        # FILTRAR
        img = Image.open("filtrar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_buscar_orden = Button(self.frame_botones_grid, text=" Filtrar", width=19, command=self.fFiltrar_orden,
                                       bg="CadetBlue", fg="black", compound="left")
        self.btn_buscar_orden.image = icono
        self.btn_buscar_orden.config(image=icono)
        self.btn_buscar_orden.grid(row=0, column=2, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_buscar_orden, msg="Activa el filtro segùn el nombre ingresado en buscar")

        # ------------------------------------------------------
        # NO RETIRADAS
        img = Image.open("no_retirada.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_no_retiradas = Button(self.frame_botones_grid, text="No retiradas", width=19,
                                       command=self.fNoretiradas, bg="CadetBlue", fg="black", compound="left")
        self.btn_no_retiradas.image = icono
        self.btn_no_retiradas.config(image=icono)
        self.btn_no_retiradas.grid(row=0, column=3, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_no_retiradas, msg="Se mostraran solamente las ordenes no retiradas")

        # ------------------------------------------------------
        # SHOW ALL
        img = Image.open("ver_todo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_showall_orden = Button(self.frame_botones_grid, text="Mostrar todo", width=19, command=self.fShowall,
                                        bg="CadetBlue", fg="black", compound="left")
        self.btn_showall_orden.image = icono
        self.btn_showall_orden.config(image=icono)
        self.btn_showall_orden.grid(row=0, column=4, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_showall_orden, msg="Se muestran todas las ordenes")

        # ------------------------------------------------------
        # ESTADISTICAS
        img = Image.open("estadisticas.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_estadistica = Button(self.frame_botones_grid, text=" Estadistica", width=19, command=self.fEstadistica,
                                      bg="CadetBlue", fg="black", compound="left")
        self.btn_estadistica.image = icono
        self.btn_estadistica.config(image=icono)
        self.btn_estadistica.grid(row=0, column=5, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_estadistica, msg="Resumen de Ordenes segun estados")

        # ------------------------------------------------------
        # INFORME TECNICO
        img = Image.open("impresora.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_inf_tecnico = Button(self.frame_botones_grid, text=" Informe Tècnico", width=18,
                                      command=self.fInfTecnico, bg="CadetBlue", fg="black", compound="left")
        self.btn_inf_tecnico.image = icono
        self.btn_inf_tecnico.config(image=icono)
        self.btn_inf_tecnico.grid(row=0, column=6, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_inf_tecnico, msg="Impresion informe tecnico para el cliente-que trabajo hicimos-")
        # ------------------------------------------------------

        # ------------------------------------------------------
        # TOPE Y FIN DE ARCHIVO
        self.photo_top_arch = Image.open('toparch.png')
        self.photo_top_arch = self.photo_top_arch.resize((25, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_top_arch = ImageTk.PhotoImage(self.photo_top_arch)
        self.btn_top_arch = Button(self.frame_botones_grid, text="", image=self.photo_top_arch, command=self.fToparch,
                                   bg="grey", fg="white")
        self.btn_top_arch.grid(row=0, column=7, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_top_arch, msg="Ir a principio de archivo")
        self.photo_fin_arch = Image.open('finarch.png')
        self.photo_fin_arch = self.photo_fin_arch.resize((25, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_fin_arch = ImageTk.PhotoImage(self.photo_fin_arch)
        self.btn_fin_arch = Button(self.frame_botones_grid, text="", image=self.photo_fin_arch, command=self.fFinarch,
                                   bg="grey", fg="white")
        self.btn_fin_arch.grid(row=1, column=7, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_fin_arch, msg="Ir al final del archivo")
        # ------------------------------------------------------

        # ------------------------------------------------------
        # NUEVA ORDEN
        img = Image.open("archivo-nuevo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_nueva_orden = Button(self.frame_botones_grid, text="Nueva", width=18, command=self.fNueva, bg="blue",
                                      fg="white", compound="left")
        self.btn_nueva_orden.image = icono
        self.btn_nueva_orden.config(image=icono)
        self.btn_nueva_orden.grid(row=1, column=0, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_nueva_orden, msg="Ingresar una nueva Orden de trabajo")

        # ------------------------------------------------------
        # EDITAR ORDEN
        img = Image.open("editar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_editar_orden = Button(self.frame_botones_grid, text="Editar", width=18, command=self.fModificar_orden,
                                       bg="blue", fg="white", compound="left")
        self.btn_editar_orden.image = icono
        self.btn_editar_orden.config(image=icono)
        self.btn_editar_orden.grid(row=1, column=1, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_editar_orden, msg="Editar Orden para modificar")

        # ------------------------------------------------------
        # VER ORDEN
        img = Image.open("ver.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_ver_orden = Button(self.frame_botones_grid, text=" Ver", width=18, command=self.fVer_orden,
                                    bg="blue", fg="white", compound="left")
        self.btn_ver_orden.image = icono
        self.btn_ver_orden.config(image=icono)
        self.btn_ver_orden.grid(row=1, column=2, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_ver_orden, msg="Visualizar una Orden")

        # ------------------------------------------------------
        # ELIMINAR ORDEN
        img = Image.open("eliminar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_borrar_orden = Button(self.frame_botones_grid, text=" Eliminar", width=18, command=self.fEliminar_orden,
                                       bg="red", fg="white", compound="left")
        self.btn_borrar_orden.image = icono
        self.btn_borrar_orden.config(image=icono)
        self.btn_borrar_orden.grid(row=1, column=3, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_borrar_orden, msg="Eliminar una Orden de trabajo")

        # ------------------------------------------------------
        # GUARDAR ORDEN
        img = Image.open("guardar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_guardar_orden = Button(self.frame_botones_grid, text=" Guardar", width=18, command=self.fGuardar_orden,
                                        bg="green", fg="white", compound="left")
        self.btn_guardar_orden.image = icono
        self.btn_guardar_orden.config(image=icono)
        self.btn_guardar_orden.grid(row=1, column=4, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_guardar_orden, msg="Guardar una nueva Orden de trabajo")

        # ------------------------------------------------------
        # CANCELAR ORDEN
        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_cancelar_orden = Button(self.frame_botones_grid, text=" Cancelar", width=18, command=self.fCancelar,
                                         bg="black", fg="white", compound="left")
        self.btn_cancelar_orden.image = icono
        self.btn_cancelar_orden.config(image=icono)
        self.btn_cancelar_orden.grid(row=1, column=5, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_cancelar_orden, msg="Cancelar lo que se este haciendo")
        # ------------------------------------------------------

        """# Esta es otra forma de asignar icono al boton
        # img = Image.open("impresora.png")
        # img = img.resize((24, 24))
        # icono = ImageTk.PhotoImage(img)"""

        # ------------------------------------------------------
        # IMPRIMIR ORDEN
        self.img2 = Image.open("impresora.png").resize((18, 18))
        self.icono2 = ImageTk.PhotoImage(self.img2)
        self.btn_imprime_orden = Button(self.frame_botones_grid, text=" Imprimir Orden", compound="left",
                                        command=self.fImprimir, bg='#5F9EF5', fg="white")
        self.btn_imprime_orden.image = self.icono2
        self.btn_imprime_orden.config(image=self.icono2)
        self.btn_imprime_orden.grid(row=1, column=6, padx=4, pady=3, sticky="nsew")
        ToolTip(self.btn_imprime_orden, msg="Imprimir una Orden de trabajo")
        # -------------------------------------------------------

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_grid.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_entrys(self):

        # nombre de cliente
        lbl_nombre_cliente = Label(self.frame_entrys_uno, text="Cliente:")
        lbl_nombre_cliente.grid(row=0, column=0)
        self.entry_nombre_cliente = Entry(self.frame_entrys_uno, textvariable=self.strvar_nombre_cliente, width=70,
                                          justify="left")
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

        # codigo cliente
        self.lbl_codigo_cliente = Label(self.frame_entrys_uno, textvariable=self.strvar_codigo_cliente, width=6,
                                        anchor='e')
        self.lbl_codigo_cliente.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")

        # cliente datos mas
        self.strvar_cli_datosmas.set(value="")
        lbl_cli_datosmas = Label(self.frame_entrys_uno, text="Datos: ")
        lbl_cli_datosmas.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")
        lbl_cli_direccion = Label(self.frame_entrys_uno, textvariable=self.strvar_cli_datosmas)
        lbl_cli_direccion.grid(row=0, column=8, padx=5, pady=2, sticky="nsew")
        lbl_cli_deuda1 = Label(self.frame_entrys_uno, text="Deuda: ")
        lbl_cli_deuda1.grid(row=0, column=9, padx=5, pady=2, sticky="nsew")
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        lbl_cli_deuda2 = Label(self.frame_entrys_uno, textvariable=self.strvar_cli_deuda, fg="red", font=fff)
        lbl_cli_deuda2.grid(row=0, column=10, padx=5, pady=2, sticky="nsew")

        # boton para buscar cliente
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((20, 20), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_entrys_uno, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")

        # reordenamiento de self.frame_entrys_uno
        for widg in self.frame_entrys_uno.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

        self.frame_entrys_uno.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # FRAME ENTRYS DOS -------------------------------------------------

        # Datos de la orden ------------------------------------------------
        self.frame_entrys_dos = LabelFrame(self.master, text="")

        # nro. de orden
        lbl_nro_orden = Label(self.frame_entrys_dos, text="Nº Orden:")
        lbl_nro_orden.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.entry_nro_orden = Entry(self.frame_entrys_dos, textvariable=self.strvar_nro_orden, width=8,
                                     justify="right")
        self.entry_nro_orden.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")
        self.lbl_codigo_cliente.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")

        # Fecha y hora de ingreso
        lbl_fecha_ingreso = Label(self.frame_entrys_dos, text="Fecha y hora de ingreso: ")
        lbl_fecha_ingreso.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
        self.lbl_valor_fecha_ingreso = Label(self.frame_entrys_dos, textvariable=self.strvar_fecha_ingreso, width=20,
                                             justify="right")
        self.lbl_valor_fecha_ingreso.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        # Fecha y hora de egreso
        lbl_fecha_egreso = Label(self.frame_entrys_dos, text="Fecha y hora de egreso: ")
        lbl_fecha_egreso.grid(row=0, column=6, padx=5, pady=2, sticky="nsew")
        self.lbl_valor_fecha_egreso = Label(self.frame_entrys_dos, textvariable=self.strvar_fecha_egreso, width=15,
                                            justify="right")
        self.lbl_valor_fecha_egreso.grid(row=0, column=7, padx=5, pady=2, sticky="nsew")

        # datos del equipo  ---------------------------------------------------------------

        # Defino un combobox con los tipos de equipos que se reciben
        self.lbl_combo_tipos_equipo = Label(self.frame_entrys_dos, text="Grupo de equipo: ")
        self.lbl_combo_tipos_equipo.grid(row=0, column=8, padx=5, pady=2, sticky="nsew")
        # lbl_combo_tipos_equipo.place(x=2, y=55)
        self.grupo_tipo_equipo = ttk.Combobox(self.frame_entrys_dos, textvariable=self.strvar_equ_grupo,
                                              state="readonly", width=14)
        # self.grupo_tipo_equipo['value'] = self.varArtic.combo_input("ma_nombre", "marcas", "ma_nombre")
        self.grupo_tipo_equipo["values"] = ("Notebooks", "PC", "Impresoras", "All in Ones", "Fuentes UPS", "Monitores",
                                            "Varios")
        self.grupo_tipo_equipo.current(0)
        self.grupo_tipo_equipo.grid(row=0, column=9, padx=5, pady=2, sticky="nsew")

        # reordenamiento de self.frame_entrys_dos
        for widg in self.frame_entrys_dos.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")


    def cuadro_entrys_equipo(self):

         # Descripcion de equipo que ingresa
        lbl_equ_ingresa = Label(self.frame_entrys_uno_bis, text="Equipo a Ingresar:")
        lbl_equ_ingresa.grid(row=0, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_equ_ingresa = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equ_ingresa, width=50)
        self.strvar_equ_ingresa.trace("w", lambda *args: self.limitador(self.strvar_equ_ingresa, 60))
        self.entry_equ_ingresa.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")

        # Procesador
        lbl_equipo_procesador = Label(self.frame_entrys_uno_bis, text="Procesador:")
        lbl_equipo_procesador.grid(row=0, column=2, padx=5, pady=2, sticky="nsew")
        self.entry_equipo_procesador = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equipo_procesador,
                                             width=30, justify="left")
        self.entry_equipo_procesador.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")
        self.strvar_equipo_procesador.trace("w", lambda *args: self.limitador(self.strvar_equipo_procesador, 30))

        # Memoria RAM
        lbl_equipo_ram = Label(self.frame_entrys_uno_bis, text="RAM Gb.:")
        lbl_equipo_ram.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
        self.entry_equipo_ram = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equipo_ram, width=50,
                                      justify="left")
        self.entry_equipo_ram.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")
        self.strvar_equipo_ram.trace("w", lambda *args: self.limitador(self.strvar_equipo_ram, 50))

        # Discos
        lbl_equipo_discos = Label(self.frame_entrys_uno_bis, text="Disco/s Gb.:")
        lbl_equipo_discos.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_equipo_discos = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equipo_discos, width=50,
                                         justify="left")
        self.entry_equipo_discos.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")
        self.strvar_equipo_discos.trace("w", lambda *args: self.limitador(self.strvar_equipo_discos, 50))

        # Sistema Operativo
        lbl_equipo_sist_oper = Label(self.frame_entrys_uno_bis, text="S.O.:")
        lbl_equipo_sist_oper.grid(row=1, column=2, padx=5, pady=2, sticky="nsew")
        self.entry_equipo_sist_oper = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equipo_sist_oper,
                                            width=30, justify="left")
        self.entry_equipo_sist_oper.grid(row=1, column=3, padx=5, pady=2, sticky="nsew")
        self.strvar_equipo_sist_oper.trace("w", lambda *args: self.limitador(self.strvar_equipo_sist_oper, 30))

        # Accesorios que acompañan al equipo
        lbl_equ_accesorios = Label(self.frame_entrys_uno_bis, text="Accesorios:")
        lbl_equ_accesorios.grid(row=1, column=4, padx=5, pady=2, sticky="nsew")
        self.entry_equ_accesorios = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equ_accesorios, width=50)
        self.strvar_equ_accesorios.trace("w", lambda *args: self.limitador(self.strvar_equ_accesorios, 50))
        self.entry_equ_accesorios.grid(row=1, column=5, padx=5, pady=2, sticky="nsew")

        # Observaciones
        lbl_equipo_ing_obser = Label(self.frame_entrys_uno_bis, text="Observaciones:")
        lbl_equipo_ing_obser.grid(row=2, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_equipo_ing_obser = Entry(self.frame_entrys_uno_bis, textvariable=self.strvar_equipo_ing_obser,
                                            width=160, justify="left")
        self.entry_equipo_ing_obser.grid(row=2, column=1, columnspan=5, padx=5, pady=2, sticky="nsew")
        self.strvar_equipo_ing_obser.trace("w", lambda *args: self.limitador(self.strvar_equipo_ing_obser, 160))

    def cuadro_entrys_equipo_dos(self):

        # Estado del equipo
        lbl_equ_estado = Label(self.frame_entrys_tres, text="Estado:")
        lbl_equ_estado.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_equ_estado = Entry(self.frame_entrys_tres, textvariable=self.strvar_equ_estado, width=80)
        self.strvar_equ_estado.trace("w", lambda *args: self.limitador(self.strvar_equ_estado, 100))
        self.entry_equ_estado.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")

        # Contraseñas y cuentas
        lbl_equ_cuentas = Label(self.frame_entrys_tres, text="Ctas/Cont.: ")
        lbl_equ_cuentas.grid(row=1, column=2)
        self.entry_cuentas = Entry(self.frame_entrys_tres, textvariable=self.strvar_cuentas, width=70)
        self.strvar_cuentas.trace("w", lambda *args: self.limitador(self.strvar_cuentas, 100))
        self.entry_cuentas.grid(row=1, column=3, padx=5, pady=2, sticky="nsew")

        # Requerimientos
        lbl_equ_requerido = Label(self.frame_entrys_tres, text="Requerido: ")
        lbl_equ_requerido.grid(row=2, column=0, padx=5, pady=2, sticky="nsew")
        self.entry_requerido = Entry(self.frame_entrys_tres, textvariable=self.strvar_requerido, width=166)
        self.strvar_requerido.trace("w", lambda *args: self.limitador(self.strvar_requerido, 170))
        self.entry_requerido.grid(row=2, column=1, columnspan=5, padx=5, pady=2, sticky="nsew")

        # reordenamiento de self.frame_entrys_tres
        for widg in self.frame_entrys_tres.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

    def cuadro_entrys_equipo_tres(self):

        # Diagnostico
        lbl_diagnostico = Label(self.frame_entrys_cuatro, text="Diagnostico:")
        lbl_diagnostico.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")
        self.text_diagnostico = ScrolledText(self.frame_entrys_cuatro)
        self.text_diagnostico.config(width=41, height=6, wrap="word", padx=4, pady=2)
        self.text_diagnostico.grid(row=1, column=0, padx=4, pady=1, sticky="nsew")

        # Trabajo realizado
        lbl_trabajo_realizado = Label(self.frame_entrys_cuatro, text="Trabajo realizado:")
        lbl_trabajo_realizado.grid(row=0, column=1, padx=4, pady=1, sticky="nsew" )
        self.text_trabajo_realizado = ScrolledText(self.frame_entrys_cuatro)
        self.text_trabajo_realizado.config(width=41, height=6, wrap="word", padx=4, pady=2)
        self.text_trabajo_realizado.grid(row=1, column=1, padx=4, pady=1, sticky="nsew")

        # Anotaciones
        lbl_anotaciones = Label(self.frame_entrys_cuatro, text="Notas Internas:")
        lbl_anotaciones.grid(row=0, column=2, padx=4, pady=1, sticky="nsew")
        self.text_anotaciones = ScrolledText(self.frame_entrys_cuatro)
        self.text_anotaciones.config(width=41, height=4, wrap="word", padx=4, pady=2)
        self.text_anotaciones.grid(row=1, column=2, padx=4, pady=1, sticky="nsew")

        # reordenamiento de self.frame_entrys_cuatro
        for widg in self.frame_entrys_cuatro.winfo_children():
            widg.grid_configure(padx=4, pady=3, sticky="nsew")

    def cuadro_entrys_pie(self):

        # Presupuesto
        lbl_presupuesto = Label(self.frame_entrys_cinco, text="Detalle Presupuesto:")
        lbl_presupuesto.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")
        self.entry_presupuesto = Entry(self.frame_entrys_cinco, textvariable=self.strvar_presupuesto, width=157)
        self.strvar_presupuesto.trace("w", lambda *args: self.limitador(self.strvar_presupuesto, 200))
        self.entry_presupuesto.grid(row=0, column=1, padx=4, pady=1, sticky="nsew")

        # Partes reemplazadas
        lbl_partes = Label(self.frame_entrys_cinco, text="Partes reemplazadas:")
        lbl_partes.grid(row=1, column=0, padx=4, pady=1, sticky="nsew")
        self.entry_partes = Entry(self.frame_entrys_cinco, textvariable=self.strvar_partes, width=157)
        self.strvar_partes.trace("w", lambda *args: self.limitador(self.strvar_partes, 200))
        self.entry_partes.grid(row=1, column=1, padx=4, pady=1, sticky="nsew")

        # reordenamiento de self.frame_entrys_cinco
        for widg in self.frame_entrys_cinco.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky="nsew")

    def cuadro_entrys_totales(self):

        # Total pesos partes
        lbl_total_partes = Label(self.frame_entrys_seis, text="Total partes:", justify="left")
        lbl_total_partes.grid(row=0, column=0, padx=5, pady=2, sticky='nsew')
        self.entry_total_partes = Entry(self.frame_entrys_seis, textvariable=self.strvar_total_partes, width=15,
                                        justify="right")
        self.entry_total_partes.grid(row=0, column=1, padx=5, pady=2, sticky="nsew")
        self.entry_total_partes.config(validate="key", validatecommand=self.vcmd)
        self.strvar_total_partes.trace("w", lambda *args: self.limitador(self.strvar_total_partes, 14))
        # mando a la funcion que suma el total final
        self.entry_total_partes.bind('<FocusOut>', lambda e: self.sumar_totalfinal())

        # Total pesos mano de obra
        lbl_total_manodeobra = Label(self.frame_entrys_seis, text="Total Mano de Obra:")
        lbl_total_manodeobra.grid(row=0, column=2, padx=5, pady=1, sticky='nsew')
        self.entry_total_manodeobra = Entry(self.frame_entrys_seis, textvariable=self.strvar_total_manodeobra, width=15,
                                            justify="right")
        self.entry_total_manodeobra.grid(row=0, column=3, padx=5, pady=1, sticky="nsew")
        self.entry_total_manodeobra.config(validate="key", validatecommand=self.vcmd)
        self.strvar_total_manodeobra.trace("w",
                                           lambda *args: self.limitador(self.strvar_total_manodeobra, 14))
        # mando a la funcion que suma el total final
        self.entry_total_manodeobra.bind('<FocusOut>', lambda e: self.sumar_totalfinal())

        # Total global pesos
        lbl_total_global = Label(self.frame_entrys_seis, text="Total a pagar:")
        lbl_total_global.grid(row=0, column=4, padx=4, pady=1, sticky=W)
        self.lbl_importe_global = Label(self.frame_entrys_seis, textvariable=self.strvar_tot_final, width=6, anchor='e')
        self.lbl_importe_global.grid(row=0, column=5, padx=5, pady=1, sticky="nsew")

        # Equipo retirado ???
        lbl_equipo_retirado = Label(self.frame_entrys_seis, text="Retirado? [S/N]:")
        lbl_equipo_retirado.grid(row=0, column=6, padx=4, pady=1, sticky=W)
        self.entry_retirado = Entry(self.frame_entrys_seis, textvariable=self.strvar_retirado, width=2)
        self.strvar_retirado.trace("w", lambda *args: self.limitador(self.strvar_retirado, 1))
        # Esta llamada, convierte la letra que pongo a mayuscula
        self.strvar_retirado.trace_add("write", self.on_write)
        self.entry_retirado.grid(row=0, column=7, padx=5, pady=1, sticky="nsew")

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btn_salir_orden = Button(self.frame_entrys_seis, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                                      bg="yellow", fg="white")
        self.btn_salir_orden.grid(row=0, column=8, padx=10, pady=1, sticky="nsew")

        for widg in self.frame_entrys_seis.winfo_children():
            widg.grid_configure(padx=24, pady=3, sticky="nsew")

    # ----------------------------------------------------------------------------
    # INFORMES -*-
    # ----------------------------------------------------------------------------

    def creopdf(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_orden.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return
        else:
            # Debo traer el registro completo desde la Tabla. Este metodo de abm_ordenrepar, me trase solo el
            # registro requerido con Id que esta en self.clave
            datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)
            # Cargo datos extra del cliente
            datos_cliente = self.varOrdenes.traer_un_cliente(datos_registro_selec[4])
            telef_cliente = datos_cliente[8]+' - '+datos_cliente[9]

        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """

        # ----------------------------------------------------------------------------------
        # CONFIGURACION
        # esto siempre debe estar
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 5)
        # salto de hoja automatico
        pdf.set_auto_page_break(auto=True, margin=20)
        # -----------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------
        # ENCABEZADO

        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
        self.pdf_numero_orden = str(datos_registro_selec[1])
        self.pdf_codigo_cliente = str(datos_registro_selec[4])
        self.pdf_nombre_cliente = datos_registro_selec[5]
        self.pdf_datos_encabezado_orden = (self.pdf_numero_orden+' - '+self.pdf_nombre_cliente+
                                           ' - ('+self.pdf_codigo_cliente+') - Telefono '+str(telef_cliente))
        # Imprimo el encabezado de pagina con el numero de orden
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0, h=5, txt='Fecha/Hora: ' + feac + ' - Orden Nº ' + self.pdf_datos_encabezado_orden, border=1,
                 align='C', fill=0, ln=1)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # DEFINO VARIABLES

        self.pdf_desc = str(datos_registro_selec[6])
        self.pdf_grupo = str(datos_registro_selec[7])
        self.pdf_acces = datos_registro_selec[13]
        self.pdf_estado = datos_registro_selec[14]
        self.pdf_cuenta = datos_registro_selec[15]
        self.pdf_requerido = datos_registro_selec[16]
        self.pdf_diagnostico = datos_registro_selec[17]
        self.pdf_presupuesto = datos_registro_selec[18]
        self.pdf_realizado = datos_registro_selec[19]
        self.pdf_partes = datos_registro_selec[20]
        self.pdf_anotaciones = datos_registro_selec[21]
        self.pdf_totmanobra = str(datos_registro_selec[22])
        self.pdf_totpartes = str(datos_registro_selec[23])
        self.totalpagar = str(datos_registro_selec[22]+datos_registro_selec[23])
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # TITULOS Y NOTAS - LINEAS DE IMPRESION YA ARMADAS

        cuerpo_1 = 'Equipo: '+self.pdf_desc+' - '+self.pdf_grupo
        cuerpo_2 = 'Accesorios: '+self.pdf_acces
        cuerpo_12 = 'Estado del equipo: '+self.pdf_estado
        cuerpo_3 = 'Cuentas y contraseñas: '+self.pdf_cuenta
        cuerpo_4 = 'Requerimiento: '+self.pdf_requerido
        cuerpo_5 = 'Diagnostico: '+self.pdf_diagnostico
        cuerpo_6 = 'Presupuesto: '+self.pdf_presupuesto
        cuerpo_7 = 'Trabajo realizado: '+self.pdf_realizado
        cuerpo_8 = 'Trabajo partes reemplazadas: '+self.pdf_partes
        cuerpo_9 = 'Trabajo anotaciones: '+self.pdf_anotaciones
        cuerpo_10 = 'Total partes $ : '+self.pdf_totpartes+\
                    ' - Total Mano de Obra $: '+self.pdf_totmanobra+' - Total a pagar $: '+self.totalpagar
        cuerpo_11 = ('NOTA: Pasado 90 dias de recibir su equipo, la casa no se responsabiliza por el estado '
                     'ni el reintegro del mismo')
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # TALON DEL CLIENTE

        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_1, border=1, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_2, border=1, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_12, border=1, align='L', fill=0)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_4, border=1, align='L', fill=0)
        # espacios
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)
        pdf.multi_cell(w=0, h=5, txt=cuerpo_11, align='L', fill=0)

        # Espaciado entre cuerpos
        pdf.cell(w=0, h=10, txt='', align='L', fill=0, ln=1)
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # TALON INTERNO

        # Encabezado
        pdf.set_font('Arial', '', 10)
        pdf.set_line_width(0.4)
        pdf.cell(w=0, h=5, txt='Fecha/Hora: ' + feac + '  - Orden Nº ' + self.pdf_datos_encabezado_orden, border=1,
                 align='C', fill=0, ln=1)
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.set_line_width(0.2)
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # CUERPO SEGUNDO TALON

        # EQUIPO
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Equipo: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_desc, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # ACCESORIOS Y ESTADO DEL EQUIPO
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Accesorios y Estado del equipo: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_acces+'  -  '+self.pdf_estado, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # CUENTAS Y CONTRASEÑAS
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Cuentas y contraseñas: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_cuenta, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # REQUERIMIENTO
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Requerimiento: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_requerido, align='L', border=1, fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # DIAGNOSTICO
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Diagnostico: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_diagnostico, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # PRESUPUESTO
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Presupuesto: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_presupuesto, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # TRABAJO REALIZADO
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Trabajo realizado: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_realizado, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # PARTES REEMPLAZADAS
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Partes reemplazadas: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=self.pdf_partes, border=1, align='L', fill=0)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # pdf.set_font('Courier', 'B', 10)
        # pdf.cell(w=0, h=5, txt='* Anotaciones: ', align='L', fill=0, ln=1)
        # pdf.set_font('Arial', '', 11)
        # pdf.multi_cell(w=0, h=5, txt=self.pdf_anotaciones, align='L', fill=0)
        # pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # CONTROLES INTERNOS
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='Bateria-Teclado-Camara-Sonido-Mic-Wifi-Lectora-Msconfig-Drivers-Fecha/Hora-Temperatura',
                 align='L', fill=0, ln=1)
        pdf.cell(w=0, h=4, txt='Disco-Antivirus-Actualizaciones-Navegadores-Crack-Restauracion-Ccleaner-Office',
                 align='L', fill=0, ln=1)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # TOTALES
        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=4, txt='* Totales: ', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=4, txt=cuerpo_10, border=1, align='L', fill=0)
        #pdf.line(10, 210, 190, 210)
        pdf.cell(w=0, h=3, txt='', align='L', fill=0, ln=1)

        # Espaciado entre cuerpos ------------------------------------
        pdf.cell(w=0, h=15, txt='', align='L', fill=0, ln=1)

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='Retirada................................ ', align='R', fill=0, ln=1)
        # --------------------------------------------------------------------------------

        """ para crear una linea recta
        #pdf.rect(x=50, y=80, w=70, h=95)
        #pdf.line(20, 150, 190, 180)
        # para crear una linea de puntos
        #pdf.dashed_line(15, 78, 80, 90, dash_length=5, space_length=6)
        # para crear un elipse
        #pdf.ellipse(x=10, y=15, w=50, h=80, style='')
        # insertar imagenes y texto
        #pdf.text(x=60, y=50, txt='Hola muchachos')
        #pd.image('impresora.png', x=10, y=10, w=30, h=30) #, link=url) """
        # ----------------------------------------------------------------------------

        # -----------------------------------------------------------------------------
        """ Para insertar lineas de escritura una debajo de otra
        por ejemplo :
        linea 1
        linea 2
        linea 3
        for i in range(1, 41):
            pdf.cell(0, 10, f'Esta es la linea {i} :D', ln=True)  """
        # -------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # margenes izq derecha arriba y abajo
        """ Margen antes de terminar la hoja o sea en tre la ultima linea de la hoja y el fin de la hoja
        pdf.set_auto_page_break(auto=True, margin=15) """
        # -------------------------------------------------------------------------------------

        """ # # para listar una base de datos forma simple basica
        # # lista_de_datos = retorno de la base de datos

        # # al ultimo le ponemos w=0 y abarca todo el resto del renglon hasta el final
        # pdf.cell(w=30, h=8, txt='Codigo', border=1, align='C', fill=0)
        # pdf.cell(w=25, h=8, txt='Rubro', border=1, align='C', fill=0)
        # pdf.cell(w=20, h=8, txt='Marca', border=1, align='C', fill=0)
        # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)

        # pdf.set_font('Arial', '', 5)
        # # retorno una lista con los registros
        # datos = self.varOrdenes.consultar_orden("")
        # for row in datos:
        #     pdf.cell(w=30, h=5, txt=row[1], border=1, align='C', fill=0)
        #     pdf.cell(w=25, h=5, txt=row[2], border=1, align='C', fill=0)
        #     pdf.cell(w=20, h=5, txt=row[3], border=1, align='C', fill=0)
        #     mostrar = row[4]
        #     cadena = (mostrar[:100])
        #     pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0) """

        pdf.output('hoja.pdf')

        # # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    def fInfTecnico(self):

        # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
        self.selected = self.grid_orden.focus()
        # Asi obtengo la clave en la tabla (campo Id) que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_orden.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return
        else:
            # Debo traer el registro completo desde la Tabla. Este metodo de abm_ordenrepar, me trase solo el
            # registro requerido con Id que esta en self.clave
            datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)
            # Cargo datos extra del cliente
            datos_cliente = self.varOrdenes.traer_un_cliente(datos_registro_selec[4])
            telef_cliente = datos_cliente[8]+' - '+datos_cliente[9]

        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """

        # -----------------------------------------------------------------------------------
        # CONFIGURACION INFORME
        # esto siempre debe estar
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 5)
        # salto de hoja automatico
        pdf.set_auto_page_break(auto=True, margin=20)
        # -----------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------
        # ARMADO DE ENCABEZADO

        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
        self.pdf_numero_orden = str(datos_registro_selec[1])
        self.pdf_codigo_cliente = str(datos_registro_selec[4])
        self.pdf_nombre_cliente = datos_registro_selec[5]
        self.pdf_datos_encabezado_orden = (self.pdf_numero_orden)
        # -----------------------------------------------------------------------------------

        # # Imprimo el encabezado de pagina con el numero de orden
        # pdf.set_font('Arial', '', 10)
        # pdf.cell(w=0, h=5, txt='Fecha/Hora: ' + feac + ' - Orden Nº ' + self.pdf_datos_encabezado_orden, border=1,
        #          align='C', fill=0, ln=1)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # PREPARACION DATOS DEL INFORME

        self.pdf_desc = str(datos_registro_selec[6])        # descripcion libre equipo que ingresa (PC-Impresora....)
        self.pdf_grupo = str(datos_registro_selec[7])       # equipo grupo combo (Notebook - PC -Impresora

        # datos componentes del equipo
        self.pdf_procesador = datos_registro_selec[8]
        self.pdf_ram = datos_registro_selec[9]
        self.pdf_discos = datos_registro_selec[10]
        self.pdf_sist_oper = datos_registro_selec[11]
        self.pdf_observaciones = datos_registro_selec[12]

        # otros datos de ingreso del equipo
        self.pdf_acces = datos_registro_selec[13]
        self.pdf_estado = datos_registro_selec[14]

        # otros datos necesarios
        self.pdf_cuenta = datos_registro_selec[15]
        self.pdf_requerido = datos_registro_selec[16]

        # datos dentro revision
        self.pdf_diagnostico = datos_registro_selec[17]
        self.pdf_presupuesto = datos_registro_selec[18]
        self.pdf_realizado = datos_registro_selec[19]
        self.pdf_partes = datos_registro_selec[20]
        self.pdf_anotaciones = datos_registro_selec[21]
        # -----------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------
        # ARMADO CUERPOS DE IMPRESION

        # datos totales honorarios y partes
        self.pdf_totmanobra = str(datos_registro_selec[22])
        self.pdf_totpartes = str(datos_registro_selec[23])
        self.totalpagar = str(datos_registro_selec[22]+datos_registro_selec[23])

        cuerpo_1 = 'Equipo: '+self.pdf_grupo+' - '+self.pdf_desc
        cuerpo_2 = ('Procesador: '+self.pdf_procesador+' - Memoria RAM: ' + self.pdf_ram+' - Discos: ' +
                    self.pdf_discos+' - Sistema Operativo: ' + self.pdf_sist_oper +
                    ' - Observaciones: '+self.pdf_observaciones)
        cuerpo_3 = 'Requerimiento: '+self.pdf_requerido
        cuerpo_4 = 'Diagnostico: '+self.pdf_diagnostico
        cuerpo_5 = 'Trabajo realizado: '+self.pdf_realizado
        cuerpo_6 = 'Anotaciones: '+self.pdf_anotaciones
        cuerpo_7 = 'Partes reemplazadas: '+self.pdf_partes
        cuerpo_8 = 'Presupuesto: '+self.pdf_presupuesto
        cuerpo_10 = 'Total partes $ : '+self.pdf_totpartes+\
                    ' - Total Mano de Obra $: '+self.pdf_totmanobra+' - Total a pagar $: '+self.totalpagar
        # -----------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------
        # IMPRESION

        # Encabezado
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(w=0, h=5, txt='Informe Tecnico: ', border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos
        pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)

        # Datos del cliente
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='Sr./a: ' + self. pdf_nombre_cliente + ' - Orden Nº ' +
                                     self.pdf_datos_encabezado_orden + ' - Fecha/Hora Ingreso: '
                                     + feac , border=1, align='C', fill=0)

        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Datos cliente
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_1, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Datos equipo
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_2, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Requerido
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_3, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Diagnostico
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_4, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Trabajo realizado
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_5, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # # Anotaciones
        # pdf.set_font('Arial', '', 10)
        # pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_6, border=1, align='L', fill=0)
        # pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Partes reemplazadas
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_7, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Presupuesto
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_8, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)

        # Total pesos
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(w=0, h=5, txt='- ' + cuerpo_10, border=1, align='L', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=2)

        # with open("inf_tecnico.txt", "r", encoding="utf-8") as f:
        #     for linea in f:
        #         pdf.multi_cell(0, 7, linea)

        pdf.set_font('Arial', '', 9)

        # Impresion de inf_tecnico.txt
        with open("C:\Proyectos_Python\ABM_Clientes\inf_tecnico.txt", "r", encoding="latin-1") as f:
            for linea in f:
                pdf.multi_cell(0, 3, linea)

        pdf.output('hoja.pdf')

        # # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)



#         # -------------------------------------------------------------
#
#         self.pantalla_estad = Toplevel()
#         self.pantalla_estad.geometry('1120x480+400+500')
#         self.pantalla_estad.transient(master=self.master)
#         self.pantalla_estad.config(bg='light green', padx=5, pady=5)
#         self.pantalla_estad.resizable(False, False)
#         self.pantalla_estad.title("Orden numero")
#
#
#         self.juan = LabelFrame(self.pantalla_estad)
#
#         # text = tk.Text(self.juan, width=60, height=15)
#         # text.pack(padx=10, pady=10)
#
#         datos = self.varOrdenes.consultar_ordenes(self.filtro_activo)
#
#         for row in datos:
#
#             # -------------------------------------------------------------
#             self.text_diagnostic = ScrolledText(self.juan)
#             #self.text_diagnostic = tk.Text(self.juan, width=100, height=15)
#             self.text_diagnostic.config(width=100, height=6, wrap="word", padx=4, pady=2)
#             self.text_diagnostic.grid(row=0, column=0, padx=4, pady=1, sticky="nsew")
#             self.text_diagnostic.insert(END, datos[17])
#             # -----------------------------------------------------------------
#
#             break
#
#
# #        print(self.text_diagnostic.get(1.0, 'end-1c'),)
#
#         # if len(self.grid_orden.get_children()) > 0:
#         #     self.grid_orden.selection_set(self.grid_orden.get_children()[0])
#         #
#         # for widg in self.pantalla_estad.winfo_children():
#         #     widg.grid_configure(padx=5, pady=3, sticky='nsew')
#
#         self.juan.pack(side="top", fill="both", expand=0, padx=3, pady=2)
#         self.pantalla_estad.grab_set()
#         self.pantalla_estad.focus_set()
#
#         mainloop()


