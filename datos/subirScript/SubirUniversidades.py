import pandas as pd
import pymongo
import numpy as np

archivo_Csv = r"C:\Users\jww11\Documents\GitHub\TFG-de-DAM\datos\Universidades Espanolas.csv"
Archivo = r"./datos/listado_centros.xlsx"
columname = ["Comunidad","Nombre","Direccion","Email","Telefono","Tipo"]
column = ["DENOMINACIÓN GENÉRICA","DOMICILIO","TELÉFONO","PROVINCIA","CÓD POSTAL","NATURALEZA"]
df = pd.read_csv(archivo_Csv,usecols=columname)
dfa = pd.read_excel(Archivo,usecols=column)
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
base = cliente["Instituciones"]
para = base["Universidad"]
for indice, fila in df.iterrows():
    documento = {"id":indice,"name":fila[columname[1]],"TOWN":fila[columname[0]],"Street":fila[columname[2]],"Phone":fila[columname[4]],"Email":fila[columname[3]]}
    print(documento)
    para.insert_one(documento)

#base = sq.connect(r"./datos/Sqlite/institution.db")
