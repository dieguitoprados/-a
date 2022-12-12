# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:41:04 2022

@author: diego
"""

import time
import statsmodels.api as sm
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
from scipy.stats import skew, kurtosis, chi2, linregress
import seaborn as sns
from itertools import combinations
import matplotlib.pylab as pl
import matplotlib


s=time.time()
import functions_diego as f
importlib.reload(f)
import plots as p
importlib.reload(p)

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
apikey='d60d2f087ecf05f94a3b9b3df34310a9'



symbol=['EQIX', 'DLR', 'NTTYY', 'KDDIY']

anet=c.get_data(apikey)

anet.get_price(symbol)
price=anet.price

anet.get_financials(symbol)
financials=anet.financials

e=p.eod_data(apikey, fredapikey)



    
p.linep([f.normalize(price[0][1]['close']),f.normalize(price[1][1]['close']),f.normalize(price[2][1]['close'])],False, symbol[0],10,dark=False, title='Crecimiento del mercado de centros de datos', subtitle='Crecimiento en % desde 20/07/2017', source='FMPcloud.io')
p.linep([price[0][1]['close']], symbol[0],10,dark=True,  title='Equinix daily price performance', subtitle='Price in U.S. Dollars', source='FMPcloud.io')

fig, ax, colors=p.layout([price[0][1]['close']], symbol[0],dark=False)
                                                                    


# g1='#0052000'
# g2='#005c00'
# g3='#006600'
# g4='#007000'
# g5='#007b00'
# g6='#258d19'
# g7='#4ea93b'
# g8='#71c55b'
# g9='#92e27a'
# g10='#b4ff9a'

# colors=[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10]




# av=matplotlib.style.available
# for i in range(len(av)):
#         plt.style.use(av[i])
#         fig, ax = plt.subplots()  
#         ax.yaxis.set_ticks_position('left')
#         ax.xaxis.set_ticks_position('bottom')
#         ax.yaxis.grid(False)
#         ax.xaxis.grid(False)
#         plt.plot(price[0][1]['close'].index, price[0][1]['close'])
#         ax.set_xlabel(str(av[i]),  color='seagreen',
#                       weight='bold')
#         ax.spines.top.set_visible(False)
#         ax.spines.right.set_visible(False)



