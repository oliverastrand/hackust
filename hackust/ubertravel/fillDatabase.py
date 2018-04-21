from .models import Attraction, AttractionTag, Restaurant, TravelTime

from geopy.geocoders import Nominatim
import googlemaps
from .GoogleMapsAPI import get_dist_and_duration
import json


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
            dist_text, duration_text = get_dist_and_duration(geolocator, gmaps, addresses[i], addresses[j], True)
            dist_val, duration_val = get_dist_and_duration(geolocator, gmaps, addresses[i], addresses[j], False)
            newTravelTime = TravelTime(start_place=addresses[i], end_place=addresses[j],
                                       duration=duration_val, distance=dist_val)
            newTravelTime.save()  # Saves to database


# Adds all attractions from a json-file to the database
def addAttractions(attractionsJson):
    json_data = open(attractionsJson).read()
    attractions_data = json.loads(json_data)

    for key in attractions_data:
        name = attractions_data[key]["name"]
        city = attractions_data[key]["city"]
        address = attractions_data[key]["address"]
        rating = attractions_data[key]["rating"] * attractions_data[key]["reviews"]
        duration = attractions_data[key]["duration"]
        description = attractions_data[key]["description"]
        newAttraction = Attraction(name=name, city=city, address=address, rating=rating, duration=duration,
                                   description=description)
        newAttraction.save()

        '''
        # If we are adding attraction tags
        tag = attractions_data[key]["tag"]
        newAttraction.attractionTag_set.create(attractionTag=tag)
        '''

# Adds all restaurants from a json-file to the database
def addRestaurants(restaurantsJson):
    json_data = open(restaurantsJson).read()
    restaurants_data = json.loads(json_data)

    for key in restaurants_data:
        name = restaurants_data[key]["name"]
        city = restaurants_data[key]["city"]
        address = restaurants_data[key]["address"]
        rating = restaurants_data[key]["rating"] * restaurants_data[key]["reviews"]
        # description = restaurants_data[key]["description"]
        duration = restaurants_data[key]["duration"]
        price = restaurants_data[key]["price"]
        cuisine = restaurants_data[key]["cuisine"]
        newRestaurant = Restaurant(name=name, city=city, address=address, rating=rating,
                                   duration=duration, price=price, cuisine=cuisine)
        newRestaurant.save()
