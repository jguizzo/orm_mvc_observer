from tkinter import *

class Ventana_secundaria():

    def __init__(self, window, datos, objeto):
        self.root_sec = window
        self.objeto_base = objeto

        self.id = datos.id
        self.concepto2 = StringVar(value=datos.concepto)
        self.valor2 = StringVar(value=datos.valor)
        self.fecha2 = StringVar(value=datos.fecha)
        self.descripcion2 = StringVar(value=datos.descripcion)

        # Frame
        self.root_sec.title("Búsqueda de datos")
        self.root_sec.resizable(width=False, height=False)

        # Etiquetas
        self.label0 = Label(self.root_sec, text="ID:")
        self.label0.grid(row=1, column=0, sticky=E, padx=5, pady=5)

        self.label1 = Label(
            self.root_sec, text=self.id, width=4, bg='white')
        self.label1.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        self.label2 = Label(self.root_sec, text="Concepto:")
        self.label2.grid(row=2, column=0, sticky=E, padx=5, pady=5)

        self.label3 = Label(self.root_sec, text="Valor en $:")
        self.label3.grid(row=3, column=0, sticky=E, padx=5, pady=5)

        self.label4 = Label(self.root_sec, text="Fecha:")
        self.label4.grid(row=4, column=0, sticky=E, padx=5, pady=5)

        self.label5 = Label(self.root_sec, text="(dd/mm/yyyy)")
        self.label5.grid(row=4, column=1, sticky=W+E, padx=5, pady=5)

        self.label6 = Label(self.root_sec, text="Descripción:")
        self.label6.grid(row=5, column=0, sticky=E, padx=5, pady=5)

        # Entradas
        self.ancho = 40

        self.concepto_entry = Entry(self.root_sec, width=self.ancho,
                                    textvariable=self.concepto2, bg='white')
        self.concepto_entry.grid(row=2, column=1, padx=5, pady=5)

        self.valor_entry = Entry(
            self.root_sec, width=15, textvariable=self.valor2, bg='white')
        self.valor_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        self.fecha_entry = Entry(
            self.root_sec, width=10, textvariable=self.fecha2, bg='white')
        self.fecha_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        self.descripcion_entry = Entry(self.root_sec, width=self.ancho,
                                       textvariable=self.descripcion2, bg='white')
        self.descripcion_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botones
        b_alta = Button(self.root_sec, text="Modificar", width=7,
                        command=lambda: self.modificar_registro())
        b_alta.grid(row=6, column=1, padx=5, pady=5, sticky='E')

    def modificar_registro(self,):
        self.objeto_base.modificar_registro(
            self.id, self.concepto_entry, self.valor_entry, self.fecha_entry, self.descripcion_entry)
        print("===============================")
        print("Cierro ventana secundaria")
        self.root_sec.destroy()
