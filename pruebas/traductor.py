import requests

url = "https://microsoft-translator-text.p.rapidapi.com/translate"

querystring = {"to[0]":"<REQUIRED>","api-version":"3.0","profanityAction":"NoAction","textType":"plain"}

payload = [{ "Text": "I would really like to drive your car around the block a few times." }]
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
	"X-RapidAPI-Host": "microsoft-translator-text.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers, params=querystring)

print(response.json())