import requests

headers = {
    'authority': 'api.transport.nsw.gov.au',
    'accept': 'application/x-google-protobuf',
    'authorization': 'apikey '+ENV['TFNSW_API_KEY'],
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'origin': 'https://opendata.transport.nsw.gov.au',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'referer': 'https://opendata.transport.nsw.gov.au/node/330/exploreapi',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
}

response = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/sydneytrains', headers=headers)

