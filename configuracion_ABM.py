import mysql.connector
from mysql.connector import Error

class DatosConfig:

    def __init__(self):

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_setting(self, orden=None):

        """👉 buffered=True = MySQL:manda TODO el resultado de una, el cursor lo guarda en memoria.
        ✔ Después podés hacer lo que quieras: otro execute, cerrar cursor, no consumir todo
        SIN errores"""
        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM informa"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def modificar_setting(self, configuracion):

        cnn=self.get_connection()
        cur = cnn.cursor(buffered=True)

        try:

            # genero instruccion sql
            sql = """
                  UPDATE informa 
                  SET i_empresa=%s, 
                      i_direccion=%s, 
                      i_localidad=%s, 
                      i_provincia=%s, 
                      i_postal=%s, 
                      i_correo=%s, 
                      i_telef1=%s,
                      i_telef2=%s, 
                      i_titular=%s, 
                      i_contacto=%s, 
                      i_sitfis=%s, 
                      i_cuit=%s, 
                      i_rentas=%s, 
                      i_municip=%s, 
                      i_iva1=%s, 
                      i_iva2=%s, 
                      i_iva3=%s, 
                      i_impint=%s, 
                      i_reten=%s, 
                      i_percep=%s, 
                      i_dolar1=%s, 
                      i_dolar2=%s, 
                      i_ultimo_saldo=%s
                  WHERE Id = %s 
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
            # y asi se genera la tupla
            valores = (
                configuracion["i_empresa"],
                configuracion["i_direccion"],
                configuracion["i_localidad"],
                configuracion["i_provincia"],
                configuracion["i_postal"],
                configuracion["i_correo"],
                configuracion["i_telef1"],
                configuracion["i_telef2"],
                configuracion["i_titular"],
                configuracion["i_contacto"],
                configuracion["i_sit_fis"],
                configuracion["i_cuit"],
                configuracion["i_rentas"],
                configuracion["i_municip"],
                configuracion["i_iva1"],
                configuracion["i_iva2"],
                configuracion["i_iva3"],
                configuracion["i_impint"],
                configuracion["i_reten"],
                configuracion["i_percep"],
                configuracion["i_dolar1"],
                configuracion["i_dolar2"],
                configuracion["i_ultimo_saldo"],
                configuracion["Id"]
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

        #                   Id, empresa, direccion, localidad, provincia, postal, correo, telef1, telef2,
        #                             titular, contacto, sitfis, cuit, rentas, municipal, iva1, iva2, iva3, impint, reten,
        #                             percep, dolar1, dolar2, ultimo_saldo):
        #
        # cur = self.cnn.cursor()
        #
        # sql = '''UPDATE informa SET i_empresa='{}', i_direccion='{}', i_localidad='{}', i_provincia='{}', i_postal='{}',
        # i_correo='{}', i_telef1='{}', i_telef2='{}', i_titular='{}', i_contacto='{}', i_sitfis='{}',
        # i_cuit='{}', i_rentas='{}', i_municip='{}',i_iva1='{}', i_iva2='{}', i_iva3='{}', i_impint='{}',
        # i_reten='{}', i_percep='{}', i_dolar1='{}', i_dolar2='{}', i_ultimo_saldo='{}'
        # WHERE Id={}'''.format(empresa, direccion, localidad, provincia, postal, correo, telef1, telef2, titular,
        #                             contacto, sitfis, cuit, rentas, municipal, iva1, iva2, iva3, impint, reten, percep,
        #                             dolar1, dolar2, ultimo_saldo, Id)
        #
        # cur.execute(sql)
        # n = cur.rowcount
        # self.cnn.commit()
        # cur.close()
        # return n
