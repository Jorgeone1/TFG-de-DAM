import requests
from bs4 import BeautifulSoup

url = 'https://testingdatagenerator.com/doi.html'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Aquí debes identificar la clase o el id de los elementos que contienen los titulares
    # Esto variará dependiendo de la estructura de la página
    print(soup)
    for headline in soup.find_all('span', class_=''):  # Reemplaza 'tu_clase_aquí' con la clase correcta
        print(headline.get_text().strip())
else:
    print(f'Error al acceder al sitio: {response.status_code}')