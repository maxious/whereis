import math
from collections import OrderedDict

def _get_distance(latA,lonA,latB,lonB):
    return math.hypot(lonA - lonB, latA - latB)

def get_nearest_trains_to_person(trains, person):
    ranked_trains = {}
    for trip_id, (lat,lon) in trains.items():
        ranked_trains[_get_distance(lat,lon,person["lat"],person["lon"])] = trip_id
    ranked_trains = OrderedDict(sorted(ranked_trains.items()))
    return ranked_trains

# if __name__ == "__main__":
#     print(get_nearest_trains_to_person)