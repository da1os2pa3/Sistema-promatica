import mysql.connector
from mysql.connector import Error


class DatosRma:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_rma(self, orden = ""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM rma"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM rma " + argumento)
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_registro(self, rma):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            sql = """
                  INSERT INTO rma (rm_fecha, rm_articulo, rm_proceso, rm_estado, rm_proveedor, rm_cliente, 
                                   rm_falla_motivo, rm_costo_venta, rm_observaciones)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """

            valores = (
                rma["rm_fecha"],
                rma["rm_articulo"],
                rma["rm_proceso"],
                rma["rm_estado"],
                rma["rm_proveedor"],
                rma["rm_cliente"],
                rma["rm_falla_motivo"],
                rma["rm_costo_venta"],
                rma["rm_observaciones"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo cliente
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def modificar_registro(self, rma):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            # genero instruccion sql
            sql = """
                  UPDATE rma 
                  SET rm_fecha=%s, rm_articulo=%s, rm_proceso=%s, rm_estado=%s, rm_proveedor=%s, rm_cliente=%s, 
                      rm_falla_motivo=%s, rm_costo_venta=%s, rm_observaciones=%s
                  WHERE Id = %s 
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la
            # clave rma[codigo] y asi se genera la tupla
            valores = (
                rma["rm_fecha"],
                rma["rm_articulo"],
                rma["rm_proceso"],
                rma["rm_estado"],
                rma["rm_proveedor"],
                rma["rm_cliente"],
                rma["rm_falla_motivo"],
                rma["rm_costo_venta"],
                rma["rm_observaciones"],
                rma["Id"]
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

    def eliminar_rma(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM rma WHERE Id = %s"
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (Id,))
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def traer_ultimo(self, xparametro):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT MAX(codigo) FROM rma")
            resultado = cur.fetchone()[0]
            return resultado or 0  # 👈 clave
        finally:
            cur.close()
            cnn.close()
