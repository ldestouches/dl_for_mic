# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 14:31:59 2022

@author: ldestouches
"""

import pandas as pd
import tifffile
import matplotlib.pyplot as plt
import numpy as np

# read image and manual csv
df = pd.read_csv("C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_100/manual_measures/test_21_st1_03.csv")

path_image = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_100/Mask_100/210709_bCPC13_Stage1-10003.tif"

# converting csv to list
indices = df["Median"].tolist()
lengths = df["Length"].tolist()
ind = 1

# choosing index from the csv
indice = indices[ind]
length = lengths[ind]

# make mask equal to chosen label
image = tifffile.imread(path_image)
mask = image==indice

# plot figure
plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(mask)




