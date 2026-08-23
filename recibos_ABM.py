import mysql.connector
from datetime import datetime
# -----------------------------------------------------

class datosRecibos:

    def __init__(self, pantalla):

        self.master = pantalla

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
        except Exception:
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
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_item_recibos(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM recibos WHERE Id = %s"
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

    def buscar_recibos(self, texto):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  SELECT * FROM recibos WHERE rc_nomcli LIKE %s ORDER BY rc_numero ASC 
                  """

            """ Como paso un solo parametro, debo colocar la coma al final para que se interprete como una tupla, sino, 
            lo toma como un string. Si vinieran mas parametros separados por coma ya se da cuenta que es una tupla"""
            #param = f"%{texto}%"
            param = (f"%{texto}%",)

            cur.execute(sql, param)
            datos = cur.fetchall()
            return datos
        finally:
            cur.close()
            cnn.close()
