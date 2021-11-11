#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:55:56 2021

@author: nadinespy

This script loads phiid files generated in matlab, calculates emergence capacity using ecmc.compute_emergence() and saves
everything in a pandas dataframe.

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
import importlib
import pickle
import random


oc = Oct2Py()

    
 
#%% 
if __name__ == "__main__":
    
    # paths
    os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
    import emergence_complexity_measures_comparison as ecmc 

    
    analyses_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/analyses/'
    plots_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/plots/'
    data_pathin = op.join(ecmc.__path__[0], 'data')

# -----------------------------------------------------------------------------
# causal emergence (based on phiid and practical)
# -----------------------------------------------------------------------------

#% load/generate data

# CREATING PANDAS DATAFRAME with the following columns:

# model:            'two_node_mvar_model'
#                   'eight_node_mvar_model_different_architectures'
#                   'eight_node_mvar_model_global_coupling'
#                   'eight_node_mvar_model_erdoes_renyi'

# noise_corr:       100 values (noise correlations) going from 0.01 to 0.9 with equal steps between them
# coupling:         for 'two_node_mvar_model': 100 values (coupling strengths) going from 0.045 to 0.45 with equal steps between them 
#                   for 'eight_node_mvar_model_different_architectures': 7 distinctly different connectivity matrices:  'optimal_A' 
#                                                                                                                       'optimal_B'
#                                                                                                                       'small_world'
#                                                                                                                       'two_communities'
#                                                                                                                       'fully_connected'
#                                                                                                                       'ring'
#                                                                                                                       'uni_ring'
#                   for 'eight_node_mvar_model_global_coupling' & 
#                   'eight_node_mvar_model_erdoes_renyi': 100 values (being either global coupling factors or densities) going from 0.05 to 0.9 with equal steps between them

# time_lag:         2 values (time lags)

# measure:          'phiid_emergence_capacity'
#                   'phiid_downward_causation'
#                   'phiid_causal_decoupling'
#                   'practical_emergence_capacity'
#                   'practical_downward_causation'
#                   'practical_causal_decoupling'
#                   'dynamical_independence'
#                   'g_emergence'

# redundancy_func:  'mmi'
#                   'ccs'      

# macro_var:        time-series (of length npoints) of macro variable    

# value:            value of emergence measure

emergence_df_temp = []

time_lags = [1, 3] 
npoints = 2000
redundancy_funcs = ['mmi','ccs']
emergence_measures = ["causal_emergence_phiid", "causal_emergence_practical"] #, "dynamical_independence", "g_emergence"]

# ----------------------------------------------------------------------------
# 2-node networks with differing noise correlation & coupling strength
# ----------------------------------------------------------------------------

coupling_vec = np.linspace(0.045, 0.45, num = 100)
noise_corr_vec = np.linspace(0.01, 0.9, num = 100)

random.seed(10)

for l in time_lags:
    time_lag = l
    
    for k in redundancy_funcs:
        redundancy_func = k
        
        for i in noise_corr_vec:
            err = i
        
            for j in coupling_vec:
                
                coupling_matrix = np.matrix([[j, j], [j, j]])
                sim_data = ecmc.mvar_sim_data(coupling_matrix, npoints = npoints, time_lag = time_lag, err = err)
                
                for n in range(len(emergence_measures)):    
                    emergence_result = ecmc.compute_emergence(emergence_measures[n], sim_data, time_lag = time_lag, redundancy_func = redundancy_func)

                    if (emergence_measures[n] == 'causal_emergence_phiid') or (emergence_measures[n] == 'causal_emergence_practical'):
                        for key in emergence_result:
                            df_temp = pd.DataFrame({'model': ['two_node_mvar_model'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], ' measure': [key], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result[key]]})
                            emergence_df_temp.append(df_temp)
                            
                    else:
                        df_temp = pd.DataFrame({'model': ['two_node_mvar_model'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': emergence_measures[n], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result]})
                        emergence_df_temp.append(df_temp)
                        
# ---------------------------------------------------------------------------- 
# 8-node networks with different architectures
# ----------------------------------------------------------------------------

file_to_read = open(data_pathin+r'/various_nets.pkl', "rb") 
various_nets = pickle.load(file_to_read)                        # load file with different coupling matrices

for l in time_lags:
    time_lag = l
    
    for k in redundancy_funcs:
        redundancy_func = k
        
        for i in noise_corr_vec:
            err = i
        
            for j in various_nets:
                coupling_matrix = various_nets[j]
                
                sr = max(abs(np.real(np.linalg.eig(coupling_matrix)[0])));              # compute spectral radius; np.linalg.eig() gives the eigenvalues (first output) plus eigenvectors (second output)
                coupling_matrix_normalized = np.divide(coupling_matrix, (1.10*sr)) 
                
                sim_data = ecmc.mvar_sim_data(coupling_matrix_normalized, npoints = npoints, time_lag = time_lag, err = err)

                for n in range(len(emergence_measures)):    
                    emergence_result = ecmc.compute_emergence(emergence_measures[n], sim_data, time_lag = time_lag, redundancy_func = redundancy_func)
                    
                    if (emergence_measures[n] == 'causal_emergence_phiid') or (emergence_measures[n] == 'causal_emergence_practical'):
                        for key in emergence_result:
                            df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_different_architectures'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': [key], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result[key]]})
                            emergence_df_temp.append(df_temp)
                    else:
                        df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_different_architectures'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': emergence_measures[n], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result]})
                        emergence_df_temp.append(df_temp)

