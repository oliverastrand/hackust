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
    cuisine = models.CharField(max_length=200)  # Western or local

    def __str__(self):
        return self.name

# Travel times between different addresses
class TravelTime(models.Model):
    start_address = models.CharField(max_length=200)
    end_address = models.CharField(max_length=200)
    duration = models.TimeField()
    length = models.IntegerField()

    def __str__(self):
        return self.start_address + " - " + self.end_address + ": " + self.duration

'''

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text
'''