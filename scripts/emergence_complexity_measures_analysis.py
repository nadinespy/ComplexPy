#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:55:56 2021

@author: nadinespy

This script calculates emergence capacity using ecmc.compute_emergence() and saves
everything in a pandas dataframe.

""" 

import os
from oct2py import Oct2Py
import numpy as np
import os.path as op
from importlib import reload 
import pandas as pd
import pickle
import random
from itertools import product
from functools import partial

oc = Oct2Py()
# TODO: make lines only ~80 long
    
 
#%% 
if __name__ == "__main__":
    # TODO: make library installable
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
#emergence_measures = ["causal_emergence_phiid", "causal_emergence_practical"] #, "dynamical_independence", "g_emergence"]


def get_results_for_measure(measure_func, measure_params, data, measure_name):
    emergence_df_temp = []
    for params in product(*[params for pname, params in measure_param_dict.items()]):
        temp_param_dict = {param_name: param for param_name, param in zip(measure_param_dict, params)} # just add variable names to param combination

        emergence_result = measure_func(data, **temp_param_dict)
        # TODO: refactor so it uses dict and only build dataframe at the end 
        
        if len(emergence_result) > 1:
            for key in emergence_result:
                df_temp = pd.DataFrame({'value': [emergence_result[key]], 'measure': [key],
                                        **{pname: [p] for pname, p in temp_param_dict.items()}})
                emergence_df_temp.append(df_temp)
                
        else:
            df_temp = pd.DataFrame(df_temp = pd.DataFrame({'value': [emergence_result], 'measure': [measure_name],
                                    **{pname: [p] for pname, p in temp_param_dict.items()}}))
            emergence_df_temp.append(df_temp)
    return pd.concat(emergence_df_temp, ignore_index = True)


def generate_two_node_data(coupling_vec=None, npoints=None, time_lag=None, noise_corr_vec=None):
    coupling_matrix = np.matrix([[coupling_vec, coupling_vec], [coupling_vec, coupling_vec]])
    sim_data = ecmc.mvar_sim_data(coupling_matrix, npoints = npoints, time_lag = time_lag, err = noise_corr_vec)
    return sim_data
    
emergence_measures = {
    "causal_emergence_phiid": ecmc.causal_emergence_phiid,}
    #"causal_emergence_practical": ecmc.causal_emergence_practical} #, "dynamical_independence", "g_emergence"]

# model dict contains model: data_function pairs, where data_function generates the data for this model
model_dict = {"2node": generate_two_node_data}


parameter_dict = {"time_lag": [1, 3], 
"coupling_vec": np.linspace(0.045, 0.45, num = 10),
"noise_corr_vec": np.linspace(0.01, 0.9, num = 10),
"redundancy_func": ['mmi','ccs'],
"npoints": [2000]
}

# TODO: variable names need to be the same as parameter names in the measure functions
measure_variables = {"causal_emergence_phiid": ["redundancy_func", "time_lag"]}

# needs to be the same name as above in model_dict
model_variables = {"2node": ["coupling_vec", "noise_corr_vec", "time_lag", "npoints"]}

# ----------------------------------------------------------------------------
# 2-node networks with differing noise correlation & coupling strength
# ----------------------------------------------------------------------------

from functools import partial

random.seed(10)

# WAS DONE
# TODO: in for loops separate parameters for data generation and parameters for different emergence parameters
# WAS DONE

# TODO: named product generator for dict of iterables
def named_product(ddict): pass

big_df_list = []

for model in model_dict:
    for params in product(*[            # params is one parameter combinaton from list generated below
            parameter_dict[param_name] for param_name in model_variables[model]]):  #this line give a list, where first element are the 100 couplings
        temp_param_dict = {param_name: param for param_name, param in zip(model_variables[model], params)} # just add variable names to param combination
        generated_data = model_dict[model](**temp_param_dict) # generate data for this parameter combination
        for measure in emergence_measures: # now generate results for each measure
            measure_param_dict = {
                param_name: parameter_dict[param_name] for param_name in measure_variables[measure] if param_name not in temp_param_dict}
            data_params_for_measure = {param_name: param for param_name, param in temp_param_dict.items() if param_name in measure_variables[measure]}
            partial_measure_func = partial(emergence_measures[measure], **data_params_for_measure)
            temp_df = get_results_for_measure(emergence_measures[measure], measure_param_dict, generated_data, measure)
            # now add data parameters to dataframe
            temp_df = temp_df.assign(**temp_param_dict)
            big_df_list.append(temp_df)

b = pd.concat(big_df_list, ignore_index = True)
#            # TODO: below should be in a function
#            for measure_params in product(*measure_param_dict.values()):
#                temp_param_dict_ms = {param_name: param for param_name, param in zip(measure_param_dict, params)}
#                # now put together the data params and measure params and let the measure func sort them out
#                measure_result = emergence_measures[measure](**{**temp_param_dict_ms, **temp_param_dict})
    


# params: (0.045, 0.01, 1, 2000)
# param: 0.045
# model_variables[model]: ['coupling_vec', 'noise_corr_vec', 'time_lags', 'npoints']
# mode: "2node"
# param_name: 'coupling_vec'


    
    



    
    


