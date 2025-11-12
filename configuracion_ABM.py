import mysql.connector
from mysql.connector import Error

class datosConfig:

    def __init__(self):
        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):
        datos = self.consultar_setting()
#        datos_inf = self.consultar_informa()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consultar_setting(self, tofil):
        cur = self.cnn.cursor()
        if tofil == "":
            cur.execute("SELECT * FROM " + tofil)
        else:
            cur.execute("SELECT * FROM " + tofil)
        # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
        """ cursor.fetchall()recupera todas las filas del resultado de una consulta. Devuelve todas
        # las filas como una "lista". Se devuelve una lista vacía si no hay ningún registro para recuperar.
        # cursor.fetchmany(size)devuelve el número de filas especificadas por size el argumento. Cuando
        # se llama repetidamente, este método recupera el siguiente conjunto de filas del resultado de una
        # consulta y devuelve una lista de tuplas. Si no hay más filas disponibles, devuelve una lista vacía.
        # cursor.fetchone()El método devuelve un solo registro o Ninguno si no hay más filas disponibles. """
        # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
        # para recuperar todas filas de una tabla de base de datos
        datos = cur.fetchone()
        cur.close()
        return datos

    def modificar_setting(self, Id, empresa, direccion, localidad, provincia, postal, correo, telef1, telef2,
                                    titular, contacto, sitfis, cuit, rentas, municipal, iva1, iva2, iva3, impint, reten,
                                    percep, dolar1, dolar2, ultimo_saldo):

        cur = self.cnn.cursor()

        sql = '''UPDATE informa SET i_empresa='{}', i_direccion='{}', i_localidad='{}', i_provincia='{}', i_postal='{}', 
        i_correo='{}', i_telef1='{}', i_telef2='{}', i_titular='{}', i_contacto='{}', i_sitfis='{}',
        i_cuit='{}', i_rentas='{}', i_municip='{}',i_iva1='{}', i_iva2='{}', i_iva3='{}', i_impint='{}', 
        i_reten='{}', i_percep='{}', i_dolar1='{}', i_dolar2='{}', i_ultimo_saldo='{}' 
        WHERE Id={}'''.format(empresa, direccion, localidad, provincia, postal, correo, telef1, telef2, titular,
                                    contacto, sitfis, cuit, rentas, municipal, iva1, iva2, iva3, impint, reten, percep,
                                    dolar1, dolar2, ultimo_saldo, Id)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n
