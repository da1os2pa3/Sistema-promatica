import os
import sys
# ---------------------------------------------------
from articulos_ABM import datosArtic
from funciones import *
from funcion_new import ClaseFuncion_new
# ---------------------------------------------------
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import tkinter.font as tkFont
#from tkinter import messagebox, filedialog
from tktooltip import ToolTip
# ---------------------------------------------------
from datetime import date, datetime
from PIL import Image, ImageTk

class Clase_Articulos(tk.Frame):

    def __init__(self, master=None):

        super().__init__(master)
        self.master = master

        # Seteo pantalla master principal  ------------------------------------------------
        self.master.grab_set()
        self.master.focus_set()
        # ---------------------------------------------------------------------------------

        # Instanciaciones -----------------------------------------------------------------
        # Creo el objeto - clase definida en articulos_ABM.py
        self.varArtic = datosArtic(self.master)
        self.varFuncion_new = ClaseFuncion_new(self.master)
        # ---------------------------------------------------------------------------------

        # Usuario no puede modificar tamaña pantalla --------------------------------------
        self.master.resizable(0, 0)
        # ---------------------------------------------------------------------------------

        # POSICIONAMIENTO VENTANA ---------------------------------------------------------

        """ Actualizamos todo el contenido de la ventana (la ventana pude crecer si se le agrega
        mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer. """

        # Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 1120
        hventana = 650
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        self.create_widgets()
        self.estado_inicial()
        self.llena_grilla("")

        # SETEO INICIAL DEL GRID --------------------------------------------------------

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        tupla vacía en caso de no haber ninguno
        . Otras funciones para manejar los elementos seleccionados incluyen:
          -selection_add(): añade elementos a la selección.
          -selection_remove(): remueve elementos de la selección.
          -selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
          -selection_toggle(): cambia la selección de un elemento.
        # Carga del Treeview y seteo de foco y punteros sobre el mismo (grid) """

        # # guarda en item el Id del elemento fila en este caso fila 0
        # item = self.grid_articulos.identify_row(0)
        # self.grid_articulos.selection_set(item)
        # # pone el foco en el item seleccionado
        # self.grid_articulos.focus(item)
        # -------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # WIDGETS -*-
    # ------------------------------------------------------------------------------

    def create_widgets(self):

        # -------------------------------------------------------------------------------
        # GPT ||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        """ Es para los mensajes sobre eventos del sistema, reemplazaria a algunos messagebox
        Ubicada ultima linea de la pantalla - barra de estado"""

        self.status_var = tk.StringVar()

        self.status_bar = tk.Label(
            self.master,
            textvariable=self.status_var,
            bd=1,
            relief="sunken",
            anchor="w",
            bg="#f0f0f0"
        )
        self.status_bar.pack(side="bottom", fill="x")
        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        # ------------------------------------------------------------------------------

        # VARIABLES  -------------------------------------------------------------------
        # para la funcion validate y controlar campos solo numericos
        self.vcmd = (self.register(self.varFuncion_new.validar), "%P")
        # ------------------------------------------------------------------------------

        # IMAGENES Y CARPETAS DE FOTOS DE ARTICULOS ------------------------------------
        self.imagen_defa = "tapiz.jpg"
        # Carpetas de trabajo
        self.carpeta_principal = os.path.dirname(__file__)
        # Debe existir la carpeta 'fotos' en la carpeta donde este el sistema
        self.carpeta_fotos = os.path.join(self.carpeta_principal, "fotos")
        # Verifico que existan carpetas
        if os.path.isfile(self.carpeta_fotos):
            messagebox.showerror("Error", "No existe carpeta de fotos")
            return
        # -------------------------------------------------------------------------------

        # TITULOS -----------------------------------------------------------------------
        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = tk.Frame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('productos.png')
        self.photo3 = self.photo3.resize((100, 75), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_articulos = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_articulos = tk.Label(self.frame_titulo_top, image=self.png_articulos, bg="red", relief="ridge", bd=5)

        self.lbl_titulo = tk.Label(self.frame_titulo_top, width=29, text="Articulos", bg="black", fg="gold",
                                font=("Arial bold", 38, "bold"), bd=5, relief="ridge", padx=10)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_articulos.grid(row=0, column=0, sticky="w", padx=4, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, padx=11, sticky="nsew")
        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=5)
        # ---------------------------------------------------------------------------------------

        # STRINGVARS ----------------------------------------------------------------------------
        self.strvar_codigo = tk.StringVar(value="")
        self.strvar_descripcion = tk.StringVar(value="")
        self.strvar_marca = tk.StringVar(value="")
        self.strvar_rubro = tk.StringVar(value="")
        self.strvar_codbar = tk.StringVar(value="")
        self.strvar_observa = tk.StringVar(value="")
        self.strvar_fechaultact = tk.StringVar(value="")
        self.strvar_costo_historico = tk.StringVar(value="0.00")
        self.strvar_imagen_Art = tk.StringVar(value="")

        self.strvar_buscar_articulo = tk.StringVar(value="")

        self.strvar_costo_neto_dolar = tk.StringVar(value="0.00")
        self.costo_neto_dolar_comparado = tk.StringVar(value="0.00")
        self.strvar_costo_neto_pesos = tk.StringVar(value="0.00")
        self.strvar_tasa_iva = tk.StringVar(value="0.00")
        self.strvar_total_iva = tk.StringVar(value="0.00")
        self.strvar_tasa_impint = tk.StringVar(value="0.00")
        self.strvar_total_impint = tk.StringVar(value="0.00")
        self.strvar_subtotal = tk.StringVar(value="0.00")
        self.strvar_tasa_ganancia = tk.StringVar(value="0.00")
        self.strvar_total_ganancia = tk.StringVar(value="0.00")
        self.strvar_total_precio_venta = tk.StringVar(value="0.00")
        self.strvar_total_precio_venta_mas10 = tk.StringVar(value="0.00")
        self.strvar_costo_dolar_bruto = tk.StringVar(value="0.00")
        self.strvar_costo_pesos_bruto = tk.StringVar(value="0.00")
        self.strvar_recargo_tarjeta = tk.StringVar(value="0.00")

        self.strvar_dolar_actual = tk.StringVar()
        # -------------------------------------------------------------------------------

        # BOTONES -----------------------------------------------------------------------

        # LabelFrame para colocar los botones laterales - Debo definirla antes que el frame del Tv
        # porque va colocada a la izquierda y el tv a la derecha
        barra_botones = tk.LabelFrame(self.master)

        # BOTONES 1 - Nuevo, Editar,.....
        self.botones1 = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.cuadro_botones1()
        self.botones1.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES 2 - Orden - Tope y fin de archivo .....
        self.botones2 = tk.LabelFrame(barra_botones, bd=5, relief="ridge")
        self.cuadro_botones2()
        self.botones2.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES 3 - Salida sistema .....
        self.botones3 = tk.LabelFrame(barra_botones, bd=2)
        self.cuadro_botones3()
        self.botones3.pack(side="top", padx=3, pady=3, fill="y")

        # BOTONES 4 - Informacion dolar .....
        self.botones4 = tk.LabelFrame(barra_botones, bd=2)
        self.cuadro_botones4()
        self.botones4.pack(side="top", padx=3, pady=3, fill="y")

        barra_botones.pack(side="left", padx=5, pady=5, ipady=5, fill="y")
        # ---------------------------------------------------------------------------------------

        # Frame principal -----------------------------------------------------------------------
        self.frame_tv = tk.Frame(self.master)

        # BUSQUEDAS -----------------------------------------------------------------------------
        self.frame_buscar = tk.LabelFrame(self.frame_tv)
        self.cuadro_buscar_articulo()
        self.frame_buscar.pack(side="top", fill="both", expand=1, padx=5, pady=3)
        # ----------------------------------------------------------------------------------------

        # TREEVIEWS ------------------------------------------------------------------------------
        self.cuadro_grid_articulos()
        # ----------------------------------------------------------------------------------------

        self.frame_tv.pack(side="top", fill="both", padx=5, pady=5)
        # ----------------------------------------------------------------------------------------

        # ENTRYS ---------------------------------------------------------------------------------

        # ENTRYS GENERAlES
        self.sector_entry = tk.LabelFrame(self.master)
        self.cuadro_entrys_generales()
        self.sector_entry.pack(expand=1, side="left", fill="both", pady=5, padx=2)

        # TOTALES PRECIO ARTICULO
        self.sector_totales = tk.LabelFrame(self.master)
        self.cuadro_sector_totales()
        self.sector_totales.pack(expand=1, side="left", fill="both", pady=5, padx=2)

        # IMAGEN DEL ARTICULO
        self.sector_imagen = tk.LabelFrame(self.master)
        self.cuadro_imagenes_articulos()
        self.entry_imagen_art.pack(expand=0, side="top", pady=3, padx=2)
        self.btn_ruta_imagen.pack(expand=0, side="top", pady=3, padx=2)
        self.lbl_imagen_art.pack(expand=1, side="top", fill="both", pady=2, padx=2)
        self.sector_imagen.pack(expand=1, side="left", fill="both", pady=5, padx=2)
        # ----------------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------
    # GRID -*-
    # ----------------------------------------------------------------------------

    def llena_grilla(self, set_foco):

        """ En set_foco viene el Id de la tabla que identidica el registro donde quiero oner el foco - 2312, 23, 456..
        Puede llegar a venir en vacio """
        # Si hay un error en insertar devuelve None la funcion insertar de ABM
        if set_foco is None:
            print("⚠️ set_foco = None (posible error al insertar)")
            return

        # Limpio el Grid
        for item in self.grid_articulos.get_children():
            self.grid_articulos.delete(item)

        # Traigo los datos a insertar en el GRid
        if len(self.filtro_activo) > 0:
            datos = self.varArtic.consultar_articulo(self.filtro_activo)
        else:
            datos = self.varArtic.consultar_articulo("ORDER BY rubro, marca, descripcion ASC")

        cont = 0
        for row in datos:

            cont += 1
            color = ('evenrow',) if cont % 2 else ('oddrow',)

            # convierto fecha de 2024-12-19 a 19/12/2024
            forma_normal = fecha_str_reves_normal(self, datetime.strftime(row[11], '%Y-%m-%d'), False)

            precio_final_pesos = round(float((row[6]*(1+(row[7]/100))) *
                                             (1+(row[9]/100))) * float(self.strvar_dolar_actual.get()))

            self.grid_articulos.insert("", "end", tags=color, text=row[0], values=(row[1], row[2], row[3],
                                                    row[4], formatear_cifra(precio_final_pesos), row[6], row[5], row[7],
                                                    row[9], row[10], forma_normal, row[12], row[13]))

        # Controles-----------------------------------------------------------------------
        # Grid negativo
        if not len(self.grid_articulos.get_children()) >= 0:
            self.set_status("❌ Error inesperado, Grid negativo", "error")
            return
        # Foco vacio, voy al primero de la grilla
        if not set_foco:
            self.grid_articulos.selection_set(self.grid_articulos.get_children()[0])
        # --------------------------------------------------------------------------------

        # Posicionamiento del foco en el Grid, voy al Id valor del set_foco --------------
        for item in self.grid_articulos.get_children():

            texto = self.grid_articulos.item(item, "text")

            # if str(texto) == str(set_foco):
            if str(texto).strip() == str(set_foco).strip():  # suponiendo que el ID está en la columna 0

                # 👉 Fuerza a Tkinter a procesar actualizaciones pendientes de la UI. Sirve para asegurarse
                # que el widget esté actualizado antes de hacer foco / scroll.
                self.grid_articulos.update_idletasks()
                # 👉 Le da el foco al Treeview(como si hicieras click sobre él).
                self.grid_articulos.focus_set()
                # 👉 Selecciona la fila encontrada.
                self.grid_articulos.selection_set(item)
                # 👉 Mueve el cursor interno del Treeview a esa fila(la deja como “activa”).
                self.grid_articulos.focus(item)
                self.grid_articulos.see(item)
                break
        # --------------------------------------------------------------------------------

    # ------------------------------------------------------------------------
    # ESTADOS -*-
    # ------------------------------------------------------------------------

    def estado_inicial(self):

        self.filtro_activo = "ORDER BY rubro, marca, descripcion ASC"
        self.alta_modif = 0
        self.limpiar_text()
        self.habilitar_text("disabled")
        self.habilitar_Btn_Oper("normal")
        self.habilitar_Btn_Final("disabled")

    def habilitar_text(self, estado):

        for entry in [
            self.entry_codigo,
            self.entry_descripcion,
            self.combo_marca,
            self.combo_rubro,
            self.entry_codbar,
            self.entry_imagen_art,
            self.entry_costo_neto_dolar,
            self.entry_costo_neto_pesos,
            self.combo_iva,
            self.entry_tasa_impint,
            self.entry_tasa_ganancia,
            self.entry_total_precio_venta,
            self.entry_observa,
            self.entry_fechaultact,
            self.entry_costo_historico,
            self.btn_ruta_imagen,
        ]:
            entry.configure(state=estado)

        if self.alta_modif == 1:
            self.grid_articulos['selectmode'] = 'none'
            self.grid_articulos.bind("<Double-Button-1>", self.fNo_modifique)
        if self.alta_modif == 2 or self.alta_modif == 0:
            self.grid_articulos['selectmode'] = 'browse'
            self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)

    def limpiar_text(self):

        for entry in [
            self.entry_codigo,
            self.entry_descripcion,
            self.combo_marca,
            self.combo_rubro,
            self.entry_codbar,
            self.entry_imagen_art,
            self.entry_costo_neto_dolar,
            self.entry_costo_neto_pesos,
            self.combo_iva,
            self.entry_tasa_impint,
            self.entry_tasa_ganancia,
            self.entry_total_precio_venta,
            self.entry_observa,
            self.entry_fechaultact,
            self.entry_costo_historico,
        ]:
            entry.delete(0, "end")

        for strvar1 in [
            self.strvar_codigo,
            self.strvar_descripcion,
            self.strvar_codbar,
            self.strvar_observa,
            self.strvar_fechaultact,
            self.strvar_codbar,
            self.strvar_observa,
            self.strvar_imagen_Art,
            self.strvar_buscar_articulo
        ]:
            strvar1.set(value="")

        for strvar2 in [
            self.strvar_costo_neto_dolar,
            self.strvar_costo_neto_pesos,
            self.strvar_tasa_impint,
            self.strvar_tasa_ganancia,
            self.strvar_tasa_iva,
            self.strvar_costo_historico,
            self.strvar_total_iva,
            self.strvar_total_impint,
            self.strvar_subtotal,
            self.strvar_total_ganancia,
            self.strvar_total_precio_venta,
            self.strvar_total_precio_venta_mas10,
            self.strvar_costo_dolar_bruto,
            self.strvar_costo_pesos_bruto,
        ]:
            strvar2.set(value="0.00")

        self.combo_marca.set("")
        self.combo_rubro.set("")
        self.combo_iva.set("")
        self.imagen_defa = "tapiz.jpg"
        self.recarga_imagen()

    def habilitar_Btn_Oper(self, estado):

        for config in [
            self.btn_nuevo,
            self.btn_eliminar,
            self.btn_editar,
            self.btn_Toparch,
            self.btn_Finarch,
            self.btn_orden_apellido,
            self.btn_orden_codigo,
            self.entry_buscar_articulo,
            self.btn_mostrar_todo,
            self.btn_buscar_articulo,
            self.combo_bus_marca,
            self.combo_bus_rubro,
            self.btn_reset_rubro,
            self.btn_reset_marca
        ]:
            config.configure(state=estado)

    def habilitar_Btn_Final(self, estado):
        self.btn_guardar.configure(state=estado)

    def fCancelar(self):
        r = messagebox.askquestion("Cancelar", "Confirma cancelar operacion actual?", parent=self)
        if r == messagebox.YES:
            self.estado_inicial()

    def fReset(self):
        self.estado_inicial()
        self.fResetmarca()
        self.fResetrubro()
        self.llena_grilla("")
        self.varFuncion_new.mover_puntero_topend(self.grid_articulos, 'TOP')
        self.btn_nuevo.focus()

    def DobleClickGrid(self, event):
        self.fEditar()

    def fNo_modifique(self, event):
        return "breack"

    def fSalir(self):
        self.master.destroy()

    # -----------------------------------------------------------------
    # CRUD -*-
    # -----------------------------------------------------------------

    def fNuevo(self):

        self.alta_modif = 1

        self.habilitar_text("normal")
        self.limpiar_text()
        self.habilitar_Btn_Final("normal")
        self.habilitar_Btn_Oper("disabled")

        self.combo_iva.current(0)

        for combo in (self.combo_rubro, self.combo_marca):
            combo.set("")
        for combo in (self.combo_rubro, self.combo_marca, self.combo_iva):
            combo.configure(state="readonly")

        # Cambio el formato de la fecha
        self.entry_fechaultact.insert(0, date.today().strftime('%d/%m/%Y'))
        self.entry_codigo.focus()

    def fEditar(self):

        """ self.selected = Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
        * self.clave = Asi obtengo la clave de la base de datos campo Id que no es lo mismo que
        el otro (numero secuencial que pone la BD automaticamente al dar el alta. """

        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')

        if self.clave == "":
            self.set_status("✔ No hay nada seleccionado", "ok")
            return

        self.alta_modif = 2

        self.habilitar_text('normal')
        self.limpiar_text()

        # --------------------------------------------
        """ para que permanezca mostrandose el filtro de busqueda actual luego de modificar el articulo que sea. 
        Por ejemplo: busco el cArtucho 133 y me muestra 10 registros, modifico uno de ellos y vuelvo al grid con 
        los mismo 10 aun seleccionados y filtrados"""

        self.filtro_edicion = "articulos WHERE Id = " + str(self.clave)
        valores = self.varArtic.consultar_articulo(self.filtro_edicion)
        # ---------------------------------------------

        for row in valores:

            self.strvar_codigo.set(value=row[1])
            self.strvar_descripcion.set(value=row[2])
            self.combo_marca.insert(0, row[3])
            self.combo_rubro.insert(0, row[4])
            self.combo_rubro.configure(state="readonly")
            self.combo_marca.configure(state="readonly")
            self.combo_iva.insert(0, row[7])
            self.combo_iva.configure(state="readonly")
            self.strvar_codbar.set(value=row[5])
            self.strvar_costo_neto_dolar.set(value=row[6])
            self.costo_neto_dolar_comparado.set(value=row[6]) # para ver si se cambio el precio y actualizar la fecha de ult. modif.
            self.strvar_tasa_impint.set(value=row[8])
            self.strvar_tasa_ganancia.set(value=row[9])
            self.strvar_observa.set(value=row[10])

            fecha_convertida = fecha_str_reves_normal(self, datetime.strftime(row[11], "%Y-%m-%d"), False)
            self.strvar_fechaultact.set(value=fecha_convertida)

            self.strvar_costo_historico.set(row[12])
            self.strvar_imagen_Art.set(value=row[13])

        # Recarga la imagen del producto
        self.recarga_imagen()

        self.habilitar_Btn_Final("normal")
        self.habilitar_Btn_Oper("disabled")

        # funcion que calcula los totales
        self.calcular('completo')
        self.entry_codigo.focus()

    def fEliminar(self):

        # selecciono el Id del GRID para su uso posterior
        self.selected = self.grid_articulos.focus()
        self.selected_ant = self.grid_articulos.prev(self.selected)
        # guardo en clave el Id pero de la Tabla (no son el mismo que el grid
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.clave_ant = self.grid_articulos.item(self.selected_ant, 'text')

        if self.clave == "":
            self.set_status("✔ No hay nada seleccionado", "ok")
            return

        # guardo todos los valores en una lista desde el Tv
        valores = self.grid_articulos.item(self.selected, 'values')
        data = "Id: "+str(self.clave)+" Nº: "+valores[0]+" Articulo: " + valores[4]

        r = messagebox.askquestion("Cuidado", "Confirma eliminar esta Orden?\n " + data, parent=self)
        if r == messagebox.NO:
            self.set_status("ℹ Eliminaion cancelada", "info")
            return

        try:
            self.varArtic.eliminar_articulo(self.clave)
        except Exception as e:
            messagebox.showerror("Error del sistema - al eliminar articulo", str(e))
            # self.set_status("❌ Error al eliminar", "error")
            return
        else:
            self.set_status("🗑 Registro eliminado correctamente", "ok")

        self.llena_grilla(self.clave_ant)

    def fGuardar(self):

        # VALIDACIONES -----------------------------------------------------------------------
        # 1 - Debe existir una descripcion-codigo de articulo
        if self.strvar_descripcion.get() == "":
            self.set_status("⚠ Campos obligatorio Descripcion", "warn")
            self.entry_descripcion.focus()
            return
        if self.strvar_codigo.get() == "":
            self.set_status("⚠ Campos obligatorio Codigo", "warn")
            self.entry_descripcion.focus()
            return
        estado = self.estado_numero(self.strvar_costo_neto_dolar)
        if estado == "vacio" or estado == "cero":
            self.set_status("⚠ Coloque costo del articulo", "warn")
            self.entry_costo_neto_dolar.focus()
            return
        elif estado == "invalido":
            messagebox.showerror("Error", "El valor ingresado no es válido")
            return
        # ------------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------------
        # guardo el Id del Treeview en selected para ubicacion del foco a posteriori (I001, I002....
        self.selected = self.grid_articulos.focus()
        # Guardo Id del registro de la base datos _Tabla (no es el mismo del otro, este puedo verlo en la tabla) 1,2,3..
        self.clave = self.grid_articulos.item(self.selected, 'text')
        # ------------------------------------------------------------------------------------

        # Calculo campos necesarios ----------------------------------------------------------
        if self.alta_modif == 1:
            self.fecha_aux = datetime.strptime(self.strvar_fechaultact.get(), '%d/%m/%Y')
        if self.alta_modif == 2:
            # Verifico que no haya cambiado el costo neto del dolar articulo, si es asi, cambio fecha de ultima modificacion
            if float(self.costo_neto_dolar_comparado.get()) != float(self.strvar_costo_neto_dolar.get()):
                self.fecha_aux = datetime.today()
            else:
                self.fecha_aux = datetime.strptime(self.strvar_fechaultact.get(), '%d/%m/%Y')
        # ------------------------------------------------------------------------------------

        # Preparo Diccionario ----------------------------------------------------------------
        articulos = {
            #"Id": self.var_Id,
            "Id": self.clave,
            "codigo": self.strvar_codigo.get(),
            "descripcion": self.strvar_descripcion.get(),
            "marca": self.combo_marca.get(),
            "rubro": self.combo_rubro.get(),
            "codbar": self.strvar_codbar.get(),
            "costodolar": self.strvar_costo_neto_dolar.get(),
            "iva": self.combo_iva.get(),
            "impint": self.strvar_tasa_impint.get(),
            "porcgan": self.strvar_tasa_ganancia.get(),
            "observa": self.strvar_observa.get(),
            "ultact": self.fecha_aux,
            "costohist": self.strvar_costo_historico.get(),
            "imagen": self.strvar_imagen_Art.get(),
        }
        # ------------------------------------------------------------------------------------

        # Ingreso datos a las tablas - Paso diccionario como parametro -----------------------
        try:
            if self.alta_modif == 1:
                self.id_nuevo = self.varArtic.insertar_articulo(articulos)
                id_ref = self.id_nuevo
            elif self.alta_modif == 2:
                self.varArtic.modificar_articulo(articulos)
                id_ref = self.clave

        # Evaluacion de errores ---------------------------------------------------------------
        except ValueError as e:
            messagebox.showwarning("Datos inválidos - error al insertar/modificar articulo", str(e))
            #self.set_status("⚠ Error en los datos", "warn")
            return
        except Exception as e:
            messagebox.showerror("Error del sistema - al insertar/modificar articulo", str(e))
            #self.set_status("❌ Error al guardar", "error")
            return
        else:
            self.set_status("✔ Registro guardado correctamente", "ok")

        # Terminacion y habilitaciones y seteo variables ---------------------------------------
        self.limpiar_text()
        self.habilitar_Btn_Final("disabled")
        self.habilitar_Btn_Oper("normal")

        self.filtro_activo = "ORDER BY rubro, marca, descripcion ASC"

        self.llena_grilla(id_ref)

        self.alta_modif = 0
        self.habilitar_text("disabled")

    # -----------------------------------------------------------------
    # VARIAS -*-
    # -----------------------------------------------------------------

    def fBusco_archivo(self):

        """ Esta funcion abre un dialogo para poder seleccionar el archivo imagen de articulo en el proceso de altas"""

        # self.dev_ruta = self.varArtic.consultar_informa()
        # print(self.dev_ruta)

        self.strvar_ruta_fotos = tk.StringVar(value="")

        print(self.dev_informa)

        for row in self.dev_informa:
            self.strvar_ruta_fotos.set(value=row[27])

        # Abro ventana dialogo en la ruta de las fotos -
        # OJO ESTO DEBERIA IR EN INFORMA
        self.file_ruta = filedialog.askopenfilename(initialdir="C:\\Proyectos_Python\\ABM_Clientes\\fotos",
                                                    title="Seleccione imagen", parent=self.master)
        # Guardo solo el nombre del archivo y no su ruta completa
        solo_nombre_archivo = os.path.basename(self.file_ruta)
        # asigno al stringvar el nombre del archivo - Si no selecciono, retorna
        if not solo_nombre_archivo:
            return
        self.strvar_imagen_Art.set(value=solo_nombre_archivo)

    def fResetrubro(self):
        self.combo_bus_rubro.set("")

    def fResetmarca(self):
        self.combo_bus_marca.set("")

    def formato_fecha(self, pollo):

        """Aqui dentro llamo a la funcion validar fechas para revisar todo sus valores posibles
        le paso la fecha tipo string con barras o sin barras """

        estado_antes = self.strvar_fechaultact.get()

        # FUNCION VALIDA FECCHAS en programa funcion
        retorno_VerFal = valida_fechas(self, self.strvar_fechaultact.get())

        if retorno_VerFal == "":
            self.strvar_fechaultact.set(value=estado_antes)
            self.entry_fechaultact.focus()
            return
        elif retorno_VerFal == "S":
            # esto es control del año y decidio seguir
            self.entry_fechaultact.focus()
        elif retorno_VerFal == "N":
            # esto es error en el año y decidio no seguir
            self.strvar_fechaultact.set(value=estado_antes)
            self.entry_fechaultact.focus()
            return
        elif retorno_VerFal == "BLANCO":
            return
        else:
            self.strvar_fechaultact.set(retorno_VerFal)

    def verif_existe(self):

        """ Verifica que exista codigo de barras en el alta o modificacion del articulo """

        if self.alta_modif == 1 and len(self.entry_codbar.get()) > 0:
            # La condicion deja entrar si es alta y el codigo de barras "NO" esta vacio

            se_busca = self.entry_codbar.get()
            que_busco = "articulos WHERE codbar = '" + se_busca + "'"

            try:
                retorno = self.varArtic.buscar_entabla(que_busco)
            except Exception as e:
                messagebox.showerror("Error del sistema - al buscar articulo", str(e))
                #self.set_status("❌ Error al buscar", "error")
                return

            if retorno != []:
                # Si retorno "NO" esta vacio es que ya existe ese codigo de barras (repetido) retorna y anula el alta.
                self.set_status("❌ Codigo de barras repetido - revise datos ingresados", "error")
                self.strvar_codbar.set(value="")
                self.entry_codbar.focus()
                return

    def limitador(self, entry_text, caract):
        entry_text.set(entry_text.get()[:caract])

    def recarga_imagen(self):

        """ Este lo usa el metodo de modificacion para cargar la imgen al editarlo, Tambien la usa "limpiartext" """

        try:
            # Borro u olvido el label anterior
            self.lbl_imagen_art.forget()
            # Regenero la imgaen del campo imgaen si existe nombre en la tabla, sino va default TAPIZ
            if len(self.strvar_imagen_Art.get()) != 0:
                self.imagen_defa = self.strvar_imagen_Art.get()
            else:
                self.imagen_defa = "tapiz.jpg"

            self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)
            self.lbl_imagen_art = tk.Label(self.sector_imagen, image=self.imagen_art, bg="white", relief="ridge", bd=5)
            self.lbl_imagen_art.bind("<Double-Button-1>", self.amplia_img)
        except:
            self.set_status("❌ Revise nombre de imagen JPG por favor", "error")

        self.lbl_imagen_art.pack(expand=1, side="top", fill="both", pady=2, padx=2)

    def validar_imagen(self):

        """ Cuando doy alta y coloco el nombre de la imagen jpg, valido que exista en la carpeta fotos y ya la cargo
        y muestro """

        # Borro u olvido el label anterior
        self.lbl_imagen_art.forget()

        if len(self.strvar_imagen_Art.get()) != 0:
            self.imagen_defa = self.strvar_imagen_Art.get()
        else:
            self.imagen_defa = "tapiz.jpg"

        try:
            self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)
        except:
            messagebox.showerror("Error", "No existe la imagen", parent=self)

            self.imagen_defa = "tapiz.jpg"

            self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
            self.imagen_art = ImageTk.PhotoImage(self.photoa)

            self.strvar_imagen_Art.set(value="")
            self.entry_imagen_art.focus()

        # muestro la imagen en el frame
        self.lbl_imagen_art = tk.Label(self.sector_imagen, image=self.imagen_art, bg="white", relief="ridge", bd=5)
        self.lbl_imagen_art.pack(expand=1, side="top", fill="both", pady=2, padx=2)

    # def amplia_img(self,koko):
    #
    #     if len(self.strvar_imagen_Art.get()) != 0:
    #
    #         # crear toplevel con imagen grande
    #         self.vent_img = tk.Toplevel(self.master)
    #         self.vent_img.geometry('420x500+1200+200')
    #         self.vent_img.config(bg='white', padx=5, pady=5)
    #         # ayuda_top.resizable(0,0)
    #         self.vent_img.resizable(1, 1)
    #         self.vent_img.title("Imagen ampliada")
    #
    #         self.photo_b = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
    #         self.photo_b = self.photo_b.resize((300, 300), Image.LANCZOS)  # Redimension (Alto, Ancho)
    #         self.imagen_art_b = ImageTk.PhotoImage(self.photo_b)
    #
    #         # muestro la imagen en el frame
    #         self.lbl_im_art_b = tk.Label(self.vent_img, image=self.imagen_art_b, bg="white", relief="ridge", bd=5)
    #
    #         self.lbl_im_art_b.pack(expand=1, side="top", fill="both", pady=2, padx=2)
    #         self.vent_img.grab_set()
    #         self.vent_img.focus_set()
    #
    #         #tk.mainloop()

    def amplia_img(self, event):

        if self.strvar_imagen_Art.get():
            self.vent_img = tk.Toplevel(self.master)
            self.vent_img.geometry('420x500+1200+200')
            self.vent_img.config(bg='white', padx=5, pady=5)
            self.vent_img.resizable(1, 1)
            self.vent_img.title("Imagen ampliada")

            photo = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
            photo = photo.resize((300, 300), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(photo)

            lbl = tk.Label(self.vent_img, image=imagen, bg="white", relief="ridge", bd=5)
            lbl.image = imagen  # mantener referencia
            lbl.pack(expand=1, fill="both", pady=2, padx=2)

            self.vent_img.grab_set()
            self.vent_img.focus_set()

    # -----------------------------------------------------------------
    # BUSQUEDAS -*-
    # -----------------------------------------------------------------

    def fBuscar_en_tabla(self):

        """ strip : 👉 elimina espacios en blanco al inicio y al final"""
        rubro = self.combo_bus_rubro.get().strip()
        marca = self.combo_bus_marca.get().strip()
        se_busca = self.entry_buscar_articulo.get().strip()

        # 🚫 Nada cargado
        if rubro == "" and marca == "" and se_busca == "":
            self.set_status("⚠ No ingreso busqueda o filtro", "warn")
            return

        try:
            condiciones = []

            # 🔹 Filtros por rubro y marca
            if rubro:
                condiciones.append(f"rubro = '{rubro}'")

            if marca:
                condiciones.append(f"marca = '{marca}'")

            # 🔹 Búsqueda por texto
            if se_busca:
                texto_cond = (
                    f"INSTR(descripcion, '{se_busca}') > 0 OR "
                    f"INSTR(codigo, '{se_busca}') > 0 OR "
                    f"INSTR(codbar, '{se_busca}') > 0"
                )
                condiciones.append(f"({texto_cond})")  # 👈 CLAVE: paréntesis

            # 🔹 Armar WHERE
            condicion_unida = " AND ".join(condiciones)

            self.filtro_activo = (
                    "WHERE "
                    + condicion_unida +
                    " ORDER BY rubro, marca, descripcion ASC"
            )

            retorno = self.varArtic.buscar_entabla(self.filtro_activo)
            if retorno == []:
                self.set_status("ℹ No encontre ninguna coincidencia para su busqueda", "info")
                self.entry_buscar_articulo.focus()
                return

            # " " = ir al primero
            self.llena_grilla("")
        except Exception as e:
            self.set_status("❌ Error de busqueda - Revise caracteres no admitidos", "error")
            self.entry_buscar_articulo.focus()

    # -----------------------------------------------------------------
    # CALCULOS -*-
    # -----------------------------------------------------------------

    def calcular(self, que_campo):

        try:
            # Funcion que no permite pasar el valor "" y  controla '-' y '.'
            if not self.control_blanco():
                self.entry_costo_historico.focus()
                return

            # reconstruye valores de variables a cero si es que borran el valor anterior y
            # lo dejan en blanco en vez de cero
            self.control_valores()

            # Verifica que costos no esten en cero, porque sino da error el calculo de precio de venta final (divide zero)
            if que_campo != "nada":
                if float(self.strvar_costo_neto_dolar.get()) == 0 and float(self.strvar_costo_neto_pesos.get()) == 0:
                    messagebox.showwarning("Cuidado", "Debe colocar costo", parent=self)
                    self.entry_costo_neto_dolar.focus()
                    return

            if que_campo == "dolar":
                # Calulo el costo neto en dolar
                x_costo_neto_dolar = float(self.strvar_costo_neto_dolar.get())
                x_valor_dolar_hoy = float(self.strvar_dolar_actual.get())
                #calc_pesos_neto = round((float(self.strvar_costo_neto_dolar.get()) * float(self.strvar_dolar_actual.get())), 2)
                calc_pesos_neto = round((x_costo_neto_dolar * x_valor_dolar_hoy), 2)
                #self.strvar_costo_neto_pesos.set(value=str(round(float(calc_pesos_neto), 2)))
                self.strvar_costo_neto_pesos.set(value=str(round(calc_pesos_neto, 2)))

            elif que_campo == "nada":
                pass

            elif que_campo == "pesos":

                # Calculo el costo en pesos a partir del ingreso de pesos
                x_costo_neto_pesos = float(self.strvar_costo_neto_pesos.get())
                x_valor_dolar_hoy = float(self.strvar_dolar_actual.get())
                x_calc_dolar_neto = round(( x_costo_neto_pesos / x_valor_dolar_hoy ), 2)
                self.strvar_costo_neto_dolar.set(value=str(round(x_calc_dolar_neto, 2)))

            elif que_campo == "iva":

                # Calculo el iva correspondiente segun la tasa seleccionada
                val1 = float(self.combo_iva.get())
                val2 = float(self.strvar_costo_neto_pesos.get())
                self.strvar_total_iva.set(value=str(round(((val1 * val2) / 100), 2)))

            elif que_campo == "impint":

                # Calculo el Impuesto Interno
                val1 = float(self.strvar_tasa_impint.get())
                val2 = float(self.strvar_costo_neto_pesos.get())
                self.strvar_total_impint.set(value=str(round(((val1 * val2) / 100), 2)))

            elif que_campo == "porgan":

                # Calculo el porcentaje de ganancia importe
                val1 = float(self.strvar_tasa_ganancia.get())
                val2 = float(self.strvar_subtotal.get())
                self.strvar_total_ganancia.set(value=str(round(((val1 * val2) / 100), 2)))

            elif que_campo == "totales":

                # Aca es si cambio el total de venta en pesos
                # Debo recalcular el nuevo porc. % de ganancia y el importe de ganancia

                # Nuevo porcentaje ganancias
                x_total_precio_venta = float(self.strvar_total_precio_venta.get())
                x_subtotal = float(self.strvar_subtotal.get())
                val8 = round((((x_total_precio_venta - x_subtotal) * 100) / x_subtotal), 2)
                self.strvar_tasa_ganancia.set(value=str(val8))

                # Ahora recalculo el nuevo importe de la ganancia
                val1 = float(self.strvar_tasa_ganancia.get())
                val2 = float(self.strvar_subtotal.get())
                self.strvar_total_ganancia.set(value=str(round(((val1 * val2) / 100), 2)))

                # calculo el precio de venta con el recargo por venta con tarjeta
                x_calc_total_ventas = float(self.strvar_total_precio_venta.get())
                x_recargo_tarjeta = float(self.strvar_recargo_tarjeta.get())
                x_calc_total_ventas_mas10 = x_calc_total_ventas * ((x_recargo_tarjeta / 100) + 1)
                self.strvar_total_precio_venta_mas10.set(value=str(round(x_calc_total_ventas_mas10, 2)))
                return

            elif que_campo == "limp":

                # limpìa todos los campos al darle cancelar
                self.strvar_total_iva.set(value="0.00")
                self.strvar_subtotal.set(value="0.00")
                self.strvar_total_ganancia.set(value="0.00")
                self.strvar_costo_pesos_bruto.set(value="0.00")
                self.strvar_costo_dolar_bruto.set(value="0.00")
                return

            elif que_campo == "completo":

                # Calculo el costo neto en dolares
                x_costo_neto_dolar = float(self.strvar_costo_neto_dolar.get())
                x_dolar_actual = float(self.strvar_dolar_actual.get())
                x_calc_pesos_neto = round((x_costo_neto_dolar * x_dolar_actual), 2)

                # self.strvar_costo_neto_pesos.set(value=0)
                self.strvar_costo_neto_pesos.set(value=str(x_calc_pesos_neto))

                # Calculo el costo en pesos neto a partir del ingreso de pesos
                x_costo_neto_pesos = float(self.strvar_costo_neto_pesos.get())
                x_dolar_actual = float(self.strvar_dolar_actual.get())
                x_calc_dolar_neto = str(round((x_costo_neto_pesos / x_dolar_actual), 2))

                # self.strvar_costo_neto_dolar.set(value=0)
                self.strvar_costo_neto_dolar.set(value=x_calc_dolar_neto)

                # Calculo el iva correspondiente segun la tasa seleccionada
                val1 = float(self.combo_iva.get())
                val2 = float(self.strvar_costo_neto_pesos.get())
                self.strvar_total_iva.set(value=str(round(((val1 * val2) / 100), 2)))

                # Calculo el Impuesto Interno
                val1 = float(self.strvar_tasa_impint.get())
                val2 = float(self.strvar_costo_neto_pesos.get())
                self.strvar_total_impint.set(value=str(round(((val1 * val2) / 100), 2)))

                # Calculo la ganancia
                x_costo_neto_pesos = float(self.strvar_costo_neto_pesos.get())
                x_total_iva = float(self.strvar_total_iva.get())
                x_total_impint = float(self.strvar_total_impint.get())
                self.strvar_subtotal.set(value=str(round((x_costo_neto_pesos + x_total_iva + x_total_impint), 2)))

                val1 = float(self.strvar_tasa_ganancia.get())
                val2 = float(self.strvar_subtotal.get())
                self.strvar_total_ganancia.set(value=str(round(((val1 * val2) / 100), 2)))

            # Aca se recalculan todos los totales por si se modifica algo
            # Total IVA
            val1 = float(self.combo_iva.get())
            val2 = float(self.strvar_costo_neto_pesos.get())
            self.strvar_total_iva.set(value=str(round(((val1 * val2) / 100), 2)))

            # Subtotal
            x_costo_neto_pesos = float(self.strvar_costo_neto_pesos.get())
            x_total_iva = float(self.strvar_total_iva.get())
            x_total_impint = float(self.strvar_total_impint.get())
            self.strvar_subtotal.set(value=str(round((x_costo_neto_pesos + x_total_iva + x_total_impint), 2)))

            # pesos y dolar bruto con impuestos
            x_subtotal = float(self.strvar_subtotal.get())
            x_dolar_actual = float(self.strvar_dolar_actual.get())
            self.strvar_costo_pesos_bruto.set(value=str(round(x_subtotal, 2)))
            self.strvar_costo_dolar_bruto.set(value=str(round((x_subtotal / x_dolar_actual), 4)))

            # importe pesos de la ganancia
            val1 = float(self.strvar_tasa_ganancia.get())
            val2 = float(self.strvar_subtotal.get())
            self.strvar_total_ganancia.set(value=str(round(((val1 * val2) / 100), 2)))

            # Total venta en pesos con la ganancia incluida
            x_costo_neto_pesos = float(self.strvar_costo_neto_pesos.get())
            x_total_iva = float(self.strvar_total_iva.get())
            x_total_impint = float(self.strvar_total_impint.get())
            x_total_ganancia = float(self.strvar_total_ganancia.get())
            x_calc_total_ventas = round((x_costo_neto_pesos + x_total_iva + x_total_impint + x_total_ganancia), 2)

            self.strvar_total_precio_venta.set(value=str(round(float(x_calc_total_ventas), 2)))

            # calculo el precio de venta con el recargo por venta con tarjeta
            x_recargo_tarjeta = float(self.strvar_recargo_tarjeta.get())
            x_calc_total_ventas_mas10 = x_calc_total_ventas * ((x_recargo_tarjeta / 100) + 1)
            self.strvar_total_precio_venta_mas10.set(value=str(round(float(x_calc_total_ventas_mas10), 2)))
        except:
            self.set_status("❌ Except_error - Revise datos numericos", "error")
            self.entry_costo_historico.focus()
            return

    # -----------------------------------------------------------------
    # VALIDACIONES -*-
    # -----------------------------------------------------------------

    def control_blanco(self):

        """ Controla valores de las variables numericas en cuanto a los '.' y los '-' y los ceros """

        variables = [
            self.strvar_costo_historico,
            self.strvar_costo_neto_dolar,
            self.strvar_costo_neto_pesos,
            self.strvar_tasa_impint,
            self.strvar_tasa_ganancia,
            self.strvar_total_precio_venta,
        ]

        for var in variables:
            valor = var.get()

            # 1. llamo a funcion 'control forma' en (funciones) - Validación de forma
            if not control_forma(valor):
                var.set("0.00")
                return False

            # 2. Casos incompletos
            if valor in ("", "-", ".", "-."):
                var.set("0.00")
                continue

            # 3. Formateo final
            try:
                var.set(f"{float(valor):.2f}")
            except ValueError:
                var.set("0.00")
                return False

        return True

    def control_valores(self):

        """ Controla los valores en blanco o cero y los pone con dos decimales automaticamente"""

        variables = [
            self.strvar_costo_historico,
            self.strvar_costo_neto_dolar,
            self.strvar_costo_neto_pesos,
            self.strvar_tasa_impint,
            self.strvar_tasa_ganancia,
            self.strvar_total_precio_venta,
        ]

        for var in variables:
            self.formatear_strvar(var)

    def formatear_strvar(self, var):
        try:
            var.set(f"{float(var.get()):.2f}")
        except ValueError:
            var.set("0.00")

    # --------------------------------------------------------------------------
    # PUNTEROS -*-
    # --------------------------------------------------------------------------

    def fToparch(self):
        #self.mover_puntero_topend('TOP')
        self.varFuncion_new.mover_puntero_topend(self.grid_articulos, 'TOP')
    def fFinarch(self):
        # self.mover_puntero_topend('END')
        self.varFuncion_new.mover_puntero_topend(self.grid_articulos, 'END')

    def forden_codigo(self):
        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY rubro, marca, descripcion ASC"
        self.llena_grilla(self.clave)

    def forden_descripcion(self):
        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY marca, descripcion ASC"
        self.llena_grilla(self.clave)

    def fQuitarfiltros(self):
        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')
        self.filtro_activo = "ORDER BY rubro, marca, descripcion ASC"
        self.fResetmarca()
        self.fResetrubro()
        self.llena_grilla(self.clave)
        self.btn_nuevo.focus()

    def cuadro_botones1(self):

        for c in range(1):
            self.botones1.grid_columnconfigure(c, weight=1, minsize=140)

        # Nuevo articulo
        icono = self.cargar_icono("archivo-nuevo.png")
        self.btn_nuevo=tk.Button(self.botones1, text=" Nuevo", command=self.fNuevo, bg="blue", fg="white", compound="left")
        self.btn_nuevo.image = icono
        self.btn_nuevo.config(image=icono)
        self.btn_nuevo.grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_nuevo, msg="Ingresar un nuevo articulo")

        # Editar articulo
        icono = self.cargar_icono("editar.png")
        self.btn_editar=tk.Button(self.botones1, text=" Editar", command=self.fEditar, bg="blue", fg="white", compound="left")
        self.btn_editar.image = icono
        self.btn_editar.config(image=icono)
        self.btn_editar.grid(row=1, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_editar, msg="Modificar el articulo seleccionado")

        # Eliminar articulo
        icono = self.cargar_icono("eliminar.png")
        self.btn_eliminar=tk.Button(self.botones1, text=" Eliminar", command=self.fEliminar, bg="red", fg="white", compound="left")
        self.btn_eliminar.image = icono
        self.btn_eliminar.config(image=icono)
        self.btn_eliminar.grid(row=2, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_eliminar, msg="Eliminar el articulo seleccionado")

        # Guardar articulo
        icono = self.cargar_icono("guardar.png")
        self.btn_guardar=tk.Button(self.botones1, text=" Guardar", command=self.fGuardar, bg="green", fg="white", compound="left")
        self.btn_guardar.image = icono
        self.btn_guardar.config(image=icono)
        self.btn_guardar.grid(row=3, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_guardar, msg="Guarda el articulo")

        # Cancelar
        icono = self.cargar_icono("cancelar.png")
        self.btn_cancelar=tk.Button(self.botones1, text=" Cancelar", command=self.fCancelar, bg="black", fg="white", compound="left")
        self.btn_cancelar.image = icono
        self.btn_cancelar.config(image=icono)
        self.btn_cancelar.grid(row=4, column=0, padx=5, pady=3, ipadx=10)
        ToolTip(self.btn_cancelar, msg="Cancela lo que se esta haciendo")

        # reordenamiento de self.frame_botones_grid
        for widg in self.botones1.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def cuadro_botones2(self):

        for c in range(1):
            self.botones2.grid_columnconfigure(c, weight=1, minsize=140)

        # Cambiar orden
        icono = self.cargar_icono("ordenar.png")
        self.btn_orden_codigo = tk.Button(self.botones2, text="Orden Rubro\nMarca-Descripcion", width=14,
                                       command=self.forden_codigo, bg="grey", fg="white", compound="left")
        self.btn_orden_codigo.image = icono
        self.btn_orden_codigo.config(image=icono)
        self.btn_orden_codigo.grid(row=5, column=0, padx=5, pady=3, ipadx=10)

        # Cambiar orden
        icono = self.cargar_icono("ordenar.png")
        self.btn_orden_apellido = tk.Button(self.botones2, text="Orden\n Marca-Descripcion", width=14,
                                         command=self.forden_descripcion, bg="grey", fg="white", compound="left")
        self.btn_orden_apellido.image = icono
        self.btn_orden_apellido.config(image=icono)
        self.btn_orden_apellido.grid(row=6, column=0, padx=5, pady=3, ipadx=10)

        # Cambiar orden
        icono = self.cargar_icono("reset.png")
        self.btn_reset = tk.Button(self.botones2, text=" Reset", width=14, command=self.fReset, bg="black", fg="white", compound="left")
        self.btn_reset.image = icono
        self.btn_reset.config(image=icono)
        self.btn_reset.grid(row=7, column=0, padx=5, pady=3, ipadx=10)

        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btn_Toparch = tk.Button(self.botones2, text="", image=self.photo4, command=self.fToparch, width=15, bg="grey",
                                 fg="white")
        self.btn_Toparch.grid(row=8, column=0, padx=5, pady=3, sticky="nsew")

        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btn_Finarch = tk.Button(self.botones2, text="", image=self.photo5, command=self.fFinarch, bg="grey", fg="white")
        self.btn_Finarch.grid(row=9, column=0, padx=5, pady=3, sticky="nsew")

        # reordenamiento de self.frame_botones_grid
        for widg in self.botones2.winfo_children():
            widg.grid_configure(padx=6, pady=3, sticky='nsew')

    def cuadro_botones3(self):

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((50, 40), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=tk.Button(self.botones3, text="Salir", image=self.photo3, command=self.fSalir, bg="yellow",
                             fg="white")
        self.btnSalir.grid(row=10, column=0, padx=5, pady=3, sticky="nsew")

    def cuadro_botones4(self):

        # VALOR DOLAR HOY - Aqui traigo de la tabla informa la cotizacion actual del dolar
        try:
            self.dev_informa = self.varArtic.consultar_informa()
        except Exception as e:
            messagebox.showerror("Error del sistema - al consultar informa", str(e))
            #self.set_status("❌ Error de consulta", "error")
            return

        for row in self.dev_informa:
            self.strvar_dolar_actual.set(value=row[21])
            self.strvar_recargo_tarjeta.set(value=row[23])

        fff = tkFont.Font(family="Arial", size=11, weight="bold")
        self.lbl_cotiza_dolarhoy = tk.Label(self.botones4, text="dolar Hoy:\n " + str(self.strvar_dolar_actual.get()),
                                         font=fff, foreground="BLUE")
        self.lbl_cotiza_dolarhoy.grid(row=12, column=0, padx=5, pady=3, sticky="s")

    def cuadro_buscar_articulo(self):

        # Combos de rubros
        self.strvar_bus_rubro = tk.StringVar(self.frame_buscar)
        self.combo_bus_rubro = ttk.Combobox(self.frame_buscar, textvariable=self.strvar_bus_rubro, state='readonly',
                                            width=20)
        self.combo_bus_rubro['value'] = self.varArtic.combo_input("ru_nombre", "rubros","ru_nombre")
        self.combo_bus_rubro.grid(row=0, column=0, padx=3, pady=1, sticky="w")
        self.btn_reset_rubro=tk.Button(self.frame_buscar, text="Reset", command=self.fResetrubro, width=5, bg='black',
                                    fg='white')
        self.btn_reset_rubro.grid(row=0, column=1, padx=3, pady=1, sticky="w")

        # combo marcas
        self.strvar_bus_marca = tk.StringVar(self.frame_buscar)
        self.combo_bus_marca = ttk.Combobox(self.frame_buscar, textvariable=self.strvar_bus_marca, state='readonly',
                                            width=20)
        self.combo_bus_marca['value'] = self.varArtic.combo_input("ma_nombre", "marcas","ma_nombre")
        self.combo_bus_marca.grid(row=0, column=2, padx=3, pady=1, sticky="w")
        self.btn_reset_marca=tk.Button(self.frame_buscar, text="Reset", command=self.fResetmarca, width=5, bg='black',
                                    fg='white')
        self.btn_reset_marca.grid(row=0, column=3, padx=3, pady=1, sticky="w")

        # buscar un articulo
        self.lbl_buscar_articulo = tk.Label(self.frame_buscar, text="Buscar: ")
        self.lbl_buscar_articulo.grid(row=0, column=4, padx=3, pady=2)
        self.entry_buscar_articulo=tk.Entry(self.frame_buscar, textvariable=self.strvar_buscar_articulo, justify="left",
                                         width=31)
        self.entry_buscar_articulo.grid(row=0, column=5, padx=3, pady=2, sticky="w")
        self.btn_buscar_articulo = tk.Button(self.frame_buscar, text="Filtrar", command=self.fBuscar_en_tabla,
                                          bg="CadetBlue", fg="white", width=18)
        self.btn_buscar_articulo.grid(row=0, column=6, padx=3, pady=2, sticky="nsew")
        self.btn_mostrar_todo=tk.Button(self.frame_buscar, text="Mostrar Todo", command=self.fQuitarfiltros, width=18,
                                     bg='CadetBlue', fg='white')
        self.btn_mostrar_todo.grid(row=0, column=7, padx=3, pady=1, sticky="nsew")

    def cuadro_entrys_generales(self):

        # CODIGO
        self.lbl_codigo = tk.Label(self.sector_entry, text="Codigo: ")
        self.lbl_codigo.grid(row=0, column=0, padx=2, pady=1, sticky="w")
        self.entry_codigo = tk.Entry(self.sector_entry, textvariable=self.strvar_codigo, justify="left", width=30)
        self.entry_codigo.grid(row=0, column=1, padx=2, pady=1, sticky='nsew')
        self.strvar_codigo.trace_add("write", lambda *args: self.limitador(self.strvar_codigo, 30))

        # DESCRIPCION
        self.lbl_descripcion = tk.Label(self.sector_entry, text="Descripcion: ")
        self.lbl_descripcion.grid(row=1, column=0, padx=2, pady=1, sticky="w")
        self.entry_descripcion = tk.Entry(self.sector_entry, textvariable=self.strvar_descripcion, justify="left",
                                       width=40)
        self.entry_descripcion.grid(row=1, column=1, padx=2, pady=1, sticky="w")
        self.strvar_descripcion.trace_add("write", lambda *args: self.limitador(self.strvar_descripcion, 150))

        # MARCA - COMBOBOX
        self.lbl_marca = tk.Label(self.sector_entry, text="Marca: ")
        self.lbl_marca.grid(row=2, column=0, padx=2, pady=1, sticky="w")
        self.combo_marca = ttk.Combobox(self.sector_entry, textvariable=self.strvar_marca, state='readonly', width=40)
        self.combo_marca.grid(row=2, column=1, padx=2, pady=1, sticky="w")
        self.combo_marca['value'] = self.varArtic.combo_input("ma_nombre", "marcas", "ma_nombre")

        # RUBRO - COMBOBOX
        self.lbl_rubro = tk.Label(self.sector_entry, text="Rubro: ")
        self.lbl_rubro.grid(row=3, column=0, padx=2, pady=1, sticky="w")
        self.combo_rubro = ttk.Combobox(self.sector_entry, textvariable=self.strvar_rubro, state='readonly', width=40)
        self.combo_rubro.grid(row=3, column=1, padx=2, pady=1, sticky="w")
        self.combo_rubro['value'] = self.varArtic.combo_input("ru_nombre", "rubros", "ru_nombre")

        # CODIGO DE BARRAS
        self.lbl_codbar = tk.Label(self.sector_entry, text="Codigo Barras: ")
        self.lbl_codbar.grid(row=4, column=0, padx=2, pady=1, sticky="w")
        self.entry_codbar = tk.Entry(self.sector_entry, textvariable=self.strvar_codbar, justify="left", width=30)
        self.entry_codbar.bind('<Tab>', lambda e: self.verif_existe())
        self.entry_codbar.grid(row=4, column=1, padx=2, pady=1, sticky="w")
        self.strvar_codbar.trace_add("write", lambda *args: self.limitador(self.strvar_codbar, 150))

        # OBSERVACIONES
        self.lbl_observa = tk.Label(self.sector_entry, text="Observaciones: ")
        self.lbl_observa.grid(row=5, column=0, padx=2, pady=1, sticky="w")
        self.entry_observa = tk.Entry(self.sector_entry, textvariable=self.strvar_observa, justify="left", width=40)
        self.entry_observa.grid(row=5, column=1, padx=2, pady=1, sticky="w")
        self.strvar_observa.trace_add("write", lambda *args: self.limitador(self.strvar_observa, 40))

        # FECHA DE ULTIMA ACTUALIZACION
        self.lbl_fechaultact = tk.Label(self.sector_entry, text="Fecha ultima Act.: ")
        self.lbl_fechaultact.grid(row=6, column=0, padx=2, pady=1, sticky="w")
        self.entry_fechaultact = tk.Entry(self.sector_entry, textvariable=self.strvar_fechaultact, justify="left",
                                       width=12)
        self.entry_fechaultact.grid(row=6, column=1, padx=2, pady=1, sticky="w")
        self.entry_fechaultact.bind("<FocusOut>", self.formato_fecha)

        # COSTO HISTORICO
        self.lbl_costo_historico = tk.Label(self.sector_entry, text="Costo Historico: ")
        self.lbl_costo_historico.grid(row=7, column=0, padx=2, pady=1, sticky="w")
        self.entry_costo_historico = tk.Entry(self.sector_entry, textvariable=self.strvar_costo_historico, justify="right",
                                           width=15)
        self.entry_costo_historico.grid(row=7, column=1, padx=2, pady=1, sticky="w")
        self.entry_costo_historico.config(validate="key", validatecommand=self.vcmd)
        self.strvar_costo_historico.trace_add("write", lambda *args: self.limitador(self.strvar_costo_historico, 10))
        self.entry_costo_historico.bind('<Tab>', lambda e: self.calcular("nada"))

    def cuadro_sector_totales(self):

        # TOTALES PRECIO ARRTICULO

        # COSTO NETO EN DOLAR
        self.lbl_costo_neto_dolar = tk.Label(self.sector_totales, text="Costo neto U$S:")
        self.lbl_costo_neto_dolar.grid(row=0, column=0, padx=2, pady=1, sticky="w")
        self.entry_costo_neto_dolar = tk.Entry(self.sector_totales, textvariable=self.strvar_costo_neto_dolar,
                                            justify="right", width=15)
        self.entry_costo_neto_dolar.grid(row=0, column=1, padx=2, pady=1, sticky="w")
        self.entry_costo_neto_dolar.config(validate="key", validatecommand=self.vcmd)
        self.strvar_costo_neto_dolar.trace_add("write", lambda *args: self.limitador(self.strvar_costo_neto_dolar, 15))
        self.entry_costo_neto_dolar.bind('<Tab>', lambda e: self.calcular("dolar"))

        # COSTO NETO EN PESOS
        self.lbl_costo_neto_pesos = tk.Label(self.sector_totales, text="Costo neto Pesos:")
        self.lbl_costo_neto_pesos.grid(row=1, column=0, padx=2, pady=1, sticky="w")
        self.entry_costo_neto_pesos = tk.Entry(self.sector_totales, textvariable=self.strvar_costo_neto_pesos,
                                            justify="right", width=15)
        self.entry_costo_neto_pesos.grid(row=1, column=1, padx=2, pady=1, sticky="w")
        self.entry_costo_neto_pesos.config(validate="key", validatecommand=self.vcmd)
        self.strvar_costo_neto_pesos.trace_add("write", lambda *args: self.limitador(self.strvar_costo_neto_pesos, 15))
        self.entry_costo_neto_pesos.bind('<Tab>', lambda e: self.calcular("pesos"))

        # ALICUOTA TASA IVA y  TOTAL IVA
        self.lbl_tasa_iva = tk.Label(self.sector_totales, text="% IVA:")
        self.lbl_tasa_iva.grid(row=2, column=0, padx=2, pady=1, sticky="w")
        self.combo_iva = ttk.Combobox(self.sector_totales, state="readonly", width=5)
        self.combo_iva['value'] = self.varArtic.combo_input("iva_alic", "alic_iva", "iva_alic")
        self.combo_iva.grid(row=2, column=1, padx=2, pady=1, sticky="w")
        self.strvar_total_iva.set(value="0.00")
        self.lbl_total_iva = tk.Label(self.sector_totales, textvariable=self.strvar_total_iva, width=10, anchor='e')
        self.lbl_total_iva.grid(row=2, column=2, padx=2, pady=1, sticky='nsew')
        self.combo_iva.bind('<Tab>', lambda e: self.calcular("iva"))

        # TASA IMPUESTOS INTERNOS
        self.lbl_impint = tk.Label(self.sector_totales, text="% Imp.Interno:")
        self.lbl_impint.grid(row=3, column=0, padx=2, pady=1, sticky="w")
        self.strvar_tasa_impint.set(value="0.00")
        self.strvar_total_impint.set(value="0.00")
        self.entry_tasa_impint = tk.Entry(self.sector_totales, textvariable=self.strvar_tasa_impint, width=5,
                                       justify="right")
        self.entry_tasa_impint.grid(row=3, column=1, padx=2, pady=1, sticky="w")
        self.entry_tasa_impint.config(validate="key", validatecommand=self.vcmd)
        self.strvar_tasa_impint.trace_add("write", lambda *args: self.limitador(self.strvar_tasa_impint, 5))

        self.lbl_total_impint = tk.Label(self.sector_totales, textvariable=self.strvar_total_impint, width=10, anchor='e')
        self.lbl_total_impint.grid(row=3, column=2, padx=2, pady=1, sticky='nsew')
        self.entry_tasa_impint.bind('<Tab>', lambda e: self.calcular("impint"))

        # SUBTOTAL COSTO CON IMPUESTOS ( BRUTO )
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.lbl_subtotal = tk.Label(self.sector_totales, text="SubTotal:", font=fff, fg='green')
        self.lbl_subtotal.grid(row=5, column=1, padx=2, pady=1, sticky="w")
        self.strvar_subtotal.set(value="0.00")
        self.lbl_importe_subtotal = tk.Label(self.sector_totales, textvariable=self.strvar_subtotal, fg='green', width=10,
                                          anchor='e')
        self.lbl_importe_subtotal.grid(row=5, column=2, padx=2, pady=1, sticky='nsew')
        # PORCIENTO GANANCIA
        self.lbl_tasa_ganancia = tk.Label(self.sector_totales, text="% Ganancia:")
        self.lbl_tasa_ganancia.grid(row=6, column=0, padx=2, pady=1, sticky="w")
        self.strvar_tasa_ganancia.set(value="0.00")
        self.strvar_total_ganancia.set(value="0.00")
        self.entry_tasa_ganancia = tk.Entry(self.sector_totales, textvariable=self.strvar_tasa_ganancia, width=8,
                                         justify="right")
        self.entry_tasa_ganancia.grid(row=6, column=1, padx=2, pady=1, sticky="w")
        self.entry_tasa_ganancia.config(validate="key", validatecommand=self.vcmd)
        self.strvar_tasa_ganancia.trace_add("write", lambda *args: self.limitador(self.strvar_tasa_ganancia, 6))
        self.lbl_total_ganancia = tk.Label(self.sector_totales, textvariable=self.strvar_total_ganancia, width=10,
                                        anchor='e')
        self.lbl_total_ganancia.grid(row=6, column=2, padx=2, pady=1, sticky='nsew')
        self.entry_tasa_ganancia.bind('<Tab>', lambda e: self.calcular("porgan"))
        # TOTAL PRECIO DE VENTA PESOS ARTICULO
        fff = tkFont.Font(family="Arial", size=9, weight="bold")
        lbl_total_venta = tk.Label(self.sector_totales, font=fff, text="Precio Venta: ", fg="blue")
        lbl_total_venta.grid(row=7, column=0, padx=2, pady=1, sticky="w")
        self.entry_total_precio_venta = tk.Entry(self.sector_totales, textvariable=self.strvar_total_precio_venta,
                                              width=20, justify="right")
        self.entry_total_precio_venta.grid(row=7, column=2, padx=2, pady=1, sticky='nsew')
        self.entry_total_precio_venta.config(validate="key", validatecommand=self.vcmd)
        self.strvar_total_precio_venta.trace_add("write", lambda *args: self.limitador(self.strvar_total_precio_venta, 10))
        self.entry_total_precio_venta.bind('<Tab>', lambda e: self.calcular("totales"))
        fff = tkFont.Font(family="Arial", size=11, weight="bold")
        lbl_total_venta_grande = tk.Label(self.sector_totales, font=fff, textvariable=self.strvar_total_precio_venta,
                                       fg="red")
        lbl_total_venta_grande.grid(row=8, column=0, padx=2, pady=1, sticky='nsew')
        # Total de venta mas el % de recargo por la venta con tarjeta
        lbl_total_venta_mas10 = tk.Label(self.sector_totales, text="Tarjeta +10%: ", fg="blue")
        lbl_total_venta_mas10.grid(row=8, column=1, padx=2, pady=1, sticky="w")
        lbl_total_venta_grande_mas10 = tk.Label(self.sector_totales, font=fff,
                                             textvariable=self.strvar_total_precio_venta_mas10, fg="red")
        lbl_total_venta_grande_mas10.grid(row=8, column=2, padx=2, pady=1, sticky="w")

        # COSTO DOLAR CON IMPUESTOS BRUTO
        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        self.strvar_costo_dolar_bruto.set(value="0.00")
        self.lbltot_costo_dolar_bruto = tk.Label(self.sector_totales, textvariable=self.strvar_costo_dolar_bruto, width=10,
                                              font=fff, fg='blue', anchor='e')
        self.lbltot_costo_dolar_bruto.grid(row=0, column=2, padx=2, pady=1, sticky='nsew')

        self.lbl_aclaracion1 = tk.Label(self.sector_totales, text="c/Iva", fg='blue')
        self.lbl_aclaracion1.grid(row=0, column=3, padx=2, pady=1, sticky='nsew')

        # COSTO PESOS CON IMPUESTOS BRUTO
        self.strvar_costo_pesos_bruto.set(value="0.00")
        self.lbltot_costo_pesos_bruto = tk.Label(self.sector_totales, textvariable=self.strvar_costo_pesos_bruto, width=10,
                                              font=fff, fg='blue', anchor='e')
        self.lbltot_costo_pesos_bruto.grid(row=1, column=2, padx=2, pady=1, sticky='nsew')

        self.lbl_aclaracion2 = tk.Label(self.sector_totales, text="c/Iva", fg='blue')
        self.lbl_aclaracion2.grid(row=1, column=3, padx=2, pady=1, sticky='nsew')

    def cuadro_imagenes_articulos(self):

        # NOMBRE DEL ARCHIVO, NO GUARDA LA RUTA
        self.entry_imagen_art = tk.Entry(self.sector_imagen, textvariable=self.strvar_imagen_Art, width=25)
        self.entry_imagen_art.bind('<Tab>', lambda e: self.validar_imagen())

        # BOTON FILE DIALOGO (BUSQUEDA DE ARCHIVO) VA A CARPETA FOTOS OR DEFAULT
        self.btn_ruta_imagen=tk.Button(self.sector_imagen, text="Seleccione archivo", command=self.fBusco_archivo,
                                    width=20, bg='blue', fg='white')

        # MUESTRA DE LA IMAGEN
        # Viene en self.imagen.defa - "tapiz.jpg" por default definida en variables generales arriba
        self.photoa = Image.open(os.path.join(self.carpeta_fotos, self.imagen_defa))
        self.photoa = self.photoa.resize((100, 100), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.imagen_art = ImageTk.PhotoImage(self.photoa)

        # MUESTRO LA IMAGEN EN EL FRAME
        self.lbl_imagen_art = tk.Label(self.sector_imagen, image=self.imagen_art, bg="white", relief="ridge", bd=5)
        self.lbl_imagen_art.bind("<Double-Button-1>", self.amplia_img)

    def cuadro_grid_articulos(self):

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tv)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_articulos = ttk.Treeview(self.frame_tv, height=11, columns=("col1", "col2", "col3", "col4", "col5",
                                                                              "col6", "col7", "col8", "col9", "col10",
                                                                              "col11", "col12"))

        self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)
        #self.grid_articulos.bind("<ButtonRelease-3>", self.muestradatos)

        self.grid_articulos.column("#0", width=60, anchor="center", minwidth=60)
        self.grid_articulos.column("col1", width=100, anchor="w", minwidth=100)
        self.grid_articulos.column("col2", width=350, anchor="w", minwidth=350)
        self.grid_articulos.column("col3", width=110, anchor="center", minwidth=110)
        self.grid_articulos.column("col4", width=130, anchor="center", minwidth=130)
        self.grid_articulos.column("col5", width=80, anchor="e", minwidth=80)
        self.grid_articulos.column("col6", width=70, anchor="e", minwidth=70)
        self.grid_articulos.column("col7", width=100, anchor="center", minwidth=100)
        self.grid_articulos.column("col8", width=70, anchor="center", minwidth=70)
        self.grid_articulos.column("col9", width=60, anchor="center", minwidth=60)
        self.grid_articulos.column("col10", width=200, anchor="center", minwidth=200)
        self.grid_articulos.column("col11", width=100, anchor="center", minwidth=100)
        self.grid_articulos.column("col12", width=80, anchor="center", minwidth=80)

        self.grid_articulos.heading("#0", text="Id", anchor="center")
        self.grid_articulos.heading("col1", text="Codigo", anchor="w")
        self.grid_articulos.heading("col2", text="Descripcion", anchor="w")
        self.grid_articulos.heading("col3", text="Marca", anchor="center")
        self.grid_articulos.heading("col4", text="Rubro", anchor="center")
        self.grid_articulos.heading("col5", text="Pesos final", anchor="center")
        self.grid_articulos.heading("col6", text="Dolar neto", anchor="center")
        self.grid_articulos.heading("col7", text="Cod.Barras", anchor="center")
        self.grid_articulos.heading("col8", text="IVA", anchor="center")
        self.grid_articulos.heading("col9", text="% Ganancia", anchor="center")
        self.grid_articulos.heading("col10", text="Observaciones", anchor="w")
        self.grid_articulos.heading("col11", text="Fecha ultima Act.", anchor="center")
        self.grid_articulos.heading("col12", text="Costo Historico", anchor="center")

        self.grid_articulos.tag_configure('oddrow', background='light grey')
        self.grid_articulos.tag_configure('evenrow', background='white')

        # SCROLLBAR del Treeview
        scroll_x = tk.Scrollbar(self.frame_tv, orient="horizontal")
        scroll_y = tk.Scrollbar(self.frame_tv, orient="vertical")
        self.grid_articulos.config(xscrollcommand=scroll_x.set)
        self.grid_articulos.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_articulos.xview)
        scroll_y.config(command=self.grid_articulos.yview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.grid_articulos['selectmode'] = 'browse'

        # PACK - de el treeview y el FRAME tv
        self. grid_articulos.pack(side= "top", fill="both", expand=1, padx=5, pady=5)

    # GPT |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    """ Esta funcion muestra en una barra de estado al pie de la pantalla un mensaje indicando el 
    resultado de una operacion"""
    def set_status(self, mensaje, tipo="info", tiempo=4000):

        # 🎨 colores según tipo
        colores = {
            "ok": ("#d4edda", "#155724"),    # verde claro / texto oscuro
            "error": ("#f8d7da", "#721c24"), # rojo
            "warn": ("#fff3cd", "#856404"),  # amarillo
            "info": ("#d1ecf1", "#0c5460")   # celeste
        }

        bg, fg = colores.get(tipo, ("#f0f0f0", "black"))

        # seteo visual
        self.status_var.set("  " + mensaje)
        self.status_bar.config(bg=bg, fg=fg)

        # 🔊 SONIDOS
        if sys.platform.startswith("win"):
            import winsound

            if tipo == "ok":
                winsound.MessageBeep(winsound.MB_OK)
            elif tipo == "error":
                winsound.MessageBeep(winsound.MB_ICONHAND)
            elif tipo == "warn":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif tipo == "info":
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            # fallback (Linux / otros)
            if tipo == "error":
                self.bell()
                self.after(120, self.bell)
            elif tipo == "warn":
                self.bell()
            elif tipo == "ok":
                self.bell()

        self.after(tiempo, self.clear_status)

    def clear_status(self):
        self.status_var.set("")
        self.status_bar.config(bg="#f0f0f0", fg="black")


        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
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

    def estado_numero(self, strvar):
        valor = strvar.get().strip()
        if valor == "":
            return "vacio"
        try:
            if float(valor) == 0:
                return "cero"
            else:
                return "valor"
        except ValueError:
            return "invalido"

    # GPT |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    def cargar_icono(self, path, size=(18,18)):
        img = Image.open(path).resize(size)
        return ImageTk.PhotoImage(img)
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
