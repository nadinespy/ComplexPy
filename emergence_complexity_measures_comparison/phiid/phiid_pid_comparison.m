clear all;
close all;
clc;

cd '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison'
addpath '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts'
addpath '/media/nadinespy/NewVolume/my_stuff/work/toolboxes_matlab'
% addpath '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/scripts/heatmaps'

PATHOUT = '/media/nadinespy/NewVolume/my_stuff/work/PhD/my_projects/PhiIDComparison/results/';
javaaddpath('infodynamics.jar');

%% calculating information atoms

% System size, coupling matrix, and vector of noise values
nvar = 2;
npoints = 2000;
tau = 1;
error_vec   = linspace(0.01, 0.99, 100);
coupling_vec = linspace(0.01,0.49, 100);

phiid_all_err_coup_mmi = zeros(16, size(coupling_vec,2), size(error_vec, 2));
phiid_all_err_coup_ccs = zeros(16, size(coupling_vec,2), size(error_vec, 2));


for i = 1:length(coupling_vec)
	A = coupling_vec(i)*ones(nvar);
	
	for j = 1:length(error_vec)
		err = error_vec(j);
		spectral_radius = max(abs(eig(A)));
		%X = statdata_corr_errors(A, npoints, err);
		X = statdata_corr_errors2(A, npoints, err);
		% X = statdata_corr_errors3(A, npoints, err);
		phiid_all_err_coup_mmi(:,i,j) = struct2array(PhiIDFull(X, tau, 'MMI'))';
		phiid_all_err_coup_ccs(:,i,j) = struct2array(PhiIDFull(X, tau, 'ccs'))';
		
	end 
	i
	%spectral_radius
end 

% save([PATHOUT 'phiid_all_err_coup_ccs_rtr.mat'],'phiid_all_err_coup_ccs_rtr');
% save([PATHOUT 'phiid_all_err_coup_ccs_sts.mat'],'phiid_all_err_coup_ccs_sts');
% save([PATHOUT 'phiid_all_err_coup_mmi_rtr.mat'],'phiid_all_err_coup_ccs_mmi');
% save([PATHOUT 'phiid_all_err_coup_mmi_sts.mat'],'phiid_all_err_coup_ccs_mmi');

%% double-redundancy & double-synergy

% extract double-redundancy & synergy term
% rows: couplings; errors: columns
phiid_all_err_coup_ccs_rtr = squeeze(phiid_all_err_coup_ccs(1,:,:));			% coupling vector will now be in the rows, and error vector in the columns
phiid_all_err_coup_ccs_sts = squeeze(phiid_all_err_coup_ccs(16,:,:));

phiid_all_err_coup_mmi_rtr = squeeze(phiid_all_err_coup_mmi(1,:,:));
phiid_all_err_coup_mmi_sts = squeeze(phiid_all_err_coup_mmi(16,:,:));

% heatmaps
x_axis = {'0.01', '', '', '', '', '', '', '', '', '0.1', '', '', '', '', '', '', '', '', '', '0.2', '', '', '', '', '', '', '', '', '', '0.3', '', '', '', '', '', '', '', '', '', ... 
	'0.4', '', '', '', '', '', '', '', '', '', '0.5', '', '', '', '', '', '', '', '', '', '0.6', '', '', '', '', '', '', '', '', '', '0.7', '', '', '', '', '', '', '', '', '', ... 
	'0.8', '', '', '', '', '', '', '', '', '', '0.9', '', '', '', '', '', '', '', '', '0.99', ''}; 
y_axis = {'0.01', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '',  '', '0.1',  '', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', ... 
	'0.2', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '',  '', '0.3', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', '', ... 
	'0.4', '', '', '', '', '', '', '', '', '',  '', '', '', '', '', '', '', '', '', '',  '0.5'};

% using matlab built-in function for heatmaps:
figure;
clf
h = heatmap(phiid_all_err_coup_mmi_rtr, 'Colormap', parula, 'ColorbarVisible', 'on') ;
h.YDisplayLabels = y_axis;
h.XDisplayLabels = x_axis;
h.XLabel = 'noise correlation';
h.YLabel = 'coupling strength';
title('double-redundancy mmi');
exportgraphics(gcf, [PATHOUT '2node_phiid_all_err_coup_mmi_rtr2.png']);

figure;
clf
h = heatmap(phiid_all_err_coup_mmi_sts, 'Colormap', parula, 'ColorbarVisible', 'on') ;
h.YDisplayLabels = y_axis;
h.XDisplayLabels = x_axis;
h.XLabel = 'noise correlation';
h.YLabel = 'coupling strength';
title('double-synergy mmi');
exportgraphics(gcf, [PATHOUT '2node_phiid_all_err_coup_mmi_sts2.png']);

figure;
clf
h = heatmap(phiid_all_err_coup_ccs_rtr, 'Colormap', parula, 'ColorbarVisible', 'on') ;
h.YDisplayLabels = y_axis;
h.XDisplayLabels = x_axis;
h.XLabel = 'noise correlation';
h.YLabel = 'coupling strength';
title('double-redundancy ccs');
exportgraphics(gcf, [PATHOUT '2node_phiid_all_err_coup_ccs_rtr2.png']);

figure;
clf
h = heatmap(phiid_all_err_coup_ccs_sts, 'Colormap', parula, 'ColorbarVisible', 'on') ;
h.YDisplayLabels = y_axis;
h.XDisplayLabels = x_axis;
h.XLabel = 'noise correlation';
h.YLabel = 'coupling strength';
title('double-synergy ccs');
exportgraphics(gcf, [PATHOUT '2node_phiid_all_err_coup_ccs_sts2.png']);

close all;

%load('A2b.mat')
%npoints = 2000;
%X = statdata(A2b,npoints);

% heatmaps (using "customizable" heatmaps: https://uk.mathworks.com/matlabcentral/fileexchange/24253-customizable-heat-maps,
% need to extract respective files from zip)
% figure;
% clf
% h = heatmap(phiid_all_err_coup_mmi_rtr, x_axis, y_axis, [], 'TickAngle', 0);
% colormap(parula);

% phiid_atom_names = {'rtr',  'rtx', 'rty', 'rts', 'xtr', 'xtx', 'xty', 'xts', 'ytr', 'ytx', 'yty', 'yts', 'str', 'stx', 'sty', 'sts'};

