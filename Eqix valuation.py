# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 16:05:19 2022

@author: Diego Prados: Greenfield investment solutions
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
import plots as p
s=time.time()
import functions_diego as f
importlib.reload(f)
import yfinance as yf

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))

from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')

#load variables for regression

directory = 'C:\\Users\\diego\\Downloads\\EQIX.CSV' # hardcoded
di = 'C:\\Users\\diego\\Downloads\\fuck.CSV' # hardcoded
data = pd.read_csv(di)
date=data.iloc[:1152]
date=date.iloc[880:]
date.index=pd.to_datetime(date['Date'], format='%Y%m')
date.index=date.index.date
date=date.drop('Date', axis=1)
date=date.loc[dt.date(2014, 1, 1):]

eqix = yf.Ticker("NFLX")
# ng = yf.Ticker("NG=F")

# # get stock info
# eqix.info

# # get historical market data
eq = eqix.history(period="max", interval = "1mo", )
eq=100*(eq['Close']/eq['Close'].shift(1)-1)

date['eqix']=eq
date['aaa'] = fred.get_series('AAA')
date['baa' ]= fred.get_series('BAA')
date['spread']=date['baa']-date['aaa']
date['be']=fred.get_series('T5YIEM')
date['cpi']=fred.get_series('CPIAUCSL')
date['ue']=date['be']-date['cpi']/date['cpi'].shift(1)
date['dgs1'] = fred.get_series('GS1')
date['exi']=date['dgs1']-date['RF']
date=date.dropna()

capm=pd.DataFrame(date[['eqix', 'RF', 'Mkt-RF']])
print('CAPM') 
Y=capm['eqix']-capm['RF']
X=capm['Mkt-RF']
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results=model.fit(cov_type='HC1')
print(results.summary())
capmean=((1+capm.mean()/100)**12)-1
capmpar=results.params
recapm=date['dgs1'][-1]/100+capmpar[1]*capmean[2]


ffm=pd.DataFrame(date[['eqix', 'RF', 'Mkt-RF', 'SMB', 'HML']])
print('FAMA-FRENCH Model')
Y=ffm['eqix']-ffm['RF']
X=ffm[['Mkt-RF', 'SMB', 'HML']]
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results=model.fit(cov_type='HC1')
print(results.summary())
ffmean=((1+ffm.mean()/100)**12)-1
ffmpar=results.params
reffm=date['dgs1'][-1]/100+ffmpar[1]*ffmean[2]+ffmpar[2]*ffmean[3]+ffmpar[3]*ffmean[4]


apmw=pd.DataFrame(date[['eqix', 'RF', 'Mkt-RF', 'SMB', 'HML', 'spread']])
print('Arbitrage Pricing Model without inflation')
Y=apmw['eqix']-apmw['RF']
X=apmw[['Mkt-RF', 'SMB', 'HML', 'spread']]
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results=model.fit(cov_type='HC1')
print(results.summary())
apmwmean=((1+apmw.mean()/100)**12)-1
apmwpar=results.params
reapmw=date['dgs1'][-1]/100+apmwpar[1]*apmwmean[2]+apmwpar[2]*apmwmean[3]+apmwpar[3]*apmwmean[4]+apmwpar[4]*apmw['spread'].mean()/100


apmexi=pd.DataFrame(date[['eqix', 'RF', 'Mkt-RF', 'SMB', 'HML','spread', 'exi']])
print('Arbitrage Pricing Model with 1y-1m')
Y=apmexi['eqix']-apmexi['RF']
X=apmexi[['Mkt-RF', 'SMB', 'HML', 'spread', 'exi']]
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results=model.fit(cov_type='HC1')
a=results.params
print(results.summary())
apmeximean=((1+apmexi.mean()/100)**12)-1
apmexipar=results.params
reapmexi=date['dgs1'][-1]/100+apmexipar[1]*apmeximean[2]+apmexipar[2]*apmeximean[3]+apmexipar[3]*apmeximean[4]+apmexipar[4]*apmexi['spread'].mean()/100+apmexipar[5]*apmexi['exi'].mean()/100


apmbe=pd.DataFrame(date[['eqix', 'RF', 'Mkt-RF', 'SMB', 'HML','spread', 'ue']]).dropna()
print('Arbitrage Pricing Model with breakeven 5yr')
Y=apmbe['eqix']-apmbe['RF']
X=apmbe[['Mkt-RF', 'SMB', 'HML', 'spread', 'ue']]
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results=model.fit(cov_type='HC1')
print(results.summary())
apmbemean=((1+apmbe.mean()/100)**12)-1
apmbepar=results.params
reapmbe=date['dgs1'][-1]/100+apmexipar[1]*apmeximean[2]+apmexipar[2]*apmeximean[3]+apmexipar[3]*apmeximean[4]+apmexipar[4]*apmbe['spread'].mean()/100+apmexipar[5]*apmbe['ue'].mean()/100

print(results.get_prediction())







print('recapm: '+str(recapm))
print('reffm: '+str(reffm))
print('reapmw: '+str(reapmw))
print('reapmexi: '+str(reapmexi))
print('reapmbe: '+str(reapmbe))
