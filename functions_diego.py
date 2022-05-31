# -*- coding: utf-8 -*-
"""
Created on Wed May  4 01:28:33 2022

@author: diegu
"""

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



    
