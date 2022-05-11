# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:57:11 2022

@author: ldestouches
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D

import tifffile as tiff
import os
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

# WIDTHS ANALYSIS OVER TIME FOR CYCLOSERINE

directory = r"C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Fosfo Analysis\Im for fosfo analysis"
nfiles = len(os.listdir(directory))

for file in os.listdir(directory):
    
    im_path = os.path.join(directory,file)
    im = tiff.imread(im_path)
    plt.figure()
    plt.imshow(im, cmap = 'gray')
    plt.title(file)
    
    nlabel = np.unique(im).size - 1
    widths = []
    lengths= []
    
    print(file)
    for i in range(nlabel):
        onebac = im==i+1
        plot_patch(onebac)
        widthbac, lengthbac = get_widthlength_rect(onebac)
        #print('bacteria with label {} has measured length of {:.2f}'.format(
        #    i+1, lengthbac))
        #print('bacteria with label {} has measured width of {:.2f}'.format(
        #    i+1, widthbac))
        widths.append(widthbac)
        lengths.append(lengthbac)
        
    filetimepoint = int(file.split('_')[3])
    print(filetimepoint)

    if filetimepoint == 1:
        widths01 = widths
    elif filetimepoint == 20:
        widths20 = widths
    elif filetimepoint == 30:
        widths30 = widths
    elif filetimepoint == 40:
        widths40 = widths
    elif filetimepoint == 60:
        widths60 = widths
    elif filetimepoint == 80:
        widths80 = widths
    else:
        continue


# boxplot
allwidths = [widths01, widths30, widths40, widths60, widths80]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(allwidths)
#plt.xticks([1,2,3,4,5],['2','60','80','120','140'])
plt.xlabel('time (min)')
plt.ylabel('width in pixels (1 pix = 0.0645 micrometer)')
plt.title('Boxplots for widths of bacteria treated with Fosfomycin')




