import mysql.connector
from datetime import datetime

class DatosPresupuestos:

    def __init__(self, pantalla):

        self.master = pantalla

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    """ tengo un filtro para resu_presup y otro para auxiliar
    tengo que hacer dos consultar presupuesto"""

    def consultar_presupuestos(self, tabla, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql=""
            if tabla == "resu_presup":
                sql = "SELECT * FROM resu_presup"
                if orden:
                    sql += " " + orden
            if tabla == "aux_presup":
                sql = "SELECT * FROM aux_presup"
                if orden:
                    sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def consultar_informa(self, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM informa WHERE 1"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def consultar_detalle_auxpresup(self, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM aux_presup WHERE 1"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

    def traer_ultimo(self, xparametro):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM resu_presup ORDER BY Id DESC LIMIT 1")
            row = cur.fetchone()
            if row is None:
                return 0
            if xparametro == 1:
                return str(row[1])
            else:
                return str(row[0])
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def vaciar_auxpresup(self, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM aux_presup"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            cnn.commit()
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, texto):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  SELECT * FROM resu_presup WHERE rp_nomcli LIKE %s ORDER BY rp_fecha ASC
                  """
            #param = f"%{texto}%"
            param = (f"%{texto}%",)
            cur.execute(sql, param)
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_auxpresup(self, diccionario):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = '''INSERT INTO aux_presup (ax_orden, ax_proved, ax_codcomp, ax_componente, ax_iva, ax_cantidad, 
                                             ax_neto_dolar, ax_total_presup, ax_total_redondo, ax_total_ganancia, 
                                             ax_total_costos) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            valores = (
                diccionario["ax_orden"],
                diccionario["ax_proved"],
                diccionario["ax_codcomp"],
                diccionario["ax_componente"],
                diccionario["ax_iva"],
                diccionario["ax_cantidad"],
                diccionario["ax_neto_dolar"],
                diccionario["ax_total_presup"],
                diccionario["ax_total_redondo"],
                diccionario["ax_total_ganancia"],
                diccionario["ax_total_costos"]
            )
            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo registro (aqui no sirve)
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_detapresup(self, diccionario):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        # Inserta los componentes presupuestados la tabla de detalle de los presupuestos realizados
        try:
            sql = '''INSERT INTO deta_presup (dp_orden, dp_numero, dp_proved, dp_codcomp, dp_componente, dp_iva, 
                                              dp_cantidad, dp_neto_dolar, dp_redondo) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            valores = (
                diccionario["dp_orden"],
                diccionario["dp_numero"],
                diccionario["dp_proved"],
                diccionario["dp_codcomp"],
                diccionario["dp_componente"],
                diccionario["dp_iva"],
                diccionario["dp_cantidad"],
                diccionario["dp_neto_dolar"],
                diccionario["dp_redondo"]
            )

            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo registro (aqui no sirve)
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_presu_entregado(self, diccionario):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:

            fecha_aux = datetime.strptime(diccionario["rp_fecha"], '%d/%m/%Y')

            # Inserta en la tabla de resumen de ventas realizadas el registro con los datos base de la venta
            sql = '''INSERT INTO resu_presup (rp_numero, rp_fecha, rp_codcli, rp_nomcli, rp_sitfiscal, rp_cuit, 
                                              rp_valor_dolar, rp_tasa_gan, rp_total_real, rp_total_redondo, 
                                              rp_forma_pago, rp_detalle_pago, rp_detalle, rp_aceptado) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

            valores = (
                diccionario["rp_numero"],
                #diccionario["rp_fecha"],
                fecha_aux,
                diccionario["rp_codcli"],
                diccionario["rp_nomcli"],
                diccionario["rp_sitfiscal"],
                diccionario["rp_cuit"],
                diccionario["rp_valor_dolar"],
                diccionario["rp_tasa_gan"],
                diccionario["rp_total_real"],
                diccionario["rp_total_redondo"],
                diccionario["rp_forma_pago"],
                diccionario["rp_detalle_pago"],
                diccionario["rp_detalle"],
                diccionario["rp_aceptado"]
            )
            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo registro - aqui no sirve
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    # Elimina un solo registro - usada desde finsertar_item_auxpresup
    def eliminar_auxpresup(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            #sql = '''DELETE FROM aux_presup WHERE Id = {}'''.format(Id)
            sql = "DELETE FROM aux_presup WHERE Id = %s"
            cur.execute(sql, (Id,))
            cnn.commit()
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_detapresup(self, nropresup):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM deta_presup WHERE dp_numero = %s"
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (nropresup,))
            cnn.commit()
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_presu_entregado2(self, nropresup):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM resu_presup WHERE rp_numero = %s"
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (nropresup,))
            cnn.commit()
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_presu_entregado1(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM resu_presup WHERE Id = %s"
            cur.execute(sql, (Id,))
            cnn.commit()
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def traer_resu_presup(self,nroventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM resu_presup WHERE rp_numero = " + nroventa)
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchone()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def traer_deta_presup(self,nropresup):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM deta_presup WHERE dp_numero = " + nropresup + " ORDER BY dp_numero, dp_orden")
            # para recuperar todas filas de una tabla de base de datos
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def marcar_presup_aceptado(self,id_tabla, estado):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("UPDATE resu_presup SET rp_aceptado = %s WHERE id = %s",(estado, id_tabla))
            cnn.commit()
        except Exception:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def actualizar_auxpresup(self, grid):

        """
            En resumen, la lógica general es:
            Leer todas las filas del Grid.
            Construir una lista de tuplas.
            Borrar la tabla aux_presup.
            Insertar nuevamente todas las filas.
            Hacer commit().
            Si algo falla, hacer rollback().
            Cerrar cursor y conexión.
        """

        cnn = self.get_connection()
        cur = cnn.cursor()

        sql = """
              INSERT INTO aux_presup (id, ax_orden, ax_proved, ax_codcomp, ax_componente, ax_iva, ax_cantidad, 
                                      ax_neto_dolar, ax_total_presup, ax_total_redondo, ax_total_ganancia, ax_total_costos) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
              """

        datos_total = []

        # Recorro todas las filas del Grid y agrega un contador
        for i, item in enumerate(grid.get_children(), start=1):

            """
            i = 1, item = 'I001'
            i = 2, item = 'I002'
            i = 3, item = 'I003'
            """

            # Aca cargo valores de la fila con los items del grid en una "LISTA" y guardo la clave del item del grid
            clave = grid.item(item, "text")
            valores = list(grid.item(item, "values"))

            # Reemplaza el primer valor por el numero de orden
            """
            Ejemplo:
            Antes: [99, "Proveedor", "ABC"]
            Después:[1, "Proveedor", "ABC"]
            """
            valores[0] = i  # asegurar orden correcto

            # Comprueba que existan exactamente 11 valores.
            if len(valores) != 11:
                print("Error en fila:", valores)
                continue

            """
                valores es (seguramente) una tupla.
                El *valores la desempaqueta.
                Entonces estás creando una tupla nueva que queda así:
                (clave, valor1, valor2, valor3, ...)
                y la agregás a datos_total.
                🔹 Ejemplo concreto
                clave = 10
                valores = ("A", "B", "C")
                datos_total = []
                datos_total.append((clave, *valores))
                Resultado:
                datos_total = [(10, "A", "B", "C")]
            """

            datos_total.append((clave, *valores))

        try:
            # Borra todos los registros antes de volver a insertar el grid actual
            cur.execute("DELETE FROM aux_presup")
            # Ejecuta el insert muchas veces
            cur.executemany(sql, datos_total)
            cnn.commit()
        except Exception:
            """
                Revierte todos los cambios NO confirmados desde el último commit().
                👉 O sea:
                Si hiciste INSERT, UPDATE o DELETE
                Pero todavía no hiciste commit()
                Entonces:
                self.cnn.rollback()
                👉 deja la base como si nunca hubieras ejecutado esas operaciones.
            """
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()
