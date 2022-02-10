import encodings
from time import strftime
from tkinter import messagebox
import sqlite3
from peewee import *
from peewee import PeeweeException
from controlador import *
from regex import validador
from datetime import datetime
import logging

####### PEEWEE CONFIG #######
db = SqliteDatabase('registro.db')

class BaseModel(Model):
    class Meta:
        database = db
class Gastos(BaseModel):
    concepto = TextField()
    valor = IntegerField()
    fecha = TextField()
    descripcion = TextField()


####### LOG FILE #######
LOG_FILENAME = 'registro.log'
logging.basicConfig(
    filename = LOG_FILENAME,
    level = logging.INFO,
    format = '%(asctime)s  -  %(message)s',
    datefmt = '%d-%m-%Y %H:%M:%S %p'
)
logging.info("####### EJECUTANDO SCRIPT controlador.py #######")




####### DECORADOR #######
def registro_log(funcion):
    def wrapper(*args):
        logging.info("Llamada a la funcion: %s" % funcion.__name__)
        
        if funcion.__name__ == 'alta_db':
            logging.info("Datos cargados: %s - %s - %s - %s " , 
            args[2].get(), 
            args[3].get(), 
            args[4].get(), 
            args[5].get())
        return funcion(*args)
    return wrapper


####### PATRON OBSERVADOR #######

####### CLASE OBSERVABLE ########
class Observable():

    observadores = []

    def agregar(self, observador):
        self.observadores.append(observador)

    def quitar(self, observador):
        self.observadores.remove(observador)

    def notificar(self, metodo):
        for observador in self.observadores:
            return observador.update(metodo)


class Observador():

    def __init__(self, objeto):
        self.observar = objeto
        self.observar.agregar(self)
    
    def update(self, metodo):
        print("Se ejecuto el metodo: %s" % metodo)


###### CLASE OBSERVABLE ###########
class Abmc(Observable):

    def __init__(self,):
        try:        
            db.connect()
            if not db.table_exists(Gastos):
                db.create_tables([Gastos])            
        except PeeweeException as mensaje:
            print(mensaje)
        else:
            print("Base de datos creada con éxito")
        finally:
            db.close()


    # Carga la tabla de la DB en treeview.
    def info_db_treeview(self, tree):
        tree.delete(*tree.get_children())
        try:
            registros = Gastos.select().tuples()
        except sqlite3.DatabaseError as mensaje:
            self.pop_up_error("Error en DB", mensaje)
            print("Error en base de datos")
        else:
            for info in registros:
                tree.insert("", "end", text=info[0], values=(
                    info[1], info[2], info[3], info[4]))
        finally:
            db.close()


    # Realiza el alta de los datos en la base.
    @registro_log
    def alta_db(self, tree, *args):
        try:
            valores = validador(*args)
            gasto = Gastos()

            gasto.concepto = valores[0]
            
            gasto.valor = valores[1]
            gasto.fecha = valores[2]
            gasto.descripcion = valores[3]

            gasto.save()

            print("===============================")
            print("Datos ingresados: ")
            for n in valores:
                print(n, end=" ")
            print()
            print("===============================")

        except PeeweeException as mensaje:
            self.pop_up_error("Error en DB", mensaje)
            print("No se pudo cargar")
        except TypeError:
            print("Error en valores cargados")
            self.pop_up_error("Error", valores)
        else:
            self.info_db_treeview(tree)
            self.limpiar_celdas(*args)
            print("Carga exitosa")
            #print(FunctionName)
            #Observable.notificar(self, self.__name__)
            print(Abmc.alta_db.__name__)


    @registro_log
    def baja_db(self, item_id):
        try:
            borrar = Gastos.get_by_id(item_id)
            borrar.delete_instance()

        except PeeweeException as mensaje:
            self.pop_up_error("Error en DB", mensaje)
            print("No se pudo borrar")
        else:
            print("Borrado exitoso")
            logging.info("Se borro el item: %s" % item_id)


    # Limpia los caracteres ingresado en la celda de texto.
    def limpiar_celdas(self, *args):
        for valor in args:
            valor.delete(0, END)

    # Borra registro del treeview
    def borrar_registro_treeview(self, tree):
        item_focus = tree.focus()
        item_actual = tree.item(item_focus)
        if item_actual['text'] != '':
            item_id = item_actual['text']
            print("===============================")
            print("Se borró el item: ", item_id)
            tree.delete(item_focus)
            self.baja_db(item_id)  # Llamo funcion que borra registro en DB.
        else:
            self.pop_up_error("Error al borrar", "Seleccione item a eliminar")

    def buscar_registro(self, tree, objeto_base):
        self.objeto_base = objeto_base
        self.tree = tree
        item_focus = self.tree.focus()
        item_actual = self.tree.item(item_focus)
        if item_actual['text'] != '':
            item_id = item_actual['text']
            print("===============================")
            print("Seleccionó item: ", item_id)
            # Llamo funcion que busca registro en DB.
            self.datos_busqueda(item_id)
        else:
            self.pop_up_error("Error al buscar", "Seleccione item a buscar")
            messagebox.showinfo(
                message="Seleccione item a buscar", title="Error al modificar")

    @registro_log
    def datos_busqueda(self, item_id):
        try:
            self.datos = Gastos.get_by_id(item_id)
        except PeeweeException as mensaje:
            self.pop_up_error("Error en DB", mensaje)
        else:
            self.call_ventana(self.objeto_base)


    # Revisa los datos modificados y los actualiza en la DB
    @registro_log
    def modificar_registro(self, id, *args):
        datos = validador(*args)
        datos.append(id)
        print(datos)

        try:
            actualizar = Gastos.update(concepto = datos[0], valor = datos[1], fecha = datos[2], descripcion = datos[3]).where(Gastos.id == datos[4])
            actualizar.execute()
            self.info_db_treeview(self.tree)
        except PeeweeException as mensaje:
            self.pop_up_error("Error en DB", mensaje)
        else:
            print("Modificacion exitosa")
            logging.info("Se modificó el item: %s" % id)

    # Invoca el metodo en el controlador que inicializa la ventana secundaria
    def call_ventana(self, objeto_base):
        Controlador.ventana_secundaria(self, self.datos, objeto_base)

    def pop_up_error(self, *args):
        messagebox.showinfo(message=args[1], title=args[0])
