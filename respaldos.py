import datetime
import os
import subprocess
#import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading

class Clase_Backup(Frame):

    def __init__(self, master=None):
        super().__init__(master, width=880, height=150)
    #     # self.master = master

        # ----------------------------------------------------------------------------------
        # TITULOS
        # ----------------------------------------------------------------------------------
        self.master.resizable(0, 0)

        """ Actualizamos el contenido de la ventana (la ventana pude crecer si se le agrega
            mas widgets).Esto actualiza el ancho y alto de la ventana en caso de crecer.
            Obtenemos el alto y  ancho de la pantalla """

        ancho = self.master.winfo_screenwidth()
        alto = self.master.winfo_screenheight()

        # Asigno fijo un ancho y un alto
        ancho_ventana = 920
        alto_ventana = 200

        # X e Y son las coordenadas para el posicionamiento del vertice superior izquierdo
        x = int((ancho - ancho_ventana) / 2)
        y = int((alto - alto_ventana) / 2)
        self.master.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        # ------------------------------------------------------------------------------

        self.create_widgets()

    # ======================================================================================
    # ================================= WIDGETS ============================================
    # ======================================================================================

    def create_widgets(self):

        # -----------------------------------------------------------------
        # STRINGVARS
        # -----------------------------------------------------------------
        self.strvar_porciento=StringVar(value="0")

        # -----------------------------------------------------------------
        # TITULOS
        # -----------------------------------------------------------------

        # --------------------------------------------
        # Encabezado logo y titulo con PACK
        self.frame_titulo_top = Frame(self.master)

        self.photocc = Image.open('backup.png')
        self.photocc = self.photocc.resize((50, 50), Image.LANCZOS)  # Redimension (Alto, Ancho)
        self.png_recibo = ImageTk.PhotoImage(self.photocc)
        self.lbl_png_recibo = Label(self.frame_titulo_top, image=self.png_recibo, bg="red", relief="ridge", bd=5)

        self.lbl_titulo = Label(self.frame_titulo_top, width=45, text="Backup",
                                bg="black", fg="gold", font=("Arial bold", 20, "bold"), bd=5, relief="ridge", padx=5)

        # Coloco logo y titulo en posicion de pantalla
        self.lbl_png_recibo.grid(row=0, column=0, sticky=W, padx=5, ipadx=22)
        self.lbl_titulo.grid(row=0, column=1, sticky="nsew")

        self.frame_titulo_top.pack(side="top", fill="x", padx=5, pady=5)
        # --------------------------------------------

        # --------------------------------------------
        self.frame_general=LabelFrame(self.master)

        # Barra de progreso (doy estilo
        style = ttk.Style()
        style.theme_use("clam")  # Más moderno que default

        style.configure("barra.Horizontal.TProgressbar",
                        troughcolor="#d9d9d9",
                        background="#4CAF50",
                        thickness=25)

        # creo la barra de progreso
        self.barra_progreso = ttk.Progressbar(
            self.frame_general,
            length=800,
            orient="horizontal",
            mode="determinate",
            style="barra.Horizontal.TProgressbar")

        self.barra_progreso.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.lbl_porciento = Label(self.frame_general,
                                   textvariable=self.strvar_porciento,
                                   font=("Arial", 12, "bold"))

        self.lbl_porciento.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_general.pack(side="top", padx=5, pady=5)
        # -------------------------------------------

        # -----------------------------------------------------------------
        # BOTONES
        # -----------------------------------------------------------------

        self.frame_botones=LabelFrame(self.master)

        self.btnstart=Button(self.frame_botones, text="Comenzar", width=10, command=self.act_1, bg="blue", fg="white")
        self.btnstart.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.btnfin=Button(self.frame_botones, text="Salir", width=10, command=self.fSalir, bg="yellow", fg="black")
        self.btnfin.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.frame_botones.pack(side="top", padx=5, pady=5)


    def act_1(self):

        """
        threading.Thread(target=self.crear_respaldos, args=("sist_prom",)) Significa:
        Thread → crear hilo
        target = → qué función ejecutar
        args = → qué parámetro pasarle
        "sist_prom" → nombre de la base
        Es equivalente a decir:
        Ejecutá crear_respaldos("sist_prom") pero en paralelo.

        ¿Qué hace hilo.start()?
        Esa línea es la que realmente lo pone a trabajar.
        Si no ponés .start(), el hilo se crea pero nunca arranca.
        """

        self.btnstart.configure(state="disabled")
        hilo = threading.Thread(target=self.crear_respaldos, args=("sist_prom",))
        hilo.start()

    def crear_respaldos(self, nombre_bd):

        self.contrasena = ""

        # creo una lista con las tablas que tengo en la carpeta
        cmd_tablas = (
            '"C:/Program Files/MySQL/MySQL Workbench 8.0 CE/mysql" '
            f'--user=root --password={self.contrasena} '
            f'-N -e "SHOW TABLES FROM {nombre_bd}"'
        )

        resultado = subprocess.check_output(cmd_tablas, shell=True, text=True)
        tablas = resultado.splitlines()

        total_tablas = len(tablas)

        # Configuro barra de progreso
        """
        “La barra va a completarse cuando llegue a la cantidad total de tablas. (maximun)”
        value = Es el progreso actual, o sea, arrancamos desde cero
        """
        self.barra_progreso["maximum"] = total_tablas
        self.barra_progreso["value"] = 0

        # Definicion de rutas y carpetas
        base_dir = os.getcwd()
        ruta_respaldos = os.path.join(base_dir, "respaldos")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta_backup = os.path.join(ruta_respaldos, timestamp)
        os.makedirs(ruta_backup, exist_ok=True)

        # Iteracion
        for i, tabla in enumerate(tablas):
            archivo = os.path.join(ruta_backup, f"{tabla}.sql")

            with open(archivo, "w", encoding="utf-8") as out:
                cmd_dump = (
                    '"C:/Program Files/MySQL/MySQL Workbench 8.0 CE/mysqldump" '
                    '--column-statistics=0 '
                    f'--user=root --password={self.contrasena} '
                    f'{nombre_bd} {tabla}'
                )

                """
                - subprocess es el módulo que permite ejecutar comandos del sistema desde Python.
                - shell=True le dice a Python:
                  Ejecutalo como si estuviera en la consola de Windows (CMD).
                  
                  stdout=out Esto es MUY importante. Significa:
                  Todo lo que el comando imprima en pantalla, guardalo en el archivo out.
                  Y out es esto:
                  with open(archivo, "w", encoding="utf-8") as out:
                """

                subprocess.run(cmd_dump, shell=True, stdout=out)

            # 🔥 ACTUALIZACIÓN PROFESIONAL
            self.barra_progreso["value"] = i + 1
            porcentaje = int(((i + 1) / total_tablas) * 100)
            self.strvar_porciento.set(f"{porcentaje}% - {tabla}")
            self.master.update_idletasks()

        self.strvar_porciento.set("✔ Backup Finalizado")
        self.btnstart.configure(state="normal")

    def fSalir(self):
        self.master.destroy()
