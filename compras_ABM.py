import mysql.connector

class DatosCompras:

    def __init__(self, pantalla):
        self.master = pantalla

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_compras(self, orden=""):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = "SELECT * FROM faltantes"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def traer_ultimo(self, _xparametro):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT MAX(codigo) FROM faltantes")
            resultado = cur.fetchone()[0]
            return resultado or 0  # 👈 clave
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def buscar_entabla(self, argumento):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM faltantes " + argumento)
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def insertar_registro(self, articulos):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
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
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def modificar_registro(self, articulos):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
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
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def eliminar_articulo(self, Id):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
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
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()
