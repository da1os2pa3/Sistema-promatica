import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class datosArtic:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_articulo()
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_articulo(self, tofil):

        """
        # cursor.fetchall() recupera todas las filas del resultado de una consulta. Devuelve todas
        # las filas como una "lista". Se devuelve una lista vacía si no hay ningún registro para recuperar.
        # cursor.fetchmany(size)devuelve el número de filas especificadas por size el argumento. Cuando
        # se llama repetidamente, este método recupera el siguiente conjunto de filas del resultado de una
        # consulta y devuelve una lista de tuplas. Si no hay más filas disponibles, devuelve una lista vacía.
        # cursor.fetchone()El método devuelve un solo registro o Ninguno si no hay más filas disponibles.
        """

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-articulo", parent=self.master)
            exit()

    def insertar_articulo(self, codigo, descripcion, marca, rubro, codbar, costodolar, tasaiva, tasaimpint,
                          tasaporcgan, observaciones, fechaultact, costo_historico, imagenart):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO articulos (codigo, descripcion, marca, rubro, codbar, costodolar, iva, impint,
            porcgan, observa, ultact, costohist, imagen)
            VALUES('{}','{}','{}','{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}')'''.format(codigo,
            descripcion, marca, rubro, codbar, costodolar, tasaiva, tasaimpint, tasaporcgan, observaciones,
            fechaultact, costo_historico, imagenart)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Insertar-articulo", parent=self.master)
            exit()

    def modificar_articulo(self, Id, codigo, descripcion, marca, rubro, codbar, costodolar, tasaiva, tasaimpint,
                           tasaporcgan, observaciones, fechaultact, costo_historico, imagenart):

        try:
            cur = self.cnn.cursor()
            sql = '''UPDATE articulos SET codigo='{}', descripcion='{}', marca='{}', rubro='{}', codbar='{}', 
            costodolar='{}', iva='{}', impint='{}', porcgan='{}', observa='{}', ultact='{}', costohist='{}', imagen='{}'
            WHERE Id={}'''.format(codigo, descripcion, marca, rubro, codbar, costodolar, tasaiva, tasaimpint,
            tasaporcgan, observaciones, fechaultact, costo_historico, imagenart, Id)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Modificar articulo", parent=self.master)
            exit()

    def eliminar_articulo(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM articulos WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Eliminar articulo", parent=self.master)
            exit()

    def consultar_informa(self):

        try:
            # Devuelve el registro de la tabla Informa
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            cur.close()
            return datos_inf
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar_informa", parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        try:
            # Busca un string en los campos indicados en una tabla
            cur = self.cnn.cursor()
            if len(argumento) <= 0:
                messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=argumento de "
                                                         "busqueda vacio", parent=self.master)
                return

            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Buscar en tabla", parent=self.master)
            exit()

    def combo_input(self, xcampo, xtabla, xorden):

        try:

            """ Llenar un combobox con datos de una tabla. Paso el campo, la tabla y el orden de los datos """

            cnn = mysql.connector.connect(host="localhost", user="root", passwd="", db="sist_prom")
            cursor = cnn.cursor()
            cursor.execute("SELECT " + xcampo + " FROM " + xtabla + " ORDER BY " + xorden)
            result = cursor.fetchall()
            return result

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=combo_input", parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        """ Devuelve el Id. del ultimo registro de la tabla (primer valor autocompletado por la tabla) """

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM articulos ORDER BY Id")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = str(row[1]) + "\n"
                else:
                    aux = str(row[0]) + "\n"
            self.cnn.commit()
            cur.close()
            if aux == "":
                aux = 0
            return aux
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Traer ultimo Id-", parent=self.master)
            exit()
