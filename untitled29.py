# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 00:40:05 2022

@author: diegu
"""

import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
import requests
import fmpsdk as fmp
import datetime as dt
import matplotlib.pyplot as plt
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as scipy
import tqdm
import functions_diego as f
import matplotlib.cm as cm
import matplotlib
import flexitext
import matplotlib.ticker as mtick
import statsmodels.api as sm
from dateutil.relativedelta import relativedelta
y = dt.date.today() - relativedelta(years=1)
mmmmmm = dt.date.today() - relativedelta(months=6)
l=dt.datetime(2000, 1, 1)
import functions_diego as f
import classes_diego as c
import plots as p

from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

bal=pd.DataFrame(fmp.balance_sheet_statement(apikey, 'ASTS')).transpose()
bala=fmp.balance_sheet_statement_as_reported(apikey, 'ASTS')
bal.index

recdays=f.recdays()
ffunds = fred.get_series('DFF')
yields=pd.DataFrame(index=ffunds.index)
yields['1d']=ffunds
yields['1M'] = fred.get_series('DGS1MO')
yields['3M'] = fred.get_series('DGS3MO')
yields['6M'] = fred.get_series('DGS6MO')
yields['dgs1'] = fred.get_series('DGS1')
yields['dgs2'] = fred.get_series('DGS2')
yields['dgs3'] = fred.get_series('DGS3')
yields['dgs5'] = fred.get_series('DGS5')
yields['dgs7'] = fred.get_series('DGS7')
yields['dgs10'] = fred.get_series('DGS10')
yields['dgs20'] = fred.get_series('DGS20')
cpi = fred.get_series('CPILFESL')
cpi=cpi/cpi.shift(12)-1
yields['dgs30'] = fred.get_series('DGS30')
yields['dgs30'] = fred.get_series('DGS30')
yields=yields.fillna(method='ffill')
yields.index=pd.to_datetime(yields.index)
yields=yields.loc[dt.datetime(2000, 1, 1):]
p.linep([yields['1d'], yields['1M']], 'linear', ['federal funds rate', '1 Month'], 10, False, '1 Month vs. Effective rate', 'Money markets', 'Federal Reserve Bank of New York')
fig, ax=plt.subplots()
ax.plot(ffunds)
plt.show()
zz=yields.loc[str(mmmmmm)]
z=yields.loc[str(y)]
zzz=yields.loc[str(l):]
n=np.arange(0,12)

fmp.cryptocurrencies_list(apikey)
btc=f.clean_financials(fmp.historical_price_full(apikey, 'BTCUSD'))
NVDA=f.clean_financials(fmp.historical_price_full(apikey, 'NVDA'))
ETH=f.clean_financials(fmp.historical_price_full(apikey, 'ETHUSD'))

# cpi=pd.DataFrame()
# cpi['cpi']=yields['cpi'].dropna()
# cpi.index = pd.to_datetime(cpi.index)
# cpi = cpi['2000-01-10':'2022-07-01']

av=fmp.available_indexes(apikey)
s=fmp.sectors_performance(apikey)

gold=f.clean_financials(fmp.historical_price_full(apikey, 'GCUSD',from_date=dt.date(1980, 1, 1) ))
gas=f.clean_financials(fmp.historical_price_full(apikey, 'LUSD',from_date=dt.date(1980, 1, 1) ))
natgas=f.clean_financials(fmp.historical_price_full(apikey, 'NGUSD',from_date=dt.date(1980, 1, 1)))
a=fmp.commodities_list(apikey)

cpi['gas']=gas['close'].values
cpi['natgas']=natgas['close']

cpi=cpi.dropna


e=p.eod_data(apikey, fred)

e.USA_eod()
e.EU_eod()
e.asia_pacific_eod()




bal=pd.DataFrame(fmp.balance_sheet_statement_as_reported(apikey, 'EQIX'))
inc=pd.DataFrame(fmp.income_statement_as_reported(apikey, 'EQIX'))
cf=pd.DataFrame(fmp.cash_flow_statement_as_reported(apikey, 'EQIX'))
cfn=f.clean_financials(fmp.cash_flow_statement_as_reported(apikey, 'EQIX',limit=5))

cff=f.clean_financials(fmp.cash_flow_statement(apikey, 'EQIX'))




# p.barp([z,zz],False, ['etti -6meses','etti -1año'], 10, True, 'ETTI -6M & -1Y', 'in % points', 'Federal reserve bank of St. Louis')


p.linep([f.normalize(gas['close']),f.normalize(zzz['cpi'].dropna())], 'Gold vs interesst rates for the US', 10, False, 'Gold vs interesst rates for the US', 'What could be next for gold?', 'Federal Reserve Bank of St. Louis')


p.linep([yields.iloc[-1],zz,z],'linear', ['ETTI hoy', 'ETTI -6 Meses', 'ETTI -1 Año'], 10,False, 'Se invierten los tipos de interés en USA', '¿Qué significa esto?', 'Federal Reserve Bank of St. Louis')
p.linep([f.normalize(btc['close']), f.normalize(NVDA['close']), f.normalize(ETH['close'])],False,['BTC', 'NVDA', 'ETH'] , 10,True, 'Nvidia vs. crypto', '¿Qué significa esto?', 'Federal Reserve Bank of St. Louis')



ffunds = fred.get_series('DFF')
inf = fred.get_series('CPALTT01USM659N')
aaa = fred.get_series('AAA')
baa = fred.get_series('BAA')
mtg = fred.get_series('MORTGAGE30US')
fffunds=ffunds.rolling(10).mean()

df=pd.DataFrame()
df['ffunds']=fffunds
df['inf']=inf
df['aaa']=aaa
df['baa']=baa

aaa=aaa.loc[dt.date(1955, 1, 1):]
baa=baa.loc[dt.date(1955, 1, 1):]
inf=inf.loc[dt.date(1955, 1, 1):]

p.linep([df['ffunds'], inf, aaa,baa], 'linear', ['Fed funds', 'CPI inflation YoY', 'Aaa rated bonds','Baa rated bonds'], 10, False, 'Macro variables for the US', 'Is inflation here to stay?','Federal Reserve Bank of St. Louis' )
p.linep([df['ffunds'], inf, aaa], 'linear', ['Fed funds', 'CPI inflation YoY', 'Aaa rated bonds'], 10, False, 'Macro variables for the US', 'Is inflation here to stay?','Federal Reserve Bank of St. Louis' )

nf=fffunds.loc[dt.date(1970, 1, 1):dt.date(1976, 1, 1)]
nff=baa.loc[dt.date(1970, 1, 1):dt.date(1976, 1, 1)]
nfff=aaa.loc[dt.date(1970, 1, 1):dt.date(1976, 1, 1)]
nffff=inf.loc[dt.date(1970, 1, 1):dt.date(1976, 1, 1)]

p.linep([nf, nff, nfff], 'linear', ['Fed funds', 'CPI inflation YoY', 'Aaa rated bonds'], 10, False, 'Macro variables for the US', 'Is inflation here to stay?','Federal Reserve Bank of St. Louis' )
p.linep([baa-aaa], 'linear', ['Credit spread'], 10, False, 'Macro variables for the US', 'Is inflation here to stay?','Federal Reserve Bank of St. Louis' )
p.linep([baa-aaa, inf], 'linear', ['Credit spread', 'CPI'], 10, False, 'Macro variables for the US', 'Is inflation here to stay?','Federal Reserve Bank of St. Louis' )

np.corrcoef(baa-aaa.loc[445:], inf)
np.corrcoef(aaa,baa-aaa)

inf['cs']=baa-aaa
inf=inf.dropna()

np.corrcoef(inf['cs'],inf[0])
recdays=f.recdays()
df2 = recdays.mask((recdays['recdays'] == 0) & ((recdays['recdays'].shift(1) == 0) | (recdays['recdays'].shift(-1) == 0)))
df2['group'] = (df2['recdays'].shift(1).isnull() & df2['recdays'].notnull()).cumsum()
df2=df2[df2['recdays'].notnull()].groupby('group')
recs=[]
for name, group in df2:
    recs.append(df2.get_group(name))

fig,ax=plt.subplots()
colors=p.col(False)
p.line([nf, nff, nfff], ['Aaa rated bonds', 'Baa rated bonds', 'Inflation'], colors, ax)
ppp=[0,1]
# recs(ax,p)
    
for i in ppp:
    ax.axvspan(recs[i].index[0], recs[i].index[-1], color='grey', alpha=0.2)
    

fig.show()
