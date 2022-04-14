# --------------------------------------------------------------------------
# Width and Length of ROI
# --------------------------------------------------------------------------

# This function takes the csv file acquired from the ROI manager and ROI_measure plugin on an annotated image
# Each individual bacteria has it's length and width measured.

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# csv file for Control and treated with Antibiotic
ctrl = pd.read_csv('roimeasure_results_Ann_Cyclo_190220_stage1_01.csv')
antib = pd.read_csv('roimeasure_results_Ann_Cyclo_190220_stage9_80.csv')

# Control 
ctrl_length = ctrl.Roi_Length.to_list()
ctrl_width = ctrl.Roi_Width.to_list()

# Antibiotic
antib_length = antib.Roi_Length.to_list()
antib_width = antib.Roi_Width.to_list()


# Plotting LENGTH

#scatterplot
plt.scatter(range(len(ctrl_length)), ctrl_length, label='control', color='green')
plt.scatter(range(len(antib_length)), antib_length, label='antibiotic', color='red')
plt.legend()
plt.title('Length per ROI')
plt.show()

#boxplot
lengths = [ctrl_length,antib_length]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(lengths)
plt.xticks([1,2],['control','antibiotics'])
plt.title('ROI Length Boxplot')
plt.show()


# Plotting WIDTH

#scatterplot
plt.scatter(range(len(ctrl_width)), ctrl_width, label='control', color='green')
plt.scatter(range(len(antib_width)), antib_width, label='antibiotic', color='red')
plt.legend()
plt.title('Width per ROI')
plt.show()

#boxplot
widths = [ctrl_width, antib_width]
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
bp = ax.boxplot(widths)
plt.xticks([1,2],['control','antibiotics'])
plt.title('ROI Width Boxplot')
plt.show()



# The yvalues correspond to number of pixels pixel size of 0.0645 microm

