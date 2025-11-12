import mysql.connector
from mysql.connector import Error
from datetime import datetime

class datosCompras:

    def __init__(self):

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):

        datos = self.consultar_compras()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consultar_compras(self, tofil):

        cur = self.cnn.cursor()
        if tofil == "":
            cur.execute("SELECT * FROM " + tofil)
        else:
            cur.execute("SELECT * FROM " + tofil)
        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def buscar_entabla(self, argumento):

        # Busca un strin en los campos indicados en una tabla
        cur = self.cnn.cursor()
        if len(argumento) > 0:
            cur.execute("SELECT * FROM " + argumento)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def insertar_registro(self, fecha, articulo, estado):

        algo = fecha
        fecha_ingreso = datetime.strptime(algo, '%d/%m/%Y')

        cur = self.cnn.cursor()

        sql = '''INSERT INTO faltantes (fa_fecha, fa_articulo, fa_estado) VALUES('{}','{}','{}')'''.format(fecha_ingreso,
                                                        articulo, estado)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def modificar_registro(self, Id, fecha, articulo, estado):

        # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
        algo = fecha
        fecha_ingreso = datetime.strptime(algo, '%d/%m/%Y')

        cur = self.cnn.cursor()
        sql = '''UPDATE faltantes SET fa_fecha='{}', fa_articulo='{}', fa_estado='{}' WHERE Id={}'''.format(fecha_ingreso,
                                                articulo, estado, Id)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_articulo(self, Id):
        cur = self.cnn.cursor()
        sql = '''DELETE FROM faltantes WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
