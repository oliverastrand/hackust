from .models import Event

def get_itinerary(city, excluded_attractions, mandatory_attractions):
    events = [event for event in Event.objects.all() if event not in excluded_attractions]
    n = len(events)
    return events, [i for i in range(n)]
