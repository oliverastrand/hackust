from django import forms
from .models import Event

class CityForm(forms.Form):

    city = forms.CharField(label="City", max_length=50, required=True)


def itinerary_form_generator(events):

    class ItineraryForm(forms.Form):






