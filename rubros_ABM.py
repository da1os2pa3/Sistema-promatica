import mysql.connector
from mysql.connector import Error
# -----------------------------------------------
#from datetime import datetime
from tkinter import messagebox

class datosRubros:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #     datos = self.consultar_rubros("")
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_rubros(self, tofil):
        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar_rubros", parent=self.master)
            exit()

    def insertar_rubros(self, ru_nombre):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO rubros (ru_nombre) VALUES('{}')'''.format(ru_nombre)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Insertar_rubros", parent=self.master)
            exit()

    def modificar_rubros(self, Id, ru_nombre):

        try:
            cur = self.cnn.cursor()
            sql = '''UPDATE rubros SET ru_nombre='{}' WHERE Id={}'''.format(ru_nombre, Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Modificar_rubros", parent=self.master)
            exit()

    def modi_rub_enart(self, tofil, anterior):
        # modifica los rubros en la tabla articulos al modificarlos en la tabla rubros

        try:
            cur = self.cnn.cursor()
            sql =  "UPDATE articulos SET rubro = '" + tofil +"' WHERE rubro = '" + anterior + "'"
            cur.execute(sql)
            datos = cur.fetchone()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Modificar_rubros", parent=self.master)
            exit()

    def eliminar_rubros(self, Id):
        cur = self.cnn.cursor()
        sql = '''DELETE FROM rubros WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def verifica_articulos(self, tofil):
        # verifica si hay articulos con el rubro a eliminar o modificar

        try:
            cur = self.cnn.cursor()
            sql =  "SELECT * FROM articulos WHERE rubro = '" + tofil + "'"
            cur.execute(sql)
            datos = cur.fetchall()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Verifica_articulos", parent=self.master)
            exit()

    def quitarubro(self, tofil):
        # quita los rubros asignados en tabla articulos al ser eliminado de la tabla rubros

        try:
            cur = self.cnn.cursor()
            sql =  "UPDATE articulos SET rubro = '' WHERE rubro = '" + tofil + "'"
            cur.execute(sql)
            datos = cur.fetchone()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=quitarubro", parent=self.master)
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-buscAr_entabla", parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM rubros ORDER BY Id")
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
