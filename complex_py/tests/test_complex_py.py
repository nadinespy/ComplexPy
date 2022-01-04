from __future__ import absolute_import, division, print_function
import os.path as op
import numpy as np
import pandas as pd
import numpy.testing as npt
import complex_py as cp
import pytest as pt

#TODO: use pytest 

# TODO: build fixture
# NOTE: if you use fixtures for testing multiple modules, put fixtures into own file


@pt.fixture
def data_dict_test():
    np.random.seed(1000)
    data_dict = dict()
    data_dict['micro'] = np.random.randn(10, 500)
    data_dict['macro'] = data_dict['micro'].sum(axis=0)
    return data_dict



@pt.mark.parametrize("time_lag,redundancy_func,expected", [(1, 'mmi', {'causal_emergence_phiid': 0.03566983858190928,
     'downward_causation_phiid': 0.006325381684875102,
     'causal_decoupling_phiid': 0.029344456897034178}), (25, 'mmi', {'causal_emergence_phiid': 0.03566983858190928,
     'downward_causation_phiid': 0.006325381684875102,
     'causal_decoupling_phiid': 0.029344456897034178})])                                                                     
def test_causal_emergence_phiid(data_dict_test, time_lag, redundancy_func, expected):
    # test that the right errors get thrown
    with pt.raises(ValueError):
        cp.causal_emergence_phiid(0, time_lag = 1, redundancy_func = 'mmi')
    with pt.raises(ValueError):
        cp.causal_emergence_phiid(dict(), time_lag = 'a', redundancy_func = 'mmi')
        
    result_dict = cp.causal_emergence_phiid(data_dict_test, time_lag = time_lag, redundancy_func = redundancy_func)
    for key in result_dict:
        assert np.isclose(result_dict[key], expected[key])
    # TODO: the same for different time_lag and redundancy_funcs
    # TODO: check whether functions work for different Python versions