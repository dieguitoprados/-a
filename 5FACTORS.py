# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 00:28:13 2022

@author: diego
"""


import time
import statsmodels.api as sm
import datetime as dt
import streamlit as st
import yfinance as yf
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
from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')





di = 'C:\\Users\\diego\\Downloads\\fu.CSV' # hardcoded
data = pd.read_csv(di)
date=data.iloc[:709]
date=date.iloc[580:]
date.index=pd.to_datetime(date['Date'], format='%Y%m')
date.index=date.index.date
date=date.drop('Date', axis=1)
date=date.loc[dt.date(2014, 1, 1):]

directory = 'C:\\Users\\diego\\Downloads\\EQIX.CSV' # hardcoded
fna = 'C:\\Users\\diego\\Downloads\\^FNAR.CSV' # hardcoded
fne= 'C:\\Users\\diego\\Downloads\\^FNER.CSV' # hardcoded
dlr= 'C:\\Users\\diego\\Downloads\\DLR.CSV' # hardcoded
eur = 'C:\\Users\\diego\\Downloads\\EURUSD=X.CSV' # hardcoded

eur= pd.read_csv(eur)
eur.index=pd.to_datetime(eur['Date'])
eur=100*(eur['Close']/eur['Close'].shift(1)-1)

dlr= pd.read_csv(dlr)
dlr.index=pd.to_datetime(dlr['Date'])
dlr=100*(dlr['Close']/dlr['Close'].shift(1)-1)

eq= pd.read_csv(directory)
eq.index=pd.to_datetime(eq['Date'])
eq=100*(eq['Close']/eq['Close'].shift(1)-1)

fnar= pd.read_csv(fna)
fnar.index=pd.to_datetime(fnar['Date'])
fnar=100*(fnar['Close']/fnar['Close'].shift(1)-1)

fner= pd.read_csv(fne)
fner.index=pd.to_datetime(fner['Date'])
fner=100*(fner['Close']/fner['Close'].shift(1)-1)


date['eqix']=eq
date['dlr']=dlr
date['eur']=eur
date['fner']=fner
date['fnar']=fnar
date['fne']=date['fner']-date['RF']
date['fna']=date['fnar']-date['RF']
date['aaa'] = fred.get_series('AAA')
date['baa' ]= fred.get_series('BAA')
date['kwh' ]= (fred.get_series('CUSR0000SEHF01')/fred.get_series('CUSR0000SEHF01').shift(12)-1)*100
date['construction' ]= (fred.get_series('TTLCONS')/fred.get_series('TTLCONS').shift(12)-1)*100
date['gas' ]= (fred.get_series('MHHNGSP')/fred.get_series('MHHNGSP').shift(12)-1)
date['spread']=date['baa']-date['aaa']
date['be']=fred.get_series('T5YIEM')
# date['30mortg']=pd.DataFrame(fred.get_series('MORTGAGE30US')).reindex('monthly', method='ffill')
date['cpi']=fred.get_series('CPIAUCSL')/fred.get_series('CPIAUCSL').shift(12)-1
date['ip']=fred.get_series('INDPRO')/fred.get_series('INDPRO').shift(12)-1
date['ue']=date['be']-date['cpi']
date['dgs1'] = fred.get_series('GS1')
date['exi']=date['dgs1']-date['RF']
date=date.dropna()

resultados=[]
for nam in ['fner','dlr','fnar', 'eqix']:
# nam='eqix'

    
    capm=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'gas', 'fna', 'fne', 'RMW', 'CMA']])
    print('CAPM '+nam) 
    Y=capm[nam]-capm['RF']
    X=capm['Mkt-RF']
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('CAPM '+nam+ '\n'+str(results.summary()))
    capmean=((1+capm.mean()/100)**12)-1
    print(capmean)
    capmvar=capm.var()
    capmpar=results.params
    recapm=date['dgs1'][-1]/100+capmpar[1]*capmean[2]#+capmpar[2]*capmean[3]
    rese=np.sqrt(np.sum(results.resid**2)/results.df_resid)
    
    ffm=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML','fna', 'fne', 'RMW', 'CMA']])
    print('FAMA-FRENCH Model '+nam)
    Y=ffm[nam]-ffm['RF']
    X=ffm[['Mkt-RF', 'SMB', 'HML','RMW', 'CMA']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('FAMA-FRENCH Model '+nam+ '\n'+str(results.summary()))
    ffmean=((1+ffm.mean()/100)**12)-1
    print(ffmean)
    ffmvar=(ffm/100).var()
    ffmpar=results.params
    reffm=date['dgs1'][-1]/100+ffmpar[1]*ffmean[2]+ffmpar[2]*ffmean[3]+ffmpar[3]*ffmean[4]
    print(ffmvar[2]*ffmean[2]**2+ffmvar[3]*ffmean[3]**2+ffmvar[4]*ffmean[4]**2+(3.295857)*2+(0.843252)*2+(0.324659)*2)
    rese=np.sqrt(np.sum(results.resid**2)/results.df_resid)
    
    apmw=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML', 'spread', 'fna', 'fne', 'RMW', 'CMA']])
    print('Arbitrage Pricing Model without inflation')
    Y=apmw[nam]-apmw['RF']
    X=apmw[['Mkt-RF', 'SMB', 'HML', 'spread', 'CMA']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('Arbitrage Pricing Model without inflation '+nam+ '\n'+str(results.summary()))
    apmwmean=((1+apmw.mean()/100)**12)-1
    apmwpar=results.params
    reapmw=date['dgs1'][-1]/100+apmwpar[1]*apmwmean[2]+apmwpar[2]*apmwmean[3]+apmwpar[3]*apmwmean[4]+apmwpar[4]*apmw['spread'].mean()/100
    
    
    apmexi=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML','spread', 'exi','RMW', 'CMA']])
    print('Arbitrage Pricing Model with 1y-1m')
    Y=apmexi[nam]-apmexi['RF']
    X=apmexi[['Mkt-RF', 'SMB', 'HML', 'spread', 'exi', 'RMW', 'CMA']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    a=results.params
    print(results.summary())
    resultados.append('Arbitrage Pricing Model with 1y-1m '+nam+ '\n'+str(results.summary()))
    apmeximean=((1+apmexi.mean()/100)**12)-1
    apmexipar=results.params
    reapmexi=date['dgs1'][-1]/100+apmexipar[1]*apmeximean[2]+apmexipar[2]*apmeximean[3]+apmexipar[3]*apmeximean[4]+apmexipar[4]*apmexi['spread'].mean()/100+apmexipar[5]*apmexi['exi'].mean()/100
    
    
    apmbe=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML','spread', 'ue', 'fna', 'fne','RMW', 'CMA']]).dropna()
    print('Arbitrage Pricing Model with breakeven 5yr')
    Y=apmbe[nam]-apmbe['RF']
    X=apmbe[['Mkt-RF', 'SMB', 'HML', 'spread', 'ue','RMW', 'CMA']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('Arbitrage Pricing Model with breakeven 5yr '+nam+ '\n'+str(results.summary()))
    apmbemean=((1+apmbe.mean()/100)**12)-1
    apmbepar=results.params
    reapmbe=date['dgs1'][-1]/100+apmexipar[1]*apmeximean[2]+apmexipar[2]*apmeximean[3]+apmexipar[3]*apmeximean[4]+apmexipar[4]*apmbe['spread'].mean()/100+apmexipar[5]*apmbe['ue'].mean()/100
    
print(results.get_prediction)
eqix = yf.Ticker("EQIX")

div=eqix.dividends
divi=f.ttm(div)
div=div.groupby(div.index.year).sum()
div = div.loc[2017:]
div=div.replace(9.3, 12.4)
divgr=div/div.shift(1)-1
divigr=divi/divi.shift(1)-1
divigr36ttm=((1+divigr.tail(12).mean())**4)-1
mdivgr=divgr.mean()
div5cagr=((1+(div.loc[2022]/div.loc[2017]-1))**(1/5))-1

eqixprice=631.16
regordoncagr=(div.loc[2022]*(1+div5cagr)/eqixprice)+div5cagr
regordonttm=(div.loc[2022]*(1+divigr36ttm)/eqixprice)+divigr36ttm  
regordon=(div.loc[2022]*(1+mdivgr)/eqixprice)+mdivgr

growthapmw=(eqixprice*reapmw-div.loc[2022])/(div.loc[2022]+eqixprice)
growthcapm=(eqixprice*recapm-div.loc[2022])/(div.loc[2022]+eqixprice)
growthffm=(eqixprice*reffm-div.loc[2022])/(div.loc[2022]+eqixprice)
growthapmexi=(eqixprice*reapmexi-div.loc[2022])/(div.loc[2022]+eqixprice)
growthapmbe=(eqixprice*reapmbe-div.loc[2022])/(div.loc[2022]+eqixprice)

print('recapm: '+str(recapm))
print('reffm: '+str(reffm))
print('reapmw: '+str(reapmw))
print('reapmexi: '+str(reapmexi))
print('reapmbe: '+str(reapmbe))
remodels=[recapm, reffm, reapmw, reapmbe, reapmexi, regordoncagr, regordonttm]
price=[]
for name in remodels:
    # price.append((12.17*(1+div5cagr))/(name-div5cagr))
    price.append((div.loc[2022]*(1+divigr36ttm))/(name-divigr36ttm))

# capmpr=price[0:2]
# ffmpr=price[2:4]
# apmwpr=price[4:6]
# apmbepr=price[6:8]
# apmexipr=price[8:10]
# gordoncagrpr=price[10:12]
# gordonttmpr=price[12:14]


# api='pk_ae18fb28cc04485e89fee37dc4ba95e0'

# from iexfinance.stocks import Stock

# a = Stock("AAPL", token=api)
# a.get_quote()

capmpr=price[0]
ffmpr=price[1]
apmwpr=price[2]
apmbepr=price[3]
apmexipr=price[4]
gordoncagrpr=price[5]
gordonttmpr=price[6]

print('capm: '+str(capmpr))
print('ffm: '+str(ffmpr))
print('apmw: '+str(apmwpr))
print('apmbe: '+str(apmbepr))
print('apmexi: '+str(apmexipr))
print('gordoncagr: '+str(gordoncagrpr))
print('gordonttm: '+str(gordonttmpr))

spr=pd.DataFrame()

spr['aaa'] = fred.get_series('AAA')
spr['baa' ]= fred.get_series('BAA')
spr['spread']=spr['baa']-spr['aaa']

spr['cpi']=fred.get_series('CPIAUCSL')/fred.get_series('CPIAUCSL').shift(12)-1


p.linep([spr['spread'], spr['aaa'], spr['baa'],spr['cpi']*100], 'linear', ['spread', 'aaa', 'bbb', 'cpi'], 10, False, 'Spread and bonds', '', '')
spr.corr()


#multiples valuation
shares=91000000
pepr=7.02*31.71
pffopr=(1745900000/shares)*14.74
pspr=72.48*5.26
evebitdapr=(2461100000/shares)*18.51

for pp in [pepr, pffopr, pspr, evebitdapr]:
    print(str(pp/eqixprice-1))
    print(str(eqixprice/pp-1))
gt=[]
for i in range(1,5):  
    gt.append(divigr36ttm-(divigr36ttm-0.045)*(i/5))

stg=[]
for name in remodels:
    stg.append((div.loc[2022]*(1+divigr36ttm))/(1+name)+(div.loc[2022]*((1+divigr36ttm)**2))/((1+name)**2)+(div.loc[2022]*((1+divigr36ttm)**3))/((1+name)**3)+
               (div.loc[2022]*(((1+divigr36ttm)**3)*(1+gt[0])))/((1+name)**4)+(div.loc[2022]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])))/((1+name)**5)+(div.loc[2022]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])*(1+gt[2])))/((1+name)**6)+(div.loc[2022]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])*(1+gt[2])*(1+gt[3])))/((1+name)**7)+
               (div.loc[2022]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])*(1+gt[2])*(1+gt[3])*(1+0.045)))/(((1+name)**7)*(name-0.045)))

