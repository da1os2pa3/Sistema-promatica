import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import messagebox

class datosCompras:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def consultar_compras(self, tofil):

        try:
            cur = self.cnn.cursor()
            if tofil == "":
                cur.execute("SELECT * FROM " + tofil)
            else:
                cur.execute("SELECT * FROM " + tofil)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo consultar compras", parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM faltantes ORDER BY fa_fecha")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = str(row[1]) + "\n"
                else:
                    aux = str(row[0]) + "\n"
            self.cnn.commit()
            cur.close()
            return aux
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=traer ultimo", parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        try:
            cur = self.cnn.cursor()
            if len(argumento) > 0:
                cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo buscar en tabla", parent=self.master)
            exit()

    def insertar_registro(self, fecha, articulo, estado):

        try:
            algo = fecha
            fecha_ingreso = datetime.strptime(algo, '%d/%m/%Y')
            cur = self.cnn.cursor()
            sql = '''INSERT INTO faltantes (fa_fecha, fa_articulo, fa_estado) VALUES('{}','{}','{}')'''.format(fecha_ingreso,
                                                            articulo, estado)
            cur.execute(sql)
            cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo insertar registro", parent=self.master)
            exit()

    def modificar_registro(self, Id, fecha, articulo, estado):

        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            algo = fecha
            fecha_ingreso = datetime.strptime(algo, '%d/%m/%Y')
            cur = self.cnn.cursor()
            sql = '''UPDATE faltantes SET fa_fecha='{}', fa_articulo='{}', fa_estado='{}' WHERE Id={}'''.format(fecha_ingreso,
                                                    articulo, estado, Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo modificar registro", parent=self.master)
            exit()

    def eliminar_articulo(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM faltantes WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo eliminar articulo", parent=self.master)
            exit()
