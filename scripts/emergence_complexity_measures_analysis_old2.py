#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 15:05:27 2021

@author: nadinespy
"""


import os
from oct2py import Oct2Py
import numpy as np
import os.path as op
import pandas as pd
import pickle
import random


oc = Oct2Py()

#%%

if __name__ == "__main__":
    # TODO: make library installable
    # paths
    os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
    import complex_py as ecmc 

    
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
coupling_vec = np.linspace(0.045, 0.45, num = 10)
noise_corr_vec = np.linspace(0.01, 0.9, num = 10)
redundancy_funcs = ['mmi','ccs']
npoints = 2000

emergence_measures = {
    "causal_emergence_phiid": ecmc.causal_emergence_phiid,}
    #"causal_emergence_practical": ecmc.causal_emergence_practical} #, "dynamical_independence", "g_emergence"]
    
for coup in coupling_vec:
    for err in noise_corr_vec:
        for time_lag in time_lags:
            coupling_matrix = np.matrix([[coup, coup], [coup, coup]])
            sim_data = ecmc.mvar_sim_data(coupling_matrix, npoints = npoints, time_lag = time_lag, err = err)
            
            for redundancy_func in redundancy_funcs:
                #for n in range(len(emergence_measures)):
                for measure in emergence_measures:    
                    #emergence_result = ecmc.compute_emergence(emergence_measures[n], sim_data, time_lag = time_lag, redundancy_func = redundancy_func)
                    emergence_result = emergence_measures[measure](sim_data, time_lag = time_lag, redundancy_func = redundancy_func)
                    
                    if (emergence_measures[measure] == 'causal_emergence_phiid') or (emergence_measures[measure] == 'causal_emergence_practical'):
                        for key in emergence_result:
                            df_temp = pd.DataFrame({'model': ['two_node_mvar_model'],
                                                    'noise_corr': [err], 'coupling': [coup], 'time_lag': [time_lag],
                                                    'measure': [key], 'redundancy_func': [redundancy_func],
                                                    'macro_var': None, 'value': [emergence_result[key]]})
                            emergence_df_temp.append(df_temp)
                            
                    else:
                        df_temp = pd.DataFrame({'model': ['two_node_mvar_model'], 'noise_corr': [err], 'coupling': [coup], 'time_lag': [time_lag],
                                                #'measure': emergence_measures[n], 'redundancy_func': [redundancy_func],
                                                'measure': measure, 'redundancy_func': [redundancy_func],

                                                'macro_var': None, 'value': [emergence_result]})
                        emergence_df_temp.append(df_temp)
                        
# ---------------------------------------------------------------------------- 
# 8-node networks with different architectures
# ----------------------------------------------------------------------------

emergence_measures = ['causal_emergence_phiid', 'causal_emergence_practical', 'dynamical_independence', 'g_emergence']
    
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
                optimal_b_net_temp.all() != float('NaN')
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
    # TODO: no double assignments
    for l in time_lags:
        time_lag = l
    
        for redundancy_func in redundancy_funcs:
        
            for i in noise_corr_vec:
                for n in range(len(emergence_measures)):    
                    emergence_result = ecmc.compute_emergence(emergence_measures[n], sim_data, time_lag = time_lag, redundancy_func = redundancy_func)
                    
                    if (emergence_measures[n] == 'causal_emergence_phiid') or (emergence_measures[n] == 'causal_emergence_practical'):
                        for key in emergence_result:
                            df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_global_coupling'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': [key], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result[key]]})
                            emergence_df_temp.append(df_temp)
                    else:
                        df_temp = pd.DataFrame({'model': ['eight_node_mvar_model_global_coupling'], 'noise_corr': [i], 'coupling': [j], 'time_lag': [time_lag], 'measure': emergence_measures[n], 'redundancy_func': [redundancy_func], 'macro_var': None, 'value': [emergence_result]})
                        emergence_df_temp.append(df_temp)
     
                err = i
                print(time_lag)
                print(k)
                print(i)
        
                for j in density_vec:
                    density = j
                    emergence_result_temp = []
                             
                    for p in range(nb_er_networks):
                        # TODO: put this into a function
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
                        # TODO: until here
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
