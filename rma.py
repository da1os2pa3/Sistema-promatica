import os
import tkinter as tk
from datetime import date
from tkinter import ttk

from PIL import Image, ImageTk

from PDF_clase import *
from funcion_new import ClaseFuncionNew
from funciones import *
from rma_ABM import DatosRma
from status_bar import StatusBar


class ClaseRma(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.status = StatusBar(self.master)

        # ------------------------------------------------------------------
        # Seteo pantalla master principal
        self.master.grab_set()
        self.master.focus_set()
        # ------------------------------------------------------------------

        #-------------------------------------------------------------------
        # Instanciaciones
        self.varRma = DatosRma(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
        #-------------------------------------------------------------------

        # --------------------------------------------------------------------
        # PANTALLA
        # --------------------------------------------------------------------
        self.master.resizable(0, 0)
        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """
        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()
        # Asigno fijo un ancho y un alto
        ancho_ventana = 1035
        alto_ventana = 530
        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        Otras funciones para manejar los elementos seleccionados incluyen:
        selection_add(): añade elementos a la selección.
        selection_remove(): remueve elementos de la selección.
        selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        selection_toggle(): cambia la selección de un elemento. """

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------

    def create_widgets(self):

        # ------------------------------------------------------------------
        # Titulos 
        # ------------------------------------------------------------------
        # Encabezado logo y titulo
        self.frame_titulo_top = tk.Frame(self.master)
        # Armo el logo y el titulo
        self.photo3 = Image.open('rma.png')
        self.photo3 = self.photo3.resize((60, 60), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_rma = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_rma = tk.Label(self.frame_titulo_top, image=self.png_rma, bg="red", relief="ridge", bd=5)
        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=49, text="Pendientes", bg="black", fg="gold",
                                                       font=("Arial bold", 22, "bold"), bd=5, relief="ridge", padx=5)
        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_rma.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # VARIABLES GENERALES
        # ------------------------------------------------------------------
        #vcmd = (self.register(self.varFuncion_new.validar), '%P')
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # STRINGVARS
        # ------------------------------------------------------------------
        una_fecha= date.today()
        self.sv_fecha = tk.StringVar(value=una_fecha.strftime('%d/%m/%Y'))
        self.sv_proveedor = tk.StringVar(value="")
        self.sv_articulo = tk.StringVar(value="")
        self.sv_cliente = tk.StringVar(value="")
        self.sv_problema = tk.StringVar(value="")
        self.sv_costo_venta = tk.StringVar(value="0.00")
        self.sv_estado = tk.StringVar(value="")
        self.sv_observaciones = tk.StringVar(value="")
        self.sv_buscostring = tk.StringVar(value="")
        self.sv_combo_estado = tk.StringVar(value="")
        self.sv_combo_proceso = tk.StringVar(value="")
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # CUADROS
        # ------------------------------------------------------------------
        self.frame_rma = tk.LabelFrame(self.master, text="RMA", foreground="#CD5C5C")

        # Botones del GRid
        self.frame_cuadro_botones_grid = tk.LabelFrame(self.frame_rma, text="", foreground="#CD5C5C")
        self.botones_grid()
        self.frame_cuadro_botones_grid.pack(side="left", fill="both", padx=5, pady=2)
        # Construccion del Grid
        self.frame_cuadro_constructor_grid = tk.LabelFrame(self.frame_rma, text="", foreground="#CD5C5C")
        self.constructor_grid()
        self.frame_cuadro_constructor_grid.pack(side="top", fill="both", padx=5, pady=2)
        # Busquedas en el Grid
        self.frame_busqueda_grid = tk.LabelFrame(self.frame_rma, text="", border=5, foreground="black", background="light blue")
        self.busqueda_grid()
        self.frame_busqueda_grid.pack(expand=0, side="top", fill="both", padx=5, pady=2)

        self.frame_rma.pack(side="top", fill="both", padx=5, pady=2)

        # ------------------------------------------------------------------
        # ENTRYS
        self.frame_cuadro_entrys_datos = tk.LabelFrame(self.master, text="", foreground="black")
        self.entrys_datos()
        self.frame_cuadro_entrys_datos.pack(side="top", fill="both", expand=0, padx=5, pady=5)
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # BOTONES finales de guardar
        self.frame_cuadro_botones_guardar = tk.LabelFrame(self.master)
        self.botones_guardar()
        self.frame_cuadro_botones_guardar.pack(expand=0, side="top", fill="both", pady=2, padx=5)


    # ------------------------------------------------------------------
    # ESTADOS
    # ------------------------------------------------------------------

    def estado_inicial(self):

        default = 'Pendiente'
        self.filtro_activo =  "rma WHERE rm_estado = '" + default + "' ORDER BY rm_fecha ASC"
        self.alta_modif = 0
        una_fecha = date.today()
        self.sv_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.limpiar_entrys()
        self.estado_entrys("disabled")
        self.estado_botones_dos("disabled")
        self.estado_botones_uno("normal")

    def limpiar_entrys(self):

        una_fecha = date.today()
        self.sv_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.sv_articulo.set(value="")
        self.sv_proveedor.set(value="")
        self.sv_problema.set(value="")
        self.sv_cliente.set(value="")
        self.sv_costo_venta.set(value="")
        self.sv_observaciones.set(value="")
        self.combo_proceso.current(0)
        self.combo_estado.current(0)
        self.sv_buscostring.set(value="")

    def estado_entrys(self, estado):

        self.entry_fecha.configure(state=estado)
        self.entry_articulo.configure(state=estado)
        self.entry_proved.configure(state=estado)
        self.entry_problema.configure(state=estado)
        self.entry_cliente.configure(state=estado)
        self.entry_costo_venta.configure(state=estado)
        self.entry_observa.configure(state=estado)
        self.combo_proceso.configure(state=estado)
        self.combo_estado.configure(state=estado)
        self.entry_busqueda_rma.configure(state=estado)

    def estado_botones_uno(self, estado):

        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)
        self.btn_nuevo_rma.configure(state=estado)
        self.btn_edito_rma.configure(state=estado)
        self.btn_borro_rma.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_buscar.configure(state=estado)
        self.entry_busqueda_rma.configure(state=estado)

    def estado_botones_dos(self, estado):
        self.btn_guardar.configure(state=estado)

    # ------------------------------------------------------------------
    # GRID
    # ------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_rma.get_children():
            self.grid_rma.delete(item)

        datos = self.varRma.consultar_rma(self.filtro_activo)

        for row in datos:
            self.grid_rma.insert("", "end", text=row[0], values=(row[1], row[2], row[3], row[4], row[5],
                                                                 row[6], row[7], row[8], row[9]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_rma.get_children()
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
            self.grid_rma.focus_set()
            self.grid_rma.focus(posicion)
            self.grid_rma.selection_set(posicion)
            self.grid_rma.see(posicion)
        else:
            for item in children:
                texto = self.grid_rma.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_rma.update_idletasks()
                    self.grid_rma.focus_set()
                    self.grid_rma.selection_set(item)
                    self.grid_rma.focus(item)
                    self.grid_rma.see(item)
                    break

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def doble_click_grid(self, _event):
        self.fedito_rma()

    def fnuevo_rma(self):
        self.alta_modif = 1
        self.estado_entrys("normal")
        self.estado_botones_dos("normal")
        self.estado_botones_uno("disabled")
        self.entry_fecha.focus()

    def fedito_rma(self):

        self.selected = self.grid_rma.focus()
        self.clave = self.grid_rma.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.estado_entrys("normal")
        self.estado_botones_dos("normal")
        self.estado_botones_uno("disabled")
        self.entry_articulo.focus()

        #self.var_Id = self.clave  #puede traer -1 , en ese caso seria un alta
        self.alta_modif = 2

        # En la lista valores cargo todos los registros completos con todos los campos
        valores = self.grid_rma.item(self.selected, 'values')

        una_fecha = datetime.strptime(valores[0], '%Y-%m-%d')
        self.sv_fecha.set(value=una_fecha.strftime('%d/%m/%Y'))
        self.sv_articulo.set(value=valores[1])
        self.sv_combo_proceso.set(value=valores[2])
        self.sv_combo_estado.set(value=valores[3])
        self.sv_proveedor.set(value=valores[4])
        self.sv_cliente.set(value=valores[5])
        self.sv_problema.set(value=valores[6])
        self.sv_costo_venta.set(value=valores[7])
        self.sv_observaciones.set(value=valores[8])

    def fborro_rma(self):

        # ---------------------------------------------------------------------
        # selecciono el Id del Tv grid para su uso posterior
        self.selected = self.grid_rma.focus()
        self.selected_ant = self.grid_rma.prev(self.selected)
        # guardo en clave el Id pero de la tabla (no son el mismo con el treeview)
        self.clave = self.grid_rma.item(self.selected, 'text')
        self.clave_ant = self.grid_rma.item(self.selected_ant, 'text')
        # ---------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Eliminar", "No hay nada seleccionado", parent=self)
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_rma.item(self.selected, 'values')
        data = str(self.clave)+" "+valores[1]
        r = messagebox.askquestion("Eliminar", "Confirma eliminar registro?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        # Metodo que ellimina el registro ------------------------------
        self.varRma.eliminar_rma(self.clave)
        # --------------------------------------------------------------
        self.status.set_status("🗑 Registro eliminado", "ok")
        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # 1- que articulo no este vacio
        if len(self.sv_articulo.get()) == 0:
            messagebox.showerror("Error", "Falta descripcion de articulo", parent=self)
            self.entry_articulo.focus()
            return

        # Asi obtengo el Id del Grid (Treeview) de donde esta el foco (I006...I002...) ------------------
        self.selected = self.grid_rma.focus()
        # Asi obtengo la clave de la tabla (campo Id de la tabla - numero secuencial) que no es lo mismo que el del Treeview
        self.clave = self.grid_rma.item(self.selected, 'text')
        # -----------------------------------------------------------------------------------------------

        # DICCIONARIO --------------------------------------------
        # Preparo la fecha y pongo en la variable "dic_rma" el diccionario completo con todos
        # los datos a ingresar a la tabla
        fecha_aux = datetime.strptime(self.sv_fecha.get(), '%d/%m/%Y')
        dic_rma = self.get_rma_dic(fecha_aux)    # funcion que genera el diccionario
        # ---------------------------------------------------------

        id_ref = ""
        try:
            if self.alta_modif == 1:
                id_ref = self.varRma.insertar_registro(dic_rma)
            elif self.alta_modif == 2:
                self.varRma.modificar_registro(dic_rma)
                id_ref = self.clave
        except ValueError as e:
            messagebox.showwarning("Datos inválidos en Insertar/Modificar", str(e))
            return
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        self.llena_grilla(id_ref)

        self.estado_botones_uno("normal")
        self.estado_botones_dos("disabled")
        self.alta_modif = 0
        self.limpiar_entrys()
        self.estado_entrys("disabled")

#NO ME HABILITA EL BOTON BUSQUEDA


    # ------------------------------------------------------------------
    # BOTONES
    # ------------------------------------------------------------------

    def fsalir(self):
        r = messagebox.askquestion("Salir", "Confirma Salida?", parent=self)
        if r == messagebox.NO:
            return
        self.master.destroy()

    def fcancelar(self):
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return
        self.limpiar_entrys()
        self.estado_inicial()


    # ------------------------------------------------------------------
    # PUNTEROS
    # ------------------------------------------------------------------

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_rma, "TOP")

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_rma, "END")

    def fshowall(self):
        self.selected = self.grid_rma.focus()
        self.clave = self.grid_rma.item(self.selected, 'text')
        self.filtro_activo = "rma ORDER BY rm_fecha"
        self.llena_grilla(self.clave)


    # ------------------------------------------------------------------
    # BUSQUEDAS
    # ------------------------------------------------------------------

    def fpendientes(self):
        default = 'Pendiente'
        self.filtro_activo =  "rma WHERE rm_estado = '" + default + "' ORDER BY rm_fecha ASC"
        self.llena_grilla("")

    def fbuscar_rma(self):

        if len(self.sv_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)

        se_busca = self.sv_buscostring.get()
        self.filtro_activo = "rma WHERE INSTR(rm_articulo, '" + se_busca + "') ORDER BY rm_fecha ASC"

        self.varRma.buscar_entabla(self.filtro_activo)
        self.llena_grilla("")

        """ Obtengo el Id del grid para que me tome la seleccion y el foco se coloque efectivamente en el 
        item buscado y asi cuando le doy -show all- el puntero se sigue quedando en el registro buscado"""
        item = self.grid_rma.selection()
        self.grid_rma.focus(item)


    # ------------------------------------------------------------------
    # VALIDACIONES
    # ------------------------------------------------------------------

    def formato_fecha(self, pollo):

        # Ejecuto funcion validar_fecha en funcion_new
        retorno_validacion = self.varFuncion_new.validar_fecha(self.sv_fecha, self.entry_fecha)

        una_fecha = date.today()

        match retorno_validacion:

            case "break":
                self.entry_fecha.focus()
                return
            case "S":
                self.entry_fecha.focus()
            case "N" | "BLANCO":
                pass
            case "":
                self.sv_fecha.set(una_fecha.strftime('%d/%m/%Y'))
                self.entry_fecha.focus()
            case _:
                return


    # ------------------------------------------------------------------
    # INFORMES
    # ------------------------------------------------------------------

    def creopdf(self):

        # traigo el registro que quiero imprimir
        self.selected = self.grid_rma.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_rma.item(self.selected, 'text')

        # if self.clave == "":
        #     messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
        #     return

        # ==================================================================================
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
        # ==================================================================================

        # Cargo la linea del treeview de resu_presu ---------------------------------------
        # valores = self.grid_rma.item(self.selected, 'values')

        # armado de encabezado ------------------------------------------------------------
        sdf = date.today()          #,todatetime.strptime(valores[1], '%Y-%m-%d')
        feac = sdf.strftime('%d-%m-%Y')
        self.titulo = "RMA Estados"
        # self.pdf_numero_presupuesto = valores[0]
        # self.pdf_nombre_cliente = valores[2]
        # self.pdf_dolar_presupuesto = valores[3]
        # self.pdf_tasa_ganancia = valores[4]

        self.pdf_datos_encabezado = feac+' '+self.titulo
        # Imprimo el encabezado de pagina
        pdf.set_font('Arial', '', 8)
        # pdf.cell(w=0, h=5, txt='Presupuesto ', border=1, align='C', fill=0, ln=1)
        # pdf.cell(w=0, h=2, txt='', align='L', fill=0, ln=1)
        pdf.cell(w=0, h=5, txt=self.pdf_datos_encabezado, border=1, align='C', fill=0, ln=1)

        # Espaciado entre cuerpos -----------------------------------------------
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        # encabezados - columnas ------------------------------------------------
        pdf.cell(w=20, h=5, txt="Fecha", border=1, align='C', fill=0, ln=0)
        pdf.cell(w=150, h=5, txt="Articulo", border=1, align='L', fill=0, ln=0)
        pdf.cell(w=20, h=5, txt="Estado", border=1, align='R', fill=0, ln=0)
        pdf.cell(w=0, h=5, txt="", border=0, align='L', fill=0, ln=1)

        # Traer todos los registros de la tabla deta_presup ---------------------
        self.items = self.varRma.consultar_rma(self.filtro_activo)

        # impresion del cuerpo del informe --------------------------------------
        pdf.set_font('Arial', '', 8)
        for row in self.items:

            fecha_conver = datetime.strftime(row[1], '%d-%m-%Y')
            pdf.cell(w=20, h=5, txt=fecha_conver, border=0, align='R', fill=0, ln=0)
            pdf.cell(w=150, h=5, txt=row[2], border=0, align='L', fill=0, ln=0)
            pdf.cell(w=20, h=5, txt=row[3], border=0, align='R', fill=0, ln=1)
            pdf.cell(w=150, h=5, txt="Proveedor: (" + row[4] + ") - Falla: (" + row[5] + ")", border=0, align='L', fill=0, ln=1)
            pdf.cell(w=150, h=5, txt="Observaciones: (" + row[6] + ")", border=0, align='L', fill=0, ln=1)

        #   # pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
        #   # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(neto_dolar_pesos, 2))), border=0, align='R', fill=0, ln=0)
        #   # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
        #     pdf.multi_cell(w=0, h=5, txt=str(row[3]), border=0, align='L', fill=0)
        #   # pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)

        # pdf.cell(w=20, h=5, txt="Neto Dolar", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Bruto pesos", border=1, align='R', fill=0, ln=0)
        # pdf.cell(w=20, h=5, txt="Final", border=1, align='R', fill=0, ln=0)
        # pdf.multi_cell(w=0, h=5, txt="Estado", border=1, align='L', fill=0)

        # fecha_conver = fecha_str_reves_normal(self, valores[0])
        # pdf.cell(w=20, h=5, txt=fecha_conver, border=0, align='R', fill=0, ln=0)
        # pdf.cell(w=140, h=5, txt=valores[1], border=0, align='L', fill=0, ln=0)
        # pdf.cell(w=30, h=5, txt=valores[2], border=0, align='R', fill=0, ln=0)
        # pdf.cell(w=0, h=5, txt="", border=0, align='R', fill=0, ln=1)
        #
        # pdf.cell(w=50, h=5, txt="Proveedor: " + valores[3], border=0, align='L', fill=0, ln=1)
        # pdf.cell(w=50, h=5, txt="Fallo: " + valores[4], border=0, align='L', fill=0, ln=1)
        # pdf.cell(w=50, h=5, txt="Observaciones: " + valores[5], border=0, align='L', fill=0, ln=1)

        # # pdf.cell(w=20, h=5, txt=str(row[7]), border=0, align='R', fill=0, ln=0)
        # # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(neto_dolar_pesos, 2))), border=0, align='R', fill=0, ln=0)
        # # pdf.cell(w=20, h=5, txt=str(formatear_cifra(round(sumo_precio_final_conganancia, 2))), border=0, align='R', fill=0)
        # pdf.multi_cell(w=0, h=5, txt=str(row[3]), border=0, align='L', fill=0)


        # Espaciado -----------------------------------------------------------------------
#         pdf.cell(w=0, h=20, txt='', align='L', fill=0, ln=1)

        pdf.output('hoja.pdf')

        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)

    # -----------------------------------------------------------------------
    # CUADROS Y CONSTRUCCTORES
    # -----------------------------------------------------------------------

    def constructor_grid(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_cuadro_constructor_grid)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")
        self.grid_rma = ttk.Treeview(self.frame_cuadro_constructor_grid, height=4, columns=("col1", "col2", "col3",
                                                            "col4", "col5", "col6", "col7", "col8", "col9"))

        self.grid_rma.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_rma.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_rma.column("col1", width=60, anchor="w", minwidth=60)
        self.grid_rma.column("col2", width=180, anchor="w", minwidth=150)
        self.grid_rma.column("col3", width=40, anchor="center", minwidth=40)
        self.grid_rma.column("col4", width=40, anchor="center", minwidth=40)
        self.grid_rma.column("col5", width=40, anchor="center", minwidth=40)
        self.grid_rma.column("col6", width=40, anchor="center", minwidth=40)
        self.grid_rma.column("col7", width=40, anchor="center", minwidth=40)
        self.grid_rma.column("col8", width=40, anchor="center", minwidth=40)
        self.grid_rma.column("col9", width=40, anchor="center", minwidth=40)

        self.grid_rma.heading("#0", text="Id", anchor="center")
        self.grid_rma.heading("col1", text="Fecha", anchor="w")
        self.grid_rma.heading("col2", text="Articulo", anchor="w")
        self.grid_rma.heading("col3", text="Proceso", anchor="center")
        self.grid_rma.heading("col4", text="Estado", anchor="center")
        self.grid_rma.heading("col5", text="Proveedor", anchor="center")
        self.grid_rma.heading("col6", text="Cliente", anchor="center")
        self.grid_rma.heading("col7", text="Falla/motivo", anchor="center")
        self.grid_rma.heading("col8", text="Costo/Venta", anchor="center")
        self.grid_rma.heading("col9", text="Observaciones", anchor="center")

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_cuadro_constructor_grid, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_cuadro_constructor_grid, orient="vertical")
        self.grid_rma.config(xscrollcommand=scroll_x.set)
        self.grid_rma.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_rma.xview)
        scroll_y.config(command=self.grid_rma.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_rma['selectmode'] = 'browse'
        self.grid_rma.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def botones_grid(self):

        # Botones CRUD
        self.btn_nuevo_rma=tk.Button(self.frame_cuadro_botones_grid, text="Nuevo Movimiento", command=self.fnuevo_rma, width=17,
                                  bg='blue', fg='white')
        self.btn_nuevo_rma.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.btn_edito_rma=tk.Button(self.frame_cuadro_botones_grid, text="Editar Movimiento", command=self.fedito_rma, width=17,
                                  bg='blue', fg='white')
        self.btn_edito_rma.grid(row=1, column=0, padx=3, pady=3, sticky="w")
        self.btn_borro_rma=tk.Button(self.frame_cuadro_botones_grid, text="Borrar Movimiento", command=self.fborro_rma, width=17,
                                  bg='red', fg='white')
        self.btn_borro_rma.grid(row=2, column=0, padx=3, pady=3, sticky="w")

        # botones para ir al tope y al fin del archivo
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_cuadro_botones_grid, text="", image=self.photo4, command=self.ftoparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=3, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnToparch, msg="Ir a principio de archivo")
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_cuadro_botones_grid, text="", image=self.photo5, command=self.ffinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=4, column=0, padx=5, sticky="nsew", pady=3)
        # ToolTip(self.btnFinarch, msg="Ir al final del archivo")

    def busqueda_grid(self):
        # Buscar un articulo en Grid

        self.lbl_busqueda_rma = tk.Label(self.frame_busqueda_grid, text="Texto a buscar: ", justify="left", bg="light blue")
        self.lbl_busqueda_rma.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_busqueda_rma = tk.Entry(self.frame_busqueda_grid, textvariable=self.sv_buscostring,
                                                  state='normal', width=36, justify="left", bg="light blue")
        self.entry_busqueda_rma.grid(row=0, column=1, padx=5, pady=2, sticky='nsew')

        self.btn_buscar=tk.Button(self.frame_busqueda_grid, text="Buscar", command=self.fbuscar_rma, width=16, bg='#5F9EA0',
                               fg='white')
        self.btn_buscar.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        # Otros botones -----------------------
        self.btn_Pendientes=tk.Button(self.frame_busqueda_grid, text="Pendientes", command=self.fpendientes, width=16,
                                   bg='#5F9EA0', fg='white')
        self.btn_Pendientes.grid(row=0, column=3, padx=5, pady=2, sticky="w")
        self.btn_showall=tk.Button(self.frame_busqueda_grid, text="Mostrar todo", command=self.fshowall, width=16,
                                bg='#5F9EA0', fg='white')
        self.btn_showall.grid(row=0, column=4, padx=5, pady=2, sticky="w")
        self.btn_imprime_presup=tk.Button(self.frame_busqueda_grid, text="Imprimir", command=self.creopdf, width=16,
                                       bg='#5F9EF5', fg='white')
        self.btn_imprime_presup.grid(row=0, column=5, padx=2, pady=2, sticky="w")

    def entrys_datos(self):
        
        # Fecha de Anotacion
        self.lbl_fecha = tk.Label(self.frame_cuadro_entrys_datos, text="Fecha: ", justify="left")
        self.lbl_fecha.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.entry_fecha = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_fecha, width=10)
        self.entry_fecha.grid(row=0, column=1, padx=3, pady=3, sticky="e")
        self.entry_fecha.bind("<FocusOut>", self.formato_fecha)

        # Entry proveedor
        self.lbl_proved = tk.Label(self.frame_cuadro_entrys_datos, text="Proveedor: ", justify="left")
        self.lbl_proved.grid(row=0, column=2, padx=3, pady=3, sticky="w")
        self.entry_proved = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_proveedor, width=30, justify="left")
        self.entry_proved.grid(row=0, column=3, padx=3, pady=3, sticky="w")
        self.sv_proveedor.trace("w", lambda *args: limitador(self.sv_proveedor, 50))

        # Combo tipo de proceso del producto
        self.lbl_combo_proceso = tk.Label(self.frame_cuadro_entrys_datos, text="Proceso", justify="left", foreground="black")
        self.lbl_combo_proceso.grid(row=0, column=4, padx=3, pady=3, sticky="w")
        self.combo_proceso = ttk.Combobox(self.frame_cuadro_entrys_datos, textvariable=self.sv_combo_proceso,
                                          state='readonly', width=15)
        self.combo_proceso['value'] = ["RMA", "Reparacion", "Prestamo"]
        self.combo_proceso.current(0)
        self.combo_proceso.grid(row=0, column=5, padx=3, pady=3, sticky="e")
        #self.combo_estado.bind('<Tab>', lambda e: self.calcular("completo"))

        # Combo estado dentro del proceso
        self.lbl_combo_estado = tk.Label(self.frame_cuadro_entrys_datos, text="Estado", justify="left", foreground="black")
        self.lbl_combo_estado.grid(row=0, column=6, padx=3, pady=3, sticky="w")
        self.combo_estado = ttk.Combobox(self.frame_cuadro_entrys_datos, textvariable=self.sv_combo_estado,
                                         state='readonly', width=15)
        self.combo_estado['value'] = ["Pendiente", "Cambio", "Credito", "No reconocido", "Devolucion", "Finalizado"]
        self.combo_estado.current(0)
        self.combo_estado.grid(row=0, column=7, padx=3, pady=3, sticky="e")
        #self.combo_estado.bind('<Tab>', lambda e: self.calcular("completo"))

        # Entry Cliente
        self.lbl_cliente = tk.Label(self.frame_cuadro_entrys_datos, text="Cliente: ", justify="left")
        self.lbl_cliente.grid(row=1, column=0, padx=3, pady=3, sticky="w")
        self.entry_cliente = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_cliente, width=151,
                                   justify="left")
        self.entry_cliente.grid(row=1, column=1, columnspan=7, padx=3, pady=3, sticky="w")
        self.sv_cliente.trace("w", lambda *args: limitador(self.sv_cliente, 80))

        # Entry articulo
        self.lbl_articulo = tk.Label(self.frame_cuadro_entrys_datos, text="Articulo: ", justify="left")
        self.lbl_articulo.grid(row=2, column=0, padx=3, pady=3, sticky="w")
        self.entry_articulo = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_articulo, width=151,
                                    justify="left")
        self.entry_articulo.grid(row=2, column=1, columnspan=7, padx=3, pady=3, sticky="w")
        self.sv_articulo.trace("w", lambda *args: limitador(self.sv_articulo, 150))

        # Entry fallo/motivo
        self.lbl_problema = tk.Label(self.frame_cuadro_entrys_datos, text="Falla/motivo: ", justify="left")
        self.lbl_problema.grid(row=3, column=0, padx=3, pady=3, sticky="w")
        self.entry_problema = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_problema, width=151,
                                    justify="left")
        self.entry_problema.grid(row=3, column=1, columnspan=7, padx=3, pady=3, sticky="w")
        self.sv_problema.trace("w", lambda *args: limitador(self.sv_articulo, 200))

        # Entry observaciones del articulo
        self.lbl_costo_venta = tk.Label(self.frame_cuadro_entrys_datos, text="Costo/Venta: ", justify="left")
        self.lbl_costo_venta.grid(row=4, column=0, padx=3, pady=3, sticky="w")
        self.entry_costo_venta = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_costo_venta, width=151,
                                       justify="left")
        self.entry_costo_venta.grid(row=4, column=1, columnspan=7, padx=3, pady=3, sticky="w")
        self.sv_costo_venta.trace("w", lambda *args: limitador(self.sv_costo_venta, 200))

        # Entry observaciones del articulo
        self.lbl_observa = tk.Label(self.frame_cuadro_entrys_datos, text="Observaciones: ", justify="left")
        self.lbl_observa.grid(row=5, column=0, padx=3, pady=3, sticky="w")
        self.entry_observa = tk.Entry(self.frame_cuadro_entrys_datos, textvariable=self.sv_observaciones, width=151,
                                   justify="left")
        self.entry_observa.grid(row=5, column=1, columnspan=7, padx=3, pady=3, sticky="w")
        self.sv_observaciones.trace("w", lambda *args: limitador(self.sv_observaciones, 200))

    def botones_guardar(self):

        self.btn_guardar=tk.Button(self.frame_cuadro_botones_guardar, text="Guardar", command=self.fguardar, width=60,
                                   bg='Green', fg='white')
        self.btn_guardar.grid(row=0, column=0, padx=5, pady=3, sticky='nsew')

        self.btn_cancelar=tk.Button(self.frame_cuadro_botones_guardar, text="Cancelar", command=self.fcancelar, width=60, bg='black',
                                 fg='white')
        self.btn_cancelar.grid(row=0, column=1, padx=5, pady=3, sticky='nsew')

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((60, 40), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=tk.Button(self.frame_cuadro_botones_guardar, text="Salir", image=self.photo3, width=130, command=self.fsalir,
                             bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=2, padx=2, pady=3)


    # -----------------------------------------------------------------------
    # DICCIONARIOS
    # -----------------------------------------------------------------------

    def get_rma_dic(self, fecha_aux):

        return {
            "Id": self.clave,
            "rm_fecha": fecha_aux,
            "rm_articulo": self.sv_articulo.get(),
            "rm_proceso": self.sv_combo_proceso.get(),
            "rm_estado": self.sv_combo_estado.get(),
            "rm_proveedor": self.sv_proveedor.get(),
            "rm_cliente": self.sv_cliente.get(),
            "rm_falla_motivo": self.sv_problema.get(),
            "rm_costo_venta": self.sv_costo_venta.get(),
            "rm_observaciones": self.sv_observaciones.get()
        }