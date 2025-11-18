# ComplexPy Architecture & Technical Reference

This document provides a technical deep-dive into ComplexPy's implementation, architecture, and design. For a general introduction, see the [main README](../README.md). For theoretical background, see [theory.md](theory.md).

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Module Reference](#module-reference)
- [File Structure](#file-structure)
- [Design Patterns](#design-patterns)
- [Dependencies](#dependencies)
- [Future Plans](#future-plans)

---

## Architecture Overview

ComplexPy uses a **two-layer architecture** combining a **Python API** with a **MATLAB computational engine**:

```
┌─────────────────────────────────────────────────┐
│         Python API (complexpy)                  │
│  - User-facing interface                        │
│  - Parameter management                         │
│  - Data handling (numpy arrays)                 │
│  - Result aggregation (pandas DataFrames)       │
└──────────────────┬──────────────────────────────┘
                   │
                   │ MATLAB Engine API
                   │
┌──────────────────▼──────────────────────────────┐
│         MATLAB Computational Engine             │
│  - PhiID calculations                           │
│  - Shannon WPE measures                         │
│  - MVAR time-series simulations                 │
│  - JIDT (Java Information Dynamics Toolbox)     │
└─────────────────────────────────────────────────┘
```

### Why This Architecture?

- **Python layer**: Provides modern, user-friendly API with excellent data science ecosystem (numpy, pandas, matplotlib)
- **MATLAB layer**: Leverages existing, well-tested implementations of complex information-theoretic computations
- **Communication**: Python's `matlabengine` package provides the bridge between layers

### Architecture Trade-offs

**Advantages:**
- Reuses validated MATLAB implementations
- Python provides accessible user interface
- Separation of concerns (API vs computation)

**Disadvantages:**
- Requires MATLAB installation (proprietary, cost barrier)
- Cross-language overhead
- Deployment complexity

See [Future Plans](#future-plans) for roadmap to pure Python implementation.

---

## Core Components

### 1. Python API Layer: `src/complexpy/`

The user-facing Python interface, organized into three main modules:

#### `complexpy.py` - Main API

**Emergence Measure Functions:**

**`phiid_wpe(data_dict, time_lag_for_measure=1, red_func='mmi')`**
- Computes PhiID-based Whole-Parts Emergence
- **Parameters**:
  - `data_dict`: Dictionary with keys `'micro'` (numpy array, shape: n_nodes × n_timepoints) and `'macro'` (numpy array, shape: 1 × n_timepoints)
  - `time_lag_for_measure`: Time lag τ for computing information measures (integer)
  - `red_func`: Redundancy function - either `'mmi'` (Minimum Mutual Information) or `'ccs'` (Common Change in Surprisal)
- **Returns**: Dictionary with:
  - `phiid_wpe`: Whole-parts emergence (emergent capacity at macro level)
  - `phiid_dc`: Downward causation (macro → micro influence)
  - `phiid_cd`: Causal decoupling (macro independence from micro)
- **Implementation**: Calls `PhiIDFull.m` via MATLAB engine

**`shannon_wpe(data_dict, time_lag_for_measure=1)`**
- Computes Shannon-based Whole-Parts Emergence
- Practical approximation using standard information theory (no full decomposition)
- **Returns**: Dictionary with `shannon_wpe`, `shannon_dc`, `shannon_cd`
- **Implementation**: Calls `EmergencePsi.m`, `EmergenceDelta.m`, `EmergenceGamma.m` via MATLAB engine

**`phiid_2sources_2targets(data_dict, time_lag_for_measure=1, red_func='mmi')`**
- Computes full Integrated Information Decomposition
- **Returns**: Dictionary with all 16 PhiID atoms (see [theory.md](theory.md#phiid-atoms))
  - Redundant: `rtr`, `rtx`, `rty`, `rts`
  - Unique X: `xtr`, `xtx`, `xty`, `xts`
  - Unique Y: `ytr`, `ytx`, `yty`, `yts`
  - Synergistic: `str`, `stx`, `sty`, `sts`
- **Implementation**: Calls `PhiIDFull.m` and extracts all atoms

**Parameter Sweep Functions:**

**`compute_emergence(model_functions, model_variables, emergence_functions, measure_variables, parameters)`**
- High-level orchestration for systematic parameter space exploration
- **Parameters**:
  - `model_functions`: Dict mapping model names to model generator functions
  - `model_variables`: Dict mapping model names to lists of their parameter names
  - `emergence_functions`: Dict mapping measure names to measure functions
  - `measure_variables`: Dict mapping measure names to lists of their parameter names
  - `parameters`: Dict with all parameter values (both model and measure parameters)
- **Returns**: pandas DataFrame with all parameter combinations and results
- **Algorithm**:
  ```python
  for each model in model_functions:
      for each measure in emergence_functions:
          for each parameter combination in cartesian_product(parameters):
              result = get_result_for_measure(model, measure, params)
              aggregate results
  return DataFrame
  ```

**`get_result_for_measure(model_function, model_params, measure_function, measure_params)`**
- Helper function computing a single measure for single parameter set
- Separates model generation from measure computation
- Returns dictionary with combined parameters and results

#### `data_simulation.py` - Time-Series Generation

**`generate_2node_mvar_data(coupling, n_points, time_lag_for_model, noise_corr, seed)`**
- Generates 2-node multivariate autoregressive (MVAR) network
- **Model equation**: X_t = A × X_{t-τ} + E_t (see [theory.md](theory.md#mvar-models))
- **Parameters**:
  - `coupling`: Coupling strength between nodes (0-1 range)
  - `n_points`: Number of time points to generate
  - `time_lag_for_model`: Time lag τ in MVAR dynamics
  - `noise_corr`: Noise correlation between nodes (0-1 range)
  - `seed`: Random seed for reproducibility
- **Returns**: Dictionary with:
  - `micro`: 2×n_points array (individual node time-series)
  - `macro`: 1×n_points array (sum of nodes)
- **Implementation**: Calls `sim_mvar_network.m` via MATLAB engine

**Macro Aggregation Functions:**
- `sum_micro_mvar()`: Returns macro = sum(micro) [default aggregation]
- `raw_micro_mvar()`: Returns micro variables without aggregation

#### `plotting.py` - Visualization Utilities

- Heatmap generation for parameter sweep results
- Built on seaborn and matplotlib
- Customizable color schemes and annotations

### 2. MATLAB Computational Engine: `src/phiid/` & `src/shannon_wpe/`

#### PhiID Engine: `src/phiid/`

**`PhiIDFull.m`** - Core PhiID computation:
- **Algorithm**:
  1. Assumes multivariate Gaussian distribution (for analytical tractability)
  2. Computes covariance matrices for sources and targets
  3. Calculates time-delayed mutual information I(Sources_t; Targets_{t+τ})
  4. Finds Minimum Information Bipartition (MIB) over all possible bipartitions
  5. Decomposes information into 16 atoms using linear algebra on covariance matrices
- **Inputs**: Micro data, macro data, time lag, redundancy function choice
- **Outputs**: 16 PhiID atoms in source-target notation
- **Key dependency**: Uses redundancy functions (MMI or CCS) to decompose information

**`DoubleRedundancyMMI.m`** - Minimum Mutual Information redundancy:
- Formula: red(X₁,X₂;Y) = min{I(X₁;Y), I(X₂;Y)}
- Conservative lower bound on redundancy
- Ensures redundancy ≥ 0

**`DoubleRedundancyCCS.m`** - Common Change in Surprisal redundancy:
- Formula: red(X₁,X₂;Y) = I(X₁;Y) + I(X₂;Y) - I(X₁,X₂;Y)
- Based on co-information
- Can be negative (interpreted as "unique info creates redundancy")

**`sim_mvar_network.m`** - MVAR simulation:
- Implements discrete-time linear dynamics: X_t = A × X_{t-τ} + E_t
- Constructs coupling matrix A from coupling parameter
- Generates correlated Gaussian noise E_t
- Ensures system stability (eigenvalues < 1)

**Dependencies:**
- `infodynamics.jar`: JIDT (Java Information Dynamics Toolbox) for some calculations

#### Shannon WPE Engine: `src/shannon_wpe/`

**`EmergencePsi.m`** - Whole-Parts Emergence (Ψ):
- Formula: Ψ = MI(V_t, V_{t+τ}) - Σᵢ MI(Xᵢ_t, V_{t+τ})
- Positive when macro has predictive info about itself that individual micros lack

**`EmergenceDelta.m`** - Downward Causation (Δ):
- Formula: Δ = Σᵢ MI(V_t, Xᵢ_{t+τ}) - MI(V_t, X_{t+τ})
- Positive when macro better predicts micro futures than micro predicts itself

**`EmergenceGamma.m`** - Causal Decoupling (Γ):
- Formula: Γ = MI(V_t, V_{t+τ}) - MI(V_t, X_{t+τ})
- Positive when macro dynamics partially independent of micro details

**Information Estimators:**
- `GaussianMI.m`: Analytical mutual information for Gaussian variables (using covariance matrices)
- `DiscreteMI.m`: Histogram-based mutual information for discrete variables

---

## Data Flow

### Typical Usage Flow

```
User Input (parameters)
    ↓
Model Function(s) generate data
    {micro: array, macro: array}
    ↓
Measure Function(s) compute emergence
    {measure_wpe: float, measure_dc: float, measure_cd: float}
    ↓
Results aggregated to DataFrame
    [model_params × measure_params × results]
```

### Detailed Execution Flow

```python
# User code
emergence_df = cp.compute_emergence(
    model_functions={'mvar': generate_2node_mvar_data},
    model_variables={'mvar': ['coupling', 'noise_corr']},
    emergence_functions={'phiid': cp.phiid_wpe},
    measure_variables={'phiid': ['time_lag_for_measure', 'red_func']},
    parameters={
        'coupling': [0.1, 0.5, 0.9],
        'noise_corr': [0.0, 0.5],
        'n_points': [1000],
        'time_lag_for_model': [1],
        'time_lag_for_measure': [1],
        'red_func': ['mmi'],
        'seed': [42]
    }
)

# Internal execution (simplified)
results = []
for model_name, model_func in model_functions.items():
    for measure_name, measure_func in emergence_functions.items():
        # Generate all parameter combinations
        for param_combo in itertools.product(*param_values):

            # 1. PYTHON: Generate data
            model_params = extract_model_params(param_combo)
            data_dict = model_func(**model_params)
            # → Calls MATLAB: sim_mvar_network.m
            # → Returns: {micro: np.array([[...], [...]]),
            #             macro: np.array([[...]])}

            # 2. PYTHON → MATLAB: Compute measure
            measure_params = extract_measure_params(param_combo)
            result_dict = measure_func(data_dict, **measure_params)
            # → Calls MATLAB: PhiIDFull.m or EmergencePsi.m etc.
            # → Returns: {phiid_wpe: 0.123, phiid_dc: 0.045, ...}

            # 3. PYTHON: Store result
            results.append({**param_combo, **result_dict})

# 4. PYTHON: Return as DataFrame
return pd.DataFrame(results)
```

### Data Dictionary Contract

Functions communicate via standardized dictionaries:

**Data Dictionary** (from model functions):
```python
{
    'micro': np.ndarray,  # Shape: (n_nodes, n_timepoints)
    'macro': np.ndarray   # Shape: (1, n_timepoints)
}
```

**Result Dictionary** (from measure functions):
```python
# For phiid_wpe or shannon_wpe:
{
    '<measure>_wpe': float,  # Whole-parts emergence
    '<measure>_dc': float,   # Downward causation
    '<measure>_cd': float    # Causal decoupling
}

# For phiid_2sources_2targets:
{
    'rtr': float, 'rtx': float, ..., 'sts': float  # 16 atoms
}
```

---

## Module Reference

### File Organization

```
ComplexPy/
├── src/
│   ├── complexpy/                   # Python API layer
│   │   ├── __init__.py              # Package init, MATLAB engine startup
│   │   ├── complexpy.py             # Measure functions & parameter sweeps
│   │   ├── data_simulation.py       # Time-series generators
│   │   └── plotting.py              # Visualization utilities
│   ├── phiid/                       # MATLAB PhiID engine
│   │   ├── PhiIDFull.m              # Main PhiID computation
│   │   ├── DoubleRedundancyMMI.m    # MMI redundancy function
│   │   ├── DoubleRedundancyCCS.m    # CCS redundancy function
│   │   ├── sim_mvar_network.m       # MVAR simulation
│   │   └── infodynamics.jar         # JIDT library
│   └── shannon_wpe/                 # MATLAB Shannon measures
│       ├── EmergencePsi.m           # Ψ (WPE) measure
│       ├── EmergenceDelta.m         # Δ (DC) measure
│       ├── EmergenceGamma.m         # Γ (CD) measure
│       ├── GaussianMI.m             # Gaussian MI estimator
│       └── DiscreteMI.m             # Discrete MI estimator
├── tests/                           # Unit tests
│   └── test_complexpy.py            # Test suite
├── scripts/                         # Example analyses
│   └── complexpy_analysis.py        # Demo script
├── doc/                             # Documentation
│   ├── architecture.md              # This file
│   ├── theory.md                    # Theoretical background
│   ├── getting-started.md           # Practical guide
│   └── how-to/                      # Task-specific guides
├── pyproject.toml                   # Poetry dependencies
├── README.md                        # Main documentation
└── CONTRIBUTING.md                  # Contribution guidelines
```

### Key File Paths

- Main API: `/src/complexpy/complexpy.py`
- Data generation: `/src/complexpy/data_simulation.py`
- PhiID computations: `/src/phiid/PhiIDFull.m`
- Shannon measures: `/src/shannon_wpe/EmergencePsi.m`
- Example usage: `/scripts/complexpy_analysis.py`
- Tests: `/tests/test_complexpy.py`

---

## Design Patterns

### 1. Strategy Pattern
Different redundancy functions are swappable implementations:

```python
# User can choose redundancy calculation strategy
phiid_wpe(data_dict, red_func='mmi')  # Uses DoubleRedundancyMMI.m
phiid_wpe(data_dict, red_func='ccs')  # Uses DoubleRedundancyCCS.m
```

**Benefits**: Easy to add new redundancy functions without changing PhiID logic

### 2. Template Method Pattern
`compute_emergence()` defines algorithm skeleton, delegates specifics to plugged-in functions:

```python
def compute_emergence(model_functions, model_variables,
                     emergence_functions, measure_variables,
                     parameters):
    results = []
    for model in models:
        for measure in measures:
            for param_combo in param_space:
                # Template delegates to specific implementations:
                result = get_result_for_measure(
                    model_function=model,      # Pluggable
                    measure_function=measure,   # Pluggable
                    params=param_combo
                )
                results.append(result)
    return pd.DataFrame(results)
```

**Benefits**: Users can extend with custom models/measures without modifying sweep logic

### 3. Dictionary-Based Interfaces
Standardized dictionary contracts for data and results:

```python
# Standard data format
data_dict = {'micro': array, 'macro': array}

# Standard result format
result_dict = {'measure_wpe': float, 'measure_dc': float, ...}
```

**Benefits**:
- Loose coupling between components
- Easy to extend with new fields
- Language-agnostic (Python ↔ MATLAB)

### 4. Facade Pattern
Python API provides simplified interface to complex MATLAB computations:

```python
# Simple user-facing call
result = cp.phiid_wpe(data_dict)

# Hides complexity of:
# - MATLAB engine management
# - Path configuration
# - Type conversions (numpy ↔ MATLAB)
# - Error handling
```

**Benefits**: Users don't need to know about MATLAB internals

---

## Dependencies

### Core Python Dependencies

```toml
[tool.poetry.dependencies]
python = ">=3.9,<3.12"
numpy = "^1.24.0"          # Numerical arrays
pandas = "^2.0.0"          # DataFrames for results
scipy = "^1.10.0"          # Scientific computing
matplotlib = "^3.7.0"      # Plotting
seaborn = "^0.12.0"        # Statistical visualizations
matlabengine = "23.2.1"    # Python-MATLAB bridge
```

### MATLAB Dependencies

- **MATLAB** (tested with R2023b): Required for computational engine
- **MATLAB Engine for Python**: Communication layer between Python and MATLAB
- **JIDT** (Java Information Dynamics Toolbox): Embedded in `src/phiid/infodynamics.jar`

### Development Dependencies

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.0"            # Testing framework
jupyter = "^1.0"           # Interactive notebooks (optional)
```

### Dependency Management

- **Poetry** (`pyproject.toml`): Manages Python dependencies and virtual environments
- **MATLAB**: Must be installed separately, MATLAB Engine configured via MathWorks installer

---

## Future Plans

This section outlines technical plans for evolving ComplexPy's architecture. For high-level roadmap, see [README](../README.md#roadmap).

### 1. Port MATLAB to Pure Python

**Motivation**:
- Remove proprietary MATLAB dependency
- Lower barrier to entry (cost, installation complexity)
- Improve deployment (Docker, cloud, HPC)
- Enable better integration with Python ecosystem

**Technical Approach**:

**Phase 1: Shannon WPE Functions** (lower complexity, good starting point)
- Port `GaussianMI.m` → Python using NumPy covariance calculations
- Port `EmergencePsi.m`, `EmergenceDelta.m`, `EmerganceGamma.m` → Python
- These functions use straightforward mutual information calculations
- **Estimated effort**: Medium (requires careful validation)

**Phase 2: MVAR Simulation**
- Port `sim_mvar_network.m` → Python
- Use NumPy for linear algebra (matrix multiplication, random number generation)
- **Estimated effort**: Low (relatively straightforward)

**Phase 3: PhiID Computations** (highest complexity)
- Port `PhiIDFull.m` → Python
- Challenges:
  - Complex covariance matrix decompositions
  - Minimum Information Bipartition search
  - Numerical stability considerations
- **Candidate libraries**:
  - `dit` (Discrete Information Theory): Has PID implementations
  - `IDTxl` (Information Dynamics Toolkit): Python alternative to JIDT
  - `jpype`: Could wrap JIDT directly from Python (intermediate solution)
- **Estimated effort**: High (complex algorithms, extensive validation needed)

**Validation Strategy**:
- Compare Python outputs to MATLAB outputs for identical inputs
- Use existing test cases as ground truth
- Check numerical accuracy (within floating-point tolerance)
- Performance benchmarking

**Migration Path**:
- Keep MATLAB implementations as reference
- Add Python implementations alongside
- Make MATLAB optional dependency
- Eventually deprecate MATLAB (after thorough testing)

### 2. Add More Time-Series Models

**8-Node MVAR Networks**:
- Extend 2-node implementation to arbitrary network sizes
- Enable different coupling topologies (ring, fully-connected, hierarchical)
- **Implementation**: Generalize `sim_mvar_network.m` (or Python equivalent)

**Kuramoto Oscillators**:
- Phase-coupled oscillators: dθᵢ/dt = ωᵢ + (K/N)Σⱼ sin(θⱼ - θᵢ)
- Study synchronization and phase relationships
- **Implementation**: New simulation function, integrate with existing API

**Empirical Data Loaders**:
- Support loading EEG, fMRI, MEG data
- Preprocessing pipelines (filtering, downsampling)
- Interface with MNE-Python, NiBabel
- **Implementation**: New module `empirical_data.py`

### 3. Add More Emergence Measures

**Dynamical Independence** ([Rosas et al., 2020](https://arxiv.org/pdf/2106.06511.pdf)):
- Measures macro independence from micro over time
- Requires implementing time-series information measures

**G-Emergence**:
- Granger causality-based emergence
- Leverages existing econometrics libraries (statsmodels)

**Complexity Measures**:
- Integrated Information (Φ)
- Neural Complexity
- Transfer Entropy matrices

**Implementation Strategy**:
- Follow existing API pattern (function returns dictionary)
- Add to `emergence_functions` in parameter sweeps
- Include in tests and documentation

### 4. Improve Testing & CI

**Testing Expansion**:
- Unit tests for each function
- Integration tests for end-to-end workflows
- Regression tests (compare to known results)
- Property-based testing (hypothesis library)

**Continuous Integration**:
- GitHub Actions for automated testing
- Test on multiple Python versions (3.9, 3.10, 3.11)
- Code coverage reporting (codecov)
- Automated linting (ruff, black)

**Challenge**: Testing MATLAB-dependent code in CI
- **Option 1**: Mock MATLAB engine in tests
- **Option 2**: Use GitHub runners with MATLAB installed
- **Option 3**: Focus CI on pure Python components once ported

### 5. Performance Optimization

**Profiling**:
- Identify bottlenecks (Python-MATLAB communication, computation)
- Use `cProfile`, `line_profiler` for Python
- MATLAB Profiler for MATLAB code

**Optimization Strategies**:
- Vectorize operations (avoid loops)
- Cache repeated calculations
- Parallelize parameter sweeps (multiprocessing)
- Consider Cython for critical paths (post-MATLAB removal)

**Benchmarking**:
- Create benchmark suite with various data sizes
- Track performance across versions
- Compare MATLAB vs Python implementations

### 6. Enhanced Visualization

**Interactive Plots**:
- Use Plotly for interactive parameter space exploration
- Jupyter widgets for live parameter adjustment

**3D Visualizations**:
- 3D parameter spaces (coupling × noise_corr × emergence)
- Network topology visualizations

**Dashboards**:
- Streamlit or Dash for web-based exploration
- Real-time analysis of streaming data

### 7. Documentation & Packaging

**API Documentation**:
- Sphinx for auto-generated API docs
- Host on Read the Docs
- Docstring coverage enforcement

**More Examples**:
- Jupyter notebook tutorials
- Gallery of use cases
- Reproduce published results

**Packaging**:
- PyPI release for `pip install complexpy`
- Conda package for conda-forge
- Docker container with MATLAB runtime (or pure Python)

---

## Technical Notes

### MATLAB Engine Lifecycle

The MATLAB engine is started when `complexpy` is imported:

```python
# In src/complexpy/__init__.py
import matlab.engine
eng = matlab.engine.start_matlab()
```

**Implications**:
- First import is slow (engine startup)
- Engine persists for Python session lifetime
- Engine shared across all function calls (stateful)

**Considerations**:
- Avoid modifying MATLAB path or global state
- Engine crash requires Python restart
- Memory usage includes MATLAB process

### Type Conversions

Data passes between Python and MATLAB with automatic conversion:

```python
# Python → MATLAB
numpy_array = np.array([[1, 2], [3, 4]])
matlab_array = matlab.double(numpy_array.tolist())

# MATLAB → Python
matlab_result = eng.some_function(matlab_array)
numpy_result = np.array(matlab_result)
```

**Performance implications**:
- Conversions add overhead
- Large arrays expensive to convert
- Consider this in performance optimization

### Random Seeds

For reproducibility across Python and MATLAB:

```python
# Python seed
np.random.seed(seed)

# MATLAB seed (passed to MATLAB functions)
eng.rng(float(seed), nargout=0)
```

Both must be set for fully reproducible results.

---

For usage examples, see [getting-started.md](getting-started.md). For theoretical background on the measures, see [theory.md](theory.md). For contributing to the architecture, see [CONTRIBUTING.md](../CONTRIBUTING.md).
