import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# -------------------------------------------
from datetime import datetime
# -------------------------------------------
import mysql.connector
# from mysql.connector import Error

# ===================================================================================
# ======================= FUNCIONES DE FECHAS =======================================
# ===================================================================================

"""
 Chequear que `new_text` esté en formato dd/mm/aaaa. Esta buena, te controla que solo puedas entrar decimales
 y te obliga a poner las barras y ningun otro caracter que no sean numeros o las barras. EN CONTRA: que
 no podes borra un solo numero por ejemplo del dia, solo te permite backspace pero desde el fondo
 """
def validate_entry(new_text):
    # Máximo de diez caracteres.
    if len(new_text) > 10:
        return False
    checks = []
    for i, char in enumerate(new_text):
        # En los índices 2 y 5 deben estar los caracteres "/".
        if i in (2, 5):
            checks.append(char == "/")
        else:
            # En el resto de los casos, la única restricción es que sean
            # números entre el 0 y el 9.
            checks.append(char.isdecimal())
    # `all()` retorna verdadero si todos los chequeos son verdaderos.
    return all(checks)

"""
Validar fechas - viene en string todo seguido sin separadores y sin barras - devuelvo fecha 
controlada y con barras puestas
"""
def valida_fechas(self, fecha_string):

    """
    asigno la fecha que ingreso como buena - si algo esta mal va a retornar error por controles
    anteriores al final de la funcion. Si llega al final de la funcion es porque es correcta.
    El unico desvio es cuando pone la fecha sin la barra, ahi yo le agrego las barras y la dejo
    con formato normal y la retorno
    """

    if len(fecha_string) != 0:

        fechaunida = fecha_string

        # Controlo el formato para dejarla dd/mm/yyyy - puede venir ddmmyyyy o culaquier cosa
        fecha_ingresada_list = list(fecha_string)

        # Debe tener 8 caracters si la ponen sin divisores o 10 si la ponen con divisores como STR
        if len(fecha_string) != 8 and len(fecha_string) != 10:
            mensajes_error_fechas(self, "B")
            return ""

        # si son 10 caracteres controlo que tenga las barras
        if len(fecha_string) == 10:

            if fecha_ingresada_list[0] == "/" and fecha_ingresada_list[1] == "/" and fecha_ingresada_list[2] == "/" and\
                fecha_ingresada_list[3] == "/" and fecha_ingresada_list[4] == "/" and fecha_ingresada_list[5] == "/" and\
                fecha_ingresada_list[6] == "/" and fecha_ingresada_list[7] == "/" and fecha_ingresada_list[8] == "/" and\
                fecha_ingresada_list[9] == "/":
                mensajes_error_fechas(self, "D")
                return  ""

            if fecha_ingresada_list[2] != "/" or fecha_ingresada_list[5] != "/":
                mensajes_error_fechas(self, "C")
                return ""

        # Si son 8 caracteres - controlo que todos sean digitos (numeros)
        if len(fecha_string) == 8:
            for ii in fecha_ingresada_list:
                if ii.isdigit():
                    pass
                else:
                    mensajes_error_fechas(self, "D")
                    return ""

            # al ser ocho, no trae las barras (22122023) entonces las agrego
            fecha_ingresada_list.insert(4, "/")
            fecha_ingresada_list.insert(2, "/")

            # ahora uno esa fecha en lista como un solo string
            fechaunida = "".join(fecha_ingresada_list)

        # obtengo año actual para luego hacer comparaciones
        ano_actual = int(datetime.strftime(datetime.today(), '%Y'))

        # obtengo en variables separadas el dia mes y año
        dias = fecha_ingresada_list[0:2]
        meses = fecha_ingresada_list[3:5]
        anos = fecha_ingresada_list[6:10]

        # uno en una variable los dias, mes y año porque venian como listas
        str_dia_control = int("".join(dias))
        str_mes_control = int("".join(meses))
        str_ano_control = int("".join(anos))

        # Controlar que el año no este muy desvandado
        if (ano_actual + 5) <= (str_ano_control) or (ano_actual - 5) >= (str_ano_control):
            sigue_sino = mensajes_error_fechas(self, "F")
            if sigue_sino == "S":
                pass
                #return (fechaunida)  # si acepta seguir con ese año
            else:
                return "N"  # no acepta seguir con ese año

        # primer control del rango de dias segun los meses de 31 dias o 30 dias
        if str_mes_control == 1 or str_mes_control == 3 or str_mes_control == 5 or str_mes_control == 7 \
                or str_mes_control == 8 or str_mes_control == 10 or str_mes_control == 12:

            if str_dia_control <= 0 or str_dia_control > 31:
                mensajes_error_fechas(self, "E")
                return ""

        # 30 dias para algunos meses
        if str_mes_control == 4 or str_mes_control == 6 or str_mes_control == 9 or str_mes_control == 11:

            if str_dia_control <= 0 or str_dia_control > 30:
                mensajes_error_fechas(self, "E")
                return ""

        # Control del rango de meses
        if str_mes_control <= 0 or str_mes_control > 12:
            mensajes_error_fechas(self, "E")
            return ""

        # Control de año bisiesto
        if str_ano_control % 4 != 0:  # no divisible entre 4
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 28:
                    mensajes_error_fechas(self, "E")
                    return ""

        elif str_ano_control % 4 == 0 and str_ano_control % 100 != 0:  # divisible entre 4 y no entre 100 o 400           BISIESTO
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 29:
                    mensajes_error_fechas(self, "E")
                    return ""

        elif str_ano_control % 4 == 0 and str_ano_control % 100 == 0 and str_ano_control % 400 != 0:  # divisible entre 4 y 10 y no entre 400
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 28:
                    mensajes_error_fechas(self, "E")
                    return ""

        elif str_ano_control % 4 == 0 and str_ano_control % 100 == 0 and str_ano_control % 400 == 0:  # divisible entre 4, 100 y 400    BISIESTO
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 29:
                    mensajes_error_fechas(self, "E")
                    return ""

        return (fechaunida)

    else:

        messagebox.showerror("Error", "Fecha ausente, se colocara fecha actual", parent=self)
        return ""

