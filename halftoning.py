import random as rd
import numpy as np


########################################################################################################################
# Image stippling, take the image as input and do all the processing to generate stippling vertices.
########################################################################################################################
# Used this source for Stippling: https://www.cs.ubc.ca/labs/imager/tr/2002/secord2002b/secord.2002b.pdf

def rejectionSampling(n, M):
    """
    :param n:   Desired amount of samples
    :param M:   Matrix containing grayscale values of pixels in image, rejection function
    :return:    Set of crude initial stippling points
    """
    r = len(M)      # Rows
    c = len(M[0])   # Columns
    a = 0           # Accepted samples
    X = [0] * n
    Y = [0] * n
    while a < n:
        x = int(rd.uniform(0, c))
        y = int(rd.uniform(0, r))
        u = rd.uniform(0, 1)
        if u > M[y][x]:
            X[a] = x
            Y[a] = y
            a += 1
    return np.array([[X[i], Y[i]] for i in range(len(X))])