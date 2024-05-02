import json
import pandas as pd
import pymongo

# Conectar al servidor MongoDB (por defecto, se conectará a localhost en el puerto 27017)
cliente = pymongo.MongoClient("mongodb://localhost:27017/")

# Seleccionar la base de datos
base_de_datos = cliente["GeneradorDeDatos"]
coleccion = base_de_datos["NombreEng"]

# Ruta al archivo JSON
ruta_json = "./datos/ESGivenMale.json"

# Abrir el archivo JSON y leer los datos
with open(ruta_json, "r") as archivo:
    # Cargar los datos del archivo JSON en una variable
    datos = json.load(archivo)
for indice, elemento in enumerate(datos):
    # Extraer los campos 'name' y 'gender'
    nombre = elemento["name"]
    genero = elemento["gender"]
    
    # Crear un nuevo diccionario con 'name', 'gender' e 'indice'
    documento = {"name": nombre, "gender": genero, "id": indice+95025}
    
    # Insertar el documento en la colección de MongoDB
    coleccion.insert_one(documento)

print("Los datos se han subido exitosamente a MongoDB.")
cliente.close()