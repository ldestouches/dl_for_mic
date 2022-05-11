# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:26:43 2022

@author: ldestouches
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
        
import cv2

def get_length_rect(msk, plot=False):
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
    return max(rect[1])

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
                              linewidth=3,edgecolor='y',
                              facecolor='none',
                              transform=Affine2D().rotate_deg_around(*rect[0], rect[2])+ax.transData))     

if __name__=='__main__':
    from skimage.filters import median
    from skimage.transform import rotate
    # generates an example
    image = np.zeros((200,200))

    length = 80
    width = 40
    image[50:50+length,80:80+width] = 1
    image = rotate(image,30)
    # gives it round edges
    image = median(image,np.ones((20,20)))
    
    # measures and compares with real value
    length_measured = get_length_rect(image)
    
    print('measured length: {}, real length: {}'.format(length_measured, length))
    plt.figure()
    plt.imshow(image,cmap='gray')   
    plot_patch(image)
    
    # second exemple: on a labeled image with 2 elements
    image2 = np.zeros((400,400))

    length = 80
    width = 40
    # creates first object. gives it label 1
    image2[50:50+length,80:80+width] = 1
    image2 = rotate(image2,50)
    
    # creates second, smaller object. Gives it label 2
    image2[ 200:200+length//2,150:150+width//2] = 2
    
    # gives it round edges
    image2 = median(image2,np.ones((20,20)))
    
    plt.figure()
    plt.imshow(image2)
    
    nlabels = 2 # there are 2 different labels in our image: 1 and 2
    for j in range(nlabels):
        # when j=1, selects only pixels that have value 1 e.g that belong to object 1
        image_oneobject = image2==j+1
        
        length = get_length_rect(image_oneobject)
        print('lobject with label {} has measured length of {:.2f}'.format(
            j+1, length))
     