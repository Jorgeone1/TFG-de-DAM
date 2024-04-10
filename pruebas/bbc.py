import requests
from bs4 import BeautifulSoup

url = r'https://es.dbpedia.org/sparql?default-graph-uri=&query=PREFIX+dbo%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2F%3E%0D%0APREFIX+dbr%3A+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0D%0APREFIX+foaf%3A+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0A%0D%0ASELECT+DISTINCT+%3Factor+%3Fname+WHERE+%7B%0D%0A++%3Factor+a+dbo%3AAutomobile.%0D%0A++%3Factor+foaf%3Aname+%3Fname+.%0D%0A%7D%0D%0A&should-sponge=&format=text%2Fhtml&timeout=0&debug=on&run=+Run+Query+'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Aquí debes identificar la clase o el id de los elementos que contienen los titulares
    # Esto variará dependiendo de la estructura de la página
    print(soup)
    for headline in soup.find_all('pre', class_=''):  # Reemplaza 'tu_clase_aquí' con la clase correcta
        print(headline.get_text().strip())
else:
    print(f'Error al acceder al sitio: {response.status_code}')