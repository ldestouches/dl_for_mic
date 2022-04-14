# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:47:09 2022

@author: ldestouches
"""

import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Loop through folder

directory = r"C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Images for Annotations\CycloFosfo_Mask"

outpath = r"C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Images for Annotations\CycloFosfo_mask_cleanname"

for file in os.listdir(directory):
    
    print('\n', file)
    im_path = os.path.join(directory,file)

    im = np.array(Image.open(im_path))
    
    plt.figure()
    plt.imshow(im)
    plt.show()
    
    cleanname = file.split('.tif')[0].split('_mask')[0] + '.tif'

    imarr = Image.fromarray(im).save(os.path.join(outpath,cleanname))
    #imarr.save(os.path.join(outpath,cleanname))
