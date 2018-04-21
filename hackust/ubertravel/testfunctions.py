from .models import Event

def get_itinerary(city, excluded_attractions, mandatory_attractions):
    return [event for event in Event.objects.all() if event not in excluded_attractions], []
