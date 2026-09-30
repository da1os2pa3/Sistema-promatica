import mysql.connector
#from mysql.connector import Error

class Datosproved:

    def __init__(self, pantalla):
        self.master = pantalla

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_proved(self, orden=""):

        """👉 buffered=True = MySQL:manda TODO el resultado de una, el cursor lo guarda en memoria.
        ✔ Después podés hacer lo que quieras: otro execute, cerrar cursor, no consumir todo
        SIN errores"""

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM proved"
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
            cur.execute("SELECT MAX(codigo) FROM proved")
            resultado = cur.fetchone()[0]
            return resultado or 0  # 👈 clave
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM proved " + argumento)
            datos = cur.fetchall()
            return datos
        finally:
            cur.close()
            cnn.close()

    def eliminar_proved(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM proved WHERE Id = %s"
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

    def insertar_proved(self, datos_proved):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  INSERT INTO proved (codigo, denominacion, direccion, localidad, provincia, postal, telefono1,
                                      telefono2, mail, fecha_alta, contacto, observaciones)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                  """

            valores = (
                datos_proved["codigo"],
                datos_proved["denominacion"],
                datos_proved["direccion"],
                datos_proved["localidad"],
                datos_proved["provincia"],
                datos_proved["postal"],
                datos_proved["telefono1"],
                datos_proved["telefono2"],
                datos_proved["mail"],
                datos_proved["fecha_alta"],
                datos_proved["contacto"],
                datos_proved["observaciones"]
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

    def modificar_proved(self, datos_proved):

         cnn = self.get_connection()
         cur = cnn.cursor(buffered=True)
         try:

             sql = """
                   UPDATE proved \
                   SET codigo=%s, \
                       denominacion=%s, \
                       direccion=%s, \
                       localidad=%s, \
                       provincia=%s, \
                       postal=%s, \
                       telefono1=%s, \
                       telefono2=%s, \
                       mail=%s, \
                       fecha_alta=%s, \
                       contacto=%s, \
                       observaciones=%s
                   WHERE Id = %s \
                   """

             # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
             # y asi se genera la tupla
             valores = (
                 datos_proved["codigo"],
                 datos_proved["denominacion"],
                 datos_proved["direccion"],
                 datos_proved["localidad"],
                 datos_proved["provincia"],
                 datos_proved["postal"],
                 datos_proved["telefono1"],
                 datos_proved["telefono2"],
                 datos_proved["mail"],
                 datos_proved["fecha_alta"],
                 datos_proved["contacto"],
                 datos_proved["observaciones"],
                 datos_proved["Id"]
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