"""
Trabaja en conjunto con valida fechas - esta solo toma el codigo de mensaje que debe enviar y lo hace
"""

def mensajes_error_fechas(self, tipo_error):

    if tipo_error == "A":
        messagebox.showerror("Error", "La fecha no puede ser vacia", parent=self)
        return
    if tipo_error == "B":
        messagebox.showerror("Error", "cantidad de caracteres de fecha erroneos", parent=self)
        return
    if tipo_error == "C":
        messagebox.showerror("Error", "separadores de fecha erroneos - use (dd/mm/aaaa)", parent=self)
        return
    if tipo_error == "D":
        messagebox.showerror("Error","algunos caracteres no son digitos numericos - use (dd/mm/aaaa) o (ddmmaaaa)", parent=self)
        return
    if tipo_error == "E":
        messagebox.showerror("Error", "rango de dias, meses o años fuera de limites - verifique", parent=self)
        return
    if tipo_error == "F":
        sigue = messagebox.askyesno("Verifique",
                                    "Notamos diferencia sustancial en el año con el actual.. Continua???",
                                    parent=self)
        if sigue == False:
            return "N"
        else:
            return "S"

"""
Toma una fecha al reves y la pone normal de 2024-12-19 a 19/12/2024
La fecha debe venir como string en parametro -par-
"""
def fecha_str_reves_normal(self, par):

    # paso a date pero sigue al reves
    date_al_reves = datetime.strptime(par, '%Y-%m-%d')
    # paso otra vez a str pero ahora al derecha
    str_al_derecho = date_al_reves.strftime('%d/%m/%Y')
    return str_al_derecho

