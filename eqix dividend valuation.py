# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 16:40:56 2022

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

# apikey='d60d2f087ecf05f94a3b9b3df34310a9'


# symbol=['EQIX']
eqix = yf.Ticker("AAPL")
# ng = yf.Ticker("NG=F")

# # get stock info
# eqix.info

# # get historical market data
ng = eqix.history(period="max", interval = "1mo", )

# # show actions (dividends, splits)
eqix.earnings
eps=eqix.earnings_history
# # show dividends


# # show splits
# eqix.splits

# # show financials
# fin=eqix.financials
# eqix.quarterly_financials






# anet=c.get_data(apikey)
# anet.get_financials(symbol)
# anet.get_price(symbol)
# price=anet.price
# financials=anet.financials
 

# # graphs

# anet.hist_inc()
# anet.liquidity()
# anet.margins()
# anet.profitability()
# anet.solvency()
# anet.hist_returns()

# p.barp([financials[0][1][1]['revenue'], financials[0][1][1]['grossProfit'],financials[0][1][1]['ebitda'],financials[0][1][1]['netIncome']], 'linear', ['Revenue', 'Gross Profit', 'EBITDA', 'Net Income'], 10, False, financials[0][5], 'Revenue breakdown', 'FMPCloud.com')

# p.linep([(-1)*financials[0][2][2]['capitalExpenditure'],financials[0][2][2]['changeInWorkingCapital'],financials[0][2][2]['depreciationAndAmortization']], 'linear', ['Capex','WC','Depreciation'], 10, False, 'title', 'subtitle', 'source')
# # p.barp([financials[0][2][2]['freeCashFlow'],financials[0][2][2]['capitalExpenditure'],financials[0][2][2]['changeInWorkingCapital'],financials[0][2][2]['depreciationAndAmortization']], False, ['FCF','Capex','WC','Depreciation'], 10, False, 'title', 'subtitle', 'source')

# sectors=f'https://fmpcloud.io/api/v4/sector_price_earning_ratio?date=2022-08-16&exchange=NYSE&apikey={apikey}'
# indus=f'https://fmpcloud.io/api/v4/industry_price_earning_ratio?date=2022-08-16&exchange=NYSE&apikey={apikey}'



# O = requests.get(sectors)
# overview = O.json()
# sec=pd.DataFrame(overview)
# sec=sec.set_index('date')

# O = requests.get(indus)
# overview = O.json()
# indus=pd.DataFrame(overview)



# sector=pd.DataFrame(fmp.stock_screener(apikey, sector='Real Estate', limit=10000000))

# sgb=sector.groupby('industry')


# for group_name, df_group in sgb:
    
#     plt.figure()
#     plt.title('Scatterplot of the '+group_name+' industry')
#     plt.scatter(sgb['price'].get_group(group_name),sgb['lastAnnualDividend'].get_group(group_name))
#     plt.xlabel('Dividend')
#     plt.ylabel('Share Price')
#     plt.grid()
#     plt.show()

# trad = sgb.get_group('REIT—Specialty')[sgb.get_group('REIT—Specialty')['isActivelyTrading']==True]


# trad=trad[(trad.country=='US')]
# trad=trad[trad['marketCap']>0]
# dividends=pd.DataFrame(index=pd.date_range(start='1/1/2011', end='08/24/2022'))
# for name in trad['symbol']:
#     dividends[name]=(f.clean_financials(fmp.historical_stock_dividend(apikey, name)['historical']))
# dividends=dividends.transpose()
    
# dividends.loc['Column_Total']= dividends.sum(numeric_only=True, axis=0)
# dividends=dividends.transpose()

# yr=dividends.resample('Y').Column_Total.sum()

# buybacks=list()
# for name in trad['symbol']:
#     buybacks.append((pd.DataFrame(f.clean_financials(fmp.cash_flow_statement(apikey, name))['commonStockRepurchased']))*-1,str(name) )

div=eqix.dividends
divi=f.ttm(div)
div=div.groupby(div.index.year).sum()
div = div.loc[2017:]
div=div.replace(9.3, 12.4)
divgr=div/div.shift(1)-1
divigr=divi/divi.shift(1)-1
divigr36ttm=((1+divigr.tail(12).mean())**4)-1
mdivgr=divgr.mean()
div5cagr=((1+(div.loc[2022]/div.loc[2017]-1))**(1/5))-1


