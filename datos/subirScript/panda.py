import pandas as pd
import pymongo

archivo_Csv = r"./datos/empresas.xlsx"
columname = ["Company Name"]
df = pd.read_excel(archivo_Csv,usecols=columname)


# Conectar al servidor MongoDB (por defecto, se conectará a localhost en el puerto 27017)
cliente = pymongo.MongoClient("mongodb://localhost:27017/")

# Seleccionar la base de datos
base_de_datos = cliente["GeneradorDeDatos"]
coleccion = base_de_datos["Apellidos"]
for indice, fila in df.iterrows():
    documento = fila.to_dict()
    documento["id"] = indice
    #coleccion.insert_one(documento)

print(df)
