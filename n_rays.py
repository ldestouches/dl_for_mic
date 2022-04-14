# ----------------------------------------------------------------------
# EVALUATION OF THE N-RAYS PARAMETER FOR STARDIST
# ----------------------------------------------------------------------

# This code can evaluate on a graph the final IoU for different parameter values of the StarDist model.

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd

# import parameter configuration, training_evaluation and Quality_Control csv files for n models
#with same parameters but different nrays
config_importlist = ['config_nr3.json',\
                     'config_nr30.json',\
                         'config_nr50.json',\
                             'config_nr100.json',\
                                 'config_nr150.json',\
                                     'config_nr200.json',\
                                         'config_nr300.json']

training_importlist = ['training_evaluation_nr3.csv',\
                       'training_evaluation_nr30.csv',\
                           'training_evaluation_nr50.csv',\
                               'training_evaluation_nr100.csv',\
                                   'training_evaluation_nr150.csv',\
                                       'training_evaluation_nr200.csv',\
                                           'training_evaluation_nr300.csv']

QC_importlist = ['Quality_control for nrays200e_nr3.csv',\
                 'Quality_Control for nrays200e_nr30.csv', \
                     'Quality_Control for nrays200e_nr50.csv', \
                         'Quality_Control for nrays200e_nr100.csv', \
                             'Quality_Control for nrays200e_nr150.csv', \
                                 'Quality_Control for nrays200e_nr200.csv',\
                                     'Quality_Control for nrays200e_nr300.csv']

# empty lists for IoU graph
nrays_list = []
floss_list = []
fvalloss_list = []
IoU_list = []

loss_list = []
valloss_list = []

# Loop through csv and json files
for i in range(len(training_importlist)):
    
    training_eval = np.array(pd.read_csv(training_importlist[i]))
    QC = np.array(pd.read_csv(QC_importlist[i]))
    config = json.load(open(config_importlist[i]))
    
    # nrays value
    nrays = config["n_rays"]
    print(nrays)
    nrays_list.append(nrays)
    
    # final loss value
    floss = training_eval[-1][0]
    print(floss)
    floss_list.append(floss)
    
    # final validation loss value
    fvalloss = training_eval[-1][1]
    print(fvalloss)
    fvalloss_list.append(fvalloss)
    
    # IoU value
    IoU = []
    for j in range(len(QC)):
        IoU.append(QC[j][1])
    IoU_mean = sum(IoU) / len(IoU)
    print(IoU_mean)
    IoU_list.append(IoU_mean)
    
    # loss and validation loss
    loss = []
    valloss = []
    for j in range(len(training_eval)):
        loss.append(training_eval[j][0])
        valloss.append(training_eval[j][1])
    loss_list.append(loss)
    valloss_list.append(valloss)


# Plot
plt.subplot(1,2,1)
plt.xscale('log')
plt.plot(nrays_list,IoU_list,'-ro', label='IoU')
plt.plot(nrays_list,floss_list,'--b', label = 'loss')
plt.plot(nrays_list,fvalloss_list,'--y', label='validation loss')
plt.xlabel('n_rays')
plt.ylabel('IoU')
plt.legend()
plt.title('Parameter Evaluation for StarDist')

plt.subplot(1,2,2)
plt.axis('off')
txt="Data extracted from StarDist training evaluation" + "\n and quality control csv files and config json files. \n"\
    +"\n Number of models trained: " + str(i+1)\
        +"\n Number of epochs: " + str(j+1) +"\n"\
            + "\n Parameter of interest: Number of Rays"\
                + "\n Number of Rays tested: \n"\
                    + str(nrays_list[:]).strip('[]')
plt.figtext(0.55, 0.4, txt, wrap=True, horizontalalignment='left', fontsize=10)

plt.show()

for i in range(len(loss_list)):
    plt.plot(range(len(loss_list[i])), loss_list[i], label='n_rays='+str(nrays_list[i]))
plt.title('Loss Curve Parameter Evaluation for StarDist')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

