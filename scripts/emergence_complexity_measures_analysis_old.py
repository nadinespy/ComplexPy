#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 14:46:11 2021

@author: nadinespy

This script loads phiid files generated in matlab, calculates emergence capacity without using ecmc.compute_emergence() and saves
everything in a pandas dataframe.

""" 

import os
from oct2py import Oct2Py
import numpy as np
import os.path as op
import glob
import scipy.io as sio
import joblib
import pandas as pd


oc = Oct2Py()

    
 
#%% 
if __name__ == "__main__":
    
    # paths
    os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
    import complex_py as ecmc 

    analyses_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/analyses/'
    plots_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/plots/'
    data_pathin = op.join(ecmc.__path__[0], 'data')

#%%
# -----------------------------------------------------------------------------
# causal emergence
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# load phiid of 2- and 8-node networks generated in matlab
# -----------------------------------------------------------------------------

def load_phiid_from_mat(phiid_path):
    try:
        phiid = sio.loadmat(phiid_path, squeeze_me=True, struct_as_record=False)['all_atoms_err_coup_mmi'] 
    except  KeyError:
        phiid = sio.loadmat(phiid_path, squeeze_me=True, struct_as_record=False)['all_atoms_err_coup_ccs']

    return phiid

# load file, if existent, otherwise load mat files and create pickle file
try:
    all_phiids = joblib.load(analyses_pathout+r'phiid_ccs_mmi_2node_8node_all_err_coup1.pkl')
except:
    phiid_paths = sorted(glob.glob(analyses_pathout+r'*_all_atoms**1**mat*')) 
    all_phiids = {}
    models = ["phiid_ccs_2node_all_err_coup1", "phiid_mmi_2node_all_err_coup1", "phiid_ccs_8node_all_err_coup1", "phiid_mmi_8node_all_err_coup1"]
    for i in range(len(phiid_paths)):
        temp_phiid = load_phiid_from_mat(phiid_paths[i])
        temp_phiid_dict = {'rtr': temp_phiid.rtr, 'rtx': temp_phiid.rtx, 'rty': temp_phiid.rty, 'rts': temp_phiid.rts, 'xtr': temp_phiid.xtr, 'xtx': temp_phiid.xtx, \
                 'xty': temp_phiid.xty, 'xts': temp_phiid.xts, 'ytr': temp_phiid.ytr, 'ytx': temp_phiid.ytx, 'yty': temp_phiid.yty, 'yts': temp_phiid.yts, \
                     'str': temp_phiid.str, 'stx': temp_phiid.stx, 'sty': temp_phiid.sty, 'sts': temp_phiid.sts}
        all_phiids[models[i]] = temp_phiid_dict
        
    joblib.dump(all_phiids, analyses_pathout+r'phiid_ccs_mmi_2node_8node_all_err_coup1.pkl')

# -----------------------------------------------------------------------------
# calculate synergistic/emergent capacity, downward causation, 
# causal decoupling and store everything in nested dictionary
# -----------------------------------------------------------------------------

# Syn(X_t;X_t-1) (synergistic capacity of the system) 
# Un (Vt;Xt'|Xt) (causal decoupling - the top term in the lattice) 
# Un(Vt;Xt'α|Xt) (downward causation) 

# synergy (only considering the synergy that the sources have, not the target): 
# {12} --> {1}{2} + {12} --> {1} + {12} --> {2} + {12} --> {12} 
 
# causal decoupling: {12} --> {12}

# downward causation: 
# {12} --> {1}{2} + {12} --> {1} + {12} --> {2}


all_causal_emergencies_dict = {}
models = ["phiid_ccs_2node_all_err_coup1", "phiid_mmi_2node_all_err_coup1", "phiid_ccs_8node_all_err_coup1", "phiid_mmi_8node_all_err_coup1"]
    
for i, j in zip(all_phiids, range(len(models))): 
    #synergistic capacity
    temp_emergence_capacity = all_phiids[i]["str"] + all_phiids[i]["stx"] + all_phiids[i]["sty"] + all_phiids[i]["sts"]
    temp_downward_causation = all_phiids[i]["str"] + all_phiids[i]["stx"] + all_phiids[i]["sty"]
    temp_causal_decoupling = temp_emergence_capacity - temp_downward_causation

    temp_causal_emergence_dict = {'emergence_capacity': temp_emergence_capacity, 'downward_causation': temp_downward_causation, 'causal_decoupling': temp_causal_decoupling}
    all_causal_emergencies_dict[list(all_phiids.keys())[j]] = temp_causal_emergence_dict
    
joblib.dump(all_causal_emergencies_dict, analyses_pathout+r'causal_emergence_ccs_mmi_2node_8node_all_err_coup1.pkl')

# -----------------------------------------------------------------------------
# convert all_causal_emergencies to dataframe to better do plots
# -----------------------------------------------------------------------------

all_causal_emergencies_dfs = []
for model in all_causal_emergencies_dict:
    for measure in all_causal_emergencies_dict[model]:
        values = all_causal_emergencies_dict[model][measure].flatten() # go from 100x100 to 10000 with first 100 elements being the first row
        
        if '2node' in model:
            coupling_labels = np.linspace(0.045, 0.45, 100)
            noise_labels = np.linspace(0.01, 0.9, 100)
            noise_labels_unpacked = np.tile(noise_labels, 100)
            coupling_labels_unpacked = np.repeat(coupling_labels, 100)
            
            temp_df = pd.DataFrame({'noise_corr': noise_labels_unpacked, 'coupling': coupling_labels_unpacked,
                                    'value': values, 'model': model, 'measure': measure})
            all_causal_emergencies_dfs.append(temp_df)
        elif '8node' in model:
            coupling_labels = ['phi_optimal_binary_network', 'phi_optimal_weighted_network', 'small_world', 'fully_connected', 'bidirectional_ring', 'unidirectional_ring']
            noise_labels = np.linspace(0.01, 0.9, 6)
            noise_labels_unpacked = np.tile(noise_labels, 6)
            coupling_labels_unpacked = np.repeat(coupling_labels, 6)
            
            temp_df = pd.DataFrame({'noise_corr': noise_labels_unpacked, 'coupling': coupling_labels_unpacked,
                                    'value': values, 'model': model, 'measure': measure})
        
            all_causal_emergencies_dfs.append(temp_df)
            

all_causal_emergencies_dfs = pd.concat(all_causal_emergencies_dfs, ignore_index=True)

