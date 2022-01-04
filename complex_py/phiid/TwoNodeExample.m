function [ res ] = TwoNodeExample()
%%TWONODEEXAMPLE Integrated information measures in a two-node AR network
%
% This function replicates the results in Figure 1 of Mediano et al. 2019, by
% computing several integrated information measures in a two-node AR network
% with fixed coupling and varying noise correlation between the nodes.
%
% Most integration measures are computed with my (Pedro's) private fork of the
% JIDT toolbox by Lizier et al. (https://www.github.com/jlizier/jidt), and the
% user is referred to the JIDT documentation for further information about
% using these estimators. Notably, PhiG is computed with version 5 of Kitazono
% and Oizumi's Phi toolbox
% (https://figshare.com/articles/code/phi_toolbox_zip/3203326/5).
%
% Reference:
%
%   Mediano, P.A.; Seth, A.K.; Barrett, A.B. Measuring Integrated Information:
%   Comparison of Candidate Measures in Theory and Simulation. Entropy 2019,
%   21, 17.
%
% Pedro Mediano, 2018-2020

%% Add paths and set system parameters
javaaddpath('infodynamics.jar');
javaaddpath('commons-math3-3.5.jar');
addpath('/media/nadinespy/NewVolume/my_stuff/work/toolboxes_matlab/phi_toolbox');

% System size, coupling matrix, and vector of noise values
N = 2;
A = 0.4*ones(N);
c_vec   = linspace(0.01, 0.99);


%% Measures to be calculated and their plot labels
calcNames = {'IntegratedInformation', 'IntegratedInteraction', 'AverageCorrelation', ...
    'DecoderIntegration', 'CausalDensity', 'IntegratedSynergy', 'TimeDelayedMutualInfo',...
    'GeometricIntegration'};

calcLabels = {'\Phi', '\tilde\Phi', '\bar\Sigma', '\Phi^*', '\mathrm{CD}',...
    '\psi', 'I(X_{t-\tau}, X_t)', '\Phi_G'};

nb_calcs = length(calcNames);

% Name template to instantiate JIDT calculators
class_template = 'infodynamics.measures.continuous.gaussian.%sCalculatorGaussian';


%% Loop and compute all measures for all noise values
res = zeros([length(calcNames), length(c_vec)]);        % size(res) = 8*100 (measures * noise values)
for j = 1:length(c_vec)
  lS = makeLaggedCovariance(A, c_vec(j));               % create a 4*4 lagged covariance matrix for a given noise value

  for i=1:nb_calcs

    % the following uses only lS, i.e., the time lagged covariance matrix,
    % to compute the measure
    if strcmp(calcNames{i}, 'AverageCorrelation')
      dlS = diag(diag(lS));
      slS = (dlS^-0.5) * lS * (dlS^-0.5);
      res(i, j) = (sum(abs(slS(:))) - sum(diag(abs(slS))))/12.0;

    elseif strcmp(calcNames{i}, 'GeometricIntegration')
      res(i, j) = PhiGMatlab(lS, 'even_bipartitions');

    else 
      calc = javaObject(sprintf(class_template, calcNames{i}));
      calc.initialise(N);
      calc.setLaggedCovariance(lS);
      res(i, j) = calc.computeAverageLocalOfObservations();
    end

  end
end


%% Plot and return
bot = min(res(:));
top = 0.8;

figure;
for i=1:nb_calcs
  subplot(1,nb_calcs,i);
  plot(c_vec, res(i,:), [0, 1], [0, 0], 'k--')
  set(gca, 'Ylim', [bot, top]);
  title(sprintf('$%s$', calcLabels{i}), 'Interpreter', 'latex')
  xlabel('c')
end

end  % of main function


function [ lS ] = makeLaggedCovariance(A, c)
  %% Auxiliary function to compute analytically the time-lagged covariance
  % matrix of an AR process with coupling matrix A and noise correlation c
  assert(size(A,1) == size(A,2));
  N = size(A, 1);
  eps = c*ones(N);			   % 2*2 matrix (correlations of noise)
  eps(1:(N+1):end) = 1;			% changes diagonal entries to 1.0

  S = dlyap(A, eps);                   % solve discrete-time lyapunov equations: ASA' − S + eps = 0 (or S = ASAT + eps); 2*2 matrix; what is S?
  lS = [S, S*A'; A*S, S];              % 4*4 matrix
  lS = 0.5*(lS + lS');                  % same 4*4 matrix, should contain the covariances between lagged versions of the time-series (lS considers one time-lag for each variable)
								% overall, I don't know why noise is introduced in this way
								% the rows of lS should be variable 1, variable 1 time lagged, variable 2, variable 2 time lagged, same with columns
                                         
end

