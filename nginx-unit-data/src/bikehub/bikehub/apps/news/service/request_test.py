import requests

url = 'http://133.167.102.92:8888/rest/news/'
headers = {'Authorization': 'Api-Key hnIVbuI3.4zBiAkyiOWFR5abnm26JcBCQ2Niqa6QCu'}

x = requests.get(url,headers=headers)

print(x.text)