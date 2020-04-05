from whereis import trains
from datetime import datetime


def test_feed_messages():
    feed_messages = trains.get_feed_messages(True)
    assert feed_messages != None


def test_train_latlons():
    train_latlons = trains.get_train_latlons(trains.get_feed_messages(True))
    assert len(train_latlons) == 142


def test_trip_to_route():
    train_latlons = trains.get_train_latlons(trains.get_feed_messages(True))
    trip_to_route = trains._load_trip_to_route()
    trips_with_routes = 0
    for trip, latlon in train_latlons.items():
        if trip_to_route.get(trip):
            trips_with_routes += 1
        elif "NonTimetabled" not in trip:
            raise AssertionError(trip, "not found")
    assert trips_with_routes == 124


def test_filtered_latlons():
    filtered_latlons = trains.get_filtered_latlons(
        "IWL_1", trains.get_feed_messages(True))
    assert len(filtered_latlons) == 7
    filtered_latlons = trains.get_filtered_latlons(
        "BMT_1", trains.get_feed_messages(True))
    assert len(filtered_latlons) == 5
    filtered_latlons = trains.get_filtered_latlons(
        "IWL_1|BMT_1", trains.get_feed_messages(True))
    assert len(filtered_latlons) == 12


def test_filtered_triproutes():
    filtered_triproutes = trains.get_filtered_triproutes(
        "IWL_1", trains.get_feed_messages(True))
    assert len(filtered_triproutes) == 7
    filtered_triproutes = trains.get_filtered_triproutes(
        "BMT_1", trains.get_feed_messages(True))
    assert len(filtered_triproutes) == 5
    filtered_triproutes = trains.get_filtered_triproutes(
        "IWL_1|BMT_1", trains.get_feed_messages(True))
    assert len(filtered_triproutes) == 12


def test_anytrip_url():
    assert trains.get_anytrip_url(
        'W593.1449.112.2.V.8.60928616') == "https://anytrip.com.au/?selectedTrip=tripInstance%2F{}%2Fau2:st:W593%2F0".format(
        datetime.now().strftime("%Y%m%d"))
