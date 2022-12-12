# -*- coding: utf-8 -*-
"""
Created on Sat May 21 20:00:03 2022

@author: diegu
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

symbol=['EQIX']


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

p.barp([financials[0][1][1]['revenue'], financials[0][1][1]['grossProfit'],financials[0][1][1]['ebitda'],financials[0][1][1]['netIncome']], 'linear', ['Revenue', 'Gross Profit', 'EBITDA', 'Net Income'], 10, False, financials[0][5], 'Revenue breakdown', 'FMPCloud.com')

p.linep([(-1)*financials[0][2][2]['capitalExpenditure'],financials[0][2][2]['changeInWorkingCapital'],financials[0][2][2]['depreciationAndAmortization']], 'linear', ['Capex','WC','Depreciation'], 10, False, 'title', 'subtitle', 'source')
# p.barp([financials[0][2][2]['freeCashFlow'],financials[0][2][2]['capitalExpenditure'],financials[0][2][2]['changeInWorkingCapital'],financials[0][2][2]['depreciationAndAmortization']], False, ['FCF','Capex','WC','Depreciation'], 10, False, 'title', 'subtitle', 'source')

sectors=f'https://fmpcloud.io/api/v4/sector_price_earning_ratio?date=2022-08-16&exchange=NYSE&apikey={apikey}'
indus=f'https://fmpcloud.io/api/v4/industry_price_earning_ratio?date=2022-08-16&exchange=NYSE&apikey={apikey}'



O = requests.get(sectors)
overview = O.json()
sec=pd.DataFrame(overview)
sec=sec.set_index('date')

O = requests.get(indus)
overview = O.json()
indus=pd.DataFrame(overview)



sector=pd.DataFrame(fmp.stock_screener(apikey, sector='Real Estate', limit=10000000))

plt.figure()
plt.title('Scatterplot of the REIT sector dividend per share')
plt.scatter(sector['lastAnnualDividend'],sector['price'])
plt.xlabel('Dividend')
plt.ylabel('Share Price')
plt.grid()
plt.show()




sgb=sector.groupby('industry')


for group_name, df_group in sgb:
    
    plt.figure()
    plt.title('Scatterplot of the '+group_name+' industry')
    plt.scatter(sgb['price'].get_group(group_name),sgb['lastAnnualDividend'].get_group(group_name))
    plt.xlabel('Dividend')
    plt.ylabel('Share Price')
    plt.grid()
    plt.show()






trad = sgb.get_group('REIT—Specialty')[sgb.get_group('REIT—Specialty')['isActivelyTrading']==True]


trad=trad[(trad.country=='US')]
stocks=list()
for name in trad['symbol']:
    stocks.append(name)
    
    
    
    
reit=c.get_data(apikey)
reit.get_financials(stocks)
reit.get_price(stocks)
pricee=reit.price
financialss=reit.financials


divv=pd.DataFrame()
for i in range(0,len(financialss)):
    divv.append(fmp.historical_stock_dividend(apikey, financialss[i][0])['historical'])
# divv=pd.DataFrame(div)
divv.loc['Column_Total']= divv.sum(numeric_only=True, axis=0)
# divv.loc[:,'Row_Total'] = divv.sum(numeric_only=True, axis=1)
divv=divv.transpose()
# yr=divv.groupby('year')['Column_Total'].transform(sum)


yr=divv.resample('Y').Column_Total.sum()
# yr.index=pd.to_datetime(yr.index).dt.date

p.barp([-1*yr], 'linear', ['Dividends paid'], 10, False, 'REIT--Specialty industry dividends', 'Meassured in $US', 'FMPCloud.io')
p.linep([-1*yr], 'log', ['Dividends paid'], 10, False, 'REIT--Specialty industry dividends', 'Meassured in $US', 'FMPCloud.io')


f.cagr(yr[0], yr[-1], len(yr)-1)

f.cagr(financialss[2][2][2]['dividendsPaid'][7], financialss[2][2][2]['dividendsPaid'][-1],7 )

rev=[]
for i in range(0,len(financialss)):
    rev.append(financialss[i][2][2]['commonStockRepurchased'])
revv=pd.DataFrame(rev)
revv.loc['Column_Total']= revv.sum(numeric_only=True, axis=0)
# divv.loc[:,'Row_Total'] = divv.sum(numeric_only=True, axis=1)
revv=revv.transpose()
# yrr=revv.groupby('year')['Column_Total'].transform(sum)


yrr=revv.resample('Y').Column_Total.sum()

p.barp([-1*yrr,-1*yr], 'linear', ['Stock Buybacks','Dividends paid'], 10, False, 'REIT--Specialty industry dividends & buybacks', 'Meassured in $US', 'FMPCloud.io')
p.linep([-1*yrr], 'linear', ['Dividends paid'], 10, False, 'REIT--Specialty industry dividends', 'Meassured in $US', 'FMPCloud.io')


f.cagr(yrr[0], yrr[-2], len(yrr)-2)

f.cagr(financialss[2][2][2]['dividendsPaid'][7], financialss[2][2][2]['dividendsPaid'][-1],7 )

# reg=pd.DataFrame()
# Eq=f.clean_financials(fmp.historical_price_full(apikey, 'EQIX'))
# sp=f.clean_financials(fmp.historical_price_full(apikey, '^GSPC'))
# mtg = pd.DataFrame(fred.get_series('MORTGAGE30US'))

# reg['EQIX']=pd.DataFrame(Eq['close']/Eq['close'].shift(1)-1)
# reg['sp']=sp['close']/sp['close'].shift(1)-1

# reg=reg.dropna()

# Y=reg['sp']
# X=reg['EQIX']
# X = sm.add_constant(X)
# model = sm.OLS(Y,X)
# results=model.fit(cov_type='HC1')
# print(results.summary())

# for i in range(len(symbol)):
    
#     div=pd.DataFrame(fmp.historical_stock_dividend(apikey, symbol[i])['historical'])
#     div=div.loc[:26]
#     div=div.loc[::-1]
    
    # plt.style.use('seaborn-darkgrid')
    # fig, ax = plt.subplots()  
    # plt.bar(div['date'],div['dividend'], label='dividend',  color='limegreen')
    # ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
    #                       ncol=2, mode="expand", borderaxespad=0.)
    # plt.xticks(rotation = 80)
    # ax.yaxis.grid(True, color='palegreen', alpha=0.3)
    
    
    # ax.set_facecolor("white")
    # ax.set_xlabel(plt.legend())
    # ax.set_xlabel(symbol[i]+' Liquidity Ratios TTM',  color='seagreen',
    #               weight='bold')
    # # ax.legend()
    # ax.text(
    #         0.75,
    #         0,
    #         'Greenfield Capital Advisors Group S.L.',
    #         horizontalalignment='center',
    #         verticalalignment='top',
    #         transform=ax.transAxes)
    # fig.tight_layout()

# dcf=fmp.discounted_cash_flow(apikey, symbol[0])
# hdcf=fmp.historical_daily_discounted_cash_flow(apikey, symbol[0], limit =60)

# l=pd.DataFrame(fmp.income_statement(apikey, symbol[0],'quarter'))
# ass=f.clean_financials(fmp.income_statement(apikey, symbol[0],'quarter', limit=90))
print("--- %s seconds ---" % (time.time() - s))

# plt.style.use('seaborn-darkgrid')
# fig, ax = plt.subplots()    
# plt.plot(financials[i])
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# plt.xticks(rotation = 80)
# # Axis formatting.
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.tick_params(bottom=False, left=False)
# ax.set_axisbelow(True)
# ax.yaxis.grid(True, color='#EEEEEE')
# ax.xaxis.grid(False)



# # Add text annotations to the top of the bars.
# # bar_color = bars[0].get_facecolor()
# # for bar in bars:

# # Add labels and a title. Note the use of `labelpad` and `pad` to add some
# # extra space between the text and the tick labels.
# ax.set_facecolor("white")
# ax.set_xlabel(plt.legend())
# ax.set_ylabel('Income', labelpad=15, color='seagreen')
# ax.set_xlabel(symbol[0]+' Income statement ',  color='seagreen',
#               weight='bold')
# # ax.legend()
# ax.text(
#         0.75,
#         0,
#         'Greenfield Capital Advisors Group S.L.',
#         horizontalalignment='center',
#         verticalalignment='top',
#         transform=ax.transAxes)
# fig.tight_layout()

# plt.savefig('filename.png', dpi=300)



# ##EXPENSES






# ##LIQUIDITY

# plt.style.use('seaborn-darkgrid')
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# fig, ax = plt.subplots()  
# plt.plot(financials[1][1][3].index,financials[1][1][3]['currentRatio'], label='currentRatio',marker='o', markersize=4, color='limegreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['quickRatio'],label='quickRatio',marker='o', markersize=4, color='forestgreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['cashRatio'],label='cashRatio',marker='o', markersize=4, color='seagreen')
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# plt.xticks(rotation = 80)
# ax.yaxis.grid(True, color='palegreen', alpha=0.3)


# ax.set_facecolor("white")
# ax.set_xlabel(plt.legend())
# ax.set_xlabel(symbol[0]+' Liquidity Ratios TTM',  color='seagreen',
#               weight='bold')
# # ax.legend()
# ax.text(
#         0.75,
#         0,
#         'Greenfield Capital Advisors Group S.L.',
#         horizontalalignment='center',
#         verticalalignment='top',
#         transform=ax.transAxes)
# fig.tight_layout()

# ##MARGINS

# plt.style.use('seaborn-darkgrid')
# fig, ax = plt.subplots()  
# plt.plot(financials[1][1][3].index,financials[1][1][3]['grossProfitMargin'], label='grossProfitMargin',marker='o', markersize=4, color='lime')
# # plt.plot(financials[1][1][3].index,financials[1][1][3]['ebitdaratio'], label='ebitdaratio',marker='o', markersize=4, color='limegreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['operatingProfitMargin'],label='operatingProfitMargin',marker='o', markersize=4, color='forestgreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['netProfitMargin'],label='netProfitMargin',marker='o', markersize=4, color='seagreen')
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# plt.xticks(rotation = 80)
# ax.yaxis.grid(True, color='palegreen', alpha=0.3)


# ax.set_facecolor("white")
# ax.set_xlabel(plt.legend())
# ax.set_xlabel(symbol[0]+' Profit Margins TTM',  color='seagreen',
#               weight='bold')
# # ax.legend()
# ax.text(
#         0.75,
#         0,
#         'Greenfield Capital Advisors Group S.L.',
#         horizontalalignment='center',
#         verticalalignment='top',
#         transform=ax.transAxes)
# fig.tight_layout()

# #profitability

# plt.style.use('seaborn-darkgrid')
# fig, ax = plt.subplots()  
# plt.plot(financials[1][1][3].index,financials[1][1][3]['returnOnAssets'], label='returnOnAssets',marker='o', markersize=4, color='lime')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['returnOnEquity'], label='returnOnEquity',marker='o', markersize=4, color='limegreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['returnOnCapitalEmployed'],label='returnOnCapitalEmployed',marker='o', markersize=4, color='forestgreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['ebitPerRevenue'],label='ebitPerRevenue',marker='o', markersize=4, color='seagreen')
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# plt.xticks(rotation = 80)
# ax.yaxis.grid(True, color='palegreen', alpha=0.3)


# ax.set_facecolor("white")
# ax.set_xlabel(plt.legend())
# ax.set_xlabel(symbol[0]+' Profitability Ratios TTM',  color='seagreen',
#               weight='bold')
# # ax.legend()
# ax.text(
#         0.75,
#         0.02,
#         'Greenfield Capital Advisors Group S.L.',
#         horizontalalignment='center',
#         verticalalignment='top',
#         transform=ax.transAxes)
# fig.tight_layout()
# #solvency

# plt.style.use('seaborn-darkgrid')
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# fig, ax = plt.subplots()  
# plt.plot(financials[1][1][3].index,financials[1][1][3]['debtEquityRatio'], label='debtEquityRatio',marker='o', markersize=4, color='lime')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['debtRatio'], label='debtRatio',marker='o', markersize=4, color='limegreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['totalDebtToCapitalization'],label='totalDebtToCapitalization',marker='o', markersize=4, color='forestgreen')
# plt.plot(financials[1][1][3].index,financials[1][1][3]['longTermDebtToCapitalization'],label='longTermDebtToCapitalization',marker='o', markersize=4, color='seagreen')
# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# plt.xticks(rotation = 80)
# ax.yaxis.grid(True, color='palegreen', alpha=0.3)


# ax.set_facecolor("white")
# ax.set_xlabel(plt.legend())
# ax.set_xlabel(symbol[0]+' Debt Ratios TTM',  color='seagreen',
#               weight='bold')
# # ax.legend()
# ax.text(
#         0.75,
#         0,
#         'Greenfield Capital Advisors Group S.L.',
#         horizontalalignment='center',
#         verticalalignment='top',
#         transform=ax.transAxes)
# fig.tight_layout()









# plt.style.use('seaborn-darkgrid')

# fig, ax = plt.subplots(figsize=(8,5))

# # Save the chart so we can loop through the bars below.
    
# bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='lime',height=self.financials[i][1][1]['revenue'],label='revenue',tick_label=self.financials[i][1][1].index.strftime('%d/%m/%Y'))
# for bar in bars:
#     ax.text(
#         bar.get_x() + bar.get_width() / 2,
#         bar.get_height() + 0.3,
#         round(bar.get_height()/1000000, 1),
#         horizontalalignment='center',
#         color='black',
#         weight='bold',size=8
#     )

# bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='limegreen',height=self.financials[i][1][1]['grossProfit'],label='grossProfit')
# for bar in bars:
#     ax.text(
#         bar.get_x() + bar.get_width() / 2,
#         bar.get_height() + 0.3,
#         round(bar.get_height()/1000000, 1),
#         horizontalalignment='center',
#         color='black',
#         weight='bold',size=8
#     )

# bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='seagreen',height=self.financials[i][1][1]['ebitda'],label='ebitda')
# for bar in bars:
#     ax.text(
#         bar.get_x() + bar.get_width() / 2,
#         bar.get_height() + 0.3,
#         round(bar.get_height()/1000000, 1),
#         horizontalalignment='center',
#         color='black',
#         weight='bold',size=8
#     )

# bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='forestgreen',height=self.financials[i][1][1]['netIncome'],label='netIncome')
# for bar in bars:
#     ax.text(
#         bar.get_x() + bar.get_width() / 2,
#         bar.get_height() -3,
#         round(bar.get_height()/1000000, 1),
#         horizontalalignment='center',
#         color='black',
#         weight='bold',size=8
#     )
    
    


# ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
#                       ncol=2, mode="expand", borderaxespad=0.)
# plt.xticks(rotation = 80)
# # Axis formatting.
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['left'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.tick_params(bottom=False, left=False)
# ax.set_axisbelow(True)
# ax.yaxis.grid(False)
# ax.xaxis.grid(False)

# ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
# scale_y = 1e6
# ticks_y = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
# ax.yaxis.set_major_formatter(ticks_y)
# ax.set_ylabel('Income in millions', color='darkgreen')
# # ax.set_xlabel(plt.legend())
# ax.set_xlabel(self.stocks[i]+' Income statement ',  color='darkgreen',
#              weight='bold')
# # ax.legend()
# ax.set_facecolor("white")
# ax.text(
#         0.75,
#         0,
#         'Greenfield Capital Advisors Group S.L.',
#         color='black',
#         horizontalalignment='center',
#         verticalalignment='top',
#         transform=ax.transAxes)
# fig.tight_layout()


















# # anet.sp_ratios()
# # sp_rat=anet.sp_rat

# # sp=fmp.sp500_constituent(apikey)

# # ratios=pd.DataFrame()
# # for i in range(0, len(sp)):
# #     try:
# #         ratiosi=pd.DataFrame(fmp.financial_ratios(apikey, sp[i]['symbol'], limit=1))
# #         ratiosi=ratiosi.set_index('symbol')
# #         ratiosi=ratiosi.select_dtypes(exclude=['object'])
# #         ratios[sp[i]['symbol']]=ratiosi.loc[sp[i]['symbol']]
# #     except Exception:
# #         pass
# # ratios=ratios.transpose()
# # for item in ratios.keys():
# #     mean = np.mean(ratios[item])
# #     std = np.std(ratios[item])
# #     skewness= skew(ratios[item])
# #     kurt = kurtosis(ratios[item]) # excess kurtosis
# #     per_05 = np.percentile(ratios[item],5)
# #     per_20 = np.percentile(ratios[item],20)
# #     per_80 = np.percentile(ratios[item],80)
# #     per_95 = np.percentile(ratios[item],95)
# #     median = np.median(ratios[item])
# #     nb_decimals=3
# #     plot_str = 'mean ' + str(np.round(mean,nb_decimals))\
# #         + ' | std dev ' + str(np.round(std,nb_decimals))\
# #         + ' | skewness ' + str(np.round(skewness,nb_decimals))\
# #         + ' | kurtosis ' + str(np.round(kurt,nb_decimals)) + '\n'\
# #         + ' | p05% ' + str(np.round(per_05,nb_decimals))\
# #         + ' | p20% ' + str(np.round(per_20,nb_decimals))\
# #         + ' | median ' + str(np.round(median,nb_decimals))\
# #         + ' | p80% ' + str(np.round(per_80,nb_decimals))\
# #         + ' | p95% ' + str(np.round(per_95,nb_decimals))

# #     plt.hist(ratios[item], bins =90)
# #     plt.xlabel(plot_str)
# #     plt.title(item)
# #     plt.show()

# # fcfe=financials[0][1][2].at['2022-03-31','netIncome']+financials[0][1][2].at['2022-03-31','depreciationAndAmortization']+financials[0][1][2].at['2022-03-31','capitalExpenditure']-financials[0][1][2].at['2022-03-31','changeInWorkingCapital']-financials[0][1][0].at['2022-03-31','netDebt']
# # fcfee=fcfe/financials[0][1][2].at['2022-03-31','netIncome']

# # comb=list(combinations(ratios, 2))
    
# # for i in range(0, len(comb)):
# #     plt.figure()
# #     plt.title(comb[i][0]+' | '+comb[i][1])
# #     plt.scatter(ratios[comb[i][0]], ratios[comb[i][1]])
# #     plt.show()
    

# # for item in bal:

# #     fig = plt.figure()
# #     ax = fig.add_axes([0,0,1,1])
# #     plt.title('Income Statement '+financials[0][0])
# #     financials[0][2].loc[item].plot
# #     plt.legend()
# #     plt.show()









