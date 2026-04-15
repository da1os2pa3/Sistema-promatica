import mysql.connector
from mysql.connector import Error
from datetime import datetime
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

    def get_connection(self):
        print("OK= Escuchando.....")
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom"
        )

    def consultar_planilla(self, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM planicaja"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def combo_input(self, xcampo, xtabla, xorden):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            # cur = self.cnn.cursor()
            cur.execute("SELECT " + xcampo + " FROM " + xtabla + " ORDER BY " + xorden)
            result = cur.fetchall()
            return result
        except Exception as e:
            raise
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM planicaja " + argumento)
            datos = cur.fetchall()
            return datos
        except Exception as e:
            raise
        finally:
            cur.close()
            cnn.close()

    def consultar_informa(self):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            return datos_inf
        except Exception as e:
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_item_planilla(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = '''DELETE FROM planicaja WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_planilla(self, planilla):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  INSERT INTO planicaja (pl_fecha, pl_tipomov, pl_detalle, pl_cantidad, pl_ingresos, pl_egreso, pl_costo, \
                                        pl_pagoscta, pl_compras, pl_cliente, pl_tipopago, pl_detapago, pl_garantia, \
                                        pl_observacion, pl_proved, pl_ctacte, pl_clavemov, pl_codcli) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                  """

            valores = (
                planilla["pl_fecha"],
                planilla["pl_tipomov"],
                planilla["pl_detalle"],
                planilla["pl_cantidad"],
                planilla["pl_ingresos"],
                planilla["pl_egreso"],
                planilla["pl_costo"],
                planilla["pl_pagoscta"],
                planilla["pl_compras"],
                planilla["pl_cliente"],
                planilla["pl_tipopago"],
                planilla["pl_detapago"],
                planilla["pl_garantia"],
                planilla["pl_observacion"],
                planilla["pl_proved"],
                planilla["pl_ctacte"],
                planilla["pl_clavemov"],
                planilla["pl_codcli"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo cliente
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def modificar_planilla(self, planilla):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            # # Convierto fecha nuevamente de String a Datetime para guardar en SQL  ------------------------
            # algo = fechapla
            # fechapla = datetime.strptime(algo, '%d/%m/%Y')

            sql = ('''UPDATE planicaja 
                SET pl_fecha=%s, 
                    pl_tipomov=%s,
                    pl_detalle=%s, 
                    pl_cantidad=%s, 
                    pl_ingresos=%s, 
                    pl_egreso=%s, 
                    pl_costo=%s, 
                    pl_pagoscta=%s, 
                    pl_compras=%s, 
                    pl_cliente=%s,
                    pl_tipopago=%s, 
                    pl_detapago=%s,
                    pl_garantia=%s,
                    pl_observacion=%s,
                    pl_proved=%s,
                    pl_ctacte=%s,
                    pl_clavemov=%s,
                    pl_codcli=%s
                WHERE Id=%s''')

            valores = (
                planilla["pl_fecha"],
                planilla["pl_tipomov"],
                planilla["pl_detalle"],
                planilla["pl_cantidad"],
                planilla["pl_ingresos"],
                planilla["pl_egreso"],
                planilla["pl_costo"],
                planilla["pl_pagoscta"],
                planilla["pl_compras"],
                planilla["pl_cliente"],
                planilla["pl_tipopago"],
                planilla["pl_detapago"],
                planilla["pl_garantia"],
                planilla["pl_observacion"],
                planilla["pl_proved"],
                planilla["pl_ctacte"],
                planilla["pl_clavemov"],
                planilla["pl_codcli"],
                planilla["Id"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo cliente
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

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
            cur.close()
            if aux == "":
                aux = 0
            return aux
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Traer ultimo-", parent=self.master)
            exit()
