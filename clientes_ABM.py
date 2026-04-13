import mysql.connector
from datetime import datetime

class datosClientes:

    def __init__(self, pantalla):

        self.master = pantalla

        # try:
        #     self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        # except Error as ex:
        #     print("Error de conexion: {0}".format(ex))

    def get_connection(self):
        print("OK= Escuchando.....")
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom"
        )

    # def consultar_clientes(self, tofil):
    def consultar_clientes(self, orden=""):

        """👉 buffered=True = MySQL:manda TODO el resultado de una, el cursor lo guarda en memoria.
        ✔ Después podés hacer lo que quieras: otro execute, cerrar cursor, no consumir todo
        SIN errores"""

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "SELECT * FROM clientes"
            if orden:
                # if not orden.upper().startswith("ORDER BY"):
                #     raise ValueError("Solo se permite ORDER BY")
                sql += " " + orden
            # else:
            #     sql += " ORDER BY apellido, nombres ASC"

            cur.execute(sql)
            return cur.fetchall()
        finally:
            cur.close()
            cnn.close()

        # try:
        #     cur.execute("SELECT * FROM clientes "+ tofil)
        #     datos = cur.fetchall()
        #     return datos
        # except Exception:
        #     raise
        # finally:
        #     cur.close()

    def traer_ultimo(self):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            cur.execute("SELECT MAX(codigo) FROM clientes")
            resultado = cur.fetchone()[0]
            return resultado or 0  # 👈 clave
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()

    def insertar_clientes(self, cliente):

        if not cliente.get("codigo"):
            raise ValueError("El código es obligatorio")
        if not cliente.get("apellido"):
            raise ValueError("El apellido es obligatorio")

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            fecha_ingreso = datetime.strptime(cliente["fecha_ingreso"], '%d/%m/%Y')

            sql = """
                  INSERT INTO clientes (codigo, apellido, nombres, direccion, localidad, provincia, postal, \
                                        telef_pers, telef_trab, mail, fecha_ingreso, sit_fis, cuit, \
                                        observaciones, apenombre) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                  """

            valores = (
                cliente["codigo"],
                cliente["apellido"],
                cliente["nombres"],
                cliente["direccion"],
                cliente["localidad"],
                cliente["provincia"],
                cliente["postal"],
                cliente["telef_pers"],
                cliente["telef_trab"],
                cliente["mail"],
                fecha_ingreso,
                cliente["sit_fis"],
                cliente["cuit"],
                cliente["observaciones"],
                cliente["apenombre"]
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

    def modificar_clientes(self, cliente):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            fecha_ingreso = datetime.strptime(cliente["fecha_ingreso"], '%d/%m/%Y')

            # genero instruccion sql
            sql = """
                  UPDATE clientes \
                  SET codigo=%s, \
                      apellido=%s, \
                      nombres=%s, \
                      direccion=%s, \
                      localidad=%s, \
                      provincia=%s, \
                      postal=%s, \
                      telef_pers=%s, \
                      telef_trab=%s, \
                      mail=%s, \
                      fecha_ingreso=%s, \
                      sit_fis=%s, \
                      cuit=%s, \
                      observaciones=%s, \
                      apenombre=%s
                  WHERE Id = %s \
                  """

            # Creo tupla valores a partir del diccionario : dame el valor de la clave cliente[codigo]
            # y asi se genera la tupla
            valores = (
                cliente["codigo"],
                cliente["apellido"],
                cliente["nombres"],
                cliente["direccion"],
                cliente["localidad"],
                cliente["provincia"],
                cliente["postal"],
                cliente["telef_pers"],
                cliente["telef_trab"],
                cliente["mail"],
                fecha_ingreso,
                cliente["sit_fis"],
                cliente["cuit"],
                cliente["observaciones"],
                cliente["apenombre"],
                cliente["Id"]
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

    def eliminar_clientes(self, Id):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = "DELETE FROM clientes WHERE Id = %s"
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

    def buscar_clientes(self, texto):

        cnn = self.get_connection()
        cur = cnn.cursor(buffered=True)
        try:
            sql = """
                  SELECT * FROM clientes WHERE apellido LIKE %s OR nombres LIKE %s OR apenombre LIKE %s
                  ORDER BY apellido, nombres ASC \
                  """

            param = f"%{texto}%"

            cur.execute(sql, (param, param, param))
            datos = cur.fetchall()
            return datos
        except Exception:
            raise
        finally:
            cur.close()
            cnn.close()
