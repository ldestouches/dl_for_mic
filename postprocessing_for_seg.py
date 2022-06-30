# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:13:30 2022

@author: ldestouches
"""

# -----------------------------------------------------------------------------
# POST-PROCESSING FOR SEGMENTATION MODELS
# -----------------------------------------------------------------------------

# For the moment can only do the removed edges on the images but can not write the csv files yet

# Imports
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import os
from PIL import Image

# PATHS

# Enter path to the folder with the label sequences
TL_label_folder = r"C:/Users/ldestouches/Documents/PAPER 2/LABELS"
# Enter path to the folder where you want to save your treated sequences
postprocessing_folder = r"C:/Users/ldestouches/Documents/PAPER 2/POST-PROCESSED SEQUENCES"
# Enter path to the fodler where you will save all your csv file
csv_folder = r"C:/Users/ldestouches/Documents/PAPER 2/CSV"

# FUNCTIONS

def extract_roi(mask):
    yy,xx=np.where(mask==1)
    ymin = max(yy.min(), 0)
    ymax = min(yy.max(), mask.shape[0])
    xmin = max(0,xx.min())
    xmax = min(xx.max(), mask.shape[1])

    return (xmin,ymin,xmax,ymax), mask[xmin:xmax,ymin:ymax]

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
    
    new_im = im2 * 0
    
    for i in range(nlabels):
        
        if label_values_2[i] in masklabels_tokeep:
            new_im += (im == label_values_2[i])*label_values_2[i] # here for as array?
    
    new_name = name.split('.tif')[0] + '_noedge.tif'
    
    plt.figure()
    plt.imshow(new_im) # cmap='Paired'
    plt.title(new_name)
    
    return new_im, new_name

# POST PROCESSING LABELS

for folder in os.listdir(TL_label_folder):
    
    print("processing folder: ", folder)
    tl_dir = os.path.join(TL_label_folder,folder) 

#####     STEP 1 - Remove masks on Edge

    # creating a outpath folder to store selected images
    rem_folder_name = folder + '_rem'    
    rem_folder_path = os.path.join(postprocessing_folder, rem_folder_name)
    os.mkdir(rem_folder_path)
    
    for file in os.listdir(tl_dir):
        
        im_path = os.path.join(tl_dir,file)
        new_im, new_name = remove_edge_masks(im_path,file)
        
        tiff.imwrite(os.path.join(rem_folder_path,new_name), np.asarray(new_im))


#####     STEP 2 - Extract widths and save into a csv file

#    for file in os.listdir(rem_folder_path):
        
        # problem is I need to save the ones of the same name in the same csv file...
        

