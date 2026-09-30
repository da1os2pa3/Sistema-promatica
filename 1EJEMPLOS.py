# =================================================================================================
# ================ METODOS POTENCIALES QUE FUI VIENDO Y PUEDEN SER UTILES =========================
# =================================================================================================


""" -----------------------------------------------------------------------
FORMATEAR_CIFRA EN FUNCION
# formatear_cifra en funcion
# numero = total_pesos_mesactual
# salida1 = "{:,.2f}".format(numero)
# salida2 = salida1.replace(',','n')
# salida3 = salida2.replace('.',',')
# salida4 = salida3.replace('n','.')
# total_pesos_mesactual = salida4
# -------------------------------------------------------------------------
"""

# =================================================================================================
# =================================== TABLAS ======================================================
# =================================================================================================



# =================================================================================================
# =================================== FECHAS ======================================================
# =================================================================================================


"""
-------------------------------------------------------------------------------------------------------------
OPERACIONES CON FECHAS
========= primer caso
from datetime import datetime
from datetime import timedelta

ahora = datetime.now()
print("Ahora: " + str(ahora))
hace_una_semana = ahora - timedelta(days=7)
print("Hace una semana: " + str(hace_una_semana))

======== segundo caso
from datetime import datetime
from datetime import timedelta
# Ahora sumar algunas horas. Vamos a parsear la fecha:
fechaCadena = "2020-04-22 00:00:00"
ahora = datetime.strptime(fechaCadena, '%Y-%m-%d %H:%M:%S')
print("Ahora: " + str(ahora))
dentro_de_1_hora = ahora + timedelta(hours=1)
print("Dentro de una hora: " + str(dentro_de_1_hora))

============== tercer caso
Usando dateutil.relativedelta
Hasta ahora hemos operado con horas y con días, pero falta operar con meses o semanas. Lo anteriormente explicado 
solo cubre horas, días y otros, pero no meses (tomando en cuenta años bisiestos y todo eso)
Afortunadamente existe un paquete que podemos instalar con pip:
pip install python-dateutil
Y a partir del mismo ya podemos usar dateutil.relativedelta. Lo importante aquí es saber que siempre vamos a sumar, 
pero que si queremos restar, debemos indicar los parámetros en negativo.

Veamos los ejemplos:

Comienza el uso de relativedelta. Recuerda instalar con:
pip install python-dateutil

dentro_de_un_mes = ahora + relativedelta(months=1)
print("Dentro de un mes: " + str(dentro_de_un_mes))

dentro_de_anio_y_semana = ahora + relativedelta(years=1, weeks=1)
print("Dentro de un año y una semana: " + str(dentro_de_anio_y_semana))

# Sumar pero con negativos, obteniendo una resta

hace_dos_anios = ahora + relativedelta(years=-2)
print("Hace dos años: " + str(hace_dos_anios))
--------------------------------------------------------------------------------------------------------
"""

"""
--------------------------------------------------------------------------------------------------------
# para filtrar tablas por fechas

        # ejemplo de senni --------------------------------------------------------------------
        # self.filtro_activo = "asig_comodatos WHERE CAST(ac_fecha AS date) >= CAST('" + \
        # fecha1 + "' AS date) and CAST(ac_fecha AS date) <= CAST('" + \
        # fecha2 + "' AS date) ORDER BY ac_nro_contrato ASC"
        # -------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
"""



# =================================================================================================
# =================================== TREEVIEW ====================================================
# =================================================================================================


"""
---------------------------------------------------------------------------------------------------------
 Hace que el treeview se posicione en el ultimo registro
self.grid_resumen_ventas.yview((self.grid_resumen_ventas.index(self.grid_resumen_ventas.get_children()[-1])))
---------------------------------------------------------------------------------------------------------
"""










