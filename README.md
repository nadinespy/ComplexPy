## emergence_complexity_measures_comparison

# ComplexPy - a Toolbox for Measures of Emergence & Complexity

This is the repository for a Python library that allows to call and apply several measures of emergence and complexity to either empirical or simulated time-series data, and provide guidance for comparisons among and conclusions about different measures. 

I work with yet unpublished software which is why I currently can't work publicly on this library. This will hopefully change in the near future.

# General idea

Measures of complexity operationalize the idea that a system of interconnected parts is both segregated (i.e., parts act independently), and integrated (i.e., parts show unified behaviour). Emergence, on the other hand, is a phenomenon in which a property occurs only in a collection of elements, but not in the individual elements themselves. Both emergence and complexity are promising concepts in the study of the brain (with a close relationship between the two).

Quantifications thereof can take on very different flavours, and there is no one-size-fits-all way to do it. While a plethora of complexity measures have been investigated quite substantially in the last couple of decades (see, e. g., [Wiesner, 2020](https://arxiv.org/pdf/1909.13243.pdf) for an overview), quantifying emergence is completely new territory. A few measures exist (see, e. g., [dynamical independence](https://arxiv.org/pdf/2106.06511.pdf), or [causal emergence](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008289), but they are not readily implementable - they are scattered over different github repositories (or people, if repositories are not existent), and programming languages (including Matlab which is not open source).

A way to easily use & compare a set of state of the art emergence and complexity measures - in an educated way, using only a few lines of code - is thus missing. This is the gap that I’d like to fill.

This library will be useful for anyone interested in micro-macro relationships using time-series data.

# Installation

# Examples 

# Citing

# Contribute

Once I have succeeded in releasing a mini-version of the library, I welcome contributions especially from people with software engineering/coding skills, and/or knowledge in information theory & complex systems, and/or a general interest in mathematical/formal micro-macro relationships, and/or a combination of the things just mentioned. Generally, contributions from anyone at any career stage and with any amount of coding experience will be welcome. Both contribution guidelines and Contributor Code of Conduct will be provided once a first release is achieved. 


[![Build Status](https://travis-ci.org/uwescience/emergence_complexity_measures_comparison.svg?branch=master)](https://travis-ci.org/uwescience/emergence_complexity_measures_comparison)

### Organization of this repository

This repository is inspired by [Shablona](https://github.com/uwescience/shablona), which is a template project for small scientific python projects. It follows the standards and conventions of much of the scientific Python eco-system, making reuse of the code for and collaboration with others easier 

This repository has the following structure:

    emergence_complexity_measures_comparison/
      |- README.md
      |- emergence_complexity_measures_comparison/
         |- __init__.py
         |- emergence_complexity_measures_comparison.py
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


The core of this library is the code inside of `emergence_complexity_measures_comparison/emergence_complexity_measures_comparison.py`.

### Module code

The module code is placed in a file called `emergence_complexity_measures_comparison.py` in the directory called
`emergence_complexity_measures_comparison`. You can type `import emergence_complexity_measures_comparison as ecmc` in an
interactive Python session to make the classes and functions defined inside of the
`emergence_complexity_measures_comparison.py` file in the `ecmc` namespace. 

    from .emergence_complexity_measures_comparison import *

### Project Data

You can create a `emergence_complexity_measures_comparison/data` folder in which you can
organize the data. This provides a standard file-system location for
the data at:

    import os.path as op
    import emergence_complexity_measures_comparison as sb
    data_path = op.join(sb.__path__[0], 'data')

### Testing

This library uses the ['pytest'](http://pytest.org/latest/) library for
testing. 

To run the tests on the command line, change your present working directory to
the top-level directory of the repository (e.g. `/Users/arokem/code/emergence_complexity_measures_comparison`),
and type:

    py.test emergence_complexity_measures_comparison

This will exercise all of the tests in your code directory. If a test fails, you
will see a message such as:


    emergence_complexity_measures_comparison/tests/test_emergence_complexity_measures_comparison.py .F...

    =================================== FAILURES ===================================
    ________________________________ test_cum_gauss ________________________________

      [definition-specific error message]

    emergence_complexity_measures_comparison/tests/test_emergence_complexity_measures_comparison.py:49: AssertionError
    ====================== 1 failed, 4 passed in 0.82 seconds ======================

You can also use a `Makefile` allowing you to run the tests with more
verbose and informative output from the top-level directory, by issuing the
following from the command line:

    make test

### Styling

`flake8` helps make the code more readable, avoid extraneous imports and lines of code, and overall keep a clean project
code-base.

In this library, `flake8` is run on most (but not all) files, on
most (but not all) checks:

```
flake8 --ignore N802,N806 `find . -name *.py | grep -v setup.py | grep -v /doc/`
```

This means, check all .py files, but exclude setup.py and everything in
directories named "doc". Do all checks except N802 and N806, which enforce
lowercase-only names for variables and functions.

The `Makefile` contains an instruction for running this command as well:

    make flake8

### Documentation

This library follows the [numpy docstring standard](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt),
which specifies in detail the inputs/outputs of every function, and specifies how to document additional details, such as references to scientific articles,
notes about the mathematics behind the implementation, etc.

To document `emergence_complexity_measures_comparison`, [sphinx documentation system](http://sphinx-doc.org/) is used. You can build upon a skeleton
documentation system in the `docs` directory already initialized and commited.

Sphinx uses a `Makefile` to build different outputs of your documentation. For example, if you want to generate the HTML rendering of the documentation (web
pages that you can upload to a website to explain the software), you will type:

	make html

This will generate a set of static webpages in the `doc/_build/html`, which you can then upload to a website of your choice.

Alternatively, [readthedocs.org](https://readthedocs.org) (careful, *not* readthedocs.**com**) is a service that will run sphinx for you,
and upload the documentation to their website. To use this service, you will need to register with RTD. After you have done that, you will need to "import your project" from your github account, through the RTD web interface. To make things run smoothly, you also will need to go to the "admin" panel of the project on RTD, and navigate into the "advanced settings" so that you can tell it that your Python configuration file is in `doc/conf.py`:

![RTD conf](https://github.com/uwescience/emergence_complexity_measures_comparison/blob/master/doc/_static/RTD-advanced-conf.png)

 http://emergence_complexity_measures_comparison.readthedocs.org/en/latest/


### Installation

A `emergence_complexity_measures_comparison/version.py` contains all of the information needed for the installation and for setting up the [PyPI page](https://pypi.python.org/pypi/emergence_complexity_measures_comparison) for the software. This also makes it possible to install your software with using `pip` and `easy_install`, which are package managers for Python software. The `setup.py` file reads this information from there and passes it to the `setup` function which takes care of the rest.


### Licensing

This code uses the MIT license. More info can be found in the `LICENSE` file. 


### Getting cited

This library uses [duecredit](http://www.duecredit.org). This is a software library that allows you to annotate the code with the correct way to cite it.
To enable `duecredit`, a file `due.py` is added into the main directory.


### Scripts

A scripts directory is used as a place to experiment with the module code, and as a place to produce scripts that contain a
narrative structure, demonstrating the use of the code, or producing scientific results from the code and the data and telling a story
with these elements.


### Git Configuration

Currently there are two files in the repository which help working with this repository, and which you could extend further:

- `.gitignore` -- specifies intentionally untracked files (such as compiled `*.pyc` files), which should not typically be committed to git (see `man gitignore`)
- `.mailmap` -- if any of the contributors used multiple names/email addresses or his git commit identity is just an alias, you could specify the ultimate name/email(s) for each contributor, so such commands as `git shortlog -sn` could take them into account (see `git shortlog --help`)

