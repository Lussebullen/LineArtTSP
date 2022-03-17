# LineArtTSP

## Authors

Lussebullen

sylviaberry

aneveu23

## Description:
PIC16A UCLA project, approximate images using a single closed curve generated by halftoning the image and finding a cycle by solving TSP on the generated stippling points.

The backbone of this project will consist of these major components:

1. Halftone an arbitrary image and convert points to graph object using rejection sampling.
2. Find (ideally) non self-intersecting Hamiltonian cycle on nodes by solving TSP using heuristic.
3. Plot the resulting curve


## Instructions:
To prepare your environment run:

conda create --name NEWENV --file requirements.txt

Using the supplied requirements.txt file.

Furthermore you must install ortools and its dependencies.

For windows see:
https://developers.google.com/optimization/install/python/windows

For Mac see:
https://developers.google.com/optimization/install/python/mac

## Scope and Limitations:
It should come as no surprise that, with a plethora of types of images, some work better or worse depending on the halftoning method used, as well as in general. The contrast method works well when the image has clearly accentuated pixels, or solid colors, as it becomes easy for the halftoning to identify regions of the image with color disparities. It does not work as well, however, for artwork such as the Mona Lisa, where ‘pixels’, irrespective of location in the image, have different colors, but oftentimes not by enough to create a meaningful contrast_threshold constant that generates a good picture. In this case, increasing the smoothing constant can help by adding a bit more structure to areas with a bit less contrast, at the expense of also adding some more random noise, without losing the structure of the image. 

The brightness method, on the other hand, works well when working with a picture wherein a pixel’s desirability is strongly connected to how dark it is. For example, the brightness method fares better than contrast on the Mona Lisa: attempting to find contrast locally in an image where there is contrast everywhere is meaningless, but brightness allows for a ‘bigger picture’ understanding of the image, and oftentimes produces better point selection as a result. Additionally, it deals well with both bright and dark areas of focus within an image, as one can use the ‘invert’ function to choose points from bright areas or dark areas. However, while it still works decently, the brightness method fails to capture the complexity of more ‘modern’  pictures, where differences between local regions within an image is clearly accentuated. In these sorts of pictures, one is better off using the contrast method with a fairly low contrast_threshold. 

Where both methods fail, however, is choosing useful points in images that are uniformly bright or dark, with only small changes in color throughout the image identifying the figure: imagine a dark figure in a cave, or a sheep in a snowy landscape. In these types of images, it becomes nearly impossible to find a contrast_threshold that both captures the essence of the image without introducing noise, and due to the uniformity of the image’s brightness, far too much noise is introduced to gain any information about specific objects in the image. Depending on the picture, this can occasionally be resolved by using the invert function with the contrast method to only take areas that are extremely uniform in color, but this is no guarantee. If we were to revisit this project in the future, finding a way to address this complicated issue would be interesting. 

A user’s biggest dilemma when using our code, aside from choosing a halftoning method, is choosing an appropriate number of points, and how long to allow the code to run. The traveling salesman problem finds the shortest path visiting every point and returning to the original point - this is highly practical when considering a path between a few dozen areas one may have to visit (say, as a delivery driver/tourist/bus driver), but expectedly becomes a much more complicated problem when trying work with hundreds or thousands of points selected from an image. It would be difficult to explain every aspect of the TSP here, but it considers how to find this path by using spanning trees between points, and these trees naturally become increasingly complex as the number of points increases. This problem is especially difficult when using the brightness halftoning method, as points tend to be in masses rather than in lines, the latter of which intuitively allows for an easier optimal path. Therefore, when running the program, the user will likely have to sacrifice one of three properties: time (as a result of runtime), image density (as a result of the number of points), or image quality (as a result of a suboptimal path chosen by TSP, due to not enough time). Unlike point selection, it is not clear that there is actually a way to resolve this problem based on the program’s current structure. However, in the future, it may be worth exploring (particularly for a halftoning method such as contrast, which, as mentioned, tends to create point structures resembling lines)  if there is a method of constructing edges between points that is less computationally expensive, even as simple as just creating a loop of edges that continuously jumps to the next closest point.

One issue that came to mind when working on our project was the jagged/unappealing nature of a graph with straight edges between vertices. As a result, our program will also output a rendition of the graph using splines. We found that this made the resulting graph more pleasant to look at, without sacrificing its structural purpose.

Our project, in our view, did not introduce any apparent ethical considerations. However, had we chosen to associate colors with points in our graphs, there may have been an accessibility problem with the graphs generated by our program, particularly regarding visual clarity. Therefore, we decided to opt for a single, high contrast color, so as to maintain the spirit of our project (generating artistic graphs from images) without sacrificing accessibility to the end result. 


## License:
This project is licensed under the terms of the MIT license.

## Demo file description:



## References
We would like to thank the Google Developers team for their detailed description of
how to apply their OR-tools library to solve the Traveling Salesman Problem.
