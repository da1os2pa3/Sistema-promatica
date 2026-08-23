"""Ctrl + Alt + O → Optimize Imports (elimina imports no usados y ordena los que quedan).
Ctrl + Alt + L → Reformat Code (reformatea el código según las reglas configuradas).
Ctrl + Alt + Shift + L → abre el cuadro de diálogo para elegir opciones avanzadas de reformateo."""

# ----------------------------------------
import os
import tkinter as tk
import tkinter.font as tkFont
from datetime import date
from tkinter import ttk
from tkinter.scrolledtext import *
from PIL import Image, ImageTk
from PDF_clase import *
from funcion_new import ClaseFuncionNew
from funciones import *
from recibos_ABM import datosRecibos
from status_bar import StatusBar


class ClaseRecibos(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)
        self.master = master
        self.status = StatusBar(self.master)

        self.master.grab_set()
        self.master.focus_set()

        # ---------------------------------------------------------------------------------
        # Instanciaciones - Objetos creados con la clase de ABM recibos
        self.varRecibos = datosRecibos(self.master)
        self.varFuncion_new = ClaseFuncionNew(self.master)
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
        ancho_ventana = 1035
        alto_ventana = 540
        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        """
            * Guarda en item el Id (I001, IB03, ..) del elemento fila en el que pase el puntero del mouse en este caso
        fila 0 el método identify_row() se usa para saber qué fila(item) del Treev está bajo una posición del mouse.
        item = self.grid_recibos.identify_row(0)
            * En Tkinter(módulo ttk), el método selection_set() del Treeview se usa para seleccionar uno o varios
        items de forma programática(por código).
        self.grid_recibos.selection_set(item)
            * Pone el foco en el item seleccionado
        self.grid_recibos.focus(item)
        """

    # ------------------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------------------

    def create_widgets(self):

        # ------------------------------------------------------------------------------
        # TITULOS
        # ------------------------------------------------------------------------------
        self.frame_titulo_top = tk.Frame(self.master)
        self.cuadro_titulos()
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=2)

        # --------------------------------------------------------------------------
        # STRINGVARS
        # --------------------------------------------------------------------------
        self.sv_buscostring =tk.StringVar(value="")
        self.sv_numero_recibo = tk.StringVar(value="0")
        self.sv_codigo_cliente = tk.StringVar(value="0")
        self.sv_nombre_cliente = tk.StringVar(value="")
        self.sv_fecha_recibo = tk.StringVar(value="")
        self.sv_importe_recibo = tk.StringVar(value="0.00")

        # --------------------------------------------------------------------------
        # VARIABLES ESPECIALES
        # --------------------------------------------------------------------------
        # La pongo aca porque si la saco arriba no tiene alcance en el scope
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")
        self.sv_fecha_recibo.set(value=datetime.strftime(date.today(), "%d/%m/%Y"))

        # --------------------------------------------------------------------------
        # TREVIEEW
        # --------------------------------------------------------------------------
        self.frame_grid_recibos=tk.LabelFrame(self.master, text="Recibos", foreground="#CF09BD")
        self.cuadro_grid_recibos()
        self.frame_grid_recibos.pack(side="top", fill="both", padx=5, pady=2)

        # --------------------------------------------------------------------------
        # BOTONES GRID - CRUD
        # --------------------------------------------------------------------------
        self.frame_botones=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_botones_grid()
        self.frame_botones.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # -------------------------------------------------------------------------------
        # BUSQUEDA - TOP Y FIN DE ARCHIVOS
        # -------------------------------------------------------------------------------
        self.frame_busquedas=tk.LabelFrame(self.master, text="", foreground="red")
        self.cuadro_busquedas()
        self.frame_busquedas.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        # -----------------------------------------------------------------------------
        # ENTRYS
        # --------------------------------------------------------------------------------
        self.frame_entrys=tk.LabelFrame(self.master, text="", foreground="red")
        
        self.frame_entrys_1=tk.LabelFrame(self.frame_entrys, text="", foreground="red")
        self.cuadro_entrys()
        self.frame_entrys_1.pack(side="top", fill="both", expand=0, padx=5, pady=2)

        self.frame_entrys_2=tk.LabelFrame(self.frame_entrys, text="Detalle recibo", foreground="red")
        self.cuadro_entrys_dos()
        self.frame_entrys_2.pack(side="top", fill="both", expand=0, padx=5, pady=3)
        
        self.frame_entrys.pack(side="top", fill="both", expand=0, padx=5, pady=3)


    # -----------------------------------------------------------------------------
    # GRID
    # -----------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        for item in self.grid_recibos.get_children():
            self.grid_recibos.delete(item)

        if len(self.filtro_activo) > 0:
            datos = self.varRecibos.consultar_recibos(self.filtro_activo)
        else:
            datos = self.varRecibos.consultar_recibos("ORDER BY cc_fecha ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[2], '%Y-%m-%d'), False)

            self.grid_recibos.insert("", "end", tags=color, text=row[0], values=(row[1], forma_normal,
                                                                                 row[4], row[5], row[6]))

        # Controles ---------------------------------------------------------

        # Devuelve una colección(tupla) con los IDs de todas las filas cargadas
        children = self.grid_recibos.get_children()
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
            self.grid_recibos.focus_set()
            self.grid_recibos.focus(posicion)
            self.grid_recibos.selection_set(posicion)
            self.grid_recibos.see(posicion)
        else:
            for item in children:
                texto = self.grid_recibos.item(item, "text")
                # print(str(set_foco) + " " + str(texto))
                if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0
                    self.grid_recibos.update_idletasks()
                    self.grid_recibos.focus_set()
                    self.grid_recibos.selection_set(item)
                    self.grid_recibos.focus(item)
                    self.grid_recibos.see(item)
                    break


    # -----------------------------------------------------------------------------
    # ESTADOS
    # -----------------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo = "ORDER BY rc_fecha ASC"
        self.dato_seleccion = ""
        self.alta_modif = 0
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_inino("disabled")
        self.habilitar_btn_inisi("normal")
        self.habilitar_btn_busqueda("normal")

    def limpiar_text(self):

        self.sv_fecha_recibo.set(value=datetime.strftime(date.today(), "%d/%m/%Y"))
        self.sv_codigo_cliente.set(value="0")
        self.sv_nombre_cliente.set(value="")
        self.sv_importe_recibo.set(value="0")
        self.text_detalle.delete('1.0', 'end')
        self.sv_buscostring.set(value="")

    def habilitar_text(self, estado):

        self.entry_fecha_recibo.configure(state=estado)
        self.entry_nombre_cliente.configure(state=estado)
        self.entry_importe_recibo.configure(state=estado)
        self.text_detalle.configure(state=estado)

    def habilitar_btn_inino(self, estado):

        self.btn_guardaritem.configure(state=estado)
        self.btn_cancelar.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)

    def habilitar_btn_inisi(self, estado):

        self.btn_nuevoitem.configure(state=estado)
        self.btn_borraitem.configure(state=estado)
        self.btn_editaitem.configure(state=estado)
        self.btn_imprime.configure(state=estado)
        self.btn_bus_cli.configure(state=estado)
        self.entry_buscar_recibo.configure(state=estado)

    def habilitar_btn_busqueda(self, estado):

        self.btn_buscar_movim.configure(state=estado)
        self.btn_showall.configure(state=estado)
        self.btn_reset_buscar.configure(state=estado)
        self.btnToparch.configure(state=estado)
        self.btnFinarch.configure(state=estado)

    # -----------------------------------------------------------------------------
    # CRUD
    # -----------------------------------------------------------------------------

    def fnuevo(self):

        self.alta_modif = 1

        self.sv_fecha_recibo.set(value=datetime.strftime(date.today(), "%d/%m/%Y"))

        self.habilitar_text("normal")
        self.habilitar_btn_inino("normal")
        self.habilitar_btn_inisi("disabled")
        self.habilitar_btn_busqueda("disabled")
        self.entry_fecha_recibo.focus()
        self.sv_numero_recibo.set(value=str(int(self.varRecibos.traer_ultimo(1)) + 1))

    def feditar(self):

        # -----------------------------------------------------------------------
        # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        self.selected = self.grid_recibos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la Tabla automaticamente al dar el alta
        self.clave = self.grid_recibos.item(self.selected, 'text')
        # -----------------------------------------------------------------------

        if self.clave == "":
            messagebox.showwarning("Modificar", "No hay nada seleccionado", parent=self)
            return

        self.alta_modif = 2

        self.habilitar_text('normal')
        self.limpiar_text()

        self.filtro_activo = "WHERE Id = " + str(self.clave)

        valores = self.varRecibos.consultar_recibos(self.filtro_activo)

        self.filtro_activo = "ORDER BY rc_fecha ASC"

        for row in valores:

            # Convierto fechas a dd/mm/aaa
            forma_normal = self.varFuncion_new.fecha_es(datetime.strftime(row[2], '%Y-%m-%d'), False)

            self.sv_fecha_recibo.set(value=forma_normal)
            self.sv_numero_recibo.set(value=row[1])
            self.sv_nombre_cliente.set(value=row[4])
            self.sv_importe_recibo.set(value=row[5])
            self.text_detalle.insert("end", row[6])

        self.habilitar_text("normal")
        self.habilitar_btn_inino("normal")
        self.habilitar_btn_inisi("disabled")
        self.habilitar_btn_busqueda("disabled")

        self.entry_fecha_recibo.focus()

    def fborrar(self):

        # -----------------------------------------------------------
        """ Guardo en self.selected, el Id del item del grid o treeview (I010, IB14.... """
        self.selected = self.grid_recibos.focus()
        self.selected_ant = self.grid_recibos.prev(self.selected)
        """ Guardo en self. clave, el Id del treeview de la primer columna (12 . 23 . 25.....) """
        self.clave = self.grid_recibos.item(self.selected, 'text')
        self.clave_ant = self.grid_recibos.item(self.selected_ant, 'text')
        # -----------------------------------------------------------

        if self.clave == "" or self.selected == "":
            self.status.set_status("❌ No hay nada seleccionado", "error")
            return

        # -----------------------------------------------------------
        """ Guardo en valores la lista con todos los valores de la fila del grid correspondiente al que voy a borrar """
        valores = self.grid_recibos.item(self.selected, 'values')
        """ En data guardo codigo y nombre del que voy a borrar para mostrar en el messagebox """
        data = str(self.clave)+" "+valores[2]
        # -----------------------------------------------------------

        r = messagebox.askquestion("Eliminar", "Confirma eliminar item?\n " + data, parent=self)
        if r == messagebox.NO:
            return

        try:
            self.varRecibos.eliminar_item_recibos(self.clave)
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("🗑 Registro eliminado correctamente", "ok")

        self.llena_grilla(self.clave_ant)

    def fguardar(self):

        # VALIDACIONES -------------------------------------------------------

        # FECHA
        if self.sv_fecha_recibo.get() == "":
            messagebox.showerror("Error", "Fecha en blanco", parent=self)
            self.entry_fecha_recibo.focus()
            return
        # Importe
        if float(self.sv_importe_recibo.get()) == 0:
            messagebox.showerror("Error", "Importe en cero", parent=self)
            self.entry_importe_recibo.focus()
            return
        # Nombre de cliente
        if self.sv_nombre_cliente.get() == "":
            messagebox.showerror("Error", "Indique cliente", parent=self)
            self.entry_nombre_cliente.focus()
            return
        # --------------------------------------------------------------------

        # --------------------------------------------------------------------
        # guardo el Id del Treeview (I001, IB00, ...) en selected para ubicacion del foco a posteriori
        self.selected = self.grid_recibos.focus()
        # Guardo el Id del registro de la Tabla (no es el mismo que el otro, este puedo verlo en la base (12, 20...)
        self.clave = self.grid_recibos.item(self.selected, 'text')
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        # PASO DICCIONARIO PARA INSERTAR O MODIFICAR
        """ Debo poner los nombres de los campos de la tabla y asignarles las variables """

        dic_recibo = {
            "Id": self.clave,
            "rc_numero": self.sv_numero_recibo.get(),
            "rc_fecha": self.sv_fecha_recibo.get(),
            "rc_codcli": self.sv_codigo_cliente.get(),
            "rc_nomcli": self.sv_nombre_cliente.get(),
            "rc_importe": self.sv_importe_recibo.get(),
            "rc_concepto": self.text_detalle.get(1.0, 'end-1c')
        }
        # -----------------------------------------------------------------

        # -----------------------------------------------------------------
        id_ref = ""
        try:
            if self.alta_modif == 1:
                self.id_nuevo = self.varRecibos.insertar_recibo(dic_recibo)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                self.varRecibos.modificar_recibos(dic_recibo)
                id_ref = self.clave
        except Exception:
            self.varFuncion_new.mostrar_error()
            return
        else:
            self.status.set_status("✔ Registro guardado correctamente", "ok")

        # Terminacion y habilitaciones
        self.filtro_activo = "ORDER BY rc_fecha ASC"
        self.limpiar_text()
        self.habilitar_btn_inino("disabled")
        self.habilitar_btn_inisi("normal")
        self.habilitar_btn_busqueda("normal")
        self.sv_numero_recibo.set(value=(int(self.varRecibos.traer_ultimo(1)) + 1))
        self.llena_grilla(id_ref)
        self.grid_recibos.focus()
        self.habilitar_text("disabled")
        self.alta_modif = 0

    def fcancelar(self):

        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.NO:
            return

        self.fshowall()
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_btn_inino("disabled")
        self.habilitar_btn_inisi("normal")
        self.habilitar_btn_busqueda("normal")
        self.sv_numero_recibo.set(value=str(int(self.varRecibos.traer_ultimo(1)) + 1))
        self.grid_recibos.focus()

    def fsalir(self):

        self.master.destroy()

    # -----------------------------------------------------------------------------
    # PUNTEROS
    # -----------------------------------------------------------------------------

    def ftoparch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_recibos, 'TOP')

    def ffinarch(self):
        self.varFuncion_new.mover_puntero_topend(self.grid_recibos, 'END')

    # -----------------------------------------------------------------------------
    # BUSQUEDAS
    # -----------------------------------------------------------------------------

    def fbuscar_en_tabla(self):

        # verifico que el string de busqueda traiga algo o este vacio
        if len(self.sv_buscostring.get()) <= 0:
            messagebox.showwarning("Buscar", "No ingreso busqueda", parent=self)
            return

        se_busca = self.sv_buscostring.get()

        # Retorno las coincidencias
        try:
            datos = self.varRecibos.buscar_recibos(se_busca)
        except Exception:
            self.varFuncion_new.mostrar_error()
            return

        # Limpio el grid
        for item in self.grid_recibos.get_children():
            self.grid_recibos.delete(item)

        # carga la grilla con los registros seleccionados
        for row in datos:
            self.grid_recibos.insert("", "end", text=row[0], values=row[1:])
            # 👉 row[1:] significa:desde el segundo elemento en adelante o sea: row[1], row[2], row[3]...

        items = self.grid_recibos.get_children()

        # selecciono el primero de la tabla y pongo foco y visibilidad
        if items:
            primero = items[0]
            self.grid_recibos.selection_set(primero)
            self.grid_recibos.focus(primero)
            self.grid_recibos.see(primero)

    def fshowall(self):
        self.filtro_activo = "ORDER BY rc_fecha ASC"
        self.selected = self.grid_recibos.focus()
        self.clave = self.grid_recibos.item(self.selected, 'text')
        self.llena_grilla(self.clave)

    def freset_buscar(self):
        self.sv_buscostring.set(value="")
        self.fshowall()

    def fbuscli(self):

        """ Creo una variable (que_busco) que contiene los parametros de busqueda - Tabla, el string de busqueda y en que
        campos debe hacerse """

        que_busco = "clientes WHERE INSTR(apellido, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(nombres, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " OR INSTR(apenombre, '" + self.sv_nombre_cliente.get() + "') > 0" \
                    + " ORDER BY apenombre"

        """ Llamo a la funcion ventana de seleccion de items. Paso parametros de Tabla-campos a mostrar en orden 
        de como quiero verlos-Titulos para cada columna de esos campos-String de busqueda definido 
        arriba (que_busco) """

        valores_new = self.varFuncion_new.ventana_selec("clientes", "apenombre", "codigo",
                      "direccion", "Apellido y nombre", "Codigo", "Direccion", que_busco,
                                                        "Orden: Alfabetico cliente", "N")

        """ Esto es ya iterar sobre lo que me devuelve la funcion de seleccion para asignar ya los valores a 
        los Entrys correspondientes """

        for item in valores_new:
            self.sv_nombre_cliente.set(value=item[15])
            self.sv_codigo_cliente.set(value=item[1])

        self.entry_nombre_cliente.focus()
        self.entry_nombre_cliente.icursor(tk.END)

    def doble_click_grid(self, event):
        self.feditar()

    # -----------------------------------------------------------------------------
    # VALIDACIONES
    # -----------------------------------------------------------------------------

    def formato_fecha(self, pollo):

        """ Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        #estado_antes = self.sv_fecha_recibo.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_validacion = self.varFuncion_new.validar_fecha(self.sv_fecha_recibo, self.entry_fecha_recibo)

        una_fecha = date.today()

        match retorno_validacion:

            case "break":
                self.entry_fecha_recibo.focus()
                return
            case "S":
                self.entry_fecha_recibo.focus()
            case "N" | "BLANCO":
                pass
            case "":
                self.sv_fecha_recibo.set(una_fecha.strftime('%d/%m/%Y'))
                self.entry_fecha_recibo.focus()
            case _:
                return

        # if retorno_VerFal == "":
        #     self.sv_fecha_recibo.set(value=estado_antes)
        #     self.entry_fecha_recibo.focus()
        #     return ("error")
        # elif retorno_VerFal == "N":
        #     # esto es error en el año y decidio no seguir
        #     self.sv_fecha_recibo.set(value=estado_antes)
        #     self.entry_fecha_recibo.focus()
        #     return ("error")
        # elif retorno_VerFal == "BLANCO":
        #     return ("error")
        # else:
        #     self.sv_fecha_recibo.set(value=retorno_VerFal)
        # return ("bien")

    # def controlar(self):
    #
    #     # Control de que no ingresen mas de una vez el '-' o el '.' - Funcion en funciones.py
    #     if not control_forma(self.sv_importe_recibo.get()):
    #         self.sv_importe_recibo.set(value="0")
    #         self.entry_importe_recibo.focus()
    #         return
    #     # Valido que los campos no me ingresen en blanco
    #     if self.sv_importe_recibo.get() == "" or self.sv_importe_recibo.get() == "-" or self.sv_importe_recibo.get() == ".":
    #         self.sv_importe_recibo.set(value="0")
    #         self.entry_importe_recibo.focus()
    #         return
    #     else:
    #         self.sv_importe_recibo.set(value=round(float(self.sv_importe_recibo.get()), 2))

    # -----------------------------------------------------------------------------
    # INFORMES - PDF
    # -----------------------------------------------------------------------------

    def fimprime(self):

        # traigo el registro que quiero imprimir
        self.selected = self.grid_recibos.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_recibos.item(self.selected, 'text')

        if self.clave == "":
            messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
            return

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

        valores = self.grid_recibos.item(self.selected, 'values')
        numero_recibo = valores[0]
        feac = valores[1]
        cliente = valores[2]
        importe = valores[3]
        detalle = valores[4]

        # Imprimo el encabezado de pagina ---------------------------------------------------
        pdf.set_font('Arial', '', 9)
        pdf.cell(w=0, h=5, txt="Recibo Nº: " + str(numero_recibo) + " - Fecha y Hora: " + feac , border=1, align='C',
                 fill=0, ln=1)
        # -----------------------------------------------------------------------------------

        importe_format = formatear_cifra(float(importe))

        var_descripcion = ("Recibi del Sr./a " + cliente + " la suma de pesos " + importe_format +" "+
                           numero_to_letras(float(importe)) + ", segun el siguiente detalle: " + " " + detalle )

        pdf.set_font('Courier', 'B', 10)
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(w=0, h=5, txt=var_descripcion, align='L', fill=0)
        pdf.cell(w=0, h=5, txt='', align='L', fill=0, ln=1)

        pdf.multi_cell(w=0, h=5, txt="Total recibido $: "+importe_format+"----------------------", align='L', fill=0)
        pdf.cell(w=0, h=15, txt='', align='L', fill=0, ln=1)

        pdf.multi_cell(w=0, h=5, txt="...........................................", align='R', fill=0)
        pdf.cell(w=0, h=1, txt='', align='L', fill=0, ln=1)
        pdf.multi_cell(w=0, h=5, txt="Promatica Computacion", align='R', fill=0)

        pdf.output('hoja.pdf')
        path = 'hoja.pdf'
        os.system(path)

    def cuadro_titulos(self):

        # Armo el logo y el titulo
        self.photocc = Image.open('recibo.png')
        self.photocc = self.photocc.resize((50, 50), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_recibo = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_recibo = tk.Label(self.frame_titulo_top, image=self.png_recibo, bg="red", relief="ridge", bd=5)

        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=52, text="Recibos",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_recibo.grid(row=0, column=0, sticky="w", padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")

    def cuadro_grid_recibos(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_grid_recibos)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_recibos = ttk.Treeview(self.frame_grid_recibos, height=5, columns=("col1", "col2", "col3", "col4",
                                                                                  "col5"))

        self.grid_recibos.bind("<Double-Button-1>", self.doble_click_grid)

        self.grid_recibos.column("#0", width=40, anchor="center", minwidth=40)
        self.grid_recibos.column("col1", width=50, anchor="center", minwidth=40)
        self.grid_recibos.column("col2", width=60, anchor="center", minwidth=60)
        self.grid_recibos.column("col3", width=120, anchor="center", minwidth=100)
        self.grid_recibos.column("col4", width=100, anchor="center", minwidth=80)
        self.grid_recibos.column("col5", width=250, anchor="center", minwidth=220)

        self.grid_recibos.heading("#0", text="Id", anchor="center")
        self.grid_recibos.heading("col1", text="Numero", anchor="center")
        self.grid_recibos.heading("col2", text="Fecha", anchor="center")
        self.grid_recibos.heading("col3", text="Cliente", anchor="center")
        self.grid_recibos.heading("col4", text="Importe", anchor="center")
        self.grid_recibos.heading("col5", text="Detalle", anchor="center")

        self.grid_recibos.tag_configure('oddrow', background='light grey')
        self.grid_recibos.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_grid_recibos, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_grid_recibos, orient="vertical")
        self.grid_recibos.config(xscrollcommand=scroll_x.set)
        self.grid_recibos.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_recibos.xview)
        scroll_y.config(command=self.grid_recibos.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_recibos['selectmode'] = 'browse'

        self.grid_recibos.pack(side="top", fill="both", expand=1, padx=5, pady=2)

    def cuadro_botones_grid(self):

        for c in range(6):
            self.frame_botones.grid_columnconfigure(c, weight=1, minsize=130)

        # Nuevo item recibo
        icono = self.cargar_icono("archivo-nuevo.png")
        self.btn_nuevoitem = tk.Button(self.frame_botones, text=" Nuevo", command=self.fnuevo, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_nuevoitem.image = icono
        self.btn_nuevoitem.config(image=icono)
        self.btn_nuevoitem.grid(row=0, column=0, padx=5, pady=2)

        # Editar
        icono = self.cargar_icono("editar.png")
        self.btn_editaitem = tk.Button(self.frame_botones, text=" Editar", command=self.feditar, width=24, bg="blue",
                                    fg="white", compound="left")
        self.btn_editaitem.image = icono
        self.btn_editaitem.config(image=icono)
        self.btn_editaitem.grid(row=0, column=1, padx=5, pady=2)

        # Eliminar
        icono = self.cargar_icono("eliminar.png")
        self.btn_borraitem = tk.Button(self.frame_botones, text=" Eliminar", command=self.fborrar, width=24, bg="red",
                                    fg="white", compound="left")
        self.btn_borraitem.image = icono
        self.btn_borraitem.config(image=icono)
        self.btn_borraitem.grid(row=0, column=2, padx=5, pady=2)

        # Guardar
        icono = self.cargar_icono("guardar.png")
        self.btn_guardaritem = tk.Button(self.frame_botones, text=" Guardar", command=self.fguardar, width=24,
                                         bg="green", fg="white", compound="left")
        self.btn_guardaritem.image = icono
        self.btn_guardaritem.config(image=icono)
        self.btn_guardaritem.grid(row=0, column=3, padx=5, pady=2)

        # Cancelar
        icono = self.cargar_icono("cancelar.png")
        self.btn_cancelar = tk.Button(self.frame_botones, text=" Cancelar", command=self.fcancelar, width=24,
                                      bg="black", fg="white", compound="left")
        self.btn_cancelar.image = icono
        self.btn_cancelar.config(image=icono)
        self.btn_cancelar.grid(row=0, column=4, padx=5, pady=2)

        # Salir
        icono = self.cargar_icono("salida.png")
        self.btn_salir=tk.Button(self.frame_botones, text="Salir", width=24, command=self.fsalir, bg="yellow",
                                 fg="black", compound="left")
        self.btn_salir.image = icono
        self.btn_salir.config(image=icono)
        self.btn_salir.grid(row=0, column=5, padx=5, pady=2, sticky="nsew")

        for widg in self.frame_botones.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_busquedas(self):

        for c in range(5):
            self.frame_busquedas.grid_columnconfigure(c, weight=1, minsize=130)

        # Busqueda titular recibo
        icono = self.cargar_icono("buscar.png")
        self.lbl_buscar_recibo = tk.Label(self.frame_busquedas, text="Buscar: ", justify="left", compound="left")
        self.lbl_buscar_recibo.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.lbl_buscar_recibo.image = icono
        self.lbl_buscar_recibo.config(image=icono)
        self.entry_buscar_recibo = tk.Entry(self.frame_busquedas, textvariable=self.sv_buscostring, width=50)
        self.entry_buscar_recibo.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        # Boton buscar recibo
        icono = self.cargar_icono("filtrar.png")
        self.btn_buscar_movim = tk.Button(self.frame_busquedas, text="Buscar", command=self.fbuscar_en_tabla, bg="blue",
                                       fg="white", width=24, compound="left")
        self.btn_buscar_movim.image = icono
        self.btn_buscar_movim.config(image=icono)
        self.btn_buscar_movim.grid(row=0, column=2, padx=5, pady=3, sticky="w")

        # Show all
        icono = self.cargar_icono("ver_todo.png")
        self.btn_showall = tk.Button(self.frame_busquedas, text=" Mostrar todo", command=self.fshowall,
                                  bg="blue", fg="white", width=24, compound="left")
        self.btn_showall.image = icono
        self.btn_showall.config(image=icono)
        self.btn_showall.grid(row=0, column=3, padx=5, pady=3, sticky="w")

        # limpiar busqueda
        icono = self.cargar_icono("limpiar.png")
        self.btn_reset_buscar = tk.Button(self.frame_busquedas, text=" Limpiar busqueda", command=self.freset_buscar,
                                       bg="blue", fg="white", width=24, compound="left")
        self.btn_reset_buscar.image = icono
        self.btn_reset_buscar.config(image=icono)
        self.btn_reset_buscar.grid(row=0, column=4, padx=5, pady=3, sticky="w")

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = tk.Button(self.frame_busquedas, text="", image=self.photo4, command=self.ftoparch, bg="grey",
                                 fg="white")
        self.btnToparch.grid(row=0, column=5, padx=5, sticky="nsew", pady=2)

        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = tk.Button(self.frame_busquedas, text="", image=self.photo5, command=self.ffinarch, bg="grey",
                                 fg="white")
        self.btnFinarch.grid(row=0, column=6, padx=5, sticky="nsew", pady=2)

        for widg in self.frame_busquedas.winfo_children():
            widg.grid_configure(padx=5, pady=3, sticky='nsew')

    def cuadro_entrys(self):

        # NUMERO DE RECIBO
        fff = tkFont.Font(family="Arial", size=12, weight="bold")
        self.lbl_numero_recibo = tk.Label(self.frame_entrys_1, text="Nº Recibo: ", justify="left")
        self.lbl_numero_recibo.grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_numero_recibo = tk.Label(self.frame_entrys_1, textvariable=self.sv_numero_recibo, font=fff,
                                         fg="blue", width=10, justify="right")
        self.entry_numero_recibo.grid(row=0, column=1, padx=5, pady=2, sticky="e")

        # FECHA DEL RECIBO
        self.lbl_fecha_recibo = tk.Label(self.frame_entrys_1, text="Fecha: ", justify="left")
        self.lbl_fecha_recibo.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_fecha_recibo = tk.Entry(self.frame_entrys_1, textvariable=self.sv_fecha_recibo, width=10,
                                        justify="right")
        self.entry_fecha_recibo.bind("<FocusOut>", self.formato_fecha)
        self.entry_fecha_recibo.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        # BOTON BUSCAR CLIENTE
        self.photo_bus_cli = Image.open('buscar.png')
        self.photo_bus_cli = self.photo_bus_cli.resize((25, 25), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_bus_cli = ImageTk.PhotoImage(self.photo_bus_cli)
        self.btn_bus_cli = tk.Button(self.frame_entrys_1, text="", image=self.photo_bus_cli, command=self.fbuscli,
                                  bg="grey", fg="white")
        self.btn_bus_cli.grid(row=0, column=4, padx=5)

        # DATOS NOMBRE CLIENTE
        self.lbl_nombre_cliente = tk.Label(self.frame_entrys_1, text="Cliente: ", justify="left")
        self.lbl_nombre_cliente.grid(row=0, column=5, padx=2, pady=2, sticky="w")
        self.entry_nombre_cliente = tk.Entry(self.frame_entrys_1, textvariable=self.sv_nombre_cliente, width=52)
        self.entry_nombre_cliente.grid(row=0, column=6, padx=2, pady=2, sticky="w")
        self.lbl_codigo_cliente = tk.Label(self.frame_entrys_1, text="(" + self.sv_codigo_cliente.get() + ")",
                                        justify="left")
        self.lbl_codigo_cliente.grid(row=0, column=7, padx=2, pady=2, sticky="w")

        # IMPORTE RECIBO
        self.lbl_importe_recibo = tk.Label(self.frame_entrys_1, text="Importe: ", justify="left")
        self.lbl_importe_recibo.grid(row=0, column=8, padx=5, pady=2, sticky="w")
        self.entry_importe_recibo = tk.Entry(self.frame_entrys_1, textvariable=self.sv_importe_recibo, width=20, justify="right")
        self.entry_importe_recibo.config(validate="key", validatecommand=self.vcmd)
        self.entry_importe_recibo.bind("<FocusOut>", lambda e: self.varFuncion_new.corregir_al_salir(self.entry_importe_recibo))
        self.entry_importe_recibo.grid(row=0, column=9, padx=5, pady=2, sticky="w")
        #self.entry_importe_recibo.bind('<Tab>', lambda e: self.controlar())
        self.sv_importe_recibo.trace("w", lambda *args: limitador(self.sv_importe_recibo, 15))

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.Resampling.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = tk.Button(self.frame_entrys_1, image=self.photo_imp, pady=3, command=self.fimprime, border=3)
        self.btn_imprime.grid(row=0, column=10, padx=4, pady=2)

    def cuadro_entrys_dos(self):

        # DETALLE Novedades
        self.text_detalle = ScrolledText(self.frame_entrys_2)
        self.text_detalle.config(width=120, height=6, wrap="word", padx=4, pady=3)
        self.text_detalle.grid(row=1, column=1, padx=4, pady=5, sticky="nsew")

    def cargar_icono(self, path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)



"""
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
🔥 CÓMO USARLO
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
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
"""
