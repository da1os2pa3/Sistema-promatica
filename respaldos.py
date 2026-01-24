import datetime
import os
import subprocess
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

class clase_backup(Frame):

    def __init__(self, master=None):
        super().__init__(master, width=880, height=150)
    #     # self.master = master

        # ----------------------------------------------------------------------------------
        # Esto esta agregado para centrar las ventanas en la pantalla
        # ----------------------------------------------------------------------------------
        master.geometry("880x510")
        master.resizable(0, 0)
        # Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
        # mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
        # Obtenemos el largo y  ancho de la pantalla
        wtotal = master.winfo_screenwidth()
        htotal = master.winfo_screenheight()
        # Guardamos el largo y alto de la ventana
        wventana = 980
        hventana = 200
        # Aplicamos la siguiente formula para calcular donde debería posicionarse
        pwidth = round(wtotal / 2 - wventana / 2) + 0
        pheight = round(htotal / 2 - hventana / 2) + 0
        # Se lo aplicamos a la geometría de la ventana
        master.geometry(str(wventana) + "x" + str(hventana) + "+" + str(pwidth) + "+" + str(pheight))
        # ------------------------------------------------------------------------------

        # carpeta_principal = os.path.dirname(__file__)
        # self.carpeta_respaldo = os.path.join(carpeta_principal, 'Respaldos')
        # self.contrasena = ""

        self.create_widgets()

    # ======================================================================================
    # ================================= WIDGETS ============================================
    # ======================================================================================

    def create_widgets(self):

        # TITULOS - PRIMERA PARTE ----------------------------------------------------

        # Stringvars
        self.strvar_porciento=StringVar(value="0")

        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)
        self.frame_general=LabelFrame(self.master)
        self.frame_botones=LabelFrame(self.master)

        # Armo el logo y el titulo
        self.photo3 = Image.open('backup.png')
        self.photo3 = self.photo3.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_backup = ImageTk.PhotoImage(self.photo3)
        self.lbl_png_backup = Label(self.frame_titulo_top, bg="red", relief=RIDGE, bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=49, text="Backups", bg="black", fg="gold",
                                font=("Arial bold", 20, "bold"), bd=5, relief=RIDGE, padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_backup.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")

        # ------------------------------------------------------------
        self.barra_progreso = ttk.Progressbar(self.frame_general, length=800, orient=HORIZONTAL, maximum=100)
        self.barra_progreso.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.lbl_porciento=Label(self.frame_general, textvariable=self.strvar_porciento)
        self.lbl_porciento.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.btnstart=Button(self.frame_botones, text="Comenzar", width=10, command=self.act_1, bg="blue", fg="white")
        self.btnstart.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.btnfin=Button(self.frame_botones, text="Salir", width=10, command=self.fSalir, bg="grey", fg="black")
        self.btnfin.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.btnfin.configure(state="disabled")

        self.btncancela=Button(self.frame_botones, text="Cancelar", width=10, command=self.fCancela, bg="red", fg="white")
        self.btncancela.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        # -------------------------------------------------------------

        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=5)
        self.frame_general.pack(side="top", padx=5, pady=5)
        self.frame_botones.pack(side="top", padx=5, pady=5)
        # --------------------------------------------------------------------------

    def act_1(self):

        self.act_progreso()
        self.crear_respaldos("sist_prom")
        self.btnfin.configure(state="normal")

    def crear_respaldos(self, nombre_bd):

        # guardo contraseña
        self.contrasena = ""

        # -------------------------------------------------------------------------
        # Aqui logro guardar todas las tablas en una lista "tablas"
        cmd_tablas = (
            '"C:/Program Files/MySQL/MySQL Workbench 8.0 CE/mysql" '
            f'--user=root --password={self.contrasena} '
            f'-N -e "SHOW TABLES FROM {nombre_bd}"'
        )

        resultado = subprocess.check_output(cmd_tablas, shell=True, text=True)
        tablas = resultado.splitlines()
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        # carpeta base del proyecto
        base_dir = os.getcwd()
        # carpeta "respaldos"
        ruta_respaldos = os.path.join(base_dir, "respaldos")
        # fecha y hora actual (formato seguro para carpetas)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # carpeta final: respaldos/2026-01-19_14-30-05
        ruta_backup = os.path.join(ruta_respaldos, timestamp)
        # crear carpetas
        os.makedirs(ruta_backup, exist_ok=True)
        # -------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        for tabla in tablas:

            archivo = os.path.join(ruta_backup, f"{tabla}.sql")

            with open(archivo, "w", encoding="utf-8") as out:

                cmd_dump = (
                    '"C:/Program Files/MySQL/MySQL Workbench 8.0 CE/mysqldump" '
                    #'--login-path=local '                    
                    '--column-statistics=0 '
                    f'--user=root --password={self.contrasena} '
                    f'{nombre_bd} {tabla}'
                )
                subprocess.run(cmd_dump, shell=True, stdout=out)
        # -------------------------------------------------------------------------

    def act_progreso(self):
        tasks = 10
        x = 0
        while(x<tasks):
            self.barra_progreso['value']+=10
            time.sleep(0.5)
            x+=1
            self.strvar_porciento.set(str(int((x / tasks) * 100)) + '%')
            self.frame_general.update_idletasks()
        return

    def fSalir(self):
        self.master.destroy()

    def fCancela(self):
        self.master.destroy()
