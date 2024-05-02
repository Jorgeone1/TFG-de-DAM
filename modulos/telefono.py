import random

def crearTelefono(idioma,tipo):
    telefono = ""

    if idioma == "ES":
        if tipo:
            telefono = "9"
            for i in range(8):
                telefono = telefono +str(round(random.uniform(0,9)))
            return telefono
        else:
            rand = round(random.uniform(0,1))
            if rand == 0:
                telefono = "6"
            else:
                telefono="7"
            for i in range(8):
                telefono = telefono +str(round(random.uniform(0,9)))
            return telefono
    elif idioma == "EN":
        telefono = ""
        if tipo:
            telefono = "01"
            for i in range(9):
                telefono = telefono + str(round(random.uniform(0,9)))
            return telefono
        else:
            telefono = "07"
            for i in range(9):
                telefono = telefono + str(round(random.uniform(0,9)))
            return telefono
        
print(crearTelefono("EN",True))