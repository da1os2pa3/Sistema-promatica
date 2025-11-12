import mysql.connector
from mysql.connector import Error
from datetime import datetime

class datosGuiasTecnicas:

    def __init__(self):

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):
        datos = self.consultar_guia()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consultar_guia(self, tofil):

        cur = self.cnn.cursor()
        if tofil == "":
            cur.execute("SELECT * FROM guias_tecnicas ORDER BY gt_clave")
        else:
            cur.execute("SELECT * FROM " + tofil)

        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def buscar_entabla(self, argumento):

        cur = self.cnn.cursor()
        if len(argumento) <= 0:
            return

        cur.execute("SELECT * FROM " + argumento)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def insertar_guia(self, clave, descripcion, ruta, contenido, fotouno, fotodos, fototres, videouno, videodos,
                      videotres):

        cur = self.cnn.cursor()

        sql = '''INSERT INTO guias_tecnicas (gt_clave, gt_brevedesc, gt_ruta, gt_contenido, gt_fotouno, gt_fotodos, 
                                             gt_fototres, gt_videouno, gt_videodos, gt_videotres) VALUES('{}','{}','{}'
                                             ,'{}','{}', '{}','{}','{}','{}','{}')'''.format(clave, descripcion,
                                                                                             ruta, contenido, fotouno,
                                                                                             fotodos, fototres, videouno,
                                                                                             videodos, videotres)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def modificar_guia(self, Id, clave, descripcion, ruta, contenido, fotouno, fotodos, fototres, videouno, videodos,
                       videotres):

        cur = self.cnn.cursor()
        sql = '''UPDATE guias_tecnicas SET gt_clave='{}', gt_brevedesc='{}', gt_ruta='{}', gt_contenido='{}', 
                                           gt_fotouno='{}', gt_fotodos='{}', gt_fototres='{}', gt_videouno='{}', 
                                           gt_videodos='{}', gt_videotres='{}' WHERE Id={}'''.format(clave,
                                                                                              descripcion, ruta, contenido,
                                                                                              fotouno, fotodos, fototres,
                                                                                              videouno, videodos, videotres, Id)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_item_guia(self, Id):

        cur = self.cnn.cursor()
        sql = '''DELETE FROM guias_tecnicas WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
