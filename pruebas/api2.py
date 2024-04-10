import requests

url = "https://twitter-data1.p.rapidapi.com/Search/"

querystring = {"q":"MDasito","count":"20"}

headers = {
	"X-RapidAPI-Key": "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
	"X-RapidAPI-Host": "twitter-data1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())