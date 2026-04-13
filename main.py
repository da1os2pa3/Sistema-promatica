from principal import *
import tkinter as tk

def main():

    root = tk.Tk()
    root.wm_title("Sistema Gestion Promatica Computacion V. 2.0")

    app = Principal(root)
    app.pack(fill="both", expand=True)  # 👈 importante

    root.mainloop()  # ✅ correcto

if __name__ == '__main__':
    main()


# def main():
#
#     root = tk.Tk()
#     root.wm_title("Sistema Gestion Promatica Computacion V. 2.0")
#     app = Principal(root)
#     app.mainloop()
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     main()
#
