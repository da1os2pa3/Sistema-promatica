import mysql.connector
from mysql.connector import Error
# ---------------------------------------
# from datetime import datetime
# ---------------------------------------
from tkinter import messagebox

class datosGarantias:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #     datos = self.consultar_garantia("")
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_garantia(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Consultar garantia-", parent=self.master)
            exit()

    # 1 uso
    def consultar_informa(self):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos_inf
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Consultar informa-", parent=self.master)
            exit()

    def insertar_garantias(self, fechamovim, meses, fechavto, codcli, nomcli, nomart, totaloper, factura, obser,
                           detalle):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO garantias (gt_fechaventa, gt_meses, gt_fechavto, gt_codcli, gt_nomcli, gt_articulo,
                                            gt_impventa, gt_factura, gt_observaciones, gt_detalle) VALUES('{}','{}',
                                            '{}','{}', '{}', '{}','{}','{}','{}','{}')'''.format(fechamovim,
                                            meses, fechavto, codcli, nomcli, nomart, totaloper, factura, obser, detalle)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Insertar garantias-", parent=self.master)
            exit()

    def modificar_garantias(self, Id, fechamovim, meses, fechavto, codcli, nomcli, nomart, totaloper, factura, obser,
                            detalle):

        try:
            cur = self.cnn.cursor()
            sql = '''UPDATE garantias SET gt_fechaventa='{}', gt_meses='{}', gt_fechavto='{}', gt_codcli='{}', 
            gt_nomcli='{}', gt_articulo='{}', gt_impventa='{}', gt_factura='{}', gt_observaciones='{}', gt_detalle='{}'
            WHERE Id={}'''.format(fechamovim, meses, fechavto, codcli, nomcli, nomart, totaloper, factura, obser,
                                  detalle, Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Modificar garantias-", parent=self.master)
            exit()

    def eliminar_item_garantia(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM garantias WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Eliminar item garantia-",
                                 parent=self.master)
            exit()

    # 1 uso
    def buscar_entabla(self, argumento):

        """
        Aqui nos llega un string de busqueda y en que campos debemos buscarlo. Devolvemos todos
        los registros que cumplan con la condicion especificada
        """

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Buscar en tabla-",
                                 parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM garantias ORDER BY Id ASC")
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
