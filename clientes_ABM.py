import mysql.connector
from mysql.connector import Error
# ----------------------------------------
from datetime import datetime
# ----------------------------------------
from tkinter import messagebox

class datosClientes:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_clientes("")
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_clientes(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM "+ tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-",
                                 parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        # Trae el último código de cliente en la tabla para proponer el nuevo número en alta

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM clientes ORDER BY codigo ASC")
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=traer ultimo",
                                 parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        try:
            cur = self.cnn.cursor()
            if len(argumento) <= 0:
                return
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=buscar_entabla",
                                 parent=self.master)
            exit()

    def insertar_clientes(self, codigo, apellido, nombres, direccion, localidad, provincia, postal, telef_pers,
                          telef_trab, mail, fecha_ingreso, sit_fis, cuit, observaciones, apenombre):

        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            fecha_ingreso = datetime.strptime(fecha_ingreso, '%d/%m/%Y')

            cur = self.cnn.cursor()
            sql = '''INSERT INTO clientes (codigo, apellido, nombres, direccion, localidad, provincia, postal, 
            telef_pers, telef_trab, mail, fecha_ingreso, sit_fis, cuit, observaciones, apenombre) VALUES('{}', '{}', 
            '{}', '{}', '{}','{}','{}', '{}', '{}','{}','{}','{}','{}','{}','{}')'''.format(codigo, apellido,
            nombres, direccion, localidad, provincia, postal, telef_pers, telef_trab, mail, fecha_ingreso, sit_fis,
            cuit, observaciones, apenombre)

            cur.execute(sql)
            #n = cur.rowcount
            self.cnn.commit()
            cur.close()
            #return n
            return
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=insertar_clientes",
                                 parent=self.master)
            exit()

    def modificar_clientes(self, Id, codigo, apellido, nombres, direccion, localidad, provincia, postal, telef_pers,
                           telef_trab, mail, fecha_ingreso, sit_fis, cuit, observaciones, apenombre):

        try:

            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            fecha_ingreso = datetime.strptime(fecha_ingreso, '%d/%m/%Y')

            cur = self.cnn.cursor()

            sql = '''UPDATE clientes SET codigo='{}', apellido='{}', nombres='{}', direccion='{}', localidad='{}', 
            provincia='{}', postal='{}', telef_pers='{}', telef_trab='{}', mail='{}', fecha_ingreso='{}', sit_fis='{}', 
            cuit='{}', observaciones='{}', apenombre='{}'
            WHERE Id={}'''.format(codigo, apellido, nombres, direccion, localidad, provincia, postal, telef_pers,
                                  telef_trab, mail, fecha_ingreso, sit_fis, cuit, observaciones, apenombre, Id)

            cur.execute(sql)
            #n = cur.rowcount
            self.cnn.commit()
            cur.close()
            #return n
            return

        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=modificar_clientes",
                                 parent=self.master)
            exit()

    def eliminar_clientes(self, Id):

        try:

            cur = self.cnn.cursor()
            sql = '''DELETE FROM clientes WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n

        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=eliminar_clientes",
                                 parent=self.master)
            exit()
