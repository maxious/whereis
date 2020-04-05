from google.transit import gtfs_realtime_pb2
import orjson
import requests
import os
import re
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TEST_DIR = os.path.join(BASE_DIR, 'tests')
trip_to_route = None


def _load_trip_to_route():
    global trip_to_route
    if not trip_to_route:
        with open(os.path.join(DATA_DIR, 'trips.json'), 'r') as f:
            trip_to_route = orjson.loads(f.read())
    return trip_to_route


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
    return {entity.vehicle.trip.trip_id: (entity.vehicle.position.latitude, entity.vehicle.position.longitude)
               for entity in feed.entity if entity.HasField('vehicle')}


def get_filtered_latlons(route_id_filter, feed=None):
    if feed is None:
        feed = get_feed_messages()
    trip_to_route = _load_trip_to_route()

    return {trip: latlon 
    for trip, latlon in get_train_latlons(feed).items() 
    if re.search(route_id_filter, trip_to_route.get(trip, ''))}

def get_filtered_triproutes(route_id_filter, feed=None):
    if feed is None:
        feed = get_feed_messages()
    trip_to_route = _load_trip_to_route()

    return {trip: {"lat":lat,"lon": lon, "route": trip_to_route.get(trip, '')} 
    for trip, (lat,lon) in get_train_latlons(feed).items() 
    if re.search(route_id_filter, trip_to_route.get(trip, ''))}


def get_anytrip_url(trip_id, date=datetime.now().strftime("%Y%m%d")):
    try:
        trip_name, timetable_id, timetable_version_id, dop_ref, set_type, number_of_cars, trip_instance = trip_id.split(
            '.')
    except ValueError:
        trip_name = trip_id
    return "https://anytrip.com.au/?selectedTrip=tripInstance%2F{}%2Fau2:st:{}%2F0".format(date, trip_name)


if __name__ == "__main__":
    # get_feed_messages()
    # get_train_latlons()

    # print("trip,lon,lat")
    # [print("%s,%s,%s"%(x,lon,lat)) for x,(lat,lon) in get_filtered_latlons("IWL_1|BMT_1", get_feed_messages(True)).items()]
 
    print("trip,route,lon,lat")
    it = get_filtered_latlons("IWL_1|BMT_1", get_feed_messages(True)).items()
    [print("%s,%s,%s,%s,%s"%(x,y['route'],y['lon'],y['lat'],get_anytrip_url(x))) 
    for x,y in get_filtered_triproutes("IWL_1|BMT_1", get_feed_messages(True)).items()]
