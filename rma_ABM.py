import mysql.connector
from mysql.connector import Error
from datetime import datetime
from tkinter import messagebox

class datosRma:

    def __init__(self):

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_rma()
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_rma(self, tofil):

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

    def buscar_entabla(self, argumento):

        # Busca un strin en los campos indicados en una tabla
        cur = self.cnn.cursor()
        if len(argumento) > 0:
            cur.execute("SELECT * FROM " + argumento)

        datos = cur.fetchall()
        self.cnn.commit()
        cur.close()
        return datos

    def insertar_registro(self, fecha, articulo, proceso, estado, proved, cliente, falla_motivo, costo_venta, observ):

        algo = fecha
        fecha_ingreso = datetime.strptime(algo, '%d/%m/%Y')

        cur = self.cnn.cursor()

        sql = '''INSERT INTO rma (rm_fecha, rm_articulo, rm_proceso, rm_estado, rm_proveedor, rm_cliente, 
                                  rm_falla_motivo, rm_costo_venta, rm_observaciones) VALUES('{}','{}','{}','{}','{}',
                                  '{}','{}','{}','{}')'''.format(fecha_ingreso, articulo, proceso, estado, proved,
                                                             cliente, falla_motivo, costo_venta, observ)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()

    def modificar_registro(self, Id, fecha, articulo, proceso, estado, proved, cliente, falla_motivo, costo_venta, observ):

        # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
        algo = fecha
        fecha_ingreso = datetime.strptime(algo, '%d/%m/%Y')

        cur = self.cnn.cursor()
        sql = '''UPDATE rma SET rm_fecha='{}', rm_articulo='{}', rm_proceso='{}', rm_estado='{}', rm_proveedor='{}', 
                                rm_cliente='{}', rm_falla_motivo='{}', rm_costo_venta='{}', rm_observaciones='{}'
                                 WHERE Id={}'''.format(fecha_ingreso, articulo, proceso, estado, proved, cliente,
                                                       falla_motivo, costo_venta, observ, Id)

        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def eliminar_rma(self, Id):

        cur = self.cnn.cursor()
        sql = '''DELETE FROM rma WHERE Id = {}'''.format(Id)
        cur.execute(sql)
        n = cur.rowcount
        self.cnn.commit()
        cur.close()
        return n

    def traer_ultimo(self, xparametro):

        # Trae el último código de cliente en la tabla para proponer el nuevo número en alta

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM rma ORDER BY Id")
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
