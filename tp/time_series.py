import csv
import json
import requests
import os

API_KEY = '12a962097bf447b9b4e8d27514c34e75'
BASE_URL = 'https://api.twelvedata.com/time_series'
OUTPUT_FILE = 'time_series_data.json'

def fetch_time_series(symbol):
    params = {
        'symbol': symbol,
        'interval': '1day',
        'outputsize': '1095',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def main():
    symbols = []
    with open('clean_meme.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            symbols.append(row['symbol'])

    # Load existing data if the file exists
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as json_file:
            all_data = json.load(json_file)
    else:
        all_data = {}

    for symbol in symbols:
        code = all_data.get(symbol, {'code' : 0}).get('code', 200)
        if symbol in all_data and 'status' in all_data[symbol] and (code == 200 or code == 404):
            print(f'Skipping {symbol}, already have successful data.')
            continue

        print(f'Fetching data for {symbol}...')
        data = fetch_time_series(symbol)
        if data.get('code', 200) == 429:
            print('API limit reached. Exiting.')
            break
        all_data[symbol] = data

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, indent=4)

    print(f'Data saved to {OUTPUT_FILE}')
    print(f"Total succesful retrieves: {len([s for s in all_data if all_data[s].get('code', 200) == 200])}")
    print(f"Total succesful retrieves: {len([s for s in all_data if all_data[s].get('code', 200) != 429])}")

if __name__ == '__main__':
    main()