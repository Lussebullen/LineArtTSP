from graph import Graph
from halftoning import rejectionSampling

# Generate test data points
n=200
# Path to image file
path = 'recurrentTheme.jpg'
# Generate points
nodes = rejectionSampling(n, path, imagestyle = "brightness")

# Create graph object solve TSP
G = Graph()
G.setNodes(nodes)
G.setDistMatrix()
G.TSP(timelimit=30)

# Plot points and approximate optimal path
G.plot(style="point")
G.plot(style="line")
G.plot(style="spline")