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

# ANALYSIS OF LABEL IMAGES

# CONTROL image
ctrlim = tiff.imread(r"C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/Fosfo Analysis/Im for fosfo analysis/Fosfo_140220_Stage9_01_9.tif")
ctrlnlabelsbac = np.unique(ctrlim).size - 1
plt.figure() # visual image
plt.imshow(ctrlim, cmap = 'nipy_spectral')
plt.show()

plt.figure() # figure for rectangles plot
plt.imshow(ctrlim,cmap='gray')   

ctrlwidths = []
ctrllengths = []

for i in range(ctrlnlabelsbac):
    onectrlbac = ctrlim==i+1
    plot_patch(onectrlbac)
    widthctrlbac, lengthctrlbac = get_widthlength_rect(onectrlbac)
    print('bacteria with label {} has measured length of {:.2f}'.format(
        i+1, lengthctrlbac))
    print('bacteria with label {} has measured width of {:.2f}'.format(
        i+1, widthctrlbac))
    ctrlwidths.append(widthctrlbac)
    ctrllengths.append(lengthctrlbac)


# ANTIBIOTIC image
antibim = tiff.imread(r"C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/Fosfo Analysis/Im for fosfo analysis/Fosfo_140220_Stage8_80_8.tif")
antibnlabelsbac = np.unique(antibim).size - 1
plt.figure() # visual image
plt.imshow(antibim, cmap = 'nipy_spectral')
plt.show()

plt.figure() # figure for rectangles plot
plt.imshow(antibim,cmap='gray')   

antibwidths = []
antiblengths = []


for j in range(antibnlabelsbac):
    oneantibbac = antibim==j+1
    plot_patch(oneantibbac)
    widthantibbac, lengthantibbac = get_widthlength_rect(oneantibbac)
    print('bacteria with label {} has measured length of {:.2f}'.format(
        j+1, lengthantibbac))
    print('bacteria with label {} has measured width of {:.2f}'.format(
        j+1, widthantibbac))
    antibwidths.append(widthantibbac)
    antiblengths.append(lengthantibbac)
    
#scatterplots

plt.figure()
plt.title("Scatter plot for widths by lengths of control and antibiotic-treated bacteria")
plt.scatter(ctrllengths,ctrlwidths, label='control', color='blue')
plt.scatter(antiblengths,antibwidths,label='antibiotic',color='orange')
plt.xlabel('length in pixels (p = 0.0645 micrometer)')
plt.ylabel('width in pixels (p = 0.0645 micrometer)')
plt.legend()

'''
plt.figure()
plt.title("Scatter plot for lengths of bacteria")
plt.scatter(range(len(ctrllengths)),ctrllengths, label='control',color='green')
plt.scatter(range(len(antiblengths)),antiblengths,label='antibiotic',color='purple')
plt.legend()
'''

# boxplot
allwidths = [ctrlwidths, antibwidths]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(allwidths)
plt.xticks([1,2],['control','antibiotics'])
plt.title('Boxplots for widths of control and antibiotic-treated bacteria')
plt.show()


# aspect ratios

ctrlratios = []
for k in range(len(ctrllengths)):
    ctrlratio = ctrlwidths[k] / ctrllengths[k]
    ctrlratios.append(ctrlratio)
    
antibratios = []
for l in range(len(antiblengths)):
    antibratio = antibwidths[l] / antiblengths[l]
    antibratios.append(antibratio)

# boxplot aspect ratios
allratios = [ctrlratios, antibratios]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(allratios)
plt.xticks([1,2],['control','antibiotics'])
plt.title('Boxplots for aspect ratios of control and antibiotic-treated bacteria')


    
    
    
    
    