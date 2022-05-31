# -*- coding: utf-8 -*-
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
fmp.financial_ratios_ttm(apikey, symbol[0])

anet=c.get_data(symbol, apikey)
anet.get_financials()
financials=anet.financials
anet.get_price()
price=anet.price



fmp.financial_ratios(apikey, symbol[0])
ttmfin=financials[0][1][1]+financials[0][1][1].shift(1)+financials[0][1][1].shift(2)+financials[0][1][1].shift(3)
ttm=ttmfin.dropna()
ttmday=ttm.reindex(price[0][1].index,method='ffill').dropna()
pe=(price[0][1]['close']/ttmday['eps']).dropna()
r=fmp.historical_rating(apikey, symbol[0])
rr=fmp.rating(apikey, symbol[0])
fmp.earnings_surprises(apikey, symbol[0])
##LIQUIDITY

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
ax.plot(price[0][1], color='green', label='Price', linewidth=1, alpha=0.8)
ax.plot(pe, color='forestgreen', label='PE ratio', linewidth=2, alpha=0.8)
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
ax.yaxis.grid(True, color='palegreen', alpha=0.3)
ax.xaxis.grid(True, color='palegreen', alpha=0.3)

# ax.xaxis.set_major_formatter(
#     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
ax.set_facecolor("white")
ax.set_xlabel(symbol[0]+' PE Ratio TTM',  color='seagreen',
              weight='bold')
# ax.legend()
ax.text(
        0.75,
        0.1,
        'Greenfield Capital Advisors Group S.L.',
        horizontalalignment='center',
        verticalalignment='top',
        transform=ax.transAxes)
fig.tight_layout()

