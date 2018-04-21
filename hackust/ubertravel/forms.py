from django import forms
from .models import Event

class CityForm(forms.Form):
    city = forms.CharField(label="city", max_length=50, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'City to explore...'}))

def itinerary_form_generator(events):
    EVENT_CHOICES = (
        (1, ("Neutral")),
        (2, ("Like")),
        (3, ("Dislike")),
    )

    class ItineraryForm(forms.Form):
        def __init__(self):
            super(ItineraryForm, self).__init__()
            for event in events:
                self.fields[event.name] = forms.ChoiceField(choices=EVENT_CHOICES, label=event.name, initial='')


    return ItineraryForm


class ItineraryForm(forms.Form):
    EVENT_CHOICES = (
        ("Neutral", ("Neutral")),
        ("Like", ("Like")),
        ("Dislike", ("Dislike")),
    )

    def __init__(self, *args, **kwargs):
        events = kwargs.pop('events')
        super(ItineraryForm, self).__init__(*args, **kwargs)
        for event in events:
            self.fields[event.name] = forms.ChoiceField(choices=self.EVENT_CHOICES, label=event.name, initial='')
