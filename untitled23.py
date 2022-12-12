# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 14:50:28 2022

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


import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)


apikey='d60d2f087ecf05f94a3b9b3df34310a9'



crypto=fmp.available_cryptocurrencies(apikey)


ind=fmp.available_indexes(apikey)

av=pd.DataFrame(fmp.sp500_constituent(apikey))

reg=c.get_data(av['symbol'], apikey)    
reg.get_price()
price=reg.price

price.append(list())
price[98].append('^NDX')#symbol nsdq
price[98].append(f.clean_financials(fmp.historical_price_full(apikey, '^NDX')))#price daily
price[98].append(f.clean_financials(fmp.historical_chart(apikey, '^NDX', time_delta='1min')))#price intraday

fingrowth=[]
for i in tqdm(range(0,len(av['symbol'])), desc = 'fingrowth:'):    # your loop's complicated code here
    

    try:
        fingrowth.append(list())
        fingrowth[i].append(av['symbol'][i])
        fingrowth[i].append(f.clean_financials(fmp.balance_sheet_statement(apikey, av['symbol'][i], 'quarter', 22)).reindex(price[i][1].index,method='ffill'))
        fingrowth[i].append(f.clean_financials(fmp.income_statement(apikey, av['symbol'][i], 'quarter', 22)).reindex(price[i][1].index,method='ffill'))
        fingrowth[i].append(f.clean_financials(fmp.cash_flow_statement(apikey, av['symbol'][i], 'quarter', 22)).reindex(price[i][1].index,method='ffill'))
    except: Exception
    pass


regresult=[]

for i in range(0,len(fingrowth)):
    try:
        regresult.append(list())
        regresult[i].append(fingrowth[i][0])
        
        Y = price[i][1]['close']
        price[i][1]['Netincome']=fingrowth[i][2]['netIncome']
        price[i][1]['equity']=fingrowth[i][1]['totalEquity']
        # price[i][1]['growthEPS']=fingrowth[i][2]['netIncome']
        # price[i][1]['nsdq']=price[98][1]['changePercent']
        # X = price[i][1][['equity', 'Netincome']]
        X = price[i][1]['Netincome']
        X = sm.add_constant(X)
        model = sm.OLS(Y,X)
        results = model.fit()
        par=results.params
        # print(results.summary())
    
        regresult[i].append(str(results.summary()))
        regresult[i].append(par)
    except: Exception
    pass

