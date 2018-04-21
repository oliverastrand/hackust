from .models import Attraction, AttractionTag, Restaurant, TravelTime
from geopy.geocoders import Nominatim
import googlemaps
from GoogleMapsAPI import get_dist_and_duration

# Adds travel times between all addresses that currently are in the database for a specific city
def addTravelTimes(city):

    # Retrieves all addresses of the attractions and restaurants
    addresses = []
    attractions = Attraction.objects.filter(city=city)
    restaurants = Restaurant.objects.filter(city=city)
    for attraction in attractions:
        addresses.append(attraction.address)
    for restaurant in restaurants:
        addresses.append(restaurant.address)

    # Fetches the travel time between all different addresses from Google Maps API
    geolocator = Nominatim()
    gmaps = googlemaps.Client(key='AIzaSyBKtJT8Le-Gh3FxX9Gc-21lEW4otPK-DYo')
    for i in range(0, len(addresses)):
        for j in range(i+1, len(addresses)):  # From i+1 to avoid fetching the same data multiple times
            dist_text, duration_text = get_dist_and_duration(geolocator, gmaps, addresses[i], addresses[j])
            newTravelTime = TravelTime(start_address=addresses[i], end_address=addresses[j],
                                       duration=duration_text, distance=dist_text)
            newTravelTime.save()  # Saves to database

# Adds all attractions from a json-file to the database
#def addAttractions():
#