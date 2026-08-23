import mysql.connector
from mysql.connector import Error
from datetime import datetime

class datosCotiz:

    def __init__(self, pantalla):
        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root",
            passwd="", database="sist_prom")
            self.master = pantalla
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom")

    def consultar_tablas(self, tabla, orden=""):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            if tabla == "aux":
                sql = "SELECT * FROM aux_ventas"
            if tabla == "resu":
                sql = "SELECT * FROM resu_ventas"
            if tabla == "deta":
                sql = "SELECT * FROM deta_ventas"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
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
        finally:
            cur.close()
            cnn.close()

    # ----------------------------------------------------------------
    # CRUD
    # ----------------------------------------------------------------

    # Inserta los datos de un nuevo articulo en la tabla aux_ventas para ser vistos en el GRID auxiliar
    def insertar_auxventa(self, dic_auxventas):

      cnn = self.get_connection()
      cur = cnn.cursor(buffered=True)
      try:
          sql = """
                INSERT INTO aux_ventas (av_codigo_art, av_desc_art, av_marca_art, av_cantidad, av_tot_uni_conta, 
                                        av_tot_uni_lista, av_neto_unidad, av_impor_iva21, av_impor_iva105, 
                                        av_impor_ganancia, av_costo_dolar, av_costo_bruto, av_tasaiva)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
          valores = (
              dic_auxventas["av_codigo_art"],
              dic_auxventas["av_desc_art"],
              dic_auxventas["av_marca_art"],
              dic_auxventas["av_cantidad"],
              dic_auxventas["av_tot_uni_conta"],
              dic_auxventas["av_tot_uni_lista"],
              dic_auxventas["av_neto_unidad"],
              dic_auxventas["av_impor_iva21"],
              dic_auxventas["av_impor_iva105"],
              dic_auxventas["av_impor_ganancia"],
              dic_auxventas["av_costo_dolar"],
              dic_auxventas["av_costo_bruto"],
              dic_auxventas["av_tasaiva"]
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

    def insertar_resuventa(self, resuventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            fecha = datetime.strptime(resuventa["rv_fecha"], '%d/%m/%Y')
            sql = """
                  INSERT INTO resu_ventas(rv_numero, rv_fecha, rv_cod_cliente, rv_cliente, rv_sitfis, rv_cuit, 
                                          rv_tipo_pago, rv_detalle_pago, rv_dolarhoy, rv_total) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
            valores = (
                resuventa["rv_numero"],
                fecha,
                resuventa["rv_cod_cliente"],
                resuventa["rv_cliente"],
                resuventa["rv_sitfis"],
                resuventa["rv_cuit"],
                resuventa["rv_tipo_pago"],
                resuventa["rv_detalle_pago"],
                resuventa["rv_dolarhoy"],
                resuventa["rv_total"]
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

    # Inserta los articulos vendidos en la tabla de detalle de las ventas realizadas
    def insertar_detaventa(self, detaventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
        # aa = 0
        # if aa == 0:
            #fecha_ingreso = datetime.strptime(resuventa["rv_fecha"], '%d/%m/%Y')
            sql = """
                  INSERT INTO deta_ventas(dv_numero, dv_codigo_art, dv_desc_art, dv_marca_art, dv_cantidad, 
                                          dv_tot_uni_conta, dv_tot_uni_lista, dv_neto_venta, dv_impor_iva21, 
                                          dv_impor_iva105, dv_impor_ganancia, dv_costo_dolar, dv_costo_bruto, 
                                          dv_tasaiva)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
            valores = (
                detaventa["dv_numero"],
                #fecha_ingreso,
                detaventa["dv_codigo_art"],
                detaventa["dv_desc_art"],
                detaventa["dv_marca_art"],
                detaventa["dv_cantidad"],
                detaventa["dv_tot_uni_conta"],
                detaventa["dv_tot_uni_lista"],
                detaventa["dv_neto_venta"],
                detaventa["dv_impor_iva21"],
                detaventa["dv_impor_iva105"],
                detaventa["dv_impor_ganancia"],
                detaventa["dv_costo_dolar"],
                detaventa["dv_costo_bruto"],
                detaventa["dv_tasaiva"]
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

    def modificar_resuventa(self, dic_resuventas):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            fecha_venta = datetime.strptime(dic_resuventas["rv_fecha"], '%d/%m/%Y')

            # genero instruccion sql
            sql = """
                  UPDATE resu_ventas
                  SET rv_numero=%s, rv_fecha=%s, rv_cod_cliente=%s, rv_cliente=%s, rv_sitfis=%s, rv_cuit=%s, 
                      rv_tipo_pago=%s, rv_detalle_pago=%s, rv_dolarhoy=%s, rv_total=%s
                  WHERE Id = %s \
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
            # y asi se genera la tupla
            valores = (
                dic_resuventas["rv_numero"],
                fecha_venta,
                dic_resuventas["rv_cod_cliente"],
                dic_resuventas["rv_cliente"],
                dic_resuventas["rv_sitfis"],
                dic_resuventas["rv_cuit"],
                dic_resuventas["rv_tipo_pago"],
                dic_resuventas["rv_detalle_pago"],
                dic_resuventas["rv_dolarhoy"],
                dic_resuventas["rv_total"],
                dic_resuventas["Id"]
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

    def modificar_auxventa(self, dic_auxventas):

      cnn = self.get_connection()
      cur = cnn.cursor(buffered=True)
      try:
          sql = """
                UPDATE aux_ventas SET av_codigo_art=%s, av_desc_art=%s, av_marca_art=%s, av_cantidad=%s, 
                                      av_tot_uni_conta=%s, av_tot_uni_lista=%s, av_neto_unidad=%s, av_impor_iva21=%s, 
                                      av_impor_iva105=%s, av_impor_ganancia=%s, av_costo_dolar=%s, av_costo_bruto=%s, 
                                      av_tasaiva=%s
                WHERE Id = %s 
                """
          valores = (
              dic_auxventas["av_codigo_art"],
              dic_auxventas["av_desc_art"],
              dic_auxventas["av_marca_art"],
              dic_auxventas["av_cantidad"],
              dic_auxventas["av_tot_uni_conta"],
              dic_auxventas["av_tot_uni_lista"],
              dic_auxventas["av_neto_unidad"],
              dic_auxventas["av_impor_iva21"],
              dic_auxventas["av_impor_iva105"],
              dic_auxventas["av_impor_ganancia"],
              dic_auxventas["av_costo_dolar"],
              dic_auxventas["av_costo_bruto"],
              dic_auxventas["av_tasaiva"],
              dic_auxventas["Id"]
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

    def eliminar_auxventa(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM aux_ventas WHERE Id = %s"
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

    # esta elimina el ancabezado de la venta por el Id que le pasemos del registro
    def eliminar_resuventa(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM resu_ventas WHERE Id = %s"
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

    # esta elimina el ancabezado de la venta por numero de venta
    def eliminar_resuventa2(self, nroventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM resu_ventas WHERE rv_numero = %s"
            #sql = "DELETE FROM resu_ventas WHERE rv_numero = {}'''.format(nroventa)
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (nroventa,))
            n = cur.rowcount
            cnn.commit()
            return n
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_detaventa(self, nroventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM deta_ventas WHERE dv_numero = %s"
            #sql = "DELETE FROM resu_ventas WHERE rv_numero = {}'''.format(nroventa)
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (nroventa,))
            cnn.commit()
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    # ----------------------------------------------------------------
    # VACIADOS
    # ----------------------------------------------------------------

    def vaciar_auxventas(self, tofil):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("DELETE FROM aux_ventas")
            cnn.commit()
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()


    # ----------------------------------------------------------------
    # BUSQUEDAS
    # ----------------------------------------------------------------

    # busca en tabla resu_venta
    def buscar_entabla(self, texto):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  SELECT * FROM resu_ventas WHERE rv_cliente LIKE %s
                  """

            param = f"%{texto}%"

            cur.execute(sql, (param,))
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    # ----------------------------------------------------------------
    # TRAER DATOS
    # ----------------------------------------------------------------

    def traer_ultimo(self, xparametro):

        """ Devuelve el Id. del ultimo registro de la tabla (primer valor autocompletado por la tabla) """

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM resu_ventas ORDER BY rv_numero ASC")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = str(row[1]) + "\n"
                else:
                    aux = str(row[0]) + "\n"
            if aux == "":
                aux = 0
            return aux
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def traer_resu_venta(self,nroventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM resu_ventas WHERE rv_numero = " + nroventa)
            datos = cur.fetchone()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def traer_deta_venta(self,nroventa):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM deta_ventas WHERE dv_numero = " + nroventa)
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()


    # ----------------------------------------------------------------
    # OTRAS
    # ----------------------------------------------------------------

    # Llenar un combobox con datos xe una tabla
    def combo_input(self, xcampo, xtabla, xorden):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT " + xcampo + " FROM " + xtabla + " ORDER BY " + xorden)
            result = cur.fetchall()
            return result
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()
