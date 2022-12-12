# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:38:57 2022

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
import plots as p
from sec_edgar_api import EdgarClient
edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
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

di = 'C:\\Users\\diego\\Downloads\\fuck.CSV' # hardcoded
data = pd.read_csv(di)
date=data.iloc[:1152]
date=date.iloc[880:]
date.index=pd.to_datetime(date['Date'], format='%Y%m')
date.index=date.index.date
date=date.drop('Date', axis=1)
date=date.loc[dt.date(2010, 1, 1):]

xle = yf.Ticker("XLE")
info=xle.info
closes=pd.DataFrame()
# # get historical market data
xle = xle.history(period="max", interval = "1mo")
xle= xle.dropna()
closes['XLE']=xle['Close']
xle=100*(xle['Close']/xle['Close'].shift(1)-1)

oil= yf.Ticker("CL=F")
oil= oil.history(period="max", interval = "1mo")
oil=100*(oil['Close']/oil['Close'].shift(1)-1)



date['XLE']=xle

date['oil']=oil
for i in range(len(info['holdings'])):
    hist=yf.Ticker(info['holdings'][i]['symbol']).history(period="max", interval = "1mo")
    hist=hist.dropna()
    closes[info['holdings'][i]['symbol']]=hist['Close']
    hist=100*(hist['Close']/hist['Close'].shift(1)-1)
    date[info['holdings'][i]['symbol']]=hist
    
date['aaa'] = fred.get_series('AAA')
date['baa' ]= fred.get_series('BAA')
date['spread']=date['baa']-date['aaa']
date['be']=fred.get_series('T5YIEM')
date['exp']=fred.get_series('EXPINF1YR')
date['cpi']=fred.get_series('CPIAUCSL')
date['CPIeu']=fred.get_series('EA19CPALTT01GYM')
date['cpiu']=fred.get_series('GBRCPIALLMINMEI')
date['CPIus']=(date['cpi']/date['cpi'].shift(12)-1)*100
date['CPIuk']=(date['cpiu']/date['cpiu'].shift(12)-1)*100
date['ue']=date['CPIus']-date['be']
date['dgs1'] = fred.get_series('GS1')
date['exi']=date['dgs1']-date['RF']
date=date.dropna()

rates=pd.DataFrame()

rates['SONIA' ]= fred.get_series('IUDSOIA')
rates['EONIA' ]= fred.get_series('ECBESTRVOLWGTTRMDMNRT')
rates['ffunds'] = fred.get_series('DFF')


rates=rates.loc[dt.date(2021, 11, 1):]



lit=[]
for i in range(len(info['holdings'])):
    lit.append(info['holdings'][i]['symbol'])
    
litt=[]
for i in range(len(info['holdings'])):
    litt.append(info['holdings'][i]['holdingName'])
    