# ----------------------------------------------------------------------------
# 8-node networks with global coupling strength using OptimalB net
# ----------------------------------------------------------------------------

optimal_b_net = various_nets['OptimalB']

k_vec = np.linspace(0.01, 0.9, num = 100000)

for i in range(99999):
    sr = max(abs(np.real(np.linalg.eig(k_vec[i] * optimal_b_net)[0])))
    
    if sr >= 1:
        sr = max(abs(np.real(np.linalg.eig(k_vec[i-1] * optimal_b_net)[0])))
        k_max = k_vec[i-1]
        break
    else:
        k_max = k_vec[i]
     
random.seed(15)

for l in time_lags:
    time_lag = l
    
    for k in redundancy_funcs:
        redundancy_func = k
        
        for i in noise_corr_vec:
            err = i
        
            for j in coupling_vec:
                global_coupling = j
                
                optimal_b_net_temp = k_max * global_coupling * optimal_b_net
                er_network_normalized.all() != float('NaN')
                sim_data = ecmc.mvar_sim_data(optimal_b_net_temp, npoints = npoints, time_lag = time_lag, err = err)

                for n in range(len(emergence_measures)):    
                    emergence_result = ecmc.compute_emergence(emergence_measures[n], sim_data, time_lag = time_lag, redundancy_func = redundancy_func)
                    
                    if (emergence_measures[n] == 'causal_emergence_phiid') or (emergence_measures[n] == 'causal_emergence_practical'):
                        for key in emergence_result:
                            df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_global_coupling'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': [key], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result[key]]})
                            emergence_df_temp.append(df_temp)
                    else:
                        df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_global_coupling'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': emergence_measures[n], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result]})
                        emergence_df_temp.append(df_temp)
     
# ----------------------------------------------------------------------------
# 8-node Erdös-Rényi networks
# ----------------------------------------------------------------------------

density_vec = np.linspace(0.05, 0.9, num = 100)
nb_er_networks = 50
	
random.seed(20)

for n in range(len(emergence_measures)):

    for l in time_lags:
        time_lag = l
    
        for k in redundancy_funcs:
            redundancy_func = k
        
            for i in noise_corr_vec:
                err = i
                print(time_lag)
                print(k)
                print(i)
        
                for j in density_vec:
                    density = j
                    emergence_result_temp = []
                             
                    for p in range(nb_er_networks):
                        er_network = np.zeros((8, 8))
                        a = 0
                        b = 0.99
                        
                        for w in range(len(er_network)):
                            for t in range(len(er_network)):
                                r = ((b-a) * random.uniform(a, b)) + a
                                    
                                if r <= density and w != t:
                                    er_network[w, t] = 1

                        sr = max(abs(np.real(np.linalg.eig(er_network)[0])))              # compute spectral radius; np.linalg.eig() gives the eigenvalues (first output) plus eigenvectors (second output)
                        er_network_normalized = np.divide(er_network, (1.10*sr)) 
                        
                        sim_data = ecmc.mvar_sim_data(er_network_normalized, npoints = npoints, time_lag = time_lag, err = err)
                    
                        emergence_result_temp.append(ecmc.compute_emergence(emergence_measures[n], sim_data, time_lag = time_lag, redundancy_func = redundancy_func))
                    
                    if (emergence_measures[n] == 'causal_emergence_phiid') or (emergence_measures[n] == 'causal_emergence_practical'):
                    
                        er_causal_decoupling_temp = []
                        er_downward_causation_temp = []
                        er_emergence_capacity_temp = []
                        for a in emergence_result_temp:
                            if (emergence_measures[n] == 'causal_emergence_phiid'):
                                er_causal_decoupling_temp.append(a['phiid_causal_decoupling']) 
                                er_downward_causation_temp.append(a['phiid_downward_causation']) 
                                er_emergence_capacity_temp.append(a['phiid_emergence_capacity']) 
                            else:
                                er_causal_decoupling_temp.append(a['practical_causal_decoupling'])
                                er_downward_causation_temp.append(a['practical_downward_causation']) 
                                er_emergence_capacity_temp.append(a['practical_emergence_capacity'])
                                
                        er_causal_decoupling = np.nanmean(er_causal_decoupling_temp)
                        er_downward_causation = np.nanmean(er_downward_causation_temp)
                        er_emergence_capacity = np.nanmean(er_emergence_capacity_temp)
                    
                        er_causal_emergence = [[er_causal_decoupling], [er_downward_causation], [er_emergence_capacity]]
                    
                        for key, value in zip(emergence_result_temp[0], er_causal_emergence):
                            df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_erdoes_renyi'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': [key], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [value]})
                            emergence_df_temp.append(df_temp)
                        
                    else:
                        emergence_result = np.nanmean(emergence_result_temp)
                        df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_erdoes_renyi'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': emergence_measures[n], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result]})
                        emergence_df_temp.append(df_temp)
                    
                    
                
