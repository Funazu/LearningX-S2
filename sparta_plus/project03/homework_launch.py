from math import radians, cos, sin, asin, sqrt
import requests

main_url = 'https://api.spacexdata.com/v4/launches'
launches_response = requests.get(main_url)
launches_json = launches_response.json()

access_token = 'pk.eyJ1IjoiZmF1enVubmFqYSIsImEiOiJjbGZidHRneXYwajBwM3ptZXZpdXlvM3RtIn0.fywEWWE2EmbwnottzzxeNQ'

launches_data = []

for i in range(len(launches_json) - 1, len(launches_json) - 21, -1):
    launchpadid = launches_json[i]['launchpad']
    date = launches_json[i]['date_utc']

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

    coordinate = mapbox_json['features'][0]['geometry']['coordinates']
    lat2 = coordinate[0]
    lon2 = coordinate[1]    
    

    # Kalkulasi Masseh
    def distance(lat1, lat2, lon1, lon2):
        # Modul matematika bermuat fungsi bernama
        # radian yang mengonversi dari derajat ke radian.
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        
        # formula Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
        c = 2 * asin(sqrt(a))
        
        # Radius bumi dalam kilometer. Gunakan 3956 untuk mil
        r = 6371
        
        # kalkulasikan hasil
        return(c * r)

        
    # HASILL AHAHAHA
    date = launche['date']
    print(date, full_name, distance(lat1, lat2, lon1, lon2))  