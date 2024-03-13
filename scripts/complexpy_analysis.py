# %%
import os
import numpy as np

if __name__ == '__main__':
    

    # import libraries

    #os.chdir('/complexpy')
    import complexpy as cp 
    #os.chdir('data_simulation')
    import complexpy.data_simulation as ds
    
    pathout_plots = '../results/plots/'
    pathout_analyses = '../results/analyses/'

    # if data exists
    pathin_data = '../data/'

    # once empirical_data module exists:
    # import empirical_data as ed


# %%
from complexpy import shannon_wpe

#cp.shannon_wpe()

#print(cp.__all__)
dir(cp)

#from complexpy import shannon_wpe
#from data_simulation import generate_2node_mvar_data

# %%

# -----------------------------------------------------------------------------
# MODEL & MEASURE PARAMETERS IN PANDAS DATAFRAME
# -----------------------------------------------------------------------------

# MODEL VARIABLES ENTIRELY SPECIFIED BY USER:
    
# model:                                            '2node_mvar'
#                                                   '8node_mvar_diff_top'
#                                                   '8node_mvar_global_coup'
#                                                   '8node_mvar_er'
#                                                   '8node_kuramoto'
#                                                   '256node_kuramoto'

# noise_corr:                                       100 values (noise correlations) going from  
#                                                   0.01 to 0.9 with equal steps between them

# beta:                                             100 values (phase lag parameters) going from h 
#                                                   0.01 to 0.4 wit equal steps between them

# coupling:         for '2node_mvar':               100 values (coupling strengths) going from 
#                                                   0.045 to 0.45 with equal steps between them 
#
#                   for '8node_mvar_diff_top':      7 distinctly different connectivity matrices:  
#                                                   'optimal_A' 
#                                                   'optimal_B'
#                                                   'small_world'
#                                                   'two_communities'
#                                                   'fully_connected'
#                                                   'ring'
#                                                   'uni_ring'
#
#                   for '8node_mvar_global_coup' 
#                   & '8node_mvar_er':              100 values (global coupling factors) going from 
#                                                   0.05 to 0.9 with equal steps between them

# density:                                          100 values (densities) going from  
#                                                   0.05 to 0.9 with equal steps between them

# macro:            time-series (of length npoints) of macro variable: 
#                   for MVAR models:                sum_micro_mvar (sum of the micro variables)
#
#                   for Kuramoto oscillators:       pair_sync (global average pairwise synchrony)
#                                                   sigma_chi (variance of synchrony of communities)

# micro:            time-series (of length npoints) of micro variables:   
#                   for MVAR models:                raw_micro_mvar (raw values of nodes in MVAR network)

#                   for Kuramoto oscillators:       raw_val_kuramoto (cosine of phases)
#                                                   phase_kuramoto (phases)
#                                                   sync_kuramoto (synchronies of communities)
#                                                   sync_bin (binarized synchronies of communities)


# time_lag:                                         1, 10, 100 


# MEASURE VARIABLES SPECIFIED IN COMPLEXPY LIBRARY:
    
# measure:                                          'phiid_wpe' 
#                                                   (dict with phiid_wpe,  
#                                                   phiid_dc, phiid_cd)
#                                                   'shannon_wpe' 
#                                                   (dict with causal_emergence_pract,  
#                                                   downward_causation_pract, causal_decoupling_pract)
#                                                   'dynamical_independence'
#                                                   'g_emergence'

# red_func:                                  'mmi'
#                                                   'ccs'      

# time_lag:                                         1, 10, 100 

# value:                                            value of emergence measure


# -----------------------------------------------------------------------------
# ALLOCATE MODEL & MEASURE PARAMETERS IN RESPECTIVE DICTIONARIES 
# -----------------------------------------------------------------------------

# model-function pairs where keys give the model and values give the corresponding function for simulation;
# keys in model_functions and model_variables need to be the same 
model_functions =       {'2node_mvar':              ds.generate_2node_mvar_data}

# measure-function pairs, where keys give the measure, and values the corresponding function;
# keys in emergence_measures and measure_variables need to be the same
#emergence_functions =    {'phiid_wpe':              cp.phiid_wpe,
#                          'shannon_wpe':            cp.shannon_wpe} 

emergence_functions =    {'shannon_wpe':            cp.shannon_wpe}

# model-variable pairs where keys give the model and values give the corresponding parameters of the model;
# each key *has* to include 'micro_func_mvar'in the parameters; depending on which measures are specified in 
# emergence_measures, it may also need to include 'macro_func_mvar' 
model_variables =       {'2node_mvar':              ['coupling', 'noise_corr', 'time_lag_for_model', 'npoints', 
                                                         'macro_func_mvar', 'micro_func_mvar']}

# variable names need to be the same as parameter names in the measure functions; each key *has* to include 
# 'micro' in the parameters; depending on which measures are specified in emergence_measures, it may also 
# need to include 'macro' 
#measure_variables =     {'phiid_wpe':               ['micro', 'red_func', 'time_lag_for_measure'],
#                         'shannon_wpe':             ['micro', 'macro', 'time_lag_for_measure']}

measure_variables =     {'shannon_wpe':             ['micro', 'macro', 'time_lag_for_measure']}