#for idx in range(128400, len(emergence_df_temp)):      
#    emergence_df_temp.pop(idx)
                        
                
emergence_df3 = pd.concat(emergence_df_temp, ignore_index = True)    
emergence_df3.to_pickle(analyses_pathout+r'emergence_df3.pkl')
emergence_df3 = pd.read_pickle(analyses_pathout+r'emergence_df3.pkl')

# emergence_df: two-node only mmi, time_lag 1
# emergece_df2: eight-node with diff. architectures & global couplings
# emergence_df3: er networks, last error was 0.12686868686868686868



f = open(analyses_pathout+r'two_node_mvar_models_sim_data.pkl',"wb")
pickle.dump(two_node_mvar_models,f)
f.close()

file_to_read = open(analyses_pathout+r'two_node_mvar_models_sim_data.pkl', "rb")
two_node_mvar_models = pickle.load(file_to_read)


#%% plotting

causal_emergence_phiid_labels = ["phiid_emergence_capacity", "phiid_downward_causation", "phiid_causal_decoupling"]

y_ticklabels_8node = ['optimal_A', 'optimal_B', 'small_world', 'two_communities', 'fully_connected', 'ring', 'uni_ring']


for o in causal_emergence_phiid_labels:
    temp_model_measure = pd.pivot_table(emergence_df3.loc[(emergence_df3.model == 'eight_node_mvar_model_erdoes_renyi') & (emergence_df3.measure == o)],
                                        values ='value', index = ['coupling'], columns = ['noise_corr'], sort  = False) 
    
    num_ticks = 10
            
    yticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
    xticks = np.linspace(0, len(temp_model_measure.columns) - 1, num_ticks, dtype = int)            
    xticklabels = ["{:.2f}".format(temp_model_measure.columns[idx]) for idx in xticks]
    #yticklabels = ["{:.2f}".format(temp_model_measure.index[idx]) for idx in yticks]
    
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['axes.titlesize'] = 8
    plt.rcParams['axes.labelsize'] = 8
    fig, ax = plt.subplots(1,1)
    sns.heatmap(temp_model_measure, cbar_kws={'label': o}, cmap = "coolwarm", ax=ax) # cmap = "YlGnBu"
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation = 0)
    
    
    
#%%
#% load/generate macro variable

#% calculate emergence measure(s)

# goal: have something like this
# causal_emergence = compute_emergence(measure, data, tau = tau, redundancy_func = 'mmi', macro_variable = macro_variable)
# statistical_complexity = compute_complexity(measure, data)


# workaround: in the final version, data should not be empty, but have the actual time-series, and phiid_path should be eliminiated, as phiid should be calculated in Python as well (as opposed to loaded from files)
data = []

# order of models described in phiid_paths should corresponds to order in models
phiid_paths = sorted(glob.glob(analyses_pathout+r'phiid/*_all_atoms**1**mat*')) 




emergence_dict = {}


for parameters in two_node_mvar_models:
    sim_data_temp = two_node_mvar_models[parameters]['sim_data']
    
    redundancy_func = 'mmi'
    emergence_measure = "causal_emergence_phiid"
    tau = 1
    try:
        emergence_result = ecmc.compute_emergence(emergence_measure, sim_data_temp, tau = tau, redundancy_func = redundancy_func)
    except:
        emergence_result = float('NaN') 
    
    dict_temp = {'model': ['two_node_mvar_model'], 'noise_corr': [i], 'coupling': [j], 'tau': [tau], ' measure': [emergence_measure], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result]}
    emergence_dict[parameters] = dict_temp






