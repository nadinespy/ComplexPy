## complexpy
[![Status: WIP](https://img.shields.io/badge/status-WIP-orange.svg)](#)
[![Stage: Research prototype](https://img.shields.io/badge/stage-research%20prototype-purple.svg)](#)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](#contribute)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10|3.11](https://img.shields.io/badge/python-3.10%20|%203.11-blue.svg)](#)
[![Poetry](https://img.shields.io/badge/packaging-poetry-60A5FA.svg)](#)

# ComplexPy - a Python Library for Measures of Emergence & Complexity
This is the repository for a Python library whose aim is to apply several measures of emergence & complexity to either empirical or simulated time-series data, and provide guidance for comparisons among and conclusions about different measures. It thereby aims to enhance reproducibility, accessibility, systematicity, inclusivity, as well as drive the iterative cycle of theory and application in relevant fields of research.

## Emergence & Complexity - an Introduction
Multi-scale relationships in emergent phenomena and complex systems are studied across various disciplines. They explore the unresolved subject of how macro- and micro-scales relate to each other – are they independent, reducible, or is their relationship more complex? Examples of the phenomena in question would be, for instance, the way galaxies are formed, how crowds and herds behave, or how conscious human experience arises from the collective activity of neurons. An emergence poster child is given by a moving flock of starlings, the aesthetics of which is appealing to many.

[FLOCK_VIDEO](https://github.com/nadinespy/ComplexPy/assets/46372572/f487455d-a412-4fe9-b69b-f52866715ee3)

Historically, the lack of formalism hindered empirical investigation, but recent research introduced quantitative measures based on information theory to quantify emergence in systems whose components evolve over *time*. Measuring emergence is new terrain, therefore requiring extensive testing and cumulative evidence. A Python library with all measures at one place will facilitate this endeavour, and help drive the iterative cycle of theory-building and empirical testing. 

## Measures of Complexity & Emergence
Measures of complexity operationalize the idea that a system of interconnected parts is both segregated (i.e., parts act "independently"), and integrated (i.e., parts show "unified" behaviour, they form a "coherent whole"), the coexistence of which makes a system "complex". Take as an example the brain: all neurons eventually work together to guide behaviour and ultimately ensure survival, but parts thereof may "do their own thing" quite in separation from the rest of the system (e. g., there are language- and motor-focused parts of the brain), or they may be redundant (if some part of the brain ceases to function, conscious experience may continue to unfold, as it doesn't "sit" in any particular area). Emergence, on the other hand, is a phenomenon in which a property occurs only in a collection of elements (e. g., the moving shape in a flock of starlings, or consciousness in a sufficient set of neurons), but not in the individual elements themselves (e. g., the single birds, or the single neurons). Both emergence and complexity are studied in the context of the brain.

Quantifications of emergence can take on very different flavours - depending how emergence is defined - and there is no one-size-fits-all way to do it. Most of them operationalize multi-scale measures using information-theoretic language and are applicable to time-series data. While a plethora of complexity measures have been investigated quite substantially in the last couple of decades (see, e. g., [Wiesner, 2020](https://arxiv.org/pdf/1909.13243.pdf) for an overview), quantifying emergence is completely new territory (see, e. g., [Dynamical Independence](https://arxiv.org/pdf/2106.06511.pdf), or [Whole-Parts Emergence](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008289))

## Goals for this Library
Measures are not readily implementable - they are scattered over different GitHub repositories and programming languages (including MATLAB which is not open source). They are not made for use in different environments, and (academic) resources about them are not well accessible. Hence, reproducibility of applications is overall hampered. 

A way to easily and reproducibly use & compare a set of state of the art emergence and complexity measures - in an educated way, using only a few lines of code, and across environments - is thus missing. This is the gap this library is supposed to fill. 

This library will be useful for anyone interested in micro/macro relationships using time-series data (simulated or empirical), and for anyone aiming to make research on emergence & complexity more *open*, *reproducible*, *systematic*, *inclusive*, and thus *better*.

## A Minimally Viable Model - What This Library Can Already Do For You
Imagine you want to generate time-series data according to some time-series model, the function of which is stored in ```model_functions``` while the model-specific parameters are in ```model_variables```, and intend to compute several measures of emergence, as defined in ```emergence_functions``` with correspdonding measure-specific parameters in ```measure_variables```. You can then use the following line of code to do a sweep over all models and measures, including all involved parameters. (```parameters``` stores all parameters from both ```model_variables``` and ```measure_variables```.)
 
```r
import complex_py as cp

emergence_df = cp.compute_emergence(model_functions, model_variables, emergence_functions, measure_variables, parameters)
```

Calling single emergence functions is possible, too:
```r
cp.phiid_wpe()
cp.shannon_wpe()
```

(```cp.phiid_wpe()``` calculates Whole-Parts-Emergence based on Partial Information Decomposition, whereas ```cp.shannon_wpe()``` computes the same measure based on standard Shannon information.)

## Installation

**Requirements:** Python 3.10-3.11 • MATLAB R2023b+ • Poetry

**Important:** The `matlabengine` version must match your MATLAB version.

| Your MATLAB | Edit pyproject.toml to |
|-------------|------------------------|
| R2023b | `matlabengine = "~23.2.0"` (default) |
| R2024a | `matlabengine = "~24.1.0"` |
| R2025a | `matlabengine = "~25.1.0"` |
| R2025b | `matlabengine = "~25.2.0"` |

**Quick install:**

```bash
# 1. Check your MATLAB version & update pyproject.toml if needed
matlab -batch "disp(matlabroot)"  # e.g., /usr/local/MATLAB/R2025a

# 2. Set MATLAB library path in ~/.bashrc (adjust R2025a to your version):
export LD_LIBRARY_PATH=/usr/local/MATLAB/R2025a/bin/glnxa64:$LD_LIBRARY_PATH
source ~/.bashrc

# 3. Install
poetry env use python3.11
poetry install

# 4. Verify
poetry run python -c "import complexpy; print('Success!')"
```

**Need help?** See the **[Installation Guide](doc/installation.md)** for detailed instructions and troubleshooting.

## Documentation

- **[Installation Guide](doc/installation.md)** - Comprehensive installation instructions and troubleshooting
- **[Getting Started Guide](doc/getting-started.md)** - Your first emergence analysis walkthrough
- **[Architecture](doc/architecture.md)** - Technical implementation details and design
- **[Theory](doc/theory.md)** - Understanding emergence, complexity, and information theory
- **[How-To Guides](doc/how-to/)** - Task-specific recipes and templates (coming soon)
- **[Contributing](CONTRIBUTING.md)** - How to contribute to ComplexPy

## Roadmap

ComplexPy aims to become the go-to toolkit for emergence and complexity research. Key goals:

- **Pure Python**: Remove MATLAB dependency for wider accessibility
- **More Measures**: Add Dynamical Independence, G-emergence, complexity measures
- **More Models**: Support 8-node networks, Kuramoto oscillators, empirical data loaders
- **Better Tooling**: Comprehensive tests, CI/CD, automated workflows
- **Rich Documentation**: Tutorials, examples, API reference

See [doc/architecture.md - Future Plans](doc/architecture.md#future-plans) for detailed technical roadmap and implementation plans.

## Citing

If you use ComplexPy in academic work, please cite both the software and the underlying methods you employ.

### Cite the software
Until a first tagged release is available, please cite the repository with the commit you used (or the access date).

Plain text (replace placeholders):
```
Spychala, N. (2025). ComplexPy. GitHub repository.
Commit: <commit-sha>, retrieved <YYYY-MM-DD>.
https://github.com/nadinespy/ComplexPy
```

BibTeX (replace placeholders):
```bibtex
@software{Spychala_ComplexPy,
  author  = {Spychala, Nadine},
  title   = {ComplexPy},
  year    = {2025},
  note    = {GitHub repository, commit: <commit-sha>, retrieved <YYYY-MM-DD>},
  url     = {https://github.com/nadinespy/ComplexPy}
}
```

### Cite the methods
Also cite the specific measures you use. Suggested references:

- If you use Integrated Information Decomposition: [Towards an extended taxonomy of information dynamics](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008289).

- If you use Whole-Parts Emergence: [Reconciling Emergences: An information-theoretic approach to identify causal emergence in multivariate data](https://arxiv.org/abs/2004.08220).

- If you use Common Change in Surprisal (CCS) as a redundancy measure for Integrated Information Decomposition: [Measuring multivariate redundant information with pointwise common change in surprisal (CCS)](https://www.mdpi.com/1099-4300/19/7/318).

## Contributing

Contributions are very welcome from anyone - whether your background is software engineering, information theory, complex systems, or you're simply interested in formal micro-macro relationships.

**Get started:**
- Read the [Contributing Guide](CONTRIBUTING.md) for setup and guidelines
- Check the [How-To templates](doc/how-to/README.md) for contribution ideas
- Open an issue to discuss ideas or report bugs
- Email nadine.spychala@gmail.com for questions

**Priority areas:**
- Port MATLAB code to Python
- Add tests and improve documentation
- Implement new models or measures

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Licensing

This code uses the MIT license. More info can be found in the `LICENSE` file. 

