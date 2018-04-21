from django.db import models

# Attractions to visit
class Attraction(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name

# Types of attractions that are valid
class AttractionTag(models.Model):
    attraction_tag = models.CharField(max_length=200)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)

    def __str__(self):
        return self.attraction + ": " + self.attraction_tag

# Restaurants
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    description = models.CharField(max_length=500)
    cuisine = models.CharField(max_length=200)  # E.g. western or local

    def __str__(self):
        return self.name

# Travel times between different addresses
class TravelTime(models.Model):
    start_address = models.CharField(max_length=200)
    end_address = models.CharField(max_length=200)
    duration = models.TimeField()
    distance = models.IntegerField()

    def __str__(self):
        return self.start_address + " - " + self.end_address + ": " + self.duration

class TravelTimeValues(models.Model):
    start_address = models.CharField(max_length=200)
    end_address = models.CharField(max_length=200)
    #duration is in Seconds
    duration = models.IntegerField()
    #distance is in Meters
    distance = models.IntegerField()

    def __str__(self):
        return self.start_address + " - " + self.end_address + ": " + self.duration