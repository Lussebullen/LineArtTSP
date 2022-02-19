# Stich together halftoning and graphsolving here and plot it
from curses.ascii import isalnum
from graph import Graph
import halftoning
import numpy as np

# Just for testing atm:
X = np.random.randint(0,10,10)
Y = np.random.randint(0,10,10)
nodes = list(zip(X,Y))

#G = Graph(nodes)
#print(G.distM)
print(isalnum(2,float))