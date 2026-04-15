import mysql.connector

class datosArtic:

    def __init__(self, pantalla):

        self.master = pantalla

    def get_connection(self):
        print("OK= Escuchando.....")
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom"
        )

    def consultar_articulo(self, orden=""):

        """
        # cursor.fetchall() recupera todas las filas del resultado de una consulta. Devuelve todas
        # las filas como una "lista". Se devuelve una lista vacía si no hay ningún registro para recuperar.
        # cursor.fetchmany(size)devuelve el número de filas especificadas por size el argumento. Cuando
        # se llama repetidamente, este método recupera el siguiente conjunto de filas del resultado de una
        # consulta y devuelve una lista de tuplas. Si no hay más filas disponibles, devuelve una lista vacía.
        # cursor.fetchone()El método devuelve un solo registro o Ninguno si no hay más filas disponibles.
        """

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM articulos"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

        # try:
        #     cur.execute("SELECT * FROM " + tofil)
        #     datos = cur.fetchall()
        #     self.cnn.commit()
        #     return datos
        # except Exception:
        #     raise
        # finally:
        #     cur.close()
        #     self.cnn.close()
        #

    def insertar_articulo(self, articulo):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  INSERT INTO articulos (codigo, descripcion, marca, rubro, codbar, costodolar, iva, \
                                        impint, porcgan, observa, ultact, costohist, imagen) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                  """

            valores = (
                articulo["codigo"],
                articulo["descripcion"],
                articulo["marca"],
                articulo["rubro"],
                articulo["codbar"],
                articulo["costodolar"],
                articulo["iva"],
                articulo["impint"],
                articulo["porcgan"],
                articulo["observa"],
                articulo["ultact"],
                articulo["costohist"],
                articulo["imagen"]
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

    def modificar_articulo(self, articulo):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = ('''UPDATE articulos 
                SET codigo=%s, 
                    descripcion=%s,
                    marca=%s, 
                    rubro=%s, 
                    codbar=%s, 
                    costodolar=%s, 
                    iva=%s, 
                    impint=%s, 
                    porcgan=%s, 
                    observa=%s,
                    ultact=%s, 
                    costohist=%s,
                    imagen=%s
                WHERE Id=%s''')

            valores = (
                articulo["codigo"],
                articulo["descripcion"],
                articulo["marca"],
                articulo["rubro"],
                articulo["codbar"],
                articulo["costodolar"],
                articulo["iva"],
                articulo["impint"],
                articulo["porcgan"],
                articulo["observa"],
                articulo["ultact"],
                articulo["costohist"],
                articulo["imagen"],
                articulo["Id"]
            )

            cur.execute(sql, valores)
            #n = cur.rowcount
            cnn.commit()
            return
        except Exception as e:
            cnn.rollback()
            raise
        finally:
            cur.close()
            cnn.close()

    def eliminar_articulo(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = '''DELETE FROM articulos WHERE Id = {}'''.format(Id)
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

    def consultar_informa(self):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            # Devuelve el registro de la tabla Informa
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchall()
            return datos_inf
        except Exception as e:
            raise
        finally:
            cur.close()
            cnn.close()

    def buscar_entabla(self, argumento):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT * FROM articulos " + argumento)
            datos = cur.fetchall()
            return datos
        except Exception as e:
            raise
        finally:
            cur.close()
            cnn.close()

    def combo_input(self, xcampo, xtabla, xorden):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            """ Llenar un combobox con datos de una tabla. Paso el campo, la tabla y el orden de los datos """
            cur.execute("SELECT " + xcampo + " FROM " + xtabla + " ORDER BY " + xorden)
            result = cur.fetchall()
            return result
        except Exception as e:
            raise
        finally:
            cur.close()
            cnn.close()

    # except Exception as e:
    # messagebox.showerror("Error", str(e))

    # def traer_ultimo(self, xparametro):
    #
    #     """ Devuelve el Id. del ultimo registro de la tabla (primer valor autocompletado por la tabla) """
    #
    #     cnn = self.get_connection()
    #     cur = cnn.cursor(buffered=True)
    #     try:
    #         cur.execute("SELECT * FROM articulos ORDER BY Id")
    #         datos = cur.fetchall()
    #         aux = ""
    #         for row in datos:
    #             if xparametro == 1:
    #                 aux = str(row[1]) + "\n"
    #             else:
    #                 aux = str(row[0]) + "\n"
    #         cnn.commit()
    #         if aux == "":
    #             aux = 0
    #         return aux
    #     except Exception:
    #         raise
    #     finally:
    #         cur.close()
    #         cnn.close()
