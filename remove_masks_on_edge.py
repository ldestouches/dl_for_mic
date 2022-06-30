# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:38:21 2022

@author: ldestouches
"""

import numpy as np
import matplotlib.pyplot as plt

import tifffile as tiff
import os

def extract_roi(mask):
    yy,xx=np.where(mask==1)
    ymin = max(yy.min(), 0)
    ymax = min(yy.max(), mask.shape[0])
    xmin = max(0,xx.min())
    xmax = min(xx.max(), mask.shape[1])

    return (xmin,ymin,xmax,ymax), mask[xmin:xmax,ymin:ymax]

# for 1 image

path = r"C:/Users/ldestouches/Documents/ANALYSIS FOR POSTER FIGURES/VANCOMYCIN/VANCO2_S3/VANCO2_LABEL_stardist_seq"
outpath = "C:/Users/ldestouches/Documents/ANALYSIS FOR POSTER FIGURES/VANCOMYCIN/VANCO2_S3/VANCO2_LABEL_edgesremoved"

def remove_edge_masks(path, name):
    
    im = tiff.imread(path)
    
    plt.figure()
    plt.imshow(im, cmap = 'gray')
    
    # name = path.split("/")[-1]
    plt.title(name)
    
    label_values = np.unique(im)
    nlabels = len(label_values)
    
    masklabels_todel = []
    masklabels_tokeep = []
    
    for i in range(1, nlabels):
        
        masklabel = im==label_values[i]
        maskcoords, mask = extract_roi(masklabel)
        
        # set the threshold for the edge masks you want to remove
        imxmin = 10
        imymin = 10
        imxmax = im.shape[1] - 10
        imymax = im.shape[0] - 10
        
        if maskcoords[0] <= imxmin or maskcoords[1] <= imymin or maskcoords[2] >= imxmax or maskcoords[3] >= imymax:
            masklabels_todel.append(label_values[i]) # save in list the label value of the masks you want to delete
            #print(maskcoords)        
            '''
            plt.figure()
            plt.subplot(121)
            plt.imshow(im)
            plt.title(name)
            plt.subplot(122)
            plt.imshow(masklabel)
            plt.title(str(label_values[i]))'''
        
        else:
            masklabels_tokeep.append(label_values[i]) # save in list the label value of the masks you want to keep
        
    print("masklabels to delete", masklabels_todel)
    print("masklabels to keep", masklabels_tokeep)
    
    # Create new image without the masks on the edge
    
    im2 = im.copy()
    label_values_2 = np.unique(im2)
    nlabels2 = len(label_values_2)
    
    new_im = 0
    
    for i in range(nlabels):
        
        if label_values_2[i] in masklabels_tokeep:
            new_im += (im == label_values_2[i])*label_values_2[i]
    
    new_name = name.split('.tif')[0] + '_noedge.tif'
    
    plt.figure()
    plt.imshow(new_im) # cmap='Paired'
    plt.title(new_name)
    
    return new_im, new_name

for file in os.listdir(path):
    
    im_path = os.path.join(path,file)
    new_im, new_name = remove_edge_masks(im_path,file)
    tiff.imwrite(os.path.join(outpath,new_name), np.asarray(new_im))