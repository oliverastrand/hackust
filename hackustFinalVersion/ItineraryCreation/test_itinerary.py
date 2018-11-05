
from hackustFinalVersion.ubertravel.fillDatabase import addAttractions
from hackustFinalVersion.ubertravel.fillDatabase import addRestaurants
from hackustFinalVersion.ubertravel.fillDatabase import addTravelTimes


def test_load():

    addRestaurants("/../DestinationCityData/Hong Kong_attractions.json")
    addAttractions("/../DestinationCityData/Hong Kong_restaurants.json")
    addTravelTimes("Hong Kong")
