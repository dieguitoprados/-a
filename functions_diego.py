# -*- coding: utf-8 -*-
"""
Created on Wed May  4 01:28:33 2022

@author: diegu
"""
import matplotlib.pylab as pl
import datetime as dt
import statsmodels.api as sm
import pandas_datareader.data as reader

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import fmpsdk as fmp
import importlib
import datetime as dt
import matplotlib.pyplot as plt
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as scipy
import matplotlib.ticker as mtick
from sec_cik_mapper import StockMapper



from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')
apikey='d60d2f087ecf05f94a3b9b3df34310a9'



apikey='d60d2f087ecf05f94a3b9b3df34310a9'

# CLEANING FUNCTIONS 

def clean_financials(df):
    
    df=pd.DataFrame(df)
    try:
        df['fillingDate']=pd.to_datetime(df['fillingDate'])
    except:
        df['end']=pd.to_datetime(df['date'])
    try:
        df=df.set_index('fillingDate')
    except:
        df=df.set_index('end')
    df=df.select_dtypes(exclude=['object'])
    df=df.sort_index(ascending=True)
    return df

def ttm(df):
    df=df+df.shift(1)+df.shift(2)+df.shift(3)
    df=df.dropna()
    
    return df

def normalize(series):
    series=100*(series/series.iloc[0]-1)
    return series

def cagr(start, end, periods):
    return(end/start)**(1/periods)-1

def cik(tikr):
    mapper = StockMapper()
    ma=mapper.ticker_to_cik
    return ma[tikr]

def tickr(cik):
    mapper = StockMapper()
    ma=mapper.cik_to_tickers
    return ma[cik]

def load_factors(start):
    factors=reader.DataReader('F-F_Research_Data_Factors', 'famafrench', start, dt.date.today())[0]
    factors.index=pd.date_range(start=start, periods=len(factors), freq='M')
    factors.index=pd.to_datetime(factors.index, format='%Y%m')
    end=factors.index[-1]
    return factors, end


def cleanfinttm(df, name):
    
    df=df['facts']['us-gaap'][name]['units']
    for lot in ['Store','USD', 'USD/shares', 'Year', ('pure','Year'), 'pure', 'shares']:
        try:
            df=pd.DataFrame(df[lot])
        except Exception:
            pass
    df['ts']=pd.to_datetime(df['end'])-pd.to_datetime(df['start'])
    dff=df.loc[df['ts']<pd.to_timedelta("100day")]
    dff=dff.drop_duplicates('end')

    dff=ttm(dff)
    dff=dff.append(df.loc[df['ts']>pd.to_timedelta("300day")])
    dff=dff.sort_values('end')
    dff.set_index(pd.to_datetime(df['end']))
    
    dff=dff.sort_index(ascending=True)
    
    return dff
def cleanfinanual(df, name):
    
    df=df['facts']['us-gaap'][name]['units']
    for lot in ['Store','USD', 'USD/shares', 'Year', ('pure','Year'), 'pure', 'shares']:
        try:
            df=pd.DataFrame(df[lot])
        except Exception:
            pass
    df['ts']=pd.to_datetime(df['end'])-pd.to_datetime(df['start'])
    dff=pd.DataFrame()
    dff=dff.append(df.loc[df['ts']>pd.to_timedelta("300day")])
    dff=dff.drop_duplicates('end')

    dff=dff.set_index(pd.to_datetime(dff['end']))
    
    dff=dff.sort_index(ascending=True)
    
    return dff
def clean(df, name):
    
    df=df['facts']['us-gaap'][name]['units']
    for lot in ['Store','USD', 'USD/shares', 'Year', ('pure','Year'), 'pure', 'shares']:
        try:
            df=pd.DataFrame(df[lot])
        except Exception:
            pass
    df=df.set_index(pd.to_datetime(df['end']))

    dff=pd.DataFrame()
    dff=dff.append(df.loc[df['form']=="10-K"])
    dff=dff.drop_duplicates('end')
    
    df=df.sort_index(ascending=True)
    
    return dff

    



