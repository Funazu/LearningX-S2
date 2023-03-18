import requests

main_url = 'https://api.spacexdata.com/v4/launches'
launches_response = requests.get(main_url)
launches_json = launches_response.json()

access_token = 'pk.eyJ1IjoiZmF1enVubmFqYSIsImEiOiJjbGZidHRneXYwajBwM3ptZXZpdXlvM3RtIn0.fywEWWE2EmbwnottzzxeNQ'

launches_data = []

for launches in launches_json:
    launchpadid = launches['launchpad']
    date = launches['date_utc']

    data = {
        'launchpadid': launchpadid,
        'date': date
    }

    launches_data.append(data)


for launche in launches_data:
    launchpadid = launche['launchpadid']

    launchpad_url = f'https://api.spacexdata.com/v4/launchpads/{launchpadid}'
    launchpad_response = requests.get(launchpad_url)
    launchpad_json = launchpad_response.json()

    full_name = launchpad_json['full_name']
    lat1 = launchpad_json['latitude']
    lon1 = launchpad_json['longitude']

    mapbox_url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{full_name}.json?access_token={access_token}'
    mapbox_response = requests.get(mapbox_url)
    mapbox_json = mapbox_response.json()


    print(mapbox_json)
    # print(full_name, lat1, lon1)
    # print(launchpadid)