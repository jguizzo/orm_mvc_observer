import re


def validador(*args):
    valores = []

    for n in args:
        valores.append(n.get())

    # Defino patrones a validar -> patrones(Concepto, Valor, Fecha, Desscripcion )
    patrones = (re.compile('\w+'), re.compile('\d+'),
                re.compile('\d+/\d+/\d{4}'), re.compile('\w+'))
    try:
        i = 0
        for patron in patrones:
            if patron.match(valores[i]):
                i += 1
                print(f"Campo {i} OK")
            else:
                raise TypeError(f"Campo {i} inválido")
    except TypeError as mensaje:
        return mensaje
    else:
        return valores

