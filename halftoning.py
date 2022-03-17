import random as rd
import numpy as np
from PIL import Image, ImageOps
import math

########################################################################################################################
# Image stippling, take the image as input and do all the processing to generate stippling vertices.
########################################################################################################################
# Used this source for Stippling: https://www.cs.ubc.ca/labs/imager/tr/2002/secord2002b/secord.2002b.pdf

def rejectionSampling(n, path, imagestyle="brightness", x_pixel_distance = 5, y_pixel_distance = 5, contrast_threshold = 0.15, smoothing_constant = 0, invert = True):
    """
    :param n:   Desired amount of samples
    :param path:   path to image file for halftoning
    :return:    Set of crude initial stippling points
    :imagestyle: brightness or contrast as a method of point selection
    :x_pixel_distance: and :y_pixel_distance: the pixel shifts used to determine contrast between pixels
    :contrast_threshold: the value about which a threshold for point selection is formed - 100% acceptance if smoothing_constant = 0 and contrast exceeds threshold
    :smoothing_constant: Linear smoothening of probability of a point being selected about the contrast threshold - allows for lower contrast to be accepted, and higher contrast to be accepted less frequently
    :invert: If on, takes points only similar to local pixels for contrast method, or points closer to white for brightness method. If off, takes points only different from local pixels for contrast
    method, or points closer to black for brightness method.
    """
    # Rotate and flip image
    M = Image.open(path).rotate(180)
    M = ImageOps.mirror(M)
    #CONTRAST METHOD 
    if imagestyle == "contrast":
        #checking some input values are legitimate
        if contrast_threshold < 0 or contrast_threshold > 1:
            raise ValueError("Contrast threshold must be a number between 0 and 1, inclusive.")
        if abs(x_pixel_distance) > M.size[0]:
            raise ValueError("x pixel shift exceeds number of x pixels")
        if abs(y_pixel_distance) > M.size[1]:
            raise ValueError("y pixel shift exceeds number of y pixels")
        #creating NP array based on image
        M_array = np.array(list(M.getdata()))
        #Checking if image has RGB pixels - if not, 'broadcasts' to RGB
        if M_array.size != M.size[1]*M.size[0]*3:
            M_array = np.stack((M_array,)*3, axis = 1)
        #reshaping array into image dimensions
        img_pixels = M_array.reshape((M.size[1], M.size[0], 3))/255
        #creating shifted contrast array based on x,y pixel distance constants
        contrast_array = np.array([[np.linalg.norm(img_pixels[i, j, :] - img_pixels[i-x_pixel_distance, j-y_pixel_distance, :])/np.sqrt(3) for j in range(max(0,x_pixel_distance), min(M.size[0], M.size[0]+x_pixel_distance))] for i in range(max(0,y_pixel_distance), min(M.size[1], M.size[1]+y_pixel_distance))])
        r = len(contrast_array)
        c = len(contrast_array[0]) 
        a = 0 
        #preemptively creating blank point 
        X = [0] * n
        Y = [0] * n
        #creating appropriate smoothing function, if smoothing is enabled
        if smoothing_constant > 0 and smoothing_constant <= 1:
            smoothing_slope = 1/(2*contrast_threshold*smoothing_constant)
        #raising value error if smoothing error is impossible value
        elif smoothing_constant < 0 or smoothing_constant > 1:
            raise ValueError("Smoothing constant must be a value between 0 and 1, inclusive.")
        #checking if inversion is on, reflecting acceptance probabilities about 0.5 if so
        if invert == False:
            while a < n:
                #choosing random x and y points
                x = int(rd.uniform(0, c))
                y = int(rd.uniform(0, r))
                #checking if we have smoothing or not - creating acceptance probability for point based on appropriate smoothing function if so
                if smoothing_constant == 0:
                    if contrast_array[y][x] > contrast_threshold:
                        acceptance_probability = 1
                    else:
                        acceptance_probability = 0
                else:
                    acceptance_probability = max(min(1, smoothing_slope*(contrast_array[y][x]-contrast_threshold)+0.5), 0)
                #randomly accepting point, otherwise it returns to the pool of possible points to be selected
                if rd.random() < acceptance_probability:
                    X[a] = x
                    Y[a] = y
                    a += 1
        else:
            while a < n:
                x = int(rd.uniform(0, c))
                y = int(rd.uniform(0, r))
                if smoothing_constant == 0:
                    if contrast_array[y][x] > 1-contrast_threshold:
                        acceptance_probability = 0
                    else:
                        acceptance_probability = 1
                else:
                    acceptance_probability = max(min(1, 1-smoothing_slope*(contrast_array[y][x]-(1-contrast_threshold))+0.5), 0)
                if rd.random() < acceptance_probability:
                    X[a] = x
                    Y[a] = y
                    a += 1
        #returning appropriate array  
        return np.array([[X[i], Y[i]] for i in range(len(X))])
    
    #BRIGHTNESS METHOD 
    #majority of pieces of code are identical to those in contrast method - refer to comments above
    if imagestyle == "brightness":
        M_gray = M.convert('L')
        M_pixels = np.array(list(M_gray.getdata())).reshape((M_gray.size[1], M_gray.size[0]))/255
        r = len(M_pixels)      # Rows
        c = len(M_pixels[0])   # Columns
        a = 0           # Accepted samples
        X = [0] * n
        Y = [0] * n
        if invert == False:
            while a < n:
                x = int(rd.uniform(0, c))
                y = int(rd.uniform(0, r))
                u = rd.uniform(0, 1)
                if u > M_pixels[y][x]:
                    X[a] = x
                    Y[a] = y
                    a += 1
        else:
            while a < n:
                x = int(rd.uniform(0, c))
                y = int(rd.uniform(0, r))
                u = rd.uniform(0, 1)
                if u < M_pixels[y][x]:
                    X[a] = x
                    Y[a] = y
                    a += 1
        return np.array([[X[i], Y[i]] for i in range(len(X))])