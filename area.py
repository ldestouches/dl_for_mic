#---------------------------------------------------------
# AREA VS TIME FRAME
#---------------------------------------------------------

# The csv file combining ID, frame and pixel area was taken from TrackMate-StarDist
# on timelapse 

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

areadf_csv = np.array(pd.read_csv('Plot of Area vs T.csv'))
areadf = np.delete(areadf_csv,[0,1],0)

label_list = []
t_list = []
area_list = []

# converting csv array into variable lists
for i in range(len(areadf)):
    
    label = areadf[i][0]
    label_list.append(label)
    
    t = int(float(areadf[i][1]))
    t_list.append(t)
    
    area = float(areadf[i][2])
    area_list.append(area)

# merge areas of same time point

t_a = [[] for i in range(max(t_list))]

for i in range(len(t_list)):
    for j in range(len(t_a)):
        if t_list[i] == j:
            t_a[j].append(area_list[i])
        else:
            continue

# plot growth rate
plt.figure()
area_mean=[]
for i in range(len(t_a)):
    area_mean.append(sum(t_a[i]))
plt.plot(range(len(area_mean)),area_mean,'--g')
plt.title('bacteria area by timeframe')
plt.xlabel('frame')
plt.ylabel('area (pixel^2)')
plt.show()
