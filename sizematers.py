# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 16:36:42 2022

@author: diego
"""

import time
import statsmodels.api as sm
import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
import requests
import fmpsdk as fmp
import importlib
import datetime as dt
import matplotlib.pyplot as plt
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as scipy
from scipy.stats import skew, kurtosis, chi2, linregress
import seaborn as sns
from itertools import combinations
import matplotlib.pylab as pl
from matplotlib import lines
from matplotlib import patches
import matplotlib.dates as mdate
import plots as p

s=time.time()
import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')

ffunds = fred.get_series('DFF')
yields=pd.DataFrame(index=ffunds.index)
yields['1d']=ffunds
yields['1M'] = fred.get_series('DGS1MO')
yields['3M'] = fred.get_series('DGS3MO')
yields['6M'] = fred.get_series('DGS6MO')
yields['dgs1'] = fred.get_series('DGS1')
yields['dgs2'] = fred.get_series('DGS2')
yields['dgs3'] = fred.get_series('DGS3')
yields['dgs5'] = fred.get_series('DGS5')
yields['dgs7'] = fred.get_series('DGS7')
yields['dgs10'] = fred.get_series('DGS10')
yields['dgs20'] = fred.get_series('DGS20')
cpi = fred.get_series('CPILFESL')
cpi=(cpi/cpi.shift(12)-1)

yields['dgs30'] = fred.get_series('DGS30')
yields=yields.fillna(method='ffill')
yields.index=pd.to_datetime(yields.index)
yields=yields.loc[dt.datetime(2000, 1, 1):]

s=[(6.4, 4.8), (6.4, 6.4), (6.4, 3.8)]
for size in s:
    fig, ax, colors, im=p.layout(size, False,'linear')
    
    p.line([cpi, (ffunds/100).rolling(30).mean()], ['CPI', 'Effective Funds Rate'], colors, ax)

p.linep([cpi, (ffunds/100).rolling(30).mean()], 'linear', ['CPI', 'Effective Funds Rate'], (6.4,4.8), False, 'Inflation vs. Federal Funds Rate', 'Will we win the battle on inflation by rsing interest rates?', 'Federal Reserve Bank of Saint Luis')
