# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 18:01:25 2022

@author: diego
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:53:59 2022

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

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))

apikey='d60d2f087ecf05f94a3b9b3df34310a9'

def layoutovb():

    # g1='#003A65'
    g1='#1A9988'
    g2='#EB5600'
    g3='black'
    g4='yellow'
    g5='#717171'
    g6='#717171'
    g7='#717171'
    g8='#717171'
    g9='#717171'
    g10='#717171'
    g11='#717171'
    colors=[]
    colors=[g1,g2,g3,g4,g5,g6,g7,g8,g9, g10, g11]
    
    plt.style.use('seaborn-ticks')
    fig, ax = plt.subplots()  
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    plt.rcParams['figure.dpi'] = 300
    im = plt.imread('lborologo.JPG')



    return fig, ax, colors,im

def lineov(v, t, colors,ax):
        for i in range(len(v)):
            try:
                ax.plot(v[i], color=colors[i], label=t[i], linewidth=0.7, alpha=0.9)
            except: Exception
            pass
        # ax.legend(fancybox=True)    
        ax.legend()    
        plt.tight_layout()
        
def addt(fig,colors,title,subtitle,source,logo=True):
    # Make room below on top and bottom
    fig.subplots_adjust(top=0.825, bottom=0.15)
    c='black'
    # Add title
    fig.text(
        0.025, 0.92, title, 
        fontsize=16,
        fontweight="bold", 
        fontfamily="Sans Serif", color=c
    )
    # Add subtitle
    fig.text(
        0.0267, 0.875, subtitle, 
        fontsize=12, 
        fontfamily="Sans Serif", color=c
    )

    # Add caption
    fig.text(
        0.0253, 0.06, source, color='#717171', 
        fontsize=8, fontfamily="Sans Serif"
    )
    # Add authorship
    fig.text(
        0.025, 0.005, "Financial Trading. Group 12", color='#717171',fontweight="bold", 
        fontsize=16, fontfamily="Sans Serif"
    )

    # # Add line and rectangle on top.
    # fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color=colors[1], solid_capstyle="butt"))
    # fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color=colors[1]))
 
def addlogo(im,fig):
    newax = fig.add_axes([0.77,0.774,0.2,0.2], anchor='NE', zorder=1)
    newax.imshow(im)
    newax.axis('off')
    plt.show()
    
    
def linelb(v,l, t,size, dark, title, subtitle, source):
    fig, ax, colors,im=layoutovb()
    lineov(v, t, colors,ax)
    addt(fig, colors, title, subtitle, source, dark)
    # if s[0]==True:
    #     secax=sec_ax()
    # return secax
    addlogo(im, fig)
    # logg(l)
    # fig.tight_layout()
    fig



    