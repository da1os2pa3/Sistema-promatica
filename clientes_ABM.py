import mysql.connector
from mysql.connector import Error
# ----------------------------------------
from datetime import datetime
# ----------------------------------------
from tkinter import messagebox

class datosClientes:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_clientes("")
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_clientes(self, tofil):

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM "+ tofil)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Consultar-",
                                 parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        # Trae el último código de cliente en la tabla para proponer el nuevo número en alta

        try:
            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM clientes ORDER BY codigo ASC")
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

    def buscar_entabla(self, argumento):

        try:
            cur = self.cnn.cursor()
            if len(argumento) <= 0:
                return
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos
        except:
            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=buscar_entabla",
                                 parent=self.master)
            exit()

    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # CRUD
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    def insertar_clientes(self, cliente):

        try:
            fecha_ingreso = datetime.strptime(cliente["fecha_ingreso"], '%d/%m/%Y')

            cur = self.cnn.cursor()

            sql = """
                  INSERT INTO clientes (codigo, apellido, nombres, direccion, localidad, provincia, postal, \
                                        telef_pers, telef_trab, mail, fecha_ingreso, sit_fis, cuit, \
                                        observaciones, apenombre) \
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                  """

            valores = (
                cliente["codigo"], cliente["apellido"], cliente["nombres"], cliente["direccion"],
                cliente["localidad"], cliente["provincia"], cliente["postal"],
                cliente["telef_pers"], cliente["telef_trab"], cliente["mail"],
                fecha_ingreso, cliente["sit_fis"], cliente["cuit"],
                cliente["observaciones"], cliente["apenombre"]
            )

            cur.execute(sql, valores)
            self.cnn.commit()
            id_nuevo = cur.lastrowid  # devolvemos el Id generado

        except Exception as e:

            self.cnn.rollback()
            messagebox.showerror("Error inesperado", str(e), parent=self.master)
            id_nuevo = None

        finally:
            cur.close()

        return id_nuevo

    def modificar_clientes(self, cliente):

        try:

            # Convierto fecha nuevamente de String a Datetime para guardar en SQL
            fecha_ingreso = datetime.strptime(cliente["fecha_ingreso"], '%d/%m/%Y')

            cur = self.cnn.cursor()

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
            self.cnn.commit()
            cur.close()
            return

        except Exception as e:
            messagebox.showerror("Error inesperado", f"{e}", parent=self.master)

    def eliminar_clientes(self, Id):

        cur = self.cnn.cursor()

        try:
            sql = "DELETE FROM clientes WHERE Id = %s"
            # 1 parámetro → (valor,)
            # varios → (v1, v2, v3)
            cur.execute(sql, (Id,))
            n = cur.rowcount
            self.cnn.commit()
            return n

        except Exception as e:
            self.cnn.rollback()
            messagebox.showerror("Error inesperado", str(e), parent=self.master)
            return 0

        finally:
            cur.close()
