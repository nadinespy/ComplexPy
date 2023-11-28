# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

%reset

from oct2py import octave as oc
import seaborn as sns
import numpy as np
import scipy.io
import os

PATHIN = '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/'
PATHOUT = '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/results/'


os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/')
oc.javaaddpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/infodynamics.jar');
oc.addpath(oc.genpath('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/'))
oc.addpath('/media/nadinespy/NewVolume/my_stuff/work/toolboxes_matlab/')
oc.eval('pkg load statistics')                                                  # needs to be loaded, as otherwise normrnd() in statdata will not be recognized



# HIER ABSOLUTEN PFAD MACHEN <3
oc.load(['/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/A2b.mat'])

nvar = 2
npoints = 10000
tau = 1
error_vec   = np.linspace(0.01, 0.99, 100)
coupling_vec = np.linspace(0.01,0.49, 100)

phiid_all_err_coup_mmi = np.zeros((16, len(coupling_vec), len(error_vec)))
phiid_all_err_coup_ccs = np.zeros((16, len(coupling_vec), len(error_vec)))


for i in range (1, len(coupling_vec)):
	A = coupling_vec[i]*np.ones(shape=(nvar,nvar))
	
	for j in range(1, len(error_vec)):
		err = error_vec[j]
		X = oc.statdata_corr_errors(A, npoints, err)                                  # for whatever reason, the rng() in statdata_corr_error.m doesn't work when called via oct2py (for now, it's disabled)
		phiid_all_err_coup_mmi[:,i,j] = struct2array(oc.PhiIDFull(X, tau, 'MMI')).T   # PhiIDFull.m doesn't work either, as mvnpdf() is not recognized
		phiid_all_err_coup_ccs[:,i,j] = struct2array(oc.PhiIDFull(X, tau, 'ccs')).T   # struct2array is from matlab - how to deal with struct outputs in python?
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