# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 00:24:30 2023

@author: diego
"""

import time
import pandas_datareader.data as web
import statsmodels.api as sm
import datetime as dt
import pandas as pd
import numpy as np
import requests
import importlib
from tqdm import tqdm
import datetime as dt
import matplotlib.pyplot as plt
import scipy.stats as scipy
from scipy.stats import skew, kurtosis, chi2, linregress
import plots as p
from sec_edgar_api import EdgarClient
edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
s=time.time()
import functions_diego as f
importlib.reload(f)
import fmpsdk as fmp

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
apikey='cdcb171caeb7cc3ab258fb24c77918a1'
from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')


