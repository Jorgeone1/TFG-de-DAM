import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/countries"

querystring = {"namePrefix":"M"}

headers = {
	"X-RapidAPI-Key": "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
	"X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())