directory = 'C:\\Users\\diego\\Downloads\\EQIX.CSV' # hardcoded
fna = 'C:\\Users\\diego\\Downloads\\^FNAR.CSV' # hardcoded
fne= 'C:\\Users\\diego\\Downloads\\^FNER.CSV' # hardcoded
dlr= 'C:\\Users\\diego\\Downloads\\DLR.CSV' # hardcoded
di = 'C:\\Users\\diego\\Downloads\\fuck.CSV' # hardcoded
eur = 'C:\\Users\\diego\\Downloads\\EURUSD=X.CSV' # hardcoded
data = pd.read_csv(di)
date=data.iloc[:1152]
date=date.iloc[1007:]
date.index=pd.to_datetime(date['Date'], format='%Y%m')
date.index=date.index.date
date=date.drop('Date', axis=1)
date=date.loc[dt.date(2014, 8, 1):]

eur= pd.read_csv(eur)
eur.index=pd.to_datetime(eur['Date'])
eur=100*(eur['Close']/eur['Close'].shift(1)-1)

dlr= pd.read_csv(dlr)
dlr.index=pd.to_datetime(dlr['Date'])
dlr=100*(dlr['Close']/dlr['Close'].shift(1)-1)

eq= pd.read_csv(directory)
eq.index=pd.to_datetime(eq['Date'])
eq=100*(eq['Close']/eq['Close'].shift(1)-1)

fnar= pd.read_csv(fna)
fnar.index=pd.to_datetime(fnar['Date'])
fnar=100*(fnar['Close']/fnar['Close'].shift(1)-1)

fner= pd.read_csv(fne)
fner.index=pd.to_datetime(fner['Date'])
fner=100*(fner['Close']/fner['Close'].shift(1)-1)


