from whereis import trains
def test_feed_messages():
    feed_messages = trains.get_feed_messages(True)
    assert feed_messages != None
def test_train_latlons():
    train_latlons = trains.get_train_latlons(trains.get_feed_messages(True))
    assert len(train_latlons) == 191

def test_filtered_latlons():
    filtered_latlons = trains.get_filtered_latlons("IWL_1", trains.get_feed_messages(True))
    assert len(filtered_latlons) == 0

def test_anytrip_url():
    assert trains.get_anytrip_url('abc123') == "https://anytrip.com.au/?selectedTrip=tripInstance%2FYMD%2Fau2:st:abc123%2F0"