import requests
import json
url = "https://transfermarket.p.rapidapi.com/clubs/get-profile"

querystring = {"id":"1","domain":"de"}

headers = {
	"X-RapidAPI-Key": "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
	"X-RapidAPI-Host": "transfermarket.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

jsondata = response.json()
market_value = jsondata['mainFacts']
print("Valor de mercado:", market_value)