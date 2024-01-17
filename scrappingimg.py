import requests
from bs4 import BeautifulSoup

# URL de la página que quieres raspar
url = 'https://imgur.com/search?q=españa'

# Realiza una solicitud HTTP para obtener el contenido de la página
response = requests.get(url)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    # Parsea el contenido HTML de la página
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encuentra todas las etiquetas "img" en la página
    img_tags = soup.find_all('img')
    
    # Itera a través de las etiquetas "img" y obtén el atributo "src"
    for img_tag in img_tags:
        src = img_tag.get('src')
        if src:
            print("SRC encontrado:", src)
else:
    print("No se pudo acceder a la página")