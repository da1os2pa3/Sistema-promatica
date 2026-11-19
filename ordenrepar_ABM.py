import mysql.connector


class DatosOrdenRepar:

    def __init__(self, pantalla):
        self.master = pantalla

    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="sist_prom"
        )

    def consultar_ordenes(self, orden=""):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = "SELECT * FROM orden_repara"
            if orden:
                sql += " " + orden
            cur.execute(sql)
            return cur.fetchall()
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def insertar_orden(self, ordenes):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = """
                  INSERT INTO orden_repara(or_num_orden, fecha_ingreso, fecha_egreso, or_cod_cliente, or_nombre_cliente,
                                           equ_ingresa, equ_grupo, equ_procesador, equ_ram, equ_discos, equ_sist_oper,
                                           equ_obser, equ_accesorios, equ_estado, dat_ctaycontr, dat_requerido,
                                           inf_diagnostico, inf_presupuesto, trab_realizado, trab_partes, 
                                           trab_anotacion, tot_mano_obra, tot_partes, fin_retirada)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
            valores = (
                ordenes["or_num_orden"],
                ordenes["fecha_ingreso"],
                ordenes["fecha_egreso"],
                ordenes["or_cod_cliente"],
                ordenes["or_nombre_cliente"],
                ordenes["equ_ingresa"],
                ordenes["equ_grupo"],
                ordenes["equ_procesador"],
                ordenes["equ_ram"],
                ordenes["equ_discos"],
                ordenes["equ_sist_oper"],
                ordenes["equ_obser"],
                ordenes["equ_accesorios"],
                ordenes["equ_estado"],
                ordenes["dat_ctaycontr"],
                ordenes["dat_requerido"],
                ordenes["inf_diagnostico"],
                ordenes["inf_presupuesto"],
                ordenes["trab_realizado"],
                ordenes["trab_partes"],
                ordenes["trab_anotacion"],
                ordenes["tot_mano_obra"],
                ordenes["tot_partes"],
                ordenes["fin_retirada"]
            )
            cur.execute(sql, valores)
            cnn.commit()
            # devolvemos el Id generado del nuevo cliente
            id_nuevo = cur.lastrowid
            return id_nuevo
        except Exception:
            cnn.rollback()
            raise
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def modificar_orden(self, ordenes):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = ('''UPDATE orden_repara
                      SET or_num_orden      =%s, 
                          fecha_ingreso     =%s, 
                          fecha_egreso      =%s, 
                          or_cod_cliente    =%s, 
                          or_nombre_cliente =%s, 
                          equ_ingresa       =%s, 
                          equ_grupo         =%s, 
                          equ_procesador    =%s, 
                          equ_ram           =%s, 
                          equ_discos        =%s, 
                          equ_sist_oper     =%s, 
                          equ_obser         =%s, 
                          equ_accesorios    =%s, 
                          equ_estado        =%s, 
                          dat_ctaycontr     =%s, 
                          dat_requerido     =%s, 
                          inf_diagnostico   =%s, 
                          inf_presupuesto   =%s, 
                          trab_realizado    =%s, 
                          trab_partes       =%s, 
                          trab_anotacion    =%s, 
                          tot_mano_obra     =%s, 
                          tot_partes        =%s, 
                          fin_retirada      =%s
                     WHERE Id=%s''')

            valores = (
                ordenes["or_num_orden"],
                ordenes["fecha_ingreso"],
                ordenes["fecha_egreso"],
                ordenes["or_cod_cliente"],
                ordenes["or_nombre_cliente"],
                ordenes["equ_ingresa"],
                ordenes["equ_grupo"],
                ordenes["equ_procesador"],
                ordenes["equ_ram"],
                ordenes["equ_discos"],
                ordenes["equ_sist_oper"],
                ordenes["equ_obser"],
                ordenes["equ_accesorios"],
                ordenes["equ_estado"],
                ordenes["dat_ctaycontr"],
                ordenes["dat_requerido"],
                ordenes["inf_diagnostico"],
                ordenes["inf_presupuesto"],
                ordenes["trab_realizado"],
                ordenes["trab_partes"],
                ordenes["trab_anotacion"],
                ordenes["tot_mano_obra"],
                ordenes["tot_partes"],
                ordenes["fin_retirada"],
                ordenes["Id"]
            )
            cur.execute(sql, valores)
            cnn.commit()
        except Exception:
            cnn.rollback()
            raise
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def eliminar_orden(self, Id):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = '''DELETE FROM orden_repara WHERE Id = {}'''.format(Id)
            cur.execute(sql)
            n = cur.rowcount
            cnn.commit()
            cur.close()
            return n
        except Exception:
            cnn.rollback()
            raise
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def traer_un_registro(self, Id):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor()
            cur.execute("SELECT * FROM orden_repara WHERE Id=%s", (Id,))
            datos_inf = cur.fetchone()
            return datos_inf
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def consultar_informa(self):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM informa WHERE 1")
            datos_inf = cur.fetchone()
            return datos_inf
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def buscar_entabla(self, argumento):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM " + argumento)
            datos = cur.fetchall()
            return datos
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def traer_ultimo(self, xparametro):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM orden_repara ORDER BY or_num_orden")
            datos = cur.fetchall()
            aux = ""
            for row in datos:
                if xparametro == 1:
                    aux = str(row[1]) + "\n"
                else:
                    aux = str(row[0]) + "\n"
            return aux
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def traer_un_cliente(self, para_codigo):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            sql = '''SELECT * FROM clientes WHERE codigo = {}'''.format(para_codigo)
            cur.execute(sql)
            datos_inf = cur.fetchone()
            return datos_inf
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()

    def suma_deuda(self, cod_cliente):

        cnn = None
        cur = None
        try:
            cnn = self.get_connection()
            cur = cnn.cursor(buffered=True)
            cur.execute("SELECT * FROM ctacte WHERE cc_codcli = " + cod_cliente)
            datos = cur.fetchall()
            return datos
        finally:
            if cur is not None:
                cur.close()
            if cnn is not None:
                cnn.close()