"""
Asigno la fecha que ingreso como buena - si algo esta mal va a retornar error por controles
anteriores al final de la funcion. Si llega al final de la funcion es porque es correcta.
El unico desvio es cuando pone la fecha sin la barra, ahi yo le agrego las barras y la dejo
con formato normal y la retorno
"""
def valida_fechas_guardar(self, fecha_string):

    if len(fecha_string) != 0:

        fechaunida = fecha_string

        # Controlo el formato para dejarla dd/mm/yyyy - puede venir ddmmyyyy o culaquier cosa
        fecha_ingresada_list = list(fecha_string)

        # Debe tener 8 caracters si la ponen sin divisores o 10 si la ponen con divisores como STR
        if len(fecha_string) != 8 and len(fecha_string) != 10:
            return ""

        # si son 10 caracteres controlo que tenga las barras
        if len(fecha_string) == 10:
            if fecha_ingresada_list[2] != "/" or fecha_ingresada_list[5] != "/":
                return ""

        # Si son 8 caracteres - controlo que todos sean digitos (numeros)
        if len(fecha_string) == 8:
            for ii in fecha_ingresada_list:
                if ii.isdigit():
                    pass
                else:
                    return ""

            # al ser ocho, no trae las barras (22122023) entonces las agrego
            fecha_ingresada_list.insert(4, "/")
            fecha_ingresada_list.insert(2, "/")

            # ahora uno esa fecha en lista como un solo string
            fechaunida = "".join(fecha_ingresada_list)

        # obtengo año actual para luego hacer comparaciones
        ano_actual = int(datetime.strftime(datetime.today(), '%Y'))

        # obtengo en variables separadas el dia mes y año
        dias = fecha_ingresada_list[0:2]
        meses = fecha_ingresada_list[3:5]
        anos = fecha_ingresada_list[6:10]

        # uno en una variable los dias, mes y año porque venian como listas
        str_dia_control = int("".join(dias))
        str_mes_control = int("".join(meses))
        str_ano_control = int("".join(anos))

        # Controlar que el año no este muy desvandado
        if (ano_actual + 5) <= (str_ano_control) or (ano_actual - 5) >= (str_ano_control):
            sigue_sino = mensajes_error_fechas(self, "F")
            if sigue_sino == "S":
                pass
                #return (fechaunida)  # si acepta seguir con ese año
            else:
                return "N"  # no acepta seguir con ese año

        # primer control del rango de dias segun los meses de 31 dias o 30 dias
        if str_mes_control == 1 or str_mes_control == 3 or str_mes_control == 5 or str_mes_control == 7 \
                or str_mes_control == 8 or str_mes_control == 10 or str_mes_control == 12:

            if str_dia_control <= 0 or str_dia_control > 31:
                return ""

        # 30 dias para algunos meses
        if str_mes_control == 4 or str_mes_control == 6 or str_mes_control == 9 or str_mes_control == 11:

            if str_dia_control <= 0 or str_dia_control > 30:
                return ""

        # Control del rango de meses
        if str_mes_control <= 0 or str_mes_control > 12:
            return ""

        # Control de año bisiesto
        if str_ano_control % 4 != 0:  # no divisible entre 4
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 28:
                    return ""

        elif str_ano_control % 4 == 0 and str_ano_control % 100 != 0:  # divisible entre 4 y no entre 100 o 400           BISIESTO
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 29:
                    return ""

        elif str_ano_control % 4 == 0 and str_ano_control % 100 == 0 and str_ano_control % 400 != 0:  # divisible entre 4 y 10 y no entre 400
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 28:
                    return ""

        elif str_ano_control % 4 == 0 and str_ano_control % 100 == 0 and str_ano_control % 400 == 0:  # divisible entre 4, 100 y 400    BISIESTO
            if str_mes_control == 2:
                if str_dia_control <= 0 or str_dia_control > 29:
                    return ""

        return (fechaunida)

    return "BLANCO"
#

# ==========================================================================================
# ========================== METODOS SOBRE TABLAS ==========================================
# ==========================================================================================





# ===============================================================
# ==================== VALIDACIONES =============================
# ===============================================================

'''
Valida que no se repitan los campos claves
parametros: el codigo ingresado - sobre que tabla - que campo de la tabla
Controla en la tabla si el codigo ingresado esta repetido en la tabla
'''

def codigo_repetido(codcontrol, tabla, campo):

    cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")

    cur = cnn.cursor()
    cur.execute("SELECT * FROM "+tabla+" WHERE "+campo+" = "+codcontrol)
    datos = cur.fetchall()
    cur.close()
    return datos


'''
# Esta se fija que no existan mas de una vez los caracteres "-", "." en el campo numerico
# retorna un valor Boolean Falso o True
'''
def control_forma(value):
    cuenta_i = 0
    cuenta_g = 0
    for i in value:
        if i == '.':
            cuenta_i += 1
        if i == '-':
            cuenta_g += 1
    if cuenta_i > 1 or cuenta_g > 1:
        return(False)
    else:
        return(True)

'''
# Esta controla los valores numericos en cuanto a inconsistencias - trabaja usando "control_forma" que esta arriba
# value = Stringvar.get() a controlar 
quepongo = al valor que quiere que devolvamos ante una inconsistencia
'''
def control_numerico(value, quepongo):

    if not control_forma(list(value)):
        return quepongo
    if value == "" or value == '-' or value == '.':
        return quepongo
    if float(value) == 0:
        return  quepongo
    if float(value) < 0:
        return (float(value) * -1)
    if float(value) > 0:
        return round(float(value), 2)

'''
# Limita la cantidad de caracteres ingresados en un Entry
'''
def limitador(entry_text, caract):
    if len(entry_text.get()) > 0:
        # donde esta el :limitas la cantidad d caracteres
        entry_text.set(entry_text.get()[:caract])
'''
# Toma una cifra y le pone los puntos de los miles y las comas decimales
'''
def formatear_cifra(cifra):
    numero = cifra
    salida1 = "{:,.2f}".format(numero)
    salida2 = salida1.replace(',','n')
    salida3 = salida2.replace('.',',')
    salida4 = salida3.replace('n','.')
    return salida4

'''
# Valida los CUIT
'''
def validar_cuit(self, cuit):
    # Metodo que valida el Numero de CUIT - Se ejecuta antes de guardar

    if len(cuit) == 0:
        return True

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    cuit = cuit.replace("-", "")  # remuevo las barras

    if len(cuit) != 11:
        return False

    # calculo el digito verificador
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])

# ================================================================
# ====================== FUNCIONALIDAD ===========================
# ================================================================

'''
# pasa numeros a letras
'''
def numero_to_letras(numero):
    indicador = [("", ""), ("MIL", "MIL"), ("MILLON", "MILLONES"), ("MIL", "MIL"), ("BILLON", "BILLONES")]
    entero = int(numero)
    decimal = int(round((numero - entero) * 100))
    # print 'decimal : ',decimal
    contador = 0
    numero_letras = ""
    while entero > 0:
        a = entero % 1000
        if contador == 0:
            en_letras = convierte_cifra(a, 1).strip()
        else:
            en_letras = convierte_cifra(a, 0).strip()
        if a == 0:
            numero_letras = en_letras + " " + numero_letras
        elif a == 1:
            if contador in (1, 3):
                numero_letras = indicador[contador][0] + " " + numero_letras
            else:
                numero_letras = en_letras + " " + indicador[contador][0] + " " + numero_letras
        else:
            numero_letras = en_letras + " " + indicador[contador][1] + " " + numero_letras
        numero_letras = numero_letras.strip()
        contador = contador + 1
        entero = int(entero / 1000)
    numero_letras = numero_letras + " con " + str(decimal) + "/100"
    #print('numero: ', numero)
    #print(numero_letras)
    return numero_letras

'''
# Trabaja en conjunto con numerpo_to_letras
'''
def convierte_cifra(numero, sw):
    lista_centana = ["", ("CIEN", "CIENTO"), "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS",
                     "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]
    lista_decena = ["", (
    "DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"),
                    ("VEINTE", "VEINTI"), ("TREINTA", "TREINTA Y "), ("CUARENTA", "CUARENTA Y "),
                    ("CINCUENTA", "CINCUENTA Y "), ("SESENTA", "SESENTA Y "),
                    ("SETENTA", "SETENTA Y "), ("OCHENTA", "OCHENTA Y "),
                    ("NOVENTA", "NOVENTA Y ")
                    ]
    lista_unidad = ["", ("UN", "UNO"), "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    centena = int(numero / 100)
    decena = int((numero - (centena * 100)) / 10)
    unidad = int(numero - (centena * 100 + decena * 10))
    # print "centena: ",centena, "decena: ",decena,'unidad: ',unidad

    texto_centena = ""
    texto_decena = ""
    texto_unidad = ""

    # Validad las centenas
    texto_centena = lista_centana[centena]
    if centena == 1:
        if (decena + unidad) != 0:
            texto_centena = texto_centena[1]
        else:
            texto_centena = texto_centena[0]

    # Valida las decenas
    texto_decena = lista_decena[decena]
    if decena == 1:
        texto_decena = texto_decena[unidad]
    elif decena > 1:
        if unidad != 0:
            texto_decena = texto_decena[1]
        else:
            texto_decena = texto_decena[0]
    # Validar las unidades
    # print "texto_unidad: ",texto_unidad
    if decena != 1:
        texto_unidad = lista_unidad[unidad]
        if unidad == 1:
            texto_unidad = texto_unidad[sw]

    return "%s %s %s" % (texto_centena, texto_decena, texto_unidad)





















# '''
# # Valida los caracteres que ingresan en los campos numericos - solo numeros punto y guion
# '''
# def validar(value):
#     print(value)
#     codigo = value
#     for i in codigo:
#         if i not in '0123456789.-':
#             return  False
#     return True
