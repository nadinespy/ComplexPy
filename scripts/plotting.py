#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 19:56:43 2021

@author: nadinespy

This script produces heatplots.

"""

import os
from oct2py import Oct2Py
from oct2py import Struct
import seaborn as sns
import numpy as np
import scipy.io
import os.path as op
import matplotlib as plt
import glob
import scipy.io as sio
from importlib import reload # %load_ext autoreload, %autoreload 2 %reset
import pickle
import joblib

#%% paths

os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
import emergence_complexity_measures_comparison as ecmc 

analyses_pathin = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/analyses/'
plots_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/plots/'
data_pathin = op.join(ecmc.__path__[0], 'data')

#%% load emergence capacity of networks

all_causal_emergencies = joblib.load(analyses_pathin+r'causal_emergence_ccs_mmi_2node_8node_all_err_coup1.pkl')

#%% plot heatmaps

sns.set_theme()

all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"]


for i in range(len(emergence_network_paths)):
    blubb_
    
ax = sns.heatmap(all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"])


num_ticks = 10
# the index of the position of yticks
yticks = np.linspace(0, len(all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"]) - 1, num_ticks, dtype=np.int)
# the content of labels of these yticks
yticklabels = np.linspace(0.045,0.45, num_ticks) 

yticklabels = [all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"][idx] for idx in yticks]



ax = sns.heatmap(all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"], yticklabels=yticklabels)
ax.set_yticks(yticks)

plt.show()

yticks = np.linspace(0, len(all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"]) - 1, num_ticks, dtype=np.int)
yticklabels = np.linspace(0.045,0.45, num_ticks) 
xticklabels = np.linspace(0.09,0.9, num_ticks) 
plot = sns.heatmap(all_causal_emergencies[list(all_causal_emergencies.keys())[0]]["emergence_capacity"], xticklabels = num_ticks, yticklabels = num_ticks)
#plot.set_xticklabels([a,b,c])
plot.set_yticklabels(yticklabels)
plot.set_xticklabels(xticklabels)
plot.yticks(rotation=0) 





#%%

sns.heatmap(data=all_causal_emergencies_dfs, x='noise', col='coupling', y='value') 

sns.catplot(data=dfs, x='model', col='measure', y='value')


