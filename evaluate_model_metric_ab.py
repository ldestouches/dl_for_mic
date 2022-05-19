# -*- coding: utf-8 -*-
"""
Created on Wed May 18 09:56:54 2022

@author: ldestouches
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:14:53 2022

@author: ldestouches
"""

# ------------------------------------------------------------------
# EVALUATING MODEL METRICS
# ------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.close('all')

path_quality_control_stardist = "C:/Users/ldestouches/Documents/SOFTWARE/FINAL_models/StarDist_GM_FINAL/Quality Control/Quality_Control for StarDist_GM_FINAL.csv"
path_quality_control_cellpose = "C:/Users/ldestouches/Documents/SOFTWARE/FINAL_models/Cellpose_GM_FINAL/Quality Control/Quality_Control for Cellpose_GM_FINAL.csv"
# see also here: https://stackoverflow.com/questions/51027717/pyplot-bar-charts-with-individual-data-points

# quality control data frame

files = [path_quality_control_stardist, path_quality_control_cellpose]
colors = ['r', 'c']
labels = ['StarDist', 'Cellpose']

metrics_names = ['Prediction v. GT Intersection over Union', 'precision', 
                 'recall', 'accuracy']
metrics_names_display = ['IoU', 'precision', 'recall', 'accuracy']

fig = plt.subplots(figsize = (12,8))
barWidth = 0.25

# plots the bars
for j, file in enumerate(files):
    averages_file = list()
    xbar = np.arange(len(metrics_names))+j*barWidth
    
    for k, mn in enumerate(metrics_names):
        qc_df = pd.read_csv(file)
        values = qc_df[mn].values
        averages_file.append( np.mean(values) )
    plt.bar(xbar, averages_file, color = (0,0,0,0), width = barWidth, edgecolor =  colors[j], 
            label = labels[j])

# plots individual points
for j, file in enumerate(files):
    # scatter values contains pairs of (x,y) points
    scatter_values = [[],[]]
    xbar = np.arange(len(metrics_names))+j*barWidth
    
    for k, mn in enumerate(metrics_names):
        qc_df = pd.read_csv(file)
        values = qc_df[mn].values
        
        scatter_values[0].extend( list(np.ones(len(values))*xbar[k]))
        scatter_values[1].extend(values)
        for jj in range(len(values)):
            # add label to legend only the first time: for first file and first metric
            lab=None
            if j==0 and k==0:
                lab = "repetition {}".format(jj+1)
            plt.scatter(xbar[k],values[jj], color="C{}".format(jj),label=lab)
        #plt.scatter(scatter_values[0],scatter_values[1], color="C0")
plt.legend()
plt.title('Comparison of Model Performance')
plt.xticks([r + barWidth for r in range(len(metrics_names))], metrics_names_display)

