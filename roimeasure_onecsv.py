# --------------------------------------------------------------------------
# Width and Length of ROI
# --------------------------------------------------------------------------

# This function takes the csv file acquired from the ROI manager and ROI_measure plugin on an annotated image
# Each individual bacteria has it's length and width measured.


# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# csv file
df = pd.read_csv('roimeasure_results_csv.csv',sep=',')

roi_index = df[[' ']]
roi_length = df[['Roi_Length']]
roi_width = df[['Roi_Width']]


# Plotting Length

plt.scatter(roi_index,roi_length)
plt.title('Length per Roi')
plt.show()

plt.boxplot(roi_length)
plt.title('Roi Length Boxplot')
plt.show()

# Plotting Width

plt.scatter(roi_index,roi_width)
plt.title('Width per Roi')
plt.show()

plt.boxplot(roi_width)
plt.title('Roi Width Boxplot')
plt.show()