"""
---------------------------------------------------------------------------------------------------------
Metodo para eliminar un registro de una tabla a traves del treeview 

    def fBorrarVenta(self):

        self.selected = self.grid_articulos.focus()
        self.clave = self.grid_articulos.item(self.selected, 'text')
        que_paso = self.puntabla1(self.selected, "E")

        r = messagebox.showwarning("Borrar", "Confirma eliminar venta Nº "+self.strvar_nro_venta.get()
                                   +" de "+self.strvar_nombre_cliente.get())

#        r = messagebox.askquestion("Eliminar", "Confirma eliminar Cliente?\n " + data, parent=self)

        if r == messagebox.YES:
            n = self.varCotiz.eliminar_venta(self.clave)
            if n == 1:
                messagebox.showinfo("Eliminar", "Registro eliminado correctamente", parent=self)
                self.limpiar_Grid()
                self.llena_grilla()
            else:
                messagebox.showinfo("Eliminar", "No fue posible eliminar el Registro", parent=self)

        que_paso = self.puntabla1(self.selected, "F")


    def eliminar_venta(self, Id):
        cur = self.cnn.cursor()

        sql = '''DELETE FROM resu_ventas WHERE Id = {}'''.format(Id)
        cur.execute(sql)

        sql = '''DELETE FROM deta_ventas WHERE Id = {}'''.format(Id)
        cur.execute(sql)

        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

=============================================================================================================
"""




# =================================================================================================
# =================================== FILTROS EN TABLAS ===========================================
# =================================================================================================

"""
========================================================================================================
Metodo donde manejo una busqueda entre dos fechas topes (muy buena)
# ejemplo de senni --------------------------------------------------------------------
# self.filtro_activo = "asig_comodatos WHERE CAST(ac_fecha AS date) >= CAST('" + \
# fecha1 + "' AS date) and CAST(ac_fecha AS date) <= CAST('" + \
# fecha2 + "' AS date) ORDER BY ac_nro_contrato ASC"
========================================================================================================
"""


