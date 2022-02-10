

class Gastos():
    def __init__(self,):
        self.concepto = 'hola'
        self.valor = '2323'
        self.fecha = '8/12/2021'
        self.descripcion = "sdfsdfsdf"


gasto = Gastos()


print(gasto)
valores = ['chau', '24354', '12/12/1212', 'sdfgsdgf']
campos = ['self.concepto', 'self.valor', 'self.fecha', 'self.descripcion']

for n in range(len(campos)):
    gasto[campos[n]] = valores[n]

print(gasto)
