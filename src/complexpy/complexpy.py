"""Add docstring: module for ...

Functions:
  phiid_wpe - returns ...
  shannon_wpe - ...
  ...
"""

import os
import numpy as np
from itertools import product
import pandas as pd
import matlab.engine

# define Matlab engine
eng = matlab.engine.start_matlab()

# -----------------------------------------------------------------------------
# CAUSAL EMERGENCE (PHIID & PRACTICAL)
# -----------------------------------------------------------------------------


def phiid_wpe(data_dict, time_lag_for_measure = 1, red_func = 'mmi'):
    """
    Purpose : Compute PhiID-based Causal Emergence.
    
    Parameters
    ----------
    data_dict : dictionary where 'micro' is key, and float array gives values 
        Time-series of micro variables.
    time_lag_for_measure : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is 1.
    red_func : string, optional
        Redundancy function to do a PhiID. The default is 'mmi'.

    Returns
    -------
    phiid_wpe_dict : dictionary where keys are 
        'phiid_wpe', 'phiid_dc', 
        'phiid_cd', and value is float
        Causal emergence, downward causation, causal decoupling based on PhiID.
    """

    if not isinstance(data_dict, dict):
        raise ValueError('data_dict is not a dict') 
    if 'micro' not in data_dict:
        raise ValueError("key 'micro' is missing in data_dict")

    if type(time_lag_for_measure) != int or time_lag_for_measure < 1:
        raise ValueError('time_lag_for_measure either is not int, or it is below one')
    if type(red_func) != str:
        raise ValueError('red_func is not a str')
    
    micro = data_dict['micro']
    if micro.shape[0] < 2 and micro.shape[1] < 2:
        raise ValueError('micro has less than 2 rows and less than 2 columns')
    
    if np.isnan(micro).any() != True:
        phiid_dict = phiid_2sources_2targets(micro, time_lag_for_measure = 1, red_func = 'mmi')
        
        if not isinstance(phiid_dict, dict):
            raise ValueError('phiid_dict is not a dict') 
    
        # check if all required_keys exist in phiid_dict
        required_phiid_dict_keys = ['rtr', 'sts', 'rtx', 'rty', 'rts', 'xtr', 'xtx', 'xty', 'xts', 'ytr', 
                           'ytx', 'yty', 'yts', 'str', 'stx', 'sty']

        if not all(key in phiid_dict for key in required_phiid_dict_keys):
            missing_keys = [key for key in required_phiid_dict_keys if key not in phiid_dict]
            raise ValueError(f"Keys {missing_keys} are required in phiid_dict")

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
    
        phiid_wpe = phiid_dict["str"] + phiid_dict["stx"] + phiid_dict["sty"] + phiid_dict["sts"]
        phiid_dc = phiid_dict["str"] + phiid_dict["stx"] + phiid_dict["sty"]
        phiid_cd = phiid_wpe - phiid_dc
    
    else: 
        phiid_wpe = float('NaN')
        phiid_dc = float('NaN')
        phiid_cd = float('NaN')

    phiid_wpe_dict = {'phiid_wpe': phiid_wpe, 'phiid_dc': phiid_dc, 'phiid_cd': phiid_cd}

    return phiid_wpe_dict

def shannon_wpe(data_dict, time_lag_for_measure = 1):
    """
    Purpose : Compute Shannon-based Causal Emergence.
    
    Parameters
    ----------
    data_dict : dictionary where 'micro' and 'macro' are keys, and float arrays give values 
        Time-series of macro and micro variables.
    time_lag_for_measure : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is 1.

    Returns
    -------
    shannon_wpe_dict : dictionary where keys are 
        'causal_emergence_pract', 'downward_causation_pract', 
        'causal_decoupling_pract', and value is float
        Causal emergence, downward causation, causal decoupling based on 
        standard Shannon information.

    """
    
    if type(data_dict) != dict:
        raise ValueError('data_dict is not a dict')
    if type(time_lag_for_measure) != int or time_lag_for_measure < 1:
        raise ValueError('time_lag_for_measure either is not int, or it is below one')
    
    micro = data_dict['micro'].T
    macro = data_dict['macro']
    
    if isinstance(macro[1], int) == False:
        macro = np.expand_dims(macro, axis = 1)
    
    if micro.shape[0] < 2 and micro.shape[1] < 2:
        raise ValueError('micro has less than 2 rows and less than 2 columns')
    if macro.shape[0] < 2 and macro.shape[1] != 1:
        raise ValueError('macro has less than 2 rows and more than 2 columns')

    #file_path = os.path.abspath(os.path.dirname(__file__))
    #oc.addpath(file_path + '/practical_measures_causal_emergence')  

    #eng.eval('pkg load statistics') 
    eng.addpath('src/shannon_wpe')
        
    shannon_wpe = eng.EmergencePsi(micro, macro, time_lag_for_measure, 'Gaussian')
    shannon_dc = eng.EmergenceDelta(micro, macro, time_lag_for_measure, 'Gaussian') 
    shannon_cd = eng.EmergenceGamma(micro, macro, time_lag_for_measure, 'Gaussian')
    
    shannon_wpe_dict = {'shannon_wpe': shannon_wpe, 
                                   'shannon_dc': shannon_dc, 
                                   'shannon_cd': shannon_cd}
    
    return shannon_wpe_dict
    
