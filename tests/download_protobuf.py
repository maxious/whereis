from tablib import Dataset
import zipfile
import requests
import os
import io
import orjson
from dotenv import load_dotenv
load_dotenv(verbose=True)
headers = {
    'accept': 'application/x-google-protobuf',
    'authorization': 'apikey '+os.getenv('TFNSW_API_KEY'),
}

response = requests.get(
    'https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/sydneytrains', headers=headers)
open('trains.protobuf', 'wb').write( response.content)
