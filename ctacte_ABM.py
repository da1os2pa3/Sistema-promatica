import mysql.connector

class DatosCtacte:

    def __init__(self, pantalla):
        self.master = pantalla

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_ctacte(self, orden=""):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = "SELECT * FROM ctacte"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def insertar_ctacte(self, datos_ctacte):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = """
                  INSERT INTO ctacte (cc_fecha, cc_detalle, cc_ingreso, cc_egreso, cc_codcli, cc_nomcli, cc_clavemov)
                  VALUES (%s, %s, %s, %s, %s, %s, %s)
                  """

            valores = (
                datos_ctacte["cc_fecha"],
                datos_ctacte["cc_detalle"],
                datos_ctacte["cc_ingreso"],
                datos_ctacte["cc_egreso"],
                datos_ctacte["cc_codcli"],
                datos_ctacte["cc_nomcli"],
                datos_ctacte["cc_clavemov"]
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
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def eliminar_item_ctacte(self, Id):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = '''DELETE FROM ctacte WHERE Id = {}'''.format(Id)
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

    def modificar_ctacte(self, datos_ctacte):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            # genero instruccion sql
            sql = """
                  UPDATE ctacte \
                  SET cc_fecha=%s, cc_detalle=%s, cc_ingreso=%s, cc_egreso=%s, cc_codcli=%s, cc_nomcli=%s, 
                      cc_clavemov=%s
                  WHERE Id = %s \
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
            # y asi se genera la tupla
            valores = (
                datos_ctacte["cc_fecha"],
                datos_ctacte["cc_detalle"],
                datos_ctacte["cc_ingreso"],
                datos_ctacte["cc_egreso"],
                datos_ctacte["cc_codcli"],
                datos_ctacte["cc_nomcli"],
                datos_ctacte["cc_clavemov"],
                datos_ctacte["Id"]
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

    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # COMPACTACION
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def sumar_compactar(self, tofil):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute(tofil)
            total_ing, total_egr = cur.fetchone()
            return [total_ing, total_egr]
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def borrar_compactar(self, tofil):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute(tofil)
            # datos = cur.fetchall()
            cnn.commit()
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def sumar_saldo_control(self, tofil):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute(tofil)
            nuevo_saldo = cur.fetchone()
            #datos = cur.fetchall()
            return nuevo_saldo
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()
