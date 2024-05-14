import requests
from bs4 import BeautifulSoup

# Realiza una solicitud HTTP para obtener el contenido HTML de la URL
url = "https://www.google.com/search?tbm=bks&q=queso"
response = requests.get(url)
html_content = response.content

# Pasa el contenido HTML a BeautifulSoup para el análisis
soup = BeautifulSoup(html_content, 'html.parser')

# Encuentra todos los divs con la clase "MjjYud"
divs_mjjyud = soup.find_all('div', class_='MjjYud')
print(divs_mjjyud)
# Itera sobre cada div y extrae los enlaces
for div in divs_mjjyud:
    # Encuentra todos los enlaces dentro del div actual
    links = div.find_all('a')
    
    # Itera sobre los enlaces e imprime o almacena su URL
    for link in links:
        print(link['href'])  # Imprime la URL del enlace
