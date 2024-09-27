import json
import csv
from requests import Session
from flatten_json import flatten

def get_response(session, start):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    params = {
        'start': start,
        'limit': '1000',
        'convert': 'USD'
    }
    response = session.get(url, params=params)
    data = json.loads(response.text)
    data = [coin for coin in data['data'] if 'memes' in coin['tags']]
    for coin in data:
        coin.pop('tags', None)
    return [flatten(coin) for coin in data]

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'f409ec0a-ee30-427f-acf7-1a0d486d5b5f',
}

session = Session()
session.headers.update(headers)

csv_file = 'memecoins.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    memecoins = get_response(session, 1)

    fieldnames = set()
    for coin in memecoins:
        fieldnames.update(coin.keys())
    
    for i in range(1, 20):
        memecoins += get_response(session, (i * 1000) + 1)
    
    fieldnames = list(fieldnames)
    for key in ['symbol', 'name', 'id']:
        fieldnames.remove(key)
        fieldnames.insert(0, key)
    
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(memecoins)