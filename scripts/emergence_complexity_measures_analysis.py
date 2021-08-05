#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:55:56 2021

@author: nadinespy

This script calculates emergence capacity from time-series.

""" 


import os
from oct2py import Oct2Py
from oct2py import Struct
import seaborn as sns
import numpy as np
import scipy.io
import os.path as op
import matplotlib as plt
import glob
import scipy.io as sio
from importlib import reload # %load_ext autoreload, %autoreload 2 %reset

os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
import emergence_complexity_measures_comparison as ecmc 

analyses_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/analyses/'
plots_pathout = '//media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/results/plots/'
data_pathin = op.join(ecmc.__path__[0], 'data')

#%% if already done: load phiid of networks

def load_mat_file(phiid_path):
    try:
        phiid_network = sio.loadmat(phiid_path,squeeze_me=True,struct_as_record=False)['all_atoms_err_coup_mmi'] 
    except:
        pass
   
    try:
        phiid_network = sio.loadmat(phiid_path,squeeze_me=True,struct_as_record=False)['all_atoms_err_coup_ccs']
    except:
        pass
    
    return phiid_network
    

phiid_network_paths = sorted(glob.glob(analyses_pathout+r'*_all_atoms**1*')) 

all_networks = [0] * len(phiid_network_paths)

for i in range(len(phiid_network_paths)):
    all_networks[i] = load_mat_file(phiid_networks_paths[i])
    

#%% calculate synergistic/emergent capacity, downward causation, causal decoupling

# Syn(X_t;X_t-1) (synergistic capacity of the system) 
# Un (Vt;Xt'|Xt) (causal decoupling - the top term in the lattice) 
# Un(Vt;Xt'α|Xt) (downward causation) 

# synergy (only considering the synergy that the sources have, not the target): 
# {12} --> {1}{2} + {12} --> {1} + {12} --> {2} + {12} --> {12} 
 
# causal decoupling: {12} --> {12}

# downward causation: 
# {12} --> {1}{2} + {12} --> {1} + {12} --> {2}


for i in range(len(phiid_network_paths)): 
    #synergistic capacity
    synergy_capacity = all_networks[i].str + all_networks[i].stx + all_networks[i].sty + all_networks[i].sts
    downward_causation = all_networks[i].str + all_networks[i].stx + all_networks[i].sty
    causal_decoupling = synergy_capacity - downward_causation

    emergence_capacity = {'synergy capacity': synergy_capacity, 'downward_causation': downward_causation, 'causal_decoupling': causal_decoupling}

    np.save(analyses_pathout+r'emergence_capacity_'+phiid_network_paths[i][-33:-4]+r'.npy', emergence_capacity)






























# HIER ABSOLUTEN PFAD MACHEN <3
oc.load(['/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/A2b.mat'])

oc = Oct2Py()
y = [1, 2]
oc.push('y', y)


oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/practical_measures_causal_emergence')  
oc.EmergencePsi(rn.randn(100,2), np.random.randn(100,1))

oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/phiid')  
X = np.random.randint(10, size=(2, 2000))
blubb = oc.struct2array(PhiIDFull(X, tau, 'MMI')).T

oc.eval('pkg load statistics') 
X = oc.statdata_coup_errors1(A, npoints, tau, err) 

nvar = 2
npoints = 10000
tau = 1
error_vec   = np.linspace(0.01, 0.99, 100)
coupling_vec = np.linspace(0.01,0.49, 100)

phiid_all_err_coup_mmi = np.zeros((16, len(coupling_vec), len(error_vec)))
phiid_all_err_coup_ccs = np.zeros((16, len(coupling_vec), len(error_vec)))

# functions do not exist in Octave workspace... help :( 
for i in range (1, len(coupling_vec)):
	A = coupling_vec[i]*np.ones(shape=(nvar,nvar))
	
	for j in range(1, len(error_vec)):
		err = error_vec[j]
        
        os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python/emergence_complexity_measures_comparison/practical_measures_causal_emergence')

        oc.eval('pkg load statistics') 
		X = oc.statdata_coup_errors1(A, npoints, tau, err)                                  # for whatever reason, the rng() in statdata_corr_error.m doesn't work when called via oct2py (for now, it's disabled)
		phiid_all_err_coup_mmi[:,i,j] = oc.struct2array(ecmc.phiid_full(X, tau, 'MMI')).T   # PhiIDFull.m doesn't work either, as mvnpdf() is not recognized
		phiid_all_err_coup_ccs[:,i,j] = oc.struct2array(ecmc.phiid_full(X, tau, 'ccs')).T   # struct2array is from matlab - how to deal with struct outputs in python?
	i	

phiid_all_err_coup_mmi_rtr = np.squeeze(phiid_all_err_coup_mmi[1,:,:])
phiid_all_err_coup_mmi_sts = np.squeeze(phiid_all_err_coup_mmi[16,:,:])

os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/results/')

np.save(phiid_all_err_coup_ccs, phiid_all_err_coup_ccs)
np.save(phiid_all_err_coup_mmi, phiid_all_err_coup_mmi)


phiid_all_err_coup_ccs = scipy.io.loadmat('phiid_all_err_coup_ccs.mat',squeeze_me=True)['phiid_all_err_coup_ccs']              # loads file as a dictionary where 4th row is the actual data
phiid_all_err_coup_mmi = scipy.io.loadmat('phiid_all_err_coup_mmi.mat',squeeze_me=True)['phiid_all_err_coup_mmi']    


#phiid_all_err_coup_ccs = list(phiid_all_err_coup_ccs.values())[3]                   # put all values from dict into a list, and take 3rd entry (which has the data)
#phiid_all_err_coup_mmi = list(phiid_all_err_coup_mmi.values())[3]

phiid_all_err_coup_mmi_rtr = np.squeeze(phiid_all_err_coup_mmi[0,:,:])
phiid_all_err_coup_mmi_sts = np.squeeze(phiid_all_err_coup_mmi[15,:,:])

#heatmap
sns.set_theme()

ax = sns.heatmap(phiid_all_err_coup_mmi_rtr)
ax1 = sns.heatmap(phiid_all_err_coup_mmi_sts)






cwd = os.getcwd()