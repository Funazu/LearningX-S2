import requests

api_key = "103a0d3f-95c5-494e-b411-b3c24ed4a005"
keyword = "potato"
url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'

res = requests.get(url)

definitions = res.json()

for definition in definitions:
    print(definition)