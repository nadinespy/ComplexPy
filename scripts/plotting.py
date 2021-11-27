#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 14:51:16 2021

@author: nadinespy
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


#%% load files


#%% plotting

causal_emergence_phiid_labels = ["phiid_emergence_capacity", "phiid_downward_causation", "phiid_causal_decoupling"]

y_ticklabels_8node = ['optimal_A', 'optimal_B', 'small_world', 'two_communities', 'fully_connected', 'ring', 'uni_ring']


for o in causal_emergence_phiid_labels:
    temp_model_measure = pd.pivot_table(emergence_df3.loc[(emergence_df3.model == 'eight_node_mvar_model_erdoes_renyi') & (emergence_df3.measure == o)],
                                        values ='value', index = ['coupling'], columns = ['noise_corr'], sort  = False) 
    
    num_ticks = 10
            
    yticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
    xticks = np.linspace(0, len(temp_model_measure.columns) - 1, num_ticks, dtype = int)            
    xticklabels = ["{:.2f}".format(temp_model_measure.columns[idx]) for idx in xticks]
    #yticklabels = ["{:.2f}".format(temp_model_measure.index[idx]) for idx in yticks]
    
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['axes.titlesize'] = 8
    plt.rcParams['axes.labelsize'] = 8
    fig, ax = plt.subplots(1,1)
    sns.heatmap(temp_model_measure, cbar_kws={'label': o}, cmap = "coolwarm", ax=ax) # cmap = "YlGnBu"
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation = 0)
    
#%% plotting

causal_emergence_phiid_labels = ["phiid_emergence_capacity", "phiid_downward_causation", "phiid_causal_decoupling"]

y_ticklabels_8node = ['optimal_A', 'optimal_B', 'small_world', 'two_communities', 'fully_connected', 'ring', 'uni_ring']


for o in causal_emergence_phiid_labels:
    temp_model_measure = pd.pivot_table(emergence_df2.loc[(emergence_df2.model == 'eight_node_mvar_model_different_architectures') & (emergence_df2.measure == o)], values ='value', index = 'coupling', columns ='noise_corr', sort  = False) 
        
    num_ticks = 10
            
    yticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
    xticks = np.linspace(0, len(temp_model_measure.columns) - 1, num_ticks, dtype = int)            
    xticklabels = ["{:.2f}".format(temp_model_measure.columns[idx]) for idx in xticks]
    #yticklabels = ["{:.2f}".format(temp_model_measure.index[idx]) for idx in yticks]
    
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['axes.titlesize'] = 8
    plt.rcParams['axes.labelsize'] = 8
    fig, ax = plt.subplots(1,1)
    sns.heatmap(temp_model_measure, cbar_kws={'label': o}, cmap = "coolwarm", ax=ax) # cmap = "YlGnBu"
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation = 0)
    
    # something has been deleted/gone wrong here - need to fix this
    if '2node' in model:
        num_ticks = 10
        yticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
        xticks = np.linspace(0, len(causal_decoupling_phiid_ccs_2node_all_err_coup1) - 1, num_ticks, dtype = int)
        xticklabels = ["{:.2f}".format(causal_decoupling_phiid_ccs_2node_all_err_coup1.columns[idx]) for idx in xticks]
        yticklabels = ["{:.2f}".format(causal_decoupling_phiid_ccs_2node_all_err_coup1.index[idx]) for idx in yticks]
    
    elif '8node' in model:
        num_ticks = 7
        yticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
        xticks = np.linspace(0, len(temp_model_measure) - 1, num_ticks, dtype = int)
        xticklabels = ["{:.2f}".format(temp_model_measure.columns[idx]) for idx in xticks]
        yticklabels = y_ticklabels_8node
    
        #fig, ax = plt.figure(figsize=(1, 1))
    
        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
        plt.rcParams['axes.titlesize'] = 8
        plt.rcParams['axes.labelsize'] = 8

        ax = sns.heatmap(temp_model_measure, cbar_kws={'label': measure}, cmap = "coolwarm") # cmap = "YlGnBu"
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels, rotation = 0)

# cbar = ax.collections[0].colorbar
# here set the labelsize by 20
# cbar.ax.tick_params(labelsize=8)
        ax.set_title(measure + ' in ' + model)
        plt.show()
        
        fig = ax.get_figure()
        fig.savefig(plots_pathout + measure + '_' + model + '.png', dpi = 300, bbox_inches="tight")  
    
        del fig


    
#sns.heatmap(data=all_causal_emergencies_dfs, x='noise', col='coupling', y='value') 
#sns.catplot(data=all_causal_emergencies_dfs, x='model', col='measure', y='value')


#heatmap
sns.set_theme()

ax = sns.heatmap(phiid_all_err_coup_mmi_rtr)
ax1 = sns.heatmap(phiid_all_err_coup_mmi_sts)