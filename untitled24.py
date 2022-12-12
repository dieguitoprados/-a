# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 18:47:44 2022

@author: diegu
"""


import matplotlib.dates as mdates
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
from scipy.stats import skew, kurtosis, chi2, linregress
import waterfall_chart
from scipy.stats import norm
import sys
from tqdm import tqdm
import matplotlib.cm as cm


import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)


apikey='d60d2f087ecf05f94a3b9b3df34310a9'

stocks=['^GSPC', 'SPY']

data=c.get_data(stocks, apikey)

data.sp_financials()

spfin=data.sp_fin

x=pd.DataFrame(index=['x', 'y', 'cat'])
for i in range(len(spfin)):
    x[spfin[i][0]]=spfin[i][6]['netIncome'][len(spfin[i][6]['netIncome'])-1],spfin[i][7]['netProfitMarginTTM'].values,spfin[i][2]
    
data=data.transpose()

x=x.transpose()
c.scatt(j)


for i in range(len(spfin)):
    for industry in spfin[i][3]:
        
        
        











fmp.market_capitalization(apikey, 'MMM')

tt=f.ttm(f.clean_financials(fmp.income_statement(apikey, 'MMM', 'quarter')))


colors=cm.viridis

colors = cm.viridis(np.linspace(0, 1, len))


