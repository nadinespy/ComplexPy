%% TO DO
% - where/how to store model information and parameter values for noise correlation & coupling matrix in the saved mat-file?
% - fill struct file in a loop?

% add macro-variables
% add integrated information measures?

%% 
% This script implements synergy capacity for 2-node and 8-node MVAR models with differing connection strengths and noise correlations

clear all;
clear java;
close all;
clc;

cd '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Matlab/scripts'
addpath '/media/nadinespy/NewVolume/my_stuff/work/toolboxes_matlab'
addpath '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Matlab/scripts/ReconcilingEmergences-master'
javaaddpath('infodynamics.jar');

PATHOUT1 = '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Matlab/results/';
PATHOUT2 = '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/EmergenceComplexityMeasuresComparison/EmergenceComplexityMeasuresComparison_Matlab/results/plots/';


%% choice of parameters

% time-lag and number of data points in time-series (same for all simulations)
npoints = 2000;
tau = 1;

% ------------------------------------------------------------------------------------------------------
% MODEL
% ------------------------------------------------------------------------------------------------------

% MULTIVARIATE AUTOREGRESSIVE TIME-SERIES (MVAR)

% simulation method (options: statdata_coup_errors1(), statdata_coup_errors2(), statdata_random())
sim_method = @statdata_coup_errors1;

