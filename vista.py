from tkinter import ttk
from tkinter import *
import datetime
from turtle import width
from modelo import Abmc, Observador


# Defino el formato en el que obtengo la fecha actual.
fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")


class Ventana_principal():

    def __init__(self, window):
        self.root = window

        self.concepto = StringVar()
        self.valor = StringVar()
        self.fecha = StringVar(value=fecha_actual)
        self.descripcion = StringVar()
        self.ancho = 40
        self.objeto_base = Abmc()

        #### Creo el observador de Abmc ####
        observador_abmc = Observador(self.objeto_base)

        # Frame
        self.root.title("Registro de Gastos")
        self.root.resizable(width=False, height=False)
        #self.root.geometry('1000x1100')
        ventana = Frame(self.root)
        ventana.grid(row = 0, column = 0, padx = 5, pady = 5)
        ventana.columnconfigure(0, weight=1)
        ventana.rowconfigure(0, weight=1)

        # Etiquetas
        self.label0 = Label(ventana, text="Ingrese los valores",
                            background='yellow', foreground='black')
        self.label0.grid(row=0, column=0, columnspan=6,
                         padx=5, pady=5, sticky=W + E)

        self.label1 = Label(ventana, text="Concepto:")
        self.label1.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        self.label2 = Label(ventana, text="Valor en $:")
        self.label2.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        self.label3 = Label(ventana, text="(no usar $ o .)")
        self.label3.grid(row=2, column=1, sticky=E, padx=5, pady=5)

        self.label4 = Label(ventana, text="Fecha:")
        self.label4.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.label5 = Label(ventana, text="(dd/mm/yyyy)")
        self.label5.grid(row=3, column=1, sticky=W+E, padx=5, pady=5)

        self.label6 = Label(ventana, text="Descripción:")
        self.label6.grid(row=4, column=0, sticky=W, padx=5, pady=5)

        self.label7 = Label(ventana, text="Registro")
        self.label7.grid(row=5, column=0, sticky=W, padx=5, pady=15)

        # Entradas
        fondo_entry = 'grey'

        self.concepto_entry = Entry(
            ventana, width=self.ancho, textvariable=self.concepto, bg= fondo_entry)
        self.concepto_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        self.valor_entry = Entry(
            ventana, width=15, textvariable=self.valor, bg=fondo_entry)
        self.valor_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        self.fecha_entry = Entry(
            ventana, width=10, textvariable=self.fecha, bg=fondo_entry)
        self.fecha_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        self.descripcion_entry = Entry(ventana, width=self.ancho,
                                       textvariable=self.descripcion, bg=fondo_entry)
        self.descripcion_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # Botones
        self.ancho_boton = 7
        self.b_alta = Button(ventana, text="Cargar", width=self.ancho_boton,
                             command=lambda: self.alta())
        self.b_alta.grid(row=5, column=1, padx=5,
                         pady=5, sticky=E, columnspan=2)

        self.b_baja = Button(ventana, text="Borrar", width=self.ancho_boton,
                             command=lambda: self.borrar())
        self.b_baja.grid(row=9, column=2, padx=5, pady=5)

        self.b_busqueda = Button(ventana, text="Buscar",
                                 width=self.ancho_boton, command=lambda: self.buscar())
        self.b_busqueda.grid(row=9, column=1, padx=5, pady=5, sticky='E')

        self.b_salir = Button(ventana, text="Salir", width=self.ancho_boton,
                              command=lambda: (self.root.destroy(), print("Bye !")))
        self.b_salir.grid(row=9, column=0, padx=5, pady=5, sticky='W')

        # Treeview
        tema =ttk.Style()
        tema.configure('Treeview', rowheight = 40)
        self.tree = ttk.Treeview(ventana, height = 16)
        self.tree.grid(
            column = 0, 
            row = 7, 
            columnspan = 3, 
            padx = (5,0), pady = (10,5)
            )
        scrollbar = ttk.Scrollbar(
            ventana, 
            orient="vertical", 
            command = self.tree.yview
            )
        scrollbar.grid(row=7, column=3, sticky='ns', padx = 0 , pady = (10,5))
        
        self.tree.configure(yscrollcommand = scrollbar.set)
        self.tree["columns"] = ("col1", "col2", "col3", "col4")
        self.tree.column("#0", width=80, minwidth=50, anchor=W)
        self.tree.heading('#0', text='ID')
        self.tree.column("col1", width=200, minwidth=100)
        self.tree.heading('col1', text='Concepto')
        self.tree.column("col2", width=150, minwidth=100, anchor= "center")
        self.tree.heading('col2', text='Valor [$]')
        self.tree.column("col3", width=200, minwidth=100, anchor= "center")
        self.tree.heading('col3', text='Fecha')
        self.tree.column("col4", width=300, minwidth=130)
        self.tree.heading('col4', text='Descripción')
        # Actualizo treeview luego de crearlo
        self.objeto_base.info_db_treeview(self.tree)

    def alta(self,):
        self.objeto_base.alta_db(self.tree, self.concepto_entry, self.valor_entry,
                                 self.fecha_entry, self.descripcion_entry)

    def borrar(self,):
        self.objeto_base.borrar_registro_treeview(self.tree)

    def buscar(self,):
        self.objeto_base.buscar_registro(self.tree, self.objeto_base)

    def modificar_registro(self, id, concepto2, valor2, fecha2, descripcion2):
        self.objeto_base(id, concepto2, valor2, fecha2, descripcion2)
