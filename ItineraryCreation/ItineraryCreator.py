from ItineraryCreation.Node import Node
import numpy
from heapq import heappop, heappush


def getNodes():
    node1 = Node(name = '1', parent=None, utility=1, location=1, path = [])
    node2 = Node(name = '2', parent=None, utility=2, location=2, path = [])
    node3 = Node(name = '3', parent=None, utility=3, location=3, path = [])
    node4 = Node(name = '4', parent=None, utility=4, location=4, path = [])
    node5 = Node(name = '5', parent=None, utility=5, location=5, path = [])
    node6 = Node(name = '6', parent=None, utility=6, location=6, path = [])



    return numpy.array([node1, node2, node3, node4, node5, node6])

class ItineraryCreator:
    def __init__(self):
        #:params
        heap = []

        nodes = getNodes()

        initialNode = nodes[5]

        current_node = initialNode
        final_node = nodes[0]
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
