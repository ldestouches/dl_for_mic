# ------------------------------------------------------------------------
# EVALUATION OF INITIAL LEARNING RATE
#-------------------------------------------------------------------------

# This code can evaluate on a graph the final IoU for different initial learning rate of the StarDist model.

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import training_evaluation and Quality_Control csv files for n models with same parameters but different ilr
training_list = ['training_evaluation (9).csv',\
                 'training_evaluation.csv',\
                 'training_evaluation (10).csv',\
                 'training_evaluation (1).csv',\
                 'training_evaluation (2).csv',\
                 'training_evaluation (3).csv', \
                 'training_evaluation (4).csv', \
                 'training_evaluation (5).csv',\
                 'training_evaluation (6).csv', \
                 'training_evaluation (7).csv', \
                 'training_evaluation (8).csv']

QC_list = ['Quality_control for ilr_test_00001.csv',\
           'Quality_Control for ilr_test_00005.csv', \
           'Quality_Control for ilr_test_0001.csv', \
           'Quality_Control for ilr_test_0002.csv', \
           'Quality_Control for ilr_test_00025.csv', \
           'Quality_Control for ilr_test_0003.csv', \
           'Quality_Control for ilr_test_0005.csv', \
           'Quality_Control for ilr_test_0015.csv', \
           'Quality_Control for ilr_test_002.csv', \
           'Quality_Control for ilr_test_003.csv',\
           'Quality_Control for ilr_test_015.csv']

# empty lists
ilr_list = []
floss_list = []
fvalloss_list = []
IoU_list = []

loss_list = []
valloss_list = []

# Loop through csv files
for i in range(len(training_list)):
    
    training_eval = np.array(pd.read_csv(training_list[i]))
    QC = np.array(pd.read_csv(QC_list[i]))
    
    # initial learning rate value
    ilr = training_eval[0][2]
    print(ilr)
    ilr_list.append(ilr)
    
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
plt.plot(ilr_list,IoU_list,'-ro', label='IoU')
plt.plot(ilr_list,floss_list,'--b', label = 'loss')
plt.plot(ilr_list,fvalloss_list,'--y', label='validation loss')
plt.xlabel('initial learning rate')
plt.ylabel('IoU')
plt.legend()
plt.title('Parameter Evaluation for StarDist')

plt.subplot(1,2,2)
plt.axis('off')
txt="Data extracted from StarDist training evaluation and quality control csv files. \n"\
     +"\n Number of models trained: " + str(i+1)\
     +"\n Number of epochs: " + str(j+1) +"\n"\
     + "\n Parameter of interest: Initial Learning Rate"\
     + "\n Initial learning rates tested: "\
     + str(ilr_list[:]).strip('[]')
plt.figtext(0.6, 0.5, txt, wrap=True, horizontalalignment='left', fontsize=12)

plt.tight_layout()
plt.show()

for i in range(len(loss_list)-1):
    plt.plot(range(len(loss_list[i])), loss_list[i], label='ILR='+str(ilr_list[i]))
plt.title('Loss Curve Parameter Evaluation for StarDist')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
