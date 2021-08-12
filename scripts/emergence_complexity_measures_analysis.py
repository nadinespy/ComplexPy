#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:55:56 2021

@author: nadinespy

This script calculates emergence capacity from time-series.

""" 

import os
from oct2py import Oct2Py
from oct2py import Struct
import seaborn as sns
import numpy as np
import scipy.io
import os.path as op
import matplotlib.pyplot as plt
import glob
import scipy.io as sio
import joblib
from importlib import reload 
import pandas as pd


oc = Oct2Py()

    
 
#%% 
if __name__ == "__main__":
    
    # paths
    os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
    import emergence_complexity_measures_comparison as ecmc 

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


#%% load/generate data

#%% load/generate macro variable

#%% calculate emergence measure(s)

# goal: have something like this
# causal_emergence = compute_emergence(measure, data, tau = tau, redundancy_func = 'mmi', macro_variable = macro_variable)
# statistical_complexity = compute_complexity(measure, data)


# workaround: in the final version, data should not be empty, but have the actual time-series, and phiid_path should be eliminiated, as phiid should be calculated in Python as well (as opposed to loaded from files)
data = []

# order of models contained in phiid_paths should corresponds to order in models
phiid_paths = sorted(glob.glob(analyses_pathout+r'phiid/*_all_atoms**1**mat*')) 
models = ["phiid_ccs_2node_all_err_coup1", "phiid_mmi_2node_all_err_coup1", "phiid_ccs_8node_all_err_coup1", "phiid_mmi_8node_all_err_coup1"]

all_causal_emergencies_dfs = []
for phiid_path, model in zip(phiid_paths, models): 
    
    causal_emergence = ecmc.compute_emergence("causal_emergence_phiid", data, tau = 1, redundancy_func = 'mmi', phiid_path = phiid_path)
    for measure in causal_emergence:
        values = causal_emergence[measure].flatten()

        if '2node' in phiid_path:
            coupling_labels = np.linspace(0.045, 0.45, 100)
            noise_labels = np.linspace(0.01, 0.9, 100)
            noise_labels_unpacked = np.tile(noise_labels, 100)
            coupling_labels_unpacked = np.repeat(coupling_labels, 100)
            
            temp_df = pd.DataFrame({'noise_corr': noise_labels_unpacked, 'coupling': coupling_labels_unpacked,
                                    'value': values, 'model': model, 'measure': measure})
            all_causal_emergencies_dfs.append(temp_df)
        elif '8node' in phiid_path:
            coupling_labels = ['phi_optimal_binary_network', 'phi_optimal_weighted_network', 'small_world', 'fully_connected', 'bidirectional_ring', 'unidirectional_ring']
            noise_labels = np.linspace(0.01, 0.9, 6)
            noise_labels_unpacked = np.tile(noise_labels, 6)
            coupling_labels_unpacked = np.repeat(coupling_labels, 6)
            
            temp_df = pd.DataFrame({'noise_corr': noise_labels_unpacked, 'coupling': coupling_labels_unpacked,
                                    'value': values, 'model': model, 'measure': measure})

            all_causal_emergencies_dfs.append(temp_df)
            
all_causal_emergencies_dfs = pd.concat(all_causal_emergencies_dfs, ignore_index=True)    

all_causal_emergencies_dfs.to_pickle(analyses_pathout+r'causal_emergence_ccs_mmi_2node_8node_all_err_coup1.pkl')


causal_decoupling_phiid_ccs_2node_all_err_coup1 = all_causal_emergencies_dfs.loc[(all_causal_emergencies_dfs.model =="phiid_ccs_8node_all_err_coup1") & (all_causal_emergencies_dfs['measure'] == "causal_decoupling")][['value', 'coupling', 'noise_corr']]

blubb = pd.pivot_table(causal_decoupling_phiid_ccs_2node_all_err_coup1, values='value', index=['coupling'], columns='noise_corr', sort = False)
#%% plotting

measures = ["emergence_capacity", "downward_causation", "causal_decoupling"]
y_ticklabels_8node = ['optimal_A', 'optimal_B', 'small_world', 'fully_connected', 'ring', 'uni_ring']
for model in models:
    for measure in measures:
        causal_decoupling_phiid_ccs_2node_all_err_coup1 = pd.pivot_table(all_causal_emergencies_dfs.loc[(all_causal_emergencies_dfs.model == model) & (all_causal_emergencies_dfs['measure'] == measure)], values='value', index=['coupling'], columns='noise_corr', sort  = False) 
        
        if '2node' in model:
            num_ticks = 10
            yticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
            xticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
            xticklabels = ["{:.2f}".format(causal_decoupling_phiid_ccs_2node_all_err_coup1.columns[idx]) for idx in xticks]
            yticklabels = ["{:.2f}".format(causal_decoupling_phiid_ccs_2node_all_err_coup1.index[idx]) for idx in yticks]
        elif '8node' in model:
            num_ticks = 6
            yticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
            xticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
            xticklabels = causal_decoupling_phiid_ccs_2node_all_err_coup1.columns
            yticklabels = y_ticklabels_8node
    
        #fig, ax = plt.figure(figsize=(1, 1))
    
        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
        plt.rcParams['axes.titlesize'] = 8
        plt.rcParams['axes.labelsize'] = 8

        ax = sns.heatmap(causal_decoupling_phiid_ccs_2node_all_err_coup1, cbar_kws={'label': measure}, cmap = "coolwarm") # cmap = "YlGnBu"
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation = 0)

# cbar = ax.collections[0].colorbar
# here set the labelsize by 20
# cbar.ax.tick_params(labelsize=8)
        ax.set_title(measure + ' in ' + model)
        plt.show()
        
        fig = ax.get_figure()
        fig.savefig(plots_pathout + measure + '_' + model + '.png', dpi = 300, bbox_inches="tight")  
    
        del fig


    
    






#%%

# HIER ABSOLUTEN PFAD MACHEN <3
oc.load(['/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/A2b.mat'])

oc = Oct2Py()
y = [1, 2]
oc.push('y', y)


oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/practical_measures_causal_emergence')  
oc.EmergencePsi(np.random.randn(100,2), np.random.randn(100,1))

oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/phiid')  
oc.javaaddpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/phiid/infodynamics.jar')
oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/phiid/statistics-1.4.2/inst')
X = np.random.randint(10, size=(2, 2000))
oc.eval('pkg load statistics') 
blubb = oc.PhiIDFull(X, tau, 'MMI')


X = oc.statdata_coup_errors1(A, npoints, tau, err) 

nvar = 2
npoints = 10000
tau = 1
error_vec   = np.linspace(0.01, 0.99, 100)
coupling_vec = np.linspace(0.01,0.49, 100)

phiid_all_err_coup_mmi = np.zeros((16, len(coupling_vec), len(error_vec)))
phiid_all_err_coup_ccs = np.zeros((16, len(coupling_vec), len(error_vec)))

# functions do not exist in Octave workspace... help :( 
for i in range (1, len(coupling_vec)):
	A = coupling_vec[i]*np.ones(shape=(nvar,nvar))
	
	for j in range(1, len(error_vec)):
		err = error_vec[j]
        
        os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/practical_measures_causal_emergence')

        oc.eval('pkg load statistics') 
		X = oc.statdata_coup_errors1(A, npoints, tau, err)                                  # for whatever reason, the rng() in statdata_corr_error.m doesn't work when called via oct2py (for now, it's disabled)
		phiid_all_err_coup_mmi[:,i,j] = oc.struct2array(ecmc.phiid_full(X, tau, 'MMI')).T   # PhiIDFull.m doesn't work either, as mvnpdf() is not recognized
		phiid_all_err_coup_ccs[:,i,j] = oc.struct2array(ecmc.phiid_full(X, tau, 'ccs')).T   # struct2array is from matlab - how to deal with struct outputs in python?
	i	

phiid_all_err_coup_mmi_rtr = np.squeeze(phiid_all_err_coup_mmi[1,:,:])
phiid_all_err_coup_mmi_sts = np.squeeze(phiid_all_err_coup_mmi[16,:,:])

os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/results/')

np.save(phiid_all_err_coup_ccs, phiid_all_err_coup_ccs)
np.save(phiid_all_err_coup_mmi, phiid_all_err_coup_mmi)


phiid_all_err_coup_ccs = scipy.io.loadmat('phiid_all_err_coup_ccs.mat',squeeze_me=True)['phiid_all_err_coup_ccs']              # loads file as a dictionary where 4th row is the actual data
phiid_all_err_coup_mmi = scipy.io.loadmat('phiid_all_err_coup_mmi.mat',squeeze_me=True)['phiid_all_err_coup_mmi']    


#phiid_all_err_coup_ccs = list(phiid_all_err_coup_ccs.values())[3]                   # put all values from dict into a list, and take 3rd entry (which has the data)
#phiid_all_err_coup_mmi = list(phiid_all_err_coup_mmi.values())[3]

phiid_all_err_coup_mmi_rtr = np.squeeze(phiid_all_err_coup_mmi[0,:,:])
phiid_all_err_coup_mmi_sts = np.squeeze(phiid_all_err_coup_mmi[15,:,:])

#heatmap
sns.set_theme()

ax = sns.heatmap(phiid_all_err_coup_mmi_rtr)
ax1 = sns.heatmap(phiid_all_err_coup_mmi_sts)






cwd = os.getcwd()