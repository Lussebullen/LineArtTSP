# Stich together halftoning and graphsolving here and plot it
#from curses.ascii import isalnum
from sympy import ordered
from graph import Graph
import halftoning
import numpy as np
from matplotlib import pyplot as plt

# Just for testing atm:
X = np.random.randint(0,100,100)
Y = np.random.randint(0,100,100)
nodes = list(zip(X,Y))

G = Graph(nodes)
fig, ax = plt.subplots(1,1)
ax.plot(X,Y,"b.")

tspsol = G.TSP()
print(tspsol)

ax.plot(tspsol[:,0],tspsol[:,1])
plt.show()