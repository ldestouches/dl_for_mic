#---------------------------------------------------------
# AREA VS TIME FRAME for multiple timelapses
#---------------------------------------------------------

# The csv file combining ID, frame and pixel area was taken from TrackMate-StarDist
# on timelapses from ARNO exp 2 

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Iterable list with names of csv files
dfcsvlist = ['Plot of Area vs T_exp2f1.csv',\
             'Plot of Area vs T_exp2f2.csv',\
             'Plot of Area vs T_exp2f3.csv',\
             'Plot of Area vs T_exp2f4.csv']

# Import as np arrays and clean the csv files, then append dataframes to a list called dfcsv
dfcsv = [[] for l in range(len(dfcsvlist))]
for i in range(len(dfcsvlist)):    
    df = np.array(pd.read_csv(dfcsvlist[i]))
    dfclean = np.delete(df,[0,1],0)
    dfcsv[i].append(dfclean)

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

# Here we sum the 
for i in range(len(dfcsv)):
    t_a = make_t_a_list(dfcsv[i][0])
    a_total_list = []
    for j in range(len(t_a)):
        a_total = sum(t_a[j])
        a_total_list.append(a_total)
    plt.plot(range(len(a_total_list)),a_total_list,label='Field '+str(i+1))

plt.title('Total Bacteria Area by Timeframe')
plt.xlabel('frame')
plt.ylabel('area (pixel^2)')
plt.legend()
plt.show()

