# Stich together halftoning and graphsolving here and plot it
#from curses.ascii import isalnum
#from sympy import ordered
from graph import Graph
from halftoning import rejectionSampling
import numpy as np
from PIL import Image

# Generate test data points
n=100
size = 1000
# Load Image, resize and convert to grayscale matrix with elements in [0,1], 0=black, 1=white.
img = Image.open('C:\\Users\\Antoine Neveu\\Desktop\\TSPProject\\LineArtTSP\\SFJxCXKMZihnZsVnn3LoEk-1200-80.jpg')   # FIXME: remove later, load image in main.
img = img.rotate(180)
###I(Toine) moved conversion to grayscale, array creation into halftoning in order to allow me to add contrast method 
nodes = rejectionSampling(n, img, "contrast")

#X = np.random.randint(0,size,n)
#Y = np.random.randint(0,size,n)
#nodes = np.array(list(zip(X,Y)))

# Create graph object solve TSP
G = Graph()
G.setNodes(nodes)
G.setDistMatrix()
G.TSP(timelimit=40)

# Plot points and approximate optimal path
G.plot(style="line")