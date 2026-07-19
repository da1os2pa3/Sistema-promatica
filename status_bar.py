import tkinter as tk

class StatusBar:

    def __init__(self, master):

        self.master = master
        self.status_var = tk.StringVar()

        self.status_bar = tk.Label(
            master,
            textvariable=self.status_var,
            bd=1,
            relief="sunken",
            anchor="w",
            bg="#f0f0f0"
        )

        self.status_bar.pack(side="bottom", fill="x")

    def set_status(self, mensaje, tipo="info", tiempo=3000):

        colores = {
            "ok": ("#d4edda", "#155724"),
            "error": ("#f8d7da", "#721c24"),
            "warn": ("#fff3cd", "#856404"),
            "info": ("#d1ecf1", "#0c5460")
        }

        bg, fg = colores.get(tipo, ("#f0f0f0", "black"))

        self.status_var.set("  " + mensaje)
        self.status_bar.config(bg=bg, fg=fg)

        if tipo == "ok":
            self.master.bell()

        elif tipo == "error":
            self.master.bell()
            self.master.after(120, self.master.bell)

        elif tipo == "warn":
            self.master.bell()

        self.master.after(tiempo, self.clear_status)

    def clear_status(self):

        self.status_var.set("")
        self.status_bar.config(bg="#f0f0f0", fg="black")