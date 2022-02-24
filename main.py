# Stich together halftoning and graphsolving here and plot it
#from curses.ascii import isalnum
#from sympy import ordered
from graph import Graph
from halftoning import rejectionSampling
import numpy as np
from PIL import Image

# Generate test data points
n=1000
size = 1000

# Load Image, resize and convert to grayscale matrix with elements in [0,1], 0=black, 1=white.
img = Image.open('recurrentTheme.jpg').convert('L')   # FIXME: remove later, load image in main.
img = img.rotate(180)
M_pixels = np.array(list(img.getdata())).reshape((img.size[1], img.size[0]))/255

nodes = rejectionSampling(n,M_pixels)

#X = np.random.randint(0,size,n)
#Y = np.random.randint(0,size,n)
#nodes = np.array(list(zip(X,Y)))

# Create graph object solve TSP
G = Graph()
G.setNodes(nodes)
G.setDistMatrix()
G.TSP(timelimit=20)

# Plot points and approximate optimal path
G.plot(style="line")