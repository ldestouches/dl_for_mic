# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:14:53 2022

@author: ldestouches
"""

# ------------------------------------------------------------------
# EVALUATING MODEL METRICS
# ------------------------------------------------------------------

import pandas as pd
import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np

import cv2

# here I import csv metrics from the quality control files and compare their values between different models

#♠ QUALITY CONTROL

qc_stardist = pd.read_csv("C:/Users/ldestouches/Documents/SOFTWARE/StarDist/StarDist_GM100_selval/Quality Control/Quality_Control for StarDist_GM100_selval.csv")
qc_splinedist = pd.read_csv("C:/Users/ldestouches/Documents/SOFTWARE/SplineDist/SplineDist_GM_100_selval/Quality Control/Quality_Control for SplineDist_GM_100_selval.csv")
qc_cellpose = pd.read_csv("C:/Users/ldestouches/Documents/SOFTWARE/Cellpose/Cellpose_GM_selval2im/Quality Control/Quality_Control for Cellpose_GM_selval2im.csv")

# AVERAGE FUNCTION
def average(metriclist):
    sumlist = sum(metriclist)
    lengthlist = len(metriclist)
    average = sumlist/lengthlist
    return average

#-----------------------------------------------------------------

# IOU

iou_stardist = qc_stardist['Prediction v. GT Intersection over Union'].tolist()
iou_splinedist = qc_splinedist['Prediction v. GT Intersection over Union'].tolist()
iou_cellpose = qc_cellpose['Prediction v. GT Intersection over Union'].tolist()
print("IoU:",iou_stardist, iou_splinedist, iou_cellpose)

iou_models = ["iou_stardist","iou_splinedist","iou_cellpose"]
iou_values = [iou_stardist, iou_splinedist, iou_cellpose]

iou_stardist_average = average(iou_stardist)
iou_splinedist_average = average(iou_splinedist)
iou_cellpose_average = average(iou_cellpose)

# --------------------------------------------------------------

# PRECISION

precision_stardist = qc_stardist['precision'].tolist()
precision_splinedist = qc_splinedist['precision'].tolist()
precision_cellpose = qc_cellpose['precision'].tolist()
print("precision:", precision_stardist, precision_splinedist, precision_cellpose)

precision_stardist_average = average(precision_stardist)
precision_splinedist_average = average(precision_splinedist)
precision_cellpose_average = average(precision_cellpose)


# --------------------------------------------------------------

# RECALL

recall_stardist = qc_stardist['recall'].tolist()
recall_splinedist = qc_splinedist['recall'].tolist()
recall_cellpose = qc_cellpose['recall'].tolist()
print("recall:", recall_stardist, recall_splinedist, recall_cellpose)

recall_stardist_average = average(recall_stardist)
recall_splinedist_average = average(recall_splinedist)
recall_cellpose_average = average(recall_cellpose)

# --------------------------------------------------------------

# ACCURACY

accuracy_stardist = qc_stardist['accuracy'].tolist()
accuracy_splinedist = qc_splinedist['accuracy'].tolist()
accuracy_cellpose = qc_cellpose['accuracy'].tolist()
print("accuracy:", accuracy_stardist, accuracy_splinedist, accuracy_cellpose)

accuracy_stardist_average = average(accuracy_stardist)
accuracy_splinedist_average = average(accuracy_splinedist)
accuracy_cellpose_average = average(accuracy_cellpose)

# --------------------------------------------------------------

# F1-SCORE


f1score_stardist = qc_stardist['f1 score'].tolist()
f1score_splinedist = qc_splinedist['f1 score'].tolist()
f1score_cellpose = qc_cellpose['f1 score'].tolist()
print("f1score:", f1score_stardist, f1score_splinedist, f1score_cellpose)

f1score_stardist_average = average(f1score_stardist)
f1score_splinedist_average = average(f1score_splinedist)
f1score_cellpose_average = average(f1score_cellpose)


# --------------------------------------------------------------
# PLOT

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize = (12,8))

# set height of bar
stardist_metrics = [iou_stardist_average, precision_stardist_average, recall_stardist_average,
                    accuracy_stardist_average, f1score_stardist_average]
splinedist_metrics = [iou_splinedist_average, precision_splinedist_average, recall_splinedist_average,
                      accuracy_splinedist_average, f1score_splinedist_average]
cellpose_metrics = [iou_cellpose_average, precision_cellpose_average, recall_cellpose_average,
                    accuracy_cellpose_average, f1score_cellpose_average]

# set position of bar on x-axis
br1 = np.arange(len(stardist_metrics))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make boxplot
plt.bar(br1, stardist_metrics, color = 'r', width = barWidth, edgecolor = 'grey', label = 'Stardist')
plt.bar(br2, splinedist_metrics, color = 'c', width = barWidth, edgecolor = 'grey', label = 'Splinedist')
plt.bar(br3, cellpose_metrics, color = 'm', width = barWidth, edgecolor = 'grey', label = 'Cellpose')

# Adding Xticks
plt.xticks([r + barWidth for r in range(len(stardist_metrics))],['IoU', 'precision', 'recall', 'accuracy', 'f1 score'])

plt.title('performance metrics for segmentation models', fontweight = 'bold', fontsize = 15)
plt.ylabel('score', fontsize = 12)
plt.xlabel('quality metrics', fontsize = 12)
plt.legend()
plt.show()

