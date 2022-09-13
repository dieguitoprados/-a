# -*- coding: utf-8 -*-
"""
Created on Wed May  4 01:28:33 2022

@author: diegu
"""
import matplotlib.pylab as pl
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
import matplotlib.ticker as mtick



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
        df['date']=pd.to_datetime(df['date'])
    try:
        df=df.set_index('fillingDate')
    except:
        df=df.set_index('date')
    df=df.select_dtypes(exclude=['object'])
    df=df.sort_index(ascending=True)
    return df

def ttm(df):
    df=df+df.shift(1)+df.shift(2)+df.shift(3)
    df=df.dropna()
    
    return df
def ttmday(df):
    df=df+df.shift(1)+df.shift(2)+df.shift(3)
    df=df.dropna()
    return df

def price_ratios(ttm, price):
    
    ttm
    
def normalize(series):
    series=100*(series/series.iloc[0]-1)
    return series

def cagr(start, end, periods):
    return(end/start)**(1/periods)-1
















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

