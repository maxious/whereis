from google.transit import gtfs_realtime_pb2
import orjson
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)
DATA_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'data')


def get_feed_messages(mock_feed=False):
    if mock_feed:
        data_dir = os.path.dirname(os.path.abspath(__file__))
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


def get_train_latlons(feed=None):
    if feed is None:
        feed = get_feed_messages()
    latlons = {}

    for entity in feed.entity:
        if entity.HasField('vehicle'):
            # with open('/home/maxious/whereis/data/trips.json', 'r') as f:
            #     trip_to_route = orjson.loads(f.read())
            # try:
            #     trip_name, timetable_id, timetable_version_id, dop_ref, set_type, number_of_cars, trip_instance = entity.vehicle.trip.trip_id.split(
            #         '.')
            # except ValueError:
            #     trip_name = entity.vehicle.trip.trip_id
            # print(entity.vehicle.trip.trip_id, trip_to_route.get(
            #     entity.vehicle.trip.trip_id, 'Unknown Route'))
            # print(trip_name, entity.vehicle.position.latitude,
            #       entity.vehicle.position.longitude)
            #
            latlons[entity.vehicle.trip.trip_id] = (entity.vehicle.position.latitude,
                                                    entity.vehicle.position.longitude)
    return latlons


def get_filtered_latlons(route_id_filter, feed=None):
    if feed is None:
        feed = get_feed_messages()
    raw_latlons = get_train_latlons(feed)
    latlons = {}
    with open(os.path.join(DATA_DIR, 'trips.json'), 'r') as f:
        trip_to_route = orjson.loads(f.read())
    for trip, latlon in raw_latlons.items():
        (lat, lon) = latlon
        if route_id_filter in trip_to_route.get(trip, ''):
            print(trip, trip_to_route.get(trip), latlon)
            latlons[trip] = latlon
    return latlons


def get_anytrip_url(trip_id, date=datetime.now().strftime("YMD")):
    try:
        trip_name, timetable_id, timetable_version_id, dop_ref, set_type, number_of_cars, trip_instance = trip_id.split(
            '.')
    except ValueError:
        trip_name = trip_id
    return "https://anytrip.com.au/?selectedTrip=tripInstance%2F{}%2Fau2:st:{}%2F0".format(date, trip_name)

# if __name__ == "__main__":
    # get_feed_messages()
    # get_train_latlons()
    # get_filtered_latlons("IWL_1")
