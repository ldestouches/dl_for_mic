# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 10:09:08 2022

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

import pandas as pd

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

def plot_patch(mask): # I don't use this function, but it is to see the rectangle on the indiv bact
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

TL_directory = ["C:/Users/ldestouches/Documents/PAPER 2/POST-PROCESSED SEQUENCES/FOSFO1_LABEL_rem",
                "C:/Users/ldestouches/Documents/PAPER 2/POST-PROCESSED SEQUENCES/FOSFO2_LABEL_rem",
                "C:/Users/ldestouches/Documents/PAPER 2/POST-PROCESSED SEQUENCES/FOSFO3_LABEL_rem"]

path_csv = 'C:/Users/ldestouches/Documents/PAPER 2/CSV/FOSFO.csv' # give new name for your csv file here before the .csv

pixel_size = 0.100

time_between_frames = 30 # in minutes # this means every frame of the timelapse used is x minutes apart

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
        
        #print("processing file: ", file, "of index", ind)
        
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
    
    return all_filewidths


# Number of bacteria and big list of widths for timelapses

combined_widths = [[] for i in range(len(os.listdir(TL_directory[0])))]

for i in range(len(TL_directory)):

    widths_tl = nlabels_and_widths_from_directory(TL_directory[i], pixel_size)
    
    for j in range(len(widths_tl)):
        combined_widths[j].extend(widths_tl[j])
    

# create csv file

D = {}

for count,i in enumerate(range(len(combined_widths))):
    
    keys = str(count*time_between_frames)
    values = combined_widths[i]
    D[keys] = values

df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in D.items() ]))
df.to_csv(path_csv)


