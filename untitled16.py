
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

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))

apikey='d60d2f087ecf05f94a3b9b3df34310a9'

def linee(v, t, title, subtitle, source):
    # g1='#003A65'
    g1='white'
    g2='#00B7E5'
    g3='#006666'
    g4='#8BBF18'
    g5='#CC0066'
    g6='#FFCC33'
    g7='lightgrey'
    g8='gainsboro'
    colors=[]
    colors=[g1,g2,g3,g4,g5,g6,g7,g8]
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots()  
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    im = plt.imread('ovbb.png')
    
    
    
    
    for i in range(len(v)):
        try:
            ax.plot(v[i], color=colors[i], label=t[i], linewidth=0.7, alpha=0.9)
        except: Exception
        pass
    # ax.legend(fancybox=True)    
    plt.tight_layout()
            
    # Make room below on top and bottom
    fig.subplots_adjust(top=0.825, bottom=0.15)
    c='white'
    # Add title
    fig.text(
        0, 0.92, title, 
        fontsize=15,
        fontweight="bold", 
        fontfamily="Sans Serif", color=c
    )
    # Add subtitle
    fig.text(
        0, 0.875, subtitle, 
        fontsize=12, 
        fontfamily="Sans Serif", color=c
    )
    
    # Add caption
    fig.text(
        0, 0.06, source, color='lightgrey', 
        fontsize=8, fontfamily="Sans Serif"
    )
    # Add authorship
    fig.text(
        0, 0.005, "Diego Prados. OVB Madrid 7", color='lightgrey',
        fontsize=16, fontfamily="Sans Serif"
    )
    
        # # Add line and rectangle on top.
        # fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color=colors[1], solid_capstyle="butt"))
        # fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color=colors[1]))
     
    newax = fig.add_axes([0.8,0.8,0.2,0.2], anchor='NE', zorder=1)
    newax.imshow(im)
    newax.axis('off')
    fig.patch.set_facecolor('#003A65')
    ax.set_facecolor('#003A65')
    plt.rcParams['figure.dpi'] = 300
    plt.show()
    
    



    