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


The core of this library is the code inside of `src/complexpy.py`.

### Module code

The module code is placed in a file called `complexpy.py` in the directory called
`complexpy`. You can type `import complexpy as cp` in an interactive Python session to make the classes and functions defined inside of the
`complex_py.py` file in the `cp` namespace. 

    from .complexpy import *

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


(see also a description of this project in this [OLS-4 speed blog post](https://openlifesci.org/posts/2022/03/17/ols-4-participant-nadine-spychala/))