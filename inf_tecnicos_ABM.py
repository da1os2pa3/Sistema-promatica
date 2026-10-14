from datetime import datetime
import mysql.connector

class ClaseInfTecnicosABM:

    def __init__(self, pantalla):
        self.master = pantalla

    @staticmethod
    def get_connection():

        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_inf_tecnicos(self, orden=None):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = "SELECT * FROM inf_tecnicos"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def consultar_edicion(self, tofil):
        # lo usa la parte de edicion del programa para mandar solo el registro solicitado

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM " + tofil)   # incluye el WHERE
            datos = cur.fetchone()
            return datos
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    # def traer_un_registro(self, Id):
    #
    #     cnn = None
    #     cur = None
    #     try:
    #         cnn = self.get_connection()
    #         cur = cnn.cursor(buffered=True)
    #         sql = '''SELECT * FROM orden_repara WHERE Id = {}'''.format(Id)
    #         cur.execute(sql)
    #         datos_inf = cur.fetchone()
    #         return datos_inf
    #     finally:
    #         if cur is not None:
    #             cur.close()
    #         if cnn is not None:
    #             cnn.close()

    def insertar_informe(self, fecha, usuario, tipodoc, numdoc, equipo, modelo, serie, diagnostico, provocado, informe):

        # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
        fecha_paso = fecha
        fecha_ingreso = datetime.strptime(fecha_paso, '%d/%m/%Y')

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)

            sql = '''INSERT INTO inf_tecnicos (it_fecha, it_usuario, it_dni, it_numdoc, it_equipo, it_modelo, it_serie, 
            it_diagnostico, it_provocado, it_informe)
            VALUES('{}', '{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}')'''.format(fecha_ingreso, usuario, tipodoc,
                                                                           numdoc, equipo, modelo, serie, diagnostico,
                                                                           provocado, informe)

            cur.execute(sql)
            n = cur.rowcount
            cnn.commit()
            return n
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def modificar_informe(self, Id, fecha, usuario, tipodoc, numdoc, equipo, modelo, serie, diagnostico, provocado,
                          informe):

        # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
        fecha_paso = fecha
        fecha_ingreso = datetime.strptime(fecha_paso, '%d/%m/%Y')

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)

            sql = '''UPDATE inf_tecnicos SET it_fecha='{}', it_usuario='{}', it_dni='{}', it_numdoc='{}', it_equipo='{}',
            it_modelo='{}', it_serie='{}', it_diagnostico='{}', it_provocado='{}', it_informe='{}' 
                                WHERE Id={}'''.format(fecha_ingreso, usuario, tipodoc, numdoc, equipo, modelo, serie,
                                               diagnostico, provocado, informe, Id)

            cur.execute(sql)
            n = cur.rowcount
            cnn.commit()
            return n
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def eliminar_informe(self, Id):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = '''DELETE FROM inf_tecnicos WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            cnn.commit()
            return n
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def traer_ultimo(self, xparametro):
        # Trae el último código de cliente en la tabla para proponer el nuevo número en alta

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM inf_tecnicos ORDER BY id ASC")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = str(row[1]) + "\n" # retorna el codigo
                else:
                    aux = str(row[0]) + "\n" # retorna el Id
            return aux
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
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            return datos
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()
