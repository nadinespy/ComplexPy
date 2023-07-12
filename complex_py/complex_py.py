"""Add docstring: module for ...

Functions:
  causal_emergence_phiid - returns ...
  causal_emergence_practical - ...
  ...
"""

import os
import numpy as np
#from .due import due, Doi
from oct2py import octave as oc 
from itertools import product
import pandas as pd
import matlab.engine

# define Matlab engine
eng = matlab.engine.start_matlab()

# -----------------------------------------------------------------------------
# CAUSAL EMERGENCE (PHIID & PRACTICAL)
# -----------------------------------------------------------------------------


def causal_emergence_phiid(data_dict, time_lag = 1, redundancy_func = 'mmi'):
    """
    Purpose : Compute PhiID-based Causal Emergence.
    
    Parameters
    ----------
    data_dict : dictionary where 'micro' is key, and float array gives values 
        Time-series of micro variables.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is 1.
    redundancy_func : string, optional
        Redundancy function to do a PhiID. The default is 'mmi'.

    Returns
    -------
    causal_emergence_phiid_dict : dictionary where keys are 
        'causal_emergence_phiid', 'downward_causation_phiid', 
        'causal_decoupling_phiid', and value is float
        Causal emergence, downward causation, causal decoupling based on PhiID.
    """
    #TODO: change to isinstance
    if not isinstance(data_dict, dict):
        raise ValueError('data_dict is not a dict') 
    if type(time_lag) != int:
        raise ValueError('time_lag is not int')
    if type(redundancy_func) != str:
        raise ValueError('redundancy_func is not a str')
    
    micro = data_dict['micro']
    if micro.shape[0] < 2 and micro.shape[1] < 2:
        raise ValueError('micro has less than 2 rows and less than 2 columns')
    
    if np.isnan(micro).any() != True:
        phiid = phiid_2sources_2targets(micro, time_lag = 1, redundancy_func = 'mmi')
        phiid_dict = {'rtr': phiid.rtr, 'rtx': phiid.rtx, 'rty': phiid.rty, 'rts': phiid.rts, 
                      'xtr': phiid.xtr, 'xtx': phiid.xtx, 'xty': phiid.xty, 'xts': phiid.xts, 
                      'ytr': phiid.ytr, 'ytx': phiid.ytx, 'yty': phiid.yty, 'yts': phiid.yts, 
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
    
        emergence_capacity_phiid =      phiid_dict["str"] + phiid_dict["stx"] + phiid_dict["sty"] + \
                                        phiid_dict["sts"]
        downward_causation_phiid =      phiid_dict["str"] + phiid_dict["stx"] + phiid_dict["sty"]
        causal_decoupling_phiid =       emergence_capacity_phiid - downward_causation_phiid

    
    else: 
        emergence_capacity_phiid =      float('NaN')
        downward_causation_phiid =      float('NaN')
        causal_decoupling_phiid =       float('NaN')

    causal_emergence_phiid_dict =   {'causal_emergence_phiid': emergence_capacity_phiid, 
                                     'downward_causation_phiid': downward_causation_phiid, 
                                     'causal_decoupling_phiid': causal_decoupling_phiid}

    return causal_emergence_phiid_dict

def causal_emergence_practical(data_dict, time_lag = 1):
    """
    Purpose : Compute Shannon-based Causal Emergence.
    
    Parameters
    ----------
    data_dict : dictionary where 'micro' and 'macro' are keys, and float arrays give values 
        Time-series of macro and micro variables.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is 1.

    Returns
    -------
    causal_emergence_practical_dict : dictionary where keys are 
        'causal_emergence_pract', 'downward_causation_pract', 
        'causal_decoupling_pract', and value is float
        Causal emergence, downward causation, causal decoupling based on 
        standard Shannon information.

    """
    
    if type(data_dict) != dict:
        raise ValueError('data_dict is not a dict')
    if type(time_lag) != int:
        raise ValueError('time_lag is not int')
    
    micro = data_dict['micro'].T
    macro = data_dict['macro']
    
    if isinstance(macro[1], int) == False:
        macro = np.expand_dims(macro, axis = 1)
    
    if micro.shape[0] < 2 and micro.shape[1] < 2:
        raise ValueError('micro has less than 2 rows and less than 2 columns')
    if macro.shape[0] < 2 and macro.shape[1] != 1:
        raise ValueError('macro has less than 2 rows and more than 2 columns')

    file_path = os.path.abspath(os.path.dirname(__file__))
    oc.addpath(file_path + '/practical_measures_causal_emergence')  
    oc.eval('pkg load statistics') 
        
    causal_emergence_pract =        oc.EmergencePsi(micro, macro, time_lag, 'Gaussian')
    downward_causation_pract =      oc.EmergenceDelta(micro, macro, time_lag, 'Gaussian') 
    causal_decoupling_pract =       oc.EmergenceGamma(micro, macro, time_lag, 'Gaussian')
    
    causal_emergence_pract_dict = {'causal_emergence_pract': causal_emergence_pract, 
                                   'downward_causation_pract': downward_causation_pract, 
                                   'causal_decoupling_pract': causal_decoupling_pract}
    
    return causal_emergence_pract_dict
    
def phiid_2sources_2targets(micro, time_lag = 1, redundancy_func = 'mmi'):
    """
    Purpose : Compute Integrated Information Decomposition.
    
    Parameters
    ----------
    micro : float array
        Time-series of micro variables.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is 1.
    redundancy_func : string, optional
        Redundancy function to do a PhiID. The default is 'mmi'.

    Returns
    -------
    phiid : Matlab struct
        Emergence capacity, downward causation, causal decoupling.

    """
    
    if type(time_lag) != int:
        raise ValueError('time_lag is not int')
    if type(redundancy_func) != str:
        raise ValueError('redundancy_func is not a str')
    if micro.shape[0] < 2 and micro.shape[1] < 2:
        raise ValueError('micro has less than 2 rows and less than 2 columns')
        
    if np.isnan(micro).any() !=  True:
        
        file_path = os.path.abspath(os.path.dirname(__file__))
        eng.chdir(file_path+'/phiid') 
        eng.javaaddpath(file_path + '/phiid/infodynamics.jar') 
        eng.eval('pkg load statistics') 
        
        micro = matlab.double(micro.tolist())
        time_lag = matlab.double(time_lag.tolist())
        
        phiid = eng.PhiIDFull(micro, time_lag, redundancy_func)
        eng.chdir(file_path)

        return phiid
        
    else: 
        return float('NaN')
    

# -----------------------------------------------------------------------------
# DYNAMICAL INDEPENDENCE
# -----------------------------------------------------------------------------

# ...

# -----------------------------------------------------------------------------
# G-EMERGENCE
# -----------------------------------------------------------------------------
    
# ...

# -----------------------------------------------------------------------------
# PARAMETER SWEEP
# -----------------------------------------------------------------------------

def get_result_for_measure(measure_func, measure_params_dict, data_dict, measure_name):                          
    """
    Purpose : Compute Integrated Information Decomposition.
    
    Parameters
    ----------
    measure_func : function
        Function to calculate a measure.
    measure_params_dict : dictionary
        Dictionary with measure parameters.
    data_dict : dictionary
        Dictionary with model parameters.
    measure_name : string
	Measure.
    Returns
    -------
    emergence_df_temp : dataframe
        Includes measure, measure and model parameters.

    """
    
    emergence_df_temp = []
    
    if type(data_dict) != dict:
        raise ValueError('data_dict is not a dict')
    if not callable(measure_func):
        raise ValueError('measure_func is not a function')
    if type(measure_params_dict) != dict:
        raise ValueError('measure_params_dict is not a dict')
    if type(measure_name) != str:
        raise ValueError('measure_name is not a str')
    
    for params in product(*[params for pname, params in measure_params_dict.items()]):
        params_dict = {param_name: param for param_name, param in zip(measure_params_dict, params)}
        emergence_result = measure_func(data_dict, **params_dict)
                
        for key in emergence_result:
            df_temp = pd.DataFrame({'value': [emergence_result[key]], 'measure': [key], 
                                    **{pname: [p] for pname, p in params_dict.items()}})
            emergence_df_temp.append(df_temp)
            
    return pd.concat(emergence_df_temp, ignore_index = True)

def compute_emergence(model_functions, model_variables, emergence_functions, measure_variables, parameters):
    """
    Purpose : Compute all measures for all measure and model parameters.
    
    Parameters
    ----------
    model_functions : dictionary
        Dictionary with function names and functions.
    model_variables : dictionary
        Dictionary with model variables.
    emergence_functions : dictionary
        Dictionary with function names and functions.
    measure_variables : dictionary
	Dictionary with measure variables.
    parameters : dictionary
        All measure and model parameters.
        
    Returns
    -------
    emergence_df : dataframe
        Includes all measures, and measure and model parameters.

    """
    
    emergence_df_temp = []
    
    if type(model_functions) != dict:
        raise ValueError('model_functions is not a dict')
    if type(emergence_functions) != dict:
        raise ValueError('emergence_functions is not a dict')
    if type(model_variables) != dict: 
        raise ValueError('model_variables is not a dict')
    if type(measure_variables) != dict: 
        raise ValueError('measure_variables is not a dict')
    if type(parameters) != dict: 
        raise ValueError('parameters is not a dict')
    
    # assert that value is a list
    if type(list(model_variables.values())[0]) != list:
        raise ValueError('value of model_variables is not a list')     
    if type(list(measure_variables.values())[0]) != list:
        raise('value of measure_variables is not a list') 
      
    # assert that each element in list is str
    for a_list in list(measure_variables.values()):
        for item in a_list:
            if type(item) != str: 
                raise ValueError('at least one list element of value of measure_variables is not str') 
           
    for a_list in list(model_variables.values()):
        for item in a_list:
            if type(item) != str: 
                raise ValueError('at least one list element of value of model_variables is not str') 
                
    # TODO: assert that each value in model_functions and emergence_functions is a function
        
  
    for model in model_functions:
        for params in product(*[parameters[param_name] for param_name in model_variables[model]]):          
            model_params_dict = {param_name: param for param_name, param in 
                                 zip(model_variables[model], params)}  
            
            data_dict = model_functions[model](**model_params_dict)   
                                          
            for measure in emergence_functions:   
                
                # replace key 'micro' in measure_variables by 'micro_func_mvar' so that we can take 
                # value of 'micro_func_mvar' in parameters (this is done below)
                search_word = 'micro'
                for key, val in parameters.items():
                    if search_word in key:
                        new_key = key
            
                for key, val in measure_variables.items():                        
                    for item in val:
                        if search_word in item:
                            index = val.index(item)
                            measure_variables[key][index] = new_key
                            
                # if existent, replace key 'macro' in measure_variables by 'macro_func_mvar'
                # so that we can take value of 'macro_func_mvar' in parameters (this is done below)
                search_word = 'macro'
                for key, val in parameters.items():
                    if search_word in key:
                        new_key = key
                        
                if new_key != []:
                    for key, val in measure_variables.items():                        
                        for item in val:
                            if search_word in item:
                                index = val.index(item)
                                measure_variables[key][index] = new_key
                
                
                                             
                measure_param_dict = {param_name: parameters[param_name] for param_name in 
                                      measure_variables[measure] if param_name not in model_params_dict}
                df_temp = get_result_for_measure(emergence_functions[measure], measure_param_dict, 
                                                 data_dict, measure)
                df_temp = df_temp.assign(**{key: value if not callable(value) 
                                            else value.__name__ for key, value in model_params_dict.items()})
                
                emergence_df_temp.append(df_temp)

    emergence_df = pd.concat(emergence_df_temp, ignore_index = True)
    
    return emergence_df




