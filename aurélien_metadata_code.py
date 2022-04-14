import json
import numpy
import tifffile  # http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html

# stolen here: https://stackoverflow.com/questions/20529187/what-is-the-best-way-to-save-image-metadata-alongside-a-tif

#generates mock data and metadata
data = numpy.arange(256).reshape((16, 16)).astype('u1')

metadata = dict(microscope='zeiss', shape=data.shape, dtype=data.dtype.str, pixel_size= 0.12,pixel_size_unit="um")
print(data.shape, data.dtype, metadata['microscope'])

# saves
metadata = json.dumps(metadata) # this outputs your info as a string
tifffile.imwrite('microscope.tif', data, description=metadata)

# loads
tif = tifffile.TiffFile('microscope.tif')    
output_metadata = tif.pages[0].tags["ImageDescription"].value
print(output_metadata)