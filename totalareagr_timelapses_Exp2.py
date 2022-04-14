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

# Here we sum and plot the total area of the bacteria in each timeframe
for i in range(len(dfcsv)):
    t_a = make_t_a_list(dfcsv[i][0])
    a_total_list = []
    for j in range(len(t_a)):
        a_total = sum(t_a[j])
        a_total_list.append(a_total)
    plt.plot(range(len(a_total_list)),a_total_list,'--',label='Field '+str(i+1))

plt.title('Total Bacteria Area by Timeframe')
plt.xlabel('frame')
plt.ylabel('area (pixel^2)')
plt.legend()
plt.show()


# Here we plot the number of bacteria at each timeframe
for i in range(len(dfcsv)):
    t_a = make_t_a_list(dfcsv[i][0])
    n_total = []
    for j in range(len(t_a)):
        n_tf = len(t_a[j])
        n_total.append(n_tf)
    plt.plot(range(len(n_total)),n_total,'--',label='Field '+str(i+1))
plt.title('Total Number of Bacteria by Timeframe')
plt.xlabel('frame')
plt.ylabel('number of bacteria')
plt.legend()
plt.show()

# Here we plot the total area but make it proportional to the initial bacterial surface area
for i in range(len(dfcsv)):
    t_a = make_t_a_list(dfcsv[i][0])
    a_total_list = []
    for j in range(len(t_a)):
        a_total = sum(t_a[j])
        a_total_list.append(a_total)
    a_total_min = min(a_total_list)
    a_norm_list = []
    for a in range(len(a_total_list)):
        a_norm = (a_total_list[a] / a_total_min) - 1
        a_norm_list.append(a_norm)
    plt.plot(range(len(a_norm_list)),a_norm_list,'--',label='Field '+str(i+1))
plt.title('delta area growth')
plt.xlabel('frame')
plt.ylabel('area (arbitrary unit)')
plt.legend()
plt.show()





