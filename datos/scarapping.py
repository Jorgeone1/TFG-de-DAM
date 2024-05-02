import os
import sqlite3 as sq
carpeta = r".\datos\coches datos"
lista = os.listdir(carpeta)

for archivo in lista:
    nuevo_nombre = archivo.replace(" ","") 
    ruta_original = os.path.join(carpeta, archivo)
            # Ruta completa del nuevo archivo
    ruta_nuevo = os.path.join(carpeta, nuevo_nombre)
    os.rename(ruta_original, ruta_nuevo)