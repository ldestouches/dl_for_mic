# --------------------------------------------------------------------------
# Width and Length of ROI
# --------------------------------------------------------------------------

# This function takes the csv file acquired from the ROI manager and ROI_measure plugin on an annotated image
# Each individual bacteria has it's length and width measured.

# install dependencies
import matplotlib.pyplot as plt
import pandas as pd

# csv file from image treated with Antibiotic (Cyclosérine)
ann = pd.read_csv('roimeasure_results_Ann_Cyclo_190220_stage9_80.csv')
stardist = pd.read_csv('roimeasure_results_StarDist_Cyclo_190220_stage9_80.csv')
cellpose = pd.read_csv('roimeasure_results_Cellpose_Cyclo_190220_stage9_80.csv')

# Annotations
ann_length = ann.Roi_Length.to_list()
ann_width = ann.Roi_Width.to_list()

# StarDist
stardist_length = stardist.Roi_Length.to_list()
stardist_width = stardist.Roi_Width.to_list()

# Cellpose
cellpose_length = cellpose.Roi_Length.to_list()
cellpose_width = cellpose.Roi_Width.to_list()


# Plotting LENGTH

#scatterplot
plt.scatter(range(len(ann_length)), ann_length, label='ann', color='green')
plt.scatter(range(len(stardist_length)), stardist_length, label='stardist', color='red')
plt.scatter(range(len(cellpose_length)), cellpose_length, label='cellpose', color='yellow')
plt.legend()
plt.title('Length per ROI')
plt.show()

#boxplot
lengths = [ann_length,stardist_length,cellpose_length]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(lengths)
plt.xticks([1,2,3],['ann','stardist','cellpose'])
plt.title('ROI Length Boxplot')
plt.show()


# Plotting WIDTH

#scatterplot
plt.scatter(range(len(ann_width)), ann_width, label='ann', color='green')
plt.scatter(range(len(stardist_width)), stardist_width, label='stardist', color='red')
plt.scatter(range(len(cellpose_width)), cellpose_width, label='cellpose', color='yellow')
plt.legend()
plt.title('Width per ROI')
plt.show()

#boxplot
widths = [ann_width, stardist_width, cellpose_width]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(widths)
plt.xticks([1,2,3],['ann','stardist','cellpose'])
plt.title('ROI Width Boxplot')
plt.show()

# The yvalues correspond to number of pixels pixel size of 0.0645 microm

