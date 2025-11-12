import mysql.connector
from mysql.connector import Error
# --------------------------------------------
from datetime import datetime
# --------------------------------------------
from tkinter import messagebox

class datosProved:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_proved()
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_proved(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar_proved",
                                 parent=self.master)
            exit()

    def traer_ultimo(self, parametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM proved ORDER BY codigo ASC")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if parametro == 1:
                    aux = str(row[1]) + "\n"
                else:
                    aux = str(row[0]) + "\n"
            self.cnn.commit()
            cur.close()
            return aux
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Traer_ultimo",
                                 parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Buscar_entabla",
                                 parent=self.master)
            exit()

    def insertar_proved(self, codigo, denominacion, direccion, localidad, provincia, postal, telefono1, telefono2, mail,
                              fecha_alta, contacto, observaciones):

        try:
            # # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            fecha_alta = datetime.strptime(fecha_alta, '%d/%m/%Y')

            cur = self.cnn.cursor()
            sql = '''INSERT INTO proved (codigo, denominacion, direccion,
            localidad, provincia, postal, telefono1, telefono2, mail, fecha_alta,
            contacto, observaciones)
            VALUES('{}', '{}', '{}', '{}', '{}', '{}','{}','{}', '{}', '{}','{}','{}')'''.format(codigo,
            denominacion, direccion, localidad, provincia, postal, telefono1, telefono2, mail, fecha_alta, contacto,
            observaciones)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Insertar_proved",
                                 parent=self.master)
            exit()

    def modificar_proved(self, Id, codigo, denominacion, direccion, localidad, provincia, postal, telefono1, telefono2,
                         mail, fecha_alta, contacto, observaciones):

        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
            fecha_alta = datetime.strptime(fecha_alta, '%d/%m/%Y')

            cur = self.cnn.cursor()
            sql = '''UPDATE proved SET codigo='{}', denominacion='{}', direccion='{}', localidad='{}', provincia='{}', 
            postal='{}', telefono1='{}', telefono2='{}', mail='{}', fecha_alta='{}', contacto='{}', observaciones='{}'
            WHERE Id={}'''.format(codigo, denominacion, direccion, localidad, provincia, postal, telefono1, telefono2,
                                  mail, fecha_alta, contacto, observaciones, Id)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Modificar__proved",
                                 parent=self.master)
            exit()









    def eliminar_proved(self, Id):

        cur = self.cnn.cursor()
        sql = '''DELETE FROM proved WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

