# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 13:20:28 2023

@author: diego
"""

import time
import pandas_datareader.data as reader
import statsmodels.api as sm
import datetime as dt
import pandas as pd
import numpy as np
import requests
import importlib
import datetime as dt
import matplotlib.pyplot as plt
import scipy.stats as scipy
from scipy.stats import skew, kurtosis, chi2, linregress
import plots as p
from sec_edgar_api import EdgarClient
edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
s=time.time()
import functions_diego as f
importlib.reload(f)
import yfinance as yf

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))

from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')

apikey='I9MAV4MUJC2LWW69'
start=dt.date(2000, 1, 31)
end=dt.date.today()
stock=['GOLD', 'NEM', 'FNV']
resultados=[]

#load variables for regression

class re():
    
    def __init__(self,start):
        self.apikey='I9MAV4MUJC2LWW69'
        self.start=start
        self.end=None
        self.factors, self.end=f.load_factors(self.start)
        self.capm=[]       
        self.ffm=[]       
        self.stocks=[]
        self.data=pd.DataFrame(index=pd.date_range(start=self.start, periods=len(self.factors), freq='M'))
    
    
    
    def mreturns(self):
        for stock in self.stocks:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={stock}&apikey={apikey}'
            r = requests.get(url)
            df = pd.DataFrame.from_dict(r.json()['Monthly Time Series']).transpose()['4. close'].rename(stock).astype('float').sort_index(ascending=True)
            df.index=pd.to_datetime(df.index).to_period('M').to_timestamp('M')
            df=df.loc[self.start-pd.DateOffset(months=1):self.end]
            df=(df/df.shift(1)-1).dropna()*100
            self.data[stock]=df
        
        return self.data

    def CAPM(self):
        for i in range(len(self.stocks)):
            df=self.factors
            df[self.stocks[i]]=self.data[self.stocks[i]]
            df=df.dropna()
            Y=df[self.stocks[i]]-df['RF']
            X=df['Mkt-RF']
            X = sm.add_constant(X)
            model = sm.OLS(Y,X)
            results=model.fit(cov_type='HC1')
            capmean=((1+df.mean()/100)**12)-1
            capmpar=results.params
            recapm=df['RF'][-1]/100+capmpar[1]*capmean[2]
            self.capm.append(list())
            self.capm[i].append(recapm)
            self.capm[i].append(results.rsquared_adj)
            for n in range(len(results.params)):
                self.capm[i].append(results.params[n])
                self.capm[i].append(results.pvalues[n])
                
        for i in range(len(self.capm)):
            self.capm[i]=[round(elem, 4) for elem in self.capm[i]]
            
        self.capm=pd.DataFrame(self.capm, index=self.stocks, columns=['E(re)', 'Adj R-squared','Intercept', 'P>|z| Int',
                                                        'B1(Mkt-RF)', 'P>|z| B1'])

        return self.capm

    def FFM(self):
        for i in range(len(self.stocks)):
            df=self.factors
            df[self.stocks[i]]=self.data[self.stocks[i]]
            df=df.dropna()
            Y=df[self.stocks[i]]-df['RF']
            X=df[['Mkt-RF', 'SMB', 'HML']]
            X = sm.add_constant(X)
            model = sm.OLS(Y,X)
            results=model.fit(cov_type='HC1')
            ffmean=((1+df.mean()/100)**12)-1
            ffmpar=results.params
            reffm=df['RF'][-1]/100+ffmpar[1]*ffmean[2]+ffmpar[2]*ffmean[3]+ffmpar[3]*ffmean[4]
            self.ffm.append(list())
            self.ffm[i].append(reffm)
            self.ffm[i].append(results.rsquared_adj)
            for n in range(len(results.params)):
                self.ffm[i].append(results.params[n])
                self.ffm[i].append(results.pvalues[n])
                
        for i in range(len(self.capm)):
            self.ffm[i]=[round(elem, 4) for elem in self.ffm[i]]
            
        self.ffm=pd.DataFrame(self.ffm, index=self.stocks, columns=['E(re)', 'Adj R-squared','Intercept', 'P>|z| Int',
                                                        'B1(Mkt-RF)', 'P>|z| B1','B2(SMB)', 'P>|z| B2','B3(HML)',
                                                        'P>|z| B3'])

        return self.ffm

        
        
        
        
MSFT=re(start)
factors=MSFT.factors
MSFT.stocks=stock
mret=MSFT.mreturns()
MSFT.CAPM()
capm=MSFT.capm
MSFT.FFM()
ffm=MSFT.ffm
MSFT.stocks[2]

