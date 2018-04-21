from django.db import models


class City(models.Model):
    name = models.TextField(max_length=200, unique=True)
    description = models.TextField(max_length=20000, null=True)


# Superclass for attractions and restaurants
class Event(models.Model):
    name = models.CharField(max_length=200, unique=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, unique=True)
    rating = models.IntegerField(default=0)
    description = models.CharField(max_length=2000)

    duration = models.IntegerField()


# Attractions to visit
class Attraction(Event):

    def __str__(self):
        return self.name


# Types of attractions that are valid
class AttractionTag(models.Model):
    attraction_tag = models.CharField(max_length=200)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    def __str__(self):
        return self.attraction + ": " + self.attraction_tag


# Restaurants
class Restaurant(Event):
    price = models.IntegerField(default=20)
    cuisine = models.CharField(max_length=200)  # E.g. western or local

    def __str__(self):
        return self.name


# Travel times between different addresses
class TravelTime(models.Model):
    start_place = models.ForeignKey('Event', related_name='start_place', on_delete=models.CASCADE)
    end_place = models.ForeignKey('Event', on_delete=models.CASCADE)

    duration = models.IntegerField()
    distance = models.IntegerField()

    def __str__(self):
        return self.start_place + " - " + self.end_place + ": " + self.duration

