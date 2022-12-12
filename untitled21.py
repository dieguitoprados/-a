# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:51:32 2022

@author: diegu
"""

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

av=fmp.available_indexes(apikey)

symbol=[ '^IXIC', '^VXN', '^GSPC','^VIX', '^RUT','^RVX' ]

symbol=['AMZN', 'AAPL', 'NFLX', 'ANET', 'CSCO', 'JNPR']

ind=c.get_data(symbol, apikey)



ind.get_price()
price=ind.price


# for i in range(0, len())

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
ax.plot(price[0][2]['close'], color='green', label=price[0][0], linewidth=1, alpha=0.8)
ax2=ax.twinx()
ax2.plot(price[1][2]['close'], color='blue', label=price[1][0], linewidth=1, alpha=0.8)

# ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
# ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
# ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
ax.yaxis.grid(True, color='palegreen', alpha=0.3)
ax2.yaxis.grid(True, color='blue', alpha=0.3)
ax.xaxis.grid(True, color='palegreen', alpha=0.3)

# ax.xaxis.set_major_formatter(
#     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
ax.set_facecolor("white")
ax.set_xlabel(symbol[0]+' Price chart',  color='seagreen',
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


plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
ax.plot(price[2][2]['close'], color='green', label=price[2][0], linewidth=1, alpha=0.8)
ax2=ax.twinx()
ax2.plot(price[3][2]['close'], color='blue', label=price[3][0], linewidth=1, alpha=0.8)

# ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
# ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
# ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
ax.yaxis.grid(True, color='palegreen', alpha=0.3)
ax2.yaxis.grid(True, color='blue', alpha=0.3)
ax.xaxis.grid(True, color='palegreen', alpha=0.3)

# ax.xaxis.set_major_formatter(
#     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
ax.set_facecolor("white")
ax.set_xlabel(symbol[2]+' Price chart',  color='seagreen',
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



plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
ax.plot(price[1][2]['close'], color='limegreen', label=price[1][0], linewidth=1, alpha=0.8)
ax.plot(price[3][2]['close'], color='green', label=price[3][0], linewidth=1, alpha=0.8)
ax.plot(price[5][2]['close'], color='forestgreen', label=price[5][0], linewidth=1, alpha=0.8)
# ax2=ax.twinx()
# ax2.plot(price[3][2]['close'], color='blue', label=price[3][0], linewidth=1, alpha=0.8)

# ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
# ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
# ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
ax.yaxis.grid(True, color='palegreen', alpha=0.3)
# ax2.yaxis.grid(True, color='blue', alpha=0.3)
ax.xaxis.grid(True, color='palegreen', alpha=0.3)

# ax.xaxis.set_major_formatter(
#     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
ax.set_facecolor("white")
ax.set_xlabel('Volatility chart intraday',  color='seagreen',
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


for i in range(0, len(symbol)):

    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()  
    ax.plot(price[i][1]['close'], color='limegreen', label=price[i][0], linewidth=1, alpha=0.8)
    # ax.plot(price[3][1]['close'], color='green', label=price[3][0], linewidth=1, alpha=0.8)
    # ax.plot(price[5][1]['close'], color='forestgreen', label=price[5][0], linewidth=1, alpha=0.8)
    # ax2=ax.twinx()
    # ax2.plot(price[3][2]['close'], color='blue', label=price[3][0], linewidth=1, alpha=0.8)
    
    # ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
    # ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
    # ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                          ncol=2, mode="expand", borderaxespad=0.)
    ax.yaxis.grid(True, color='palegreen', alpha=0.3)
    # ax2.yaxis.grid(True, color='blue', alpha=0.3)
    ax.xaxis.grid(True, color='palegreen', alpha=0.3)
    
    # ax.xaxis.set_major_formatter(
    #     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.set_facecolor("white")
    ax.set_xlabel(price[i][0],  color='seagreen',
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



coin=f.clean_financials(fmp.income_statement(apikey, 'COIN', 'quarter'))
coin=f.clean_financials(fmp.financial_ratios(apikey, 'COIN', 'quarter'))






p=fmp.h











