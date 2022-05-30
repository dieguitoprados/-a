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

s=time.time()
import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

symbol=['ANET', 'CSCO']

anet=c.get_data(symbol, apikey)

anet.get_financials()
financials=anet.financials
anet.get_price()
price=anet.price

execs=fmp.key_executives(apikey, symbol[0])
# graphs

anet.hist_inc()
anet.liquidity()
anet.margins()
anet.profitability()
anet.solvency()
anet.hist_returns()

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









