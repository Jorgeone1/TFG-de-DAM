import requests
from bs4 import BeautifulSoup

URL = "https://generador-de-dni.com/generador-de-cuentas-bancarias"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="bank-generator")
job_elements = results.find_all("div", class_="content")
print(job_elements)

