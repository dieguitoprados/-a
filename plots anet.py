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

for i in range (0, len(symbol)):


    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.tick_params(bottom=False, left=False)
    # ax.set_axisbelow(True)
    # ax.yaxis.grid(False)
    # ax.xaxis.grid(False)


    # Plot
    #     Plot histogram
    mean = np.mean(price[0][1]['changePercent'])
    std = np.std(price[0][1]['changePercent'])
    skewness= skew(price[0][1]['changePercent'])
    kurt = kurtosis(price[0][1]['changePercent']) # excess kurtosis
    per_05,per_25,per_75,per_95 = np.percentile(price[0][1]['changePercent'],5),np.percentile(price[0][1]['changePercent'],25),np.percentile(price[0][1]['changePercent'],75),np.percentile(price[0][1]['changePercent'],95)
    median = np.median(price[0][1]['changePercent'])
    nb_decimals=3
    plot_str = symbol[0]+'  Histogram of Returns' + '\n'\
        +'mean ' + str(np.round(mean,nb_decimals))\
        + ' | std dev ' + str(np.round(std,nb_decimals))\
        + ' | skewness ' + str(np.round(skewness,nb_decimals))\
        + ' | kurtosis ' + str(np.round(kurt,nb_decimals)) + '\n'\
        + 'p05% ' + str(np.round(per_05,nb_decimals))\
        + ' | p20% ' + str(np.round(per_25,nb_decimals))\
        + ' | median ' + str(np.round(median,nb_decimals))\
        + ' | p80% ' + str(np.round(per_75,nb_decimals))\
        + ' | p95% ' + str(np.round(per_95,nb_decimals))
    fig, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')        
    cm = plt.cm.get_cmap('YlGn')
    n, bins, patches = plt.hist(price[0][1]['changePercent'], bins=90, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7, density=True)
    
    n = n.astype('int') # it MUST be integer
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # scale values to interval [0,1]
    col = bin_centers - min(bin_centers)
    col /= max(col)
    
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    ax.plot()
    x=np.linspace(mean - 3*std, mean + 3*std, 100)
    plt.plot(x,norm.pdf(x, mean, std),linestyle = ":", alpha=0.75,color='darkgreen')
    plt.xlabel(plot_str, color='forestgreen',weight='bold')
        # Quantile lines
    
    # X
        # Limit x range to 0-4
    
    # Y
    # ax.set_ylim(0, 1)
    # ax.set_yticklabels([])
    # ax.set_ylabel("")
    
    # Annotations
    # ax.text(per_05,0.3, "5%", size = 10, alpha = 0.8)
    ax.axvline(per_05,0,0.32, linestyle = ":", alpha=0.75,color='limegreen')
    # ax.text(per_25, 0.75, "25%", size = 10, alpha = 0.8)
    ax.axvline(per_25,0,0.46, linestyle = ":", alpha=0.75,color='forestgreen')
    # ax.text(median,0.85, "50%", size = 12, alpha = 0.8)
    ax.axvline(median,0,0.54, linestyle = ":", alpha=0.75,color='forestgreen')
    # ax.text(mean,0.85, "Avg.", size = 12, alpha = 0.8)
    ax.axvline(mean,0,0.54, linestyle = ":", alpha=0.75,color='forestgreen')
    # ax.text(per_75,0.2, "75%", size = 10, alpha = 0.8)
    ax.axvline(per_75,0,0.46, linestyle = ":", alpha=0.75,color='forestgreen')
    # ax.text(per_95,0.65, "95%", size = 10, alpha =.8)
    ax.axvline(per_95,0,0.32, linestyle = ":", alpha=0.75,color='limegreen')
    
    # Overall
    ax.set_facecolor("white")

    ax.text(0.2, 0.2,
            'Greenfield Capital Advisors Group S.L.',
            horizontalalignment='center',
            verticalalignment='top', size=28, alpha=0.5, color='green')

    plt.show() 


