#---------------------------------------------------------------------------------------------
# MAIN Command Center
#---------------------------------------------------------------------------------------------

from PIL import Image
import os
import tifffile as tiff
import numpy as np
from get_image_psize import *
from resize_psize import *

# Choose the target pixel size for resizing:
target_psize = 0.0645

# Loop through folder

directory = r"C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ANTIBIO\Images for Annotations\CycloFosfo_mask_cleanname"

outpath = r"C:\Users\ldestouches\Documents\IMAGES & TIMELAPSES\ML_ANTIBIO_FINAL_dataset_100\Mask_100"

for file in os.listdir(directory):
    
    print('\n', file)
    im_path = os.path.join(directory,file)

    im_tif = tiff.TiffFile(im_path)
    ori_psize_im = 0.0645 #get_image_psize(im_tif)
    
    im_pil = Image.open(im_path)
    resized_im = resize_psize(im_pil, ori_psize_im, target_psize)

    name = file.split('.tif')[0].split('_resized')[0].split('_mask')[0] + '.tif'

    new_meta = 'Pixel size: ' + str(target_psize) + ' micro meter'
    
    meta_img = tiff.imwrite(os.path.join(outpath,name), np.asarray(resized_im), description=new_meta)

