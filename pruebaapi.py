import requests

url = "https://twitter-data1.p.rapidapi.com/AutoComplete/"

querystring = {"q":"MDasito"}

headers = {
	"X-RapidAPI-Key": "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
	"X-RapidAPI-Host": "twitter-data1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data  =response.json()
nombres = [usuario['name'] for usuario in data['users']]

# Imprimir los nombres
for nombre in nombres:
    print(nombre)