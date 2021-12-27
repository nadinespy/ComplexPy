import os
import numpy as np
#from .due import due, Doi
from oct2py import octave as oc 
from itertools import product
import pandas as pd


#__all__ = ["causal_emergence_phiid", "causal_emergence_practical", "mvar_sim_data", "phiid", "cumgauss"] # "compute_emergence", 

# Use duecredit (duecredit.org) to provide a citation to relevant work to
# be cited. This does nothing, unless the user has duecredit installed,
# And calls this with duecredit (as in `python -m duecredit script.py`):
# due.cite(Doi("10.1167/13.9.30"),
#          description="Template project for small scientific Python projects",
#          tags=["reference-implementation"],
#          path='emergence_complexity_measures_comparison')

# alternative FIXME: replace named keyword arguments with **kwargs
# def compute_emergence(measure, data, time_lag = 1, redundancy_func = 'mmi', macro_variable = None):
#     emergence = globals()[measure](data, time_lag = time_lag, redundancy_func = redundancy_func, macro_variable = macro_variable)
#     return emergence

# TODO: correct doc strings


# -----------------------------------------------------------------------------
# CAUSAL EMERGENCE (PHIID & PRACTICAL)
# -----------------------------------------------------------------------------


def causal_emergence_phiid(data_dict, time_lag = 1, redundancy_func = 'mmi'):
    """
    Purpose : ...
    
    Parameters
    ----------
    data : float array
        DESCRIPTION.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is None.
    redundancy_func : string, optional
        Redundancy function to do a PhiID. The default is None.
    phiid_path : string, optional
        Path to PhiID files. The default is None.

    Returns
    -------
    causal_emergence_phiid_dict : dictionary
        Emergence capacity, downward causation, causal decoupling.
        
    Notes
    -----
    ...

    """
    micro = data_dict['micro']
    
    if np.isnan(micro).any() != True:
        phiid = phiid_2sources_2targets(micro, time_lag = 1, redundancy_func = 'mmi')
        phiid_dict = {'rtr': phiid.rtr, 'rtx': phiid.rtx, 'rty': phiid.rty, 'rts': phiid.rts, 'xtr': phiid.xtr, 'xtx': phiid.xtx, \
                        'xty': phiid.xty, 'xts': phiid.xts, 'ytr': phiid.ytr, 'ytx': phiid.ytx, 'yty': phiid.yty, 'yts': phiid.yts, \
                        'str': phiid.str, 'stx': phiid.stx, 'sty': phiid.sty, 'sts': phiid.sts}
    
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
    
        emergence_capacity_phiid = phiid_dict["str"] + phiid_dict["stx"] + phiid_dict["sty"] + phiid_dict["sts"]
        downward_causation_phiid = phiid_dict["str"] + phiid_dict["stx"] + phiid_dict["sty"]
        causal_decoupling_phiid = emergence_capacity_phiid - downward_causation_phiid

        causal_emergence_phiid_dict = {'causal_emergence_phiid': emergence_capacity_phiid, 'downward_causation_phiid': downward_causation_phiid, 'causal_decoupling_phiid': causal_decoupling_phiid}
    
        return causal_emergence_phiid_dict
    
    else: 
        emergence_capacity_phiid = float('NaN')
        downward_causation_phiid = float('NaN')
        causal_decoupling_phiid = float('NaN')

        causal_emergence_phiid_dict = {'causal_emergence_phiid': emergence_capacity_phiid, 'downward_causation_phiid': downward_causation_phiid, 'causal_decoupling_phiid': causal_decoupling_phiid}
    
        return causal_emergence_phiid_dict

