# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:03:17 2022

@author: ldestouches
"""
# ----------------------------------------------------------------------------------------------------------
# ANALYSE LABELS OF PREDICTED MASK IMAGES
#-----------------------------------------------------------------------------------------------------------

# Here we analyse the labels produced by the prediction models

import os
import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt

import cv2

# SPLINEDIST PREDICTION
spline_directory = r'C:\Users\ldestouches\Documents\SOFTWARE\SplineDist\SplineDist_GM_100_200eDefault\Quality Control\Prediction'

spline_prediction_areas = []

for file in os.listdir(spline_directory):
    im_path = os.path.join(spline_directory,file)
    im = tiff.imread(im_path)
    plt.figure()
    plt.imshow(im, cmap = 'nipy_spectral')
    plt.show()

    # number of labels
    nlabels = np.unique(im).size - 1


    # areas of labels - object size in pixel
    # multiply later by real value.    
    tot_bact_area = cv2.countNonZero(im)
    
    area_list = []
    
    area = 0
    for i in range(1,nlabels):
        if im == i: # returns error -- i want it to count for each pixel when it is equal to i
            area = area+1
        else:
            continue
    area_list.append(area)
    
    
    spline_prediction_areas.append(area_list)
    
    # length of labels
    # width of labels
        