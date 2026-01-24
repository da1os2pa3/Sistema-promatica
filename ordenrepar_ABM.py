import mysql.connector
from mysql.connector import Error
# ---------------------------------------
from tkinter import messagebox

class DatosOrdenRepar:

    def __init__(self, pantalla):

        self.master = pantalla

        try:
            self.cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
        except Error as ex:
            print("Error de conexion: {0}".format(ex))

    # def __str__(self):
    #
    #     datos = self.consultar_ordenes()
    #     aux = ""
    #     for row in datos:
    #         aux = aux + str(row) + "\n"
    #     return aux

    def consultar_ordenes(self, tofil):

        try:

            cur = self.cnn.cursor()

            if tofil == "":
                cur.execute("SELECT * FROM orden_repara ORDER BY or_num_orden")
            else:
                cur.execute("SELECT * FROM " + tofil)

            """ cursor.fetchall()recupera todas las filas del resultado de una consulta. Devuelve todas
            # las filas como una "lista". Se devuelve una lista vacía si no hay ningún registro para recuperar.
            # cursor.fetchmany(size)devuelve el número de filas especificadas por size el argumento. Cuando
            # se llama repetidamente, este método recupera el siguiente conjunto de filas del resultado de una
            # consulta y devuelve una lista de tuplas. Si no hay más filas disponibles, devuelve una lista vacía.
            # cursor.fetchone()El método devuelve un solo registro o Ninguno si no hay más filas disponibles. """

            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Consultar Ordenes-", parent=self.master)
            exit()

    def insertar_orden(self, numero_orden, fecha_ingreso, codigo_cliente, nombre_cliente, equipo_ingresa, grupo_ingresa,
                             equipo_procesador, equipo_ram, equipo_discos, equipo_sist_oper, equipo_obser,
                             equipo_accesorios, equipo_estado, cuentas, trabajo_requerido, text_diagnostico,
                             presupuesto, text_trabajo_realizado, partes, text_anotaciones, total_mano_obra,
                             total_partes, retirada):
        try:
        #aaa = 0
        #if aaa == 0:
            cur = self.cnn.cursor()
            sql = '''INSERT INTO orden_repara (or_num_orden, fecha_ingreso, or_cod_cliente, or_nombre_cliente, equ_ingresa, 
                                               equ_grupo, equ_procesador, equ_ram, equ_discos, equ_sist_oper, equ_obser, 
                                               equ_accesorios, equ_estado, dat_ctaycontr, dat_requerido, 
                                               inf_diagnostico, inf_presupuesto, trab_realizado, trab_partes, 
                                               trab_anotacion, tot_mano_obra, tot_partes, fin_retirada) 
                     VALUES('{}','{}','{}','{}', '{}', '{}','{}','{}','{}','{}','{}','{}', '{}','{}','{}','{}','{}',
                            '{}', '{}', '{}','{}','{}','{}')'''.format(numero_orden, fecha_ingreso,
                                                                       codigo_cliente, nombre_cliente, equipo_ingresa,
                                                                       grupo_ingresa, equipo_procesador, equipo_ram,
                                                                       equipo_discos, equipo_sist_oper, equipo_obser,
                                                                       equipo_accesorios, equipo_estado, cuentas,
                                                                       trabajo_requerido, text_diagnostico, presupuesto,
                                                                       text_trabajo_realizado, partes, text_anotaciones,
                                                                       total_mano_obra, total_partes, retirada)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n
        #else:
        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Insertar Orden-", parent=self.master)
            exit()

    def modificar_orden(self, Id, numero_orden, fecha_ingreso, fecha_egreso, codigo_cliente, nombre_cliente,
                              equipo_ingresa, grupo_ingresa, equipo_procesador, equipo_ram, equipo_discos,
                              equipo_sist_oper, equipo_obser, equipo_accesorios, equipo_estado, cuentas,
                              trabajo_requerido, text_diagnostico, presupuesto, text_trabajo_realizado, partes,
                              text_anotaciones, total_mano_obra, total_partes, retirada):

        #try:
        aaa = 0
        if aaa==0:

            cur = self.cnn.cursor()

            sql = '''UPDATE orden_repara SET or_num_orden='{}', fecha_ingreso='{}', fecha_egreso='{}', 
                                             or_cod_cliente='{}', or_nombre_cliente='{}', equ_ingresa='{}', 
                                             equ_grupo='{}', equ_procesador='{}', equ_ram='{}', equ_discos='{}', 
                                             equ_sist_oper='{}', equ_obser='{}', equ_accesorios='{}', equ_estado='{}', 
                                             dat_ctaycontr='{}', dat_requerido='{}', inf_diagnostico='{}', 
                                             inf_presupuesto='{}', trab_realizado='{}', trab_partes='{}', 
                                             trab_anotacion='{}', tot_mano_obra='{}', tot_partes='{}', fin_retirada='{}'
                     WHERE Id={}'''.format(numero_orden, fecha_ingreso, fecha_egreso, codigo_cliente,
                                             nombre_cliente, equipo_ingresa, grupo_ingresa, equipo_procesador,
                                             equipo_ram, equipo_discos, equipo_sist_oper, equipo_obser,
                                             equipo_accesorios, equipo_estado, cuentas, trabajo_requerido,
                                             text_diagnostico, presupuesto, text_trabajo_realizado, partes,
                                             text_anotaciones, total_mano_obra, total_partes, retirada, Id)

            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n

        else:
        #except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Modificar Orden-", parent=self.master)
            exit()

    def eliminar_orden(self, Id):

        try:

            cur = self.cnn.cursor()
            sql = '''DELETE FROM orden_repara WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return n

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo=Eliminar Orden-", parent=self.master)
            exit()

    def traer_un_registro(self, Id):

        try:

            cur = self.cnn.cursor()
            sql = '''SELECT * FROM orden_repara WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            datos_inf = cur.fetchone()
            n = cur.rowcount                       # ver esto porque no lo uso en la modif
            self.cnn.commit()
            cur.close()
            return datos_inf

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Traer un registro-", parent=self.master)
            exit()

    def consultar_informa(self):

        try:

            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchone()
            self.cnn.commit()
            cur.close()
            return datos_inf

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Consultar Informa-", parent=self.master)
            exit()

    def buscar_entabla(self, argumento):

        aaa = 0
        #try:
        if aaa==0:

            cur = self.cnn.cursor()
            if len(argumento) <= 0:
                return
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos

        else:
        #except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Buscar en tabla-", parent=self.master)
            exit()

    def traer_ultimo(self, xparametro):

        try:

            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM orden_repara ORDER BY or_num_orden")
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

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Traer ultimo-", parent=self.master)
            exit()

    def traer_un_cliente(self, para_codigo):

        try:

            cur = self.cnn.cursor()
            sql = '''SELECT * FROM clientes WHERE codigo = {}'''.format(para_codigo)
            cur.execute(sql)
            datos_inf = cur.fetchone()
            n = cur.rowcount
            self.cnn.commit()
            cur.close()
            return datos_inf

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Traer un cliente-", parent=self.master)
            exit()

    def suma_deuda(self, cod_cliente):

        try:

            cur = self.cnn.cursor()
            cur.execute("SELECT * FROM ctacte WHERE cc_codcli = " + cod_cliente)
            datos = cur.fetchall()
            self.cnn.commit()
            cur.close()
            return datos

        except:

            messagebox.showerror("Error inesperado", "Contacte asistencia-Metodo-Suma deuda-", parent=self.master)
            exit()
