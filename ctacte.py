import os
import tkinter as tk
import tkinter.font as tkfont
from datetime import date, timedelta
from tkinter import ttk
from PIL import Image, ImageTk
from PDF_clase import *
from ctacte_ABM import DatosCtacte
from funcion_new import ClaseFuncionNew
from funciones import *
from status_bar import StatusBar


class ClaseCuentaCorriente(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master, width=880, height=510)
        self.master = master
        self.status = StatusBar(self.master)

        self.master.grab_set()
        self.master.focus_set()

        # ------------------------------------------------------------------------------
        # Instanciaciones-Creo una instancia de clientesABM y de funcion_new
        self.varCtacte = DatosCtacte(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
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
        hventana = 470
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
        self.frame_titulo_top = tk.Frame(self.master)
        # Armo el logo y el titulo
        self.photocc = Image.open('ctacte.png')
        self.photocc = self.photocc.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ctacte = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_ctacte = tk.Label(self.frame_titulo_top, image=self.png_ctacte, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=52, text="Cuentas Corrientes",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ctacte.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # STRINGVARS
        # ------------------------------------------------------------------
        self.sv_nombre_cliente = tk.StringVar(value="")
        self.sv_codigo_cliente = tk.StringVar(value="0")
        self.sv_fecha_movim = tk.StringVar(value="")
        self.sv_detalle_movim = tk.StringVar(value="")
        self.sv_saldo_cliente = tk.StringVar(value="0.00")
        self.sv_debito_movim = tk.StringVar(value="0.00")
        self.sv_credito_movim = tk.StringVar(value="0.00")
        self.sv_clavemov = tk.StringVar(value="0")

        # ------------------------------------------------------------------------------
        # VARIABLES GENERALES
        # ------------------------------------------------------------------
        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.sv_fecha_movim = tk.StringVar(value=una_fecha)
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------
        # GRID - TREVIEEW
        # ------------------------------------------------------------------
        self.frame_tvw_ctacte=tk.LabelFrame(self.master, text="Cuentas Corrientes: ", foreground="#CF09BD")
        self.cuadro_grid_ctacte()
        self.frame_tvw_ctacte.pack(side="top", fill="both", padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # ENTRYS
        # ------------------------------------------------------------------
        self.frame_primero=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys()
        self.frame_primero.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ---------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------
        # ENTRYS MOVIMIENTOS
        self.frame_tercero=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_entrys_movimientos()
        self.frame_tercero.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # BOTONES TREEVIEW
        # ------------------------------------------------------------------
        self.frame_cuarto=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_botonestv()
        self.frame_cuarto.pack(side="top", fill="both", expand=0, padx=5, pady=2)
        # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # GRID
    # ------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_ctacte.get_children():
            self.grid_ctacte.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varCtacte.consultar_ctacte(self.filtro_activo)
        else:
            datos = self.varCtacte.consultar_ctacte("ctacte ORDER BY cc_fecha ASC")

        self.suma_debitos = 0
        self.suma_creditos = 0
        self.suma_saldos = 0

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)
            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[1], '%Y-%m-%d'), False)

            self.suma_saldos += row[3] - row[4]
            self.grid_ctacte.insert("", "end", tags=color, text=row[0], values=(forma_normal, row[2],
                                                                            row[3], row[4], self.suma_saldos, row[7]))
            self.suma_debitos += row[3]
            self.suma_creditos += row[4]

        self.sv_saldo_cliente.set(value=str((self.suma_debitos-self.suma_creditos)))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_ctacte.get_children()
        # Si no hay filas (grid vacio), salgo sin intentar seleccionar
        if not children:
            self.status.set_status("ℹ Grid vacio...", "info")
            return

        # Si el parametro set_foco esta vacío (no hay foco), voy al ultimo de la grilla,
        # caso contrario, voy a la clave que se haya enviado en set_foco para dejar el puntero.
        if not set_foco:
            # self.grid_orden.selection_set(children[0]) # asi tambien voy al ultimo
            posicion = children[-1]                      # ultimo
            # posicion = children[0]                     # primero
            self.grid_ctacte.focus_set()
            self.grid_ctacte.focus(posicion)
            self.grid_ctacte.selection_set(posicion)
            self.grid_ctacte.see(posicion)
        else:
            for item in children:
                texto = self.grid_ctacte.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_ctacte.update_idletasks()
                    self.grid_ctacte.focus_set()
                    self.grid_ctacte.selection_set(item)
                    self.grid_ctacte.focus(item)
                    self.grid_ctacte.see(item)
                    break

    def estado_inicial(self):

        self.filtro_activo = "ctacte WHERE cc_codcli = 0 ORDER BY cc_fecha ASC"
        self.alta_modif = 0
        self.habilitar_text("disabled")
        self.habilitar_btn_final("disabled")
        self.habilitar_btn_busquedas("disabled")
        self.habilitar_btn_oper("disabled")
        self.entry_nombre_cliente.focus()

    def limpiar_text(self):

        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.sv_fecha_movim.set(value=una_fecha)
        self.entry_detalle_movim.delete(0, "end")
        self.sv_debito_movim.set(value="0.00")
        self.sv_credito_movim.set(value="0.00")

    def habilitar_text(self, estado):

        self.entry_fecha_movim.configure(state=estado)
        self.entry_detalle_movim.configure(state=estado)
        self.entry_debito_movim.configure(state=estado)
        self.entry_credito_movim.configure(state=estado)

    def habilitar_btn_oper(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)
        self.btn_compactar.configure(state=estado)

    def habilitar_btn_final(self, estado):
        self.btn_guardaritem.configure(state=estado)

    def habilitar_btn_busquedas(self, estado):
        self.btn_imprime.configure(state=estado)

    def reset_stringvars(self):

        self.sv_nombre_cliente.set(value="")
        self.sv_codigo_cliente.set(value="0")
        una_fecha = datetime.strftime(date.today(), "%d/%m/%Y")
        self.sv_fecha_movim.set(value=una_fecha)
        self.sv_detalle_movim.set(value="")
        self.sv_saldo_cliente.set(value="0.00")
        self.sv_debito_movim.set(value="0.00")
        self.sv_credito_movim.set(value="0.00")

    def reset_campos(self):

        self.sv_detalle_movim.set(value="")
        self.sv_debito_movim.set(value="0.00")
        self.sv_credito_movim.set(value="0.00")

    def freset_selcli(self):

        self.entry_nombre_cliente.configure(state="normal")
        self.btn_bus_cli.configure(state="normal")
        self.sv_nombre_cliente.set(value="")
        self.sv_codigo_cliente.set(value="0")
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_oper("disabled")
        self.habilitar_btn_final("disabled")
        self.sv_saldo_cliente.set(value="0")

        self.entry_nombre_cliente.focus()

    def fcancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelacion?", parent=self)
        if r == messagebox.NO:
            return

        self.entry_nombre_cliente.configure(state="normal")
        self.btn_bus_cli.configure(state="normal")
        self.sv_nombre_cliente.set(value="")
        self.sv_codigo_cliente.set(value="0")
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_oper("disabled")
        self.habilitar_btn_final("disabled")
        self.sv_saldo_cliente.set(value="0.00")
        self.entry_nombre_cliente.focus()

    # -------------------------------------------------------------
    # CRUD
    # -------------------------------------------------------------

    def fnuevo(self):

        # VALIDACIONES

        if self.sv_nombre_cliente.get() == "" or self.sv_codigo_cliente.get() == "0":
            messagebox.showwarning("Error", " Debe existir un cliente asignado", parent=self)
            self.entry_nombre_cliente.focus()
            return

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.habilitar_btn_busquedas("disabled")
        self.habilitar_btn_oper("disabled")
        self.habilitar_btn_final("normal")
        self.entry_fecha_movim.focus()

    def feditar(self):

        # ------------------------------------------------------------------------
        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_ctacte.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        # ------------------------------------------------------------------------

        if self.clave == "":
            self.status.set_status("ℹ No hay nada seleccionado...", "info")
            return

        self.alta_modif = 2

        self.habilitar_text('normal')

        # Obtengo todos los valores de la fila seleccionada
        valores = self.grid_ctacte.item(self.selected, 'values')

        self.sv_fecha_movim.set(value=valores[0])
        self.sv_detalle_movim.set(value=valores[1])
        self.sv_debito_movim.set(value=valores[2])
        self.sv_credito_movim.set(value=valores[3])

        self.habilitar_text("normal")
        self.habilitar_btn_oper("disabled")
        self.habilitar_btn_final("normal")
        self.entry_nombre_cliente.focus()

    def fborrar(self):

        # -----------------------------------------------------------------------
        # guardo item seleccionado en el grid
        self.selected = self.grid_ctacte.focus()
        self.selected_ant = self.grid_ctacte.prev(self.selected)
        # guardo el Id del item correspondiente a la Tabla
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        self.clave_ant = self.grid_ctacte.item(self.selected_ant, 'text')
        # -----------------------------------------------------------------------

        # guardo la clae de movimiento anterior si la hay
        self.clavemov_ant = 0

        if self.clave == "":
            self.status.set_status("ℹ No hay nada seleccionado...", "info")
            return

        valores = self.grid_ctacte.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[2]

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            messagebox.showinfo("Eliminar", "Eliminacion cancelada", parent=self)
            return

        # Elimino item ----------------------------------------------
        self.varCtacte.eliminar_item_ctacte(self.clave)
        # -----------------------------------------------------------

        self.status.set_status("🗑 Registro eliminado correctamente", "ok")
        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # ----------------------------------------------------------------
        # VALIDACIONES
        # ----------------------------------------------------------------

        # FECHA
        if self.sv_fecha_movim.get() == "":
            self.status.set_status("❌ Fecha en blanco", "error")
            self.entry_fecha_movim.focus()
            return
        # DETALLE
        if self.sv_detalle_movim.get() == "":
            self.status.set_status("❌ Agregue detalle", "error")
            self.entry_detalle_movim.focus()
            return
        # CAMPOS DE IMPORTE
        if self.sv_debito_movim.get() == "0.00" and self.sv_credito_movim.get() == "0.00":
            self.status.set_status("❌ No ingreso importes", "error")
            self.entry_debito_movim.focus()
            return
        # ----------------------------------------------------------------

        # -------------------------------------------------------------
        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori
        self.selected = self.grid_ctacte.focus()
        # Guardo el Id del registro de la base de datos (no es el mismo que el otro, este puedo verlo en la base)
        self.clave = self.grid_ctacte.item(self.selected, 'text')
        # -------------------------------------------------------------

        fecha_aux = datetime.strptime(self.sv_fecha_movim.get(), '%d/%m/%Y')
        dic_ctacte = self.get_ctacte_dic(fecha_aux)    # funcion que genera el diccionario

        id_ref = ""
        try:
            if self.alta_modif == 1:
                # debe ser cero si es un alta de nuevo movimiento
                self.sv_clavemov.set(value="0")
                id_ref = self.varCtacte.insertar_ctacte(dic_ctacte)
            elif self.alta_modif == 2:
                self.sv_clavemov.set(value="0")
                id_ref = self.varCtacte.modificar_ctacte(dic_ctacte)
        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Insertar/Modificar", str(e))
            return
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        # cierre de las novedades y reseteando pantalla para nuevo movimiento - actualizando grilla
        self.reset_campos()
        # Deshabilitar variables a estado cero
        self.habilitar_text("disabled")
        # rehabilitar botones correspondientes
        self.habilitar_btn_oper("normal")
        self.habilitar_btn_final("disabled")
        self.llena_grilla(id_ref)
        self.btn_nuevoitem.focus()

    def doble_click_grid(self, _event):
        self.feditar()

    def fsalir(self):
        self.master.destroy()

    # -------------------------------------------------------
    # PUNTERO
    # -------------------------------------------------------

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_ctacte,"TOP")

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_ctacte, 'END')

    def fbuscli(self):

        """
        Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en que
        campos debe hacerse
        """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.sv_nombre_cliente.get() + "') > 0" \
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
            self.sv_nombre_cliente.set(value=item[15])
            self.sv_codigo_cliente.set(value=item[1])

        self.habilitar_btn_busquedas("normal")
        self.habilitar_btn_oper("normal")

        # si el codigo de cliente no es cero, filtro la tabla por el cliente seleccionado
        if int(self.sv_codigo_cliente.get()) != 0:

            # filtrar la cuenta corriente para este cliente
            self.filtro_activo = "ctacte WHERE cc_codcli = '" + self.sv_codigo_cliente.get() +" ' ORDER BY cc_fecha"

            self.llena_grilla("")

            # inhabilito edicion de nombre de cliente para que no pueda cambiarlo
            self.entry_nombre_cliente.configure(state="disabled")
            self.btn_bus_cli.configure(state="disabled")

    # -------------------------------------------------------
    # VALIDACIONES
    # -------------------------------------------------------

    def formato_fecha_compactar(self, _pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        # FUNCION VALIDA FECCHAS en modulo funcion
        retorno_validacion = self.varFuncion_new.validar_fecha(self.sv_fecha_tope_compactar, self.entry_fecha_compactar)

        una_fecha = date.today()

        match retorno_validacion:

            case "break":
                self.entry_fecha_compactar.focus()
                return
            case "S":
                self.entry_fecha_compactar.focus()
            case "N" | "BLANCO":
                pass
            case "":
                self.sv_fecha_tope_compactar.set(una_fecha.strftime('%d/%m/%Y'))
                self.entry_fecha_compactar.focus()
            case _:
                return

    def formato_fecha(self, _pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
            le paso la fecha tipo string con barras o sin barras """

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_validacion = self.varFuncion_new.validar_fecha(self.sv_fecha_movim, self.entry_fecha_movim)

        una_fecha = date.today()

        match retorno_validacion:

            case "break":
                self.entry_fecha_movim.focus()
                return
            case "S":
                self.entry_fecha_movim.focus()
            case "N" | "BLANCO":
                pass
            case "":
                self.sv_fecha_movim.set(una_fecha.strftime('%d/%m/%Y'))
                self.entry_fecha_movim.focus()
            case _:
                return

    @staticmethod
    def limitador(entry_text, caract):
        if len(entry_text.get()) > 0:
            # donde esta CARACT va la cantidad de caracteres
            entry_text.set(entry_text.get()[:caract])

    def calcular(self):

        self.sv_debito_movim.set(value=self.varFuncion_new.corregir_valor(self.sv_debito_movim.get()))
        self.sv_credito_movim.set(value=self.varFuncion_new.corregir_valor(self.sv_credito_movim.get()))

    def cuadro_entrys(self):

        # DATOS NOMBRE CLIENTE
        self.lbl_texto_nombre_cliente = tk.Label(self.frame_primero, text="Cliente: ", justify="left")
        self.lbl_texto_nombre_cliente.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_nombre_cliente = tk.Entry(self.frame_primero, textvariable=self.sv_nombre_cliente, width=48)
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        self.lbl_texto_codigo_cliente = tk.Label(self.frame_primero, textvariable=self.sv_codigo_cliente, width=10 )
        self.lbl_texto_codigo_cliente.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        # BOTON BUSCAR CLIENTE EN LISTBOX
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = tk.Button(self.frame_primero, text="", image=self.photo_bus_cli, command=self.fbuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=3, padx=5)

        # BOTON RESET BUSQUEDA DE CLIENTE - HABILLITO ENTRY DEL NOMBRE
        self.photo_reset_cli = Image.open('reset.png')
        self.photo_reset_cli = self.photo_reset_cli.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_reset_cli = ImageTk.PhotoImage(self.photo_reset_cli)
        self.btn_reset_cli = tk.Button(self.frame_primero, text="", image=self.photo_reset_cli, command=self.freset_selcli,
                                    bg="grey", fg="white")
        self.btn_reset_cli.grid(row=0, column=4, padx=5)

        # Saldo del cliente
        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        self.lbl_saldo_cliente = tk.Label(self.frame_primero, text="Saldo: ", font=fff, justify="left")
        self.lbl_saldo_cliente.grid(row=0, column=5, padx=5, pady=2, sticky="w")
        self.lbl_importe_saldo_cliente = tk.Label(self.frame_primero, textvariable=self.sv_saldo_cliente, width=20,
                                               font=fff, justify="left")
        self.lbl_importe_saldo_cliente.grid(row=0, column=6, padx=5, pady=2, sticky="w")

        # Boton para compactar
        self.btn_compactar = tk.Button(self.frame_primero, text="Compactar", command=self.fcompactar, width=15,
                                    bg="medium purple", fg="white")
        self.btn_compactar.grid(row=0, column=7, padx=4, pady=2)

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = tk.Button(self.frame_primero, image=self.photo_imp, pady=3, command=self.fimprime, border=3)
        self.btn_imprime.grid(row=0, column=8, padx=4, pady=2)
        #self.btnPlaniCaja.place(x=555, y=10, width=100, height=100)

        # botones fin y principio archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_primero, text="", image=self.photo4, command=self.ftoparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=9, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_primero, text="", image=self.photo5, command=self.ffinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=10, padx=5, sticky="nsew", pady=2)

    def cuadro_entrys_movimientos(self):

        # Fecha del movimiento
        self.lbl_fecha_movim = tk.Label(self.frame_tercero, text="Fecha: ", justify="left")
        self.lbl_fecha_movim.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_fecha_movim = tk.Entry(self.frame_tercero, textvariable=self.sv_fecha_movim, width=10,
                                       justify="right")
        self.entry_fecha_movim.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_movim.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        # Detalle del movimiento
        self.lbl_detalle_movim = tk.Label(self.frame_tercero, text="Detalle: ", justify="left")
        self.lbl_detalle_movim.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_detalle_movim = tk.Entry(self.frame_tercero, textvariable=self.sv_detalle_movim, width=125,
                                         justify="left")
        self.sv_detalle_movim.trace("w", lambda *args: limitador(self.sv_detalle_movim, 200))
        self.entry_detalle_movim.grid(row=0, column=3, columnspan = 30, padx=5, pady=2, sticky="w")

        # Importe Debito
        self.lbl_debito_movim = tk.Label(self.frame_tercero, text="Debito: ", justify="left")
        self.lbl_debito_movim.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_debito_movim = tk.Entry(self.frame_tercero, textvariable=self.sv_debito_movim, width=20,
                                        justify="right")
        self.entry_debito_movim.config(validate="key", validatecommand=self.vcmd)
        self.entry_debito_movim.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        self.entry_debito_movim.config(validate="key", validatecommand=self.vcmd)
        self.sv_debito_movim.trace("w", lambda *args: self.limitador(self.sv_debito_movim, 15))
        self.entry_debito_movim.bind('<Tab>', lambda e: self.calcular())

        # Importe Credito
        self.lbl_credito_movim = tk.Label(self.frame_tercero, text="Credito: ", justify="left")
        self.lbl_credito_movim.grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.entry_credito_movim = tk.Entry(self.frame_tercero, textvariable=self.sv_credito_movim, width=20,
                                         justify="right")
        self.entry_credito_movim.config(validate="key", validatecommand=self.vcmd)
        self.entry_credito_movim.grid(row=1, column=3, padx=5, pady=2, sticky="w")
        self.entry_credito_movim.config(validate="key", validatecommand=self.vcmd)
        self.sv_credito_movim.trace("w", lambda *args: self.limitador(self.sv_credito_movim, 15))
        self.entry_credito_movim.bind('<Tab>', lambda e: self.calcular())

    def cuadro_botonestv(self):

        for c in range(5):
            self.frame_cuarto.grid_columnconfigure(c, weight=1, minsize=140)

        # Columnas mas cortas
        # self.botones1.grid_rowconfigure(0, weight=3, minsize=60)
        # self.frame_buscar.grid_columnconfigure(3, weight=1, minsize=50)
        # self.frame_buscar.grid_columnconfigure(2, weight=3, minsize=50)

        # Nuevo ingreso a cuenta
        icono = self.cargar_icono("archivo-nuevo.png")
        self.btn_nuevoitem = tk.Button(self.frame_cuarto, text="Nuevo Item", command=self.fnuevo, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_nuevoitem.image = icono
        self.btn_nuevoitem.config(image=icono)
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)

        # Editar movimiento
        icono = self.cargar_icono("editar.png")
        self.btn_editaitem = tk.Button(self.frame_cuarto, text="Edita Item", command=self.feditar, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_editaitem.image = icono
        self.btn_editaitem.config(image=icono)
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)

        # Borrar un movimiento
        icono = self.cargar_icono("eliminar.png")
        self.btn_borraitem = tk.Button(self.frame_cuarto, text="Elimina Item", command=self.fborrar, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_borraitem.image = icono
        self.btn_borraitem.config(image=icono)
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)

        # Guardar movimiento en archivos
        icono = self.cargar_icono("guardar.png")
        self.btn_guardaritem = tk.Button(self.frame_cuarto, text="Guardar item", command=self.fguardar, width=24,
                                      bg="green", fg="white", compound="left")
        self.btn_guardaritem.image = icono
        self.btn_guardaritem.config(image=icono)
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)

        # Cancelar lo que se este haciendo
        icono = self.cargar_icono("cancelar.png")
        self.btn_Cancelar = tk.Button(self.frame_cuarto, text="Cancelar", command=self.fcancelar, width=24, bg="black",
                                   fg="white", compound="left")
        self.btn_Cancelar.image = icono
        self.btn_Cancelar.config(image=icono)
        self.btn_Cancelar.grid(row=0, column=4, padx=5, pady=2)

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_cuarto.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=tk.Button(self.frame_cuarto, text="Salir", image=self.photo3, width=65, command=self.fsalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

    def cuadro_grid_ctacte(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_ctacte)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_ctacte = ttk.Treeview(self.frame_tvw_ctacte, height=7, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5", "col6"))

        self.grid_ctacte.bind("<Double-Button-1>", self.doble_click_grid)

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

        self.grid_ctacte.tag_configure('oddrow', background='light grey')
        self.grid_ctacte.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_tvw_ctacte, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_tvw_ctacte, orient="vertical")
        self.grid_ctacte.config(xscrollcommand=scroll_x.set)
        self.grid_ctacte.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_ctacte.xview)
        scroll_y.config(command=self.grid_ctacte.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_ctacte['selectmode'] = 'browse'

        self.grid_ctacte.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # COMPACTAR MOVIMIENTOS
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def fcompactar(self):

        # ---------------------------------------------------------------------------
        # VALIDACIONES

        # verifico que existan movimientos cargados en el grid
        self.varFuncion_new.mover_puntero_topend(self.grid_ctacte, "TOP")
        self.selected = self.grid_ctacte.focus()
        if self.selected == "":
            messagebox.showwarning("Cuidado", "No existen movimientos o no selecciono cuenta", parent=self)
            return
        # Verifico que exista una cuenta cargada
        if self.sv_codigo_cliente.get() == "" or self.sv_codigo_cliente.get() == "0":
            messagebox.showwarning("Cuidado", "Seleccione una cuenta", parent=self)
            return
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # DEFINO PANTALLA FLOTANTE
        self.pantalla_estad = tk.Toplevel()
        self.pantalla_estad.geometry('630x390+660+380')
        self.pantalla_estad.transient(master=self.master)
        self.pantalla_estad.config(bg='light green', padx=5, pady=5)
        self.pantalla_estad.resizable(False, False)
        self.pantalla_estad.title("Compactar movimientos")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # TITULOS

        self.frame_titulo_compactar = tk.Frame(self.pantalla_estad, bg="light green")

        # Armo el logo y el titulo
        self.photo = Image.open('ctacte.png')
        self.photo = self.photo.resize((30, 30), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_cta = ImageTk.PhotoImage(self.photo)
        self.lbl_png_cta = tk.Label(self.frame_titulo_compactar, image=self.png_cta, bg="red", relief="ridge", bd=5)
        self.lbl_tit = tk.Label(self.frame_titulo_compactar, width=22, text="Compactar", bg="black", fg="gold",
                                font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_cta.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
        self.lbl_tit.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_compactar.pack(side="top", fill="x", padx=5, pady=2)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # VARIABLES STRINGVARS

        # Fechas inferior y tope de compactacion
        self.sv_fecha_inicial = tk.StringVar(value="")
        self.sv_fecha_ultima = tk.StringVar(value="")
        self.sv_fecha_tope_compactar = tk.StringVar(value="")

        # Debitos y creditos existentes todos
        self.sv_suma_debitos_ant = tk.StringVar(value="0")
        self.sv_suma_creditos_ant = tk.StringVar(value="0")

        # Saldo inicial luego de borrar los debitos y creditos comprendidos entre las fechas a compactar
        self.sv_nuevo_saldo_inicial = tk.StringVar(value="0")

        # sumas de debitos y creditos a eliminar y recalculo del saldo para control
        self.sv_suma_debitos_eliminar = tk.StringVar(value="0")
        self.sv_suma_creditos_eliminar = tk.StringVar(value="0")
        self.sv_saldo_despues_eliminar = tk.StringVar(value="0")
        # ---------------------------------------------------------------------------

        # guardo filtro activo
        filtro_anterior = self.filtro_activo

        # Obtengo primera y ultima fecha de los movimientos -------------------------
        primera_fecha = self.obtener_fecha_movimiento("TOP")
        ultima_fecha = self.obtener_fecha_movimiento("END")
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # CONVERSION DE LAS FECHAS A FORMATO NUESTRO - fecha de 2024-12-19 a 19/12/2024

        forma_normal_inicial = fecha_str_reves_normal(self, datetime.strftime(primera_fecha, '%Y-%m-%d'), False)
        # sumo 30 dias a la primera fecha
        fecha_inicial_mas30 = primera_fecha + timedelta(days=30)

        forma_normal_final = fecha_str_reves_normal(self, datetime.strftime(fecha_inicial_mas30, '%Y-%m-%d'), False)
        forma_normal_ultima = fecha_str_reves_normal(self, datetime.strftime(ultima_fecha, '%Y-%m-%d'), False)

        self.sv_fecha_inicial = tk.StringVar(value=forma_normal_inicial)
        self.sv_fecha_ultima = tk.StringVar(value=forma_normal_ultima)
        self.sv_fecha_tope_compactar = tk.StringVar(value=forma_normal_final)

        self.sv_suma_debitos_ant = tk.StringVar(value=str(self.suma_debitos))
        self.sv_suma_creditos_ant = tk.StringVar(value=str(self.suma_creditos))
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # TOTAL SALDOS DEBITOS CREDITOS
        self.frame_info_saldos = tk.LabelFrame(self.pantalla_estad, bg="light green")
        self.cuadro_saldos_estado_actual()
        self.frame_info_saldos.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # CUADRO DE INFORMACION SOBRE FECHAS
        self.frame_info_compactar = tk.LabelFrame(self.pantalla_estad, bg="light green")
        self.cuadro_informacion_fechas()
        self.frame_info_compactar.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # ENTRY HASTA QUE FECHA COMPACTAR MOVIMIENTOS
        self.frame_parametros_compactar = tk.LabelFrame(self.pantalla_estad, bg="light green")
        self.entrys_fecha_compactar()
        self.frame_parametros_compactar.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        # BOTON PREVISUALIZAR RESULTADOS PARA CONTROL
        self.frame_botones_previsual = tk.LabelFrame(self.pantalla_estad, bg="light green")
        self.botones_previsualizar()
        self.frame_botones_previsual.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        self.frame_previsualizar = tk.LabelFrame(self.pantalla_estad, bg="light green")
        self.frame_previsualizar.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        # ---------------------------------------------------------------------------
        # BOTONES Continuar Canccelar
        self.frame_botones_compactar = tk.LabelFrame(self.pantalla_estad, bg="light green")
        self.botones_compactar()
        self.frame_botones_compactar.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------

        # vuelvo filtro activo a estado anterior
        self.filtro_activo = filtro_anterior

        self.pantalla_estad.grab_set()
        self.pantalla_estad.focus_set()

        tk.mainloop()

    def obtener_fecha_movimiento(self, posicion):

        self.varFuncion_new.mover_puntero_topend(self.grid_ctacte, posicion)
        selected = self.grid_ctacte.focus()
        clave = self.grid_ctacte.item(selected, "text")
        datos = self.varCtacte.consultar_ctacte(
            f"ctacte WHERE id = {clave}"
        )
        return datos[0][1] if datos else ""

    def fprevisualizar(self):

        # Valida el rango de fechas
        if not self.validar_fecha(self.sv_fecha_tope_compactar.get(), self.sv_fecha_inicial.get(), self.sv_fecha_ultima.get()):
            messagebox.showerror("Error", "Parametros de fecha incorrectos, verifique", parent=self)
            self.entry_fecha_compactar.focus_set()
            return

        # Suma Debitos y creditos a eliminar ---------------------------------------------------

        # .......................................................................................
        # Suma los debitos y creditos entre las dos fechas solicitadas inclusive esas fechas ....
        # Seria la suma de debitos y creditos de los movimientos que se van a eliminar ----------
        # .......................................................................................

        """ Estas instrucciones SQL funcionaron bien
        #SELECT SUM(importe) AS total FROM ctacte WHERE fecha BETWEEN '2026-01-01' AND '2026-01-31'
        #SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte WHERE cc_fecha BETWEEN '2024-07-02' AND '2024-08-01' """

        # Debo mandar las fechas en formato "2026-05-12", tippo date
        fecha1 = self.sv_fecha_inicial.get()
        fecha_convertida1 = datetime.strptime(fecha1, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha2 = self.sv_fecha_tope_compactar.get()
        fecha_convertida2 = datetime.strptime(fecha2, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Consulta SQL
        self.filtro_activo = (f"SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte "
                              f"WHERE cc_fecha BETWEEN '{fecha_convertida1}' AND '{fecha_convertida2}' "
                              f"AND cc_codcli = '{self.sv_codigo_cliente.get()}'")

        # Retorna totales de debito y credito a eliminar como una Tupla en retorno
        retorno = self.varCtacte.sumar_compactar(self.filtro_activo)

        # Muestro suma de debitos y creditos, tambien el total de lo que sera el movimiento a ingresar como saldo inicial
        self.sv_suma_debitos_eliminar.set(value=retorno[0])
        self.sv_suma_creditos_eliminar.set(value=retorno[1])
        self.sv_nuevo_saldo_inicial.set(value=retorno[0] - retorno[1])

        # Calculo nuevo saldo de control ------------------------------------------------------
        # Calcular el nuevo saldo para control SIN tener en cuenta los movimientos a eliminar
        self.filtro_activo = (f"SELECT SUM(cc_ingreso-cc_egreso) AS nuevo_saldo FROM ctacte "
                              f"WHERE (cc_fecha < '{fecha_convertida1}' AND cc_codcli = '{self.sv_codigo_cliente.get()}') "
                              f"OR (cc_fecha > '{fecha_convertida2}' AND cc_codcli = '{self.sv_codigo_cliente.get()}')")

        # Vuelve el total del nuevo saldo calculado con los movimientos que quedarian + el nuevo saldo inicial OJO
        retorno = self.varCtacte.sumar_saldo_control(self.filtro_activo)

        # OJO sumarle el nuevo saldo inicial
        con_saldoini = float(retorno[0]) + float(self.sv_nuevo_saldo_inicial.get())

        self.sv_saldo_despues_eliminar.set(value=str(con_saldoini))

        # ---------------------------------------------------------------------------------
        # VISUALIZACION DE TOTALES DE CONTROL

        fff = tkfont.Font(family="Arial", size=10, weight="bold")

        for c in range(4):
            self.frame_previsualizar.grid_columnconfigure(c, weight=1, minsize=120)

        # Suma de los debitos a eliminar
        self.lbl_suma_debitos_eliminar_tit = tk.Label(self.frame_previsualizar, text="Suma debitos a eliminar: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_suma_debitos_eliminar_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_suma_debitos_eliminar_var = tk.Label(self.frame_previsualizar, textvariable=self.sv_suma_debitos_eliminar,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_suma_debitos_eliminar_var.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        # Suma de los creditos a eliminar
        self.lbl_suma_creditos_eliminar_tit = tk.Label(self.frame_previsualizar, text="Suma creditos a eliminar: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_suma_creditos_eliminar_tit.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_suma_creditos_eliminar_var = tk.Label(self.frame_previsualizar, textvariable=self.sv_suma_creditos_eliminar,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_suma_creditos_eliminar_var.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")

        # muestro el importe del movimiento que voy a generar como saldo inicial
        self.lbl_nuevo_saldo_inicial_tit = tk.Label(self.frame_previsualizar, text="Nuevo saldo inicial: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_inicial_tit.grid(row=1, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_nuevo_saldo_inicial_var = tk.Label(self.frame_previsualizar, textvariable=self.sv_nuevo_saldo_inicial,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_inicial_var.grid(row=1, column=1, padx=5, pady=3, sticky="nsew")

        # Saldo resultante de estos movimientos (debe coincidir con el anterior)
        self.lbl_nuevo_saldo_final_tit = tk.Label(self.frame_previsualizar, text="Saldo resultante: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_final_tit.grid(row=1, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_nuevo_saldo_final_var = tk.Label(self.frame_previsualizar, textvariable=self.sv_saldo_despues_eliminar,
                                                 font=fff, bg="light green", bd=5, justify="center")
        self.lbl_nuevo_saldo_final_var.grid(row=1, column=3, padx=5, pady=3, sticky="nsew")

        for widg in self.frame_previsualizar.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

        if float(self.sv_saldo_cliente.get()) != float(self.sv_saldo_despues_eliminar.get()):
            messagebox.showerror("Error", "No coinciden los saldos finales, verifique", parent=self)
            self.entry_fecha_compactar.focus_set()
            return

    def botones_previsualizar(self):

        self.btn_previsualizar = tk.Button(self.frame_botones_previsual, text=" Previsualizacion",
                                             command=self.fprevisualizar, width=50, bg="black", fg="white",
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

        icono = self.cargar_icono("ejecucion.png")
        self.btn_cancelar_compactar = tk.Button(self.frame_botones_compactar, text=" Continuar",
                                             command=self.fejecutar_compactar, width=24, bg="black", fg="white",
                                             compound="left")
        self.btn_cancelar_compactar.image = icono
        self.btn_cancelar_compactar.config(image=icono)
        self.btn_cancelar_compactar.grid(row=0, column=0, padx=5, pady=3)

        icono = self.cargar_icono("cancelar.png")
        self.btn_cancelar_compactar = tk.Button(self.frame_botones_compactar, text=" Salir", command=self.fsalir_compactar,
                                                width=24, bg="black", fg="white", compound="left")
        self.btn_cancelar_compactar.image = icono
        self.btn_cancelar_compactar.config(image=icono)
        self.btn_cancelar_compactar.grid(row=0, column=1, padx=5, pady=3)
        # ---------------------------------------------------------------------------

        # reordenamiento de self.frame_botones_grid
        for widg in self.frame_botones_compactar.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    @staticmethod
    def validar_fecha(fecha_tope, fecha_inicial, fecha_ultima):

        # las paso a formato date
        f1 = datetime.strptime(fecha_tope, "%d/%m/%Y")
        f2 = datetime.strptime(fecha_inicial, "%d/%m/%Y")

        # Si la fecha tope(hasta donde voy a compactar inclusive) < Fecha inicial (fecha minima de los movimientos)
        if f1 < f2:
            return "false"

        # las paso a formato date
        f1 = datetime.strptime(fecha_tope, "%d/%m/%Y")
        f2 = datetime.strptime(fecha_ultima, "%d/%m/%Y")

        # Si la fecha tope(hasta donde voy a compactar inclusive) >= Fecha del ultimo movimiento que registra la cuenta
        if f1 >= f2:
            return "false"
        return True

    def entrys_fecha_compactar(self):

        # Muestra los parametros de fechas para el intervalo a compactar
        fff = tkfont.Font(family="Arial", size=10, weight="bold")

        # Desde que fecha compacto - Por defecto es desde la mas vieja
        self.lbl_fecha_inicial_tit = tk.Label(self.frame_parametros_compactar, text="Compactar: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_fecha_inicial_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_inicial_tit = tk.Label(self.frame_parametros_compactar, text="Desde : Fecha inicial: ", font=fff,
                                           bg="light green", bd=5, justify="center")
        self.lbl_fecha_inicial_tit.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_inicial_var = tk.Label(self.frame_parametros_compactar, textvariable=self.sv_fecha_inicial,
                                           bg="light green", bd=5)
        self.lbl_fecha_inicial_var.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")

        # Hasta que fecha compacto - Fecha a elegirse (control sobre esta fecha que no supere algunos parametros)
        # Por defecto le sumamos 30 dias
        self.lbl_fecha_final = tk.Label(self.frame_parametros_compactar, text="Hasta: Fecha final: ", font=fff,
                                     bg="light green", bd=5, justify="center")
        self.lbl_fecha_final.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")
        self.entry_fecha_compactar = tk.Entry(self.frame_parametros_compactar, textvariable=self.sv_fecha_tope_compactar,
                                      bd=5, width=10, justify="right")
        self.entry_fecha_compactar.bind("<FocusOut>", self.formato_fecha_compactar)
        self.entry_fecha_compactar.grid(row=0, column=4, padx=5, pady=3, sticky="nsew")

        for widg in self.frame_parametros_compactar.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_informacion_fechas(self):

        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        # Fecha mas baja de los movimientos actuales
        self.lbl_fecha_primer_movimiento_tit = tk.Label(self.frame_info_compactar, text="Fecha primer movimiento: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_fecha_primer_movimiento_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_primer_movimiento_var = tk.Label(self.frame_info_compactar, textvariable=self.sv_fecha_inicial,
                                                     bg="light green", bd=5)
        self.lbl_fecha_primer_movimiento_var.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        # Fecha mas alta de los movimientos actuales
        self.lbl_fecha_ultimo_movimiento_tit = tk.Label(self.frame_info_compactar, text="Fecha ultimo movimiento: ", font=fff,
                                                     bg="light green", bd=5, justify="center")
        self.lbl_fecha_ultimo_movimiento_tit.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_fecha_ultimo_movimiento_var = tk.Label(self.frame_info_compactar, textvariable=self.sv_fecha_ultima,
                                                     bg="light green", bd=5)
        self.lbl_fecha_ultimo_movimiento_var.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")

    def cuadro_saldos_estado_actual(self):

        fff = tkfont.Font(family="Arial", size=10, weight="bold")
        # El saldo actual
        self.lbl_saldo_tit = tk.Label(self.frame_info_saldos, text="Saldo a la fecha: ", font=fff, bg="light green",
                                      bd=5, justify="center")
        self.lbl_saldo_tit.grid(row=0, column=0, padx=5, pady=3, sticky="nsew")
        self.lbl_saldo_var = tk.Label(self.frame_info_saldos, textvariable=self.sv_saldo_cliente, bg="light green", bd=5)
        self.lbl_saldo_var.grid(row=0, column=1, padx=5, pady=3, sticky="nsew")

        # Suma de los debitos antes de compactacion (todos)
        self.lbl_debitos_tit = tk.Label(self.frame_info_saldos, text="Debitos: ", font=fff, bg="light green", bd=5,
                                        justify="center")
        self.lbl_debitos_tit.grid(row=0, column=2, padx=5, pady=3, sticky="nsew")
        self.lbl_debitos_var = tk.Label(self.frame_info_saldos, textvariable=self.sv_suma_debitos_ant, bg="light green", bd=5)
        self.lbl_debitos_var.grid(row=0, column=3, padx=5, pady=3, sticky="nsew")

        # Suma de los creditos antes de compactacion (todos)
        self.lbl_creditos_tit = tk.Label(self.frame_info_saldos, text="Creditos: ", font=fff, bg="light green", bd=5,
                                         justify="center")
        self.lbl_creditos_tit.grid(row=0, column=4, padx=5, pady=3, sticky="nsew")
        self.lbl_creditos_var = tk.Label(self.frame_info_saldos, textvariable=self.sv_suma_creditos_ant,
                                         bg="light green", bd=5)
        self.lbl_creditos_var.grid(row=0, column=5, padx=5, pady=3, sticky="nsew")

    def fejecutar_compactar(self):

        confirma = messagebox.askquestion("Confirmar",
                                          "Confirma continuar con ajuste de movimientos de la cuenta?? " + self.sv_nombre_cliente.get(),
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
        fecha1 = self.sv_fecha_inicial.get()
        fecha_convertida1 = datetime.strptime(fecha1, "%d/%m/%Y").strftime("%Y-%m-%d")
        fecha2 = self.sv_fecha_tope_compactar.get()
        fecha_convertida2 = datetime.strptime(fecha2, "%d/%m/%Y").strftime("%Y-%m-%d")

        self.filtro_activo = (f"SELECT SUM(cc_ingreso) AS total_ing, SUM(cc_egreso) AS total_egr FROM ctacte "
                              f"WHERE cc_fecha BETWEEN '{fecha_convertida1}' AND '{fecha_convertida2}' "
                              f"AND cc_codcli = '{self.sv_codigo_cliente.get()}'")

        # vuelven los totales de debito y los de credito a eliminar como una tupla en retorno
        retorno = self.varCtacte.sumar_compactar(self.filtro_activo)

        # nuevo saldo inicial
        self.sv_nuevo_saldo_inicial.set(value=retorno[0] - retorno[1])
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        # CARGO VARIABLES PARA INGRESAR A LA TABLA

        # Cargo las variables para mandar el registro con el nuevo saldo inicial con la fecha inferior
        self.sv_clavemov.set(value="0")
        self.sv_detalle_movim.set(value="Saldo de compactacion")
        self.sv_debito_movim.set(value="0")
        self.sv_credito_movim.set(value="0")
        if float(self.sv_nuevo_saldo_inicial.get()) < 0:
            self.sv_credito_movim.set(value=str((self.sv_nuevo_saldo_inicial.get()))*-1)
        if float(self.sv_nuevo_saldo_inicial.get()) > 0:
            self.sv_debito_movim.set(value=str(self.sv_nuevo_saldo_inicial.get()))

        # EL resto de los campos ya estan cargados
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # MENSAJES

        # Mensajes mientras procesamos
        self.varFuncion_new.mostrar_toast(
            self.pantalla_estad,
            "🧹 Iniciando borrado de registros...",
            "green",
            2500,
            ""
        )

        # --- proceso real ---
        self.pantalla_estad.after(
            3000,
            lambda: self.varFuncion_new.mostrar_toast(
                self.pantalla_estad,
                "✅ Proceso finalizado",
                "green",
                2500,
                ""
            )
        )
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # BORRAR MOVIMIENTOS DE COMPACTACION
        # ....................................................................................................
        # Primero elimino los movimientos antes de dar alta al nuevo saldo inicial, si lo hago despues       .
        # tambien me lo borraria.                                                                            .
        # ....................................................................................................
        self.filtro_activo= (f"DELETE FROM ctacte WHERE cc_fecha >= '{fecha_convertida1}' AND "
                             f"cc_fecha <= '{fecha_convertida2}' AND cc_codcli = '{self.sv_codigo_cliente.get()}'")
        # metodo de borrado de los movimientos seleccionados entre fechas
        self.varCtacte.borrar_compactar(self.filtro_activo)
        #retorno = self.varCtacte.borrar_compactar(self.filtro_activo)
        # -----------------------------------------------------------------------

        # -----------------------------------------------------------------------
        # INGRESAR EL MOVIMIENTO CON EL NUEVO SALDO INICIAL
        # Ingreso el movimiento del nuevo saldo inicial
        fecha_aux = datetime.strptime(self.sv_fecha_tope_compactar.get(), '%d/%m/%Y')
        dic_ctacte = self.get_ctacte_dic(fecha_aux)    # funcion que genera el diccionario
        self.varCtacte.insertar_ctacte(dic_ctacte)

        # NO DEBERIA IR LLENA_GRILLA??????????

    def fsalir_compactar(self):
        self.pantalla_estad.destroy()

    def get_ctacte_dic(self, fecha_aux):
        return {
            "Id": self.clave,
            "cc_fecha": fecha_aux,
            "cc_detalle": self.sv_detalle_movim.get(),
            "cc_ingreso": self.sv_debito_movim.get(),
            "cc_egreso": self.sv_credito_movim.get(),
            "cc_codcli": self.sv_codigo_cliente.get(),
            "cc_nomcli": self.sv_nombre_cliente.get(),
            "cc_clavemov": self.sv_clavemov.get()
        }

    @staticmethod
    def cargar_icono(path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)

    # -------------------------------------------------------
    # INFORMES
    # -------------------------------------------------------

    def fimprime(self):

        # ---------------------------------------------------------------------------
        # VALIDACIONES

        # verifico que existan movimientos vargador en el grid
        self.varFuncion_new.mover_puntero_topend(self.grid_ctacte,"TOP")
        self.selected = self.grid_ctacte.focus()
        if self.selected == "":
            messagebox.showwarning("Cuidado", "No existen movimientos o no selecciono cuenta", parent=self)
            return
        # Verifico que exista una cuenta cargada
        if self.sv_codigo_cliente.get() == "" or self.sv_codigo_cliente.get() == "0":
            messagebox.showwarning("Cuidado", "Seleccione una cuenta", parent=self)
            return
        # ---------------------------------------------------------------------------

        # Debo filtrar el cliente seleccionado
        adad = self.sv_codigo_cliente.get()
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



        """
        #........................................................................
        # ejempos de mensajes para metodo toast                                 .
        # self.mostrar_toast("✅ Borrado correcto", 2500, "success")            .
        # self.mostrar_toast("❌ Error al borrar", 4000, "error")               .
        # self.mostrar_toast("🧹 Iniciando borrado...", 2000, "info")           .
        #........................................................................
        """

        """
        🔥 CÓMO USAR SET_STATUS
        ✔ Guardar
        self.set_status("✔ Registro guardado correctamente", "ok")
        🗑 Eliminar
        self.set_status("🗑 Cliente eliminado", "ok")
        ⚠ Validación
        self.set_status("⚠ CUIT incorrecto", "warn")
        ❌ Error
        self.set_status("❌ Error al guardar", "error")
        ℹInfo
        self.set_status("ℹ Buscando clientes...", "info")
        """
