import pymongo

cliente = pymongo.MongoClient("mongodb://localhost:27017/")
db = cliente["GeneradorDeDatos"]["PaisEN"]
# datos = db.aggregate([
#     { "$group": { "_id": "$continente", "conti": { "$addToSet": "$continente" } } }
# ])
datos = db.aggregate([{ "$sample": { "size": 1}}]).next()
print (datos)