date['eqix']=eq
date['dlr']=dlr
date['eur']=eur
date['fner']=fner
date['fnar']=fnar
date['fne']=date['fner']-date['RF']
date['fna']=date['fnar']-date['RF']
date['aaa'] = fred.get_series('AAA')
date['baa' ]= fred.get_series('BAA')
date['kwh' ]= (fred.get_series('CUSR0000SEHF01')/fred.get_series('CUSR0000SEHF01').shift(12)-1)*100
date['construction' ]= (fred.get_series('TTLCONS')/fred.get_series('TTLCONS').shift(12)-1)*100
date['gas' ]= (fred.get_series('MHHNGSP')/fred.get_series('MHHNGSP').shift(12)-1)
date['spread']=date['baa']-date['aaa']
date['be']=fred.get_series('T5YIEM')
# date['30mortg']=pd.DataFrame(fred.get_series('MORTGAGE30US')).reindex('monthly', method='ffill')
date['cpi']=fred.get_series('CPIAUCSL')/fred.get_series('CPIAUCSL').shift(1)-1
date['ip']=fred.get_series('INDPRO')/fred.get_series('INDPRO').shift(1)-1
date['ue']=date['be']-date['cpi']
date['dgs1'] = fred.get_series('GS1')
date['exi']=date['dgs1']-date['RF']
date=date.dropna()
resultados=[]
for nam in ['fner','dlr','fnar', 'eqix']:
# nam='eqix'

    
    capm=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'gas', 'fna', 'fne', 'ue', 'exi']])
    print('CAPM '+nam) 
    Y=capm[nam]-capm['RF']
    X=capm[['Mkt-RF']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('CAPM '+nam+ '\n'+str(results.summary()))
    capmean=((1+capm.mean()/100)**12)-1
    print(capmean)
    capmvar=capm.var()
    capmpar=results.params
    recapm=date['dgs1'][-1]/100+capmpar[1]*capmean[2]#+capmpar[2]*capmean[3]
    rese=np.sqrt(np.sum(results.resid**2)/results.df_resid)
    
    ffm=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML']])
    print('FAMA-FRENCH Model '+nam)
    Y=ffm[nam]-ffm['RF']
    X=ffm[['Mkt-RF', 'SMB', 'HML']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('FAMA-FRENCH Model '+nam+ '\n'+str(results.summary()))
    ffmean=((1+ffm.mean()/100)**12)-1
    print(ffmean)
    ffmvar=(ffm/100).var()
    ffmpar=results.params
    reffm=date['dgs1'][-1]/100+ffmpar[1]*ffmean[2]+ffmpar[2]*ffmean[3]+ffmpar[3]*ffmean[4]
    print(ffmvar[2]*ffmean[2]**2+ffmvar[3]*ffmean[3]**2+ffmvar[4]*ffmean[4]**2+(3.295857)*2+(0.843252)*2+(0.324659)*2)
    rese=np.sqrt(np.sum(results.resid**2)/results.df_resid)
    
    apmw=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML', 'spread']])
    print('Arbitrage Pricing Model without inflation')
    Y=apmw[nam]-apmw['RF']
    X=apmw[['Mkt-RF', 'SMB', 'HML', 'spread']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('Arbitrage Pricing Model without inflation '+nam+ '\n'+str(results.summary()))
    apmwmean=((1+apmw.mean()/100)**12)-1
    apmwpar=results.params
    reapmw=date['dgs1'][-1]/100+apmwpar[1]*apmwmean[2]+apmwpar[2]*apmwmean[3]+apmwpar[3]*apmwmean[4]+apmwpar[4]*apmw['spread'].mean()/100

    
    apmexi=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML','spread', 'exi']])
    print('Arbitrage Pricing Model with 1y-1m')
    Y=apmexi[nam]-apmexi['RF']
    X=apmexi[['Mkt-RF', 'SMB', 'HML', 'spread', 'exi']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    a=results.params
    print(results.summary())
    resultados.append('Arbitrage Pricing Model with 1y-1m '+nam+ '\n'+str(results.summary()))
    apmeximean=((1+apmexi.mean()/100)**12)-1
    apmexipar=results.params
    reapmexi=date['dgs1'][-1]/100+apmexipar[1]*apmeximean[2]+apmexipar[2]*apmeximean[3]+apmexipar[3]*apmeximean[4]+apmexipar[4]*apmexi['spread'].mean()/100+apmexipar[5]*apmexi['exi'].mean()/100
    
    
    apmbe=pd.DataFrame(date[[nam, 'RF', 'Mkt-RF', 'SMB', 'HML','spread', 'ue', 'fna', 'fne']]).dropna()
    print('Arbitrage Pricing Model with breakeven 5yr')
    Y=apmbe[nam]-apmbe['RF']
    X=apmbe[['Mkt-RF', 'SMB', 'HML', 'spread', 'ue']]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results=model.fit(cov_type='HC1')
    print(results.summary())
    resultados.append('Arbitrage Pricing Model with breakeven 5yr '+nam+ '\n'+str(results.summary()))
    apmbemean=((1+apmbe.mean()/100)**12)-1
    apmbepar=results.params
    reapmbe=date['dgs1'][-1]/100+apmexipar[1]*apmeximean[2]+apmexipar[2]*apmeximean[3]+apmexipar[3]*apmeximean[4]+apmexipar[4]*apmbe['spread'].mean()/100+apmexipar[5]*apmbe['ue'].mean()/100
    
print(results.get_prediction)

eqixprice=631.16
regordoncagr=(div.loc[2022]*(1+div5cagr)/eqixprice)+div5cagr
regordonttm=(div.loc[2022]*(1+divigr36ttm)/eqixprice)+divigr36ttm  
regordon=(div.loc[2022]*(1+mdivgr)/eqixprice)+mdivgr
regordons=(div.loc[2022]*(1+0.06)/eqixprice)+0.06

growthapmw=(eqixprice*reapmw-div.loc[2022])/(div.loc[2022]+eqixprice)
growthcapm=(eqixprice*recapm-div.loc[2022])/(div.loc[2022]+eqixprice)
growthffm=(eqixprice*reffm-div.loc[2022])/(div.loc[2022]+eqixprice)
growthapmexi=(eqixprice*reapmexi-div.loc[2022])/(div.loc[2022]+eqixprice)
growthapmbe=(eqixprice*reapmbe-div.loc[2022])/(div.loc[2022]+eqixprice)

print('reffm: '+str(growthffm))
print('reapmw: '+str(growthapmw))
print('reapmexi: '+str(growthapmexi))
print('reapmbe: '+str(growthapmbe))

print('recapm: '+str(recapm))
print('reffm: '+str(reffm))
print('reapmw: '+str(reapmw))
print('reapmexi: '+str(reapmexi))
print('reapmbe: '+str(reapmbe))
remodels=[recapm, reffm, reapmw, reapmbe, reapmexi, regordoncagr, regordonttm]
price=[]
fgro=[]
for name in remodels:
    # price.append((12.17*(1+div5cagr))/(name-div5cagr))
    price.append((divi.iloc[-1]*(1+divigr36ttm))/(name-divigr36ttm))
    g=np.linspace(0, name)
    fgro.append(pd.DataFrame((divi.iloc[-1]*(1+g)/(name-g)), index=np.round(g, 4)))
    regordon=(div.loc[2022]*(1+g)/eqixprice)+g

    
    
# lab=['recapm', 'reffm', 'reapmw']
# p.linep([fgro[0],fgro[1],fgro[2]], 'linear',['recapm', 'reffm', 'reapmw'], 10, False, 'price as a function of growth','' , 'source')
# p.linep([regordon], 'linear',['regordon'], 10, False, 're as a function of growth','' , 'source')

# fig, ax, colors, im=p.layout(10, False, 'log')
# p.line([fgro[0],fgro[1],fgro[2]], ['re capm', 're ffm', 're ffm + SPREAD'], colors,ax)
# p.addt(fig, colors, 'Price of Equinix ', 'as a function of dividends growth', 'Yahoofinance.com', False)
# plt.savefig('p(g).png', dpi=600)




# capmpr=price[0:2]
# ffmpr=price[2:4]
# apmwpr=price[4:6]
# apmbepr=price[6:8]
# apmexipr=price[8:10]
# gordoncagrpr=price[10:12]
# gordonttmpr=price[12:14]


# api='pk_ae18fb28cc04485e89fee37dc4ba95e0'

# from iexfinance.stocks import Stock

# a = Stock("AAPL", token=api)
# a.get_quote()

capmpr=price[0]
ffmpr=price[1]
apmwpr=price[2]
apmbepr=price[3]
apmexipr=price[4]
gordoncagrpr=price[5]
gordonttmpr=price[6]

print('capm: '+str(capmpr))
print('ffm: '+str(ffmpr))
print('apmw: '+str(apmwpr))
print('apmbe: '+str(apmbepr))
print('apmexi: '+str(apmexipr))
print('gordoncagr: '+str(gordoncagrpr))
print('gordonttm: '+str(gordonttmpr))

# spr=pd.DataFrame()

# spr['aaa'] = fred.get_series('AAA')
# spr['baa' ]= fred.get_series('BAA')
# spr['spread']=spr['baa']-spr['aaa']

# spr['cpi']=fred.get_series('CPIAUCSL')/fred.get_series('CPIAUCSL').shift(12)-1


# p.linep([spr['spread'], spr['aaa'], spr['baa'],spr['cpi']*100], 'linear', ['spread', 'aaa', 'bbb', 'cpi'], 10, False, 'Spread and bonds', '', '')
# spr.corr()


#multiples valuation
shares=91000000
pepr=7.02*31.71
pffopr=(1745900000/shares)*14.74
pspr=72.48*5.26
evebitdapr=(2461100000/shares)*18.51

for pp in [pepr, pffopr, pspr, evebitdapr]:
    print(str(pp/eqixprice-1))
    print(str(eqixprice/pp-1))



gg=np.linspace(0.03, 0.08,11)
remodels=[recapm, reffm, reapmw]
for n in gg:
    gc=n
    gt=[]
    for i in range(1,5):  
        gt.append(divigr36ttm-(divigr36ttm-gc)*(i/5))
    
    stg=[]
    # name=reffm
    for name in remodels:
        stg.append((divi.iloc[-1]*(1+divigr36ttm))/(1+name)+(divi.iloc[-1]*((1+divigr36ttm)**2))/((1+name)**2)+(divi.iloc[-1]*((1+divigr36ttm)**3))/((1+name)**3)+
                       (divi.iloc[-1]*(((1+divigr36ttm)**3)*(1+gt[0])))/((1+name)**4)+(divi.iloc[-1]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])))/((1+name)**5)+(divi.iloc[-1]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])*(1+gt[2])))/((1+name)**6)+(divi.iloc[-1]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])*(1+gt[2])*(1+gt[3])))/((1+name)**7)+
                       (divi.iloc[-1]*(((1+divigr36ttm)**3)*(1+gt[0])*(1+gt[1])*(1+gt[2])*(1+gt[3])*(1+gc)))/(((1+name)**7)*(name-gc)))
    print(str(n)+str(stg))







# #recapm: 0.09252293115466206
# reffm: 0.11482521374349393
# reapmw: 0.15447721161056177
# reapmexi: 0.14762766983173195
# reapmbe: 0.14681964163628541-

# recapm: 0.08285288843905315
# reffm: 0.09779702070142059
# reapmw: 0.12901520888715057
# reapmexi: 0.12240620411114143
# reapmbe: 0.11689637028204652