def phiid_2sources_2targets(micro, time_lag_for_measure = 1, red_func = 'mmi'):
    """
    Purpose : Compute Integrated Information Decomposition.
    
    Parameters
    ----------
    micro : float array
        Time-series of micro variables.
    time_lag_for_measure : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is 1.
    red_func : string, optional
        Redundancy function to do a PhiID. The default is 'mmi'.

    Returns
    -------
    phiid : Matlab struct
        Whole-parts emergence, downward causation, causal decoupling.

    """
    
    if type(time_lag_for_measure) != int or time_lag_for_measure < 1:
        raise ValueError('time_lag_for_measure either is not int, or it is below one')
    if type(red_func) != str:
        raise ValueError('red_func is not a str')
    if micro.shape[0] < 2 and micro.shape[1] < 2:
        raise ValueError('micro has less than 2 rows and less than 2 columns')
        
    if np.isnan(micro).any() !=  True:
        
        #file_path = os.path.abspath(os.path.dirname(__file__))
        #eng.chdir(file_path+'/phiid') 
        #eng.javaaddpath(file_path + '/phiid/infodynamics.jar') 
        #eng.eval('pkg load statistics') 

        eng.addpath('src/phiid')
        eng.javaaddpath('src/phiid/infodynamics.jar', '-end', nargout=0)
        
        micro = matlab.double(micro.tolist())
        time_lag_for_measure = matlab.double(time_lag_for_measure)
        
        phiid = eng.PhiIDFull(micro, time_lag_for_measure, red_func)
        #eng.chdir(file_path)

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
    
    for measure_params in product(*[measure_params for measure_param_name, measure_params in measure_params_dict.items()]):

        # we create a dict with measure parameters for one possible single calculation
        measure_params_dict_for_calc = {measure_param_name_for_calc: measure_param_for_calc for 
                                        measure_param_name_for_calc, measure_param_for_calc in 
                                        zip(measure_params_dict, measure_params)}
        
        emergence_result = measure_func(data_dict, **measure_params_dict_for_calc)
                
        for key in emergence_result:
            df_temp = pd.DataFrame({'value': [emergence_result[key]], 'measure': [key], 
                                    **{measure_param_name_for_calc: [measure_param_for_calc] for 
                                       measure_param_name_for_calc, measure_param_for_calc in 
                                       measure_params_dict_for_calc.items()}})
            
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
    
    # create empty list
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
            print(params)

            # we create a dict with model parameters for one possible single model instantiation
            model_params_dict = {param_name: param for param_name, param in 
                                 zip(model_variables[model], params)}  
            
            # we create a dict with micro and macro time series following one possible model instantiation
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

                # we create a dict with measure parameters with all possible values;
                # includes only those measure parameters which are not already entailed by 
                # model_params_dict   
                measure_params_dict = {param_name: parameters[param_name] for param_name in 
                                      measure_variables[measure] if param_name not in model_params_dict}
                
                # includes only measure parameters
                df_temp = get_result_for_measure(emergence_functions[measure], measure_params_dict, 
                                                 data_dict, measure)
                
                # includes both measure and model parameters
                df_temp = df_temp.assign(**{key: value if not callable(value) 
                                            else value.__name__ for key, value in model_params_dict.items()})
                
                # add df_temp to list emergence_df_temp
                emergence_df_temp.append(df_temp)

    emergence_df = pd.concat(emergence_df_temp, ignore_index = True)
    
    return emergence_df




