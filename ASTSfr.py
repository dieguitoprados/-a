# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 17:21:05 2022

@author: diego
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import tqdm
from sec_edgar_api import EdgarClient
import numpy as np
import plots as p
import functions_diego as f
import json
import ovbapp as ovb
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

tickr='ASTS'

edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
filings=edgar.get_submissions(f.cik(tickr))
filings=pd.DataFrame(filings['filings']['recent'])
facts=edgar.get_company_facts(f.cik(tickr))
def cleanfinQ(facts, name):

    df=facts['facts']['us-gaap'][name]['units']
    for lot in ['Store','USD', 'USD/shares', 'Year', ('pure','Year'), 'pure', 'shares']:
        try:
            df=pd.DataFrame(df[lot])
        except Exception:
            pass
    df['end']=pd.to_datetime(df['end'])
    df['ts']=pd.to_datetime(df['end'])-pd.to_datetime(df['start'])
    # df=df.set_index('end')
    dff=df.loc[df['ts']<pd.to_timedelta("100day")]
    dff=dff.drop_duplicates('end')
    dff=dff.set_index('end')
    dfff=df.loc[df['ts']>pd.to_timedelta("269day")]
    dfff=dfff.drop_duplicates('end')
    a=dfff.loc[df['ts']>pd.to_timedelta("300day")]
    n=dfff.loc[df['ts']<pd.to_timedelta("300day")]
    qqqq=pd.DataFrame((val1- val2 for val1, val2 in zip(a['val'],n['val'])),index=a['end'])
    dff=dff['val'].append(qqqq.squeeze())
    dff=dff.sort_index(ascending=True)
    dff=dff.rename(name)    
    return dff


def incQ():
    incq=pd.DataFrame()
    names=['RevenueFromContractWithCustomerIncludingAssessedTax','CostOfRevenue', 'GrossProfit',
           'OtherGeneralExpense', 'GeneralAndAdministrativeExpense', 'ResearchAndDevelopmentExpense',
            'DepreciationAndAmortization', 'OperatingExpenses', 'FairValueAdjustmentOfWarrants',
            'InterestIncomeExpenseNonoperatingNet', 'NonoperatingIncomeExpense',
            'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest',
            'IncomeTaxExpenseBenefit', 'ProfitLoss',
            'NetIncomeLossAttributableToNoncontrollingInterest', 'NetIncomeLossAvailableToCommonStockholdersBasic']
    for name in names:
        incq=incq.append(cleanfinQ(facts,name))
    incq=incq.transpose()
    incq=incq.sort_index(ascending=True)
    incq=incq.transpose()
    return incq

incq=incQ()

incq=incq.iloc[:,3:]

def cleanbalQ(facts, name):
    
    df=facts['facts']['us-gaap'][name]['units']
    for lot in ['Store','USD', 'USD/shares', 'Year', ('pure','Year'), 'pure', 'shares']:
        try:
            df=pd.DataFrame(df[lot])
        except Exception:
            pass
    dff=df.drop_duplicates('end')    
    dff=dff.set_index(pd.to_datetime(dff['end']))
    dff=dff.sort_index(ascending=True)
    dff=dff['val'].rename(name)
    return dff

cash=cleanbalQ(facts, 'CashAndCashEquivalentsAtCarryingValue')



def balQ():
    balq=pd.DataFrame()
    names=['CashAndCashEquivalentsAtCarryingValue','RestrictedCashCurrent','AccountsReceivableNetCurrent',
           'InventoryNet','PrepaidExpenseCurrent','OtherAssetsCurrent','AssetsCurrent',
           'ConstructionInProgressGross','PropertyPlantAndEquipmentNet','OperatingLeaseRightOfUseAsset','IntangibleAssetsNetExcludingGoodwill',
           'Goodwill','OtherAssetsNoncurrent','OtherAssetsNoncurrent','Assets','AccountsPayableCurrent',
           'ContractWithCustomerLiabilityCurrent',
           'OperatingLeaseLiabilityCurrent','LiabilitiesCurrent',
           'OperatingLeaseLiabilityNoncurrent','LongTermDebtNoncurrent','Liabilities',
           'AdditionalPaidInCapital','AccumulatedOtherComprehensiveIncomeLossNetOfTax',
           'RetainedEarningsAccumulatedDeficit','MinorityInterest','StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest',
           'LiabilitiesAndStockholdersEquity']
    for name in names:
        balq=balq.append(cleanbalQ(facts,name))
    balq=balq.transpose()
    balq=balq.sort_index(ascending=True)
    balq=balq.transpose()

    return balq

balq=balQ()

p.linep([balq.loc['CashAndCashEquivalentsAtCarryingValue']], 'linear', ['Cash and Equivalens'], (6.8, 4.8), False, 'ASTS Cash and equivalents', 'At Carrying Value in US Dollars', 'sec.gov')


# ordenar balances

# horizontal, vertical, ratios, assumptions, forecast, delays & done!








# directory = 'C:\\Users\\diego\\OneDrive\\Documents\\GitHub\\-a\\companyfacts\\CIK0001780312.json'

# factsa=json.load(open(directory))
