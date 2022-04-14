# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 10:03:42 2022

@author: ldestouches
"""

#---------------------------------------------------------
# GROWTH RATE CURVES
#---------------------------------------------------------

# The csv file combining ID, frame and pixel area was taken from TrackMate-StarDist
# on timelapses from ARNO exp 1

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Iterable list with names of csv files
dfcsvlist = ['Plot of Area vs T_exp1f1.csv',\
             'Plot of Area vs T_exp1f2.csv',\
                 'Plot of Area vs T_exp1f3.csv',\
                     'Plot of Area vs T_exp1f4.csv',\
                         'Plot of Area vs T_exp1f5.csv']

# Import as np arrays and clean the csv files, then append dataframes to a list called dfcsv
dfcsv = [[] for l in range(len(dfcsvlist))]
for i in range(len(dfcsvlist)):    
    df = np.array(pd.read_csv(dfcsvlist[i]))
    dfclean = np.delete(df,[0,1],0)
    dfcsv[i].append(dfclean)


# FUNCTION FOR AREA SORTED IN TIMEFRAMES
# This function reformates the arrays into lists that are easier to handle.
# The output is a list of lists called t_a where all the areas are stored into lists corresponding to
#each timeframe
def make_t_a_list(arr):
    
    label_list = []
    t_list = []
    area_list = []
    
    for i in range(len(arr)):
        
        label = arr[i][0]
        label_list.append(label)
        
        t = int(float(arr[i][1]))
        t_list.append(t)
        
        area = float(arr[i][2])
        area_list.append(area)
        
    t_a = [[] for i in range(max(t_list))]

    for i in range(len(t_list)):
        for j in range(len(t_a)):
            if t_list[i] == j:
                t_a[j].append(area_list[i])
            else:
                continue
            
    return t_a


# FUNCTION FOR PLOT VARIABLES
def variables_for_plot(dfcsv):

    plot_alist = [[] for l in range(len(dfcsv))]
    plot_nlist = [[] for l in range(len(dfcsv))]
    plot_vlist = [[] for l in range(len(dfcsv))]
    plot_slist = [[] for l in range(len(dfcsv))]

    for i in range(len(dfcsv)):

        t_a = make_t_a_list(dfcsv[i][0])

        a_total_list = []
        n_list = []
        v_list = []
        s_list = []
        
        for j in range(len(t_a)):

            a_total = sum(t_a[j])
            a_total_list.append(a_total)

            n = len(t_a[j])
            n_list.append(n)
        
        a_total_min = max(a_total_list)
        for a in range(len(a_total_list)):
            a_var = (a_total_list[a] / a_total_min) #- 1
            v_list.append(a_var)
        
        for a in range(3,len(a_total_list)):
            a_smooth = (a_total_list[a] + a_total_list[a-1] + a_total_list[a-2]) / 3
            s_list.append(a_smooth)
        
        plot_alist[i].append(a_total_list)
        plot_nlist[i].append(n_list)
        plot_vlist[i].append(v_list)
        plot_slist[i].append(s_list)
        
    return plot_alist, plot_nlist, plot_vlist, plot_slist

# retrieve the variables from function
plot_alist, plot_nlist, plot_vlist, plot_slist = variables_for_plot(dfcsv)

# same, but different
'''
fig, ax = plt.subplots(1,1)

for i in range(len(plot_alist)):
    field_label = 'Field ' + str(i+1)
    ax.plot(range(len(plot_alist[i][0])), plot_alist[i][0], label=field_label)
ax.set_title('Total Bacteria Area by Timeframe, different')
ax.set_xlabel('frame')
ax.set_ylabel('area (pixel^2)')
fig.legend()
fig.show()
# PLOTS
'''
for i in range(len(plot_alist)):
    field_label = 'Field ' + str(i+1)
    plt.plot(range(len(plot_alist[i][0])), plot_alist[i][0], label=field_label)
plt.title('Total Bacteria Area by Timeframe')
plt.xlabel('frame')
plt.ylabel('area (pixel^2)')
plt.legend()
plt.show()

for i in range(len(plot_nlist)):
    field_label = 'Field ' + str(i+1)
    plt.plot(range(len(plot_nlist[i][0])), plot_nlist[i][0], label=field_label)
plt.title('Total Number of Bacteria by Timeframe')
plt.xlabel('frame')
plt.ylabel('number of bacteria')
plt.legend()
plt.show()

for i in range(len(plot_vlist)):
    field_label = 'Field ' + str(i+1)
    plt.plot(range(len(plot_vlist[i][0])), plot_vlist[i][0], label=field_label)
plt.title('Variation in Area Growth')
plt.xlabel('frame')
plt.ylabel('variation in area (arbitrary unit)')
plt.legend()
plt.show()

for i in range(len(plot_slist)):
    field_label = 'Field ' + str(i+1)
    plt.plot(range(len(plot_slist[i][0])), plot_slist[i][0], label=field_label)
plt.title('Area by Timeframe (smoothed)')
plt.xlabel('frame')
plt.ylabel('area (arbitrary unit)')
plt.legend()
plt.show()

