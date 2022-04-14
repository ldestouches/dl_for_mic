#---------------------------------------------------------------------------------------------
# Function to add pixel size to image metadata
#---------------------------------------------------------------------------------------------

# This function adds metadata to tif image in a new file.
'''
import tifffile as tiff

def new_metadata(image_tif, psize, name):
    
    name = name.split('.tif')[0] + '_meta' + '.tif'
    
    new_meta = 'Pixel size: ' + str(psize) + ' micro meter' # this is what goes in the description
    tiff.imsave(name, image_tif, description=new_meta)
    
    print('\n Your image was saved with new metadata as: ' + name)
    
    return

'''
import tifffile as tiff
import numpy as np

def new_metadata(image, psize, name):
    
    name = name.split('.tif')[0].split('_resized')[0].split('_mask')[0] + '.tif'
    
    new_meta = 'Pixel size: ' + str(psize) + ' micro meter' # this is what goes in the description
    
    meta_img = tiff.imwrite(name, np.asarray(image), description=new_meta)
    
    return meta_img


'''
def new_metadata_ij(image_tif, psize, name): # doesn't work yet
    ijinfo = {"Plane Info": [{"spatial-calibration-x": "0.100"}]}
    ijmetadata = json.dumps(ijinfo)
    name = name.split('.tif')[0] + '_metadata' + '.tif'
    tiff.imsave(name, image_tif, description=ijmetadata)
    print('\n Your image was saved as: ' + name)
    return

# Copying old metadata in new metadata with pixel value changed
new_metadata = metadata.copy()
new_metadata['PlaneInfo']['spatial-calibration-x'] = new_metadata['PlaneInfo']['spatial-calibration-x'] * x
print(new_metadata)

'''
