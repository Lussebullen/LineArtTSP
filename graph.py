# Create Graph class here, with appropriate built in methods
# OR-Tools https://developers.google.com/optimization/install/python/windows
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
from scipy import interpolate

class Graph:
    def __init__(self, nodes) -> None:
        """Initializes Graph object with its nodes converted
        to a distance matrix.

        Args:
            nodes (list of 2-tuples of integers or floats): List of coordinates

        Raises:
            TypeError: Raise error if nodes is not a numpy array
            TypeError: Raise error if array does not have 2 columns
        """

        # Error handling
        if not isinstance(nodes,np.ndarray):
            raise TypeError("Nodes must be a numpy array")
        if nodes.shape[1] != 2:
            raise TypeError("Array must have 2 columns")
        
        self.nodes = nodes
        self.distM = None

    def createDistMatrix(self):
        """
        Creates a distance matrix from the nodes in a graph.

        Args:
            nodes (list of 2-tuples of integers or floats): List of coordinates.

        Returns:
            array of floats: n x n array of mutual distances between coordinates.
        """
        n = len(self.nodes)
        dist = np.zeros((n,n))
        for i in tqdm(range(n)):  #Progress bar for the outer loop
            for j in range(i+1):
                P1, P2 = self.nodes[i], self.nodes[j]
                d = np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)
                dist[i][j], dist[j][i] = d, d
        print("Distance Matrix Completed")
        self.distM = dist


    def TSP(self, scalingfactor = 100, timelimit=30):
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
            return int(data['distance_matrix'][from_node][to_node]*scalingfactor)

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        #Set cost function
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        print("TSP solver framework constructed. Setting solver parameters")

        # Set search parameters and heuristic
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        # Heuristic 1
        #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Heuristic 2
        search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = timelimit  # Sets alotted time limit
        search_parameters.log_search = True # Prints log information during solving.

        print("Solving...")
        # Solve
        solution = routing.SolveWithParameters(search_parameters)

        print("Solver finished")
        # Get the approximated optimal order of nodes for the shortest path as a list of indexes
        index = routing.Start(0)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))

        # re-order self.nodes to be order of (approximately) optimal path
        self.nodes = self.nodes[route]
        self.distM = None   # Distance matrix no longer valid

    def plot(self, style="line"):
        """Plots the nodes of the graph in the given style.

        Args:
            style (str, optional): Plots line graph, spline graph or point graph. Defaults to "line".
        """
        fig, ax = plt.subplots(1,1)
        if style=="line":
            ax.plot(self.nodes[:,0], self.nodes[:,1])
        elif style=="spline":
            X = self.nodes[:,0]
            Y = self.nodes[:,1]
            #create spline function
            f, _ = interpolate.splprep([X, Y], s=0, per=True)
            #Create interpolated list of points and plot
            xint, yint = interpolate.splev(np.linspace(0, 1, len(self.nodes)*20), f)
            ax.plot(xint, yint)
        else:
            ax.plot(self.nodes[:,0], self.nodes[:,1],"b.")
        plt.show()