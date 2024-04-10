import requests

url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/back"

querystring = {"limit":"10"}

headers = {
	"X-RapidAPI-Key": "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())