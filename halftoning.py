import random as rd
import numpy as np
from PIL import Image, ImageOps

########################################################################################################################
# Image stippling, take the image as input and do all the processing to generate stippling vertices.
########################################################################################################################
# Used this source for Stippling: https://www.cs.ubc.ca/labs/imager/tr/2002/secord2002b/secord.2002b.pdf

def rejectionSampling(n, path, imagestyle="brightness", pixel_distance = 5, contrast_threshold = 0.15):
    """
    :param n:   Desired amount of samples
    :param path:   path to image file for halftoning
    :return:    Set of crude initial stippling points
    """
    # Rotate and flip image
    M = Image.open(path).rotate(180)
    M = ImageOps.mirror(M)

    #CONTRAST METHOD 
    if imagestyle == "contrast":
        img_pixels = np.array(list(M.getdata())).reshape((M.size[1], M.size[0], 3))/255
        #play around with the i-5 and range(5, ..); change 5 to various values
        contrast_array = np.array([[np.linalg.norm(img_pixels[i, j, :] - img_pixels[i-pixel_distance, j-pixel_distance, :])/np.sqrt(3) for j in range(pixel_distance, M.size[0])] for i in range(pixel_distance, M.size[1])])
        #I set up the following code identically
        r = len(contrast_array)
        c = len(contrast_array[0]) 
        a = 0 
        X = [0] * n
        Y = [0] * n
        while a < n:
            x = int(rd.uniform(0, c))
            y = int(rd.uniform(0, r))
            #play around with this u constant; it determines what level of contrast is considered.

            if contrast_array[y][x] > contrast_threshold:
                X[a] = x
                Y[a] = y
                a += 1
        return np.array([[X[i], Y[i]] for i in range(len(X))])
    
    #BRIGHTNESS METHOD 
    if imagestyle == "brightness":
        M_gray = M.convert('L')
        M_pixels = np.array(list(M_gray.getdata())).reshape((M_gray.size[1], M_gray.size[0]))/255
        r = len(M_pixels)      # Rows
        c = len(M_pixels[0])   # Columns
        a = 0           # Accepted samples
        X = [0] * n
        Y = [0] * n
        while a < n:
            x = int(rd.uniform(0, c))
            y = int(rd.uniform(0, r))
            u = rd.uniform(0, 1)
            if u > M_pixels[y][x]:
                X[a] = x
                Y[a] = y
                a += 1
        return np.array([[X[i], Y[i]] for i in range(len(X))])