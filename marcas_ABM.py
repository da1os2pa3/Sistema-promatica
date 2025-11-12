import mysql.connector
from mysql.connector import Error
#from datetime import datetime
# --------------------------------------------------
from tkinter import messagebox

class datosMarcas:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def __str__(self):

        datos = self.consultar_marcas()
        aux = ""
        for row in datos:
            aux = aux + str(row) + "\n"
        return aux

    def consultar_marcas(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar marcas",
                                 parent=self.master)
            exit()

    def insertar_marcas(self, ma_nombre):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO marcas (ma_nombre)
            VALUES('{}')'''.format(ma_nombre)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=insertar_marcas",
                                 parent=self.master)
            exit()

    def modificar_marcas(self, Id, ma_nombre):

        try:
            cur = self.cnn.cursor()
            sql = '''UPDATE marcas SET ma_nombre='{}'
            WHERE Id={}'''.format(ma_nombre, Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Modificar_marcas",
                                 parent=self.master)
            exit()

    def modi_marca_enart(self, tofil, anterior):
        # modifica las marcas en tabla articulos al modificarla en tabla marcas

        try:
            cur = self.cnn.cursor()
            # print(tofil)
            # print(anterior)
            sql =  "UPDATE articulos SET marca = '" + tofil +"' WHERE marca = '" + anterior + "'"
            cur.execute(sql)
            datos = cur.fetchone()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=modi_marca_enart",
                                 parent=self.master)
            exit()

    def eliminar_marcas(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM marcas WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=eliminar_marcas",
                                 parent=self.master)
            exit()

    def quitamarca(self, tofil):

        # quita las marcas asignadas en tabla articulos al ser eliminada de la tabla marcas

        try:
            cur = self.cnn.cursor()
            sql =  "UPDATE articulos SET marca = '' WHERE marca = '" + tofil + "'"
            cur.execute(sql)
            datos = cur.fetchone()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=quitamarca",
                                 parent=self.master)
            exit()

    def verifica_articulos(self, tofil):

        # verifica si hay articulos con el rubro a eliminar o modificar

        try:
            cur = self.cnn.cursor()
            sql =  "SELECT * FROM articulos WHERE marca = '" + tofil + "'"
            cur.execute(sql)
            datos = cur.fetchall()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=verifica_articulos",
                                 parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        try:
            cur = self.cnn.cursor()
            if len(argumento) > 0:
                cur.execute("SELECT * FROM " + argumento)
            else:
                cur.execute("SELECT * FROM " + argumento)

            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=buscar_entabla",
                                 parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM marcas ORDER BY Id")
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
