# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 00:51:13 2023

@author: diego
"""

import requests
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

symbol='GOLD'
start=dt.date(2000, 1, 1)
end=dt.date.today()
def mret(symbol, apikey, start, end):
    df=f.clean_financials(fmp.historical_price_full(apikey, symbol, from_date=start, to_date=end))['close'].rename(symbol)
    return np.log(df/df.shift(1)).dropna()

gold=mret(symbol, apikey, start, end)
p.linep([gold.cumsum()], 'linear', ['goldcumsum'], (6.4, 4.8), False, 'Gold log returns monthly', 'log terms', 'fmp')


