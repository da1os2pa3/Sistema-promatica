import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import messagebox

class clase_inf_tecnicos_ABM:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):
        datos = self.consultar_inf_tecnicos()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def aplicar_filtro(self, tofil):

        cur = self.cnn.cursor()

        cur.execute("SELECT * FROM " + tofil)   # incluye el WHERE
        datos = cur.fetchall()

        self.cnn.commit()
        cur.close()
        print("cambio de filtro exitoso")
        return

    def consultar_inf_tecnicos(self, tofil):

        try:

            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)   # incluye el WHERE
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-", parent=self.master)
            exit()

    def consultar_edicion(self, tofil):
        # lo usa la parte de edicion del programa para mandar solo el registro solicitado
        try:

            cur = self.cnn.cursor()

            cur.execute("SELECT * FROM " + tofil)   # incluye el WHERE
            datos = cur.fetchone()

            self.cnn.commit()
            cur.close()
            #messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-", parent=self.master)

            return datos

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-", parent=self.master)
            exit()

    def traer_un_registro(self, Id):

        cur = self.cnn.cursor()
        sql = '''SELECT * FROM orden_repara WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        datos_inf = cur.fetchone()
        n = cur.rowcount                       # ver esto porque no lo uso en la modif
        self.cnn.commit()
        cur.close()
        return datos_inf

    def insertar_informe(self, fecha, usuario, tipodoc, numdoc, equipo, modelo, serie, diagnostico, provocado, informe):

        # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
        fecha_paso = fecha
        fecha_ingreso = datetime.strptime(fecha_paso, '%d/%m/%Y')

        cur = self.cnn.cursor()
        sql = '''INSERT INTO inf_tecnicos (it_fecha, it_usuario, it_dni, it_numdoc, it_equipo, it_modelo, it_serie, 
        it_diagnostico, it_provocado, it_informe)
        VALUES('{}', '{}', '{}', '{}', '{}','{}','{}', '{}', '{}', '{}')'''.format(fecha_ingreso, usuario, tipodoc,
                                                                       numdoc, equipo, modelo, serie, diagnostico,
                                                                       provocado, informe)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def modificar_informe(self, Id, fecha, usuario, tipodoc, numdoc, equipo, modelo, serie, diagnostico, provocado,
                          informe):

        # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
        fecha_paso = fecha
        fecha_ingreso = datetime.strptime(fecha_paso, '%d/%m/%Y')

        cur = self.cnn.cursor()
        sql = '''UPDATE inf_tecnicos SET it_fecha='{}', it_usuario='{}', it_dni='{}', it_numdoc='{}', it_equipo='{}',
        it_modelo='{}', it_serie='{}', it_diagnostico='{}', it_provocado='{}', it_informe='{}' 
                            WHERE Id={}'''.format(fecha_ingreso, usuario, tipodoc, numdoc, equipo, modelo, serie,
                                           diagnostico, provocado, informe, Id)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_informe(self, Id):

        cur = self.cnn.cursor()
        sql = '''DELETE FROM inf_tecnicos WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def traer_ultimo(self, xparametro):

        # Trae el último código de cliente en la tabla para proponer el nuevo número en alta

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM inf_tecnicos ORDER BY id ASC")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = str(row[1]) + "\n" # retorna el codigo
                else:
                    aux = str(row[0]) + "\n" # retorna el Id
            self.cnn.commit()
            cur.close()
            return aux
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=traer ultimo",
                                 parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        cur = self.cnn.cursor()
        if len(argumento) <= 0:
            return

        cur.execute("SELECT * FROM " + argumento)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos
