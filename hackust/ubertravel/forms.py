from django import forms
from .models import Event, Attraction, Restaurant

class CityForm(forms.Form):
    city = forms.CharField(label="", max_length=50, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'City to explore...'}))

class ItineraryForm(forms.Form):
    EVENT_CHOICES = (
        ("Neutral", ("Neutral")),
        ("Like", ("Like")),
        ("Dislike", ("Dislike")),
    )

    def __init__(self, *args, **kwargs):
        events = kwargs.pop('events')
        times = kwargs.pop("times")
        super(ItineraryForm, self).__init__(*args, **kwargs)
        '''
        for i in range(0, len(events)):
            event = events[i]
            if isinstance(event, Attraction):
                self.fields[event.name] = forms.ChoiceField(choices=self.EVENT_CHOICES, label=event.name, initial='',
                                                        attrs={"name": event.name, "description": event.description,
                                                               "time": times[i]})
            elif event is Restaurant:
                self.fields[event.name] = forms.ChoiceField(choices=self.EVENT_CHOICES, label=event.name, initial='',
                                                            attrs={"name": event.name, "price": event.price,
                                                                   "time": times[i], "rating": event.rating})
            else:
                print("Här")
                self.fields[event.name] = forms.ChoiceField(choices=self.EVENT_CHOICES, label=event.name, initial='',
                                                            attrs={"name": event.name, "description": event.description,
                                                                   "time": times[i]})
        '''