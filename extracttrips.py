import requests
import os
import io
headers = {
    'accept': 'application/x-google-protobuf',
    'authorization': 'apikey '+os.getenv('TFNSW_API_KEY'),
}
#response = requests.get('https://api.transport.nsw.gov.au/v1/gtfs/schedule/sydneytrains', headers=headers)
#open('gtfs.zip', 'wb').write(response.content)
import zipfile
from tablib import Dataset
archive = zipfile.ZipFile('gtfs.zip', 'r')
trips = Dataset().load(io.TextIOWrapper(archive.open('trips.txt','r')),format='csv')
for trip in trips:
    print(trip['trip_id'],trip['route_id'])
