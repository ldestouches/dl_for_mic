# -*- coding: utf-8 -*-
"""
Created on Wed May 18 16:28:08 2022

@author: ldestouches
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 13 16:48:38 2022

@author: aurelienb
"""

import cellpose
import stardist

from stardist.models import StarDist2D
from cellpose import models
from tifffile import imread
import glob
import matplotlib.pyplot as plt
import numpy as np
from csbdeep.utils import Path, normalize

from PIL import Image
plt.close('all')
QC_model_path = """C:/Users/ldestouches/Documents/SOFTWARE/FINAL_models/Cellpose_GM_FINAL/cellpose_residual_on_style_on_concatenation_off_train_folder_2022_05_18_13_33_18.490485"""

# -------- cellpose ---------------

path_images = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ANTIBIO/reworked TL/resized/resized_ctrl/13-02-20_Stage30036.tif"
images = glob.glob(path_images+'*.tif')
images = [imread(w) for w in images]
channels=[[0,0]]

model = models.CellposeModel(gpu=False, pretrained_model=QC_model_path,
                             diam_mean=30.0, net_avg=True, device=None, 
                             residual_on=True, style_on=True, concatenation=False)

out = model.eval(images, diameter=None, channels=channels)

# masks, flows, styles, diams

masks, flows, styles = out

n0 = 0

mask = masks[n0].astype(float)

proba = flows[n0][2]

mask[mask==0]=np.nan

plt.figure()
plt.subplot(131)
plt.imshow(images[n0])
plt.subplot(132)
plt.imshow(mask%20,cmap="tab20")
plt.subplot(133)
plt.imshow(proba, cmap = "RdYlGn")
plt.title('probability map')
plt.colorbar()
plt.suptitle('Cellpose')

# ------- Stardist ---------

path_model_stardist = r"C:\Users\ldestouches\Documents\SOFTWARE\FINAL_models"
model_sd = StarDist2D(None,name="StarDist_GM_FINAL",basedir = path_model_stardist)

out_sd = model_sd.predict_instances(normalize(images[n0],pmin=0,pmax=99.8), return_predict = True)
labels, polygons = out_sd[0]
proba_sd = out_sd[1][0]

labels = labels.astype(float)

labels[labels==0]=np.nan


fig,axes = plt.subplots(1,3, sharex=True,sharey=True)

axes[0].imshow(images[n0])

axes[1].imshow(labels%20,cmap="tab20")

proba_reshaped = np.array(Image.fromarray(proba_sd).resize(images[n0].shape[::-1]))
axes[2].imshow(np.array(proba_reshaped), cmap = "RdYlGn")
axes[2].set_title('probability map')
