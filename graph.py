# Create Graph class here, with appropriate built in methods
# OR-Tools https://developers.google.com/optimization/install/python/windows
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np

class Graph:
    def __init__(self, nodes) -> None:
        """Initializes Graph object with its nodes converted
        to a distance matrix.

        Args:
            nodes (list of 2-tuples of integers or floats): List of coordinates

        Raises:
            TypeError: Raise error if nodes is not a list
            TypeError: Raise error if list contains anything but tuples
        """

        # Error handling
        if not isinstance(nodes,list):
            raise TypeError("Nodes must be a list")
        if not all([isinstance(i,tuple) and len(i)==2 for i in nodes]):
            raise TypeError("All node entries must be 2-tuples")
        # FIXME: Add error handling, all coordinates must be int / floats
        
        self.distM = self.createDistMatrix(nodes)

    def createDistMatrix(self, nodes):
        """
        Creates a distance matrix from the nodes in a graph.

        Args:
            nodes (list of 2-tuples of integers or floats): List of coordinates.

        Returns:
            array of floats: n x n array of mutual distances between coordinates.
        """
        n = len(nodes)
        dist = np.zeros((n,n))
        for i in range(n):
            for j in range(i+1):
                P1, P2 = nodes[i], nodes[j]
                d = np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)
                dist[i][j], dist[j][i] = d, d
        return dist
    
    def TSP(self, scalingfactor = 100):
        #Solve TSP here and return graph object with adjacencylist containing the edges
        #approximated Hamiltonian cycle.
        pass