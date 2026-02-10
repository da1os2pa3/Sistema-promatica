
from funciones import *
from funcion_new import *
from ctacte_ABM import *
#----------------------------------------------
import os
from PDF_clase import *
from datetime import date, datetime, timedelta
from PIL import Image, ImageTk
#-----------------------------------------------
import tkinter as tk
from tkinter import ttk

#from tkinter import *
#from tkinter import ttk
#import tkinter as tk

import tkinter.font as tkFont
from tkinter import messagebox

class CuentaCorriente(Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ------------------------------------------------------------------------------
        # Instanciaciones
        # Creo una instancia de clientesABM y de funcion_new
        self.varCtacte = datosCtacte(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ----------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        # master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 450
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")
        # ------------------------------------------------------------------------------

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_ctacte.identify_row(0)
        # self.grid_ctacte.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_ctacte.focus(item)

        # self.habilitar_text("disabled")
        # self.habilitar_Btn_Final("disabled")
        # self.habilitar_Btn_busquedas("disabled")
        # #self.habilitar_Selec_cliente("disabled")
        # self.habilitar_Btn_Oper("disabled")
        # self.entry_nombre_cliente.focus()

        """ 
        La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. 
        """

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")

        # ------------------------------------------------------------------
        # TITULOS
        # ------------------------------------------------------------------

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('ctacte.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ctacte = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_ctacte = Label(self.frame_titulo_top, image=self.png_ctacte, bg="red", relief="ridge", bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Cuentas Corrientes",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ctacte.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # STRINGVARS
        # ------------------------------------------------------------------
        self.strvar_nombre_cliente = tk.StringVar(value="")
        self.strvar_codigo_cliente = tk.StringVar(value="0")
        self.strvar_fecha_movim = tk.StringVar(value="")
        self.strvar_detalle_movim = tk.StringVar(value="")
        self.strvar_saldo_cliente = tk.StringVar(value="0.00")
        self.strvar_debito_movim = tk.StringVar(value="0.00")
        self.strvar_credito_movim = tk.StringVar(value="0.00")
        self.strvar_clavemov = tk.StringVar(value="0")

        # ------------------------------------------------------------------------------
        # VARIABLES GENERALES
        # ------------------------------------------------------------------
        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.strvar_fecha_movim = tk.StringVar(value=una_fecha)
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------
        # GRID - TREVIEEW
        # ------------------------------------------------------------------
        self.frame_tvw_ctacte=LabelFrame(self.master, text="Cuentas Corrientes: ", foreground="#CF09BD")
        self.cuadro_grid_ctacte()
        self.frame_tvw_ctacte.pack(side="top", fill="both", padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS
        # ------------------------------------------------------------------
        self.frame_primero=LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys()
        self.frame_primero.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------
        # ENTRYS MOVIMIENTOS
        self.frame_tercero=LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys_movimientos()
        self.frame_tercero.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # BOTONES TREEVIEW
        # ------------------------------------------------------------------
        self.frame_cuarto=LabelFrame(self.master, text="", foreground="red")
        self.cuadro_botonestv()
        self.frame_cuarto.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # GRID
    # ------------------------------------------------------------------

    def limpiar_Grid(self):

        for item in self.grid_ctacte.get_children():
            self.grid_ctacte.delete(item)

    def llena_grilla(self, ult_tabla_id):

        if len(self.filtro_activo) > 0:
            datos = self.varCtacte.consultar_ctacte(self.filtro_activo)
        else:
            datos = self.varCtacte.consultar_ctacte("ctacte ORDER BY cc_fecha ASC")

        self.suma_debitos = 0
        self.suma_creditos = 0
        self.suma_saldos = 0

        for row in datos:

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'), "hora_no")

            self.suma_saldos += row[3] - row[4]
            self.grid_ctacte.insert("", "end", text=row[0], values=(forma_normal, row[2], row[3], row[4],
                                                                  self.suma_saldos, row[7]))
            self.suma_debitos += row[3]
            self.suma_creditos += row[4]

        self.strvar_saldo_cliente.set(value=str((self.suma_debitos-self.suma_creditos)))

        if len(self.grid_ctacte.get_children()) > 0:
            self.grid_ctacte.selection_set(self.grid_ctacte.get_children()[0])

        # ----------------------------------------------------------------------------------
        # Procedimiento para acomodar los punteros en caso de altas, modif. ....)

        """ ult_tabla_id = Trae el Id de la tabla (21, 60, 61, ..) correspondiente identificando al registro 
        en el cual yo quiero que se ponga el puntero del GRID.
        Traera blanco ('') si la funcion llena_grilla es llamada desde cualquier lugar que no 
        necesite acomodar puntero en un item en particular (caso altas, modificaciones ...)."""

        if ult_tabla_id:
            """ regis = Guardo todos los Id del Grid (I001, IB003, ...)"""
            regis = self.grid_ctacte.get_children()
            rg = ""

            for rg in regis:

                """ buscado = guardo el 'text' correspondiente al Id del grid que esta en regis y muevo toda 
                la linea de datos del treeview a la variable buscado), o sea, para el Id I0001 paso el Id de la 
                tabla 57... y asi ira cambiando para cada rg
                text = te da el valor de la primera columna del grid, que es donde veo el Id del registro 
                asignado en la tabla"""

                buscado = self.grid_ctacte.item(rg)['text']
                if int(buscado) == int(ult_tabla_id):
                    """ Si coinciden los Id quiere decir que encontre al registro que estoy buscando por Id de tabla."""
                    break

            """ Ahora ejecuto este procedimiento que se encarga de poner el puntero en el registro que acabamos 
                de encontrar correspondiente al Id de tabla asignado en el parametro de la funcion llena_grilla. 
            "rg" = es el Text o Index del registro en el Treeview I001, IB002.... y ahi posiciono el foco 
                con las siguientes instrucciones. """

            self.grid_ctacte.selection_set(rg)
            # Para que no me diga que no hay nada seleccionado
            self.grid_ctacte.focus(rg)
            # para que la linea seleccionada no me quede fuera del area visible del treeview
            self.grid_ctacte.yview(self.grid_ctacte.index(rg))
        else:
            # caso de que el parametro ult_tabla_id sea " " muevo el puntero al final del GRID
            self.mover_puntero_topend("END")

    def estado_inicial(self):

        self.filtro_activo = "ctacte WHERE cc_codcli = 0 ORDER BY cc_fecha ASC"
        self.var_Id = -1
        self.alta_modif = 0

        self.habilitar_text("disabled")
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_Btn_Oper("disabled")
        self.entry_nombre_cliente.focus()

    def limpiar_text(self):

        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.strvar_fecha_movim.set(value=una_fecha)
        self.entry_detalle_movim.delete(0, END)
        self.strvar_debito_movim.set(value="0.00")
        self.strvar_credito_movim.set(value="0.00")

    def habilitar_text(self, estado):

        self.entry_fecha_movim.configure(state=estado)
        self.entry_detalle_movim.configure(state=estado)
        self.entry_debito_movim.configure(state=estado)
        self.entry_credito_movim.configure(state=estado)

    def habilitar_Btn_Oper(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)
        self.btn_compactar.configure(state=estado)

    def habilitar_Btn_Final(self, estado):

        self.btn_guardaritem.configure(state=estado)

    def habilitar_Btn_busquedas(self, estado):

        #self.btn_compactar.configure(state=estado)
        self.btn_imprime.configure(state=estado)

    def reset_stringvars(self):

        self.strvar_nombre_cliente.set(value="")
        self.strvar_codigo_cliente.set(value="0")
        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.strvar_fecha_movim.set(value=una_fecha)
        self.strvar_detalle_movim.set(value="")
        self.strvar_saldo_cliente.set(value="0.00")
        self.strvar_debito_movim.set(value="0.00")
        self.strvar_credito_movim.set(value="0.00")

    def reset_campos(self):

        self.strvar_detalle_movim.set(value="")
        self.strvar_debito_movim.set(value="0.00")
        self.strvar_credito_movim.set(value="0.00")

    def fReset_selcli(self):

        self.entry_nombre_cliente.configure(state="normal")
        self.btn_bus_cli.configure(state="normal")
        self.strvar_nombre_cliente.set(value="")
        self.strvar_codigo_cliente.set(value="0")
        self.limpiar_text()
        self.habilitar_text("disabled")

        self.habilitar_Btn_Oper("disabled")
        self.habilitar_Btn_Final("disabled")
        self.limpiar_Grid()
        self.strvar_saldo_cliente.set(value="0")

        self.entry_nombre_cliente.focus()

    def fCancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelacion?", parent=self)
        if r == messagebox.YES:
            self.entry_nombre_cliente.configure(state="normal")
            self.btn_bus_cli.configure(state="normal")
            self.strvar_nombre_cliente.set(value="")
            self.strvar_codigo_cliente.set(value="0")
            self.limpiar_text()
            self.habilitar_text("disabled")

            self.habilitar_Btn_Oper("disabled")
            self.habilitar_Btn_Final("disabled")
            self.limpiar_Grid()
            self.strvar_saldo_cliente.set(value="0")

            self.entry_nombre_cliente.focus()

    # -------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------

    def fNuevo(self):

        # VALIDACIONES

        if self.strvar_nombre_cliente.get() == "" or self.strvar_codigo_cliente.get() == "0":
            messagebox.showwarning("Error", " Debe existir un cliente asignado", parent=self)
            self.entry_nombre_cliente.focus()
            return

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.habilitar_Btn_busquedas("disabled")
        self.habilitar_Btn_Oper("disabled")
        self.habilitar_Btn_Final("normal")
        self.entry_fecha_movim.focus()

    def fEditar(self):

        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_ctacte.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_ctacte.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2
        self.var_Id = self.clave  # puede traer -1 , en ese caso seria un alta

        self.habilitar_text('normal')

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_ctacte.item(self.selected, 'values')

        # Al modificar tambien debo convertir la fecha SQL a string dd/mm/yyyy para visualizarla
        #una_fecha = datetime.strptime(valores[0], '%Y-%m-%d')
        self.strvar_fecha_movim.set(value=valores[0])
        self.strvar_detalle_movim.set(value=valores[1])
        self.strvar_debito_movim.set(value=valores[2])
        self.strvar_credito_movim.set(value=valores[3])

        self.habilitar_text("normal")
        self.habilitar_Btn_Oper("disabled")
        self.habilitar_Btn_Final("normal")
        self.entry_nombre_cliente.focus()

    def fBorrar(self):

        # guardo item seleccionado en el grid
        self.selected = self.grid_ctacte.focus()
        self.selected_ant = self.grid_ctacte.prev(self.selected)
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        self.clave_ant = self.grid_ctacte.item(self.selected_ant, 'text')

        # guardo la clae de movimiento anterior si la hay
        self.clavemov_ant = 0

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        valores = self.grid_ctacte.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)

        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        # Elimino de tabla planicaja
        self.varCtacte.eliminar_item_ctacte(self.clave)

        messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)

        self.limpiar_Grid()
        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # Validaciones

        # FECHA
        if self.strvar_fecha_movim.get() == "":
            messagebox.showerror("Error", "Fecha en blanco", parent=self)
            self.entry_fecha_movim.focus()
            return
        # DETALLE
        if self.strvar_detalle_movim.get() == "":
            messagebox.showerror("Error", "Agregue un detalle", parent=self)
            self.entry_detalle_movim.focus()
            return
        # CAMPOS DE IMPORTE
        if self.strvar_debito_movim.get() == "0.00" and self.strvar_credito_movim.get() == "0.00":
            messagebox.showerror("Error", "No i mgreso importes", parent=self)
            self.entry_debito_movim.focus()
            return

        aaa = 0
        if aaa == 0:
        # #try:

            # guardo el Id del Treeview en selected para ubicacion del foco a posteriori
            self.selected = self.grid_ctacte.focus()
            # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
            self.clave = self.grid_ctacte.item(self.selected, 'text')

            #self.nuevo_itempla = ""

            if self.alta_modif == 1:

                #self.nuevo_itempla = str(self.strvar_detalle_movim.get())

                # debe ser cero si es un alta de nuevo movimiento
                self.strvar_clavemov.set(value="0")

                fecha_aux = datetime.strptime(self.strvar_fecha_movim.get(), '%d/%m/%Y')
                self.varCtacte.insertar_ctacte(fecha_aux, self.strvar_detalle_movim.get(),
                                self.strvar_debito_movim.get(), self.strvar_credito_movim.get(),
                                self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                self.strvar_clavemov.get())

                messagebox.showinfo("Correcto", "Item ingresado correctamente", parent=self)

            else:

                self.strvar_clavemov.set(value="0")

                self.varCtacte.modificar_ctacte(self.var_Id, self.strvar_fecha_movim.get(),
                            self.strvar_detalle_movim.get(), self.strvar_debito_movim.get(),
                            self.strvar_credito_movim.get(), self.strvar_codigo_cliente.get(),
                            self.strvar_nombre_cliente.get(), self.strvar_clavemov.get())

                self.var_Id == -1

                messagebox.showinfo("Modificacion", "La modificacion fue exitosa", parent=self)

            # cierre de las novedades y reseteando pantalla para nuevo movimiento - actualizando grilla
            self.limpiar_Grid()
            self.reset_campos()

            # Deshabilitar variables a estado cero
            self.habilitar_text("disabled")
            # rehabilitar botones correspondientes
            self.habilitar_Btn_Oper("normal")
            self.habilitar_Btn_Final("disabled")

            if self.alta_modif == 1:
                ultimo_tabla_id = self.varCtacte.traer_ultimo(0)
                self.llena_grilla(ultimo_tabla_id)
            elif self.alta_modif == 2:
                self.llena_grilla(self.clave)

            self.btn_nuevoitem.focus()

        # #except:

        #     messagebox.showerror("Error", "Revise Fechas", parent=self)
        #     self.entry_fecha_planilla.focus()
        #     return

    def DobleClickGrid(self, event):
        self.fEditar()

    def fSalir(self):
        self.master.destroy()

    # -------------------------------------------------------
    # PUNTERO
    # -------------------------------------------------------

    def fToparch(self):
        self.mover_puntero_topend("TOP")

    def fFinarch(self):
        self.mover_puntero_topend('END')

    def mover_puntero_topend(self, param_topend):

        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview (I001, I002.....
            regis = self.grid_ctacte.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_ctacte.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_ctacte.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_ctacte.yview(self.grid_ctacte.index(self.grid_ctacte.get_children()[0]))

        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview (I001, I002, ..........
            regis = self.grid_ctacte.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            # barro hasta el ultimo
            for rg in regis:
                continue
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_ctacte.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_ctacte.focus(rg)
            # lleva el foco al final del treeview
            self.grid_ctacte.yview(self.grid_ctacte.index(self.grid_ctacte.get_children()[-1]))

    # -------------------------------------------------------
    # BUSQUEDAS
    # -------------------------------------------------------

    def fBuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.strvar_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.strvar_buscostring.get()

        self.filtro_anterior = self.filtro_activo

        self.filtro_activo = ("ctacte WHERE cc_codcli = '" + self.strvar_codigo_cliente.get() +
                              "' AND INSTR(cc_detalle, '" + se_busca + "') > 0")

        self.varCtacte.buscar_entabla(self.filtro_activo)
        self.limpiar_Grid()
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_ctacte.selection()
        self.grid_ctacte.focus(item)

#        self.puntabla("", "S")

    def fShowall(self):

        self.selected = self.grid_ctacte.focus()
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        self.filtro_activo = "ctacte WHERE cc_codcli = '" + self.strvar_codigo_cliente.get() + "' ORDER BY cc_fecha ASC"
        self.limpiar_Grid()
        self.llena_grilla("self.clave")

    def fBuscli(self):

        """
        Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en que
        campos debe hacerse
        """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.strvar_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ 
        Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden 
        de como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido arriba (que_busco)
        """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                                                        "Orden: Alfabetico cliente", "N")

        """ 
        Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes
        """

        for item in valores_new:
            self.strvar_nombre_cliente.set(value=item[15])
            self.strvar_codigo_cliente.set(value=item[1])

        self.habilitar_Btn_busquedas("normal")
        self.habilitar_Btn_Oper("normal")

        # si el codigo de cliente no es cero, filtro la tabla por el cliente seleccionado
        if int(self.strvar_codigo_cliente.get()) != 0:

            # filtrar la cuenta corriente para este cliente
            self.filtro_activo = "ctacte WHERE cc_codcli = '" + self.strvar_codigo_cliente.get() +" ' ORDER BY cc_fecha"

            self.limpiar_Grid()
            self.llena_grilla("")

            # inhabilito edicion de nombre de cliente para que no pueda cambiarlo
            self.entry_nombre_cliente.configure(state="disabled")
            self.btn_bus_cli.configure(state="disabled")

    # -------------------------------------------------------
    # VALIDACIONES
    # -------------------------------------------------------

    def formato_fecha_compactar(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        # FUNCION VALIDA FECCHAS en modulo funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_tope_compactar.get())

        una_fecha = date.today()

        if retorno_VerFal == "":
            # Retorno con error
            self.strvar_fecha_tope_compactar.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.entry_fecha_compactar.focus_set()
            return "error"
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.entry_fecha_compactar.focus()
            return "bien"
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_tope_compactar.set(value=una_fecha.strftime('%d/%m/%Y'))
            self.entry_fecha_compactar.focus()
            return "error"
        elif retorno_VerFal == "BLANCO":
            return "bien"
        else:
            self.strvar_fecha_tope_compactar.set(retorno_VerFal)
            return "bien"

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
            le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fecha_movim.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fecha_movim.get())

        if retorno_VerFal == "":
            self.strvar_fecha_movim.set(value=estado_antes)
            self.entry_fecha_movim.focus()
            return ("error")
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.filtro_activo = ("planicaja WHERE CAST(pl_fecha AS date) = CAST('" + self.strvar_fecha_movim.get()
                                  + "' AS date)")
            self.limpiar_Grid()
            self.llena_grilla()
            self.entry_fecha_movim.focus()
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fecha_movim.set(value=estado_antes)
            self.entry_fecha_movim.focus()
            return ("error")
        elif retorno_VerFal == "BLANCO":
            return ("error")
        else:
            self.strvar_fecha_movim.set(value=retorno_VerFal)

        return ("bien")

    def limitador(self, entry_text, caract):

        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def calcular(self):

        try:
            # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
            if not control_forma(list(self.strvar_debito_movim.get())):
                self.strvar_debito_movim.set(value="0")
                self.entry_debito_movim.focus()
                return
            if not control_forma(list(self.strvar_credito_movim.get())):
                self.strvar_credito_movim.set(value="0")
                self.entry_credito_movim.focus()
                return

            # Control de valor en blanco o solo un . o -
            if (self.strvar_debito_movim.get() == "" or self.strvar_debito_movim.get() == "." or
                    self.strvar_debito_movim.get() == "-"):
                self.strvar_debito_movim.set(value="0")
            if (self.strvar_credito_movim.get() == "" or self.strvar_credito_movim.get() == "." or
                    self.strvar_credito_movim.get() == "-"):
                self.strvar_credito_movim.set(value="0")

            # control de valor en cero o si tiene mas de dos decimales lo trunco a dos
            if float(self.strvar_debito_movim.get()) == 0:
                self.strvar_debito_movim.set(value="0")
            else:
                self.strvar_debito_movim.set(value=str(round(float(self.strvar_debito_movim.get()), 2)))

            if float(self.strvar_credito_movim.get()) == 0:
                self.strvar_credito_movim.set(value="0")
            else:
                self.strvar_credito_movim.set(value=str(round(float(self.strvar_credito_movim.get()), 2)))
        except:
            messagebox.showerror("Error", "Revise entradas numericas", parent=self)
            self.entry_total_partes.focus()
            return

    def cuadro_entrys(self):

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = Label(self.frame_primero, text="Cliente: ", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_nombre_cliente = Entry(self.frame_primero, textvariable=self.strvar_nombre_cliente, width=48)
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.lbl_texto_codigo_cliente = Label(self.frame_primero, textvariable=self.strvar_codigo_cliente, width=10 )
        self.lbl_texto_codigo_cliente.grid(row=0, column=2, padx=5, pady=2, sticky=W)

        # BOTON BUSCAR CLIENTE EN LISTBOX
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = Button(self.frame_primero, text="", image=self.photo_bus_cli, command=self.fBuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=3, padx=5)

        # BOTON RESET BUSQUEDA DE CLIENTE - HABILLITO ENTRY DEL NOMBRE
        self.photo_reset_cli = Image.open('reset.png')
        self.photo_reset_cli = self.photo_reset_cli.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_reset_cli = ImageTk.PhotoImage(self.photo_reset_cli)
        self.btn_reset_cli = Button(self.frame_primero, text="", image=self.photo_reset_cli, command=self.fReset_selcli,
                                    bg="grey", fg="white")
        self.btn_reset_cli.grid(row=0, column=4, padx=5)

        # Saldo del cliente
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_saldo_cliente = Label(self.frame_primero, text="Saldo: ", font=fff, justify="left")
        self.lbl_saldo_cliente.grid(row=0, column=5, padx=5, pady=2, sticky=W)
        self.lbl_importe_saldo_cliente = Label(self.frame_primero, textvariable=self.strvar_saldo_cliente, width=20,
                                               font=fff, justify="left")
        self.lbl_importe_saldo_cliente.grid(row=0, column=6, padx=5, pady=2, sticky=W)

        # Boton para compactar
        self.btn_compactar = Button(self.frame_primero, text="Compactar", command=self.fCompactar, width=15,
                                    bg="medium purple", fg="white")
        self.btn_compactar.grid(row=0, column=7, padx=4, pady=2)

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = Button(self.frame_primero, image=self.photo_imp, pady=3, command=self.fImprime, border=3)
        self.btn_imprime.grid(row=0, column=8, padx=4, pady=2)
        #self.btnPlaniCaja.place(x=555, y=10, width=100, height=100)

        # botones fin y principio archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_primero, text="", image=self.photo4, command=self.fToparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=9, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_primero, text="", image=self.photo5, command=self.fFinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=10, padx=5, sticky="nsew", pady=2)

    def cuadro_entrys_movimientos(self):

        # Fecha del movimiento
        self.lbl_fecha_movim = Label(self.frame_tercero, text="Fecha: ", justify="left")
        self.lbl_fecha_movim.grid(row=0, column=0, padx=5, pady=2, sticky=W)
        self.entry_fecha_movim = Entry(self.frame_tercero, textvariable=self.strvar_fecha_movim, width=10,
                                       justify="right")
        self.entry_fecha_movim.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_movim.grid(row=0, column=1, padx=5, pady=2, sticky=W)

        # Detalle del movimiento
        self.lbl_detalle_movim = Label(self.frame_tercero, text="Detalle: ", justify="left")
        self.lbl_detalle_movim.grid(row=0, column=2, padx=5, pady=2, sticky=W)
        self.entry_detalle_movim = Entry(self.frame_tercero, textvariable=self.strvar_detalle_movim, width=125,
                                         justify="left")
        self.strvar_detalle_movim.trace("w", lambda *args: limitador(self.strvar_detalle_movim, 200))
        self.entry_detalle_movim.grid(row=0, column=3, columnspan = 30, padx=5, pady=2, sticky=W)

        # Importe Debito
        self.lbl_debito_movim = Label(self.frame_tercero, text="Debito: ", justify="left")
        self.lbl_debito_movim.grid(row=1, column=0, padx=5, pady=2, sticky=W)
        self.entry_debito_movim = Entry(self.frame_tercero, textvariable=self.strvar_debito_movim, width=20,
                                        justify="right")
        self.entry_debito_movim.config(validate="key", validatecommand=self.vcmd)
        self.entry_debito_movim.grid(row=1, column=1, padx=5, pady=2, sticky=W)
        self.entry_debito_movim.config(validate="key", validatecommand=self.vcmd)
        self.strvar_debito_movim.trace("w", lambda *args: self.limitador(self.strvar_debito_movim, 15))
        self.entry_debito_movim.bind('<Tab>', lambda e: self.calcular())

        # Importe Credito
        self.lbl_credito_movim = Label(self.frame_tercero, text="Credito: ", justify="left")
        self.lbl_credito_movim.grid(row=1, column=2, padx=5, pady=2, sticky=W)
        self.entry_credito_movim = Entry(self.frame_tercero, textvariable=self.strvar_credito_movim, width=20,
                                         justify="right")
        self.entry_credito_movim.config(validate="key", validatecommand=self.vcmd)
        self.entry_credito_movim.grid(row=1, column=3, padx=5, pady=2, sticky=W)
        self.entry_credito_movim.config(validate="key", validatecommand=self.vcmd)
        self.strvar_credito_movim.trace("w", lambda *args: self.limitador(self.strvar_credito_movim, 15))
        self.entry_credito_movim.bind('<Tab>', lambda e: self.calcular())

    def cuadro_botonestv(self):

        for c in range(5):
            self.frame_cuarto.grid_columnconfigure(c, weight=1, minsize=140)

        # Columnas mas cortas
        # self.botones1.grid_rowconfigure(0, weight=3, minsize=60)
        # self.frame_buscar.grid_columnconfigure(3, weight=1, minsize=50)
        # self.frame_buscar.grid_columnconfigure(2, weight=3, minsize=50)

        # Nuevo ingreso a cuenta
        img = Image.open("archivo-nuevo.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_nuevoitem = Button(self.frame_cuarto, text="Nuevo Item", command=self.fNuevo, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_nuevoitem.image = icono
        self.btn_nuevoitem.config(image=icono)
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)

        # Editar movimiento
        img = Image.open("editar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_editaitem = Button(self.frame_cuarto, text="Edita Item", command=self.fEditar, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_editaitem.image = icono
        self.btn_editaitem.config(image=icono)
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)

        # Borrar un movimiento
        img = Image.open("eliminar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_borraitem = Button(self.frame_cuarto, text="Elimina Item", command=self.fBorrar, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_borraitem.image = icono
        self.btn_borraitem.config(image=icono)
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)

        # Guardar movimiento en archivos
        img = Image.open("guardar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_guardaritem = Button(self.frame_cuarto, text="Guardar item", command=self.fGuardar, width=24,
                                      bg="green", fg="white", compound="left")
        self.btn_guardaritem.image = icono
        self.btn_guardaritem.config(image=icono)
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)

        # Cancelar lo que se este haciendo
        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_Cancelar = Button(self.frame_cuarto, text="Cancelar", command=self.fCancelar, width=24, bg="black",
                                   fg="white", compound="left")
        self.btn_Cancelar.image = icono
        self.btn_Cancelar.config(image=icono)
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_cuarto.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_cuarto, text="Salir", image=self.photo3, width=65, command=self.fSalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")


    def cuadro_grid_ctacte(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_ctacte)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_ctacte = ttk.Treeview(self.frame_tvw_ctacte, height=7, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5", "col6"))

        self.grid_ctacte.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_ctacte.column("#0", width=40, anchor="center", minwidth=60)
        self.grid_ctacte.column("col1", width=80, anchor="center", minwidth=60)
        self.grid_ctacte.column("col2", width=300, anchor="center", minwidth=200)
        self.grid_ctacte.column("col3", width=90, anchor="center", minwidth=80)
        self.grid_ctacte.column("col4", width=90, anchor="center", minwidth=80)
        self.grid_ctacte.column("col5", width=90, anchor="center", minwidth=80)
        self.grid_ctacte.column("col6", width=60, anchor="center", minwidth=80)

        self.grid_ctacte.heading("#0", text="Id", anchor="center")
        self.grid_ctacte.heading("col1", text="Fecha", anchor="center")
        self.grid_ctacte.heading("col2", text="Detalle", anchor="center")
        self.grid_ctacte.heading("col3", text="Debito", anchor="center")
        self.grid_ctacte.heading("col4", text="Credito", anchor="center")
        self.grid_ctacte.heading("col5", text="Saldo", anchor="center")
        self.grid_ctacte.heading("col6", text="Clave", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_ctacte, orient="horizontal")
        scroll_y = Scrollbar(self.frame_tvw_ctacte, orient="vertical")
        self.grid_ctacte.config(xscrollcommand=scroll_x.set)
        self.grid_ctacte.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_ctacte.xview)
        scroll_y.config(command=self.grid_ctacte.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_ctacte['selectmode'] = 'browse'

        self.grid_ctacte.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    # -------------------------------------------------------
    # INFORMES
    # -------------------------------------------------------

    def fImprime(self):

        # ---------------------------------------------------------------------------
        # VALIDACIONES

        # verifico que existan movimientos vargador en el grid
        self.mover_puntero_topend("TOP")
        self.selected = self.grid_ctacte.focus()
        if self.selected == "":
            messagebox.showwarning("Cuidado", "No existen movimientos o no selecciono cuenta", parent=self)
            return
        # Verifico que exista una cuenta cargada
        if self.strvar_codigo_cliente.get() == "" or self.strvar_codigo_cliente.get() == "0":
            messagebox.showwarning("Cuidado", "Seleccione una cuenta", parent=self)
            return
        # ---------------------------------------------------------------------------

        # Debo filtrar el cliente seleccionado
        adad = self.strvar_codigo_cliente.get()
        datos_registro_selec = self.varCtacte.consultar_ctacte("ctacte WHERE cc_codcli = '" + adad + "' ORDER BY cc_fecha")

        # Definir parametros listado
        """
        P : portrait (vertical)
        L : landscape (horizontal)
        A4 : 210x297mm
        """

        # esto siempre debe estar ------------------------------------------------------------
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # numero de paginas para luego usar en numeracion de pie de pagina
        pdf.alias_nb_pages()
        # Esto fuerza agregar una pagina al PDF
        pdf.add_page()
        # set de letra, tipo y tamaño
        pdf.set_font('Times', '', 12)
        # -----------------------------------------------------------------------------------

        # armado de encabezado --------------------------------------------------------------
        feactual = datetime.now()
        feac = feactual.strftime("%d-%m-%Y %H:%M:%S")

        # Imprimo el encabezado de pagina ---------------------------------------------------
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=0, h=5, txt='Saldos en Cuenta Corriente - Fecha y Hora: ' + feac , border=1, align='C', fill=0, ln=1)
        # -----------------------------------------------------------------------------------

        pdf.cell(w=17, h=8, txt='Fecha', border=1, align='C', fill=0)
        pdf.cell(w=110, h=8, txt='Detalle', border=1, align='C', fill=0)
        pdf.cell(w=20, h=8, txt='Ingreso', border=1, align='C', fill=0)
        pdf.cell(w=20, h=8, txt='Egreso', border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=8, txt='Saldo', border=1, align='C', fill=0)
        # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)
        pdf.set_font('Arial', '', 9)

        tot_saldo = 0
        for row in datos_registro_selec:

            fecha1 = datetime.strftime(row[1], "%d-%m-%Y")

            tot_saldo += row[3] - row[4]
            pdf.cell(w=17, h=6, txt=fecha1, border=1, align='C', fill=0)
            pdf.cell(w=110, h=6, txt=row[2], border=1, align='C', fill=0)
            pdf.cell(w=20, h=6, txt=str(row[3]), border=1, align='R', fill=0)
            pdf.cell(w=20, h=6, txt=str(row[4]), border=1, align='R', fill=0)
            pdf.multi_cell(w=0, h=6, txt=str(tot_saldo), border=1, align='R', fill=0)

        pdf.output('hoja.pdf')
        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # COMPACTAR MOVIMIENTOS
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def fCompactar(self):

        # ---------------------------------------------------------------------------
        # VALIDACIONES

        # verifico que existan movimientos vargador en el grid
        self.mover_puntero_topend("TOP")
        self.selected = self.grid_ctacte.focus()
        if self.selected == "":
            messagebox.showwarning("Cuidado", "No existen movimientos o no selecciono cuenta", parent=self)
            return
        # Verifico que exista una cuenta cargada
        if self.strvar_codigo_cliente.get() == "" or self.strvar_codigo_cliente.get() == "0":
            messagebox.showwarning("Cuidado", "Seleccione una cuenta", parent=self)
            return
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # DEFINO PANTALLA FLOTANTE

        self.pantalla_estad = Toplevel()
        self.pantalla_estad.geometry('630x390+660+380')
        self.pantalla_estad.transient(master=self.master)
        self.pantalla_estad.config(bg='light green', padx=5, pady=5)
        self.pantalla_estad.resizable(False, False)
        self.pantalla_estad.title("Compactar movimientos")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # TITULOS

        self.frame_titulo_compactar = Frame(self.pantalla_estad, bg="light green")

        # Armo el logo y el titulo
        self.photo = Image.open('ctacte.png')
        self.photo = self.photo.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_cta = ImageTk.PhotoImage(self.photo)
        self.lbl_png_cta = Label(self.frame_titulo_compactar, image=self.png_cta, bg="red", relief="ridge", bd=5)

        self.lbl_tit = Label(self.frame_titulo_compactar, width=22, text="Compactar",
                             bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_cta.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_tit.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_compactar.pack(side="top", fill="x", padx=5, pady=2)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # VARIABLES STRINGVARS

        # Fechas inferior y tope de compactacion
        self.strvar_fecha_inicial = StringVar(value="")
        self.strvar_fecha_ultima = StringVar(value="")
        self.strvar_fecha_tope_compactar = StringVar(value="")

        # Debitos y creditos existentes todos
        self.strvar_suma_debitos_ant = StringVar(value="0")
        self.strvar_suma_creditos_ant = StringVar(value="0")

        # Saldo inicial luego de borrar los debitos y creditos comprendidos entre las fechas a compactar
        self.strvar_nuevo_saldo_inicial = StringVar(value="0")

        # sumas de debitos y creditos a eliminar y recalculo del saldo para control
        self.strvar_suma_debitos_eliminar = StringVar(value="0")
        self.strvar_suma_creditos_eliminar = StringVar(value="0")
        self.strvar_saldo_despues_eliminar = StringVar(value="0")
        # ---------------------------------------------------------------------------

        # guardo filtro activo
        filtro_anterior = self.filtro_activo

        # ---------------------------------------------------------------------------
        # OBTENER PRIMERA FECHA DE MOVIMIENTOS

        self.mover_puntero_topend("TOP")
        # guardo item seleccionado en el grid
        self.selected = self.grid_ctacte.focus()
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        self.filtro_activo = f"ctacte WHERE id = {self.clave}"
        # Traigo el registro solamente el primero y  obtengo su fecha
        datos = self.varCtacte.consultar_ctacte(self.filtro_activo)
        primera_fecha = ""
        for i in datos:
            primera_fecha = i[1]
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # OBTENER ULTIMA FECHA DE MOVIMIENTOS

        self.mover_puntero_topend("END")
        # guardo item seleccionado en el grid
        self.selected = self.grid_ctacte.focus()
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        self.filtro_activo = f"ctacte WHERE id = {self.clave}"
        # Traigo el registro solamente el primero y  obtengo su fecha
        datos = self.varCtacte.consultar_ctacte(self.filtro_activo)
        ultima_fecha = ""
        for i in datos:
            ultima_fecha = i[1]
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # CONVERSION DE LAS FECHAS A FORMATO NUESTRO - fecha de 2024-12-19 a 19/12/2024

        forma_normal_inicial = fecha_str_reves_normal(self, datetime.strftime(primera_fecha, '%Y-%m-%d'), "hora_no")
        # sumo 30 dias a la primera fecha
        fecha_inicial_mas30 = primera_fecha + timedelta(days=30)

        forma_normal_final = fecha_str_reves_normal(self, datetime.strftime(fecha_inicial_mas30, '%Y-%m-%d'), "hora_no")
        forma_normal_ultima = fecha_str_reves_normal(self, datetime.strftime(ultima_fecha, '%Y-%m-%d'), "hora_no")

        self.strvar_fecha_inicial = StringVar(value=forma_normal_inicial)
        self.strvar_fecha_ultima = StringVar(value=forma_normal_ultima)
        self.strvar_fecha_tope_compactar = StringVar(value=forma_normal_final)

        self.strvar_suma_debitos_ant = StringVar(value=str(self.suma_debitos))
        self.strvar_suma_creditos_ant = StringVar(value=str(self.suma_creditos))
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # TOTAL SALDOS DEBITOS CREDITOS
        self.frame_info_saldos = LabelFrame(self.pantalla_estad, bg="light green")
        self.cuadro_saldos_estado_actual()
        self.frame_info_saldos.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # CUADRO DE INFORMACION SOBRE FECHAS
        self.frame_info_compactar = LabelFrame(self.pantalla_estad, bg="light green")
        self.cuadro_informacion_fechas()
        self.frame_info_compactar.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # ENTRY HASTA QUE FECHA COMPACTAR MOVIMIENTOS
        self.frame_parametros_compactar = LabelFrame(self.pantalla_estad, bg="light green")
        self.entrys_fecha_compactar()
        self.frame_parametros_compactar.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # BOTON PREVISUALIZAR RESULTADOS PARA CONTROL
        self.frame_botones_previsual = LabelFrame(self.pantalla_estad, bg="light green")
        self.botones_previsualizar()
        self.frame_botones_previsual.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        self.frame_previsualizar = LabelFrame(self.pantalla_estad, bg="light green")
        self.frame_previsualizar.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        # ---------------------------------------------------------------------------
        # BOTONES Continuar Canccelar
        self.frame_botones_compactar = LabelFrame(self.pantalla_estad, bg="light green")
        self.botones_compactar()
        self.frame_botones_compactar.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # vuelvo filtro activo a estado anterior
        self.filtro_activo = filtro_anterior

        self.pantalla_estad.grab_set()
        self.pantalla_estad.focus_set()

        mainloop()

    def fPrevisualizar(self):

        # Valida el rango de fechas
        if not self.validar_fecha(self.strvar_fecha_tope_compactar.get(), self.strvar_fecha_inicial.get(), self.strvar_fecha_ultima.get()):
            messagebox.showerror("Error", "Parametros de fecha incorrectos, verifique", parent=self)
            self.entry_fecha_compactar.focus_set()
            return

        # .......................................................................................
        # Suma los debitos y creditos entre las dos fechas solicitadas inclusive esas fechas ....
        # Seria la suma de debitos y creditos de los movimientos que se van a eliminar ----------
        # .......................................................................................

        """ Estas instrucciones SQL funcionaron bien
        #SELECT SUM(importe) AS total FROM ctacte WHERE fecha BETWEEN '2026-01-01' AND '2026-01-31'
        #SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte WHERE cc_fecha BETWEEN '2024-07-02' AND '2024-08-01' """

        # Debo mandar las fechas en formato "2026-05-12", tippo date
        fecha1 = self.strvar_fecha_inicial.get()
        fecha_convertida1 = datetime.strptime(fecha1, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha2 = self.strvar_fecha_tope_compactar.get()
        fecha_convertida2 = datetime.strptime(fecha2, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Consulta SQL
        self.filtro_activo = (f"SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte "
                              f"WHERE cc_fecha BETWEEN '{fecha_convertida1}' AND '{fecha_convertida2}' "
                              f"AND cc_codcli = '{self.strvar_codigo_cliente.get()}'")

        # Retorna totales de debito y credito a eliminar como una Tupla en retorno
        retorno = self.varCtacte.sumar_campactar(self.filtro_activo)

        # Muestro suma de debitos y creditos y tambien el total de lo que sera el movimiento a ingresar omo saldo inicial
        self.strvar_suma_debitos_eliminar.set(value=retorno[0])
        self.strvar_suma_creditos_eliminar.set(value=retorno[1])
        self.strvar_nuevo_saldo_inicial.set(value=retorno[0] - retorno[1])

        # Calcular el nuevo saldo para control SIN tener en cuenta los movimientos a eliminar
        self.filtro_activo = (f"SELECT SUM(cc_ingreso-cc_egreso) AS nuevo_saldo FROM ctacte "
                              f"WHERE (cc_fecha < '{fecha_convertida1}' AND cc_codcli = '{self.strvar_codigo_cliente.get()}') "
                              f"OR (cc_fecha > '{fecha_convertida2}' AND cc_codcli = '{self.strvar_codigo_cliente.get()}')")

        # Vuelve el total del nuevo saldo calculado con los movimientos que quedarian + el nuevo saldo inicial OJO
        retorno = self.varCtacte.sumar_saldo_control(self.filtro_activo)

        # OJO sumarle el nuevo saldo inicial
        con_saldoini = float(retorno[0]) + float(self.strvar_nuevo_saldo_inicial.get())

        self.strvar_saldo_despues_eliminar.set(value=str(con_saldoini))

        # ---------------------------------------------------------------------------------
        # VISUALIZACION DE TOTALES DE CONTROL

        fff = tkFont.Font(family="Arial", size=10, weight="bold")

        for c in range(4):
            self.frame_previsualizar.grid_columnconfigure(c, weight=1, minsize=120)

        # Suma de los debitos a eliminar
        self.lbl_suma_debitos_eliminar_tit = Label(self.frame_previsualizar, text="Suma debitos a eliminar: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_suma_debitos_eliminar_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_suma_debitos_eliminar_var = Label(self.frame_previsualizar, textvariable=self.strvar_suma_debitos_eliminar,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_suma_debitos_eliminar_var.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        # Suma de los creditos a eliminar
        self.lbl_suma_creditos_eliminar_tit = Label(self.frame_previsualizar, text="Suma creditos a eliminar: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_suma_creditos_eliminar_tit.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_suma_creditos_eliminar_var = Label(self.frame_previsualizar, textvariable=self.strvar_suma_creditos_eliminar,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_suma_creditos_eliminar_var.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")

        # muestro el importe del movimiento que voy a generar como saldo inicial
        self.lbl_nuevo_saldo_inicial_tit = Label(self.frame_previsualizar, text="Nuevo saldo inicial: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_inicial_tit.grid(row=1, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_nuevo_saldo_inicial_var = Label(self.frame_previsualizar, textvariable=self.strvar_nuevo_saldo_inicial,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_inicial_var.grid(row=1, column=1, padx=5, pady=3, sticky="nsew")

        # Saldo resultante de estos movimientos (debe coincidir con el anterior)
        self.lbl_nuevo_saldo_final_tit = Label(self.frame_previsualizar, text="Saldo resultante: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_final_tit.grid(row=1, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_nuevo_saldo_final_var = Label(self.frame_previsualizar, textvariable=self.strvar_saldo_despues_eliminar,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_final_var.grid(row=1, column=3, padx=5, pady=3, sticky="nsew")

        for widg in self.frame_previsualizar.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

        if float(self.strvar_saldo_cliente.get()) != float(self.strvar_saldo_despues_eliminar.get()):
            messagebox.showerror("Error", "No coinciden los saldos finales, verifique", parent=self)
            self.entry_fecha_compactar.focus_set()
            return

    def botones_previsualizar(self):

        self.btn_previsualizar = Button(self.frame_botones_previsual, text=" Previsualizacion",
                                             command=self.fPrevisualizar, width=50, bg="black", fg="white",
                                             compound="left")
        self.btn_previsualizar.grid(row=0, column=0, padx=5, pady=5)
        # ........................................................................................
        # Centra el boton dentro del LabelFrame                                                  .
        # Con weight = 1, la columna se expande y el botón queda centrado horizontalmente.       .
        # ........................................................................................
        self.frame_botones_previsual.grid_columnconfigure(0, weight=1)
        # ........................................................................................

    def botones_compactar(self):

        for c in range(2):
            self.frame_botones_compactar.grid_columnconfigure(c, weight=1, minsize=140)

        img = Image.open("ejecucion.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_cancelar_compactar = Button(self.frame_botones_compactar, text=" Continuar",
                                             command=self.fEjecutar_compactar, width=24, bg="black", fg="white",
                                             compound="left")
        self.btn_cancelar_compactar.image = icono
        self.btn_cancelar_compactar.config(image=icono)
        self.btn_cancelar_compactar.grid(row=0, column=0, padx=5, pady=3)

        img = Image.open("cancelar.png").resize((18, 18))
        icono = ImageTk.PhotoImage(img)
        self.btn_cancelar_compactar = Button(self.frame_botones_compactar, text=" Salir",
                                             command=self.fSalir_compactar, width=24, bg="black", fg="white",
                                             compound="left")
        self.btn_cancelar_compactar.image = icono
        self.btn_cancelar_compactar.config(image=icono)
        self.btn_cancelar_compactar.grid(row=0, column=1, padx=5, pady=3)
        # ---------------------------------------------------------------------------

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_compactar.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')


    def validar_fecha(self, fecha_tope, fecha_inicial, fecha_ultima):

        # las paso a formato date
        f1 = datetime.strptime(fecha_tope, "%d/%m/%Y")
        f2 = datetime.strptime(fecha_inicial, "%d/%m/%Y")

        # Si la fecha tope(hasta donde voy a compactar inclusive) < Fecha inicial (fecha minima de los movimientos)
        if f1 < f2:
            return FALSE

        # las paso a formato date
        f1 = datetime.strptime(fecha_tope, "%d/%m/%Y")
        f2 = datetime.strptime(fecha_ultima, "%d/%m/%Y")

        # Si la fecha tope(hasta donde voy a compactar inclusive) >= Fecha del ultimo movimiento que registra la cuenta
        if f1 >= f2:
            return FALSE

        return True

    def entrys_fecha_compactar(self):

        # Muestra los parametros de fechas para el intervalo a compactar
        fff = tkFont.Font(family="Arial", size=10, weight="bold")

        # Desde que fecha compacto - Por defecto es desde la mas vieja
        self.lbl_fecha_inicial_tit = Label(self.frame_parametros_compactar, text="Compactar: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_fecha_inicial_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_inicial_tit = Label(self.frame_parametros_compactar, text="Desde : Fecha inicial: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_fecha_inicial_tit.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_inicial_var = Label(self.frame_parametros_compactar, textvariable=self.strvar_fecha_inicial,
                                           bg="light green", bd=5)
        self.lbl_fecha_inicial_var.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")

        # Hasta que fecha compacto - Fecha a elegirse (control sobre esta fecha que no supere algunos parametros)
        # Por defecto le sumamos 30 dias
        self.lbl_fecha_final = Label(self.frame_parametros_compactar, text="Hasta: Fecha final: ", font=fff,
                                     bg="light green", bd=5, justify="center")
        self.lbl_fecha_final.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")
        self.entry_fecha_compactar = Entry(self.frame_parametros_compactar, textvariable=self.strvar_fecha_tope_compactar,
                                      bd=5, width=10, justify="right")
        self.entry_fecha_compactar.bind("<FocusOut>", self.formato_fecha_compactar)
        self.entry_fecha_compactar.grid(row=0, column=4, padx=5, pady=3, sticky="nsew")

        for widg in self.frame_parametros_compactar.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_informacion_fechas(self):

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        # Fecha mas baja de los movimientos actuales
        self.lbl_fecha_primer_movimiento_tit = Label(self.frame_info_compactar, text="Fecha primer movimiento: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_fecha_primer_movimiento_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_primer_movimiento_var = Label(self.frame_info_compactar, textvariable=self.strvar_fecha_inicial,
                                                     bg="light green", bd=5)
        self.lbl_fecha_primer_movimiento_var.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        # Fecha mas alta de los movimientos actuales
        self.lbl_fecha_ultimo_movimiento_tit = Label(self.frame_info_compactar, text="Fecha ultimo movimiento: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_fecha_ultimo_movimiento_tit.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_ultimo_movimiento_var = Label(self.frame_info_compactar, textvariable=self.strvar_fecha_ultima,
                                                     bg="light green", bd=5)
        self.lbl_fecha_ultimo_movimiento_var.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")

    def cuadro_saldos_estado_actual(self):

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        # El saldo actual
        self.lbl_saldo_tit = Label(self.frame_info_saldos, text="Saldo a la fecha: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_saldo_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_saldo_var = Label(self.frame_info_saldos, textvariable=self.strvar_saldo_cliente,
                                                     bg="light green", bd=5)
        self.lbl_saldo_var.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        # Suma de los debitos antes de compactacion (todos)
        self.lbl_debitos_tit = Label(self.frame_info_saldos, text="Debitos: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_debitos_tit.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_debitos_var = Label(self.frame_info_saldos, textvariable=self.strvar_suma_debitos_ant,
                                                     bg="light green", bd=5)
        self.lbl_debitos_var.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")

        # Suma de los creditos antes de compactacion (todos)
        self.lbl_creditos_tit = Label(self.frame_info_saldos, text="Creditos: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_creditos_tit.grid(row=0, column=4, padx=5, pady=3, sticky="nsew")
        self.lbl_creditos_var = Label(self.frame_info_saldos, textvariable=self.strvar_suma_creditos_ant,
                                                     bg="light green", bd=5)
        self.lbl_creditos_var.grid(row=0, column=5, padx=5, pady=3, sticky="nsew")

    def fEjecutar_compactar(self):

        confirma = messagebox.askquestion("Confirmar", "Confirma continuar con ajuste de movimientos de la cuenta?? "+ self.strvar_nombre_cliente.get(),
                                          parent=self.frame_info_compactar)
        if confirma == messagebox.NO:
            self.entry_fecha_compactar.focus_set()
            return

        """ 
        Estas instrucciones funcionaron
        #SELECT SUM(importe) AS total FROM ctacte WHERE fecha BETWEEN '2026-01-01' AND '2026-01-31'
        #SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte WHERE cc_fecha BETWEEN '2024-07-02' AND '2024-08-01' 
        """

        # --------------------------------------------------------------------------------
        # CALCULO EL SALDO INICIAL QUE QUEDARIA PARA COLOCAR EN LA TABLA LUEGO DE BORRAR

        # debo mandar las fechas en formato "2026-05-12"
        fecha1 = self.strvar_fecha_inicial.get()
        fecha_convertida1 = datetime.strptime(fecha1, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha2 = self.strvar_fecha_tope_compactar.get()
        fecha_convertida2 = datetime.strptime(fecha2, "%d/%m/%Y").strftime("%Y-%m-%d")

        self.filtro_activo = (f"SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte "
                              f"WHERE cc_fecha BETWEEN '{fecha_convertida1}' AND '{fecha_convertida2}' "
                              f"AND cc_codcli = '{self.strvar_codigo_cliente.get()}'")

        # vuelven los totales de debito y los de credito a eliminar como una tupla en retorno
        retorno = self.varCtacte.sumar_campactar(self.filtro_activo)

        # nuevo saldo inicial
        # self.strvar_suma_debitos_eliminar.set(value=retorno[0])
        # self.strvar_suma_creditos_eliminar.set(value=retorno[1])
        self.strvar_nuevo_saldo_inicial.set(value=retorno[0] - retorno[1])
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # CARGO VARIABLES PARA INGRESAR A LA TABLA

        # Cargo las variables para mandar el registro con el nuevo saldo inicial con la fecha inferior
        self.strvar_clavemov.set(value="0")
        self.strvar_detalle_movim.set(value="Saldo de compactacion")
        self.strvar_debito_movim.set(value="0")
        self.strvar_credito_movim.set(value="0")
        if float(self.strvar_nuevo_saldo_inicial.get()) < 0:
            #self.strvar_debito_movim.set(value="0")
            self.strvar_credito_movim.set(value=str((self.strvar_nuevo_saldo_inicial.get()))*-1)
        if float(self.strvar_nuevo_saldo_inicial.get()) > 0:
            self.strvar_debito_movim.set(value=str(self.strvar_nuevo_saldo_inicial.get()))
            #self.strvar_credito_movim.set(value="0")

        # EL resto de los campos ya estan cargados
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # MENSAJES

        #........................................................................
        # ejempos de mensajes para metodo toast                                 .
        # self.mostrar_toast("✅ Borrado correcto", 2500, "success")            .
        # self.mostrar_toast("❌ Error al borrar", 4000, "error")               .
        # self.mostrar_toast("🧹 Iniciando borrado...", 2000, "info")           .
        #........................................................................

        # Mensajes mientras procesamos
        self.mostrar_toast("🧹 Iniciando borrado de registros...", "green", 2500, "")
        # --- proceso real ---
        self.pantalla_estad.after(3000, lambda: self.mostrar_toast("✅ Proceso finalizado", "green", 2500, ""))
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # BORRAR MOVIMIENTOS DE COMPACTACION

        # ....................................................................................................
        # Primero elimino los movimientos antes de dar alta al nuevo saldo inicial, si lo hago despues       .
        # tambien me lo borraria.                                                                            .
        # ....................................................................................................

        self.filtro_activo= (f"DELETE FROM ctacte WHERE cc_fecha >= '{fecha_convertida1}' AND "
                             f"cc_fecha <= '{fecha_convertida2}' AND cc_codcli = '{self.strvar_codigo_cliente.get()}'")

        # metodo de borrado de los movimientos seleccionados entre fechas
        retorno = self.varCtacte.borrar_campactar(self.filtro_activo)
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # INGRESAR EL MOVIMIENTO CON EL NUEVO SALDO INICIAL

        # Ingreso el movimiento del nuevo saldo inicial
        fecha_aux = datetime.strptime(self.strvar_fecha_tope_compactar.get(), '%d/%m/%Y')
        self.varCtacte.insertar_ctacte(fecha_aux, self.strvar_detalle_movim.get(),
                                       self.strvar_debito_movim.get(), self.strvar_credito_movim.get(),
                                       self.strvar_codigo_cliente.get(), self.strvar_nombre_cliente.get(),
                                       self.strvar_clavemov.get())

    def mostrar_toast(self, mensaje, pa_color, duracion=3000, tipo="info"):

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

        toast = tk.Toplevel(self.pantalla_estad)
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
        self.pantalla_estad.update_idletasks()
        toast.update_idletasks()

        ventana_x = self.pantalla_estad.winfo_rootx()
        ventana_y = self.pantalla_estad.winfo_rooty()
        ventana_ancho = self.pantalla_estad.winfo_width()
        ventana_alto = self.pantalla_estad.winfo_height()

        toast_ancho = toast.winfo_width()
        toast_alto = toast.winfo_height()

        x = ventana_x + ventana_ancho - toast_ancho - 20
        y = ventana_y + ventana_alto - toast_alto - 50

        toast.geometry(f"+{x}+{y}")

        # Auto cerrar
        toast.after(duracion, toast.destroy)

    def fSalir_compactar(self):
        self.pantalla_estad.destroy()


