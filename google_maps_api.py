import googlemaps
from datetime import datetime, timedelta
from geopy import geocoders

from geopy.geocoders import Nominatim
geolocator = Nominatim()

gmaps = googlemaps.Client(key='AIzaSyBKtJT8Le-Gh3FxX9Gc-21lEW4otPK-DYo')


def get_dist_and_duration(start, end):
    """
    Get the distance and duration
    :param start: string of the start point (address) of journey
    :param end: string of the end point (address) of journey
    :return: tuple of distance, duration string pair
    """
    now = datetime.now()
    # origins = []
    # destinations = []
    orig_text = '25 lower kent ridge road'
    dest_text = 'Changi airport'
    location_orig = geolocator.geocode(orig_text)
    location_dest = geolocator.geocode(dest_text)

    # string with start/end coordinates (x, y)
    orig_coordinates_text = location_orig.raw['lat'] + ', ' + location_orig.raw['lon']
    dest_coordinates_text = location_dest.raw['lat'] + ', ' + location_dest.raw['lon']

    # call google maps mpi
    directions_result = gmaps.directions(orig_coordinates_text,
                                         dest_coordinates_text,
                                         mode="driving",
                                         avoid="ferries",
                                         departure_time=now
                                        )

    # type -> datetime.timedelta
    duration_val = timedelta(seconds=directions_result[0]['legs'][0]['duration']['value'])
    duration_text = directions_result[0]['legs'][0]['duration']['text']
    dist_val = directions_result[0]['legs'][0]['distance']['value'] / 1000.0
    dist_text = directions_result[0]['legs'][0]['distance']['text']

    return dist_text, duration_text

    # print(duration_val)
    # print(duration_text)
    # print(dist_val)
    # print(dist_text)
