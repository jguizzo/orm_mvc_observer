from tkinter import Tk
from vista import *
from vista_2 import *


class Controlador():

    def __init__(self, root):
        self.root_controlador = root
        self.ventana_principal()

    def ventana_principal(self,):
        Ventana_principal(self.root_controlador)

    def ventana_secundaria(self, datos, objeto):
        print("Despliego ventana secundaria")
        self.root_sec = Toplevel()
        Ventana_secundaria(self.root_sec, datos, objeto)
        self.root_sec.grab_set()
        self.root_sec.focus_set()
        self.root_sec.wait_window()

    
if __name__ == "__main__":
    root = Tk()
    Controlador(root)
    root.mainloop()