% save plots & matrices according to simulation method (options: '1' (for statdata_coup_errors1()), '2' (for statdata_coup_errors2()), '3' (for statdata_random())
sim_index = '1';

% network (options: '2node' for 2-node network with 100 different coupling strengths & noise correlations (if choosing sim_index = 1 or 2) OR random 2-node network with 100 zero couplings & 100 zero noise correlations (if choosing sim_index = 3);
% '8node' for 8-node networks with 6 different architectures & noise correlations (if choosing sim_index = 1 or 2) OR random 8-node networks with 100 zero couplings & 100 zero correlations (if choosing sim_index = 3))
network = '8node';

% KURAMOTO OSCILLATORS


% ------------------------------------------------------------------------------------------------------
% MEASURE
% ------------------------------------------------------------------------------------------------------


% ------------------------------------------------------------------------------------------------------
% MACRO VARIABLE
% ------------------------------------------------------------------------------------------------------



%% load files (if already existent, to, e. g., only create plots)

%{
load([PATHOUT1 network '_emergence_ccs' sim_index '.mat'], 'emergence_ccs');
load([PATHOUT1 network '_emergence_mmi' sim_index '.mat'], 'emergence_mmi');
load([PATHOUT1 network '_all_atoms_err_coup_ccs' sim_index '.mat'],'all_atoms_err_coup_ccs');
load([PATHOUT1 network '_all_atoms_err_coup_mmi' sim_index '.mat'],'all_atoms_err_coup_mmi');

synergistic_capacity_mmi = emergence_mmi.synergy_capacity_mmi; 
downward_causation_mmi = emergence_mmi.downward_causation_mmi; 
causal_decoupling_mmi = emergence_mmi.causal_decoupling_mmi; 

%}

%% create coupling matrices & noise correlations depending on the chosen network size

% {
if network == '2node'
	
	if sim_index == '3' 
		coupling_vec = linspace(0.0, 0.0, 100);
		error_vec = linspace(0.0, 0.0, 100); 
	else coupling_vec = linspace(0.01,0.45, 100);
		error_vec = linspace(0.01, 0.9, 100); 
	end 

	coupling_matrices = []; 
	for i = 1:length(coupling_vec)
		coupling_matrices(:,:,i) = coupling_vec(i)*ones(2);
	end 
	
elseif network == '8node' 
	if sim_index == '3'

		coupling_vec = linspace(0.0, 0.0, 100);
		error_vec = linspace(0.0, 0.0, 100);
		
		coupling_matrices = []; 
		for i = 1:length(coupling_vec)
			coupling_matrices(:,:,i) = coupling_vec(i)*ones(8);
		end 
	
	else load('all_nets.mat');									% phi-optimal binary network, phi-optimal weighted network, small world, fully connected, bidirectional ring, unidirectional ring
		
		net_names = fields(all_nets);
		nb_nets = length(net_names);

		error_vec = linspace(0.01, 0.9, 6);
		
		coupling_matrices = [];
		for i = 1:size(net_names,1);
			coupling_matrices(:,:,i) = all_nets.(net_names{i});
		end 
		
	end

end 


%% calculating information atoms

% {
% instantiate variables to store atoms for different coupling matrices and noise correlations
phiid_all_err_coup_mmi = zeros(16, size(coupling_matrices,3), size(error_vec, 2));
phiid_all_err_coup_ccs = zeros(16, size(coupling_matrices,3), size(error_vec, 2));

% instantiate variables to store practical measures for synergistic capacity for different coupling matrices and noise correlations
synergy_capacity_practical = zeros(size(coupling_matrices,3), size(error_vec, 2));
shannon_dc = zeros(size(coupling_matrices,3), size(error_vec, 2));
shannon_cd = zeros(size(coupling_matrices,3), size(error_vec, 2));

% instantiate average covariance matrix
all_average_cov_X = zeros(size(coupling_matrices,3), size(error_vec, 2));

rng(1);
for i = 1:size(coupling_matrices,3)
	
	coupling_matrix = coupling_matrices(:,:,i);
	spectral_radius = max(abs(eig(coupling_matrix)));
	
	for j = 1:length(error_vec)
		
		err = error_vec(j);
		X = sim_method(coupling_matrix, npoints, tau, err);
		
		% PhiID (synergistic capacity is calculated below)
		phiid_all_err_coup_mmi(:,i,j) = struct2array(PhiIDFull(X, tau, 'MMI'))';
		phiid_all_err_coup_ccs(:,i,j) = struct2array(PhiIDFull(X, tau, 'ccs'))';
		phiid_all_err_coup_mmi(:,i,j) = struct2array(PhiIDFull(X, tau, 'MMI'))';
		phiid_all_err_coup_ccs(:,i,j) = struct2array(PhiIDFull(X, tau, 'ccs'))';
		
		% practical measures for causal emergence
		
		% some super simple meaningless macro variable - adding up the micro
		macro_variable = zeros(1, npoints);
		for k = 1:(size(X,1))
			macro_variable = macro_variable + X(k,:);
		end 
		
		synergy_capacity_practical(i,j) = EmergencePsi(X', macro_variable');
		shannon_dc(i,j) = EmergenceDelta(X', macro_variable');
		shannon_cd(i,j) = synergy_capacity_practical(i,j) - shannon_dc(i,j);
		
		% 
		cov_X = cov(X');
		all_average_cov_X(i,j) = mean(nonzeros(tril(cov_X,-1)), 'all');
		
	end 
	i
	%spectral_radius
end 

% allocating variable names for the atoms in a struct;
% extract single atoms such that rows are the couplings, and columns the errors

% rtr:  {1}{2}-->{1}{2}
% rtx: {1}{2}-->{1}
% rty: {1}{2}-->{2}
% rts: {1}{2}-->{12}
% xtr: {1}-->{1}{2}
% xtx: {1}-->{1}
% xty: {1}-->{2} 
% xts: {1}-->{12}
% ytr: {2}-->{1}{2}
% ytx: {2}-->{1}
% yty: {2}-->{2}
% yts: {2}-->{12} 
% str: {12}-->{1}{2}
% stx: {12}-->{1} 
% sty: {12}-->{2} 
% sts: {12}-->{12}

all_atoms_err_coup_mmi = [];
all_atoms_err_coup_mmi.rtr = squeeze(phiid_all_err_coup_mmi(1,:,:));
all_atoms_err_coup_mmi.rtx = squeeze(phiid_all_err_coup_mmi(2,:,:));
all_atoms_err_coup_mmi.rty = squeeze(phiid_all_err_coup_mmi(3,:,:));
all_atoms_err_coup_mmi.rts = squeeze(phiid_all_err_coup_mmi(4,:,:));
all_atoms_err_coup_mmi.xtr = squeeze(phiid_all_err_coup_mmi(5,:,:));
all_atoms_err_coup_mmi.xtx = squeeze(phiid_all_err_coup_mmi(6,:,:));
all_atoms_err_coup_mmi.xty = squeeze(phiid_all_err_coup_mmi(7,:,:));
all_atoms_err_coup_mmi.xts = squeeze(phiid_all_err_coup_mmi(8,:,:));
all_atoms_err_coup_mmi.ytr = squeeze(phiid_all_err_coup_mmi(9,:,:));
all_atoms_err_coup_mmi.ytx = squeeze(phiid_all_err_coup_mmi(10,:,:));
all_atoms_err_coup_mmi.yty = squeeze(phiid_all_err_coup_mmi(11,:,:));
all_atoms_err_coup_mmi.yts = squeeze(phiid_all_err_coup_mmi(12,:,:));
all_atoms_err_coup_mmi.str = squeeze(phiid_all_err_coup_mmi(13,:,:));
all_atoms_err_coup_mmi.stx = squeeze(phiid_all_err_coup_mmi(14,:,:));
all_atoms_err_coup_mmi.sty = squeeze(phiid_all_err_coup_mmi(15,:,:));
all_atoms_err_coup_mmi.sts = squeeze(phiid_all_err_coup_mmi(16,:,:));

all_atoms_err_coup_ccs = [];
all_atoms_err_coup_ccs.rtr = squeeze(phiid_all_err_coup_ccs(1,:,:));
all_atoms_err_coup_ccs.rtx = squeeze(phiid_all_err_coup_ccs(2,:,:));
all_atoms_err_coup_ccs.rty = squeeze(phiid_all_err_coup_ccs(3,:,:));
all_atoms_err_coup_ccs.rts = squeeze(phiid_all_err_coup_ccs(4,:,:));
all_atoms_err_coup_ccs.xtr = squeeze(phiid_all_err_coup_ccs(5,:,:));
all_atoms_err_coup_ccs.xtx = squeeze(phiid_all_err_coup_ccs(6,:,:));
all_atoms_err_coup_ccs.xty = squeeze(phiid_all_err_coup_ccs(7,:,:));
all_atoms_err_coup_ccs.xts = squeeze(phiid_all_err_coup_ccs(8,:,:));
all_atoms_err_coup_ccs.ytr = squeeze(phiid_all_err_coup_ccs(9,:,:));
all_atoms_err_coup_ccs.ytx = squeeze(phiid_all_err_coup_ccs(10,:,:));
all_atoms_err_coup_ccs.yty = squeeze(phiid_all_err_coup_ccs(11,:,:));
all_atoms_err_coup_ccs.yts = squeeze(phiid_all_err_coup_ccs(12,:,:));
all_atoms_err_coup_ccs.str = squeeze(phiid_all_err_coup_ccs(13,:,:));
all_atoms_err_coup_ccs.stx = squeeze(phiid_all_err_coup_ccs(14,:,:));
all_atoms_err_coup_ccs.sty = squeeze(phiid_all_err_coup_ccs(15,:,:));
all_atoms_err_coup_ccs.sts = squeeze(phiid_all_err_coup_ccs(16,:,:));

save([PATHOUT1 network '_all_atoms_err_coup_ccs' sim_index '.mat'],'all_atoms_err_coup_ccs');
save([PATHOUT1 network '_all_atoms_err_coup_mmi' sim_index '.mat'],'all_atoms_err_coup_mmi');
%}

% allocating variable names for the atoms in a struct;
emergence_practical = [];
emergence_practical = [];

emergence_practical.synergy_capacity_practical = synergy_capacity_practical;
emergence_practical.shannon_cd = shannon_cd;
emergence_practical.shannon_dc = shannon_dc;

save([PATHOUT1 network '_emergence_practical' sim_index '.mat'], 'emergence_practical');
%}

%% synergistic/emergent capacity, downward causation, causal decoupling

% {
% calculate:
% Syn(X_t;X_t-1) (synergistic capacity of the system) 
% Un (Vt;Xt'|Xt) (causal decoupling - the top term in the lattice) 
% Un(Vt;Xt'α|Xt) (downward causation) 

% synergy (only considering the synergy that the sources have, not the target): 
% {12} --> {1}{2} +
% {12} --> {1} + 
% {12} --> {2} +
% {12} --> {12} 
 
% causal decoupling: {12} --> {12}

% downward causation: 
% {12} --> {1}{2} + 
% {12} --> {1} + 
% {12} --> {2}

% synergistic capacity
synergy_capacity_ccs = all_atoms_err_coup_ccs.str + ...
	all_atoms_err_coup_ccs.stx + all_atoms_err_coup_ccs.sty + all_atoms_err_coup_ccs.sts;

downward_causation_ccs = all_atoms_err_coup_ccs.str + all_atoms_err_coup_ccs.stx + all_atoms_err_coup_ccs.sty;

synergy_capacity_mmi = all_atoms_err_coup_mmi.str + ...
	all_atoms_err_coup_mmi.stx + all_atoms_err_coup_mmi.sty + all_atoms_err_coup_mmi.sts;

downward_causation_mmi = all_atoms_err_coup_mmi.str + all_atoms_err_coup_mmi.stx + all_atoms_err_coup_mmi.sty;

causal_decoupling_ccs = synergy_capacity_ccs - downward_causation_ccs;
causal_decoupling_mmi = synergy_capacity_mmi - downward_causation_mmi;

% save variables in a struct
emergence_ccs = [];
emergence_mmi = [];

emergence_ccs.synergy_capacity_ccs = synergy_capacity_ccs;
emergence_ccs.causal_decoupling_ccs = causal_decoupling_ccs;
emergence_ccs.downward_causation_ccs = downward_causation_ccs;

emergence_mmi.synergy_capacity_mmi = synergy_capacity_mmi;
emergence_mmi.causal_decoupling_mmi = causal_decoupling_mmi;
emergence_mmi.downward_causation_mmi = downward_causation_mmi;

save([PATHOUT1 network '_emergence_ccs' sim_index '.mat'], 'emergence_ccs');
save([PATHOUT1 network '_emergence_mmi' sim_index '.mat'], 'emergence_mmi');
%}

%% plotting 

% axes ticks
if sim_index == '3'
	x_axis = {'' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' ''  ... 
		'' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' };
	y_axis = {'' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' ''  ... 
		'' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' '' };
elseif network == '2node'
	x_axis = {'0.09', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0.3', '', '', '', '', '', '', ... 
		'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0.6', '', '', '', '', '', '', '', '', '', '', '', '', '', ... 
		'', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '0.9', ''};
	y_axis = {'0.0045', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '0.09',  '', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', ... 
		'0.18', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '',  '', '0.27', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', '', ... 
		'0.36', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', '0.45', ''};
	
elseif network == '8node' 
	x_axis = {'0.15', '0.3', '0.45', '0.6', '0.75', '0.9'};
	y_axis = {'optimal A', 'optimal B', 'small world', 'fully connected', 'ring', 'uni ring'};

end 

% double-redundancy & double-synergy

% {
% heatmaps using matlab built-in function

atoms = {all_atoms_err_coup_ccs.rtr, all_atoms_err_coup_mmi.rtr, all_atoms_err_coup_ccs.sts, all_atoms_err_coup_mmi.sts};
file_names = {'_all_err_coup_ccs_rtr', '_all_err_coup_mmi_rtr', '_all_err_coup_ccs_sts', '_all_err_coup_mmi_sts'};
titles = {'double-redundancy ccs', 'double-redundancy mmi', 'double-synergy ccs', 'double-synergy mmi'};

for i = 1:size(atoms,2)
	
	figure;
	clf
	h = heatmap(atoms{i}, 'Colormap', parula, 'ColorbarVisible', 'on', 'CellLabelColor', 'none') ;
	h.YDisplayLabels = y_axis;
	h.XDisplayLabels = x_axis;
	%caxis([0, 0.1]);
	
	if sim_index == '3'
		h.YLabel = 'zero coupling';
		h.XLabel = 'zero noise correlation';
	
	else 
		h.XLabel = 'noise correlation';
		if network == '2node' 
			h.YLabel = 'coupling strength';
		else 
			h.YLabel = 'network architecture';
		end
	end 
	
	title(titles{i});
	exportgraphics(gcf, [PATHOUT2 network file_names{i} sim_index '.png']);

end
%}

% synergistic capacity, downward causation, causal decoupling

% {
% heatmaps using matlab built-in function:

atoms = {synergy_capacity_ccs, synergy_capacity_mmi, synergy_capacity_practical, downward_causation_ccs, downward_causation_mmi, shannon_dc, causal_decoupling_ccs, causal_decoupling_mmi, shannon_cd, all_average_cov_X};
file_names = {'_all_err_coup_ccs_synergy_capacity', '_all_err_coup_mmi_synergy_capacity',  '_all_err_coup_practical_synergy_capacity', '_all_err_coup_ccs_downward_causation', '_all_err_coup_mmi_downward_causation', '_all_err_coup_practical_downward_causation', '_all_err_coup_ccs_causal_decoupling', '_all_err_coup_mmi_causal_decoupling', '_all_err_coup_practical_causal_decoupling', '_all_err_coup_average_cov_X'};
titles = {'synergy capacity ccs', 'synergy capacity mmi', 'synergy capacity practical', 'downward causation ccs', 'downward causation mmi', 'downward causation practical', 'causal decoupling ccs', 'causal decoupling mmi', 'causal decoupling practical', 'average covariance X'};

for i = 1:size(atoms,2)
	
	figure;
	clf
	h = heatmap(atoms{i}, 'Colormap', parula, 'ColorbarVisible', 'on', 'CellLabelColor', 'none') ;
	h.YDisplayLabels = y_axis;
	h.XDisplayLabels = x_axis;
	%caxis([0, 0.1]);
	
	if sim_index == '3'
		h.YLabel = 'zero coupling';
		h.XLabel = 'zero noise correlation';
	
	else 
		h.XLabel = 'noise correlation';
		if network == '2node' 
			h.YLabel = 'coupling strength';
		else 
			h.YLabel = 'network architecture';
		end
	end 
	
	title(titles{i});
	exportgraphics(gcf, [PATHOUT2 network file_names{i} sim_index '.png']);

end
%}

close all;
