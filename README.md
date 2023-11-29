## complex_py

# ComplexPy - a Library for Measures of Emergence & Complexity
This is the repository for a Python library that allows to call and apply several measures of emergence and complexity to either empirical or simulated time-series data, and provide guidance for comparisons among and conclusions about different measures (see a description of this project also in this [OLS-4 speed blog: Developing a library in Python for applying measures of emergence and complexity](https://openlifesci.org/posts/2022/03/17/ols-4-participant-nadine-spychala/)). 

It has long been private due to unsettled publications statuses of software used, and has been made public only very recently. For that reason, preparations to make it ready for contributions from others lay dormant. I aim to change this soon, and all necessary info (e. g., contributor's guide) will be included, and further work on the code base that is necessary to have a minimally working library will follow.

# General Idea
Multi-scale relationships in emergent phenomena and complex systems are studied across various disciplines. They explore the unresolved subject of how macro- and micro-scales relate to each other – are they independent, reducible, or is their relationship more complex? Examples of the phenomena in question would be, for instance, the way galaxies are formed, how crowds and herds behave, or how conscious human experience arises from the collective activity of neurons. An emergence poster child is given by a moving flock of starlings, the aesthetics of which is appealing to many.

[INSERT FLOCK VIDEO]

Historically, the lack of formalism hindered empirical investigation, but recent research introduced quantitative measures based on information theory to quantify emergence in systems whose components evolve over *time*. Measuring emergence is new terrain, therefore requiring extensive testing and cumulative evidence. A Python library with all measures at one place will facilitate this endeavour, and help drive the iterative cycle of theory-building and empirical testing. 

## Measures of Complexity & Emergence
Measures of complexity operationalize the idea that a system of interconnected parts is both segregated (i.e., parts act "independently"), and integrated (i.e., parts show "unified" behaviour, they form a "coherent whole"), the coexistence of which makes a system "complex". Take as an example the brain: all neurons eventually work together to guide behaviour and ultimately ensure survival, but parts thereof may "do their own thing" quite in separation from the rest of the system (e. g., there are language- and motor-focused parts of the brain), or they may be redundant (if some part of the brain ceases to function, conscious experience may continue to unfold, as it doesn't "sit" in any particular area). Emergence, on the other hand, is a phenomenon where a property occurs only in a collection of elements (e. g., the moving shape of a flock of starlings), but not in the individual elements themselves (e. g., the single birds). Both emergence and complexity are studied in the context of the brain.

Quantifications of emergence can take on very different flavours - depending how emergence is defined - and there is no one-size-fits-all way to do it. While a plethora of complexity measures have been investigated quite substantially in the last couple of decades (see, e. g., [Wiesner, 2020](https://arxiv.org/pdf/1909.13243.pdf) for an overview), quantifying emergence is completely new territory (see, e. g., [Dynamical Independence](https://arxiv.org/pdf/2106.06511.pdf), or [Whole-Parts Emergence](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008289)

## What this Library Does
Measures are not readily implementable - they are scattered over different GitHub repositories and programming languages (including MATLAB which is not open source). They are not made for use in different environments, hence reproducibility of applications is hampered. 

A way to easily use & compare a set of state of the art emergence and complexity measures - in an educated way, using only a few lines of code, and *across environments* - is thus missing. This is the gap this library is supposed to fill.

This library will be useful for anyone interested in micro/macro relationships using time-series data (simulated or empirical).

# Installation

# Examples 

# Citing

# Contribute

Once I have succeeded in releasing a mini-version of the library, I welcome contributions especially from people with software engineering/coding skills, and/or knowledge in information theory & complex systems, and/or a general interest in mathematical/formal micro-macro relationships, and/or a combination of the things just mentioned. Generally, contributions from anyone at any career stage and with any amount of coding experience will be welcome. Both contribution guidelines and Contributor Code of Conduct will be provided once a first release is achieved. 

### Organization of this repository

This repository is adapted from [Shablona](https://github.com/uwescience/shablona), which is a template project for small scientific python projects. It follows the standards and conventions of much of the scientific Python eco-system, making reuse of the code for and collaboration with others easier 

This repository has the following structure:

    complex_py/
      |- README.md
      |- complex_py/
         |- __init__.py
         |- complex_py.py
         |- due.py
         |- data/
            |- ...
         |- tests/
            |- ...
      |- doc/
         |- Makefile
         |- conf.py
         |- sphinxext/
            |- ...
         |- _static/
            |- ...
      |- setup.py
      |- .travis.yml
      |- .mailmap
      |- appveyor.yml
      |- LICENSE
      |- Makefile
      |- ipynb/
         |- ...


The core of this library is the code inside of `complex_py/complex_py.py`.

### Module code

The module code is placed in a file called `complex_py.py` in the directory called
`complex_py`. You can type `import complex_py as ecmc` in an
interactive Python session to make the classes and functions defined inside of the
`complex_py.py` file in the `ecmc` namespace. 

    from .complex_py import *

### Project Data

You can create a `complex_py/data` folder in which you can
organize the data. This provides a standard file-system location for
the data at:

    import os.path as op
    import complex_py as sb
    data_path = op.join(sb.__path__[0], 'data')

### Testing

This library uses the ['pytest'](http://pytest.org/latest/) library for
testing. 

To run the tests on the command line, change your present working directory to
the top-level directory of the repository (e.g. `/Users/nadinespy/code/complex_py`),
and type:

    py.test complex_py

This will exercise all of the tests in your code directory. If a test fails, you
will see a message such as:


    complex_py/tests/test_complex_py.py .F...

    =================================== FAILURES ===================================
    ________________________________ test_phiid_wpe ________________________________

      [definition-specific error message]

    complex_py/tests/test_complex_py.py:49: AssertionError
    ====================== 1 failed, 4 passed in 0.82 seconds ======================

You can also use a `Makefile` allowing you to run the tests with more
verbose and informative output from the top-level directory, by issuing the
following from the command line:

    make test

### Styling

### Documentation

This library follows the [numpy docstring standard](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt),
which specifies in detail the inputs/outputs of every function, and specifies how to document additional details, such as references to scientific articles,
notes about the mathematics behind the implementation etc.

### Licensing

This code uses the MIT license. More info can be found in the `LICENSE` file. 

### Getting cited
