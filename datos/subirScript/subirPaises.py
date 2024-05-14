import requests
from bs4 import BeautifulSoup
import pymongo
# URL de la página que contiene la tabla 
url = 'https://www.sport-histoire.fr/es/Geografia/Paises_en_orden_alfabetico.php'
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
base = cliente["GeneradorDeDatos"]
para = base["PaisES"]
continentes = {
    "África": "Africa",
    "América": "America",
    "Asia": "Asia",
    "Europa": "Europe",
    "Oceanía": "Oceania",
    "Antártida": "Antarctica"
}
# Realizar la solicitud HTTP
response = requests.get(url)

# Crear el objeto BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

tablas = soup.find_all('table',class_="tableau_gris_centrer")
id = 0
filtro = True

if tablas:
    for tabla in tablas:  
        filas = tabla.find_all('tr')
        
        # Iterar sobre cada fila
        for fila in filas:
            # Extraer todas las celdas de la fila
            celdas = fila.find_all('td')
            indice = 0
            dicts = {}
            # Imprimir el contenido de cada celda
            for celda in celdas:
                
                if indice == 0:
                    if celda.text =="\n\n":
                        filtro = False
                        break
                    dicts["pais"] = celda.text
                if indice == 1:
                    dicts["capital"] = celda.text
                if indice ==2:
                    hola = celda.text
                    holas = hola.replace("\n","")
                    dicts["continente"]= holas
                indice += 1
            if filtro:
                dicts["id"] = id
                para.insert_one(dicts)
                print(dicts)
                id += 1
            else:
                filtro = True

            
    