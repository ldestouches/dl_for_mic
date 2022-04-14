#---------------------------------------------------------------------------------------------
# MAIN Command Center
#---------------------------------------------------------------------------------------------

# WARNING this code is probably obsolete

from PIL import Image
import os
import tifffile as tiff
import numpy as np
from get_image_psize import *
from resize_psize import *

# Choose the target pixel size for resizing:
target_psize = 0.100

# Resizing for 1 isolated image
'''
img_path = 'C:/Users/ldestouches/Documents/SOFTWARE/Python/resizeimage/treated images 2/Car_SIM/220210_RCL273_NileRed_BeforeFixation_01_LSIM561_P561_010_Texp050ms_SIM-1.tif'
img_tif = tiff.TiffFile(img_path) # imported with tifffile for get_psize
img_PIL = Image.open(img_path) # imported with PIL for resize_psize


# General info about img
print(' The img format is: ', img_PIL.format, \
      '\n The mode of img is: ', img_PIL.mode, \
      '\n The size (width, height) of img is: ', img_PIL.size)

# Acquire the original pixel size of your image:
ori_psize = get_image_psize(img_tif)

# Resizing
# The image argument must originate from the PIL import
resized_img = resize_psize(img_PIL, ori_psize, target_psize)

# Save resized image
name_resized = img_path.split('/')[-1].split('.tif')[0] + '_resized' + '.tif' # keep original name + '_resized'
resized_img.save(name_resized)

# Save new metadata
new_metadata(resized_img, target_psize, name_resized)
'''