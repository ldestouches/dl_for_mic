#---------------------------------------------------------------------------------------------
# Function to get image pixel per meter (ppm)
#---------------------------------------------------------------------------------------------

# This function outputs the pixel size of a microscopy image from its metadata.

# The metadata comes from when the image was acquired with the microscope and is based on calibration.
# This function tries to find the information in the metadata, first for the Nikon metadata format, then
# for the ZEISS metadata format. If it does not find the information in metadata, the function will
# ask you to input the value of pixel size. The value of pixel size will come from your own empirical knowledge.

from get_metadata_zeiss_SIMpsize import *

def get_image_psize_corr(image):
    
    ori_psize = 0
    
    # For NIKON
    try:
        metadata = image.metaseries_metadata
        ori_psize = metadata['PlaneInfo']['spatial-calibration-x']
    except:
        print('not Nikon metadata')
    else:
        print('This image is from NIKON', 'and the pixel size is: ', ori_psize, 'microm')
    
    # For ZEISS
    if ori_psize == 0:
        try:
            ori_psize = get_metadata_zeiss_SIMpsize(image)
            print('This image is from ZEISS', 'and the pixel size is: ', ori_psize, 'microm')
        except:
            print('not ZEISS metadata')
    
    # For internally-produced metadata
    if ori_psize == 0:
        try:
            metadata = image.pages[0].tags["ImageDescription"].value.split(' ')[2]
        except:
            print('not internally-produced metadata')
            print('Original pixel size NOT FOUND for: ', image)
        else:
            ori_psize = metadata
            print('This images metadata was internally-produced', 'and the pixel size is: ', ori_psize, 'microm')
            
    
    # For no metadata
    if ori_psize == 0:
        print('No metadata provided, input pixel size in micrometer: ')
        ori_psize = float(input())
        print('The image pixel size is: ', ori_psize, 'microm')
    else:
        pass
        
    return ori_psize