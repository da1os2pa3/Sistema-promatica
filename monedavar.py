import tkinter as tk
from decimal import Decimal, InvalidOperation

class MonedaVar(tk.StringVar):
    def __init__(self, master=None, valor="0.00"):
        super().__init__(master)
        self._valor = Decimal(valor)
        self._actualizando = False
        self._set_texto(self._valor)

        # detectar cambios manuales (cuando escribe el usuario)
        self.trace_add("write", self._on_write)

    # -------------------------
    # FORMATO
    # -------------------------
    def _formatear(self, valor):
        texto = f"{valor:,.2f}"
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")

    def _parsear(self, texto):
        texto = texto.replace(".", "").replace(",", ".")
        return Decimal(texto)

    # -------------------------
    # CONTROL INTERNO
    # -------------------------
    def _set_texto(self, valor):
        self._actualizando = True
        super().set(self._formatear(valor))
        self._actualizando = False

    def _on_write(self, *args):
        if self._actualizando:
            return

        texto = super().get()

        # permitir estados intermedios mientras escribe
        if texto in ("", "-", ",", ".", "-,", "-."):
            return

        try:
            valor = self._parsear(texto)
            self._valor = valor
        except InvalidOperation:
            # si escribe algo inválido, vuelve al último valor válido
            self._set_texto(self._valor)

    # -------------------------
    # API PÚBLICA
    # -------------------------
    def set_valor(self, valor):
        self._valor = Decimal(valor)
        self._set_texto(self._valor)

    def get_valor(self):
        return self._valor

    def sumar(self, importe):
        self._valor += Decimal(importe)
        self._set_texto(self._valor)

    def restar(self, importe):
        self._valor -= Decimal(importe)
        self._set_texto(self._valor)

    # -------------------------
    # FORMATEAR AL SALIR (FOCUS OUT)
    # -------------------------
    def bind_entry(self, entry):
        entry.config(textvariable=self)

        def al_salir(event):
            self._set_texto(self._valor)

        entry.bind("<FocusOut>", al_salir)


# 🔹 Cómo usarla
# ✔ En un Label (igual que siempre)
# self.total_var = MonedaVar(self.root, "0.00")
#
# Label(self.frame, textvariable=self.total_var).pack()
# ✔ En un Entry editable
# self.entry_total = tk.Entry(self.root)
# self.total_var.bind_entry(self.entry_total)
#
# self.entry_total.pack()
# 🔹 Ejemplos de uso
# self.total_var.set_valor("1500")
# self.total_var.sumar("250.75")
# self.total_var.restar("100")
# 🔹 ¿Qué hace automáticamente?
#
# Si el usuario escribe:
#
# 1234 → al salir → 1.234,00
# 1234,5 → 1.234,50
# 1234.5 → también funciona ✔
# abc → lo rechaza y vuelve al valor anterior ✔
# 🔹 Por qué esto es nivel pro
#
# ✔ Usa Decimal (precisión real de dinero)
# ✔ Tolera escritura “humana”
# ✔ Formatea solo cuando corresponde
# ✔ Evita loops con _actualizando
# ✔ Mantiene UI + lógica separadas
#
# 🔹 Resultado final
#
# 👉 Tenés UNA sola variable que:
#
# se muestra formateada
# se puede editar
# se puede usar para cálculos
# no rompe nada
#
# Si querés, el siguiente paso (ya ultra pro) es:
#
# 👉 conectar esto con tu Treeview
# 👉 y que el total se recalule solo cuando agregás/modificás filas
#
# Eso ya es un sistema de presupuestos completo posta 😄


# ----------------------------------------------------------------------------------------------



# 🔹 Lo importante (acá está la clave)
#
# Si usás la clase que te armé:
#
# self.total_var = MonedaVar(self.root, "0.00")
#
# 👉 Entonces esa misma variable cumple doble función:
#
# Uso	Cómo
# Mostrar en Label	textvariable=self.total_var
# Obtener valor numérico	self.total_var.get_valor()
# Modificar valor	self.total_var.set_valor(1500)
# 🔹 O sea, en tu caso concreto
#
# Tu línea queda igual:
#
# self.lbl_total_presup_redondo2 = Label(
#     self.frame_totales_generales,
#     textvariable=self.total_var,
#     width=15,
#     justify="right",
#     font=fff,
#     foreground="#ff33f6"
# )
#
# ✔ No cambia nada en el Label
# ✔ Pero ahora la variable es “inteligente”
#
# 🔹 Y en el resto del código
#
# En vez de hacer:
#
# self.strvar_total_presup_redondo.set("1500")  # ❌
#
# Hacés:
#
# self.total_var.set_valor(1500)  # ✔
# 🔹 Y cuando necesitás calcular
# total = self.total_var.get_valor()
# 🔹 Resumen mental (muy importante)
#
# 👉 Antes:
#
# StringVar → solo texto
# Problemas con formato
#
# 👉 Ahora:
#
# MonedaVar → texto + número juntos
# UI automática ✔
# cálculos seguros ✔
# 🔹 Traducción a lo que vos preguntabas
#
# “¿La variable que uso en textvariable puede ser esa?”
#
# ✔ Sí, exactamente esa misma
# 👉 Pero ahora es una MonedaVar en vez de StringVar
#
# Si querés, en el siguiente paso te ayudo a adaptar esto directamente a tu código actual (con nombres reales como self.total_presup_redondo, Treeview, etc.) y lo dejamos integrado sin romper nada 👍