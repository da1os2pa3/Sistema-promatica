import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import messagebox

class datosRecibos:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_recibos(self,  orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)

        try:
            sql = "SELECT * FROM recibos"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def traer_ultimo(self, xparametro):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM recibos ORDER BY Id DESC LIMIT 1")
            row = cur.fetchone()
            if row is None:
                return 0
            if xparametro == 1:
                return str(row[1])
            else:
                return str(row[0])
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_recibo(self, val_recibo):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            # Convierto formato de fecha
            fecha_convert = datetime.strptime(val_recibo["rc_fecha"], '%d/%m/%Y')

            sql = """
                  INSERT INTO recibos (rc_numero, rc_fecha, rc_codcli, rc_nomcli, rc_importe, rc_concepto) \
                  VALUES (%s, %s, %s, %s, %s, %s) \
                  """

            # Genero una tupla ("valores") con los valores que vienen en el parametro (diccionario)
            valores = (
                val_recibo["rc_numero"],  # de val_recibo, dame su valor
                fecha_convert,
                #val_recibo["rc_fecha"],
                val_recibo["rc_codcli"],
                val_recibo["rc_nomcli"],
                val_recibo["rc_importe"],
                val_recibo["rc_concepto"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo cliente
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def modificar_recibos(self, val_recibo):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            # Convierto formato de fecha
            fecha_convert = datetime.strptime(val_recibo["rc_fecha"], '%d/%m/%Y')

            # genero instruccion sql
            sql = """
                  UPDATE recibos \
                  SET rc_numero=%s, rc_fecha=%s, rc_codcli=%s, rc_nomcli=%s, rc_importe=%s, rc_concepto=%s
                  WHERE Id = %s \
                  """

            # Genero una tupla ("valores") con los valores que vienen en el parametro (diccionario)
            valores = (
                val_recibo["rc_numero"],  # de val_recibo, dame su valor
                fecha_convert,
                #val_recibo["rc_fecha"],
                val_recibo["rc_codcli"],
                val_recibo["rc_nomcli"],
                val_recibo["rc_importe"],
                val_recibo["rc_concepto"],
                val_recibo["Id"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            return
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_item_recibos(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = '''DELETE FROM recibos WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            return n
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            # Busca un string en los campos indicados en una tabla
            if len(argumento) > 0:
                cur.execute("SELECT * FROM " + argumento)
            else:
                return ""
            datos = cur.fetchall()
            self.cnn.commit()
            return datos
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()