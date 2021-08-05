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

os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
import emergence_complexity_measures_comparison as ecmc 

analyses_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/analyses/'
plots_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/plots/'
data_pathin = op.join(ecmc.__path__[0], 'data')

#%% load emergence capacity of networks

def load_mat_file(phiid_path):
    try:
        phiid_network = sio.loadmat(phiid_path,squeeze_me=True,struct_as_record=False)['all_atoms_err_coup_mmi'] 
    except:
        pass
   
    try:
        phiid_network = sio.loadmat(phiid_path,squeeze_me=True,struct_as_record=False)['all_atoms_err_coup_ccs']
    except:
        pass
    
    return phiid_network
    

emergence_network_paths = sorted(glob.glob(analyses_pathout+r'*emergence_capacity*pkl')) 

all_networks = [0] * len(emergence_network_paths)

for i in range(len(emergence_network_paths)):
    all_networks[i] = joblib.load(emergence_network_paths[i])
    
#%% plot heatmaps

sns.set_theme()

ax = sns.heatmap(phiid_all_err_coup_mmi_rtr)
ax1 = sns.heatmap(phiid_all_err_coup_mmi_sts)





