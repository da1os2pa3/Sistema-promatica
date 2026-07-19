import mysql.connector
from datetime import datetime
from tkinter import messagebox


class datosGarantias:

    def __init__(self, pantalla):

        self.master = pantalla

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_garantia(self, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM garantias"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()
    # 1 uso
    def consultar_informa(self):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            return datos_inf
        finally:
            cur.close()
            cnn.close()

    def insertar_garantias(self, val_garantias):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            aux_fecha_venta = datetime.strptime(val_garantias["gt_fechaventa"], '%d/%m/%Y')
            aux_fecha_vto = datetime.strptime(val_garantias["gt_fechavto"], '%d/%m/%Y')

            sql = """
                  INSERT INTO garantias (gt_fechaventa, gt_meses, gt_fechavto, gt_codcli, gt_nomcli, gt_articulo, 
                                       gt_impventa, gt_factura, gt_observaciones, gt_detalle) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                  """

            # Genero una tupla ("valores") con los valores que vienen en el parametro (diccionario)
            valores = (
                aux_fecha_venta,
                val_garantias["gt_meses"],
                aux_fecha_vto,
                val_garantias["gt_codcli"],
                val_garantias["gt_nomcli"],
                val_garantias["gt_articulo"],
                val_garantias["gt_impventa"],
                val_garantias["gt_factura"],
                val_garantias["gt_observaciones"],
                val_garantias["gt_detalle"]
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

    def modificar_garantias(self, val_garantias):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            aux_fecha_venta = datetime.strptime(val_garantias["gt_fechaventa"], '%d/%m/%Y')
            aux_fecha_vto = datetime.strptime(val_garantias["gt_fechavto"], '%d/%m/%Y')

            sql = """
                  UPDATE garantias 
                  SET gt_fechaventa=%s, gt_meses=%s, gt_fechavto=%s, gt_codcli=%s, gt_nomcli=%s, gt_articulo=%s, 
                      gt_impventa=%s, gt_factura=%s, gt_observaciones=%s, gt_detalle=%s
                  WHERE Id = %s 
                  """

            # Genero una tupla ("valores") con los valores que vienen en el parametro (diccionario)
            valores = (
                aux_fecha_venta,
                val_garantias["gt_meses"],
                aux_fecha_vto,
                val_garantias["gt_codcli"],
                val_garantias["gt_nomcli"],
                val_garantias["gt_articulo"],
                val_garantias["gt_impventa"],
                val_garantias["gt_factura"],
                val_garantias["gt_observaciones"],
                val_garantias["gt_detalle"],
                val_garantias["Id"]
            )
            cur.execute(sql, valores)
            cnn.commit()
            return
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_item_garantia(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM garantias WHERE Id = %s"
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (Id,))
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    # 1 uso
    def buscar_entabla(self, texto):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  SELECT * FROM garantias WHERE gt_nomcli LIKE %s OR gt_articulo LIKE %s ORDER BY gt_fechavto ASC 
                  """

            """ Como paso un solo parametro, debo colocar la coma al final para que se interprete como una tupla, sino, 
            lo toma como un string. Si vinieran mas parametros separados por coma ya se da cuenta que es una tupla"""
            param = f"%{texto}%"
            #param = (f"%{texto}%",)

            cur.execute(sql, (param, param))
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

        # """
        # Aqui nos llega un string de busqueda y en que campos debemos buscarlo. Devolvemos todos
        # los registros que cumplan con la condicion especificada
        # """
        # try:
        #     cur = self.cnn.cursor()
        #     cur.execute("SELECT * FROM " + argumento)
        #     datos = cur.fetchall()
        #     self.cnn.commit()
        #     cur.close()
        #     return datos
        # except:
        #
        #     messagebox.showerror("Error inesperado", "Contacte asistencia-Buscar en tabla-",
        #                          parent=self.master)
        #     exit()












    # def traer_ultimo(self, xparametro):
    #
    #     try:
    #         cur = self.cnn.cursor()
    #         cur.execute("SELECT * FROM garantias ORDER BY Id ASC")
    #         datos = cur.fetchall()
    #         aux = ""
    #         for row in datos:
    #             if xparametro == 1:
    #                 aux = str(row[1]) + "\n"
    #             else:
    #                 aux = str(row[0]) + "\n"
    #         self.cnn.commit()
    #         cur.close()
    #         return aux
    #     except:
    #         messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=traer ultimo",
    #                              parent=self.master)
    #         exit()
