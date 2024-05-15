import pymongo,json
import requests

def obtener_datos():
    url = 'http://127.0.0.1:5000/nombres/F/ES/100/nom'
    response = requests.get(url)
    data = response.json()  # Convertir la respuesta a JSON
    print("Datos recibidos del servidor:")
    print(data["nom"])
if __name__ == '__main__':
    obtener_datos()
