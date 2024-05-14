import pandas as pd
import pymongo

archivo_Csv = r"BBDDSPAIN centraldecomunicacion.es DEMO.xlsx"
columname = ["EMPRESA","WEB","COMUNIDAD","DIRECCION","ACTIVIDAD"]
df = pd.read_excel(archivo_Csv,usecols=columname, engine='openpyxl')

# Conectar al servidor MongoDB (por defecto, se conectará a localhost en el puerto 27017)
cliente = pymongo.MongoClient("mongodb://localhost:27017/")

# Seleccionar la base de datos
base_de_datos = cliente["Empresas"]
coleccion = base_de_datos["EmpresasES"]
for indice, fila in df.iterrows():
    
    documento = {"id":indice,"nombre":fila[columname[0]],"web":fila[columname[1]],"direccion":fila[columname[3]],"provincia":fila[columname[2]],"actividad":fila[columname[4]]}
    print(documento)
    coleccion.insert_one(documento)

print(df)
