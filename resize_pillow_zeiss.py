
#---------------------------------------------------------------------------------------------------
# RESIZING IMAGES FROM ZEISS MICROSCOPE
#---------------------------------------------------------------------------------------------------

# Resizing images using pillow

# For ZEISS

from PIL import Image
import tifffile as tiff
import matplotlib.pyplot as plt

path = 'P:/microscopy/ZEISS/Louise/Aurelien/2022_02_15/Image 27.tif'
img_PIL = Image.open(path) # imported with PIL
img_tif = tiff.TiffFile(path) # imported with tifffile


# Function to acquire metadata
def get_image_metadata(image):
    meta_dict = image.imagej_metadata
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

# Open metadata on a Zeiss image
path = "P:/microscopy/ZEISS/Louise/Aurelien/2022_02_15/Image 27.tif"
metadata = get_image_metadata(img_tif)


# How to extract pixel size on a Zeiss image

if 'Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX #1' in metadata:
    xscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX #1']*10**6
    yscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingY #1']*10**6
else:
    xscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX']*10**6
    yscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingY']*10**6
# this is because either #1 or not - in our expample not

# Original ppm
ori_ppm = xscale
print('The image ppm is: ', ori_ppm, 'microm')


# General info about img
print(' The img format is: ', img_PIL.format, \
      '\n The mode of img is: ', img_PIL.mode, \
      '\n The size (width, height) of img is: ', img_PIL.size)

# Desired pixel size
target_ppm = 0.128 # =128nm
x = target_ppm / ori_ppm

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
resized_img = resized_img.save('resized_zeiss.tif')

