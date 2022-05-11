#---------------------------------------------------------------------------------------------
# Function to resize the pixel size
#---------------------------------------------------------------------------------------------

# https://appdividend.com/2020/06/19/how-to-resize-image-in-python-using-pillow-example/
# This function resize the original pixel size to a target pixel size chosen in the main command center.
# The image needs to be imported with pillow.
# the ori_psize is the output from the get_image_psize function.
# target_psize can be modified from the main command center

import matplotlib.pyplot as plt
from get_image_psize import *

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
    plt.show()
    
    # return resized image
    return resized_img

