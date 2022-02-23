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
            TypeError: Raise error if coordinates inside list are not int or floats
        """

        # Error handling
        if not isinstance(nodes,list):
            raise TypeError("Nodes must be a list")
        if not all([isinstance(i,tuple) and len(i)==2 for i in nodes]):
            raise TypeError("All node entries must be 2-tuples")
        typewhitelist = (int, float,np.int32,np.float64)
        if not all([isinstance(i[0],typewhitelist) and isinstance(i[1],typewhitelist) for i in nodes]):
            raise TypeError("All coordinates must be int / floats")
        # FIXME: Add error handling, all coordinates must be int / floats
        
        self.nodes = nodes
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
        #From OR tools documentation:

        # Structure needed for package TSP solver.
        # depot -> starting node
        # num_vehicles -> number of "salesmen"
        data = {"distance_matrix":self.distM,"num_vehicles":1,"depot":0}
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),data['num_vehicles'], data['depot'])
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the scaled integer distance between the two nodes.

            Args:
                from_index (int): index of start node
                to_index (int): index of end node
                scalingfactor (float): factor with which to scale distances
                manager (RoutingIndexManager): Manager object from pywrapcp
            """
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]*scalingfactor

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        #Set cost function
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Set search parameters and heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        
        # Solve
        solution = routing.SolveWithParameters(search_parameters)

        # Get the approximated optimal order of nodes for the shortest path as a list of indexes
        index = routing.Start(0)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))

        # Return reordered array of nodes.
        nodarray = np.array(self.nodes)
        return nodarray[route]
    