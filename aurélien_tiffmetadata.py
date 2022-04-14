#@@ -0,0 +1,49 @@
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 10:28:14 2022

@author: aurelien
"""
import tifffile

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


# Example: Open metadata on a Zeiss image
path = "C:/Users/ldestouches/Documents/IMAGES/All microscope images/Charlène/Timelapse/timelapsefluosequence_stage1/stage1-10000.tif"

metadata = get_image_metadata(path)

# How to extract pixel size on a Zeiss image
dt = metadata['finterval']
if 'Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX #1' in metadata:
    xscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX #1']*10**6
    yscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingY #1']*10**6
else:
    xscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX']*10**6
    yscale = metadata['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingY']*10**6
    
'''    
# On a Nikon image file:
path_nikon = "C:/Users/ldestouches/Documents/IMAGES/All microscope images/Charlène/images/CCBS349_1_561.tif"
img = tifffile.TiffFile(path_nikon)
metadata = img.metaseries_metadata
'''