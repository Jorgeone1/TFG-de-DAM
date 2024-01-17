import http.client

conn = http.client.HTTPSConnection("open-weather13.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "5bc5499bfcmsh73f439fe6a74a7fp111394jsn66dd4d5ba73d",
    'X-RapidAPI-Host': "open-weather13.p.rapidapi.com"
}

conn.request("GET", "/city/madrid", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))