# Stich together halftoning and graphsolving here and plot it
#from curses.ascii import isalnum
#from sympy import ordered
from graph import Graph
import halftoning
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

# Generate test data points
n=50
size = 1000
X = np.random.randint(0,size,n)
Y = np.random.randint(0,size,n)
nodes = np.array(list(zip(X,Y)))

# Create graph object solve TSP
G = Graph(nodes)
G.createDistMatrix()
G.TSP(timelimit=3)


# Plot points and approximate optimal path
G.plot(style="spline")