def causal_emergence_practical(data_dict, time_lag = 1):
    """
    Purpose : ...
    
    Parameters
    ----------
    data : float
        DESCRIPTION.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is None.
    macro : float, optional
        Candidate emergent macro variable. The default is None.

    Returns
    -------
    causal_emergence_practical_dict : dictionary
        Emergence capacity, downward causation, causal decoupling.
    
    Notes
    -----
    ...

    """
    
    micro = data_dict['micro'].T
    macro = data_dict['macro']

    file_path = os.path.abspath(os.path.dirname(__file__))
    oc.addpath(file_path + '/practical_measures_causal_emergence')  
    oc.eval('pkg load statistics') 
        
    causal_emergence_pract = oc.EmergencePsi(micro, macro, time_lag, 'Gaussian')
    downward_causation_pract = oc.EmergenceDelta(micro, macro, time_lag, 'Gaussian') 
    causal_decoupling_pract = oc.EmergenceGamma(micro, macro, time_lag, 'Gaussian')
    
    causal_emergence_pract_dict = {'causal_emergence_pract': causal_emergence_pract, 'downward_causation_pract': downward_causation_pract, 'causal_decoupling_pract': causal_decoupling_pract}
    
    return causal_emergence_pract_dict
    
def phiid_2sources_2targets(micro, time_lag = 1, redundancy_func = 'mmi'):
    """
    Purpose : ...
    
    Parameters
    ----------
    data : float
        DESCRIPTION.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is None.
    macro : float, optional
        Candidate emergent macro variable. The default is None.

    Returns
    -------
    causal_emergence_practical_dict : dictionary
        Emergence capacity, downward causation, causal decoupling.
    
    Notes
    -----
    ...

    """
        
    if np.isnan(micro).any() !=  True:
        
        file_path = os.path.abspath(os.path.dirname(__file__))
        oc.chdir(file_path+'/phiid') 
        oc.javaaddpath(file_path + '/phiid/infodynamics.jar') 
        oc.eval('pkg load statistics') 
        
        phiid = oc.PhiIDFull(micro, time_lag, redundancy_func)
        os.chdir(file_path)
        
        return phiid
        
    else: 
        return float('NaN')
    

# -----------------------------------------------------------------------------
# DYNAMICAL INDEPENDENCE
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# G-EMERGENCE
# -----------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------
# PARAMETER SWEEP
# -----------------------------------------------------------------------------

def get_result_for_measure(measure_func, measure_params_dict, data_dict, measure_name):                          
    emergence_df_temp = []
    
    for params in product(*[params for pname, params in measure_params_dict.items()]):
        params_dict = {param_name: param for param_name, param in zip(measure_params_dict, params)}
        emergence_result = measure_func(data_dict, **params_dict)
                
        for key in emergence_result:
            df_temp = pd.DataFrame({'value': [emergence_result[key]], 'measure': [key], **{pname: [p] for pname, p in params_dict.items()}})
            emergence_df_temp.append(df_temp)
    return pd.concat(emergence_df_temp, ignore_index = True)


def compute_emergence(model_functions, model_variables, emergence_measures, measure_variables, parameters):
      
    emergence_df_temp = []

    for model in model_functions:
        for params in product(*[parameters[param_name] for param_name in model_variables[model]]):          
            model_params_dict = {param_name: param for param_name, param in zip(model_variables[model], params)}  
            data_dict = model_functions[model](**model_params_dict)  
                                          
            for measure in emergence_measures:                                                                    
                measure_param_dict = {param_name: parameters[param_name] for param_name in measure_variables[measure] if param_name not in model_params_dict}
                df_temp = get_result_for_measure(emergence_measures[measure], measure_param_dict, data_dict, measure)
                df_temp = df_temp.assign(**{key: value if not callable(value) else value.__name__ for key, value in model_params_dict.items()})
                emergence_df_temp.append(df_temp)

    emergence_df = pd.concat(emergence_df_temp, ignore_index = True)
    return emergence_df






# UNDERSTANDING THE ABOVE LOOPS - EXAMPLE
# 
# GIVEN VARIABLES:
# emergence_measures =  {'causal_emergence_phiid': ecmc.causal_emergence_phiid}
# model_functions =          {'2node_mvar': generate_2node_mvar_data}

