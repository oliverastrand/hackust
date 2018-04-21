import numpy
import functools

@functools.total_ordering
class Node:
    def __init__(self, name, parent, location, utility, path):
        """
        :param name:string is the name of the attraction,
        is also the reference to the information pages
        :param parent:node is None if self is a root node or a node, if the node has a parent
        :param location:string is a string indicating the adress to lookup the distance in Google Maps
        :param utility:value, defines the utility of the attraction
        :param path:list<node>, contains a list with the nodes that go from the start location via other locations to the end

        """
        self.name = name
        self.parent = parent
        self.location = location
        self.utility = utility
        self.path = path

    def get_utility(self):
        if self.parent is not None:
            return self.utility + self.parent.utility
        else: return self.utility

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
                newNode = node.cpy()
                newNode.parent = self
                newPath = list(self.path)
                newPath.append(self)
                newNode.path = newPath
                if numpy.positive(newNode.get_distance_from_parent())<=2:
                    children.append(newNode)
        self.children = numpy.array(children)
        return self.children

    def cpy(self):
        return Node(self.name, self.parent, self.location, self.utility,self.path)

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