# ComplexPy Installation Guide

Complete installation instructions for ComplexPy, including detailed troubleshooting for all scenarios.

**Quick start?** See the [README quick installation](../README.md#installation).

## Table of Contents
- [System Requirements](#system-requirements)
- [Understanding the Dependencies](#understanding-the-dependencies)
- [Version Compatibility](#version-compatibility)
- [Installation Steps](#installation-steps)
  - [Step 1: Install MATLAB](#step-1-install-matlab)
  - [Step 2: Configure MATLAB Engine](#step-2-configure-matlab-engine)
  - [Step 3: Set Up Python Environment](#step-3-set-up-python-environment)
  - [Step 4: Install ComplexPy](#step-4-install-complexpy)
  - [Step 5: Verify Installation](#step-5-verify-installation)
- [Common Installation Issues](#common-installation-issues)
- [Platform-Specific Notes](#platform-specific-notes)
- [Advanced Topics](#advanced-topics)

---

## System Requirements

### Essential Requirements
- **Python**: 3.9, 3.10, or 3.11 (3.10 or 3.11 recommended)
- **MATLAB**: R2023b or later (any recent version)
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 4GB RAM minimum (8GB+ recommended for larger analyses)
- **Disk Space**: ~5GB (for MATLAB + Python environment + ComplexPy)

### Recommended Tools
- **Poetry**: For dependency management (strongly recommended)
- **pyenv**: For Python version management (optional but helpful)

### Not Included (Yet)
ComplexPy currently requires MATLAB. A pure Python implementation is planned (see [Roadmap](../README.md#roadmap)) but not yet available.

---

## Understanding the Dependencies

### Why MATLAB is Required

ComplexPy uses a **two-layer architecture**:
- **Python API**: User-friendly interface you interact with
- **MATLAB computational engine**: Performs complex information-theoretic calculations

The MATLAB Engine for Python acts as a bridge between these layers. This means:
- You need a MATLAB installation (licensed)
- Python calls MATLAB functions in the background
- The `matlabengine` Python package must match your MATLAB version

**Future**: We're working to remove this dependency by porting MATLAB code to pure Python (see [architecture.md - Future Plans](architecture.md#future-plans)). Contributions welcome!

### What is LD_LIBRARY_PATH?

`LD_LIBRARY_PATH` is a Linux/macOS environment variable that tells the system where to find shared libraries (`.so` files on Linux, `.dylib` on macOS).

**Why it matters for ComplexPy:**
- MATLAB Engine needs to load MATLAB's compiled libraries
- These libraries are in `/usr/local/MATLAB/R20XXy/bin/glnxa64/` (or similar)
- Without `LD_LIBRARY_PATH`, the system can't find them → installation fails

**What we'll do:**
Add MATLAB's library directory to `LD_LIBRARY_PATH` in your shell configuration file (`~/.bashrc` or `~/.zshrc`), so it's set automatically in every terminal session.

---

## Version Compatibility

### MATLAB ↔ matlabengine Version Table

**Critical**: The `matlabengine` Python package version must match your MATLAB installation version.

| Your MATLAB Version | pyproject.toml Should Have | Poetry Will Install | Notes |
|---------------------|----------------------------|---------------------|-------|
| R2023b | `matlabengine = "~23.2.0"` | 23.2.x | ✓ Default in repo |
| R2024a | `matlabengine = "~24.1.0"` | 24.1.x | Edit before install |
| R2025a | `matlabengine = "~25.1.0"` | 25.1.x | Edit before install |
| R2025b | `matlabengine = "~25.2.0"` | 25.2.x | Edit before install |

**Pattern**: R20XXy → matlabengine ~XX.Y.0 (where a=1, b=2)

### Check Your MATLAB Version

```bash
# Method 1: Check version
matlab -batch "version"

# Method 2: Check installation directory
matlab -batch "disp(matlabroot)"
# Output example: /usr/local/MATLAB/R2025a
```

### Understanding the `~` Version Constraint

We use `~25.1.0` which means "approximately 25.1.0" - allows 25.1.x but not 25.2.x or higher.

This ensures you stay within your MATLAB release series (e.g., R2025**a** uses 25.**1**.x, R2025**b** uses 25.**2**.x).

---

## Installation Steps

### Step 1: Install MATLAB

#### Verify MATLAB Installation

Check if MATLAB is installed and accessible:

```bash
# Check if matlab command is available
which matlab
# Expected: /usr/local/bin/matlab (or similar)

# Check MATLAB root directory
matlab -batch "disp(matlabroot)"
# Expected: /usr/local/MATLAB/R2025a (or your version)

# Check MATLAB version
matlab -batch "version"
# Expected: 24.2.0.2712019 (R2025a) Update 1 (or similar)
```

#### If MATLAB is Not Installed

1. Download MATLAB from [MathWorks](https://www.mathworks.com/downloads/)
2. Requires a MathWorks account and license
3. Install to default location (recommended):
   - **Linux**: `/usr/local/MATLAB/R20XXy/`
   - **macOS**: `/Applications/MATLAB_R20XXy.app/`
   - **Windows**: `C:\Program Files\MATLAB\R20XXy\`

#### Supported MATLAB Versions

- **Minimum**: R2023b
- **Recommended**: R2024a or later
- **Maximum**: Any recent version (as long as corresponding `matlabengine` exists on PyPI)

---

### Step 2: Configure MATLAB Engine

This step sets up the environment so Python can find MATLAB's libraries.

#### Linux Configuration

**1. Find your MATLAB library path:**

```bash
matlab -batch "disp(matlabroot)"
# Output: /usr/local/MATLAB/R2025a

# Library path is: <matlabroot>/bin/glnxa64
# Example: /usr/local/MATLAB/R2025a/bin/glnxa64
```

**2. Add to `~/.bashrc` (or `~/.zshrc` if using zsh):**

```bash
# Open .bashrc in editor
nano ~/.bashrc
# or
vim ~/.bashrc

# Add this line at the end (replace R2025a with your version):
export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH
```

**3. Reload your shell configuration:**

```bash
source ~/.bashrc
# or
source ~/.zshrc
```

**4. Verify it's set:**

```bash
echo $LD_LIBRARY_PATH
# Should include: /usr/local/MATLAB/R2025a/bin/glnxa64
```

#### macOS Configuration

Similar to Linux, but the path is different:

```bash
# Library path format: <matlabroot>/bin/maci64 (Intel) or maca64 (Apple Silicon)

# For Intel Macs:
export DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025a.app/bin/maci64:$DYLD_LIBRARY_PATH

# For Apple Silicon Macs:
export DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025a.app/bin/maca64:$DYLD_LIBRARY_PATH
```

Add to `~/.zshrc` (macOS default shell is zsh).

#### Windows Configuration

Windows uses `PATH` instead of `LD_LIBRARY_PATH`:

```powershell
# Add to System Environment Variables:
# MATLAB bin directory: C:\Program Files\MATLAB\R2025a\bin\win64

# Or set temporarily in PowerShell:
$env:PATH = "C:\Program Files\MATLAB\R2025a\bin\win64;" + $env:PATH
```

See [Platform-Specific Notes](#platform-specific-notes) for more details.

---

### Step 3: Set Up Python Environment

#### Option A: Using pyenv (Recommended)

**Install pyenv** (if not already installed):

```bash
# Linux:
curl https://pyenv.run | bash

# macOS:
brew install pyenv
```

**Install and configure Python 3.11:**

```bash
# Install Python 3.11.12
pyenv install 3.11.12

# From the repository root, set Python version for this project
pyenv local 3.11.12

# Verify
python --version
# Output: Python 3.11.12
```

**Configure Poetry to use this Python:**

```bash
poetry env use python
# Output: Using virtualenv: /home/user/.cache/pypoetry/virtualenvs/complexpy-XXXXX-py3.11
```

#### Option B: Using System Python

If you already have Python 3.10 or 3.11 installed:

```bash
# From the repository root, tell Poetry which Python to use
poetry env use python3.11
# or
poetry env use python3.10
```

#### Verify Python Setup

```bash
poetry run python --version
# Should show: Python 3.10.x or 3.11.x
```

---

### Step 4: Install ComplexPy

#### Check/Update matlabengine Version

**Before installing**, ensure `pyproject.toml` has the correct `matlabengine` version for your MATLAB:

```bash
# Check your MATLAB version
matlab -batch "disp(matlabroot)"
# Example output: /usr/local/MATLAB/R2025a

# Open pyproject.toml
nano pyproject.toml
# or
vim pyproject.toml

# Find the matlabengine line:
[tool.poetry.dependencies]
python = ">=3.9,<3.12"
matlabengine = "~23.2.0"  # ← UPDATE THIS if needed

# For R2025a, change to:
matlabengine = "~25.1.0"

# Save and exit
```

**Quick reference:**
- R2023b → `"~23.2.0"`
- R2024a → `"~24.1.0"`
- R2024b → `"~24.2.0"`
- R2025a → `"~25.1.0"`
- R2025b → `"~25.2.0"`

#### Install Dependencies

```bash
# Basic installation (runtime dependencies only)
poetry install

# OR: Include development tools (Jupyter, etc.)
poetry install --with dev
```

**What to expect:**
- First time: Downloads and installs ~100 packages (5-10 minutes)
- `matlabengine` installation may take 1-2 minutes (compiles C extensions)
- Total download size: ~500MB

**During matlabengine installation:**
- You'll see: `Installing matlabengine (25.1.2)`
- It searches for MATLAB libraries using `LD_LIBRARY_PATH`
- If successful: proceeds to next package
- If failed: see [Common Installation Issues](#common-installation-issues)

---

### Step 5: Verify Installation

#### Test 1: Basic Import

```bash
poetry run python -c "import complexpy; print('✓ ComplexPy imported successfully')"
```

**Expected:**
- Takes 10-30 seconds (MATLAB Engine starting)
- Prints: `✓ ComplexPy imported successfully`

**If it hangs:**
- First import starts MATLAB Engine (slow)
- Wait up to 60 seconds
- If still hanging, see troubleshooting below

#### Test 2: Check Functions Available

```bash
poetry run python -c "import complexpy as cp; print('shannon_wpe:', hasattr(cp, 'shannon_wpe')); print('phiid_wpe:', hasattr(cp, 'phiid_wpe'))"
```

**Expected output:**
```
shannon_wpe: True
phiid_wpe: True
```

#### Test 3: Run Unit Tests

```bash
poetry run pytest -v
```

**Expected:**
- Several tests run and pass
- May take 1-2 minutes
- Some tests start MATLAB Engine (slow)

#### Test 4: Run Example Script

```bash
poetry run python scripts/complexpy_analysis.py
```

**Expected:**
- Generates emergence analysis
- Outputs results to console
- May take several minutes

#### Verification Checklist

- [ ] Python 3.10 or 3.11 installed
- [ ] MATLAB installed and accessible
- [ ] `LD_LIBRARY_PATH` set in `~/.bashrc`
- [ ] `matlabengine` version matches MATLAB version
- [ ] `poetry install` completed successfully
- [ ] ComplexPy imports without errors
- [ ] Functions available (`shannon_wpe`, `phiid_wpe`)
- [ ] Tests pass

**All checked?** You're ready to use ComplexPy! See [getting-started.md](getting-started.md) for your first analysis.

---

## Common Installation Issues

### Error: "MATLAB R20XXy installation not found"

**Full error message:**
```
RuntimeError: MATLAB R2025b installation not found. Install to default location,
or add <matlabroot>/bin/glnxa64 to LD_LIBRARY_PATH, where <matlabroot> is the
root of a MATLAB R2025b installation.
```

**Cause 1: LD_LIBRARY_PATH not set**

**Solution:**
```bash
# Check if LD_LIBRARY_PATH includes MATLAB
echo $LD_LIBRARY_PATH | grep MATLAB

# If nothing shows, add to ~/.bashrc:
echo 'export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Try again
poetry install
```

**Cause 2: matlabengine version mismatch**

The error says "R2025**b**" but you have R2025**a**:

```bash
# Check your MATLAB
matlab -batch "disp(matlabroot)"
# Output: /usr/local/MATLAB/R2025a  ← You have R2025a

# But pyproject.toml has wrong version
# Edit pyproject.toml:
matlabengine = "~25.1.0"  # For R2025a (was ~25.2.0 for R2025b)

# Update lock file and reinstall
poetry update matlabengine
```

**Cause 3: Terminal not reloaded**

After editing `~/.bashrc`, you must reload:

```bash
source ~/.bashrc
# or close and reopen terminal
```

### Error: "matlabengine build failed"

**Error snippet:**
```
PEP517 build of a dependency failed
Backend subprocess exited when trying to invoke build_wheel
```

**Cause:** Usually means LD_LIBRARY_PATH is not set during build.

**Solution:**
```bash
# Set LD_LIBRARY_PATH and install in same command
export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH && poetry install

# Then make it permanent in ~/.bashrc (see Step 2)
```

### Warning: "ipykernel 6.27.0 is yanked"

**Full warning:**
```
Warning: The locked version 6.27.0 for ipykernel is yanked.
Reason for being yanked: broke %edit magic
```

**What this means:**
- Affects Jupyter's `%edit` magic command (if you use Jupyter notebooks)
- ComplexPy core functionality is **not affected**
- Safe to ignore if you don't use Jupyter or don't use the `%edit` command

**To fix (if needed):**
```bash
poetry update ipykernel
```

### Error: "ImportError: libMatlabEngine.so: cannot open shared object file"

**Full error:**
```python
ImportError: libMatlabEngine.so: cannot open shared object file: No such file or directory
```

**Cause:** `LD_LIBRARY_PATH` not set at runtime (when importing).

**Solution:**
```bash
# Make sure it's in ~/.bashrc (not just exported temporarily)
echo 'export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH' >> ~/.bashrc

# Reload
source ~/.bashrc

# Verify
echo $LD_LIBRARY_PATH

# Try import again
poetry run python -c "import complexpy"
```

### Error: "MATLAB Engine for Python not found"

**Cause:** `matlabengine` package not installed.

**Solution:**
```bash
# Check if installed
poetry show matlabengine

# If not found, install explicitly
poetry add matlabengine@~25.1.0  # adjust version

# Or reinstall everything
poetry install
```

### Installation Hangs During "Installing matlabengine"

**Symptoms:**
- `poetry install` gets stuck at "Installing matlabengine"
- No error message, just hangs

**Cause:** Build process waiting for MATLAB libraries that can't be found.

**Solution:**
```bash
# Cancel with Ctrl+C
# Set LD_LIBRARY_PATH explicitly
export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH

# Try with verbose output
poetry install -vvv

# Look for error messages in verbose output
```

### Import Takes Very Long (30+ seconds)

**Symptoms:**
- `import complexpy` takes 30-60 seconds
- Eventually succeeds

**Cause:** MATLAB Engine starting (this is normal for first import).

**Expected behavior:**
- First import in a session: 10-30 seconds (MATLAB Engine starts)
- Subsequent imports in same session: instant (engine already running)

**Not a problem if:**
- Eventually succeeds
- Subsequent imports are fast

### Python Version Error

**Error:**
```
The current project's Python requirement (>=3.9,<3.12) is not compatible with your Python version (3.13.0)
```

**Solution:**
ComplexPy requires Python 3.9-3.11 (not 3.12+). Use pyenv to install a compatible version:

```bash
pyenv install 3.11.12
pyenv local 3.11.12
poetry env use python
poetry install
```

---

## Platform-Specific Notes

### Linux

**Standard installation paths:**
- MATLAB: `/usr/local/MATLAB/R20XXy/`
- Libraries: `/usr/local/MATLAB/R20XXy/bin/glnxa64/`

**Shell config file:** `~/.bashrc` (bash) or `~/.zshrc` (zsh)

**Environment variable:** `LD_LIBRARY_PATH`

**Verify MATLAB libraries:**
```bash
ls /usr/local/MATLAB/R2025a/bin/glnxa64/*.so | head -5
# Should show: libMatlabEngine.so, libmx.so, etc.
```

### macOS

**Standard installation paths:**
- MATLAB: `/Applications/MATLAB_R20XXy.app/`
- Libraries (Intel): `/Applications/MATLAB_R20XXy.app/bin/maci64/`
- Libraries (Apple Silicon): `/Applications/MATLAB_R20XXy.app/bin/maca64/`

**Shell config file:** `~/.zshrc` (zsh is default on modern macOS)

**Environment variable:** `DYLD_LIBRARY_PATH`

**Check your architecture:**
```bash
uname -m
# x86_64 → Intel (use maci64)
# arm64 → Apple Silicon (use maca64)
```

**Example for Apple Silicon:**
```bash
export DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025a.app/bin/maca64:$DYLD_LIBRARY_PATH
```

### Windows

**Standard installation paths:**
- MATLAB: `C:\Program Files\MATLAB\R20XXy\`
- Libraries: `C:\Program Files\MATLAB\R20XXy\bin\win64\`

**Environment variable:** `PATH` (not `LD_LIBRARY_PATH`)

**Setting PATH (PowerShell):**
```powershell
# Temporary (current session):
$env:PATH = "C:\Program Files\MATLAB\R2025a\bin\win64;" + $env:PATH

# Permanent (System Environment Variables):
# 1. Open "Environment Variables" in System Properties
# 2. Edit "Path" under "System variables"
# 3. Add: C:\Program Files\MATLAB\R2025a\bin\win64
```

**Poetry on Windows:**
```powershell
# Install Poetry
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Use Poetry
poetry install
```

**Note:** Windows support is less tested. Linux or macOS recommended for development.

---

## Advanced Topics

### Multiple MATLAB Versions

If you have multiple MATLAB versions installed, you can switch between them:

**Method 1: Change symlink**
```bash
# Create symlink to current MATLAB
sudo ln -sf /usr/local/MATLAB/R2025a /usr/local/MATLAB/current

# Update LD_LIBRARY_PATH to use symlink
export LD_LIBRARY_PATH=/usr/local/MATLAB/current/bin/glnxa64:$LD_LIBRARY_PATH
```

**Method 2: Project-specific environment variables**

Use `direnv` to automatically set variables when entering the project directory:

```bash
# Install direnv first (if not installed):
# Linux: sudo apt install direnv
# macOS: brew install direnv

# Add to ~/.bashrc:
eval "$(direnv hook bash)"

# From the repository root, create .envrc:
cat > .envrc << 'EOF'
export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH
export MATLAB_VERSION=R2025a
EOF

# Allow direnv to load the file:
direnv allow
```

Variables are now set automatically when you `cd` into the directory.

**Method 3: Separate copies for different MATLAB versions**
- Clone the ComplexPy repository multiple times (e.g., `ComplexPy-R2024a`, `ComplexPy-R2025a`)
- Each copy has its `pyproject.toml` configured for the appropriate `matlabengine` version

### Installing Without Poetry

**Using pip directly:**

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Set LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH

# Install
pip install --upgrade pip
pip install .
```

**Note:** Poetry is recommended for reproducible installs.

### Offline Installation

If you need to install on a machine without internet:

1. **On a machine with internet, export dependencies:**
   ```bash
   # From the repository root:
   poetry export -f requirements.txt --output requirements.txt --without-hashes
   pip download -r requirements.txt -d packages/
   ```

2. **Transfer both `requirements.txt` and `packages/` directory to offline machine**

3. **On offline machine:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install --no-index --find-links=packages/ -r requirements.txt
   pip install --no-index --find-links=packages/ .
   ```

**Note**: MATLAB must still be installed and accessible on the offline machine.

### Docker Installation

A Dockerfile is planned but not yet available. Challenges:
- **MATLAB licensing**: Licenses are typically node-locked, complicates container deployment
- **MATLAB Runtime vs full MATLAB**:
  - MATLAB Runtime: Free, smaller (~2GB), runs compiled MATLAB code only
  - Full MATLAB: Licensed, large (~10GB), can run and edit MATLAB code
  - ComplexPy currently requires full MATLAB (uses MATLAB Engine, not compiled code)
- **Image size**: Would result in very large Docker images

**Interested in Docker support?** Open an issue on GitHub to discuss requirements and approaches.

### Development Installation

For contributors:

```bash
# Clone the repository
git clone https://github.com/nadinespy/ComplexPy.git

# Navigate to the cloned repository
cd ComplexPy  # Or whatever you named the directory

# Install with dev dependencies
poetry install --with dev

# Install pre-commit hooks (when available)
# pre-commit install

# Run tests
poetry run pytest

# Activate shell
poetry shell
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for full contributor guide.

---

## Getting Help

### Still Having Issues?

1. **Check this guide** - Search for your error message
2. **Check existing issues** - [GitHub Issues](https://github.com/nadinespy/ComplexPy/issues)
3. **Open a new issue** - Include:
   - Your OS and Python version
   - Your MATLAB version
   - Full error message
   - Output of `echo $LD_LIBRARY_PATH`
   - Steps you've tried
4. **Email** - nadine.spychala@gmail.com

### Useful Debugging Commands

```bash
# Check Python version
poetry run python --version

# Check MATLAB version
matlab -batch "version"

# Check LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH

# Check installed packages
poetry show

# Check matlabengine specifically
poetry show matlabengine

# Verbose install output
poetry install -vvv

# Test MATLAB Engine directly
poetry run python -c "import matlab.engine; eng = matlab.engine.start_matlab(); print('MATLAB Engine works!')"
```

---

## Next Steps

Installation complete? Great! Here's what to do next:

1. **[Getting Started Guide](getting-started.md)** - Your first emergence analysis (recommended)
2. **[Theory](theory.md)** - Understand the measures you're computing
3. **[Architecture](architecture.md)** - How ComplexPy works under the hood
4. **[Contributing](../CONTRIBUTING.md)** - Help improve ComplexPy

**Questions?** Open an issue or email nadine.spychala@gmail.com

Happy analyzing! 🚀