# parameters =          {'time_lag': [1, 3], 
#                        'coupling': np.linspace(0.045, 0.45, num = 10),
#                       'noise_corr': np.linspace(0.01, 0.9, num = 10),
#                       'redundancy_func': ['mmi','ccs'],
#                       'npoints': [2000]}
# measure_variables =   {'causal_emergence_phiid': ['redundancy_func', 'time_lag']}
# model_variables =     {'2node_mvar': ['coupling', 'noise_corr', 'time_lag', 'npoints']}

# WHAT THE VARIABLES IN THE LOOPS MEAN:
# params:                       can be (0.045, 0.01, 1, 2000)
# param:                        can be 0.045
# model_variables[model]:       ['coupling', 'noise_corr', 'time_lags', 'npoints']
# mode:                         '2node_mvar'
# param_name:                   can be 'coupling'
# model:                        '2node_mvar'
# model_variables[model]:       ['coupling', 'noise_corr', 'time_lag', 'npoints']
# measure:                      'causal_emergence_phiid'
# emergence_measures[measure]:  ecmc.causal_emergence_phiid
# measure_variables[measure]:   ['redundancy_func', 'time_lag']
# measure_param_dict:           can be {'time_lag': [3], 'redundancy_func': ['ccs']}                                        --> includes parameters relevant for measure
# model_params_dict:            can be {'coupling': 0.045, 'noise_corr': 0.01, 'time_lag': 1, 'npoints': 2000}      --> includes parameters relevant for data generation
# data_params_for_measure:      can be {'time_lag': [1]}                                                                    --> includes parameters relevant to both measure and data generation
# partial_measure_func:         is a function which will take parameters shared between measure and data generation as separate inputs
# df_temp:                      can be {'value': [0.0332], 'measure': ['phiid_downward_causation'], 'time_lag': [1], 'redundancy_func': ['ccs']} *before* adding data parameters, and
#                               {'value': [0.0332], 'measure': ['phiid_downward_causation'], 'time_lag': [1], 'redundancy_func': ['ccs'], ...
#                                         'coupling': [0.045], 'noise_corr': [0.01], 'time_lag': [1], 'npoints': [2000]} *after* adding data parameters


# GOING THROUGH THE LOOPS:
# for [one model, like'2node_mvar'] in [variable storing all models and corresponding data generation function, in this case model_functions]:
#     for [one parameter combination, like (0.045, 0.01, 1, 2000)] in product([all possible parameter combinations]):
#         model_params_dict = [store parameter names and parameter values in dict, like {'coupling': 0.045, 'noise_corr': 0.01, 'time_lag': 1, 'npoints': 2000}]
#         data_dict = generate_2node_mvar_data(**model_params_dict) --> generate_2node_mvar_data() will use keys as variable names and assign it the respective values
#         for [one measure, like 'causal_emergence_phiid'] in [variable which stores all measures and corresponding function to calculate it, in this case emergence_measures]:
#             measure_param_dict = [store parameter names and parameter values in dict - but only those which are not already in model_params_dict! -, like {'redundancy_func': ['ccs']}]
#             data_params_for_measure = [store parameter names and parameter values in dict - but only those which are in *both* model_params_dict and measure_param_dict, like {'time_lag': [1]}]
#             partial_measure_func = partial(emergence_measures[measure], **data_params_for_measure)
#             df_temp = get_result_for_measure(emergence_measures[measure], measure_param_dict, data_dict, measure)
#             df_temp = df_temp.assign(**model_params_dict)
#             big_df_list.append(df_temp)

# comprehensive lists:
# for params in product(*[parameters[param_name] for param_name in model_variables[model]]): for one set of parameters, take value of key of each key in model_variables of the respective model
# general way comprehensive lists work: do X for Y in Z
# product = product(*[parameters[param_name] for param_name in model_variables['2node_mvar']]) # what is the output of product()?

