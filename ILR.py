# ------------------------------------------------------------------------
# EVALUATION OF INITIAL LEARNING RATE
#-------------------------------------------------------------------------

# This code can evaluate on a graph the final IoU for different initial learning rate of the StarDist model.

# install dependencies
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import training_evaluation and Quality_Control csv files for n models with same parameters but different ilr

# GM1_1
training_eval_1 = np.array(pd.read_csv('C:/Users/ldestouches/Documents/SOFTWARE/Python/loss evaluation/training_eval/GM_1_1/training_evaluation_GM_1_1.csv'))
QC_1 = np.array(pd.read_csv('C:/Users/ldestouches/Documents/SOFTWARE/Python/loss evaluation/QC/Quality_Control for GM_1_1.csv'))

# GM1_2
#training_eval_2 = np.array(pd.read_csv(''))
#QC_2 = np.array(pd.read_csv(''))

# acquire the ILR from training_eval
ilr_1 = training_eval_1[0][2]

# acquire the final loss and val_loss value for 100 epochs
floss_1 = training_eval_1[99][0]
fvalloss_1 = training_eval_1[99][1]

# acquire the IoU avergae value from Quality-Control
IoU_1 = (QC_1[0][1] + QC_1[1][1] + QC_1[2][1]) / 3

# plot final loss and final val_loss over ILR
plt.plot(floss_1,ilr_1,'ro')
plt.show()

# plot IoU over ILR
plt.plot(IoU_1,ilr_1,'ro')
plt.show()