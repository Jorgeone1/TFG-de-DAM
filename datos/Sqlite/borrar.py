import sqlite3 as sq

conexion = sq.connect("./datos/sqlite/CochesES.db")

cursor = conexion.cursor()

cursor.execute("Select distinct tipo from Coches ")
datos = cursor.fetchall()

print(datos)
cursor.close()
conexion.close()