import numpy
import functools
from hackust.ubertravel.models import TravelTime
from django.core.exceptions import ObjectDoesNotExist

def duration_sum(newPath):
    """

    :param newPath: list of the visited nodes
    :return: number of minutes as the sum of the durations
    """
    sum = 0
    for p in newPath:
        sum += p.duration + p.duration_to_get_there
    return sum

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

@functools.total_ordering
class Node:
    def __init__(self, name, parent, rating, path, duration, adress):
        """
        :param name:string is the name of the attraction,
        is also the reference to the information pages
        :param parent:node is None if self is a root node or a node, if the node has a parent
        :param location:string is a string indicating the adress to lookup the distance in Google Maps
        :param rating:value, defines the utility of the attraction
        :param path:list<node>, contains a list with the nodes that go from the start location via other locations to the end
        :param duration:int the number of minutes it takes us to go through the attraction
        :param duration_to_get_there: int number of minutes to get to the event
        """
        self.name = name
        self.parent = parent
        self.rating = rating
        self.path = path
        self.start_time = 540 #minutes == 9 o clock
        self.finish_time = 1080 #minutes == 18 o clock
        self.duration = duration
        self.duration_to_get_there = 0
        self.no_restaurant_yet = True
        self.is_restaurant = False
        self.adress = adress


    def get_utility(self):
        if self.parent is not None:
            return self.rating + self.parent.get_utility() - duration_sum(self.path)
        else: return self.rating

    def get_distance_from_parent(self):
        return numpy.sqrt(numpy.power(self.location-self.parent.location, 2))

    def explore_next_level(self, nodes_available):
        children = list()
        for node in nodes_available:
            is_in_path = False
            for p in self.path:
                if p.name == node.name:
                    is_in_path=True
            if node.name != self.name and not is_in_path:
                #copy the node information
                newNode = node.cpy()
                #set the current node as the parent of the new one
                newNode.parent = self
                #append the current node as part of the path
                #necessity to deep copy
                newPath = list(self.path)
                newPath.append(self)
                newNode.path = newPath

                #tell how long it will take to go there
                try:
                    travel_time = TravelTime.objects.get(start_place = self.adress, end_place = newNode.adress)
                except ObjectDoesNotExist:
                    travel_time = TravelTime.objects.get(start_place = newNode.adress, end_place=self.adress)

                #travel_time = levenshtein(self.name, newNode.name)
                newNode.duration_to_get_there = travel_time
                #add previous restaurant information
                newNode.no_restaurant_yet = self.no_restaurant_yet

                #hard constraints
                c = duration_sum(newPath) + self.start_time
                d = newNode.duration + newNode.duration_to_get_there
                a = self.no_restaurant_yet
                R = newNode.is_restaurant
                if ((not R) or (c > 60 * 12 and c < 60 * 14 and not a)) and (R or (c + d < 60 * 14 or (c + d > 60 * 14 and a))) and c + d < self.finish_time:
                    if R:
                        newNode.no_restaurant_yet = False
                    children.append(newNode)



        self.children = numpy.array(children)
        return self.children

    def cpy(self):
        return Node(self.name, self.parent, self.rating, self.path, self.duration, self.adress)

    def _is_valid_operand(self, other):
        return (hasattr(other, "get_utility") and
                hasattr(other, "name"))

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.get_utility()==other.get_utility and self.name==self.name

    #Here every operator is resverse as we are using a min heap map.
    #Therefore, a node is selected first if the utility is lowest. By inverting the functions we can bypass that
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        if self.get_utility()>other.get_utility():
            return True
        elif self.get_utility()<other.get_utility():
            return False
        elif self.name>other.name:
            return True
        else: return False