import pymongo

# Establece la conexión con la base de datos MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.GeneradorDeDatos
  # Reemplaza "nombre_de_tu_base_de_datos" con el nombre de tu base de datos
coleccion = db.NombreEng  # Reemplaza "nombre_de_tu_coleccion" con el nombre de tu colección

# Ejecuta la agregación para seleccionar un documento aleatorio con género "M"
documento_aleatorio = coleccion.aggregate([
    { "$match": { "gender": "M" } },  # Filtrar por género "M"
    { "$sample": { "size": 1 } }       # Seleccionar un documento aleatorio
])

# Itera sobre el cursor resultante y obtén el documento aleatorio
for documento in documento_aleatorio:
    print(documento)
