from google.transit import gtfs_realtime_pb2
import orjson
import requests
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)


for entity in feed.entity:
    if entity.HasField('vehicle'):
        try:
            trip_name, timetable_id, timetable_version_id, dop_ref, set_type, number_of_cars, trip_instance = entity.vehicle.trip.trip_id.split(
                '.')
        except ValueError:
            trip_name = entity.vehicle.trip.trip_id
        print(entity.vehicle.trip.trip_id, trip_to_route.get(
            entity.vehicle.trip.trip_id, 'Unknown Route'))
        print(trip_name, entity.vehicle.position.latitude,
              entity.vehicle.position.longitude)
        print("https://anytrip.com.au/?selectedTrip=tripInstance%2F{}%2Fau2:st:{}%2F0".format('20200213', trip_name))


def get_feed_messages(mock_feed=False):
    if mock_feed:

        data_dir = os.path.dirname(os.path.abspath(__file__))
        with open('trips.json', 'r') as f:
            trip_to_route = orjson.loads(f.read())
        with open(os.path.join('tests', 'trains.protobuf'), 'rb') as f:
            trains_pb = f.read()
    else:
        headers = {
            'accept': 'application/x-google-protobuf',
            'authorization': 'apikey '+os.getenv('TFNSW_API_KEY'),
        }

        response = requests.get(
            'https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/sydneytrains', headers=headers)
        trains_pb = response.content

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(trains_pb)
    return feed


def get_train_latlons()
def get_t2_bmt_latlons()

if __name__ == "__main__":
  get_feed_messages()