import pydantic as da
from faker import Faker 

fake = Faker()
hola = []
for i in range(10):
    hola.append({"nombre":fake.name(),"correo":fake.email(),"telefono":fake.phone_number()})
tab = "\t"
cantidad = 0
xml = "<nombre>"
for holas in hola:
    cantidad = 1
    xml+=f"\n{tab*cantidad}<nombres>"
    cantidad = cantidad+2
    for indice, dato in holas.items():
        xml += f"\n{tab*cantidad}<{indice}>{dato}</{indice}>"
    cantidad = 1
    xml +=f"\n{tab*cantidad}<nombres>"
xml += "\n</nombre>"

basededatos=""
for holas in hola:
    indices = list(holas.keys())
    datos = list(holas.values())
    basededatos += f"insert into nombre({",".join(map(str,indices))}) Values({",".join(map(str,datos))});\n"

json = "["
for holas in hola:
    json+="\n\t{"
    for indice,dato in holas.items():
        json+= f'\n\t\t"{indice}":"{dato}"'
    json +="\n\t}"
json +="\n]"
print(json)