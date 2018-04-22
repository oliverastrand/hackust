from ItineraryCreation.Node import Node, duration_sum
from hackust.ubertravel.models import TravelTime, Event, Restaurant

import numpy
from heapq import heappop, heappush

def getNodes(city):
    """

    :param city:string, is a string that defines for which city the itinerary is created
    :return: returns an array with all the events available in the city
    """
    nodes = list()
    events = Event.objects.filter(city=city)
    
    
    for e in events:
        nodes.append(Node(name=e.name, parent=None, rating=e.rating, path=[], duration=e.duration))
    
    restaurants = Restaurant.objects.filter(city="Hong Kong")
    for n in nodes:
        for r in restaurants:
            if n.name == r.name:
                n.is_restaurant=True

    """nodes.append(Node(name="Start", parent=None, rating=0, path=[], duration=0, adress="Start"))
    nodes.append(Node(name="Peak", parent=None, rating=10000, path=[], duration=120, adress="Peak"))
    nodes.append(Node(name="Skyline", parent=None, rating=5000, path=[], duration=30, adress="Skyline"))
    nodes.append(Node(name="Buddha", parent=None, rating=7500, path=[], duration=240, adress="Buddha"))
    nodes.append(Node(name="Monestary", parent=None, rating=7500, path=[], duration=60, adress="Monestary"))
    nodes.append(Node(name="Italian Pizza Place", parent=None, rating=8000, path=[], duration=80, adress="Italian Pizza Place"))
    nodes.append(Node(name="End", parent=None, rating=0, path=[], duration=0, adress="End"))
    nodes[len(nodes)-1].is_restaurant=True
"""
    return numpy.array(nodes)


def nodes_to_events(path, city):
    """

    :param path: list of nodes that should be turned into events again
    :param city:string, is a string that defines for which city the itinerary is created
    :return: list of events
    """
    all_events = Event.objects.filter(city=city)
    events = list()
    for p in path:
        for e in all_events:
            if e.name == p.name:
                events.add(e)

    return e


class ItineraryCreator:
    def __init__(self, city):
        """
        :param city: the name of the city we plan the itinerary for
        """
        heap = []

        nodes = getNodes(city)

        for i in range(0, len(nodes)):
            if nodes[i].name == "Start":
                initial_node = nodes[i]
            if nodes[i].name=="End":
                final_node = nodes[i]


        current_node = initial_node

        while current_node.name != final_node.name:
            newNodes = current_node.explore_next_level(nodes_available=nodes)
            for n in newNodes:

                try:
                    heappush(heap, n)
                except TypeError:
                    pass
            current_node = heappop(heap)

        path = current_node.path
        path.append(current_node)

        self.times_leaving= list()

        for p in path:
            self.times_leaving.append(self.times_leaving[len(self.imes_leaving)-1]+p.duration+p.duration_to_get_there)

        self.events = nodes_to_events(path)