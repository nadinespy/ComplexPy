function X = statdata_coup_errors1(coupling_matrix, npoints, tau, err)

% -----------------------------------------------------------------------
%   FUNCTION: statdata_coup_errors1.m
%   PURPOSE:  Obtain time-series data for a Gaussian MVAR(p) process
%             X_t=A_1*X_{t-1}+A_2*X_{t-2}+...+A_p*X_{t-p}+E_t
%
%   INPUT:  coupling_matrix - generalized connectivity matrix, A=(A_1 A_2 ... A_p)
%		    npoints - number of time-steps
%		    tau - time-lag
%               err - covariance matrix for E_t
%
%   OUTPUT: X - time-series data, rows are variables, columns are observations
% -----------------------------------------------------------------------

settle=500; %will only keep post-equilibrium data points
npoints = npoints+settle;
nvar=size(coupling_matrix,1); 

%% simulate time-series of correlated error terms

% simulate time-series of correlated errors (by multiplying M with the upper triangular matrix L obtained from the Cholesky decomposition of the desired correlation matrix R) 
% but: I get different values for corr, which might be due to the fact that chol might fail, if the covarince matrix is singular or near singular. 
%{
mu = 0;
sigma = 1;
M = mu + sigma*randn(N,size(coupling_matrix,2));
R = [1 c; c 1];
L = chol(R);
E = (M*L)';

corr_errors = corrcoef(E(1,:),E(2,:));
%} 

% alternative: simulate errors from correlated multivariate standard normal distribution
% but: this can yield different actual correlations for them; the chosen correlation will only be yielded, if sample size is large 
mu = zeros(1, nvar);

% construct correlation matrix
R = eye(nvar);
R(R==0)=err;

% only necessary for non-standard normal distributions, otherwise R = cov_matrix
standard_dev = ones(1, nvar);							   % vector of standard deviations of the errors
cov_err = diag(standard_dev)*R*diag(standard_dev);	 % diag() converts std vector to matrix where the diagonal entries are the stds, and all other entries 0
rng(1);
E = mvnrnd(mu,cov_err,npoints)';						% simulate correlated errors

corr_errors = corrcoef(E(1,:), E(2,:));					   % check correlation

%% simulate time-series of the network

p=floor(size(coupling_matrix,2)/nvar);								  % time-steps to look into the past

X = zeros([nvar, npoints]);

% non-vectorized version
%{ 
for i=tau+1:npoints
    for j=1:nvar
        for k=1:nvar
            for m=1:tau
			X(j,i)= (A(j,k+(m-1)*nvar)*X(k,i-m)+E(j,i));
            end
        end
    end
end 
%} 

% vectorized version
for t=(1+tau):npoints
	X(:,t) = coupling_matrix*X(:,t-tau) + E(:,t);
end
	
% alternative: drawing *at each time-step* error values from a correlated 
% multi-dimensional Gaussian, and adding it to the A*X_(t-1) term
%{
rng(1);
for t=tau+1:npoints
	X(:,t) = A*X(:,t-tau) + mvnrnd(zeros([1, size(A,1)]), cov_err)';
end
%}
	
X = X(:,settle+1:end);

end
	
