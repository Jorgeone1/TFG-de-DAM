
import requests

# Pedir al usuario la cantidad de DNIs a generar
cantidad = int(input("Ingrese la cantidad de DNIs a generar: "))

# Enviar solicitud POST a la ruta /codigo con la cantidad especificada
response = requests.post('http://localhost:5000/codigo', data={'cantidad': cantidad})

if response.status_code == 200:
    data = response.json()
    dniss = data['dniss']
    print("DNIs generados:")
    for dni in dniss:
        print(dni)
else:
    print("Error al obtener los DNIs:", response.status_code)
