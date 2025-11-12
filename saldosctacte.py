"""
# ============================ WIDGETS
# ============================ STRINGVARS
# ============================ TREEVIEW
# ============================ PANTALLA (GRILLA - LIMPIAR - BOTONES ON OFF .....)
# ============================ MOVIMIENTO EN TREEVIEW
# ============================ IMPRESION
# ========================================================================================================
# FUNCIONES METODOS ======================================================================================
# ========================================================================================================
# ---------------------------------------- PANTALLA - WIDGETS - TREEVIEW
# def llena_grilla(self):
# ---------------------------------------- STRINGVARS
# ---------------------------------------- CRUD
# def fSalir(self):
# --------------------------------------- MOVIMIENTOS ARCHIVO
# def fToparch(self):
# def fFinarch(self):
# def mover_puntero(self, param_topend):
# def puntabla(self, registro, tipo_mov):
# --------------------------------------- BUSQUEDAS
# --------------------------------------- VALIDACIONES
# --------------------------------------- IMPRESION
# def fImprime(self):
# ========================================================================================================
"""

import os
from PDF_clase import *
from tkinter import *
from tkinter import ttk
from saldosctacte_ABM import *
from tkinter import messagebox
#from datetime import date, datetime
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkFont

class Saldosctacte(Frame):

    # Creo la clase - clase definida en cotiz_ABM.py
    varSaldoscc = datosSaldosctacte()

    def __init__(self, master=None):
        super().__init__(master, width=880, height=510)
        self.master = master

        self.master.grab_set()
        self.master.focus_set()

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        #master.geometry("880x510")
        self.master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # ------ Obtenemos el largo y  ancho de la pantalla
        wtotal = self.master.winfo_screenwidth()
        htotal = self.master.winfo_screenheight()
        # ------ Guardamos el largo y alto de la ventana
        wventana = 1035
        hventana = 475
        # ------ Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 100
        pheight = round(htotal / 2 - hventana / 2) - 50
        # ------ Se lo aplicamos a la geometría de la ventana
        self.master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # Se usa para saber que filtro esta activo y mantenerlo - a continuacion se setea a un valor inicial
        self.filtro_activo = "saldosctacte ORDER BY scc_nomcli ASC"

        self.create_widgets()
        self.llena_grilla()

    #     # guarda en item el Id del elemento fila en este caso fila 0
    #     item = self.grid_ctacte.identify_row(0)

        """ La función Treeview.selection() retorna una tupla con los ID de los elementos seleccionados o una
        # tupla vacía en caso de no haber ninguno
        # Otras funciones para manejar los elementos seleccionados incluyen:
        # selection_add(): añade elementos a la selección.
        # selection_remove(): remueve elementos de la selección.
        # selection_set(): similar a selection_add(), pero remueve los elementos previamente seleccionados.
        # selection_toggle(): cambia la selección de un elemento. """

    #     self.grid_ctacte.selection_set(item)
    #     # pone el foco en el item seleccionado
    #     self.grid_ctacte.focus(item)
    #     self.habilitar_text("disabled")
    #     self.habilitar_Btn_Final("disabled")
    #     self.habilitar_Btn_busquedas("disabled")
    #     self.habilitar_Selec_cliente("disabled")
    #     self.habilitar_Btn_Oper("disabled")


    # ==================================================================================================
    # ========================================== WIDGETS ===============================================
    # ==================================================================================================


    def create_widgets(self):

        # TITULOS =============================================================================

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        # Armo el logo y el titulo
        self.photocc = Image.open('ctacte.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_ctacte = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_ctacte = Label(self.frame_titulo_top, image=self.png_ctacte, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=52, text="Saldos en cuentas Corrientes",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_ctacte.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")
        self.frame_titulo_top.pack(side=TOP, fill=X, padx=5, pady=2)
        # --------------------------------------------------------------------------

        # VARIABLES GENERALES - =====================================================================
        # Para identificar si el movimiento es alta o modificacion (1 - ALTA 2 - Modificacion)
        self.var_Id = -1
        self.alta_modif = 0


        # =====================================================================================
        # ============================ STRINGVARS =============================================
        # =====================================================================================


        self.strvar_saldo_total =tk.StringVar(value="0.00")


        # ========================================================================================
        # ====================================== TREVIEEW  =======================================
        # ========================================================================================


        # LABELFRAME DEL TREEVIEW ---------------------------------------------------------------------------
        self.frame_tvw_ctacte=LabelFrame(self.master, text="Saldos en Cuentas Corrientes: ", foreground="#CF09BD")

        # STYLE TREEVIEW
        style = ttk.Style(self.frame_tvw_ctacte)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="black", foreground="white")

        self.grid_saldos_ctacte = ttk.Treeview(self.frame_tvw_ctacte, height=14, columns=("col1", "col2", "col3"))

        #self.grid_articulos.bind("<Double-Button-1>", self.DobleClickGrid)

        self.grid_saldos_ctacte.column("#0", width=50, anchor=CENTER, minwidth=50)
        self.grid_saldos_ctacte.column("col1", width=50, anchor=CENTER, minwidth=50)
        self.grid_saldos_ctacte.column("col2", width=300, anchor=CENTER, minwidth=200)
        self.grid_saldos_ctacte.column("col3", width=100, anchor=CENTER, minwidth=80)

        self.grid_saldos_ctacte.heading("#0", text="Id", anchor=CENTER)
        self.grid_saldos_ctacte.heading("col1", text="", anchor=CENTER)
        self.grid_saldos_ctacte.heading("col2", text="Cliente", anchor=CENTER)
        self.grid_saldos_ctacte.heading("col3", text="Saldo", anchor=CENTER)

        # SCROLLBAR del Treeview
        scroll_x = Scrollbar(self.frame_tvw_ctacte, orient=HORIZONTAL)
        scroll_y = Scrollbar(self.frame_tvw_ctacte, orient=VERTICAL)
        self.grid_saldos_ctacte.config(xscrollcommand=scroll_x.set)
        self.grid_saldos_ctacte.config(yscrollcommand=scroll_y.set)
        scroll_x.config(command=self.grid_saldos_ctacte.xview)
        scroll_y.config(command=self.grid_saldos_ctacte.yview)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        self.grid_saldos_ctacte['selectmode'] = 'browse'

        self.grid_saldos_ctacte.pack(side=TOP, fill=BOTH, expand=1, padx=5, pady=2)
        self.frame_tvw_ctacte.pack(side=TOP, fill=BOTH, padx=5, pady=2)

        # Armado de los Frames -------------------------------------------------------------------
        self.frame_primero=LabelFrame(self.master, text="", foreground="red")

        # botones fin y principio archivo -------------------------------------------------------------------
        self.photo4 = Image.open('toparch.png')
        self.photo4 = self.photo4.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo4 = ImageTk.PhotoImage(self.photo4)
        self.btnToparch = Button(self.frame_primero, text="", image=self.photo4, command=self.fToparch, bg="grey", fg="white")
        self.btnToparch.grid(row=0, column=0, padx=5, sticky="nsew", pady=2)
        self.photo5 = Image.open('finarch.png')
        self.photo5 = self.photo5.resize((25, 25), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo5 = ImageTk.PhotoImage(self.photo5)
        self.btnFinarch = Button(self.frame_primero, text="", image=self.photo5, command=self.fFinarch, bg="grey", fg="white")
        self.btnFinarch.grid(row=0, column=1, padx=5, sticky="nsew", pady=2)
        # ---------------------------------------------------------------------------------

        # Boton Imprimir
        self.photo_imp = Image.open('impresora.png')
        self.photo_imp = self.photo_imp.resize((35, 35), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo_imp = ImageTk.PhotoImage(self.photo_imp)
        self.btn_imprime = Button(self.frame_primero, image=self.photo_imp, pady=3, command=self.fImprime, border=3)
        self.btn_imprime.grid(row=0, column=2, padx=4, pady=2)
        #self.btnPlaniCaja.place(x=555, y=10, width=100, height=100)

        self.photo3 = Image.open('salida.png')
        self.photo3 = self.photo3.resize((30, 30), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.photo3 = ImageTk.PhotoImage(self.photo3)
        self.btnSalir=Button(self.frame_primero, text="Salir", image=self.photo3, width=65, command=self.fSalir, bg="yellow", fg="white")
        self.btnSalir.grid(row=0, column=3, padx=5, pady=2, sticky="nsew")

        fff = tkFont.Font(family="Arial", size=10, weight="bold")
        lbl_saldototal = Label(self.frame_primero, text="Saldo total: ", font=fff, justify=LEFT)
        lbl_saldototal.grid(row=0, column=4, padx=4, pady=2)
        lbl_imp_saldototal = Label(self.frame_primero, textvariable=self.strvar_saldo_total, font=fff, justify=RIGHT)
        lbl_imp_saldototal.grid(row=0, column=5, padx=4, pady=2)

        # Cerrado de los Frames PACKS ---------------------------------------------------------------------
        self.frame_primero.pack(side=TOP, fill=BOTH, expand=0, padx=5, pady=2)


    # =============================================================================================
    # ==================================== PANTALLA ===============================================
    # =============================================================================================


    def llena_grilla(self):

        # Tomo la base de ctacte y la ordeno por codigo de cliente ----------------------------------------------
        if len(self.filtro_activo) > 0:
            datos = self.varSaldoscc.consultar_saldosctacte("ctacte ORDER BY cc_codcli ASC")
        else:
            datos = self.varSaldoscc.consultar_saldosctacte("ctacte ORDER BY cc_codcli ASC")

        # eliminar movimientos en tabla auxiliar de saldos "saldosctacte"
        self.varSaldoscc.vaciar_auxsaldos("saldosctacte")

        # Debo realizar un corte de control para calcular los saldos finales para cada cliente ------------------
        # Defino las variables a utilizar en el calculo
        suma_debitos = 0
        suma_creditos = 0
        saldo_total = 0
        antecod = ""
        antecli = ""

        # Tomo solamente el primer elemento que viene en la lista datos para usar en el corte de control --------
        for primer in datos:
            antecod = primer[5]
            antecli = primer[6]
            break

        # Hago el barrido en toda la lista datos, acumulando mientras se repita el codigo de cliente ------------
        for row in datos:

            # aqui provoco el corte de control cuando cambia el codigo de cliente -------------------------------
            if antecod != row[5]:
                # calculo saldo final
                saldofinal = suma_debitos - suma_creditos

                if saldofinal != 0:
                    # inserto el resultado en treeview de saldosctacte
                    self.grid_saldos_ctacte.insert("", END, text=row[0], values=(antecod, antecli, saldofinal))

                    self.varSaldoscc.insertar_saldoctacte(antecod, antecli, saldofinal)

                    saldo_total += saldofinal

                # cargo nuevo cliente para corte de control
                antecod = row[5]
                antecli = row[6]
                # vuelvo a cero los acumuladores
                suma_debitos = 0
                suma_creditos = 0

            # para mismo cliente sumo sus debitos y sus creditos
            suma_debitos += row[3]
            suma_creditos += row[4]

        self.strvar_saldo_total.set(value=saldo_total)

        if len(self.grid_saldos_ctacte.get_children()) > 0:
            self.grid_saldos_ctacte.selection_set(self.grid_saldos_ctacte.get_children()[0])

    def fSalir(self):
        self.master.destroy()


    # # ================================================================================================
    # # ================================= MOVIMIENTO EN TREEVIEW =======================================
    # # ================================================================================================


    def fToparch(self):
        self.mover_puntero('TOP')

    def fFinarch(self):
        self.mover_puntero('END')

    def mover_puntero(self, param_topend):

        # Para ir a tope o fin de archivo -----------------------------------------------------------
        if param_topend == "":
            # Asi obtengo el Id del Grid de donde esta el foco (I006...I002...)
            self.selected = self.grid_saldos_ctacte.focus()
            # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
            # que pone la BD automaticamente al dar el alta
            clave = self.grid_saldos_ctacte.item(self.selected, 'text')

        # Si es tope de archivo ----------------------------------------------------------------------
        if param_topend == 'TOP':

            # obtengo una lista con todos los Id del treeview
            regis = self.grid_saldos_ctacte.get_children()
            # barro y salgo al primero, pero me quedo en el primero
            rg = ""
            for rg in regis:
                break
            if rg == "":
                return
            # selecciono el Id primero de la lista en este caso
            self.grid_saldos_ctacte.selection_set(rg)
            # pongo el foco sobre el primero Id
            self.grid_saldos_ctacte.focus(rg)
            # lleva el foco al principio del treeview con esta instruccion que encontre
            self.grid_saldos_ctacte.yview(self.grid_saldos_ctacte.index(self.grid_saldos_ctacte.get_children()[0]))

        # Si es fin de archivo -----------------------------------------------------------------------
        elif param_topend == 'END':

            # Obtengo una lista con todos los Id del treeview
            regis = self.grid_saldos_ctacte.get_children()
            # Barro la lista y ,me quedo conel ultimo Id
            rg = ""
            for rg in regis:
                pass
            if rg == "":
                return
            # Selecciono el ultimo Id en este caso
            self.grid_saldos_ctacte.selection_set(rg)
            # Pongo el foco alultimo elemento de la lista (al final)
            self.grid_saldos_ctacte.focus(rg)
            # lleva el foco al final del treeview  -------------------------
            self.grid_saldos_ctacte.yview(self.grid_saldos_ctacte.index(self.grid_saldos_ctacte.get_children()[-1]))

    def puntabla(self, registro, tipo_mov):

        # metodo para posicionar el puntero en el TV luego de las distintas acciones sobre los datos

        # trae el indice de la tabla "I001"
        regis = self.grid_saldos_ctacte.get_children()
        rg = ""
        contador = 0
        # --------------------------------------------------------------------------------

        # aca traigo el codigo del registr0 (cod.cliente, cod. art.... que estoy dando de alta porque aun no tengo ID)
        # ALTA
        if tipo_mov == "A":
            for rg in regis:
                buscado = self.grid_saldos_ctacte.item(rg)['values']
                # contador = contador + 1
                # busco el codigo de contrato que ingrese nuevo - Aca busco un campo de la tabla
                # a registro se le paso el nro de contrato en este caso
                if str(buscado[0]) == registro:
                    break
         # ----------------------------------------------------------------------------------------------------

        # Aca es para acomodar el puntero cuando el registro si existe en la tabla, entonces puedo usar el ID
        # MODIFICACION
        if tipo_mov == "B":
            for rg in regis:
                # En buscado guardo el Id de la tabla (base datos) del que estoy posicionado
                buscado = self.grid_saldos_ctacte.item(rg)['text']
                # en registro viene "clave" que es el Id del que estoy parado y lo paso a la funcion como parametro
                contador += 1
                # busco el ID de la tabla con el que guarde antes en "clave" - aca busco un Id de la tabla
                # a registro se le paso el Id de la tabla (es distinto la busqueda a ALTA)
                if buscado == registro:  # 72
                    break
        # -----------------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 1 -es la parte donde tomo el Id del registro que le sigue al que voy a eliminar
        if tipo_mov == 'E':
            control = 1
            self.buscado2 = ""
            for rg in regis:
                contador += 1
                if control == 0:
                    # guardo Id del que sigue
                    buscado = self.grid_saldos_ctacte.item(rg)['values']
                    self.buscado2 = str(buscado[2])
                    break
                if rg == registro:  # registro seria self.selected o sea el Id de la BD
                    control = 0
        # -------------------------------------------------------------------------------------------

        # ELIMINAR REGISTRO PARTE 2 - Aca si ya busco poner el puntero en el Id del que obtuve antes
        # que es el que sigue al que borre
        if tipo_mov == 'F':
            for rg in regis:
                buscado = self.grid_saldos_ctacte.item(rg)['values']
                if self.buscado2 == str(buscado[2]):
                    break
        # ------------------------------------------------------------------------------------------

        # BUSCAR EN TABLA - Viene de la funcion que busca en la tabla lo que se requiere
        if tipo_mov == 'S':
            if regis != ():
                for rg in regis:
                    break
                if rg == "":
                    self.btn_buscar_planilla.configure(state="disabled")
                    return
        # ----------------------------------------------------------------------------------------

        self.grid_saldos_ctacte.selection_set(rg)
        self.grid_saldos_ctacte.focus(rg)
        self.grid_saldos_ctacte.yview(self.grid_saldos_ctacte.index(rg))

        if rg == "":
            return False
        return True


    # =================================================================================================
    # ======================================= IMPRESION ===============================================
    # =================================================================================================


    def fImprime(self):

        # traigo el registro que quiero imprimir
        self.selected = self.grid_saldos_ctacte.focus()
        # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
        # que pone la BD automaticamente al dar el alta
        self.clave = self.grid_saldos_ctacte.item(self.selected, 'text')

        # if self.clave == "":
        #     messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
        #     return

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
        pdf.set_font('Arial', '', 8)
        pdf.cell(w=0, h=5, txt='Saldos en Cuenta Corriente - Fecha y Hora: ' + feac , border=1, align='C', fill=0, ln=1)
        # -----------------------------------------------------------------------------------

        # para listar una base de datos forma simple basica ---------------------------------
        # lista_de_datos = retorno de la base de datos
        # al ultimo le ponemos w=0 y abarca completo el resto del renglon hasta el final

        pdf.cell(w=15, h=8, txt='Cliente', border=1, align='C', fill=0)
        pdf.cell(w=150, h=8, txt='Cliente', border=1, align='C', fill=0)
        pdf.multi_cell(w=0, h=8, txt='Saldo', border=1, align='C', fill=0)
        # pdf.multi_cell(w=0, h=8, txt='Descripcion', border=1, align='C', fill=0)
        pdf.set_font('Arial', '', 5)

        # retorno una lista con los registros ----------------------------------------------------
        datos = self.varSaldoscc.consultar_saldosctacte("saldosctacte")

        pdf.set_font('Arial', '', 11)

        for row in datos:
            pdf.cell(w=15, h=6, txt=str(row[1]), border=1, align='C', fill=0)
            pdf.cell(w=150, h=6, txt=row[2], border=1, align='C', fill=0)
            #pdf.cell(w=20, h=5, txt=row[3], border=1, align='C', fill=0)
            #mostrar = row[4]
            #cadena = (mostrar[:100])
            pdf.multi_cell(w=0, h=6, txt=str(row[3]), border=1, align='R', fill=0)

        pdf.output('hoja.pdf')
        # Abre el archivo PDF para luego, si quiero, poder imprimirlo
        path = 'hoja.pdf'
        os.system(path)
