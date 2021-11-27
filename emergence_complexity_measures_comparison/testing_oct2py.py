#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 10:24:28 2021

@author: nadinespy
"""
import numpy as np
import os
from oct2py import Oct2Py
oc = Oct2Py()

os.chdir('/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Python')
import emergence_complexity_measures_comparison as ecmc

redundancy_function = 'mmi'
tau = 1
data = np.random.randn(2,1000)

phiid = ecmc.phiid_full(data, tau, redundancy_function)


current_path = os.getcwd()
oc.chdir(current_path+'/emergence_complexity_measures_comparison/phiid')
oc.addpath(current_path+'/emergence_complexity_measures_comparison/practical_measures_causal_emergence')  
oc.javaaddpath(current_path+'/emergence_complexity_measures_comparison/phiid/infodynamics.jar')
oc.eval('pkg load statistics') 
    
phiid = oc.PhiIDFull(data, tau, redundancy_function)

