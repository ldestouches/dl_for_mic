# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:40:12 2022

@author: ldestouches
"""

# ----------------------------------------------------------------------------

# GROWTH & WIDTH

# ----------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D

import tifffile as tiff
import os
import cv2

# FUNCTION

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
    return min(rect[1]) #,max(rect[1]) choosing just the widths

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


TL1_directory = r"C:/Users/ldestouches/Documents/ANALYSIS FOR POSTER FIGURES/CONTROL/CTRL1 2020-02-13 st3/LABEL_CTRL1_edgesremoved"
TL2_directory = r"C:/Users/ldestouches/Documents/ANALYSIS FOR POSTER FIGURES/D-CYCLOSERINE/CYCLO1 P7/CYCLO1_LABEL_edgesremoved"

pixel_size_T1 = 0.100
pixel_size_T2 = 0.100

def nlabels_and_widths_from_directory(directory, pixel_size):
    
    # number of files in directory
    nfiles = len(os.listdir(directory))
    print("the number of files in the directory is: ", nfiles)
    
    # list for storing all the widths of all the images
    all_filewidths = [[] for i in range(nfiles)]
    # list for storing the number of bacteria in each image
    all_nlabels = []
    
    # index for the lists
    ind = 0
    
    for file in os.listdir(directory):
        
        # read and show image
        im_path = os.path.join(directory,file)
        im = tiff.imread(im_path)
        '''
        plt.figure()
        plt.imshow(im, cmap = 'gray')
        plt.title(file)
        '''
        # find number of bacteria in image
        label_values = np.unique(im)
        nlabel = np.unique(im).size - 1
        all_nlabels.append(nlabel) # add to all files list
        
        # Empty lists where we put the widths for the image
        widths = []
        
        print("processing file: ", file, "of index", ind)
        
        for i in range(1,nlabel):
            onebac = im==label_values[i]
            # plot_patch(onebac)
            widthbac = get_widthlength_rect(onebac) * pixel_size # multiply by pixel size
            #print('bacteria with label {} has measured width of {:.2f}'.format(i+1, widthbac))
            widths.append(widthbac)
              
        # need to make a loop to iterate over nfiles
        for i in range(0,nfiles):
            if ind == i:
                all_filewidths[i] = widths # here I append a list within a list
    
        ind = ind + 1
    
    return all_nlabels, all_filewidths

# Number of bacteria and big list of widths for timelapse 1
nlabels_TL1, filewidths_TL1 = nlabels_and_widths_from_directory(TL1_directory, pixel_size_T1)
print(nlabels_TL1, filewidths_TL1)

# for timelapse 2
nlabels_TL2, filewidths_TL2 = nlabels_and_widths_from_directory(TL2_directory, pixel_size_T2)
print(nlabels_TL2, filewidths_TL2)


# Combine boxplot and growth rate
# TIMELAPSE 1

c1 = 'g'
c2 = 'r'

fig1 = plt.figure()
ax1 = fig1.add_axes([0,0,1,1])
bp1 = ax1.boxplot(filewidths_TL1,vert=True,  # vertical box alignment
                     patch_artist=True,
                     boxprops = dict(facecolor=c1, color=c1))
plt.title("growth and width of bacteria over time")
plt.xlabel("timepoint (every 8 minutes)")
plt.ylabel("boxplot widths of bacteria (μm)", color = 'k')

ax2 = ax1.twinx()
ax2.plot(range(1,(len(nlabels_TL1)+1)),nlabels_TL1, '.-g', label = 'ctrl')
plt.ylabel('number of bacteria', color = 'k')

# TIMELAPSE 2

figA = plt.figure()
axA = figA.add_axes([0,0,1,1])
bp2 = axA.boxplot(filewidths_TL2, vert=True,  # vertical box alignment
                     patch_artist=True,
                     boxprops = dict(facecolor=c2, color=c2))
plt.title("growth and width of bacteria over time")
plt.xlabel("timepoint (every 8 minutes)")
plt.ylabel("boxplot widths of bacteria (μm)", color = 'k')

axB = axA.twinx()
axB.plot(range(1,(len(nlabels_TL2)+1)),nlabels_TL2, '.-r')
plt.ylabel('number of bacteria', color = c2)


# overlapping graphs
bp3 = ax1.boxplot(filewidths_TL2, vert=True,  # vertical box alignment
                     patch_artist=True,
                     boxprops = dict(facecolor=c2, color=c2))
plt.title("growth and width of bacteria over time")
plt.xlabel("timepoint (every 8 minutes)")
plt.ylabel("boxplot widths of bacteria (μm)", color = 'k')

ax2.plot(range(1,(len(nlabels_TL2)+1)),nlabels_TL2, '.-r', label = 'Fosfo')
plt.ylabel('number of bacteria', color = c2)
ax2.legend(loc='upper left')