# all parameters relevant for either measures or data generation; will need to include keys and values only 
# for functions for macro and micro variables, not for macro and micro variables themselves
parameters =            {'time_lag_for_model':      [10, 100], 
                         'time_lag_for_measure':    [10, 100],
                         'coupling':                np.linspace(0.045, 0.45, num = 10),
                         'noise_corr':              np.linspace(0.01, 0.9, num = 10),
                         'red_func':                ['mmi','ccs'],
                         'npoints':                 [2000],
                         'macro_func_mvar':         [ds.sum_micro_mvar],
                         'micro_func_mvar':         [ds.raw_micro_mvar]}

# FINAL GOAL:
# emergence_measures =  {'phiid_wpe':      cp.phiid_wpe, 
#                        'shannon_wpe':  cp.shannon_wpe, 
#                        'dynamical_independence':      cp.dynamical_independence, 
#                        'g_emergence':                 cp.g_emergence}

# model_functions =     {'2node_mvar':                  ds.generate_2node_mvar_data,
#                        '8node_mvar_global_coup':      ds.generate_8node_global_coup_data, 
#                        '8node_mvar_er':               ds.generate_8node_mvar_er_data,
#                        '8node_mvar_diff_top':         ds.generate_8node_mvar_diff_top_data,
#                        '12node_kuramoto':             ds.generate_12node_kuramoto,
#                        '256node_kuramoto':            ds.generate_256node_kuramoto}

# data = load some data

# load file for different 8-node MVAR architectures
# file_to_read = open(data_pathin+r'/various_nets.pkl', 'rb') 
# various_nets = pickle.load(file_to_read) 

# if data is simulated:
# parameters =          {'time_lag':                    [1, 10, 100], 
#                        'coupling':                    np.linspace(0.045, 0.45, num = 10),
#                        'noise_corr':                  np.linspace(0.01, 0.9, num = 10),
#                        'red_func':             ['mmi','ccs'],
#                        'npoints':                     [2000, 10000],
#                        '8node_architectures':         various_nets,
#                        'global_coupling':             np.linspace(0.05, 0.9, num = 10),
#                        'density_vec':                 np.linspace(0.05, 0.9, num = 10),
#                        'macro_func_mvar':             [ds.sum_micro_mvar],
#                        'micro_func_mvar':             [ds.raw_val_mvar],
#                        'macro_func_kuramoto':         [ds.sigma_chi_kuramoto, ds.pair_sync_kuramoto],
#                        'micro_func_kuramoto':         [ds.raw_val_kuramoto, ds.phase_kuramoto, 
#                                                        ds.sync_kuramoto, ds.sync_bin_kuramoto]}

# if data is empirical:
# parameters =          {'time_lag':                    [1, 10, 100], 
#                        'red_func':             ['mmi','ccs'],
#                        'npoints':                     [2000, 10000],
#                        'macro_func_mvar':             [ed.sum_micro_data],
#                        'micro_func_mvar':             [ed.raw_val_data]}

# model_variables =     {'2node_mvar':                  ['coupling', 'noise_corr', 'time_lag', 'npoints', 
#                                                        'macro_func_mvar', 'micro_func_mvar'], 
#                        '8node_mvar_er':               ['density_vec', 'noise_corr', 'time_lag', 'npoints', 
#                                                        'macro_func_mvar', 'micro_func_mvar'],
#                        '8node_mvar_global_coup':      ['coupling', 'noise_corr', 'time_lag', 'npoints', 
#                                                        'macro_func_mvar', 'micro_func_mvar'],
#                        '8node_mvar_diff_top':         ['coupling_matrix', 'noise_corr', 'time_lag', 
#                                                        'npoints', 'macro_func_mvar', 'micro_func_mvar'],
#                        '12node_kuramoto':             ['coupling', 'beta', 'time_lag', 'npoints', 
#                                                        'macro_func_kuramoto', 'micro_func_kuramoto'],
#                        '256node_kuramoto':            ['coupling', 'beta', 'time_lag', 'npoints', 
#                                                        'macro_func_kuramoto', 'micro_func_kuramoto']}

# measure_variables =   {'phiid_wpe':      ['micro', 'red_func', 'time_lag'],
#                        'shannon_wpe':  ['macro', 'micro', 'time_lag'],
#                        'dynamical_independence':      ['macro', 'micro', 'time_lag'],
#                        'g_emergence':                 ['macro', 'micro', 'time_lag']}


# %%

# compute emergence for all parameter combinations - ONLY ONE LINE OF CODE!

# if data is simulated
emergence_df = cp.compute_emergence(model_functions, model_variables, emergence_functions, measure_variables, parameters)

# if data is empirical
# emergence_df = cp.compute_emergence(data, emergence_functions, measure_variables, parameters)

# it actually needs to be:

# if data is empirical:
# emergence_df = cp.compute_emergence(emergence_functions, measure_variables, data=data, parameters)

# if data is simulated:
# emergence_df = cp.compute_emergence(emergence_functions, measure_variables, model_functions=model_functions, model_variables=model_variables, parameters)




            
    


    
    




# %%
from importlib import reload 
reload(cp)
reload(ds)


