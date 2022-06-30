# -*- coding: utf-8 -*-
"""
Created on Tue May 31 10:06:36 2022

@author: ldestouches
"""

import numpy as np
import matplotlib.pyplot as plt

import tifffile as tiff
import os

TL_raw_path = r"C:/Users/ldestouches/Documents/ANALYSIS FOR POSTER FIGURES/VANCOMYCIN/VANCO2_S3/VANCO2_raw_seq"
TL_tfsel_outpath = r"C:/Users/ldestouches/Documents/ANALYSIS FOR POSTER FIGURES/VANCOMYCIN/VANCO2_S3/VANCO2_sel_seq"

for count, file in enumerate(os.listdir(TL_raw_path)):

    if count % 4 == 0:
        
        im_path = os.path.join(TL_raw_path,file)
        im = tiff.imread(im_path)
        plt.figure()
        plt.imshow(im, cmap = 'gray')
        plt.title(file)
        
        name = file.split('.tif')[0] + '_sel.tif'
        
        im_outpath = os.path.join(TL_tfsel_outpath,name)
        
        tiff.imsave(im_outpath, np.asarray(im))
