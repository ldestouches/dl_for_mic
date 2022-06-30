# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 15:46:09 2022

@author: ldestouches
"""

# -----------------------------------------------------------------------------
# PRE-PROCESSING FOR SEGMENTATION MODELS
# -----------------------------------------------------------------------------

# Imports
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import os
from PIL import Image

# PATHS

# Enter path to the raw fluorescent sequence
TL_raw_folder = r"C:/Users/ldestouches/Documents/PAPER 2/RAW SEQUENCES"
# Enter path to the folder where you want to save your treated sequences
preprocessing_folder = r"C:/Users/ldestouches/Documents/PAPER 2/PRE-PROCESSED SEQUENCES/"

# INPUT VALUES

# write the step of timeframes you want. For example, I want to select every 15th image of the sequence
step = 15
# write the original pixel size of the raw images
ori_psize = 0.0645


# FUNCTIONS

# Resizing function:
def resize_psize(image_PIL, ori_psize, target_psize):
    
    #ori_psize = get_image_psize(image_tiff)
    x = target_psize / ori_psize
    
    # find original image dimensions
    w, h = image_PIL.size[0], image_PIL.size[1] # original width and height
    print('the original image size is: ', image_PIL.size)
    W, H = int(w / x), int(h / x) # desired width and height

    # Resizing img
    resized_img = image_PIL.resize((W,H))
    print('The size of the resized img is: ', resized_img.size)

    # Show image
    plt.figure()
    plt.subplot(121)
    plt.imshow(image_PIL)
    plt.subplot(122)
    plt.imshow(resized_img)
    
    # return resized image
    return resized_img

for folder in os.listdir(TL_raw_folder):
    
    print("processing folder: ", folder)
    tl_dir = os.path.join(TL_raw_folder,folder) 

#####     STEP 1 - Select timeframes
    
    # creating a outpath folder to store selected images
    sel_folder_name = folder.split('_rawseq')[0] + '_selseq'    
    sel_folder_path = os.path.join(preprocessing_folder,sel_folder_name)
    os.mkdir(sel_folder_path)
    
    for count, file in enumerate(os.listdir(tl_dir)):
    
        if count % step == 0:
            
            # showing you the selected images
            im_path = os.path.join(tl_dir,file)
            im = tiff.imread(im_path)
            plt.figure()
            plt.imshow(im, cmap = 'gray')
            plt.title(file)
            
            # giving the selected image their original name with '_sel' at the end
            sel_name = file.split('.tif')[0] + '_sel.tif'
            
            im_outpath = os.path.join(sel_folder_path,sel_name)
            print('im_outpath',im_outpath)
            
            tiff.imsave(im_outpath, np.asarray(im))


#####     STEP 2 - Resize images to 0.100 micrometer per pixel
    
    # creating an outpath folder to store the resized images
    resized_folder_name = sel_folder_name + '_resized'
    resized_folder_path = os.path.join(preprocessing_folder, resized_folder_name)
    os.mkdir(resized_folder_path)
    
    # target pixel size is 0.100 for our segmentation model
    target_psize = 0.100
    
    for file in os.listdir(sel_folder_path):
        
        im_path = os.path.join(sel_folder_path, file)
        im = Image.open(im_path) # opening the image using PIL for the resizing function in this library
        resized_im = resize_psize(im, ori_psize, target_psize)
        
        resized_name = file.split('.tif')[0] + '_resized.tif'
        im_outpath = os.path.join(resized_folder_path, resized_name)
        
        new_meta = 'Pixel size: ' + str(target_psize) + ' micro meter' # adding the new pixel size to the metadata of the image
        tiff.imwrite(im_outpath, np.asarray(resized_im), description=new_meta) # saving the im using TIFF library

























