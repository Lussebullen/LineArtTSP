# Stich together halftoning and graphsolving here and plot it
#from curses.ascii import isalnum
#from sympy import ordered
from graph import Graph
import halftoning
import numpy as np
from matplotlib import pyplot as plt

# Generate test data points
n=50
size = 1000
X = np.random.randint(0,size,n)
Y = np.random.randint(0,size,n)
nodes = list(zip(X,Y))

# Create graph object solve TSP
G = Graph(nodes)
G.createDistMatrix()
G.TSP(timelimit=10)
tspsol = G.nodes

# Plot points and approximate optimal path
G.plot()