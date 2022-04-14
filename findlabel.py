#-----------------------------------------------------
# REMOVING IMAGES LESS THAN 5 MASKS
#-----------------------------------------------------

# This code finds the number of masks in an tiffile img and creates a dataset with all images apart from those with
# less than 5 masks per image.

import os
import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt

# Find label length for 1 image

'''
path = r"C:/Users/ldestouches/Documents/IMAGES/ML/TRAIN/Masks/210709_bCPC13_Stage1-10003.tif"

img = tifffile.imread(path)

plt.figure()
plt.imshow(img, cmap = 'nipy_spectral')
plt.show()

#print(np.unique(img))
print(np.unique(img).size-1)

print(path.split('/')[-1])
'''

# For loop

# path to folder of masks

directory = r'C:/Users/ldestouches/Documents/IMAGES/ML/TRAIN/Masks'

for file in os.listdir(directory):
    im_path = os.path.join(directory,file)
    im = tiff.imread(im_path)
    plt.figure()
    plt.imshow(im, cmap = 'nipy_spectral')
    plt.show()
    nlabel = np.unique(im).size - 1
    if nlabel <= 5:
        print(file, 'has', nlabel, 'labels')
    else:
        continue
    
# stage4_10000.tif HAS 4 LABELS
