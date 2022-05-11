# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:22:47 2022

@author: ldestouches
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D

import tifffile as tiff        
import cv2

def get_widthlength_rect(msk, plot=False):
    """Gets the length of a mask using minarea rectangle"""
    mask = msk.copy()
    mask = mask.astype(np.uint8)
    if np.count_nonzero(mask)<2:
        return 0
    cnt,hierarchy = cv2.findContours(mask, 1, 2)
    cnt = np.vstack(cnt).squeeze()
    
    # returns the min area rectangle: ( (x_centre, y_centre), (x_size, y_size), rotation_angle )
    rect = cv2.minAreaRect(cnt)
    if plot:
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        
        # converts image to BGR (=3 color channels) for display purpose
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(mask,[box],0,(0,0,255),1)
        cv2.imshow("mask and approximation",mask)
    return min(rect[1]),max(rect[1])

def plot_patch(mask):
    """Method to plot the rectangle detected from a mask on the current axis."""
    mask = mask.astype(np.uint8)
    if np.count_nonzero(mask)<2:
        return 0
    cnt,hierarchy = cv2.findContours(mask, 1, 2)
    cnt = np.vstack(cnt).squeeze()
    
    # returns the min area rectangle: ( (x_centre, y_centre), (x_size, y_size), rotation_angle )
    rect = cv2.minAreaRect(cnt)

    xy = np.array(rect[0])-np.array(rect[1])/2
    
    # plt.gca().scatter(rect[0][0],rect[0][1])
    ax = plt.gca()
    ax.add_patch(patches.Rectangle(xy,rect[1][0],rect[1][1],
                              linewidth=1,edgecolor='y',
                              facecolor='none',
                              transform=Affine2D().rotate_deg_around(*rect[0], rect[2])+ax.transData))     


# from a real image
image3 = tiff.imread(r"C:/Users/ldestouches/Documents/SOFTWARE/SplineDist/SplineDist_CycloFosfo_100eDefault_patch128/Quality Control/Prediction/Fosfo_241120_Position2_80_2.tif")
nlabelsbac = np.unique(image3).size - 1
plt.figure() # visual image
plt.imshow(image3, cmap = 'nipy_spectral')
plt.show()

plt.figure() # figure for rectangles plot
plt.imshow(image3,cmap='gray')   

widths = []
lengths = []

for k in range(nlabelsbac):
    onebac = image3==k+1
    plot_patch(onebac)
    widthbac, lengthbac = get_widthlength_rect(onebac)
    print('bacteria with label {} has measured length of {:.2f}'.format(
        k+1, lengthbac))
    print('bacteria with label {} has measured width of {:.2f}'.format(
        k+1, widthbac))
    widths.append(widthbac)
    lengths.append(lengthbac)
    
plt.figure()
plt.title("Scatter plot for widths of bacteria")
plt.scatter(range(len(widths)),widths,color='red')
plt.figure()
plt.title("Scatter plot for lengths of bacteria")
plt.scatter(range(len(lengths)),lengths,color='green')
