from __future__ import absolute_import, division, print_function
import os.path as op
import numpy as np
import pandas as pd
import numpy.testing as npt
import emergence_complexity_measures_comparison as ecmc

data_path = op.join(sb.__path__[0], 'data')
practical_measures_causal_emergence_path = op.join(ecmc.__path__[0], 'practical_measures_causal_emergence')
phiid_path = op.join(ecmc.__path__[0], 'phiid')

#TODO: use pytest 
