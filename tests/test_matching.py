from whereis import trains, matching
from datetime import datetime


def test_match():
    person = {"lat": -33.86697, "lon": 151.08611} # homebush station
    trains_nearby = trains.get_filtered_latlons(
        "IWL_1|BMT_1", trains.get_feed_messages(True))
    nearest_trains = matching.get_nearest_trains_to_person(trains_nearby,person)
    assert next(iter(nearest_trains)) < 0.01
    assert next(iter(nearest_trains.values())) == '8--W.1449.112.2.B.8.60929769'