# BOILING DOWN THE LOOPS ONCE MORE:
# for generate_2node_mvar_data:
#     for (0.045, 0.01, 1, 2000): 
#         # we need to go from tuple of parameters to dictionary with parameter names as keys and parameters as values to use named arguments for functions 
#         model_params_dict = {'coupling': 0.045, 'noise_corr': 0.01, 'time_lag': 1, 'npoints': 2000}
#         data_dict = generate_2node_mvar_data(coupling = 0.045, npoints = 2000, time_lag = 1, noise_corr = 0.01)
    
#         for ecmc.causal_emergence_phiid:
#             # we need to go from tuple of parameters to dictionary with parameter names as keys and parameters as values to use named arguments for functions 
#             measure_param_dict = {'time_lag': [3], 'redundancy_func': ['ccs']}
#             df_temp = get_result_for_measure(ecmc.causal_emergence_phiid, measure_param_dict, data_dict, 'causal_emergence_phiid')
#             # get_result_for_measure() will be equal to {'value': [0.0332], 'measure': ['phiid_downward_causation'], 'time_lag': [1], 'redundancy_func': ['ccs']} --> includes only measure parameters!
#             df_temp = df_temp.assign(**model_params_dict)
#             # df_temp will be equal to {'value': [0.0332], 'measure': ['phiid_downward_causation'], 'time_lag': [1], 'redundancy_func': ['ccs'], ...
#                                         'coupling': [0.045], 'noise_corr': [0.01], 'time_lag': [1], 'npoints': [2000]} --> includes *both* measure and data parameters!
#             big_df_list.append(df_temp)




# UNDERSTANDING get_result_for_measures(measure_func, measure_params_dict, data, measure_name):
# function is called as: df_temp = get_result_for_measure(emergence_measures[measure], measure_param_dict, data_dict, measure) 
#
# INPUT VARIABLES:
# emergence_measures[measure] = ecmc.causal_emergence_phiid 
# measure_param_dict =          {'time_lag': [3], 'redundancy_func': ['ccs']}
# measure =                     'causal_emergence_phiid'
#                               data_dict

# WHAT THE VARIABLES IN THE LOOPS MEAN:
# params:               can be (0.045, 0.01, 1, 2000)  
# param:                can be 0.045 
# param_name:           can be 'coupling'
# model_params_dict:    can be {'time_lag': [3], 'redundancy_func': ['ccs']}
# df_temp:              can be {'value': [0.0332], 'measure': ['phiid_downward_causation'], 'time_lag': [1], 'redundancy_func': ['ccs']}
# emergence_result:     can be {'phiid_emergence_capacity': [0.0332], 'phiid_downward_causation': [0.0456], ' phiid_causal_decoupling': [0.0222]}

# GOING THROUGH THE LOOPS:
# for  [one parameter combination, like {3,'ccs'}] in product([all possible parameter combinations]): 
    # model_params_dict = [store parameter names and parameter values in dict, like {'time_lag': [3], 'redundancy_func': ['ccs']}]  # just add variable names to param combination
    # emergence_result = ecmc.causal_emergence_phiid(data_dict, **model_params_dict)
    # for key in emergence_result:
    #     df_temp = pd.DataFrame({'value': [emergence_result[key]], 'measure': [key], **{pname: [p] for pname, p in model_params_dict.items()}})
    #     emergence_df_temp.append(df_temp)
    
    # pd.concat(emergence_df_temp, ignore_index = True)

# BOILING DOWN THE LOOPS ONCE MORE:
# for {3,'ccs'}: 
#     model_params_dict = {'time_lag': [3], 'redundancy_func': ['ccs']}
#     emergence_result = 0.0465
#     for 'phiid_downward_causation':
#         df_temp = pd.DataFrame({'value': [0.0332], 'measure': ['phiid_downward_causation'], 'time_lag': [1], 'redundancy_func': ['ccs']})

# comprehensive lists:
# for params in product(*[params for pname, params in measure_param_dict.items()]): for one set of parameters, get values of keys for key and value of key in measure_param_dict

 
