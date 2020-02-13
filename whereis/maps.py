from locationsharinglib import Service
google_email = 'maxious@gmail.com'
service = Service(cookies_file='cookies.txt', authenticating_account=google_email)
for person in service.get_all_people():
    print(person.nickname,person.latitude,person.longitude)
