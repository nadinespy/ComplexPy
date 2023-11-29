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
# SHANNON_WPE()
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# assert correct data types of inputs/outputs, and ensure 'phiid_wpe', 
# 'phiid_cd', 'phiid_dc' are part of output dict
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("time_lag_for_measure, expected", [
    (1, {'shannon_wpe': float, 'shannon_dc': float, 'shannon_cd': float}),
    (1, {'shannon_wpe': int, 'shannon_dc': float, 'shannon_cd': float}),
])
def test_shannon_wpe_data_types(data_dict_test, time_lag_for_measure, expected):

    # test that the right errors get thrown
    with pt.raises(expected):
        cp.shannon_wpe(data_dict_test, time_lag_for_measure='time')
    with pt.raises(ValueError):
        cp.shannon_wpe(0, time_lag_for_measure=1)
    with pt.raises(ValueError):
        cp.shannon_wpe(dict(), time_lag_for_measure='a')

    result = cp.shannon_wpe(data_dict_test, time_lag_for_measure=time_lag_for_measure)
        
    assert isinstance(result, dict)

    required_shannon_dict_keys = ['shannon_wpe', 'shannon_dc', 'shannon_cd']
    for key in  required_shannon_dict_keys:  
        assert key in result
        assert isinstance(result[key], float)
        assert not np.isnan(result[key])

# ----------------------------------------------------------------------------------
# assert that particular data & set of parameters yield expected result
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("time_lag_for_measure, expected", [(1, {'shannon_wpe': -0.0075746999352517864,
                                                             'shannon_dc': -0.0033544310640316564,
                                                             'shannon_cd': 0.0072812758416552935}),
                                                       (25, {'shannon_wpe': -0.006368655884905357,
                                                             'shannon_dc': -0.0035834375888473186,
                                                             'shannon_cd': 0.011226937782589678})])                                                                     
def test_shannon_wpe_output(data_dict_test, time_lag_for_measure, expected):
    
    result_dict = cp.shannon_wpe(data_dict_test, time_lag_for_measure=time_lag_for_measure)
    for key in result_dict:
        assert result_dict[key] == pt.approx(expected[key])
    
    # TODO: the same for different time_lag and red_funcs
    # TODO: check whether functions work for different Python versions


# ----------------------------------------------------------------------------------
# PHIID_WPE()
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# assert correct data types of inputs/outputs, and ensure 'phiid_wpe', 
# 'phiid_cd', 'phiid_dc' are part of output dict
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [
    (1, 'mmi', {'phiid_wpe': float, 'phiid_dc': float, 'phiid_cd': float}),
    (1, 'mmi', {'phiid_wpe': int, 'phiid_dc': float, 'phiid_cd': float}),
])
def test_phiid_wpe_data_types(data_dict_test, time_lag_for_measure, red_func, expected):

     # test that the right errors get thrown for wrong values of data_dict 
     # and time_lag_for_measure
    with pt.raises(ValueError):
        cp.phiid_wpe(0, time_lag_for_measure=1, red_func='mmi')
    with pt.raises(ValueError):
        cp.phiid_wpe(dict(), time_lag_for_measure='a', red_func='mmi')
    with pt.raises(ValueError):
        cp.phiid_wpe(data_dict_test, time_lag_for_measure=time_lag_for_measure, red_func=[])

    result_dict = cp.phiid_wpe(data_dict_test, time_lag_for_measure=time_lag_for_measure,
                               red_func=red_func)

    assert isinstance(result_dict, dict)

    required_phiid_dict_keys = ['phiid_wpe', 'phiid_dc', 'phiid_cd']
    for key in  required_phiid_dict_keys:  
        assert key in result_dict
        assert isinstance(result_dict[key], float)
        assert not np.isnan(result_dict[key])

# ----------------------------------------------------------------------------------
# assert that particular data & set of parameters yield expected result
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [(1, 'mmi',
                                                                   {'phiid_wpe': 0.03566983858190928,
                                                                   'phiid_dc': 0.006325381684875102, 
                                                                   'phiid_cd': 0.029344456897034178}),
                                                                  (25, 'mmi', 
                                                                   {'phiid_wpe': 0.03566983858190928, 
                                                                    'phiid_dc': 0.006325381684875102,
                                                                    'phiid_cd': 0.029344456897034178})])                                                                     
def test_phiid_wpe_output(data_dict_test, time_lag_for_measure, red_func, expected):
    
    result_dict = cp.phiid_wpe(data_dict_test, time_lag_for_measure = time_lag_for_measure, 
                               red_func = red_func)
    for key in result_dict:
        assert np.isclose(result_dict[key], expected[key])
    
    # TODO: the same for different time_lag and red_funcs
    # TODO: check whether functions work for different Python versions

