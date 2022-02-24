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
tspsol = G.TSP(timelimit=20)

# Plot points and approximate optimal path
fig, ax = plt.subplots(1,1)
ax.plot(X,Y,"b,")
ax.plot(tspsol[:,0],tspsol[:,1])
plt.show()

print()