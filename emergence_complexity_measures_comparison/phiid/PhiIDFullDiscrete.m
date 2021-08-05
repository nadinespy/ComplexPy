function [ A, L ] = PhiIDFullDiscrete(varargin)
%%PHIIDFULLDISCRETE Computes full PhiID decomposition of discrete input data.
%
%   A = PHIIDFULLDISCRETE(X, TAU), where X is a D-by-T data matrix of D
%   dimensions for T timesteps, and TAU is an integer integration timescale,
%   computes the PhiID decomposition of the time-delayed mutual information of
%   X. If TAU is not provided, it is set to 1. If D > 2, PhiID is calculated
%   across the minimum information bipartition (MIB) of the system.
%
%   A = PHIIDFULLDISCRETE(X1, X2, Y1, Y2), where all inputs are 1D vectors of
%   the same length, computes the PhiID decomposition of the mutual information
%   between them, I(X1, X2; Y1, Y2).
%
%   A = PHIIDFULLDISCRETE(..., M) uses PhiID measure M (default: 'MMI')
%
%   [A, L] = PHIIDFULLDISCRETE(...) returns the local PhiID atoms for each
%   sample in the input. NOTE: local PID is not available for all measures
%   (e.g. BMMI). For those measures, L = A.
%
% In all cases, results are returned in a struct A with all integrated
% information atoms. Atoms are named with a three-char string of the form QtP,
% where Q and P are one of r, x, y, or s (redundancy, unique X, unique Y or
% synergy, respectively). For example:
%
%            A.rtr is atom {1}{2}->{1}{2}
%            A.xty is atom {1}->{2}
%            A.stx is atom {12}->{1}
%            ...
%
% If input data is discrete-compatible (as per ISDISCRETE), it is passed
% directly to the underlying information-theoretic calculators. If it isn't
% (e.g. if it is real-valued data), it is mean-binarised first.
%
% Reference:
%   Mediano*, Rosas*, Carhart-Harris, Seth and Barrett (2019). Beyond
%   Integrated Information: A Taxonomy of Information Dynamics Phenomena.
%
% Pedro Mediano and Andrea Luppi, Jan 2021

% Find JIDT and add relevant paths
p = strrep(mfilename('fullpath'), 'PhiIDFullDiscrete', '');
if exist([p, '../elph_base'], 'dir')
  addpath([p, '../elph_base']);
end
if ~any(~cellfun('isempty', strfind(javaclasspath('-all'), 'infodynamics')))
  if exist([p, '../elph_base/infodynamics.jar'], 'file')
    javaaddpath([p, '../elph_base/infodynamics.jar']);
  elseif exist([p, 'private/infodynamics.jar'], 'file')
    javaaddpath([p, 'private/infodynamics.jar']);
  else
    error('Unable to find JIDT (infodynamics.jar).');
  end
end

if nargin == 1
  atoms = private_TDPhiID(varargin{1});
elseif nargin == 2
  atoms = private_TDPhiID(varargin{1}, varargin{2});
elseif nargin == 3
  atoms = private_TDPhiID(varargin{1}, varargin{2}, varargin{3});
elseif nargin == 4
  atoms = private_FourVectorPhiID(varargin{1}, varargin{2}, varargin{3}, varargin{4});
elseif nargin == 5
  atoms = private_FourVectorPhiID(varargin{1}, varargin{2}, varargin{3}, varargin{4}, varargin{5});
else
  error('Wrong number of arguments. See `help PhiIDFullDiscrete` for help.');
end

A = structfun(@mean, atoms, 'UniformOutput', 0);
if nargout > 1
  L = atoms;
end

end


%*********************************************************
%*********************************************************
function [ atoms ] = private_TDPhiID(X, tau, measure)

% Argument checks and parameter initialisation
if isempty(X) || ~ismatrix(X)
  error('Input must be a 2D data matrix');
end
[D, T] = size(X);
if T <= D
  error(sprintf(['Your matrix has %i dimensions and %i timesteps. ', ...
        'If this is true, you cant compute a reasonable covariance matrix. ', ...
        'If it is not true, you may have forgotten to transpose the matrix'], D, T));
end
if nargin < 2 || isempty(tau)
  tau = 1;
end
if nargin < 3 || isempty(measure)
  measure = 'MMI';
end

% Binarise the data, if not already discrete
if ~isdiscrete(X)
  X = 1*(X > mean(X, 2));
end


% Use JIDT to compute Phi and MIB
phiCalc = javaObject('infodynamics.measures.discrete.IntegratedInformationCalculatorDiscrete', 2, size(X, 1));
if tau > 1
  phiCalc.setProperty(phiCalc.PROP_TAU, num2str(tau));
