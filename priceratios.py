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

av=fmp.available_indexes(apikey)
indexes=pd.DataFrame(f.clean_financials(fmp.historical_price_full(apikey, '^TYX'))['close'])
for i in range(1,len(av)):
    indexes[av[i]['symbol']]=f.clean_financials(fmp.historical_price_full(apikey, av[i]['symbol']))['close']

indma20=indexes.rolling(window=100).mean()
indma50=indexes.rolling(window=50).mean()
indma100=indexes.rolling(window=100).mean()


fmp.financial_ratios(apikey, symbol[0])
ttmfin=financials[0][1][1]+financials[0][1][1].shift(1)+financials[0][1][1].shift(2)+financials[0][1][1].shift(3)
ttm=ttmfin.dropna()
ttmday=ttm.reindex(price[0][1].index,method='ffill').dropna()
pe=pd.DataFrame()
pe['pe']=(price[0][1]['close']/ttmday['eps']).dropna()
pe['ps']=(price[0][1]['close']/(ttmday['revenue']/320000000)).dropna()
pe['peg25']=((price[0][1]['close']/ttmday['eps'])/25).dropna()
pe['peg30']=((price[0][1]['close']/ttmday['eps'])/30).dropna()
pe['peg35']=((price[0][1]['close']/ttmday['eps'])/35).dropna()
pe['peg40']=((price[0][1]['close']/ttmday['eps'])/40).dropna()
r=fmp.historical_rating(apikey, symbol[0])
rr=fmp.rating(apikey, symbol[0])
s=fmp.earnings_surprises(apikey, symbol[0])
##LIQUIDITY

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
ax.plot(pe['peg25'], color='lime', label='peg25', linewidth=.5, alpha=0.8)
ax.plot(pe['peg30'], color='limegreen', label='peg30', linewidth=.5, alpha=0.8)
ax.plot(pe['peg35'], color='darkgreen', label='peg35', linewidth=.5, alpha=0.8)
ax.plot(pe['peg40'], color='black', label='peg40', linewidth=.5, alpha=0.8)
# ax2=ax.twinx()

# ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
# ax2.plot(indexes['^VIX'], color='black', label='PE ratio', linewidth=1, alpha=0.5)
# ax2.plot(price[0][1]['close'], color='forestgreen', label='Price', linewidth=1, alpha=0.8)
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
# ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      # ncol=2, mode="expand", borderaxespad=0.)
ax.yaxis.grid(True, color='palegreen', alpha=0.3)
# ax2.yaxis.grid(True, color='forestgreen', alpha=0.3)
ax.xaxis.grid(True, color='palegreen', alpha=0.3)

# ax.xaxis.set_major_formatter(
#     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
ax.set_facecolor("white")
ax.set_xlabel(symbol[0]+' Price Ratios TTM',  color='seagreen',
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
plt.savefig(symbol[0]+'_price_ratios_'+str(dt.date.today()),dpi=600)









plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
plt.plot(financials[1][2][3].index,financials[1][2][3]['returnOnAssets'], label='ROA',marker='o', markersize=4, color='limegreen')
plt.plot(financials[1][2][3].index,financials[1][2][3]['returnOnEquity'],label='ROE',marker='o', markersize=4, color='forestgreen')
plt.plot(financials[1][2][3].index,financials[1][2][3]['returnOnCapitalEmployed'],label='ROCE',marker='o', markersize=4, color='seagreen')
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
plt.xticks(rotation = 80)
ax.yaxis.grid(True, color='palegreen', alpha=0.3)


ax.set_facecolor("white")
ax.set_xlabel(plt.legend())
ax.set_xlabel(symbol[1]+' Profitability Ratios TTM',  color='seagreen',
              weight='bold')

ax.text(
        0.75,
        0.02,
        'Greenfield Capital: Diego Prados',
        horizontalalignment='center',
        verticalalignment='top',
        transform=ax.transAxes)
fig.tight_layout()
plt.savefig(symbol[1]+'_profit_ratios_'+str(dt.date.today()),dpi=600)


