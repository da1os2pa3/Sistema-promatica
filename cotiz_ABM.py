import mysql.connector
from mysql.connector import Error

class datosCotiz:

    def __init__(self):
        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):

        datos = self.consultar_articulo()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consultar_articulo(self, tofil):
        cur = self.cnn.cursor()

        if tofil == "":
            cur.execute("SELECT * FROM " + tofil)
        else:
            cur.execute("SELECT * FROM " + tofil)

        # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
        """ cursor.fetchall()recupera todas las filas del resultado de una consulta. Devuelve todas
        # las filas como una "lista". Se devuelve una lista vacía si no hay ningún registro para recuperar.
        # cursor.fetchmany(size)devuelve el número de filas especificadas por size el argumento. Cuando
        # se llama repetidamente, este método recupera el siguiente conjunto de filas del resultado de una
        # consulta y devuelve una lista de tuplas. Si no hay más filas disponibles, devuelve una lista vacía.
        # cursor.fetchone()El método devuelve un solo registro o Ninguno si no hay más filas disponibles. """
        # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def consultar_articulo_item_vta(self, tofil):
        cur = self.cnn.cursor()

        if tofil == "":
            cur.execute("SELECT * FROM " + tofil)
        else:
            cur.execute("SELECT * FROM " + tofil)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def consultar_detalle_auxventas(self, tofil):

        cur = self.cnn.cursor()

        if tofil == "":
            cur.execute("SELECT * FROM " + tofil)
        else:
            cur.execute("SELECT * FROM " + tofil)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def vaciar_auxventas(self, tofil):

        cur = self.cnn.cursor()
        cur.execute("DELETE FROM " + tofil)
        self.cnn.commit()
        cur.close()
        return

    def buscar_entabla(self, argumento):
        # Busca un strin en los campos indicados en una tabla

        cur = self.cnn.cursor()
        if len(argumento) > 0:
            cur.execute("SELECT * FROM " + argumento)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def traer_ultimo(self):

        # Trae el ultimo codigo de cliente en la tabla para proponer el nuevo numero en alta -----------------------

        cur = self.cnn.cursor()
        cur.execute("SELECT * FROM resu_ventas ORDER BY rv_numero ASC")
        datos = cur.fetchall()
        aux = ""
        for row in datos:
            aux = str(row[1]) + "\n"
        self.cnn.commit()
        cur.close()
        if aux == "":
            aux = 0

        return aux

    def consultar_informa(self):
        cur = self.cnn.cursor()

        cur.execute("SELECT * FROM informa WHERE 1")

        datos_inf = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos_inf

    def insertar_auxventa(self, codart, descart, marcaart, cantidad, total_pesos, total_neto, imporiva21, imporiva105,
                          imporganancia, costobruto, costodolar, tasaiva):

        cur = self.cnn.cursor()

        sql = '''INSERT INTO aux_ventas (av_codigo_art, av_desc_art, av_marca_art, av_cantidad, av_total_pesos, av_netoventa, 
                                         av_impor_iva21, av_impor_iva105,    
                                         av_impor_ganancia, av_costo_bruto, av_costo_dolar, av_tasaiva) VALUES('{}',
                                         '{}','{}', '{}','{}', '{}','{}','{}','{}','{}','{}','{}')'''.format(codart,
                                         descart, marcaart, cantidad, total_pesos, total_neto, imporiva21, imporiva105,
                                         imporganancia, costobruto, costodolar, tasaiva)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def insertar_resuventa(self, nroventa, fechavta, codcli, nomcli, sitfis, cuit, tipopago, detapago, dolarhoy, totalventa):

        # Inserta en la tabla de resumen de ventas realizadas el registro con los datos base de la venta
        cur = self.cnn.cursor()

        sql = '''INSERT INTO resu_ventas (rv_numero, rv_fecha, rv_cod_cliente, rv_cliente, rv_sitfis, rv_cuit,
        rv_tipo_pago, rv_detalle_pago, rv_dolarhoy, rv_total) VALUES('{}','{}','{}','{}', '{}', '{}','{}','{}',
        '{}', '{}')'''.format(nroventa, fechavta, codcli, nomcli, sitfis, cuit, tipopago, detapago, dolarhoy, totalventa)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def insertar_detaventa(self, nroventa, codigoart, nombreart, marcaart, cantidad, finalventa, netoventa,
                           imporiva21, imporiva105,imporganan, costodolar, costobruto, tasaiva):

        # Inserta los articulos vendidos en la tabla de detalle de las ventas realizadas

        cur = self.cnn.cursor()

        sql = '''INSERT INTO deta_ventas (dv_numero, dv_codigo_art, dv_desc_art, dv_marca_art, dv_cantidad, dv_final_venta, 
                                          dv_neto_venta, dv_impor_iva21, dv_impor_iva105, 
                                          dv_impor_ganancia, dv_costo_dolar, dv_costo_bruto, dv_tasaiva) VALUES('{}','{}',
                                          '{}','{}','{}', '{}','{}', '{}','{}','{}','{}','{}','{}')'''.format(nroventa,
                                          codigoart, nombreart, marcaart, cantidad, finalventa, netoventa, imporiva21,
                                          imporiva105, imporganan, costodolar, costobruto, tasaiva)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def traer_resu_venta(self,nroventa):
        cur = self.cnn.cursor()

        cur.execute("SELECT * FROM resu_ventas WHERE rv_numero = " + nroventa)

        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchone()
        self.cnn.commit()
        cur.close()
        return datos

    def traer_deta_venta(self,nroventa):
        cur = self.cnn.cursor()

        cur.execute("SELECT * FROM deta_ventas WHERE dv_numero = " + nroventa)

        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def eliminar_auxventa(self, Id):
        cur = self.cnn.cursor()
        sql = '''DELETE FROM aux_ventas WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_resuventa(self, Id):
        cur = self.cnn.cursor()
        sql = '''DELETE FROM resu_ventas WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_resuventa2(self, nroventa):
        cur = self.cnn.cursor()
        sql = '''DELETE FROM resu_ventas WHERE rv_numero = {}'''.format(nroventa)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_detaventa(self, nroventa):
        cur = self.cnn.cursor()
        sql = '''DELETE FROM deta_ventas WHERE dv_numero = {}'''.format(nroventa)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n


    # -----------------------------------------------------------------------------------------------
    # ------------------- METODOS DE USO GENERAL ----------------------------------------------------
    # -----------------------------------------------------------------------------------------------


    # Llenar un combobox con datos xe una tabla
    def combo_input(self, xcampo, xtabla, xorden):
#        cnn = mysql.connector.connect(host="localhost", user="root", passwd="", db="sist_prom")
        cur = self.cnn.cursor()
        cur.execute("SELECT " + xcampo + " FROM " + xtabla + " ORDER BY " + xorden)
        result = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return result

