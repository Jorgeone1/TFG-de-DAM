from pymongo import MongoClient

# Conectarse a la base de datos
cliente = MongoClient('localhost', 27017)
base_de_datos = cliente["GeneradorDeDatos"]
coleccion = base_de_datos["NombreEsp"]


# Actualizar todos los documentos en la colección
coleccion.update_many(
    {},  # Filtro vacío para aplicar la actualización a todos los documentos
    { "$rename": { "indices": "id" } }  # Operador $rename para cambiar el nombre del campo
)