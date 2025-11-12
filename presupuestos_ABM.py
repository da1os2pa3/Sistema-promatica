from tkinter import messagebox
# -----------------------------------
import mysql.connector
from mysql.connector import Error
# -----------------------------------
#from datetime import datetime

class datosPresupuestos:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_presupuestos()
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_presupuestos(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-presupuestos",
                                 parent=self.master)
            exit()

    def consultar_informa(self):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos_inf
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-informa",
                                 parent=self.master)
            exit()

    def consultar_articulo(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-articulo",
                                 parent=self.master)
            exit()

    def consultar_detalle_auxpresup(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-detalle auxpresup",
                                 parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM resu_presup ORDER BY rp_numero ASC")
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Traer ultimo",
                                 parent=self.master)
            exit()

    def vaciar_auxpresup(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("DELETE FROM " + tofil)
            self.cnn.commit()
            cur.close()
            return
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Vaciar auxpresup-",
                                 parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        try:
            # Busca un strin en los campos indicados en una tabla
            cur = self.cnn.cursor()
            if len(argumento) > 0:
                cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Buscar en tabla-",
                                 parent=self.master)
            exit()

    def insertar_auxpresup(self, proveedor, codcomponente, componente, tasaiva, cantidad, netodolar, totpresup, totredondo,
                                 totganancia, totcostos):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO aux_presup (ax_proved, ax_codcomp, ax_componente, ax_iva, ax_cantidad, ax_neto_dolar, 
                                             ax_total_presup, ax_total_redondo, ax_total_ganancia, ax_total_costos) 
                                             VALUES('{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}')'''.format(proveedor,
                                             codcomponente, componente, tasaiva, cantidad, netodolar, totpresup, totredondo,
                                             totganancia, totcostos)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Insertar auxpresup-",
                                 parent=self.master)
            exit()


    def insertar_detapresup(self, nroventa, proveedor, codigo_comp_proved, componente, tasaiva, cantidad, costo_neto_dolar, total_redondo):

        # Inserta los componentes presupuestados la tabla de detalle de los presupuestos realizados
        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO deta_presup (dp_numero, dp_proved, dp_codcomp, dp_componente, dp_iva, dp_cantidad, 
                                              dp_neto_dolar, dp_redondo) VALUES('{}','{}','{}','{}','{}', '{}','{}',
                                              '{}')'''.format(nroventa, proveedor, codigo_comp_proved, componente,
                                                              tasaiva, cantidad, costo_neto_dolar, total_redondo)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Insertar detapresup-",
                                 parent=self.master)
            exit()

    def insertar_resupresup(self, nroventa, fechavta, codcli, nomcli, sitfiscal, cuit, dolarhoy, tasaganancia, total_real,
                            total_redondo, forma_pago, detapago, detalle):

        try:
            # Inserta en la tabla de resumen de ventas realizadas el registro con los datos base de la venta
            cur = self.cnn.cursor()
            sql = '''INSERT INTO resu_presup (rp_numero, rp_fecha, rp_codcli, rp_nomcli, rp_sitfiscal, rp_cuit, rp_valor_dolar, rp_tasa_gan, 
                                              rp_total_real, rp_total_redondo, rp_forma_pago, rp_detalle_pago, rp_detalle) 
                                              VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',
                                              '{}','{}')'''.format(nroventa, fechavta, codcli, nomcli, sitfiscal, cuit,
                                              dolarhoy, tasaganancia, total_real, total_redondo, forma_pago, detapago, detalle)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Insertar resupresup-",
                                 parent=self.master)
            exit()

    def eliminar_auxpresup(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM aux_presup WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Eliminar auxpresup-",
                                 parent=self.master)
            exit()

    def eliminar_detapresup(self, nroventa):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM deta_presup WHERE dp_numero = {}'''.format(nroventa)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Eliminar detapresup-",
                                 parent=self.master)
            exit()

    def eliminar_resupresup2(self, nroventa):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM resu_presup WHERE rp_numero = {}'''.format(nroventa)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Eliminar resupresup2-",
                                 parent=self.master)
            exit()

    def eliminar_resupresup1(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM resu_presup WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Eliminar resupresup1-",
                                 parent=self.master)
            exit()

    def traer_resu_presup(self,nroventa):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM resu_presup WHERE rp_numero = " + nroventa)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchone()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Traer resupresup-",
                                 parent=self.master)
            exit()

    def traer_deta_presup(self,nropresup):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM deta_presup WHERE dp_numero = " + nropresup)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Traer detapresup-",
                                 parent=self.master)
            exit()
