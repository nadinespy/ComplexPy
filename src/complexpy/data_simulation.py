#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 17:44:25 2021

@author: nadinespy
"""

import numpy as np
import os 

import matlab.engine

# define Matlab engine
eng = matlab.engine.start_matlab()

# -----------------------------------------------------------------------------
# FUNCTIONS FOR DATA GENERATION
# -----------------------------------------------------------------------------

def generate_2node_mvar_data(coupling = None, npoints = None, time_lag_for_model = None, noise_corr = None, 
                             macro_func_mvar = None, micro_func_mvar = None):
    data_dict = dict()
    coupling_matrix = np.matrix([[coupling, coupling], [coupling, coupling]])
    sim_data = mvar_sim_data(coupling_matrix, npoints = npoints, time_lag_for_model = time_lag_for_model, noise_corr = noise_corr)

    data_dict['macro'] = macro_func_mvar(sim_data) if macro_func_mvar is not None else None
    data_dict['micro'] = micro_func_mvar(sim_data) if micro_func_mvar is not None else sim_data

    return data_dict

def mvar_sim_data(coupling_matrix, npoints = None, time_lag_for_model = None, noise_corr = None):
    """
    Purpose : ...
    
    Parameters
    ----------
    data : float
        DESCRIPTION.
    time_lag : integer, optional
        Time-lag in multivariate autoregressive time-series model. The default is None.
    macro_var : float, optional
        Candidate emergent macro variable. The default is None.

    Returns
    -------
    shannon_wpe_dict : dictionary
        Emergence capacity, downward causation, causal decoupling.
    
    Notes
    -----
    ...

    """
    
    if np.isnan(coupling_matrix).any() != True:
                
        #file_path = os.path.abspath(os.path.dirname(__file__))
        #oc.addpath(file_path)    
        #oc.eval('pkg load statistics') 
        
        #eng.eval('pkg load statistics') 
        #eng.chdir('/src')
        #os.chdir('src/phiid')
        eng.addpath('src/phiid')

        coupling_matrix = matlab.double(coupling_matrix.tolist())
        npoints = matlab.double(npoints)
        time_lag_for_model = matlab.double(time_lag_for_model)
        noise_corr = matlab.double(noise_corr)

        sim_data = eng.sim_mvar_network(npoints, noise_corr, coupling_matrix, time_lag_for_model)
        sim_data = np.array(sim_data)

        return sim_data
    
    else: 
        return float('NaN')


# FINAL GOAL: generate data for all other models as well
# def generate_8node_mvar_global_coup_data(coupling = None, npoints = None, time_lag = None, 
#                                          noise_corr = noise_corr):
#     sim_data = ecmc.mvar_sim_data(coupling, npoints = npoints, time_lag = time_lag, noise_corr = noise_corr)
#     return sim_data

# def generate_8node_mvar_diff_top_data(coupling_matrix = None, npoints = None, time_lag = None, 
#                                       noise_corr = noise_corr):
#     sim_data = ecmc.mvar_sim_data(coupling_matrix, npoints = npoints, time_lag = time_lag, 
#                                   noise_corr = noise_corr)
#     return sim_data

# def generate_8node_mvar_er_data(density_vec = None, npoints = None, time_lag = None, noise_corr = None):
#     sim_data = ecmc.mvar_sim_data(density_vec, npoints = npoints, time_lag = time_lag, 
#                                   noise_corr = noise_corr)
#     return sim_data

# def generate_kuramoto_network(coupling = None, npoints = None, phase_vec = None, intra_comm_size = None, 
#                               n_comm = None):
#     sim_data = ecmc.mvar_sim_data(coupling, npoints = npoints, phase = phase_vec, 
#                                   intra_comm_size = intra_comm_size, n_comm = n_comm)
#     return sim_data

# -----------------------------------------------------------------------------
# FUNCTIONS FOR MICRO & MACRO VARIABLES GENERATION
# -----------------------------------------------------------------------------

def sum_micro_mvar(data):
    macro_var = np.sum(data, axis = 0)
    return macro_var

def raw_micro_mvar(data):
    micro_var = data
    return micro_var

# FINAL GOAL: get micro and macro variables for other models as well
# def sigma_chi_kuramoto():
#     macro_var = ...
#     return macro_var

# def pair_sync_kuramoto():
#     macro_var = ...
#     return macro_var

# def raw_val_kuramoto(data):
#     micro_var = np.cos(data)
#     return micro_var

# def phase_kuramoto(data):
#     micro_var = data
#     return micro_var