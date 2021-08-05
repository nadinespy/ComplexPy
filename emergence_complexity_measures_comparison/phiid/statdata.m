function X = statdata(A,npoints)

% -----------------------------------------------------------------------
%   FUNCTION: statdata.m
%   PURPOSE:  Obtain time-series data for a Gaussian MVAR(p) process
%             X_t=A_1*X_{t-1}+A_2*X_{t-2}+...+A_p*X_{t-p}+E_t
%
%   INPUT:  A        -    generalized connectivity matrix. 
%                           A=(A_1 A_2 ... A_p)
%           Omega    -    covariance matrix for E_t
%
%   OUTPUT: X        -    time-series data, rows are variables, columns are
%                         observations
%
%   Adam Barrett May 2010.
% -----------------------------------------------------------------------

settle=500; %will only keep post-equilibrium data points
N = npoints+settle;

nvar=size(A,1);             
p=floor(size(A,2)/nvar);    
    
X = normrnd(0,1,nvar,N);
%Y = zeros(nvar,N);

for i=p+1:N
    for j=1:nvar
        for k=1:nvar
            for m=1:p
                X(j,i)= X(j,i)+A(j,k+(m-1)*nvar)*X(k,i-m);
            end
        end
    end
end
X = X(:,settle+1:end);