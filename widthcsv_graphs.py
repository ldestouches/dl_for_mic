# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 12:21:37 2022

@author: ldestouches
"""

# Import CSV from the width_for_timelapse_csvexport code
# Use it to make graphs

import numpy as np
import matplotlib.pyplot as plt

import os
import pandas as pd


# function to create variables from csv files
def antibcsv_tolists(csvpath, timepoints):
   widthslist = list()
   nlist = list()
   
   for i in range(len(timepoints)):
       cleanlist = csvpath[timepoints[i]].dropna().tolist()
       widthslist.append(cleanlist)
       n = len(cleanlist)
       nlist.append(n)

   return widthslist, nlist

# Select folder with the csv files in it
csv_folder = "C:/Users/ldestouches/Documents/PAPER 2/CSV"


antib_names = list()  # where the names of the antibiotics will be stored in order
all_widths = list() # where the widths taken from the csv files will be stored
all_nlabels = list() # where the number of bacteria per frame will be stored

colors = ['darkgreen','darkblue','green','grey','pink'] # colors assigned to each antibiotic

# try and loop through csv files in folder to create 
for file in os.listdir(csv_folder):
    
    antibname = file.split('.csv')[0]
    print("Treating: ", antibname)
    antib_names.append(antibname)
    
    antib_csv = pd.read_csv(os.path.join(csv_folder,file)) # opening csv file
    
    # making list of strings of timepoints
    timepoints = list(antib_csv.keys())
    timepoints.remove(timepoints[0])

    antib_widths, antib_n = antibcsv_tolists(antib_csv, timepoints) # using function to extract lists
    all_widths.append(antib_widths) # joining the seperate lists in a big list of lists
    all_nlabels.append(antib_n) # joining the number of bac in a big list of lists
    
# PLOTTING

for i in range(len(all_widths)):
    
    fig = plt.figure()
    ax1 = fig.add_axes([0,0,1,1])
    
    ax1.set_ylim([0.5,2.5]) # limit for the y axis
    
    bp = ax1.boxplot(all_widths[i],vert=True,  # vertical box alignment
                         patch_artist=True,
                         boxprops = dict(facecolor=colors[i], color=colors[i])) # giving the antib graph its corresponding color color
    
    ax1.set_xticks(range(1,len(all_widths[i])+1))
    ax1.set_xticklabels(timepoints, Fontsize=10)
        
    plt.title(antib_names[i])
    plt.xlabel("time (min)")
    plt.ylabel("Boxplot: maximum widths of bacteria (μm)")

    ax2 = ax1.twinx()
    ax2.set_ylim([0,360])
    ax2.plot(range(1,len(all_nlabels[i])+1),all_nlabels[i], '.-', c=colors[i])
    plt.ylabel("Curve: number of bacteria")


