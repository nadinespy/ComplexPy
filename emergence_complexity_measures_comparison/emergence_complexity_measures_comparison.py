import os
import numpy as np
#from .due import due, Doi
from oct2py import octave as oc 


#__all__ = ["causal_emergence_phiid", "causal_emergence_practical", "mvar_sim_data", "phiid_full", "cumgauss"] # "compute_emergence", 


# Use duecredit (duecredit.org) to provide a citation to relevant work to
# be cited. This does nothing, unless the user has duecredit installed,
# And calls this with duecredit (as in `python -m duecredit script.py`):
# due.cite(Doi("10.1167/13.9.30"),
#          description="Template project for small scientific Python projects",
#          tags=["reference-implementation"],
#          path='emergence_complexity_measures_comparison')

# alternative FIXME: replace named keyword arguments with **kwargs
#def compute_emergence(measure, data, time_lag = 1, redundancy_func = 'mmi', macro_variable = None):
#     emergence = globals()[measure](data, time_lag = time_lag, redundancy_func = redundancy_func, macro_variable = macro_variable)
#     return emergence


# TODO: short summary on top of docstring of function purpose
def causal_emergence_phiid(data, time_lag = 1, redundancy_func = 'mmi', macro_variable = None):
    """
    
    
    Parameters
    ----------
    data : float
        DESCRIPTION.
    tau : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is None.
    redundancy_func : string, optional
        Redundancy function to do a PhiID. The default is None.
    macro_variable : float, optional
        Candidate emergent macro variable. The default is None.
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
    
    if np.isnan(data).any() != True:
        phiid = phiid_full(data, time_lag = 1, redundancy_func = 'mmi')
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

        causal_emergence_phiid_dict = {'phiid_emergence_capacity': emergence_capacity_phiid, 'phiid_downward_causation': downward_causation_phiid, 'phiid_causal_decoupling': causal_decoupling_phiid}
    
        return causal_emergence_phiid_dict
    
    else: 
        emergence_capacity_phiid = float('NaN')
        downward_causation_phiid = float('NaN')
        causal_decoupling_phiid = float('NaN')

        causal_emergence_phiid_dict = {'phiid_emergence_capacity': emergence_capacity_phiid, 'phiid_downward_causation': downward_causation_phiid, 'phiid_causal_decoupling': causal_decoupling_phiid}
    
        return causal_emergence_phiid_dict

def causal_emergence_practical(data, macro_variable = None):
    """
    
    Parameters
    ----------
    data : float
        DESCRIPTION.
    tau : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is None.
    redundancy_func : string, optional
        Redundancy function to do a PhiID. The
    macro_variable : float, optional
        Candidate emergent macro variable. The default is None.
    phiid_path : string, optional
        Path to PhiID files. The default is None.

    Returns
    -------
    causal_emergence_practical_dict : dictionary
        Emergence capacity, downward causation, causal decoupling.
    
    Notes
    -----
    ...

    """
    #........ to be filled
    return None
    
def phiid_full(data, time_lag = 1, redundancy_func = 'mmi'):
    
    if np.isnan(data).any() !=  True:
        current_path = os.getcwd()
        #print(current_path)
        oc.chdir(current_path+'/emergence_complexity_measures_comparison/phiid')
        oc.addpath(current_path+'/emergence_complexity_measures_comparison/practical_measures_causal_emergence')  
        oc.javaaddpath(current_path+'/emergence_complexity_measures_comparison/phiid/infodynamics.jar')
        oc.eval('pkg load statistics') 
        
        phiid = oc.PhiIDFull(data, time_lag, redundancy_func)
        os.chdir(current_path)
        
        return phiid
        
    else: 
        return float('NaN')
    

def mvar_sim_data(coupling_matrix, npoints = 2000, time_lag = 1, err = 0.1):
    
    if np.isnan(coupling_matrix).any() != True:
        # Is there a way to direct to that folder without taking absolute paths?
        current_path = os.getcwd()
        #print('This is the current path: '+current_path)
        os.chdir(current_path+'/emergence_complexity_measures_comparison/phiid')
    
        oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/phiid')    
        oc.javaaddpath(current_path+'/emergence_complexity_measures_comparison/phiid/infodynamics.jar');
        oc.eval('pkg load statistics') 
    
        sim_data = oc.statdata_coup_errors1(coupling_matrix, npoints, time_lag, err)
        os.chdir(current_path)
        
        return sim_data
    
    else: 
        return float('NaN')


