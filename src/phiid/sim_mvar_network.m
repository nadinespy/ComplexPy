function [X corr_X] = sim_mvar_network(time_length, noise_corr, coupling_matrix, time_lag)
% sim_mvar_network() simulates a time-series of a multivariate autoregressive 
% network using different methods (which can be chosen by bracketing or 
% unbracketing the respective code blocks)
% 
% - if SIM METHOD = X, Z, Y or W: 
%   X_t = A * X_{t-time_lag} + E_t
%
% - if SIM MEHTOD = Y or V: Gaussian MVAR(p) process:
%   X_t = A_1*X_{t-1}+A_2*X_{t-2}+...+A_p*X_{t-p}+E_t
%
% Takes as inputs scalar values ([time_length], [noise_corr], [time_lag]), 
% connectivity matrix ([coupling_matrix]).
% 
% Example: [X corr_X] = sim_mvar_network(time_length, noise_corr, 
%	     coupling_matrix, time_lag)
% 
% INPUTS - required
%    coupling_matrix        -			generalized connectivity matrix, 
%							A = (A_1 A_2 ... A_p)
%    time_length		    -			lenght of time-series
%    time_lag		    -			time-lag
%    noise_corr		    -			covariance matrix for E_t
%
% OUTPUT: 
%    X, Z, Y, W, Y, or V    -			time-series data, rows are variables, 
%							columns are observations
%    corr_X			    -			correlation between nodes
%
% For my own simulations, I've chosen X as a simulation method.
% -----------------------------------------------------------------------

settle = 500;				% keep only post-equilibrium data points
time_length = time_length+settle;
nvar = size(coupling_matrix,1); 

%% simulate time-series of correlated error terms

% -------------------------------------------------------------------------
% using Cholesky decomposition
% -------------------------------------------------------------------------
%{
% multiplying M with the upper triangular matrix L obtained from the Cholesky 
% decomposition of the desired correlation matrix R) but: I get different 
% values for corr, which might be due to the fact that chol might fail, 
% if the covarince matrix is singular or near singular. 

mu = 0;
sigma = 1;
M = mu + sigma*randn(N,size(coupling_matrix,2));
R = [1 c; c 1];
L = chol(R);
E = (M*L)';

corr_errors = corrcoef(E(1,:),E(2,:));
%} 

% -------------------------------------------------------------------------
% using correlated multivariate standard normal distribution but
% -------------------------------------------------------------------------

% {
% this can yield different actual correlations for them; the chosen 
% correlation  will only be yielded, if sample size is large 
mu = zeros(1, nvar);

% construct correlation matrix
R = eye(nvar);
R(R==0) = noise_corr;

% only necessary for non-standard normal distributions, otherwise R = cov_matrix
standard_dev = ones(1, nvar);					% vector of standard deviations of the errors
cov_err = diag(standard_dev)*R*diag(standard_dev);	% diag() converts std vector to matrix where the  
									% diagonal entries are the stds, and all other entries 0
rng(1);
E = mvnrnd(mu,cov_err,time_length)';				% simulate correlated errors
empirical_corr_err = corrcoef(E(1,:), E(2,:));		% check correlation

%}

%% simulate time-series of the network

% -------------------------------------------------------------------------
% SIM METHOD X: *only* the datapoint at t-time_lag influences the current datapoint
% -------------------------------------------------------------------------

% {
X = zeros([nvar, time_length]);

% incorporate correlation between nodes
%{
corr_matrix = eye(nvar);
corr_matrix(corr_matrix==0) = 0.75;

rng(1);
X = mvnrnd(mu,corr_matrix,time_length)';			% simulate time-series with zero mean and given covariance
corr_X = corrcoef(X(1,:), X(2,:));	
%}

for t = (1+time_lag):time_length
	X(:,t) = coupling_matrix*X(:,t-time_lag) + E(:,t);	
end
corr_X = corrcoef(X(1,:), X(2,:));
%}

% -------------------------------------------------------------------------
% SIM METHOD Z: alternative - drawing *at each time-step* error values from multi-dim Gaussian
% -------------------------------------------------------------------------

%{
Z = zeros([nvar, time_length]);
rng(1);
for t = time_lag+1:time_length
	Z(:,t) = coupling_matrix*Z(:,t-time_lag) + mvnrnd(zeros([1, size(coupling_matrix,1)]), cov_err)';
end
corr_Z = corrcoef(Z(1,:), Z(2,:));
%}

% -------------------------------------------------------------------------
% SIM METHOD W: alternative - using lagged covariance matrix
% -------------------------------------------------------------------------

% here, *only* the datapoint at t-time_lag influences the current datapoint
%{
lagged_cov = makeLaggedCovariance(coupling_matrix, noise_corr);			% get time-lagged covariance for a network		
covariance = lagged_cov(1:(length(lagged_cov)/2), 1:(length(lagged_cov)/2));	% get same-time covariance of network 
													% (by taking the first quadrant of S)
rng(1);
W = mvnrnd(zeros([nvar,1])', covariance, time_length)';					% draw samples from a multi-dimensional 
													% correlated Gaussian using a covariance 
													% which already incorporates the connection 
													% strengths & error correlation

% W_t will already entail the error and the covariance of the variables 
% in W - only the effect of the past term coupling_matrix*W_(t-time_lag) remains to be added.

for t = 1+time_lag:time_length
	W(:,t) = coupling_matrix*W(:,t-time_lag) + W(:,t);
end
corr_W = corrcoef(W(1,:), W(2,:));
%}

% -------------------------------------------------------------------------
% SIM METHOD Y: *any* datapoint up to t-time_lag influences the current datapoint
% -------------------------------------------------------------------------

%{
Y = zeros([nvar, time_length]);
for t = (1+time_lag):time_length
	next_value = 0;
	for k = 1:time_lag
		temp_value = coupling_matrix*Y(:,t-k);
		next_value = next_value + temp_value;
	end
	Y(:,t) = next_value + E(:,t);
end
corr_Y = corrcoef(Y(1,:), Y(2,:));
%}

% -------------------------------------------------------------------------
% SIM METHOD V: alternative (same as above, just differently written)
% -------------------------------------------------------------------------

%{
% create coupling matrix where connectivities for all time-lags are included
big_coupling_matrix = [];
for t = 1:time_lag;
	big_coupling_matrix = [big_coupling_matrix, coupling_matrix];
	t = 1+1;
end 

V = E;
for i = time_lag+1:time_length;
    for j = 1:nvar
        for k = 1:nvar
            for m = 1:time_lag
			V(j,i) = V(j,i) + (big_coupling_matrix(j,k+(m-1)*nvar)*V(k,i-m));
		end
        end
    end
end 
corr_V = corrcoef(V(1,:), V(2,:));
%}

X = X(:,settle+1:end);
% Y = Y(:,settle+1:end);
% Z = Z(:,settle+1:end);
% V = V(:,settle+1:end);
% W = W(:,settle+1:end);

end


