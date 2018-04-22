# Generated by Django 2.0.4 on 2018-04-21 21:30

from django.shortcuts import get_object_or_404
from django.db import migrations
# from ubertravel.fillDatabase import addAttractions, addRestaurants, addTravelTimes, add_cities
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import googlemaps, json


def add_travel_times(city, Event, TravelTime, Attraction, Restaurant, City):
    # Retrieves all addresses of the attractions and restaurants
    addresses = []
    attractions = Attraction.objects.filter(city=City.objects.get(name=city))
    restaurants = Restaurant.objects.filter(city=City.objects.get(name=city))
    for attraction in attractions:
        addresses.append(((attraction.lat, attraction.long), attraction.address))
    for restaurant in restaurants:
        addresses.append(((restaurant.lat, restaurant.long), restaurant.address))

    # Fetches the travel time between all different addresses from Google Maps API
    # geolocator = Nominatim()
    # gmaps = googlemaps.Client(key='AIzaSyBKtJT8Le-Gh3FxX9Gc-21lEW4otPK-DYo')
    for i in range(0, len(addresses)):
        for j in range(i+1, len(addresses)):  # From i+1 to avoid fetching the same data multiple times
            # dist_text, duration_text = get_dist_and_duration((addresses[i][0], addresses[i][1]), (addresses[j][0], addresses[j][1]), True)
            dist_val, duration_val = get_dist_and_duration((addresses[i][0][0], addresses[i][0][1]),
                                                           (addresses[j][0][0], addresses[j][0][1]), False)

            newTravelTime, created = TravelTime.objects.get_or_create(start_name=addresses[i][1],
                                       end_name=addresses[j][1],
                                       duration=duration_val, distance=dist_val)
            newTravelTime.save()  # Saves to database


def get_dist_and_duration(start, end, get_text):
    """
    Get the distance and duration
    :param start: string of the start point (address) of journey -> presented as (lat, lon) pair
    :param end: string of the end point (address) of journey -> -> presented as (lat, lon) pair
    :param getText: boolean (true returns string values, false return int values)
    :return: tuple of distance, duration (string, string) or (int - distance in meters, int - time in seconds) pair
    """
    now = datetime.now()
    geolocator = Nominatim()
    gmaps = googlemaps.Client(key='AIzaSyBKtJT8Le-Gh3FxX9Gc-21lEW4otPK-DYo')
    # location_orig = geolocator.geocode(start)
    # location_dest = geolocator.geocode(end)
    '''
    if location_orig is None or location_dest is None:
        if get_text:
            return '1000000', '1000000000'
        else:
            return 1000000, 1000000000'''

    # string with start/end coordinates (x, y)
    # orig_coordinates_text = location_orig.raw['lat'] + ', ' + location_orig.raw['lon']
    # dest_coordinates_text = location_dest.raw['lat'] + ', ' + location_dest.raw['lon']
    orig_coordinates_text = start[0] + ', ' + start[1]
    dest_coordinates_text = end[0] + ', ' + end[1]
    print(orig_coordinates_text)
    print(dest_coordinates_text)

    # call google maps mpi
    directions_result = gmaps.directions(orig_coordinates_text,
                                         dest_coordinates_text,
                                         mode="driving",
                                         avoid="ferries",
                                         departure_time=now
                                        )

    # type -> datetime.timedelta
    # duration_val = timedelta(seconds=directions_result[0]['legs'][0]['duration']['value'])
    #if directions_result:
    duration_val = directions_result[0]['legs'][0]['duration']['value']
    duration_text = directions_result[0]['legs'][0]['duration']['text']
    dist_val = directions_result[0]['legs'][0]['distance']['value']
    dist_text = directions_result[0]['legs'][0]['distance']['text']

    if get_text:
        return dist_text, duration_text
    else:
        return dist_val, duration_val


# Adds all attractions from a json-file to the database
def add_attractions(attractions_json, Attraction, City):
    with open(attractions_json, 'r') as dictionary:
        attractions_data = json.load(dictionary)

    for key in attractions_data:
        name = attractions_data[key]["name"]
        city = City.objects.get(name=attractions_data[key]["city"])
        address = attractions_data[key]["address"]
        lat = attractions_data[key]["lat"]
        lon = attractions_data[key]["lon"]
        rating = attractions_data[key]["rating"] * attractions_data[key]["reviews"]
        duration = attractions_data[key]["duration"]
        description = attractions_data[key]["description"]
        newAttraction, created = Attraction.objects.get_or_create(name=name, city=city, address=address, rating=rating,
                                                                  duration=duration, lat=lat, long=lon, description=description)
        newAttraction.save()

        '''
        # If we are adding attraction tags
        tag = attractions_data[key]["tag"]
        newAttraction.attractionTag_set.create(attractionTag=tag)
        '''


def add_cities(city_json, City):
    with open(city_json, 'r') as dictionary:
        city_data = json.load(dictionary)

    city, created = City.objects.get_or_create(name=city_data['1']["city"])
    city.save()


# Adds all restaurants from a json-file to the database
def add_restaurants(restaurantsJson, Restaurant, City):
    with open(restaurantsJson, 'r') as dictionary:
        restaurants_data = json.load(dictionary)
    # json_data = open(restaurantsJson).read()
    # restaurants_data = json.loads(json_data)

    for key in restaurants_data:
        name = restaurants_data[key]["name"]
        city = City.objects.get(name=restaurants_data[key]["city"])
        address = restaurants_data[key]["address"]
        lat = restaurants_data[key]["lat"]
        # print(lat)
        lon = restaurants_data[key]["lon"]
        # print(lon)
        rating = restaurants_data[key]["rating"] * restaurants_data[key]["reviews"]
        # description = restaurants_data[key]["description"]
        duration = restaurants_data[key]["duration"]
        price = restaurants_data[key]["price"]
        cuisine = restaurants_data[key]["cuisine"]
        newRestaurant, created = Restaurant.objects.get_or_create(name=name, city=city, address=address, rating=rating,
                                   lat=lat, long=lon, duration=duration, price=price, cuisine=cuisine)
        newRestaurant.save()


def some_func(apps, schema_editor):
    City = apps.get_model('ubertravel', 'City')
    Event = apps.get_model('ubertravel', 'Event')
    Restaurant = apps.get_model('ubertravel', 'Restaurant')
    Attraction = apps.get_model('ubertravel', 'Attraction')
    TravelTime = apps.get_model('ubertravel', 'TravelTime')

    add_cities("../CityData/Hong Kong_attractions.json", City)
    add_restaurants("../CityData/Hong Kong_restaurants.json", Restaurant, City)
    add_attractions("../CityData/Hong Kong_attractions.json", Attraction, City)
    add_travel_times("Hong Kong", Event, TravelTime, Attraction, Restaurant,City)


class Migration(migrations.Migration):

    dependencies = [
        ('ubertravel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(some_func)
    ]
