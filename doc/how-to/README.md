# How-To Guides

This directory will contain **task-specific guides** for extending and using ComplexPy. These guides assume you're already familiar with ComplexPy basics (see [getting-started.md](../getting-started.md)).

**Current Status**: Placeholder with templates and planned content

---

## Planned Guides

### For Users

#### **Analyzing Your Own Data**
*Loading and preprocessing empirical time-series*

**Topics to cover**:
- Loading data from files (CSV, MAT, NumPy)
- Preprocessing: filtering, downsampling, normalization
- Defining micro and macro variables from your data
- Handling missing data or irregular sampling
- Example: EEG data analysis

#### **Advanced Parameter Sweeps**
*Strategies for exploring large parameter spaces*

**Topics to cover**:
- Choosing parameter ranges effectively
- Parallelizing computations for speed
- Handling large result DataFrames
- Visualizing high-dimensional parameter spaces
- Memory management for big sweeps

#### **Interpreting Negative or Zero Emergence**
*Understanding edge cases in results*

**Topics to cover**:
- When negative values are meaningful vs estimation error
- Zero emergence: truly absent or insufficient data?
- Comparing Shannon vs PhiID interpretations
- Statistical significance testing (bootstrap approaches)
- Troubleshooting unexpected results

---

### For Contributors

#### **Adding a Custom Time-Series Model**
*Implementing new data generators*

**Topics to cover**:
- Function signature requirements
- Return dictionary format (`{'micro': array, 'macro': array}`)
- Integration with `compute_emergence()`
- Example: Adding Kuramoto oscillators
- Testing your model

