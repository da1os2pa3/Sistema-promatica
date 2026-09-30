import mysql.connector
# from mysql.connector import Error

class DatosRubros:

    def __init__(self, pantalla):

        self.master = pantalla

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_rubros(self, orden=None):

        """👉 buffered=True = MySQL:manda TODO el resultado de una, el cursor lo guarda en memoria.
        ✔ Después podés hacer lo que quieras: otro execute, cerrar cursor, no consumir todo
        SIN errores"""

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM rubros"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def traer_ultimo(self):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT MAX(codigo) FROM rubros")
            resultado = cur.fetchone()[0]
            return resultado or 0  # 👈 clave
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM rubros " + argumento)
            datos = cur.fetchall()
            return datos
        finally:
            cur.close()
            cnn.close()

    def insertar_rubros(self, datos_rubros):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  INSERT INTO rubros (ru_nombre)
                  VALUES (%s) 
                  """
            valores = (
                datos_rubros["ru_nombre"],
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

    def modificar_rubros(self, datos_rubros):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            sql = """
                  UPDATE rubros 
                  SET ru_nombre=%s 
                  WHERE Id = %s 
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
            # y asi se genera la tupla
            valores = (
                datos_rubros["ru_nombre"],
                datos_rubros["Id"]
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

    def modi_rub_enart(self, tofil, anterior):
        # modifica los rubros en la tabla articulos al modificarlos en la tabla rubros

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql =  "UPDATE articulos SET rubro = '" + tofil +"' WHERE rubro = '" + anterior + "'"
            cur.execute(sql)
            # datos = cur.fetchone()
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_rubros(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM rubros WHERE Id = %s"
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

    def verifica_articulos(self, tofil):
        # verifica si hay articulos con el rubro a eliminar o modificar

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql =  "SELECT * FROM articulos WHERE rubro = '" + tofil + "'"
            cur.execute(sql)
            # datos = cur.fetchall()
            n = cur.rowcount
            cur.close()
            return n
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def quitarubro(self, tofil):
        # quita los rubros asignados en tabla articulos al ser eliminado de la tabla rubros

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql =  "UPDATE articulos SET rubro = '' WHERE rubro = '" + tofil + "'"
            cur.execute(sql)
            # datos = cur.fetchone()
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()