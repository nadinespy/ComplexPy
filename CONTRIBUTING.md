# Contributing to ComplexPy

> **Note**: ComplexPy is currently a **research prototype** in active development. The processes described here represent our goals and ideals as the project matures, but are not yet fully established.
>
> **For now**: Contributions are welcome and informal! Open an issue to discuss ideas, or email nadine.spychala@gmail.com. We'll work with you to integrate your contributions.

Thank you for your interest in contributing to ComplexPy! This project aims to make emergence and complexity research more open, reproducible, and accessible. Contributions of all kinds are welcome - whether your background is software engineering, information theory, neuroscience, complex systems, or you're simply interested in formal micro-macro relationships.

---

## Table of Contents

- [Current State (2025)](#current-state-2025)
- [Vision for Contribution Process](#vision-for-contribution-process)
- [Where to Contribute](#where-to-contribute)
- [Development Setup](#development-setup)
- [Code Guidelines](#code-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Get Help](#get-help)

---

## Current State (2025)

While we work toward the structured processes outlined below, here's the current reality:

- ✅ **Do**: Open issues, submit PRs, reach out by email
- ✅ **Do**: Start discussions about ideas or design decisions
- ✅ **Do**: Ask questions - no question is too small
- ⏳ **Coming soon**: CI/CD, automated tests, code review guidelines
- ⏳ **Coming soon**: Issue templates, PR templates
- 📋 **Planned**: Contributor code of conduct, maintainer guidelines

**We're building these processes together with early contributors!** Your feedback on what works and what doesn't is invaluable.

---

## Vision for Contribution Process

As ComplexPy grows, we aim to establish the following guidelines to ensure quality, consistency, and a welcoming environment for contributors.

---

## Where to Contribute

We welcome contributions in these areas:

### High Priority

#### **Port MATLAB to Python**
**Why**: Remove proprietary dependency, increase accessibility

**Where to start**:
- `src/shannon_wpe/` functions (simpler, good first contribution)
- Example: `GaussianMI.m` → Python (see [porting guide](doc/how-to/README.md#porting-checklist))
- See [architecture.md](doc/architecture.md#future-plans) for detailed technical approach

**Skills needed**: NumPy, SciPy, information theory basics

#### **Add Tests**
**Why**: Ensure code reliability, catch regressions

**Where to start**:
- Unit tests for existing functions in `tests/test_complexpy.py`
- Test edge cases (empty arrays, NaN values, extreme parameters)
- Integration tests for full workflows

**Skills needed**: pytest, Python testing practices

#### **Improve Documentation**
**Why**: Make the library more accessible

**Where to start**:
- Expand docstrings (add examples, improve descriptions)
- Write how-to guides (see [how-to/README.md](doc/how-to/README.md))
- Add code comments for complex algorithms
- Fix typos, improve clarity

**Skills needed**: Technical writing, understanding of the library

### Medium Priority

#### **Add New Time-Series Models**
**Why**: Enable more research applications

**Ideas**:
- 8-node MVAR networks with different topologies
- Kuramoto oscillators (phase-coupled)
- Empirical data loaders (EEG, fMRI)

**See**: [Model function template](doc/how-to/README.md#model-function-template)

**Skills needed**: Dynamical systems, time-series modeling

#### **Add New Emergence Measures**
**Why**: Expand the toolkit

**Ideas**:
- Dynamical Independence
- G-emergence (Granger causality-based)
- Complexity measures (Integrated Information, Neural Complexity)

**See**: [Measure function template](doc/how-to/README.md#measure-function-template)

**Skills needed**: Information theory, complexity theory

#### **Improve Visualizations**
**Why**: Help users explore results

**Ideas**:
- Interactive plots (Plotly, Bokeh)
- 3D parameter space visualizations
- Network topology visualizations
- Animated time-series

**Skills needed**: matplotlib, seaborn, plotly

### Lower Priority (But Still Welcome!)

- Performance optimization (profiling, Cython, parallelization)
- Better error messages and input validation
- Jupyter notebook tutorials
- Example analyses reproducing published results
- Documentation translations

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/ComplexPy.git
cd ComplexPy
```

### 2. Set Up Environment

**Using Poetry (recommended)**:

```bash
# Use Python 3.10 or 3.11
poetry env use python3.10

# Install runtime + dev dependencies
poetry install --with dev

# Activate environment
poetry shell
```

**Without Poetry**:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

### 3. Install MATLAB Engine

See [README MATLAB notes](README.md#notes-on-matlab-engine) for setup instructions.

### 4. Verify Installation

```bash
# Run tests
poetry run pytest -v

# Check import works
poetry run python -c "import complexpy; print(complexpy.__version__)"
```

### 5. Create a Branch

```bash
git checkout -b feature/my-contribution
```

---

## Code Guidelines

### Style

**Python Code**:
- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable names
- Keep functions focused (single responsibility)
- Maximum line length: 100 characters (flexible for readability)

**Formatting** (coming soon):
- We plan to use `black` for auto-formatting
- And `ruff` for linting

### Docstrings

Use NumPy-style docstrings:

```python
def my_function(param1, param2):
    """
    One-line summary of what the function does.

    Longer description if needed. Explain the purpose,
    algorithm, or any important details.

    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2

    Returns
    -------
    type
        Description of return value

    Examples
    --------
    >>> my_function(1, 2)
    3
    """
    return param1 + param2
```

### Comments

- Use comments to explain *why*, not *what*
- Complex algorithms should have high-level comments explaining the approach
- Reference papers for theoretical concepts

```python
# Good
# Use MMI redundancy as conservative lower bound (Williams & Beer, 2010)
red_func = 'mmi'

# Less helpful
# Set red_func to mmi
red_func = 'mmi'
```

---

## Testing

### Writing Tests

- Tests go in `tests/test_*.py`
- Use pytest
- Test both expected behavior and edge cases
- Include docstring explaining what's being tested

```python
def test_shannon_wpe_basic():
    """Test shannon_wpe returns expected dict keys and positive values."""
    data_dict = {
        'micro': np.random.randn(2, 1000),
        'macro': np.random.randn(1, 1000)
    }

    result = cp.shannon_wpe(data_dict, time_lag_for_measure=1)

    # Check keys
    assert 'shannon_wpe' in result
    assert 'shannon_dc' in result
    assert 'shannon_cd' in result

    # Check types
    assert isinstance(result['shannon_wpe'], float)

    # Check reasonable values (not NaN, not infinite)
    assert not np.isnan(result['shannon_wpe'])
    assert not np.isinf(result['shannon_wpe'])
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_complexpy.py

# Run specific test
poetry run pytest tests/test_complexpy.py::test_shannon_wpe_basic
```

### Test Coverage (coming soon)

We plan to track code coverage to ensure tests are comprehensive.

---

## Documentation

### Code Documentation

- All public functions must have docstrings
- Docstrings should include examples
- Update relevant docs when changing functionality

### User Documentation

When adding features, update:

- **README.md**: If it changes installation or basic usage
- **doc/architecture.md**: If it changes architecture or adds modules
- **doc/theory.md**: If it adds new theoretical concepts
- **doc/getting-started.md**: If it's a feature beginners should know
- **doc/how-to/**: Consider adding a task-specific guide

### Documentation Style

- Be clear and concise
- Assume reader has basic Python knowledge but not necessarily domain expertise
- Use examples liberally
- Link between documents (e.g., "see architecture.md for details")

---

## Pull Request Process

### Before Submitting

1. **Create an issue first** (for non-trivial changes)
   - Describe what you want to change and why
   - Get feedback before investing significant time

2. **Make your changes**
   - Keep commits focused and logical
   - Write clear commit messages

3. **Test your changes**
   - Run existing tests: `poetry run pytest`
   - Add tests for new functionality
   - Manually test the feature

4. **Update documentation**
   - Add/update docstrings
   - Update relevant docs
   - Add examples if applicable

### Submitting the PR

1. **Push to your fork**

```bash
git push origin feature/my-contribution
```

2. **Create pull request on GitHub**
   - Provide clear title and description
   - Reference related issues (e.g., "Fixes #42")
   - Describe what changed and why
   - Include any relevant testing notes

3. **PR Description Template** (coming soon):
   - What: Brief description of changes
   - Why: Motivation for the changes
   - How: Technical approach
   - Testing: How you tested it
   - Docs: Documentation updated?

### After Submitting

- Be responsive to feedback
- Make requested changes in new commits (don't force-push)
- Ask questions if feedback is unclear
- Be patient - review may take time (we're a small team!)

### What to Expect

**Currently**:
- Informal review process
- Feedback via GitHub comments or email
- May take a week or more for review (this is a side project!)

**Future goal**:
- Automated CI checks (tests, linting)
- Code review from maintainers
- Faster turnaround

---

## Code of Conduct (Coming Soon)

We're working on a formal code of conduct. In the meantime:

- **Be respectful**: Treat everyone with respect and kindness
- **Be constructive**: Focus on the work, not the person
- **Be inclusive**: Welcome contributors of all backgrounds and experience levels
- **Be patient**: Remember we're all volunteers with limited time
- **Ask questions**: There are no stupid questions!

If you experience or witness unacceptable behavior, please email nadine.spychala@gmail.com.

---

## Get Help

### For Contribution Questions

- **Open an issue**: [github.com/nadinespy/ComplexPy/issues](https://github.com/nadinespy/ComplexPy/issues)
- **Email**: nadine.spychala@gmail.com
- **Discussions**: Use GitHub issues for now; Discussions may be enabled later

### For Technical Questions

- **Check docs first**: [README](README.md), [architecture.md](doc/architecture.md), [theory.md](doc/theory.md)
- **Search existing issues**: Someone may have asked before
- **Open an issue**: Tag as "question"

### For Bug Reports

Include:
- ComplexPy version (`complexpy.__version__`)
- Python version
- Operating system
- Minimal code to reproduce
- Expected vs actual behavior
- Error message (full traceback)

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS file (coming soon)
- Acknowledged in release notes
- Co-authors on published papers using ComplexPy (as appropriate)

We deeply appreciate all contributions, no matter how small!

---

## Additional Resources

- **[Getting Started Guide](doc/getting-started.md)**: Learn ComplexPy basics
- **[Architecture](doc/architecture.md)**: Understand the codebase structure
- **[Theory](doc/theory.md)**: Learn the theoretical foundations
- **[How-To Guides](doc/how-to/)**: Task-specific recipes and templates

---

## Questions?

Don't hesitate to reach out! We're excited to work with you.

- Email: nadine.spychala@gmail.com
- GitHub Issues: [github.com/nadinespy/ComplexPy/issues](https://github.com/nadinespy/ComplexPy/issues)

**Thank you for contributing to open, reproducible emergence research!** 🎉
