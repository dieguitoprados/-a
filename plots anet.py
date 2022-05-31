# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:16:48 2022

@author: diego
"""

#plotsanet

"""
Created on Mon May 30 14:33:31 2022

@author: diego
"""

"""PRICE RATIOS TTM TIMESERIES"""

import matplotlib.dates as mdates

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



import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)


apikey='d60d2f087ecf05f94a3b9b3df34310a9'

symbol=['ANET', 'CSCO']
anet=c.get_data(symbol, apikey)
anet.get_financials()
financials=anet.financials
anet.get_price()
price=anet.price

labels = financials[0][1][1].index
men_means = financials[0][1][1]['revenue']
women_means = financials[0][1][1]['netIncome']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots(figsize=(8,5))
rects1 = ax.bar(x - width/2, financials[0][1][1]['revenue']/1000000, width, label='Men')
rects2 = ax.bar(x + width/2, financials[0][1][1]['netIncome']/1000000, width, label='Women')
ax.bar_label(np.round(rects1,1), padding=3,size=8, weight='bold')
ax.bar_label(rects2, padding=3)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(x, labels)
ax.legend()



fig.tight_layout()

plt.show()



