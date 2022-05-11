# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:01:30 2022

@author: ldestouches
"""


import pandas as pd
import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np

import cv2

im_path_1 = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_064/Masks/Cyclo_190220_stage5_20_5.tif"
im_path_2 = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_064/Masks/Cyclo_271120_Position18_20_18.tif"
im_path_3 = "C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_064/Masks/Exp2_Field1-10000.tif"


# function for python rectangles for code measurements
def get_widthlength_rect(msk, plot=False):
    """Gets the length of a mask using minarea rectangle"""
    mask = msk.copy()
    mask = mask.astype(np.uint8)
    if np.count_nonzero(mask)<2:
        return 0
    cnt,hierarchy = cv2.findContours(mask, 1, 2)
    cnt = np.vstack(cnt).squeeze()
    
    # returns the min area rectangle: ( (x_centre, y_centre), (x_size, y_size), rotation_angle )
    rect = cv2.minAreaRect(cnt)
    if plot:
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        
        # converts image to BGR (=3 color channels) for display purpose
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(mask,[box],0,(0,0,255),1)
        cv2.imshow("mask and approximation",mask)
    return min(rect[1]),max(rect[1])

im_1 = tiff.imread(im_path_1)
im_2 = tiff.imread(im_path_2)
im_3 = tiff.imread(im_path_3)

# show randomly selected images
plt.figure()
plt.imshow(im_1, cmap = 'gray')
plt.title('image 1')
plt.figure()
plt.imshow(im_2, cmap = 'gray')
plt.title('image 2')
plt.figure()
plt.imshow(im_3, cmap = 'gray')
plt.title('image 3')

# number of labels in image
nlabel_1 = np.unique(im_1).size - 1
nlabel_2 = np.unique(im_2).size - 1
nlabel_3 = np.unique(im_3).size - 1

# randomly selected labels to measure
rand_label_no_1 = [18,20,31,33,45]
rand_label_no_2 = [29,32,34,39,53]
rand_label_no_3 = [1,2,3,4,6]

# ---------------------------
# CODE MEASUREMENTS

code_l = []
code_w = []

# loop for im_1
for i in range(nlabel_1):
    for j in range(len(rand_label_no_1)):
        if i == rand_label_no_1[j]:
            
            onebac = im_1==i
            widthbac, lengthbac = get_widthlength_rect(onebac)
            print('bacteria with label {} has code-measured length of {:.2f}'.format(
                i, lengthbac))
            print('bacteria with label {} has code-measured width of {:.2f}'.format(
                i, widthbac))
            
            code_l.append(lengthbac)
            code_w.append(widthbac)
            
            plt.figure()
            plt.imshow(onebac)
            plt.title('im 1 mask label '+str(i))

print(code_l,'\n',code_w)

# loop for im 2
for i in range(nlabel_2):
    for j in range(len(rand_label_no_2)):
        if i == rand_label_no_2[j]:
            
            onebac = im_2==i
            widthbac, lengthbac = get_widthlength_rect(onebac)
            print('bacteria with label {} has code-measured length of {:.2f}'.format(
                i, lengthbac))
            print('bacteria with label {} has code-measured width of {:.2f}'.format(
                i, widthbac))
            
            code_l.append(lengthbac)
            code_w.append(widthbac)
            
            plt.figure()
            plt.imshow(onebac)
            plt.title('im 2 mask label '+str(i))

print(code_l,'\n',code_w)

# loop for im 3
for i in range(nlabel_3):
    for j in range(len(rand_label_no_3)):
        if i == rand_label_no_3[j]:
            
            onebac = im_3==i
            widthbac, lengthbac = get_widthlength_rect(onebac)
            print('bacteria with label {} has code-measured length of {:.2f}'.format(
                i, lengthbac))
            print('bacteria with label {} has code-measured width of {:.2f}'.format(
                i, widthbac))
            
            code_l.append(lengthbac)
            code_w.append(widthbac)
            
            plt.figure()
            plt.imshow(onebac)
            plt.title('im 3 label '+str(i))

print(code_l,'\n',code_w)

# -----------------------
# MANUAL MEASUREMENTS

# all manual measures go in these lists
manual_l = []
manual_w = []

df_1 = pd.read_csv("C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_064/manual measures/cyclo19st520_randmaskmeasures_lengthwidth.csv")
df_2 = pd.read_csv("C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_064/manual measures/cyclo27pos1820_randmaskmeasures_lengthwidth.csv")
df_3 = pd.read_csv("C:/Users/ldestouches/Documents/IMAGES & TIMELAPSES/ML_GM_064/manual measures/exp2f100_randmaskmeasures_lengthwidth.csv")

# converting csv to list
#label_no_1 = df_1["Median"].tolist()
measures_1 = df_1["Length"].tolist()
measures_2 = df_2["Length"].tolist()
measures_3 = df_3["Length"].tolist()

for i in range (len(measures_1)):
    if i % 2 == 0:
        manual_l.append(measures_1[i])
    else:
        manual_w.append(measures_1[i])        
print(df_1)
print(manual_l,manual_w)

for i in range (len(measures_2)):
    if i % 2 == 0:
        manual_l.append(measures_2[i])
    else:
        manual_w.append(measures_2[i])        
print(df_2)
print(manual_l,manual_w)

for i in range (len(measures_3)):
    if i % 2 == 0:
        manual_l.append(measures_3[i])
    else:
        manual_w.append(measures_3[i])        
print(df_3)
print(manual_l,manual_w)

# ------------------------
# TRUE VALUES
# making values into true values converted from pixel lengths

code_l_tv = code_l 
code_w_tv = code_w
manual_l_tv = manual_l 
manual_w_tv = manual_w

for i in range(len(code_l_tv)):
    code_l_tv[i] = code_l_tv[i] *0.0645
    code_w_tv[i] = code_w_tv[i] *0.0645
    if i < 10:
        manual_l_tv[i] = manual_l_tv[i] *0.0645
        manual_w_tv[i] = manual_w_tv[i] *0.0645
    
print('length and width true values in micrometers for code measures: \n', code_l_tv, '\n', code_w_tv)
print('length and width true values in micrometers for manual measures: \n', manual_l_tv, '\n', manual_w_tv)

# plot

x1,x2 = [3,10], [0.65,1.2]
y1,y2 = x1,x2

plt.figure()
plt.plot(code_l_tv,manual_l_tv,'o')
plt.plot(x1,y1,'--')
plt.title('lengths measured by code and manually for given bacteria')
plt.xlabel('code lengths in micrometer')
plt.ylabel('manual lengths in micrometer')

plt.figure()
plt.plot(code_w_tv,manual_w_tv,'o')
plt.plot(x2,y2,'--')
plt.title('widths measured by code and manually for given bacteria')
plt.xlabel('code widths in micrometer')
plt.ylabel('manual widths in micrometer')

