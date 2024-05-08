import sqlite3 as sq
import os
import pandas as pd
datos = sq.connect("./datos/Sqlite/CochesEN.db")

cursor = datos.cursor()
tabla =  '''
    Create table IF NOT EXISTS Coches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modelo Varchar,
        clasificacion varchar,
        tipo varchar,
        id_coche varchar,
        id_coches intenger,
        FOREIGN KEY (id_coches) References Marca(id)
    )
'''
traducciones = {
    'Gasolina': 'Gasoline',
    'Eléctricos puros': 'Pure electric',
    'Gasóleo': 'Diesel',
    'Híbridos enchufables': 'Plug-in hybrid',
    'Híbridos de gasolina': 'Gasoline hybrid',
    'Gas natural': 'Natural gas',
    'Híbridos de gasóleo': 'Diesel hybrid',
    'Gases licuados del petróleo (GLP)': 'Liquefied petroleum gas (LPG)',
    'Pila de combustible': 'Fuel cell'
}
cursor.execute(tabla)
carpeta = "./datos/coches datos"
lista = os.listdir(carpeta)
columname =  ["Modelo","Clasificación Energética","Motorización"]
for archivo in lista:
    nombre = archivo.replace(".csv","")
    cursor.execute(f"select id from marca where nombre = '{nombre}'")  
    num = cursor.fetchone()  
    df = pd.read_csv(os.path.join(carpeta,archivo),usecols=columname)
    print(df)
    for indice,filas in df.iterrows():

        cursor.execute(f"INSERT into Coches(modelo,clasificacion,tipo,id_coche) Values('{filas["Modelo"]}','{filas["Clasificación Energética"]}','{traducciones[filas["Motorización"]]}',{num[0]})")
        datos.commit()
#cursor.execute("Select * from Marca")
#registros = cursor.fetchall()
#print(registros)
cursor.close()
datos.close()