**Template**: See below ([Model Function Template](#model-function-template))

#### **Adding a Custom Emergence Measure**
*Implementing new measures*

**Topics to cover**:
- Function signature requirements
- Taking `data_dict` as input
- Return dictionary format
- MATLAB integration (if needed)
- Adding to parameter sweeps
- Documentation and tests

**Template**: See below ([Measure Function Template](#measure-function-template))

#### **Porting MATLAB Code to Python**
*Removing MATLAB dependency*

**Topics to cover**:
- Which functions to start with (Shannon WPE = easiest)
- NumPy equivalents for MATLAB operations
- Validation against MATLAB outputs
- Performance benchmarking
- When to use scipy vs custom implementations

**Template**: See below ([Porting Checklist](#porting-checklist))

#### **Creating Visualizations**
*Adding new plotting functions*

**Topics to cover**:
- Using seaborn/matplotlib effectively
- Heatmaps for 2D parameter spaces
- 3D plots for higher dimensions
- Interactive plots with Plotly
- Publication-quality figures
- Adding to `plotting.py`

---

## Templates

### Model Function Template

Use this template when creating a new time-series model:

```python
def generate_my_model_data(param1, param2, npoints,
                          macro_func, micro_func, seed=None):
    """
    Generate time-series data from [MODEL NAME].

    Parameters
    ----------
    param1 : float
        Description of param1
    param2 : float
        Description of param2
    npoints : int
        Number of time points to generate
    macro_func : callable
        Function to compute macro variable from micro
    micro_func : callable
        Function to process/return micro variables
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    dict
        Dictionary with keys:
        - 'micro': numpy array, shape (n_nodes, npoints)
        - 'macro': numpy array, shape (1, npoints)

    Examples
    --------
    >>> data = generate_my_model_data(param1=0.5, param2=1.0,
    ...                               npoints=1000,
    ...                               macro_func=sum_micro,
    ...                               micro_func=raw_micro)
    >>> data['micro'].shape
    (n_nodes, 1000)
    """
    if seed is not None:
        np.random.seed(seed)

    # 1. Generate micro-level time-series
    #    [Your simulation code here]
    micro_data = ...  # Shape: (n_nodes, npoints)

    # 2. Apply micro function (usually just returns micro_data)
    micro = micro_func(micro_data)

    # 3. Apply macro function (aggregates micro to macro)
    macro = macro_func(micro_data)

    # 4. Return standardized dictionary
    return {
        'micro': micro,  # Must be 2D array: (n_nodes, npoints)
        'macro': macro   # Must be 2D array: (1, npoints)
    }
```

**Usage in `compute_emergence()`:**

```python
model_functions = {'my_model': generate_my_model_data}
model_variables = {'my_model': ['param1', 'param2', 'npoints',
                                'macro_func', 'micro_func']}
parameters = {
    'param1': [0.1, 0.5, 1.0],
    'param2': [0.5, 1.0],
    'npoints': [2000],
    'macro_func': [sum_micro],
    'micro_func': [raw_micro]
}
```

---

### Measure Function Template

Use this template when creating a new emergence measure:

```python
def my_emergence_measure(data_dict, time_lag=1, param1=None):
    """
    Compute [MEASURE NAME] emergence measure.

    Parameters
    ----------
    data_dict : dict
        Dictionary with keys:
        - 'micro': numpy array, shape (n_nodes, npoints)
        - 'macro': numpy array, shape (1, npoints)
    time_lag : int, optional
        Time lag for computing information measures (default: 1)
    param1 : type, optional
        Additional parameter description

    Returns
    -------
    dict
        Dictionary with emergence measure results.
        Keys should be descriptive measure names.

    Examples
    --------
    >>> result = my_emergence_measure(data_dict, time_lag=1)
    >>> print(result['my_wpe'])
    0.123
    """
    # 1. Extract micro and macro data
    micro = data_dict['micro']  # Shape: (n_nodes, npoints)
    macro = data_dict['macro']  # Shape: (1, npoints)

    # 2. Compute your measure
    #    [Your computation code here]
    #    This might involve:
    #    - Information-theoretic calculations
    #    - Calling MATLAB functions (if needed)
    #    - Statistical computations

    my_wpe_value = ...
    my_dc_value = ...
    my_cd_value = ...

    # 3. Return standardized dictionary
    return {
        'my_wpe': my_wpe_value,  # Main emergence measure
        'my_dc': my_dc_value,    # Downward causation
        'my_cd': my_cd_value     # Causal decoupling
    }
```

**Usage in `compute_emergence()`:**

```python
emergence_functions = {'my_measure': my_emergence_measure}
measure_variables = {'my_measure': ['micro', 'macro', 'time_lag', 'param1']}
parameters = {
    'time_lag': [1, 5, 10],
    'param1': [None],  # or specific values
    # ... other parameters
}
```

**Integration with MATLAB** (if needed):

```python
def my_measure_with_matlab(data_dict, time_lag=1):
    """Measure that calls MATLAB code."""
    import matlab.engine

    # Get MATLAB engine (already started in __init__.py)
    from complexpy import eng

    # Convert numpy to MATLAB format
    micro_matlab = matlab.double(data_dict['micro'].tolist())
    macro_matlab = matlab.double(data_dict['macro'].tolist())

    # Call MATLAB function
    result = eng.my_matlab_function(
        micro_matlab,
        macro_matlab,
        float(time_lag),
        nargout=1
    )

    # Convert back to Python
    result_array = np.array(result)

    return {'my_measure': float(result_array[0])}
```

---

### Porting Checklist

Use this checklist when porting MATLAB code to Python:

#### Phase 1: Preparation

- [ ] Identify MATLAB function to port (start with simpler ones)
- [ ] Review MATLAB code and understand algorithm
- [ ] Identify dependencies (other MATLAB functions, JIDT, etc.)
- [ ] Create test cases with known inputs/outputs from MATLAB
- [ ] Document expected numerical accuracy

#### Phase 2: Implementation

- [ ] Create Python function with equivalent signature
- [ ] Port MATLAB operations to NumPy/SciPy:
  - [ ] Matrix operations → `np.matmul()`, `@` operator
  - [ ] Element-wise operations → NumPy broadcasting
  - [ ] Random numbers → `np.random`
  - [ ] Statistical functions → `scipy.stats`
  - [ ] Linear algebra → `scipy.linalg`
- [ ] Handle edge cases (empty arrays, NaN values)
- [ ] Add type hints and docstrings

#### Phase 3: Validation

- [ ] Run Python function on test inputs
- [ ] Compare outputs to MATLAB (should match within tolerance)
- [ ] Check numerical precision (typically < 1e-10 difference)
- [ ] Test on various data sizes
- [ ] Test edge cases (zeros, very small/large values)
- [ ] Benchmark performance (Python vs MATLAB)

#### Phase 4: Integration

- [ ] Add unit tests (`tests/test_*.py`)
- [ ] Update function calls to use Python version
- [ ] Make MATLAB version optional (backwards compatibility)
- [ ] Update documentation
- [ ] Add example usage in docstring
- [ ] Update getting-started guide if relevant

#### Phase 5: Cleanup

- [ ] Remove redundant MATLAB files (after thorough testing)
- [ ] Update dependencies in `pyproject.toml` (remove matlabengine if fully ported)
- [ ] Update README installation instructions
- [ ] Announce in CHANGELOG

**Example Equivalences**:

| MATLAB | Python/NumPy |
|--------|--------------|
| `A * B` | `A @ B` or `np.matmul(A, B)` |
| `A .* B` | `A * B` (broadcasting) |
| `A'` | `A.T` |
| `size(A)` | `A.shape` |
| `length(A)` | `len(A)` or `A.size` |
| `zeros(n, m)` | `np.zeros((n, m))` |
| `randn(n, m)` | `np.random.randn(n, m)` |
| `cov(A)` | `np.cov(A)` |
| `inv(A)` | `np.linalg.inv(A)` or `scipy.linalg.inv(A)` |
| `det(A)` | `np.linalg.det(A)` |
| `eig(A)` | `np.linalg.eig(A)` |
| `log(A)` | `np.log(A)` (natural log) |

---

## How-To Structure

Each how-to guide should follow this structure:

### 1. Goal Statement
**One sentence**: "This guide shows you how to [accomplish specific task]."

### 2. Prerequisites
- Skills: What should reader know?
- Setup: What needs to be installed/configured?

### 3. Steps
Clear, numbered steps to accomplish the task:
1. Do X
2. Do Y
3. Do Z

**Each step should**:
- Start with an action verb
- Include code examples
- Show expected output
- Explain *what* but not *why* (that's for theory.md)

### 4. Complete Example
Full working code from start to finish

### 5. Common Issues
- **Issue**: Description
- **Solution**: How to fix

### 6. See Also
Links to related docs

---

## Contributing a How-To

We welcome how-to contributions! To add a guide:

1. **Choose a task** from the planned list or propose a new one
2. **Use the templates** above as starting points
3. **Follow the structure** outlined
4. **Test your code** - all examples must work
5. **Submit a PR** (see [CONTRIBUTING.md](../../CONTRIBUTING.md))

**Questions?** Open an issue or email nadine.spychala@gmail.com

---

## Priority Guides

If you'd like to contribute, these are most needed:

1. **Adding a Custom Time-Series Model** (helps contributors extend library)
2. **Analyzing Your Own Data** (helps users with empirical data)
3. **Porting MATLAB to Python** (critical for removing dependency)

---

For the getting-started guide, see [getting-started.md](../getting-started.md). For theoretical background, see [theory.md](../theory.md). For technical details, see [architecture.md](../architecture.md).
