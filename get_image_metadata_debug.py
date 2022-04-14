
import tifffile

path = "C:/Users/ldestouches/Documents/IMAGES/Testcode/Image 3.tif"
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

meta_dict['Experiment|AcquisitionBlock|AcquisitionModeSetup|ScalingX']
