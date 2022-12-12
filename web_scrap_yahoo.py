# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 16:37:56 2022

@author: diegu
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import scipy
import importlib
import matplotlib.pyplot as plt
import datetime as dt
from scipy.stats import skew, kurtosis, chi2, linregress
from scipy.optimize import minimize
from numpy import linalg as LA
from pandas_datareader import data
import yfinance as yf

# import our own files and reload
import file_classes
importlib.reload(file_classes)
import file_functions
importlib.reload(file_functions)

tickers_list=['CME', 'SI', 'NVDA', 'TWTR',  'MSTR', '8473.T']
tickers_data= {}
for ticker in tickers_list:
    ticker_object = yf.Ticker(ticker)

    #convert info() output from dictionary to dataframe
    temp = pd.DataFrame.from_dict(ticker_object.info, orient="index")
    temp.reset_index(inplace=True)
    temp.columns = ["Attribute", "Recent"]
    
    # add (ticker, dataframe) to main dictionary
    tickers_data[ticker] = temp

tickers_data
tickers_data
combined_data = pd.concat(tickers_data)
combined_data = combined_data.reset_index()
combined_data

del combined_data["level_1"] # clean up unnecessary column
combined_data.columns = ["Ticker", "Attribute", "Recent"] # update column names

combined_data

beta = combined_data[combined_data["Attribute"]=="beta"].reset_index()
del beta["index"] # clean up unnecessary column

beta
print(str(beta))

# # tickers.info
# financials=tickers.tickers.TWTR.financials
# balance=tickers.balance_sheet
# cashflow=tickers.cashflow
# earnings=tickers.earnings
# print(str(tickers.recommendations))
# tickers.options
# opt = tickers.option_chain('2022-03-18')
# print(tickers)

# plt.subplot(cashflow)
