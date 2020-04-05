from locationsharinglib import Service
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)


def get_people_latlons():
    service = Service(cookies_file='cookies.txt',
                      authenticating_account=os.getenv('GOOGLE_ACCOUNT_EMAIL'))
    people = {}
    for person in service.get_all_people():
        people[person.nickname] = {
            'latitude': person.latitude, 'longitude': person.longitude}
        print(person.nickname, person.latitude, person.longitude)
    return people

if __name__ == "__main__":
  get_feed_messages()
