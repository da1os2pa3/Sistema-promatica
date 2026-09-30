import mysql.connector
from mysql.connector import Error

class DatosCompras:

    def __init__(self, pantalla):
        self.master = pantalla

        # try:
        #     self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        # except Error as ex:
        #     print("Error de conexion: {0}".format(ex))

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_compras(self, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM faltantes"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def traer_ultimo(self, _xparametro):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT MAX(codigo) FROM faltantes")
            resultado = cur.fetchone()[0]
            return resultado or 0  # 👈 clave
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM faltantes " + argumento)
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_registro(self, articulos):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  INSERT INTO faltantes (fa_fecha, fa_articulo, fa_estado, fa_observaciones)
                  VALUES (%s, %s, %s, %s) 
                  """

            valores = (
                articulos["fa_fecha"],
                articulos["fa_articulo"],
                articulos["fa_estado"],
                articulos["fa_observaciones"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo registro
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def modificar_registro(self, articulos):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            #fecha_ingreso = datetime.strptime(cliente["fecha_ingreso"], '%d/%m/%Y')

            # genero instruccion sql
            sql = """
                  UPDATE faltantes 
                  SET fa_fecha=%s, fa_articulo=%s, fa_estado=%s, fa_observaciones=%s
                  WHERE Id = %s 
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
            # y asi se genera la tupla
            valores = (
                articulos["fa_fecha"],
                articulos["fa_articulo"],
                articulos["fa_estado"],
                articulos["fa_observaciones"],
                articulos["Id"]
            )
            cur.execute(sql, valores)
            cnn.commit()
            return
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_articulo(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM faltantes WHERE Id = %s"
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (Id,))
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()
