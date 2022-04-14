#@@ -0,0 +1,49 @@
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:28:14 2022

@author: aurelien
"""
import tifffile

'''
def get_image_metadata(path):
    img = tifffile.TiffFile(path)
    meta_dict = img.imagej_metadata
    description = meta_dict.pop('Info')
    description = description.split('\n')
    for d in description:
        if len(d)>1 and '=' in d:
            oo = d.split('=')
            if len(oo)==2:
                k, val = oo
            elif len(oo)>2:
                k = oo[0]
                val = "=".join(oo[1:])
            k = k.strip(' ')
            val = val.strip(' ')
            try:
                meta_dict[k] = float(val)
            except:
                meta_dict[k] = val
    return meta_dict
'''
# On a Nikon image file:
path_nikon = "C:/Users/ldestouches/Documents/IMAGES/All microscope images/Charlène/images/CCBS349_1_561.tif"
img = tifffile.TiffFile(path_nikon)
metadata = img.metaseries_metadata

get_image_metadata(path_nikon)


# Resize pixels

def resize_image():
    #get_image_metadata(path_nikon)
    ori_pixel = metadata['PlaneInfo']['spatial-calibration-x']
    target_pixel = 0.128 # =128nm
    x = target_pixel / ori_pixel
    new_pixel = ori_pixel * x # new value of pixels
    
    for i in metadata:
        for j in i:
            if j == 'spatial-calibration-x':
                j = new_pixel
            else:
                pass
            
    return metadata

resize_image()
