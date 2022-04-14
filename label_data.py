
import os
import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt

# For loop

# path to folder of masks

directory = r'C:\Users\ldestouches\Documents\IMAGES\ML_SIM\SIM_treated\mask_treated'

for file in os.listdir(directory):
    
    # upload image
    im_path = os.path.join(directory,file)
    im = tiff.imread(im_path)
    
    # show image
    plt.figure()
    plt.imshow(im, cmap = 'nipy_spectral')
    plt.show()
    
    # save labels
    labels = np.unique(im)
    
    # 
    
    
# stage4_10000.tif HAS 4 LABELS
