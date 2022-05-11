# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 15:14:22 2022

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

TL_directory = r"C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Cyclo Analysis\TL_masks_trackmate_StarDist\test_code"
# C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Cyclo Analysis\TL_masks_trackmate_StarDist\test_code
# C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Cyclo Analysis\TL_masks_trackmate_StarDist\Cyclo_271120_Pos18_Stardist600eselval_unstacked
nfiles = len(os.listdir(TL_directory))
print(nfiles)
all_filewidths = [[] for i in range(nfiles)]
all_nlabels = []
#ind_files = [i for i in range(nfiles)] 
print(all_filewidths)

ind = 0

for file in os.listdir(TL_directory):
    
    im_path = os.path.join(TL_directory,file)
    im = tiff.imread(im_path)
    plt.figure()
    plt.imshow(im, cmap = 'gray')
    plt.title(file)
    
    label_values = np.unique(im)
    nlabel = np.unique(im).size - 1
    all_nlabels.append(nlabel)

    widths = []
    lengths= []
    
    print(file,ind)
    
    for i in range(1,nlabel):
        onebac = im==label_values[i]
        # plot_patch(onebac)
        widthbac, lengthbac = get_widthlength_rect(onebac)
        #print('bacteria with label {} has measured length of {:.2f}'.format(
        #    i+1, lengthbac))
        #print('bacteria with label {} has measured width of {:.2f}'.format(
        #    i+1, widthbac))
        widths.append(widthbac)
        lengths.append(lengthbac)
          
    # need to make a loop to iterate over nfiles
    for i in range(1,nfiles):
        if ind == i:
            all_filewidths[i] = widths # here I append a list within a list

    ind = ind + 1
    
print(all_filewidths)

# boxplot
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(all_filewidths)
plt.xticks(list(range(nfiles)),list(range(nfiles)), fontsize=6 ) # what to do here?
plt.xlabel('timepoints (tp = 2 min)')
plt.ylabel('width in pixels (1 pix = 0.0645 micrometer)')
plt.title('Boxplots for widths of Cyclosérine-treated bacteria from TrackMate-StarDist')

# plot growth rate
fig2 = plt.figure()
ax2 = fig2.add_axes([0,0,1,1])
ax2.plot(range(len(all_nlabels)),all_nlabels)
ax2.set_title('growth of bacteria')
ax2.set_xlabel('timepoints (1 tp = 2min)')
ax2.set_ylabel('number of bacteria')