# ==================================================================================================
# ejemplo de informe pdf
# ==================================================================================================
'''
def creopdf(self):
    # traigo el registro que quiero imprimir de la base datos de ordenes reparacion
    self.selected = self.grid_orden.focus()
    # Asi obtengo la clave de la base de datos campo Id que no es lo mismo que el otro (numero secuencial
    # que pone la BD automaticamente al dar el alta
    self.clave = self.grid_orden.item(self.selected, 'text')

    if self.clave == "":
        messagebox.showwarning("Alerta", "No hay nada seleccionado", parent=self)
    else:
        # Debo traer el registro completo desde la base de datos
        # este metodo de abm_ordenrepar - me trase un solo registro requerido con Id
        datos_registro_selec = self.varOrdenes.traer_un_registro(self.clave)

    # Tambien debo traer los datos de domicilio y telefono delcliente pero desde la tabla de clientes

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
    # salto de hoja automatico
    pdf.set_auto_page_break(auto=True, margin=15)
    # -----------------------------------------------------------------------------------

    # armado de encabezado
    feactual = datetime.now()
    feac = feactual.strftime("%d-%m-%Y %H:%M:%S")
    self.pdf_numero_orden = str(datos_registro_selec[1])
    self.pdf_codigo_cliente = str(datos_registro_selec[4])
    self.pdf_nombre_cliente = datos_registro_selec[5]
    self.pdf_datos_encabezado_orden = self.pdf_numero_orden + ' - ' + self.pdf_nombre_cliente + ' - (' + self.pdf_codigo_cliente + ')'
    # Imprimo el encabezado de pagina con el numero de orden
    pdf.set_font('Arial', '', 8)
    pdf.cell(w=0, h=5,
             txt='Fecha y Hora: ' + feac + '  -  Numero Orden de reparacion ' + self.pdf_datos_encabezado_orden,
             border=1, align='C', fill=0, ln=1)
    # -----------------------------------------------------------------------

    self.pdf_desc = str(datos_registro_selec[6])
    self.pdf_grupo = str(datos_registro_selec[7])
    self.pdf_acces = datos_registro_selec[8]
    self.pdf_estado = datos_registro_selec[9]
    self.pdf_cuenta = datos_registro_selec[10]
    self.pdf_requerido = datos_registro_selec[11]
    self.pdf_diagnostico = datos_registro_selec[12]
    self.pdf_presupuesto = datos_registro_selec[13]
    self.pdf_realizado = datos_registro_selec[14]
    self.pdf_partes = datos_registro_selec[15]
    self.pdf_anotaciones = datos_registro_selec[16]
    self.pdf_totpartes = str(datos_registro_selec[17])
    self.pdf_totmanobra = str(datos_registro_selec[18])
    self.totalpagar = str(datos_registro_selec[17] + datos_registro_selec[18])

    cuerpo_1 = 'Equipo: ' + self.pdf_desc + ' - ' + self.pdf_grupo
    cuerpo_2 = 'Accesorios: ' + self.pdf_acces + ' - Estado del equipo: ' + self.pdf_estado
    cuerpo_3 = 'Cuentas y contraseñas: ' + self.pdf_cuenta
    cuerpo_4 = 'Requerimiento: ' + self.pdf_requerido
    cuerpo_5 = 'Diagnostico: ' + self.pdf_diagnostico
    cuerpo_6 = 'Presupuesto: ' + self.pdf_presupuesto
    cuerpo_7 = 'Trabajo realizado: ' + self.pdf_realizado
    cuerpo_8 = 'Trabajo partes reemplazadas: ' + self.pdf_partes
    cuerpo_9 = 'Trabajo anotaciones: ' + self.pdf_anotaciones
    cuerpo_10 = 'Trabajo Total partes $ : ' + self.pdf_totpartes + \
                ' - Trabajo Total Mano de Obra $: ' + self.pdf_totmanobra + ' - Total a pagar $: ' + self.totalpagar

    # talon cliente ----------------------------------------------
    pdf.multi_cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0)

    # Espaciado entre cuerpos ------------------------------------
    pdf.cell(w=0, h=50, txt='', align='L', fill=0, ln=1)

    # talon interno ----------------------------------------------
    # pdf.cell(w=0, h=5, txt='Orden de reparacion ' + self.pdf_datos_encabezado_orden, border=1, align='C', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_3, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_5, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_6, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_7, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_8, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_9, align='L', fill=0, ln=1)
    # pdf.cell(w=0, h=5, txt=cuerpo_10, align='L', border=1, fill=0, ln=1)
    # #pdf.cell(w=0, h=5, txt=cuerpo_11, align='L', fill=0, ln=1)

    pdf.multi_cell(w=0, h=5, txt='Orden de reparacion ' + self.pdf_datos_encabezado_orden, border=1, align='C', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_1, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_2, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_4, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_3, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_5, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_6, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_7, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_8, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_9, align='L', fill=0)
    pdf.multi_cell(w=0, h=5, txt=cuerpo_10, align='L', border=1, fill=0)

    # -----------------------------------------------------------------------------
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
    """ 
    Para insertar lineas de escritura una debajo de otra
    por ejemplo :
    linea 1
    linea 2
    linea 3

    for i in range(1, 41):
        pdf.cell(0, 10, f'Esta es la linea {i} :D', ln=True)
    """
    # -------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # margenes izq derecha arriba y abajo
    """
    Margen antes de terminar la hoja o sea en tre la ultima linea de la hoja y el fin de la hoja
    pdf.set_auto_page_break(auto=True, margin=15)
    """
    # -------------------------------------------------------------------------------------

    # # para listar una base de datos forma simple basica
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
    #     pdf.multi_cell(w=0, h=5, txt=cadena, border=1, align='E', fill=0)
    #

    pdf.output('hoja.pdf')

    # # Abre el archivo PDF para luego, si quiero, poder imprimirlo
    path = 'hoja.pdf'
    os.system(path)
'''



""" ----------------------------------------------------------------------------------------------------------
    MOSTRAR ERROR
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
----------------------------------------------------------------------------------------------------------
        SET_STATUS
        
        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
        self.set_status("✔ Registro guardado correctamente", "ok")
        self.set_status("🗑 Cliente eliminado", "ok")
        self.set_status("⚠ CUIT incorrecto", "warn")
        self.set_status("❌ Error al guardar", "error")
        self.set_status("ℹ Buscando clientes...", "info")
"""

