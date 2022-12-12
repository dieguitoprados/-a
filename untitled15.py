
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
import plots as p
s=time.time()
import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

symbol=['EQIX', 'DLR', 'SBAC', 'CCI']


anet=c.get_data(apikey)
anet.get_financials(symbol)
anet.get_price(symbol)
price=anet.price
financials=anet.financials

# graphs

anet.hist_inc()
anet.liquidity()
anet.margins()
anet.profitability()
anet.solvency()
anet.hist_returns()

v=financials[0][1][1]['incomeTaxExpense']/financials[0][1][1]['incomeBeforeTax']


ffunds = fred.get_series('BAA')


p.linep([financials[0][2][1]['incomeTaxExpense']/financials[0][2][1]['incomeBeforeTax'].loc[dt.date(2016, 2, 26):]], 'linear', ['tax %'], 10, False, 'Effective tax rate', financials[0][5], 'FMPcloud.com')
p.linep([financials[0][2][1]['interestExpense']/financials[0][2][0]['totalDebt'].loc[dt.date(2010, 1, 1):], ffunds.loc[dt.datetime(2010, 1, 1):]/100], 'linear', ['interest expense %', 'BAA rated bond yields'], 10, False, 'Effective tax rate', financials[0][5], 'FMPcloud.com')


g=((financials[0][2][2]['operatingCashFlow'])/financials[0][2][0]['totalEquity'])*(1+financials[0][2][2]['dividendsPaid']/financials[0][2][2]['operatingCashFlow'])
g


gg=(financials[0][2][2]['operatingCashFlow'])/(financials[0][2][2]['operatingCashFlow'].shift(1))-1


p.linep([g,gg], 'linear', ['Implied Growth Rate FFO', 'actual grrowth rate FFO'], 10, False, 'Growth rates', financials[0][5], 'FMPcloud.com')