# ----------------------------------------------------------------------------------
# PHIID_2SOURCES_2TARGETS()
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# assert correct data types of inputs/outputs, and ensure 'rtr', 'sts'
# etc. are part of output dict
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("time_lag_for_measure, red_func, expected", [
    (10, 'mmi', {'rtr': float, 'rtx': float, 'rty': float, 'rts': float, 'xtr': float,
                 'xtx': float, 'xty': float, 'xts': float, 'ytr': float, 'ytx': float,
                 'yty': float, 'yts': float, 'str': float, 'stx': float, 'sty': float,
                 'sts': float}),
    (10, 0, TypeError),
])
def test_phiid_2sources_2targets_data_types(data_dict_test, time_lag_for_measure,
                                            red_func, expected):
    
    # test that the right errors get thrown for wrong values 
    with pt.raises(ValueError):
        cp.phiid_wpe(0, time_lag_for_measure=1, red_func='mmi')
    with pt.raises(ValueError):
        cp.phiid_wpe(dict(), time_lag_for_measure='a', red_func='mmi')
    with pt.raises(ValueError):
        cp.phiid_2sources_2targets(data_dict_test['micro'],
                                   time_lag_for_measure='time',
                                   red_func=red_func)
        
    result_dict = cp.phiid_2sources_2targets(data_dict_test['micro'],
                                             time_lag_for_measure=time_lag_for_measure,
                                             red_func=red_func)
        
    assert isinstance(result_dict, dict)
    
    required_phiid_dict_keys = ['rtr', 'sts', 'rtx', 'rty', 'rts', 'xtr', 'xtx', 'xty', 'xts',
                                'ytr', 'ytx', 'yty', 'yts', 'str', 'stx', 'sty']
    for key in required_phiid_dict_keys:  
        assert key in result_dict
        assert isinstance(result_dict[key], float)
        assert not np.isnan(result_dict[key])

# ----------------------------------------------------------------------------------
# assert that particular data & set of parameters yield expected result
# ----------------------------------------------------------------------------------
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

    result_dict = cp.phiid_2sources_2targets(data_dict_test['micro'],
                                             time_lag_for_measure=time_lag_for_measure,
                                             red_func=red_func)

    for key in result_dict:
        assert result_dict[key] == pt.approx(expected[key])


# ----------------------------------------------------------------------------------
# GET_RESULT_FOR_MEASURE()
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# assert correct data types of inputs/outputs, and ensure 'rtr', 'sts'
# etc. are part of output dict
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("measure_name, measure_func, measure_params_dict, expected", [
    ('phiid_wpe', cp.phiid_wpe, {'time_lag_for_measure': [1], 'red_func': ['mmi']},
                       pd.DataFrame({'value': [float,
                                               float,
                                               float], 
                                     'measure': [str, str, str], 
                                     'time_lag_for_measure': [int, int, int]})),
                       ('shannon_wpe', cp.shannon_wpe, {'time_lag_for_measure': [1]},
                       pd.DataFrame({'value': [float,
                                               float,
                                               float], 
                                     'measure': [str, str, str], 
                                     'time_lag_for_measure': [int, int, int]})),
])
def test_get_result_for_measure_data_types(data_dict_test, measure_name, measure_func,
                                           measure_params_dict, expected):
    
    # test that the right errors get thrown for wrong values 
    with pt.raises(expected):
        cp.get_result_for_measure('phiid_wpe', cp.phiid_wpe,
                                  {'time_lag_for_measure': [1], 'red_func': [3]},
                                  data_dict_test)
    with pt.raises(ValueError):
        cp.get_result_for_measure(0, cp.shannon_wpe, {'time_lag_fo_measure': [1], 'red_func': ['mmi']},
                                  data_dict_test)
    with pt.raises(ValueError):
        cp.get_result_for_measure('phiid_shannon', dict(), {'time_lag_fo_measure': [1], 'red_func': ['mmi']},
                                  data_dict_test)

    result_df = cp.get_result_for_measures(measure_name, measure_func,
                                               measure_params_dict, data_dict_test)
        
    assert isinstance(result_df, pd.DataFrame)
    
    required_df_columns = ['value', 'measure']
    for column in required_df_columns:  
        assert column in result_df
        assert isinstance(result_df['value'], float)
        assert not np.isnan(result_df['value'])
        assert isinstance(result_df['measure'], str)

# ----------------------------------------------------------------------------------
# assert that particular data & set of parameters yield expected result
# ----------------------------------------------------------------------------------
@pt.mark.parametrize("measure_name, measure_func, measure_params_dict, expected",
                     [('phiid_wpe', cp.phiid_wpe, {'time_lag_for_measure': [1], 'red_func': ['mmi']},
                       pd.DataFrame({'value': [0.03566983858190928,
                                               0.006325381684875102,
                                               0.029344456897034178], 
                                     'measure': ['phiid_wpe','phiid_dc', 'phiid_cd'], 
                                     'time_lag_for_measure': [1, 1, 1]})),
                       ('shannon_wpe', cp.shannon_wpe, {'time_lag_for_measure': [1]},
                       pd.DataFrame({'value': [-0.0075746999352517864,
                                               -0.0033544310640316564,
                                               0.0072812758416552935],
                                    'measure': ['shannon_wpe','shannon_dc', 'shannon_cd'],
                                    'time_lag_for_measure': [1, 1, 1]}))
])                                                                     
def test_get_result_for_measure_output(data_dict_test, measure_name, measure_func,
                                       measure_params_dict, expected):

    # assert expected results for dataframe
    result_df = cp.get_result_for_measure(measure_name, measure_func, measure_params_dict,
                                          data_dict_test)

    assert isinstance(result_df, pd.DataFrame)
    assert result_df['value'].all == pt.approx(expected['value'].all)

    required_result_df_columns = ['measure', 'value']
    for column in required_result_df_columns:  
        assert column in result_df
    
    assert isinstance(result_df.loc[:,'value'], float)
    assert not np.isnan(result_df.loc[:,'value'])
    assert isinstance(result_df.loc[:,'measure'], str)