end
phiCalc.setObservations(octaveToJavaIntMatrix(X'));
phi = phiCalc.computeAverageLocalOfObservations();
mib = phiCalc.getMinimumInformationPartition();

% Extract MIB partition indices
p1 = str2num(mib.get(0).toString()) + 1;
p2 = str2num(mib.get(1).toString()) + 1;

% Stack data and call full PhiID function
atoms = private_FourVectorPhiID(X(p1,1:end-tau), X(p2,1:end-tau), ...
                                X(p1,1+tau:end), X(p2,1+tau:end), measure);

end


%*********************************************************
%*********************************************************
function [ atoms ] = private_FourVectorPhiID(X1, X2, Y1, Y2, measure)

% Argument checks and parameter initialisation
checkmat = @(v) ~isempty(v) && ismatrix(v);
if ~(checkmat(X1) && checkmat(X2) && checkmat(Y1) && checkmat(Y2))
  error('All inputs must be non-empty data matrices');
end
T = size(X1, 2);
if size(X2, 2) ~= T || size(Y1, 2) ~= T || size(Y2, 2) ~= T
  error('All input matrices must have the same number of columns');
end
if nargin < 5 || isempty(measure)
  measure = 'MMI';
end

if strcmp(lower(measure), 'mmi')
  MIFun = @localmi;
  RedFun = @RedundancyMMI;
  DoubleRedFun = @(x1, x2, y1, y2) DoubleRedundancyMMIDiscrete(x1, x2, y1, y2, 'PlugIn');
elseif strcmp(lower(measure), 'bmmi')
  MIFun = @bmi;
  RedFun = @RedundancyMMI;
  DoubleRedFun = @(x1, x2, y1, y2) DoubleRedundancyMMIDiscrete(x1, x2, y1, y2, 'NSB');
elseif strcmp(lower(measure), 'rmin')
  MIFun = @localmi;
  RedFun = @RedundancyRmin;
  DoubleRedFun = @DoubleRedundancyRminDiscrete;
elseif strcmp(lower(measure), 'ccs')
  MIFun = @localmi;
  RedFun = @RedundancyCCS;
  DoubleRedFun = @DoubleRedundancyCCSDiscrete;
else
  error(['Unknown redundancy measure. Currently implemented measures are ' ...
        '''MMI'', ''bMMI'', ''CCS'', and ''Rmin''']);
end


% Compute values of intersection informations
[~, rtr] = DoubleRedFun(X1, X2, Y1, Y2);

% Binarise data (if not already discrete) and stack for easier handling
binarify = @(v) ensure_combined(isdiscrete(v)*v + (~isdiscrete(v))*(v > mean(v, 2)));
bX = [binarify(X1); binarify(X2); binarify(Y1); binarify(Y2)];

% (Note that we do not need to keep track of variable sizes here, since they
% have all been collapsed into 1D variables of different alphabet sizes.)
Ixta   = MIFun(bX, 1, 3);
Ixtb   = MIFun(bX, 1, 4);
Iyta   = MIFun(bX, 2, 3);
Iytb   = MIFun(bX, 2, 4);
Ixyta  = MIFun(bX, [1 2], 3);
Ixytb  = MIFun(bX, [1 2], 4);
Ixtab  = MIFun(bX, 1, [3 4]);
Iytab  = MIFun(bX, 2, [3 4]);
Ixytab = MIFun(bX, [1 2], [3 4]);

Rxyta  = RedFun(bX, 1, 2, 3, Ixta, Iyta, Ixyta);
Rxytb  = RedFun(bX, 1, 2, 4, Ixtb, Iytb, Ixytb);
Rxytab = RedFun(bX, 1, 2, [3 4], Ixtab, Iytab, Ixytab);
Rabtx  = RedFun(bX, 3, 4, 1, Ixta, Ixtb, Ixtab);
Rabty  = RedFun(bX, 3, 4, 2, Iyta, Iytb, Iytab);
Rabtxy = RedFun(bX, 3, 4, [1 2], Ixyta, Ixytb, Ixytab);


% Assemble and solve system of equations
reds = [rtr Rxyta Rxytb Rxytab Rabtx Rabty Rabtxy ...
        Ixta Ixtb Iyta Iytb Ixyta Ixytb Ixtab Iytab Ixytab];

M = [1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0; % rtr
     1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0; % Rxyta
     1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0; % Rxytb
     1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0; % Rxytab
     1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0; % Rabtx
     1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0; % Rabty
     1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0; % Rabtxy
     1 1 0 0 1 1 0 0 0 0 0 0 0 0 0 0; % Ixta
     1 0 1 0 1 0 1 0 0 0 0 0 0 0 0 0; % Ixtb
     1 1 0 0 0 0 0 0 1 1 0 0 0 0 0 0; % Iyta
     1 0 1 0 0 0 0 0 1 0 1 0 0 0 0 0; % Iytb
     1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0; % Ixyta
     1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0; % Ixytb
     1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0; % Ixtab
     1 1 1 1 0 0 0 0 1 1 1 1 0 0 0 0; % Iytab
     1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]; % Ixytab

partials = linsolve(M, reds');


% Sort the results and return
atoms = [];
atoms.rtr = partials(1,:);
atoms.rtx = partials(2,:);
atoms.rty = partials(3,:);
atoms.rts = partials(4,:);
atoms.xtr = partials(5,:);
atoms.xtx = partials(6,:);
atoms.xty = partials(7,:);
atoms.xts = partials(8,:);
atoms.ytr = partials(9,:);
atoms.ytx = partials(10,:);
atoms.yty = partials(11,:);
atoms.yts = partials(12,:);
atoms.str = partials(13,:);
atoms.stx = partials(14,:);
atoms.sty = partials(15,:);
atoms.sts = partials(16,:);

end


%*********************************************************
% Utility functions to compute basic information-theoretic measures
%*********************************************************
function [ res ] = bmi(bX, src, tgt)
  res = QuasiBayesMI(bX(src,:), bX(tgt,:));
end

function [ res ] = mi(bX, src, tgt)
  x = ensure_combined(bX(src,:));
  y = ensure_combined(bX(tgt,:));

  miCalc = javaObject('infodynamics.measures.discrete.MutualInformationCalculatorDiscrete', max(x)+1, max(y)+1, 0);
  miCalc.initialise();
  miCalc.addObservations(x', y');
  res = miCalc.computeAverageLocalOfObservations();
end

function [ l ] = localmi(bX, src, tgt)

  x = ensure_combined(bX(src,:));
  y = ensure_combined(bX(tgt,:));

  miCalc = javaObject('infodynamics.measures.discrete.MutualInformationCalculatorDiscrete', max(x)+1, max(y)+1, 0);
  miCalc.initialise();
  miCalc.addObservations(x', y');
  l = miCalc.computeLocalFromPreviousObservations(x', y');

end


%*********************************************************
% A few PID (single-target) redundancy functions
%*********************************************************
function [ R ] = RedundancyMMI(bX, src1, src2, tgt, mi1, mi2, mi12)
  if mean(mi1) < mean(mi2)
    R = mi1;
  else
    R = mi2;
  end
end


function [ R ] = RedundancyCCS(bX, src1, src2, tgt, mi1, mi2, mi12)

c = mi12 - mi1 - mi2;
signs = [sign(mi1), sign(mi2), sign(mi12), sign(-c)];
R = all(signs == signs(:,1), 2).*(-c);

end


function [ R ] = RedundancyRmin(bX, src1, src2, tgt, mi1, mi2, mi12)
  T = size(bX, 2);
  rplus = inf([T, 1]);
  rminus = inf([T, 1]);

  % If any of the variables is multivariate, combine into a single integer value
  src = {ensure_combined(bX(src1,:)), ensure_combined(bX(src2,:))};
  tgt = ensure_combined(bX(tgt,:));

  for i=1:length(src)

    % Compute specificity (r^+) as the minimum over source local entropies
    hCalc = javaObject('infodynamics.measures.discrete.EntropyCalculatorDiscrete', max(src{i})+1);
    hCalc.initialise();
    rplus = min(rplus, hCalc.computeLocal(src{i}'));

    % Compute ambiguity (r^-) as the minimum over source and target conditional entropies
    joint = ensure_combined([src{i}; tgt]);

    hCalc  = javaObject('infodynamics.measures.discrete.EntropyCalculatorDiscrete', max(tgt)+1);
    jhCalc = javaObject('infodynamics.measures.discrete.EntropyCalculatorDiscrete', max(joint)+1);

    hc = jhCalc.computeLocal(joint') - hCalc.computeLocal(tgt');
    rminus = min(rminus, hc);

  end

  % Take redundancy as their difference
  R = rplus - rminus;
end


%*********************************************************
%*********************************************************
function [ V ] = ensure_combined(U)
  if size(U, 1) == 1
    V = U;
  else
    [~,~,V] = unique(U', 'rows');
    V = V(:)' - 1;
  end
end

