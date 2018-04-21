from ItineraryCreation.Node import Node
from hackust.ubertravel.models import TravelTime, Event

import numpy
from heapq import heappop, heappush

def getNodes(city):
    """

    :param city:string, is a string that defines for which city the itinerary is created
    :return: returns an array with all the events available in the city
    """
    events = Event.objects.get(city=city)
    nodes = list()
    for e in events:
        nodes.append(Node(name=e.name, parent=None, rating=e.rating, path=[], duration=e.duration))

    return numpy.array(nodes)


def nodes_to_events(path, city):
    """

    :param path: list of nodes that should be turned into events again
    :param city:string, is a string that defines for which city the itinerary is created
    :return: list of events
    """
    all_events = Event.objects.get(city=city)
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
                print(1/n.get_utility())
                try:
                    heappush(heap, n)
                except TypeError:
                    pass
            current_node = heappop(heap)

        path = current_node.path
        path.append(current_node)

        self.events = nodes_to_events(path)