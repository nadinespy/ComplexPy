import os
import numpy as np
import pandas as pd
import scipy.optimize as opt
from scipy.special import erf
from .due import due, Doi
from oct2py import octave as oc
import scipy.io as sio


# current_path = os.getcwd()
#os.chdir(current_path+'/phiid')
#oc.addpath(current_path+'practical_measures_causal_emergence')  
#oc.javaaddpath(current_path+'/phiid'+'infodynamics.jar');
#oc.eval('pkg load statistics')  





__all__ = ["causal_emergence_phiid", "compute_emergence", "statdata_coup_errors1", "phiid_full", "cumgauss"]


# Use duecredit (duecredit.org) to provide a citation to relevant work to
# be cited. This does nothing, unless the user has duecredit installed,
# And calls this with duecredit (as in `python -m duecredit script.py`):
due.cite(Doi("10.1167/13.9.30"),
         description="Template project for small scientific Python projects",
         tags=["reference-implementation"],
         path='emergence_complexity_measures_comparison')



def load_phiid_from_mat(phiid_path):
    try:
        phiid = sio.loadmat(phiid_path, squeeze_me = True, struct_as_record=False)['all_atoms_err_coup_mmi'] 
    except  KeyError:
        phiid = sio.loadmat(phiid_path, squeeze_me = True, struct_as_record=False)['all_atoms_err_coup_ccs']

    return phiid

def compute_emergence(measure, data, tau = None, redundancy_func = None, macro_variable = None, phiid_path = None):
    emergence = globals()[measure](data, tau = tau, redundancy_func = redundancy_func, macro_variable = macro_variable, phiid_path = phiid_path)
    return emergence
    

def causal_emergence_phiid(data, tau = None, redundancy_func = None, macro_variable = None, phiid_path = None):
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

    ReturnsThis script loads phiid files generated in matlab, calculates emergence capacity without using ecmc.compute_emergence() and saves
everything in a pandas dataframe.
    -------
    causal_emergence_phiid_dict : dictionary
        Emergence capacity, downward causation, causal decoupling.

    """
    phiid = load_phiid_from_mat(phiid_path)
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

    causal_emergence_phiid_dict = {'emergence_capacity': emergence_capacity_phiid, 'downward_causation': downward_causation_phiid, 'causal_decoupling': causal_decoupling_phiid}
    
    return causal_emergence_phiid_dict


def phiid_full(data, tau, redundancy_function):
    current_path = os.getcwd()
    print(current_path)
    os.chdir(current_path+'/emergence_complexity_measures_comparison/phiid')
    oc.addpath(current_path+'/emergence_complexity_measures_comparison/practical_measures_causal_emergence')  
    oc.javaaddpath(current_path+'/phiid/emergence_complexity_measures_comparison/infodynamics.jar');
    #oc.eval('pkg load statistics') 
    
    phiid = oc.PhiIDFull(data, tau, redundancy_function)
    return phiid

def statdata_coup_errors1(coupling_matrix, npoints, tau, err):
    
    # Is there a way to direct to that folder without taking absolute paths?
    current_path = os.getcwd()
    print('This is the current path: '+current_path)
    os.chdir(current_path+'results/analyses/phiid/emergence_complexity_measures_comparison/phiid')
    
    oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/phiid')    
    oc.javaaddpath(current_path+'/emergence_complexity_measures_comparison/phiid/infodynamics.jar');
    oc.eval('pkg load statistics') 
    
    sim_data = oc.statdata_coup_errors1(coupling_matrix, npoints, tau, err)
    return sim_data

# example of how to document a function

def cumgauss(x, mu, sigma):
    """
    The cumulative Gaussian at x, for the distribution with mean mu and
    standard deviation sigma.

    Parameters
    ----------
    x : float or array
       The values of x over which to evaluate the cumulative Gaussian function

    mu : float
       The mean parameter. Determines the x value at which the y value is 0.5

    sigma : float
       The variance parameter. Determines the slope of the curve at the point
       of Deflection

    Returns
    -------

    g : float or array
        The cumulative gaussian with mean $\\mu$ and variance $\\sigma$
        evaluated at all points in `x`.

    Notes
    -----
    Based on:
    http://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function

    The cumulative Gaussian function is defined as:

    .. math::

        \\Phi(x) = \\frac{1}{2} [1 + erf(\\frac{x}{\\sqrt{2}})]

    Where, $erf$, the error function is defined as:

    .. math::

        erf(x) = \\frac{1}{\\sqrt{\\pi}} \\int_{-x}^{x} e^{t^2} dt
    """
    return 0.5 * (1 + erf((x - mu) / (np.sqrt(2) * sigma)))


