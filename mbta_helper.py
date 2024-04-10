import json
import pprint
import urllib.request
from config import MAPBOX_TOKEN, MBTA_API_KEY

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as f:
        response_text = f.read().decode('utf-8')
        response_data = json.loads(response_text)
        return response_data


def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    place_name = place_name.replace(' ', '%20') # In URL encoding, spaces are typically replaced with "%20". You can also use urllib.parse.quote function. 
    url=f'{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}&types=poi'
    response_data = get_json(url)
    # pprint.pprint(response_data)
    longitude = response_data['features'][0]['center'][0]
    latitude = response_data['features'][0]['center'][1]

    return latitude, longitude


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """    
    url = f'{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}'
    response_data = get_json(url)
    pprint.pprint(response_data["data"][0]["attributes"]["name"])

    # print(len(response_data['data']))
    station_name = response_data['data'][0]['attributes']['name']
    wheelchair_accessible = response_data['data'][0]['attributes']['wheelchair_boarding']
    return station_name, wheelchair_accessible



def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    This function might use all the functions above.
    """
    lat, long = get_lat_lng(place_name)
    print(lat, long)
    return get_nearest_station(lat, long)


def main():
    """
    You should test all the above functions here
    """
    # Test get_lat_lng()
    print(get_lat_lng("Fenway Park, Boston"))

    # Test get_nearest_station()
    print(get_nearest_station("42.3463355", "-71.0975175"))

    # Test find_stop_near()
    print(find_stop_near("Fenway Park, Boston"))
    
if __name__ == '__main__':
    main()