models = ["phiid_ccs_2node_all_err_coup1", "phiid_mmi_2node_all_err_coup1", "phiid_ccs_8node_all_err_coup1", "phiid_mmi_8node_all_err_coup1"]
all_causal_emergencies_dfs = []
for model in models: 
    
    causal_emergence = ecmc.compute_emergence("causal_emergence_phiid", data, tau = 1, redundancy_func = 'mmi')
    
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
            coupling_labels = ['phi_optimal_binary_network', 'phi_optimal_weighted_network', 'small_world', 'two_communities', 'fully_connected', 'bidirectional_ring', 'unidirectional_ring']
            noise_labels = np.linspace(0.01, 0.9, 7)
            noise_labels_unpacked = np.tile(noise_labels, 7)
            coupling_labels_unpacked = np.repeat(coupling_labels, 7)
            
            temp_df = pd.DataFrame({'noise_corr': noise_labels_unpacked, 'coupling': coupling_labels_unpacked,
                                    'value': values, 'model': model, 'measure': measure})

            all_causal_emergencies_dfs.append(temp_df)
            
all_causal_emergencies_dfs = pd.concat(all_causal_emergencies_dfs, ignore_index=True)    

all_causal_emergencies_dfs.to_pickle(analyses_pathout+r'causal_emergence_ccs_mmi_2node_8node_all_err_coup1.pkl')


causal_decoupling_phiid_ccs_2node_all_err_coup1 = all_causal_emergencies_dfs.loc[(all_causal_emergencies_dfs.model =="phiid_ccs_8node_all_err_coup1") & (all_causal_emergencies_dfs['measure'] == "causal_decoupling")][['value', 'coupling', 'noise_corr']]

#%% plotting

causal_emergence_phiid_labels = ["phiid_emergence_capacity", "phiid_downward_causation", "phiid_causal_decoupling"]

y_ticklabels_8node = ['optimal_A', 'optimal_B', 'small_world', 'two_communities', 'fully_connected', 'ring', 'uni_ring']


for o in causal_emergence_phiid_labels:
    temp_model_measure = pd.pivot_table(emergence_df2.loc[(emergence_df2.model == 'eight_node_mvar_model_different_architectures') & (emergence_df2.measure == o)], values ='value', index = 'coupling', columns ='noise_corr', sort  = False) 
        
    num_ticks = 10
            
    yticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
    xticks = np.linspace(0, len(temp_model_measure.columns) - 1, num_ticks, dtype = int)            
    xticklabels = ["{:.2f}".format(temp_model_measure.columns[idx]) for idx in xticks]
    #yticklabels = ["{:.2f}".format(temp_model_measure.index[idx]) for idx in yticks]
    
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['axes.titlesize'] = 8
    plt.rcParams['axes.labelsize'] = 8
    fig, ax = plt.subplots(1,1)
    sns.heatmap(temp_model_measure, cbar_kws={'label': o}, cmap = "coolwarm", ax=ax) # cmap = "YlGnBu"
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation = 0)
    
    # something has been deleted/gone wrong here - need to fix this
    if '2node' in model:
        num_ticks = 10
        yticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
        xticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
        xticklabels = ["{:.2f}".format(causal_decoupling_phiid_ccs_2node_all_err_coup1.columns[idx]) for idx in xticks]
        yticklabels = ["{:.2f}".format(causal_decoupling_phiid_ccs_2node_all_err_coup1.index[idx]) for idx in yticks]
    
    elif '8node' in model:
        num_ticks = 7
        yticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
        xticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
        xticklabels = ["{:.2f}".format(temp_model_measure.columns[idx]) for idx in xticks]
        yticklabels = y_ticklabels_8node
    
        #fig, ax = plt.figure(figsize=(1, 1))
    
        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
        plt.rcParams['axes.titlesize'] = 8
        plt.rcParams['axes.labelsize'] = 8

        ax = sns.heatmap(temp_model_measure, cbar_kws={'label': measure}, cmap = "coolwarm") # cmap = "YlGnBu"
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


    
#sns.heatmap(data=all_causal_emergencies_dfs, x='noise', col='coupling', y='value') 
#sns.catplot(data=all_causal_emergencies_dfs, x='model', col='measure', y='value')






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