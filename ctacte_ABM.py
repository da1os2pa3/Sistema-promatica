import mysql.connector
from mysql.connector import Error
# --------------------------------------
from datetime import datetime
from tkinter import messagebox
# --------------------------------------

class datosCtacte:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):

        datos = self.consultar_ctacte("")
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consultar_ctacte(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar_ctacte-",
                         parent=self.master)
            exit()

    def insertar_ctacte(self, fecha, detalle, ingreso, egreso, codcli, nomcli, clavemov):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO ctacte (cc_fecha, cc_detalle, cc_ingreso, cc_egreso, cc_codcli, cc_nomcli, 
                                         cc_clavemov) VALUES('{}','{}','{}','{}', '{}', '{}','{}')'''.format(fecha,
                                         detalle, ingreso, egreso, codcli, nomcli, clavemov)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Insertar_ctacte-",
                         parent=self.master)
            exit()

    def eliminar_item_ctacte_xmodif(self, clave_movimiento):

        """
        Este metodo elimina el movimiento en cuenta corriente corresondiente a la clave de movimiento pasada
        como parametro, esto pasa cuando se modifica un item de planilla de caja con imputacion a cuenta corriente
        """

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM ctacte WHERE cc_clavemov = ''' + clave_movimiento
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=eliminar_item_ctacte_xmodif-",
                         parent=self.master)
            exit()

    def eliminar_item_ctacte(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM ctacte WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=eliminar_item_ctacte-",
                         parent=self.master)
            exit()

    def modificar_ctacte(self, Id, fechamovim, detalle, debito, credito, codcli, nomcli, clavemovim):

        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            algo = fechamovim
            fechapla = datetime.strptime(algo, '%d/%m/%Y')

            cur = self.cnn.cursor()

            sql = '''UPDATE ctacte SET cc_fecha='{}', cc_detalle='{}', cc_ingreso='{}', cc_egreso='{}', cc_codcli='{}', 
            cc_nomcli='{}', cc_clavemov='{}' WHERE Id={}'''.format(fechapla, detalle, debito, credito, codcli,
                                                                   nomcli, clavemovim, Id)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=modificar_ctacte-",
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=buscar_entabla-",
                         parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM ctacte ORDER BY Id")
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo traer ultimo",
                                 parent=self.master)
            exit()
