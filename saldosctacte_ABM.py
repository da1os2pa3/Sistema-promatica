import mysql.connector
from mysql.connector import Error
from datetime import datetime

class datosSaldosctacte:

    def __init__(self):
        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):
        pass

    def consultar_saldosctacte(self, tofil):

        cur = self.cnn.cursor()
        if tofil == "":
            cur.execute("SELECT * FROM " + tofil)
        else:
            cur.execute("SELECT * FROM " + tofil)
        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchall()
        cur.close()
        return datos

    def insertar_saldoctacte(self, codcliente, nomcliente, saldo):

        cur = self.cnn.cursor()

        sql = ('''INSERT INTO saldosctacte (scc_codcli, scc_nomcli, scc_saldo) VALUES('{}','{}','{}')'''
                                .format(codcliente, nomcliente, saldo))

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def vaciar_auxsaldos(self, tofil):

        cur = self.cnn.cursor()
        cur.execute("DELETE FROM " + tofil)
        self.cnn.commit()
        cur.close()
        return
