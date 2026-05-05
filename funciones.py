from tkinter import messagebox
from datetime import datetime
import mysql.connector

"""
===================================================================================
FUNCIONES DE FECHAS
===================================================================================
"""

"""
--------------------------------------------------------------------------------------------
1 - Validar fechas - viene en string todo seguido sin separadores y sin barras - devuelvo fecha 
    controlada y con barras puestas
--------------------------------------------------------------------------------------------
"""
def valida_fechas(self, fecha_string):

    if not fecha_string:
        mensajes_error_fechas(self, "A")
        return ""

    fecha_string = fecha_string.strip()

    # ✅ Caso 1: viene sin barras (ddmmaaaa)
    if len(fecha_string) == 8 and fecha_string.isdigit():
        fecha_string = f"{fecha_string[0:2]}/{fecha_string[2:4]}/{fecha_string[4:8]}"

    # ✅ Caso 2: formato con barras
    elif len(fecha_string) == 10:
        if fecha_string[2] != "/" or fecha_string[5] != "/":
            mensajes_error_fechas(self, "C")
            return ""
    else:
        mensajes_error_fechas(self, "B")
        return ""

    # ✅ Validación REAL de fecha (incluye bisiestos)
    try:
        fecha = datetime.strptime(fecha_string, "%d/%m/%Y")
    except ValueError:
        mensajes_error_fechas(self, "E")
        return ""

    # ✅ Control de año
    ano_actual = datetime.today().year

    if abs(fecha.year - ano_actual) > 5:
        sigue = mensajes_error_fechas(self, "F")
        if sigue != "S":
            return "N"
    return fecha.strftime("%d/%m/%Y")
"""
--------------------------------------------------------------------------------------------
"""

"""
--------------------------------------------------------------------------------------------
2 BIS - Trabaja en conjuento con valida_fechas - da los mensajes de error
--------------------------------------------------------------------------------------------
"""
def mensajes_error_fechas(self, tipo_error):

    mensajes = {
        "A": "La fecha no puede ser vacía",
        "B": "Cantidad de caracteres de fecha erróneos",
        "C": "Separadores incorrectos - use (dd/mm/aaaa)",
        "D": "Caracteres inválidos - use solo números",
        "E": "Fecha inválida - verifique día/mes/año",
    }

    if tipo_error in mensajes:
        messagebox.showerror("Error", mensajes[tipo_error], parent=self)
        return

    if tipo_error == "F":
        return "S" if messagebox.askyesno(
            "Verifique",
            "Diferencia grande con el año actual. ¿Continuar?",
            parent=self
        ) else "N"
"""
------------------------------------------------------------------------------------------------------
"""

"""
------------------------------------------------------------------------------------------------------
2 - Toma una fecha al reves y la pone normal de 2024-12-19(tabla) a 19/12/2024(uso sistema). La fecha debe 
    venir como string en parametro -par- . Puedo retornar la fecha con la hora o sola
------------------------------------------------------------------------------------------------------
"""
def fecha_str_reves_normal(self, par, con_hora=False):

    try:
        if con_hora:
            formato_entrada = '%Y-%m-%d %H:%M'
            formato_salida = '%d/%m/%Y %H:%M'
        else:
            formato_entrada = '%Y-%m-%d'
            formato_salida = '%d/%m/%Y'

        fecha_dt = datetime.strptime(par, formato_entrada)
        return fecha_dt.strftime(formato_salida)
    except ValueError:
        return ""  # o podrías devolver None o lanzar error
"""
------------------------------------------------------------------------------------------------------
"""


"""
************************************************************************
FUNCIONES NUMERICAS - CONTROLES
*************************************************************************
"""

"""
-------------------------------------------------------------------------------------------
1 - pasa numeros a letras
-------------------------------------------------------------------------------------------
"""
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
"""
-------------------------------------------------------------------------------------------
"""

"""
-------------------------------------------------------------------------------------------
1 BIS - Trabaja en conjunto con numero_to_letras
-------------------------------------------------------------------------------------------
"""
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
"""
-------------------------------------------------------------------------------------------
"""

'''
-------------------------------------------------------------------------------------------
2 - Toma una cifra y le pone los puntos de los miles y las comas decimales
-------------------------------------------------------------------------------------------
'''
def formatear_cifra(cifra):
    numero = cifra
    salida1 = "{:,.2f}".format(numero)
    salida2 = salida1.replace(',','n')
    salida3 = salida2.replace('.',',')
    salida4 = salida3.replace('n','.')
    return salida4
'''
-------------------------------------------------------------------------------------------
'''

'''
-------------------------------------------------------------------------------------------
3 - Limita la cantidad de caracteres ingresados en un Entry
-------------------------------------------------------------------------------------------
'''
def limitador(entry_text, caract):
    if len(entry_text.get()) > 0:
        # donde esta el :limitas la cantidad d caracteres
        entry_text.set(entry_text.get()[:caract])
'''
-------------------------------------------------------------------------------------------
'''


"""
===================================================================================
VALIDACIONES
===================================================================================
"""

"""
-------------------------------------------------------------------------------------------
1 - Valida los CUIT - Digito verificador
-------------------------------------------------------------------------------------------
"""
def validar_cuit(self, cuit):

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
"""
-------------------------------------------------------------------------------------------
"""

'''
-------------------------------------------------------------------------------------------
2 - Valida que no se repitan los campos claves
    parametros: el codigo ingresado - sobre que tabla - que campo de la tabla
   Controla en la tabla si el codigo ingresado esta repetido en la tabla
-------------------------------------------------------------------------------------------
'''
def codigo_repetido(codcontrol, tabla, campo):
    cnn = mysql.connector.connect(host="localhost", user="root", passwd="", database="sist_prom")
    cur = cnn.cursor()
    cur.execute("SELECT * FROM "+tabla+" WHERE "+campo+" = "+codcontrol)
    datos = cur.fetchall()
    cur.close()
    return datos
"""
-------------------------------------------------------------------------------------------
"""


'''
-------------------------------------------------------------------------------------------
3 - Esta controla los valores numericos en cuanto a inconsistencias - trabaja usando "control_forma" que esta arriba
    value = Stringvar.get() a controlar 
    quepongo = al valor que quiere que devolvamos ante una inconsistencia
-------------------------------------------------------------------------------------------
'''
def control_numerico(value, quepongo):
    if not control_forma(value):
        return quepongo
    num = float(value)
    if num == 0:
        return quepongo
    return round(abs(num), 2)

def control_forma(value):
    """
    🧠 ¿Qué hace exactamente? Intenta convertir value a tipo float. Si puede hacerlo, devuelve True.
        Si falla(porque no es un número válido), devuelve False.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
"""
-------------------------------------------------------------------------------------------
"""











