import mysql.connector
from mysql.connector import Error
# ---------------------------------------
from datetime import datetime
# ---------------------------------------
from tkinter import messagebox

class datosPlanilla:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))
            messagebox.showerror("Error inesperado", "Contacte asistencia-Error conexion base de datos-",
                                 parent=self.master)
            exit()

    # def __str__(self):
    #
    #     datos = self.consultar_planilla("")
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_planilla(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM " + tofil)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Consultar planilla-", parent=self.master)
            exit()

    def combo_input(self, xcampo, xtabla, xorden):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT " + xcampo + " FROM " + xtabla + " ORDER BY " + xorden)
            result = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return result
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-combo input-", parent=self.master)
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Buscar en tabla-", parent=self.master)
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
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-combo input-", parent=self.master)
            exit()

    def eliminar_item_planilla(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM planicaja WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Eliminar item planilla-",
                                 parent=self.master)
            exit()

    def insertar_planilla(self, fecha, tipomov, detalle, cantidad, ingreso, egreso, costo, pagoscta, compras, cliente,
                          tipopago, detapago, garantia, observaciones, proved, ctacte, clavemovim, codcli):

        try:
            cur = self.cnn.cursor()

            sql = '''INSERT INTO planicaja (pl_fecha, pl_tipomov, pl_detalle, pl_cantidad, pl_ingresos, pl_egreso,
            pl_costo, pl_pagoscta, pl_compras, pl_cliente, pl_tipopago, pl_detapago, pl_garantia, pl_observacion, 
            pl_proved, pl_ctacte, pl_clavemov, pl_codcli) VALUES('{}','{}','{}','{}', '{}', '{}','{}','{}','{}','{}',
            '{}', '{}','{}', '{}', '{}','{}','{}','{}')'''.format(fecha, tipomov,detalle, cantidad, ingreso,
                                                                  egreso, costo, pagoscta, compras, cliente, tipopago,
                                                                  detapago, garantia, observaciones, proved, ctacte,
                                                                  clavemovim, codcli)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Insertar planilla-", parent=self.master)
            exit()

    def modificar_planilla(self, Id, fechapla, tipomov, detalle, cantidad, ingreso, egreso, costo, pagoscta, compras,
                           cliente, tipopago, detapago, garantia, observaciones, proved, ctacte, clavemovim, codcli):

        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
            algo = fechapla
            fechapla = datetime.strptime(algo, '%d/%m/%Y')

            cur = self.cnn.cursor()
            sql = '''UPDATE planicaja SET pl_fecha='{}', pl_tipomov='{}', pl_detalle='{}', pl_cantidad='{}', 
            pl_ingresos='{}', pl_egreso='{}', pl_costo='{}', pl_pagoscta='{}', pl_compras='{}', pl_cliente='{}', 
            pl_tipopago='{}', pl_detapago='{}', pl_garantia='{}', pl_observacion='{}', pl_proved='{}', 
            pl_ctacte='{}', pl_clavemov='{}', pl_codcli='{}'
            WHERE Id={}'''.format(fechapla, tipomov, detalle, cantidad, ingreso, egreso, costo, pagoscta, compras,
                                  cliente, tipopago, detapago, garantia, observaciones, proved, ctacte, clavemovim,
                                  codcli, Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Modificar planilla-", parent=self.master)
            exit()

    def insertar_ctacte(self, fecha, detalle, ingreso, egreso, codcli, nomcli, clavemov):

        try:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO ctacte (cc_fecha, cc_detalle, cc_ingreso, cc_egreso, cc_codcli, cc_nomcli, 
                                         cc_clavemov) VALUES('{}','{}','{}','{}', '{}', '{}',
                                         '{}')'''.format(fecha, detalle, ingreso, egreso, codcli,
                                                         nomcli, clavemov)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Insertar ctacte-", parent=self.master)
            exit()

    def eliminar_item_ctacte_xmodif(self, clave_movimiento):

        """ Este metodo elimina el movimiento en cuenta corriente corresondiente a la clave de movimiento pasada
        como parametro, esto pasa cuando se modifica un item de planilla de caja con imputacion a cuenta corriente """

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM ctacte WHERE cc_clavemov = ''' + clave_movimiento
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Eliminar_item_ctacte_xmodif-", parent=self.master)
            exit()

    def eliminar_item_ctacte(self, Id):

        try:
            cur = self.cnn.cursor()
            sql = '''DELETE FROM planicaja WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Eliminar item ctacte-", parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM planicaja ORDER BY pl_fecha ASC")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = (str(row[1]))
                           #+ "\n")
                else:
                    aux = (str(row[0]))
                           #+ "\n")
            self.cnn.commit()
            cur.close()
            if aux == "":
                aux = 0
            return aux
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Traer ultimo-", parent=self.master)
            exit()
