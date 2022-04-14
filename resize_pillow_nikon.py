# Resizing images using pillow


#---------------------------------------------------------------------------------------------------
# RESIZING IMAGES FROM NIKON MICROSCOPE
#---------------------------------------------------------------------------------------------------

# For NIKON

from PIL import Image
import tifffile as tiff
import matplotlib.pyplot as plt

img_path = 'C:/Users/ldestouches/Documents/IMAGES/All microscope images/Charlène/images/CCBS349_1_561.tif'
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
W = int(w / x) # desired width
H = int(h / x) # desired height
# turning our values to integers for the resizing
print('\n We want to resize our img to these dimensions: ', W, H)

# Resizing img
resized_img = img_PIL.resize((W,H))
print('\n The size of the resized img is: ', resized_img.size)

# Show image
plt.figure()
plt.subplot(121)
plt.imshow(img_PIL)
plt.subplot(122)
plt.imshow(resized_img)
plt.show()

# Save image
resized_img.save('resized.tif')

