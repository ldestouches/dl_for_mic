# Resizing images using pillow

# For NIKON

from PIL import Image
import tifffile as tiff

img_path = 'C:/Users/ldestouches/Documents/IMAGES/All microscope images/Dimitri_Nikon_back cross/190904 delta pos rep 1/mgso4/1.tif'
img_PIL = Image.open(img_path) # imported with PIL
img_tif = tiff.TiffFile(img_path) # imported with tifffile

# Read metadata using tifffile
metadata = img_tif.metaseries_metadata

# General info about img
print(' The img format is: ', img_PIL.format, \
      '\n The mode of img is: ', img_PIL.mode, \
      '\n The size (width, height) of img is: ', img_PIL.size)

# Pixel size info
ori_pixel = metadata['PlaneInfo']['spatial-calibration-x']
print('\n The img pixel size is: ', ori_pixel)

# Desired pixel size
target_pixel = 0.128 # =128nm
x = target_pixel / ori_pixel

# Pixel size to image dimensions
w = img_PIL.size[0] # original width
h = img_PIL.size[1] # original height
W = int(w / x) # desired W
H = int(h / x) # desired H
# turning our values to integers for the resizing
print('\n We want to resize our img to these dimensions: ', W, H)

# Resizing img
resized_img = img_PIL.resize((W,H))
print('\n The size of the resized img is: ', resized_img.size)

# Save image
resized_img = resized_img.save('resized.tif')



'''
# Adding new info in metadata
new_metadata = metadata.copy()
new_metadata['PlaneInfo']['spatial-calibration-x'] = new_metadata['PlaneInfo']['spatial-calibration-x'] * x
# print(new_metadata['PlaneInfo']['spatial-calibration-x'])

# Save new metadata to image
resized_withmeta = tiff.imsave('resized_withmeta.tif', resized_img, description=new_metadata)
'''