def re(tickr):
    eqix = yf.Ticker(tickr)
    ng = eqix.history(period="max", interval = "1mo").dropna()
    ng=100*(ng['Close']/ng['Close'].shift(1)-1)
    di = 'C:\\Users\\diego\\Downloads\\fuck.CSV' # hardcoded
    data = pd.read_csv(di)
    date=data.iloc[:1152]
    date=date.iloc[880:]
    date.index=pd.to_datetime(date['Date'], format='%Y%m')
    date.index=date.index.date
    date=date.drop('Date', axis=1)
    date=date.loc[dt.date(2014, 1, 1):]
    date[tickr]=ng
    resultados=[]
    date['aaa'] = fred.get_series('AAA')
    date['baa' ]= fred.get_series('BAA')
    date['spread']=date['baa']-date['aaa']
    date['dgs1'] = fred.get_series('GS1')
    
    capm=pd.DataFrame(date[[tickr, 'RF', 'Mkt-RF']])
    print('CAPM '+tickr) 
    Y=capm[tickr]-capm['RF']
    X=capm[['Mkt-RF']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('CAPM '+tickr+ '\n'+str(results.summary()))
    capmean=((1+capm.mean()/100)**12)-1
    print(capmean)
    capmpar=results.params
    recapm=date['dgs1'][-1]/100+capmpar[1]*capmean[2]#+capmpar[2]*capmean[3]
    rese=np.sqrt(np.sum(results.resid**2)/results.df_resid)
    
    ffm=pd.DataFrame(date[[tickr, 'RF', 'Mkt-RF', 'SMB', 'HML']])
    print('FAMA-FRENCH Model '+tickr)
    Y=ffm[tickr]-ffm['RF']
    X=ffm[['Mkt-RF', 'SMB', 'HML']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('FAMA-FRENCH Model '+tickr+ '\n'+str(results.summary()))
    ffmean=((1+ffm.mean()/100)**12)-1
    print(ffmean)
    ffmvar=(ffm/100).var()
    ffmpar=results.params
    reffm=date['dgs1'][-1]/100+ffmpar[1]*ffmean[2]+ffmpar[2]*ffmean[3]+ffmpar[3]*ffmean[4]
    print(ffmvar[2]*ffmean[2]**2+ffmvar[3]*ffmean[3]**2+ffmvar[4]*ffmean[4]**2+(3.295857)*2+(0.843252)*2+(0.324659)*2)
    
    apmw=pd.DataFrame(date[[tickr, 'RF', 'Mkt-RF', 'SMB', 'HML', 'spread']])
    print('Arbitrage Pricing Model without inflation')
    Y=apmw[tickr]-apmw['RF']
    X=apmw[['Mkt-RF', 'SMB', 'HML', 'spread']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('Arbitrage Pricing Model without inflation '+tickr+ '\n'+str(results.summary()))
    apmwmean=((1+apmw.mean()/100)**12)-1
    apmwpar=results.params
    reapmw=date['dgs1'][-1]/100+apmwpar[1]*apmwmean[2]+apmwpar[2]*apmwmean[3]+apmwpar[3]*apmwmean[4]+apmwpar[4]*apmw['spread'].mean()/100
    re=[recapm, reffm, reapmw]

    return resultados, re










def recdays():
    recdays=pd.DataFrame(fred.get_series('JHDUSRGDPBR'), columns=['recdays'])
    dates = pd.date_range(recdays.index[0], recdays.index[-1], freq='D')
    dates.name = 'date'
    dates=dates.date
    recdays = recdays.reindex(dates, method='bfill')
    df2 = recdays.mask((recdays['recdays'] == 0) & ((recdays['recdays'].shift(1) == 0) | (recdays['recdays'].shift(-1) == 0)))
    df2['group'] = (df2['recdays'].shift(1).isnull() & df2['recdays'].notnull()).cumsum()
    df2=df2[df2['recdays'].notnull()].groupby('group')
    recs=[]
    for name, group in df2:
        recs.append(df2.get_group(name))

    for name , group in df2:
        recs.append(str(df2.get_group(name).index[0])+'---'+str(df2.get_group(name).index[-1]))


    return recs

