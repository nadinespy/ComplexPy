#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Wed Aug  4 13:55:56 2021

@author: nadinespy

This script calculates emergence capacity using ecmc.compute_emergence() and saves
everything in a pandas dataframe.

''' 

# TODO: make library installable
# TODO: make lines only ~80 long
    
import os
from oct2py import octave as oc 
import numpy as np
import pandas as pd
 
#%% 

if __name__ == '__main__':
    

    # paths
    os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
    import emergence_complexity_measures_comparison as ecmc 
    
    os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/data')
    import data_simulation as ds

    main_directory = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python'
    analyses_pathout = main_directory + '/results/analyses/'
    plots_pathout = main_directory + '/results/plots/'
    data_pathin = main_directory + '/data/'

# -----------------------------------------------------------------------------
# MODEL & MEASURE PARAMETERS
# -----------------------------------------------------------------------------

# creating pandas dataframe with the following variables as columns:

# VARIABLES SPECIFIED BY USER:
    
# model:            '2node_mvar'

# noise_corr:       100 values (noise correlations) going from 0.01 to 0.9 with equal steps between them
# coupling:         for '2node_mvar': 100 values (coupling strengths) going from 0.045 to 0.45 with equal steps between them 
#                   for '8node_mvar_diff_top': 7 distinctly different connectivity matrices:  'optimal_A' 
#                                                                                             'optimal_B'
#                                                                                             'small_world'
#                                                                                             'two_communities'
#                                                                                             'fully_connected'
#                                                                                             'ring'
#                                                                                             'uni_ring'
#                   for '8node_mvar_global_coup' & 
#                   '8node_mvar_er': 100 values (being either global coupling factors or densities) going from 0.05 to 0.9 with equal steps between them

# macro:        time-series (of length npoints) of macro variable: 
#                   sum_micro_mvar

# micro:        time-series (of length npoints) of micro variables:   
#                   raw_micro_mvar   

# time_lag:         1, 10, 100 


# VARIABLES SPECIFIED BY ECMC LIBRARY:
# measure:          'causal_emergence_phiid' (dict with causal_emergence_phiid, downward_causation_phiid, causal_decoupling_phiid)
#                   'causal_emergence_practical' (dict with causal_emergence_pract, downward_causation_pract, causal_decoupling_pract)
#                   'dynamical_independence'
#                   'g_emergence'

# redundancy_func:  'mmi'
#                   'ccs'      

# value:            value of emergence measure





#%%

# ALLOCATE MODEL & MEASURE PARAMETERS IN RESPECTIVE DICTIONARIES 

# model-function pairs where keys give the model and values give the corresponding function for simulation;
# keys in model_functions and model_variables need to be the same 
model_functions =       {'2node_mvar': ds.generate_2node_mvar_data}

# model-variables pairs where keys give the model and values give the corresponding parameters of the model
model_variables =       {'2node_mvar': ['coupling', 'noise_corr', 'time_lag', 'npoints', 'macro_func_mvar', 'micro_func_mvar']}

# measure-function pairs, where keys give the measure, and values the corresponding function;
# keys in emergence_measures and measure_variables need to be the same
emergence_measures =    {'causal_emergence_phiid': ecmc.causal_emergence_phiid,
                         'causal_emergence_practical': ecmc.causal_emergence_practical} 

# variable names need to be the same as parameter names in the measure functions
measure_variables =     {'causal_emergence_phiid': ['micro', 'redundancy_func', 'time_lag'],
                         'causal_emergence_practical': ['macro', 'micro', 'time_lag']}

# all parameters relevant for either measures or data generation
parameters =            {'time_lag': [1, 10, 100], 
                         'coupling': np.linspace(0.045, 0.45, num = 10),
                         'noise_corr': np.linspace(0.01, 0.9, num = 10),
                         'redundancy_func': ['mmi','ccs'],
                         'npoints': [2000],
                         'macro_func_mvar': [ds.sum_micro_mvar],
                         'micro_func_mvar': [ds.raw_micro_mvar]}

# FINAL GOAL:
# emergence_measures =  {'causal_emergence_phiid': ecmc.causal_emergence_phiid, 
#                        'causal_emergence_practical': ecmc.causal_emergence_practical, 
#                        'dynamical_independence': ecmc.dynamical_independence, 
#                        'g_emergence': ecmc.g_emergence}

# model_functions =     {'2node_mvar': generate_2node_mvar_data,
#                        '8node_mvar_global_coup': generate_8node_global_coup_data, 
#                        '8node_mvar_er': generate_8node_mvar_er_data,
#                        '8node_mvar_diff_top': generate_8node_mvar_diff_top_data}

# load file for different 8-node MVAR architectures
# file_to_read = open(data_pathin+r'/various_nets.pkl', 'rb') 
# various_nets = pickle.load(file_to_read) 

# parameters =          {'time_lag': [1, 10, 1000], 
#                        'coupling': np.linspace(0.045, 0.45, num = 10),
#                        'noise_corr': np.linspace(0.01, 0.9, num = 10),
#                        'redundancy_func': ['mmi','ccs'],
#                        'npoints': [2000, 10000],
#                        '8node_architectures': various_nets,
#                        'global_coupling': np.linspace(0.05, 0.9, num = 10),
#                        'density_vec': np.linspace(0.05, 0.9, num = 10),
#                        'macro_mvar': [sum_micro_mvar],
#                        'micro_mvar': [raw_val_mvar],
#                        'macro_kuramoto': [sigma_chi_kuramoto, pair_sync_kuramoto],
#                        'micro_kuramoto': [raw_val_kuramoto, phase_kuramoto, sync_kuramoto, sync_bin_kuramoto]}

# model_variables =     {'2node_mvar': ['coupling', 'noise_corr', 'time_lag', 'npoints'], 
#                        '8node_mvar_er': ['density_vec', 'noise_corr', 'time_lag', 'npoints'],
#                        '8node_mvar_global_coup': ['coupling', 'noise_corr', 'time_lag', 'npoints'],
#                        '8node_mvar_diff_top': ['coupling_matrix', 'noise_corr', 'time_lag', 'npoints'],
#                        '8node_kuramoto': ['coupling', 'beta', 'time_lag', 'npoints'],
#                        '256node_kuramoto': ['coupling', 'beta', 'time_lag', 'npoints']}

# measure_variables =   {'causal_emergence_phiid': ['micro', 'redundancy_func', 'time_lag'],
#                        'causal_emergence_practical': ['macro', 'micro',  'time_lag'],
#                        'dynamical_independence': ['macro', 'micro',  'time_lag'],
#                        'g_emergence': ['macro', 'micro', 'time_lag']}

#%%

# compute emergence for all parameter combinations
emergence_df = ecmc.compute_emergence(model_functions, model_variables, emergence_measures, measure_variables, parameters)


            
    


    
    


