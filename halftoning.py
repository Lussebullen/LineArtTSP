import random as rd
import numpy as np
from matplotlib import pyplot as plt


########################################################################################################################
# Image stippling, take the image as input and do all the processing to generate stippling vertices.
########################################################################################################################
# Used this source for Stippling: https://www.cs.ubc.ca/labs/imager/tr/2002/secord2002b/secord.2002b.pdf

def rejectionSampling(n, M, imagestyle="brightness"):
    """
    :param n:   Desired amount of samples
    :param M:   Matrix containing grayscale values of pixels in image, rejection function
    :return:    Set of crude initial stippling points
    """
    #CONTRAST METHOD 
    if imagestyle == "contrast":
        img_pixels = np.array(list(M.getdata())).reshape((M.size[1], M.size[0], 3))/255
        contrast_array = np.array([[np.linalg.norm(img_pixels[i, j, :] - img_pixels[i-5, j, :])/np.sqrt(3) for j in range(M.size[0])] for i in range(5, M.size[1])])
        r = len(contrast_array)      # Rows
        c = len(contrast_array[0]) 
        a = 0           # Accepted samples
        X = [0] * n
        Y = [0] * n
        while a < n:
            x = int(rd.uniform(0, c))
            y = int(rd.uniform(0, r))
            u = 0.15
            if contrast_array[y][x] > u:
                X[a] = x
                Y[a] = y
                a += 1
        return np.array([[X[i], Y[i]] for i in range(len(X))])
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