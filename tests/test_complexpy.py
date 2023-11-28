from __future__ import absolute_import, division, print_function
import os.path as op
import numpy as np
import pandas as pd
import numpy.testing as npt
import complexpy as cp
import pytest as pt


# NOTE: if you use fixtures for testing multiple modules, put fixtures into own file


@pt.fixture
def data_dict_test():
    np.random.seed(1000)
    data_dict = dict()
    data_dict['micro'] = np.random.randn(10, 500)
    data_dict['macro'] = data_dict['micro'].sum(axis=0)
    return data_dict

# ----------------------------------------------------------------------------------
# PHIID_WPE()
# ----------------------------------------------------------------------------------

# assert correct data types of inputs/outputs, and ensure 'phiid_wpe', 
# 'phiid_cd', 'phiid_dc' are part of output dict
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [
    (1, 'mmi', {'phiid_wpe': float, 'phiid_dc': float, 'phiid_cd': float}),
    (1, 'mmi', {'phiid_wpe': int, 'phiid_dc': float, 'phiid_cd': float}),
])
def test_phiid_wpe_data_types(data_dict_test, time_lag_for_measure, red_func, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pt.raises(expected):
            cp.phiid_wpe(data_dict_test, time_lag_for_measure=time_lag_for_measure, red_func=red_func)
    else:
        result = cp.phiid_wpe(data_dict_test, time_lag_for_measure=time_lag_for_measure, red_func=red_func)
        assert isinstance(result, dict)
        assert 'phiid_wpe' in result
        assert 'phiid_dc' in result
        assert 'phiid_cd' in result
        assert isinstance(result['phiid_wpe'], float)
        assert isinstance(result['phiid_dc'], float)
        assert isinstance(result['phiid_cd'], float)
        assert not np.isnan(result['phiid_wpe'])
        assert not np.isnan(result['phiid_dc'])
        assert not np.isnan(result['phiid_cd'])


# assert that particular data & set of parameters yield expected result
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [(1, 'mmi',
                                                                   {'phiid_wpe': 0.03566983858190928,
                                                                   'phiid_dc': 0.006325381684875102, 
                                                                   'phiid_cd': 0.029344456897034178}),
                                                                  (25, 'mmi', 
                                                                   {'phiid_wpe': 0.03566983858190928, 
                                                                    'phiid_dc': 0.006325381684875102,
                                                                    'phiid_cd': 0.029344456897034178})])                                                                     
def test_phiid_wpe_output(data_dict_test, time_lag_for_measure, red_func, expected):
    # test that the right errors get thrown for wrong values of data_dict and time_lag_for_measure
    with pt.raises(ValueError):
        cp.phiid_wpe(0, time_lag_for_measure = 1, red_func = 'mmi')
    with pt.raises(ValueError):
        cp.phiid_wpe(dict(), time_lag_for_measure = 'a', red_func = 'mmi')
        
    result_dict = cp.phiid_wpe(data_dict_test, time_lag_for_measure = time_lag_for_measure, 
                               red_func = red_func)
    for key in result_dict:
        assert np.isclose(result_dict[key], expected[key])
    
    # TODO: the same for different time_lag and red_funcs
    # TODO: check whether functions work for different Python versions

# ----------------------------------------------------------------------------------
# PHIID_2SOURCES_2TARGETS()
# ----------------------------------------------------------------------------------

# assert correct data types of inputs/outputs, and ensure 'rtr', 'sts'
# etc. are part of output dict
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [
    (10, 'mmi', {'rtr': float, 'rtx': float, 'rty': float, 'rts': float, 'xtr': float,
                 'xtx': float, 'xty': float, 'xts': float, 'ytr': float, 'ytx': float,
                 'yty': float, 'yts': float, 'str': float, 'stx': float, 'sty': float,
                 'sts': float}),
    (10, 'mmi', {'rtr': float, 'rtx': float, 'rty': float, 'rts': float, 'xtr': float,
                 'xtx': float, 'xty': float, 'xts': float, 'ytr': float, 'ytx': float,
                 'yty': int, 'yts': int, 'str': float, 'stx': float, 'sty': float,
                 'sts': int}),
])
def test_phiid_2sources_2targets_data_types(data_dict_test, time_lag_for_measure, red_func, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pt.raises(expected):
            cp.phiid_2sources_2targets(data_dict_test['micro'], time_lag_for_measure=time_lag_for_measure, 
                                       red_func=red_func)
    else:
        result = cp.phiid_2sources_2targets(data_dict_test['micro'], time_lag_for_measure=time_lag_for_measure, 
                                            red_func=red_func)
        assert isinstance(result, dict)
        required_phiid_dict_keys = ['rtr', 'sts', 'rtx', 'rty', 'rts', 'xtr', 'xtx', 'xty', 'xts', 
                                    'ytr', 'ytx', 'yty', 'yts', 'str', 'stx', 'sty']
        for key in required_phiid_dict_keys:  
            assert key in result
            assert isinstance(result[key], float)
            assert not np.isnan(result[key])

# assert that particular data & set of parameters yield expected result
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [(10, 'mmi', 
                                                                 {'rtr': 0.011698997414625658, 
                                                                  'rtx': 7.678718063891419e-17, 
                                                                  'rty': 0.001765050592875013, 
                                                                  'rts': 0.027125354055413997, 
                                                                  'xtr': 0.001765050592875013, 
                                                                  'xtx': 0.022634204439107224, 
                                                                  'xty': -0.001765050592875013, 
                                                                  'xts': -0.015159861003016419, 
                                                                  'ytr': -1.0070434800019268e-16, 
                                                                  'ytx': 1.0070434800019268e-16, 
                                                                  'yty': 0.013284039258620248, 
                                                                  'yts': -0.013284039258620248, 
                                                                  'str': 0.02693853794868931, 
                                                                  'stx': -0.01581906871219834,
                                                                  'sty': -0.013284039258620248,
                                                                  'sts': 0.042451941408777866}),
])                                                                     
def test_phiid_2sources_2targets_output(data_dict_test, time_lag_for_measure, red_func, expected):

    result_dict = cp.phiid_2sources_2targets(data_dict_test['micro'], time_lag_for_measure=time_lag_for_measure, red_func=red_func)

    for key in result_dict:
        assert result_dict[key] == pt.approx(expected[key])


