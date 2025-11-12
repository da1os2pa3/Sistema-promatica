import mysql.connector
from mysql.connector import Error
#from datetime import datetime
from tkinter import messagebox

class datosRecibos:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def consultar_recibos(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Consultar recibos-", parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM recibos ORDER BY Id ASC")
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
            # Busca un string en los campos indicados en una tabla
            cur = self.cnn.cursor()
            if len(argumento) > 0:
                cur.execute("SELECT * FROM " + argumento)
            else:
                return ""
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo:buscar_entabla", parent=self.master)
            exit()

    def insertar_recibo(self, numero_recibo, fecha, codcli, nomcli, importe, detalle):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO recibos (rc_numero, rc_fecha, rc_codcli, rc_nomcli,rc_importe, rc_concepto) 
                                          VALUES('{}', '{}','{}','{}', '{}', '{}')'''.format(numero_recibo,
                                                                fecha, codcli, nomcli, importe, detalle)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo:insertar_recibo", parent=self.master)
            exit()

    def eliminar_item_recibos(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM recibos WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo:eliminar_item_recibos", parent=self.master)
            exit()

    def modificar_recibos(self, Id, numero_venta, fechamovim, codcli, nomcli, importe, detalle):

        try:
            cur = self.cnn.cursor()
            sql = '''UPDATE recibos SET rc_numero='{}', rc_fecha='{}', rc_codcli='{}', rc_nomcli='{}', 
                                        rc_importe='{}', rc_concepto='{}' WHERE Id={}'''.format(numero_venta,
                                                                fechamovim, codcli, nomcli, importe, detalle, Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo:modificar_recibos", parent=self.master)
            exit()