resultados=[]    
for i in range(len(info['holdings'])):
    
    capm=pd.DataFrame(date[[info['holdings'][i]['symbol'],'CPIus', 'SMB', 'HML', 'RF', 'Mkt-RF','oil', 'ue']])
    # capm=capm.loc[capm['CPIus']>2]
    print('CAPM'+' '+info['holdings'][i]['holdingName']) 
    Y=capm[info['holdings'][i]['symbol']]-capm['RF']
    X=capm[['Mkt-RF', 'CPIus', 'SMB', 'HML']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    capmean=((1+capm.mean()/100)**12)-1
    capmpar=results.params
    capmpv=results.pvalues
    recapm=date['dgs1'][-1]/100+capmpar[1]*capmean[2]
    resultados.append(list())
    resultados[i].append(results.rsquared_adj)
    for n in range(len(capmpar)):
        resultados[i].append(results.params[n])
        resultados[i].append(results.pvalues[n])
for i in range(len(resultados)):
    resultados[i]=[round(elem, 4) for elem in resultados[i]]



print('CAPM + Inflation')
Y=date['XLE']-date['RF']
X=date[['Mkt-RF', 'CPIus']]
X = sm.add_constant(X)
model = sm.OLS(Y,X)
results=model.fit(cov_type='HC1')
print(results.summary())

rr=pd.DataFrame(resultados, index=litt, columns=['Adj R-squared','Intercept', 'P>|z| Int',
                                                'B1(Mkt-RF)', 'P>|z| B1','B2(CPIus)','P>|z| B2','B3(SMB)', 'P>|z| B3','B4(HML)',
                                                'P>|z| B4'])
styler = rr.style
styler = styler.background_gradient()
htmlCodeWithStyle = styler.to_html()
file = open("pandas.html","w")
file.write(htmlCodeWithStyle)
file.close()


import lboro_graphs as lb

lb.linelb([date['ue'], date['be'], (date['cpi']/date['cpi'].shift(12)-1)*100, date['ue']+date['be']], 'linear', ['Unexpected Inflation', 'Breakeven Inflation', 'Consumer Price Index (US)', 'UI + BEI'], (6.4,4.8), False, 'Inflation Expectations in the US', 'In percentage points', 'Federal Reserve Bank of Saint Louis')   

closes=closes.dropna()
closess=closes.loc[dt.datetime(2022, 1, 1):]
closes=closes/closes.iloc[0]
closess=closess/closess.iloc[0]
lb.linelb([closes[lit[0]], closes[lit[1]], closes[lit[9]],closes['XLE'],closes[lit[3]], closes[lit[4]],
           closes[lit[5]],closes[lit[6]],closes[lit[7]],closes[lit[8]],closes[lit[2]]],
          'linear', [lit[0], lit[2], lit[9], 'XLE', lit[4], lit[5], lit[6],
                     lit[7], lit[8], lit[3]], (6.4,4.8), False, 'Inflation Expectations in the US', 'In percentage points', 'Federal Reserve Bank of Saint Louis')   

lb.linelb([closess[lit[0]], closess[lit[1]], closess[lit[9]],closess['XLE'],closess[lit[3]], closess[lit[4]],
           closess[lit[5]], closess[lit[6]], closess[lit[7]],closess[lit[8]],closess[lit[2]]],
          'linear', [lit[0], lit[2], lit[9], 'XLE', lit[4], lit[5], lit[6],
                     lit[7], lit[8], lit[3]], (6.4,4.8), False, 'Inflation Expectations in the US', 'In percentage points', 'Federal Reserve Bank of Saint Louis')   


uk= pd.DataFrame()
uk['ftse']=pd.DataFrame(yf.Ticker("^FTSE").history(period="2y", interval = "1d"))['Close']/pd.DataFrame(yf.Ticker("^FTSE").history(period="2y", interval = "1d"))['Close'].iloc[0]-1
uk['SPY']=pd.DataFrame(yf.Ticker("SPY").history(period="2y", interval = "1d"))['Close']/pd.DataFrame(yf.Ticker("SPY").history(period="2y", interval = "1d"))['Close'].iloc[0]-1
uk['XLE']=pd.DataFrame(yf.Ticker("XLE").history(period="2y", interval = "1d"))['Close']/pd.DataFrame(yf.Ticker("XLE").history(period="2y", interval = "1d"))['Close'].iloc[0]-1
uk[['XLE', 'SPY']].corr()

cp=pd.DataFrame()
cp['cpi']=fred.get_series('CPIAUCSL')
cp['CPIeu']=fred.get_series('EA19CPALTT01GYM')
cp['cpiu']=fred.get_series('GBRCPIALLMINMEI')
cp['CPIus']=(cp['cpi']/cp['cpi'].shift(12)-1)*100
cp['CPIuk']=(cp['cpiu']/cp['cpiu'].shift(12)-1)*100
cp=cp.loc[dt.date(2000, 1, 1):]


lb.linelb([cp['CPIus'],cp['CPIuk'],cp['CPIeu']], 'linear', ['CPI US', 'CPI UK', 'CPI EU'], (6.4,4.8), False, 'Inflation around the world', 'In percentage points', 'Federal Reserve Bank of Saint Louis')   
lb.linelb([rates['ffunds'],rates['SONIA'],rates['EONIA']], 'linear',['Federal Funds Rate (US): '+str(rates['ffunds'].iloc[-1]), 'Sterling Overnight interest (UK): '+str(rates['SONIA'].iloc[-1]), 'Euro Short Term Rate (EU): '+str(rates['EONIA'].iloc[-1])],(6.4,4.8), False, 'Interest rates of the main central banks', 'In percentage points', 'Federal Reserve Bank of Saint Louis')   


uktickr=['LAND.L', 'BLND.L', 'UTG.L', 'QQ.L', 'CHG.L', 'BA.L', 'SCT.L', 'AAF.L', 'BBOX.L']
for tickr in uktickr:
    uk[tickr]=(pd.DataFrame(yf.Ticker(tickr).history(period="2y", interval = "1d"))['Close']/pd.DataFrame(yf.Ticker(tickr).history(period="2y", interval = "1d"))['Close'].iloc[0]-1).dropna()
uk=uk.drop('2022-06-14 00:00:00')
for tickr in uktickr:
    lb.linelb([uk['ftse'], uk[tickr]], 'linear', ['FTSE 100', tickr], (6.4,4.8), False,tickr + ' change against FTSE 100', 'Measured in percentage points', 'Yahoo Finance API')

uktickr=['CVX', 'XOM']
for tickr in uktickr:
    uk[tickr]=(pd.DataFrame(yf.Ticker(tickr).history(period="2y", interval = "1d"))['Close']/pd.DataFrame(yf.Ticker(tickr).history(period="2y", interval = "1d"))['Close'].iloc[0]-1).dropna()
# uk=uk.drop('2022-06-14 00:00:00')
for tickr in uktickr:
    lb.linelb([uk['XLE'], uk[tickr],uk['SPY']], 'linear', ['XLE', tickr, 'SPY'], (6.4,4.8), False,tickr + ' change against XLE', 'Measured in percentage points', 'Yahoo Finance API')

