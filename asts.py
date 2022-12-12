# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 20:12:05 2022

@author: diego
"""

#Analisis ASTS

import fmpsdk as fmp
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

tickr='AAPL'

edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
filings=edgar.get_submissions(f.cik(tickr))
filings=pd.DataFrame(filings['filings']['recent'])
facts=edgar.get_company_facts(f.cik(tickr))


#Income Statement


def inc():

    CostOfRevenue=f.cleanfinanual(facts, 'CostOfGoodsAndServicesSold')['val'].rename('CostOfRevenue')
    GrossProfit=f.cleanfinanual(facts, 'GrossProfit')['val'].rename('GrossProfit')
    Revenue=(GrossProfit+CostOfRevenue).rename('Revenue')
    
    RnD=f.cleanfinanual(facts, 'ResearchAndDevelopmentExpense')['val'].rename('RnD')
    sellgeneralexpense=f.cleanfinanual(facts, 'SellingGeneralAndAdministrativeExpense')['val'].rename('SellingGeneralAndAdministrativeExpense')
    OperatingExpenses=f.cleanfinanual(facts, 'OperatingExpenses')['val'].rename('OperatingExpenses')
    OperatingIncome=f.cleanfinanual(facts, 'OperatingIncomeLoss')['val'].rename('OperatingIncome')
    
    
    ebt=f.cleanfinanual(facts, 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest')['val'].rename('ebt')
    interest=f.cleanfinanual(facts, 'InterestExpense')['val'].rename('InterestExpense')
    interestincome=f.cleanfinanual(facts, 'InvestmentIncomeInterestAndDividend')['val'].rename('InterestIncome')
    otherincexp=f.cleanfinanual(facts, 'OtherNonoperatingIncomeExpense')['val'].rename('otherincexp')
    DepreciationAndAmortization=f.cleanfinanual(facts, 'DepreciationAndAmortization')['val']
    DepreciationAndAmortization=DepreciationAndAmortization.append(f.cleanfinanual(facts, 'Depreciation')['val']).rename('DepreciationAndAmortization')
    tax=f.cleanfinanual(facts, 'IncomeTaxExpenseBenefit')['val'].rename('IncomeTaxExpenseBenefit')
    NetIncome=f.cleanfinanual(facts, 'NetIncomeLoss')['val'].rename('NetIncome')
    Dividends=f.cleanfinanual(facts, 'PaymentsOfDividends')['val'].rename('Dividends')
    Buybacks=f.cleanfinanual(facts, 'PaymentsForRepurchaseOfCommonStock')['val'].rename('Buybacks')
    stockcomp=f.cleanfinanual(facts, 'ShareBasedCompensation')['val'].rename('ShareBasedCompensation')
    # fcf=f.cleanfinanual(facts, '')['val'].rename('')
    
    
    inc=pd.DataFrame().append([CostOfRevenue, GrossProfit,Revenue,RnD,sellgeneralexpense, OperatingExpenses, 
                    OperatingIncome,interest,interestincome,otherincexp,ebt, DepreciationAndAmortization,tax,NetIncome,Dividends, 
                    Buybacks, stockcomp]).dropna(axis=1)
    return inc, Revenue
inc, Revenue=inc()

plt.plot(inc.loc['RnD']/Revenue)
plt.plot(inc.loc['SellingGeneralAndAdministrativeExpense']/Revenue)
plt.plot((inc.loc['OperatingExpenses']+inc.loc['CostOfRevenue'])/Revenue)

#Balance Sheet

def ass(Revenue):

    cashAndCashEquivalents=f.clean(facts, 'CashAndCashEquivalentsAtCarryingValue')['val'].rename('cashAndCashEquivalents')
    shortTermInvestments=f.clean(facts, 'MarketableSecuritiesCurrent')['val'].rename('shortTermInvestments')
    cashAndShortTermInvestments=pd.DataFrame().append([cashAndCashEquivalents, shortTermInvestments]).sum().rename('cashAndShortTermInvestments')
    
    inventory=f.clean(facts, 'InventoryNet')['val'].rename('inventory')
    
    acc=f.clean(facts, 'AccountsReceivableNetCurrent')['val']
    non=f.clean(facts, 'NontradeReceivablesCurrent')['val']
    netReceivables=pd.DataFrame().append([acc, non]).sum().rename('netReceivables') 
    
    other_current=f.clean(facts, 'OtherAssetsCurrent')['val'].rename('other_current')
    totalasscurr=f.clean(facts, 'AssetsCurrent')['val'].rename('totalasscurr')
    PropertyPlantAndEquipmentNet=f.clean(facts, 'PropertyPlantAndEquipmentNet')['val'].rename('PropertyPlantAndEquipmentNet')
   
    # MarketableSecuritiesNoncurrent=f.clean(facts, 'MarketableSecuritiesNoncurrent')['val'].rename('MarketableSecuritiesNoncurrent')
    # Goodwill=f.clean(facts, 'Goodwill')['val'].rename('Goodwill')
    # IntangibleAssetsNetExcludingGoodwill=f.clean(facts, 'IntangibleAssetsNetExcludingGoodwill')['val'].rename('IntangibleAssetsNetExcludingGoodwill')
    
    OtherAssetsNoncurrent=f.clean(facts, 'OtherAssetsNoncurrent')['val'].rename('OtherAssetsNoncurrent')
    totalass=f.clean(facts, 'Assets')['val'].rename('totalass')
    AssetsNoncurrent=(totalass-totalasscurr).rename('AssetsNoncurrent')
    
    currliab=f.clean(facts, 'LiabilitiesCurrent')['val'].rename('LiabilitiesCurrent')
    liab=f.clean(facts, 'Liabilities')['val'].rename('Liabilities')
    pasivo=f.clean(facts, 'LiabilitiesAndStockholdersEquity')['val'].rename('LiabilitiesAndStockholdersEquity')
    noncurrliab=(liab-currliab).rename('LiabilitiesNonCurrent')
    StockholdersEquity=f.clean(facts, 'StockholdersEquity')['val'].rename('StockholdersEquity')
    CommonStock=f.clean(facts, 'CommonStocksIncludingAdditionalPaidInCapital')['val'].rename('CommonStock')
    RetainedEarnings=f.clean(facts, 'RetainedEarningsAccumulatedDeficit')['val'].rename('RetainedEarnings')    
    ass=pd.DataFrame()
    ass=ass.append([cashAndShortTermInvestments,netReceivables,other_current, inventory, totalasscurr,
                    PropertyPlantAndEquipmentNet,OtherAssetsNoncurrent,
                    AssetsNoncurrent, totalass, currliab, noncurrliab,liab,CommonStock, RetainedEarnings, StockholdersEquity, pasivo])
    ass=ass.dropna(axis=1)
    asssales=(ass/Revenue).dropna(axis=1)
    
    return ass, asssales

ass, asssales=ass(Revenue)

# # #Assumptions

# Sales Growth -2, 28 al 95%-98% centrada en 12
yrcagr=(Revenue.iloc[-1]/Revenue.iloc[10])**(1/5)-1
yrcagrr=(Revenue.iloc[-1]/Revenue.iloc[5])**(1/10)-1
annualgrowth=(Revenue/Revenue.shift(1)-1).dropna()
annualgrowth.mean()
annualgrowth.std()
annualgrowth.tail().mean()
yrcagr
yrcagrr
fig, ax=plt.subplots()
plt.hist(annualgrowth, bins=15)
plt.show()
plt.plot(annualgrowth)
ltg=0.065



#CurrentAssets/Sales 0.4+-0.1
ass.loc['totalasscurr']-ass.loc['cashAndShortTermInvestments']
plt.plot((ass.loc['totalasscurr']-ass.loc['cashAndShortTermInvestments'])/Revenue)
plt.plot(asssales.loc['cashAndShortTermInvestments'])

curry=((ass.loc['totalasscurr']-ass.loc['cashAndShortTermInvestments'])/Revenue).mean()
asssales.loc['totalasscurr'].std()


#CurrentLiabilities/Sales .37+-.1
plt.plot(asssales.loc['LiabilitiesCurrent'])
plt.plot(asssales.loc['Liabilities'])

lir=asssales.loc['LiabilitiesCurrent'].mean()
asssales.loc['LiabilitiesCurrent'].std()

#NetFixedassets/Sales

plt.plot(asssales.loc['PropertyPlantAndEquipmentNet'])
plt.plot(asssales.loc['Liabilities'])

na=asssales.loc['PropertyPlantAndEquipmentNet'].mean()
asssales.loc['PropertyPlantAndEquipmentNet'].std()

#Cost/Sales
cs=inc.loc['CostOfRevenue']/Revenue
cs.mean()
cs.std()

#Cost/Sales
cs=(inc.loc['CostOfRevenue']+inc.loc['OperatingExpenses'])/Revenue
cs.mean()
cs.std()
#Depretiation%
ds=inc.loc['DepreciationAndAmortization']/ass.loc['PropertyPlantAndEquipmentNet']
ds.mean()
ds.std()
plt.plot(ds)
#Interest% on Debt
inter=inc.loc['InterestExpense']/ass.loc['Liabilities']
plt.plot(inter)
#Interest% on Marketable Securities InterestIncome
interp=inc.loc['InterestIncome']/ass.loc['cashAndShortTermInvestments']
plt.plot(interp)
#Tax%20+-5
taxx=inc.loc['IncomeTaxExpenseBenefit']/inc.loc['ebt']
plt.plot(taxx)


#Dividend Payout
payout=(inc.loc['Dividends']+inc.loc['Buybacks']-inc.loc['ShareBasedCompensation'])/inc.loc['NetIncome']
pay=inc.loc['Dividends']/inc.loc['NetIncome']


plt.plot(ass.loc['RetainedEarnings'])
plt.plot(asssales.loc['cashAndShortTermInvestments'])
plt.plot(inc.loc['Buybacks'])

##Projections

def projectionsbasecase():
    incproject=pd.DataFrame()
    revenue=[inc.loc['Revenue'][-1]]
    COGSOpEx=[inc.loc['CostOfRevenue'][-1]+inc.loc['OperatingExpenses'][-1]]
    OperatingIncome=[revenue[0]-COGSOpEx[0]]
    othercurrentass=[ass.loc['totalasscurr'][-1]-ass.loc['cashAndShortTermInvestments'][-1]]
    netfixedass=[ass.loc['PropertyPlantAndEquipmentNet'][-1]]
    currliab=[ass.loc['LiabilitiesCurrent'][-1]]
    debt=[ass.loc['LiabilitiesNonCurrent'].iloc[-1]+ass.loc['LiabilitiesCurrent'].iloc[-1]]
    stock=[ass.loc['CommonStock'][-1]]
    otherexpenses=[inc.loc['otherincexp'][-1]]
    ebt=[inc.loc['ebt'][-1]]
    tax=[inc.loc['IncomeTaxExpenseBenefit'][-1]]
    netincome=[inc.loc['NetIncome'][-1]]
    dividends=[inc.loc['Dividends'][-1]]
    retainedearnings=[ass.loc['RetainedEarnings'][-1]]
    totaleq=[ass.loc['StockholdersEquity'][-1]]
    totalass=[ass.loc['totalass'][-1]]
    cashandeq=[ass.loc['cashAndShortTermInvestments'][-1]]
    depreciation=[inc.loc['DepreciationAndAmortization'][-1]]
    incurrass=[(ass.loc['totalasscurr'][-1]-ass.loc['cashAndShortTermInvestments'][-1])-(ass.loc['totalasscurr'][2]-ass.loc['cashAndShortTermInvestments'][-2])]
    incurrliab=[ass.loc['LiabilitiesCurrent'][-1]-ass.loc['LiabilitiesCurrent'][-2]]
    infixass=[ass.loc['PropertyPlantAndEquipmentNet'][-1]-ass.loc['PropertyPlantAndEquipmentNet'][-2]]
    aftertaxint=[inc.loc['InterestIncome'][-1]-inc.loc['InterestIncome'][-1]*taxx.mean()]
    aftertaxinrat=[inc.loc['InterestExpense'][-1]-inc.loc['InterestExpense'][-1]*taxx.mean()]
    fcf=[netincome[0]+depreciation[0]-incurrass[0]+incurrliab[0]-infixass[0]+aftertaxinrat[0]-aftertaxint[0]]

    for i in range(1,6):
        revenue.append(revenue[i-1]*(1+yrcagr))
        COGSOpEx.append(revenue[i]*cs.mean())
        OperatingIncome.append(revenue[i]-COGSOpEx[i])
        otherexpenses.append(cashandeq[i-1]*interp[-1]-debt[i-1]*inter[-1])
        ebt.append(OperatingIncome[i]+otherexpenses[i])
        tax.append(ebt[i]*taxx.mean())
        netincome.append(ebt[i]-tax[i])
        dividends.append(pay.iloc[-1]*netincome[i])
        stock.append(stock[i-1])
        retainedearnings.append(retainedearnings[i-1]+netincome[i]*(1-pay.iloc[-1]))
        totaleq.append(stock[i]+retainedearnings[i])
        debt.append(ass.loc['LiabilitiesNonCurrent'].iloc[-1]+revenue[i]*lir)
        totalass.append(totaleq[i]+debt[i])
        netfixedass.append(revenue[i]*na)
        currliab.append(revenue[i]*lir)
        othercurrentass.append(revenue[i]*curry)
        cashandeq.append(totalass[i]-netfixedass[i]-othercurrentass[i])
        depreciation.append(netfixedass[i]*ds.mean())
        incurrass.append(othercurrentass[i]/othercurrentass[i-1]-1)
        incurrliab.append(currliab[1]/currliab[i-1]-1)
        infixass.append(netfixedass[1]/netfixedass[i-1]-1)
        aftertaxint.append(cashandeq[i-1]*interp[-1]-cashandeq[i-1]*interp[-1]*taxx.mean())
        aftertaxinrat.append(debt[i-1]*inter[-1]-debt[i-1]*inter[-1]*taxx.mean())
        fcf.append(netincome[i]+depreciation[i]-incurrass[i]+incurrliab[i]-infixass[i]+aftertaxinrat[i]-aftertaxint[i])
    
    incproject={'Revenue':revenue, 'COGSOpEx':COGSOpEx,'OperatingIncome':OperatingIncome,
                'otherexpenses':otherexpenses, 'ebt':ebt,'tax':tax, 'NetIncome':netincome,
                'Dividends':dividends, 'CommonStock':stock, 'RetainedEarnings':retainedearnings,
                'TotalEquity':totaleq, 'Liabilities':debt, 'TotalAssets':totalass, 
                'NetFixedAssets':netfixedass, 'OtheCurrentAssets':othercurrentass, 'CashAndEquivalents':cashandeq,
                'Depreciation':depreciation, 'IncreaseCurrentAssets':incurrass, 'IncreaseCurrentLiab':incurrliab,
                'IncreaseFixedAssets':infixass, 'AfterTaxIntPaid':aftertaxint, 'AfterTaxIntExpense':aftertaxinrat,
                'FreeCashFlow':fcf}
    incproject=pd.DataFrame(incproject,index=pd.date_range('30/9/2022', '30/9/2027',6 ))    
    incproject=incproject.transpose()
    
    return incproject
incproject=projectionsbasecase()

resultados, re=f.re(tickr)
rd=0.0425
ed=(ass.loc['StockholdersEquity'].append(incproject.loc['TotalEquity'])/(ass.loc['LiabilitiesAndStockholdersEquity'].append(incproject.loc['Liabilities'])+ass.loc['StockholdersEquity'].append(incproject.loc['TotalEquity']))).mean()
wacc=re[1]*ed+rd*(1-ed)

waccc=(1+wacc)**(np.linspace(0, 5, 6))

(incproject.loc['FreeCashFlow'][-1]*(1+ltg)/(wacc-ltg))/((1+wacc)**5)
shares=f.cleanfinanual(facts, 'WeightedAverageNumberOfSharesOutstandingBasic')['val'][-1]
(sum(incproject.loc['FreeCashFlow']/waccc)+(incproject.loc['FreeCashFlow'][-1]*(1+ltg)/(wacc-ltg))/((1+wacc)**5))/shares

p.linep([ass.loc['StockholdersEquity'].append(incproject.loc['TotalEquity']),
         ass.loc['cashAndShortTermInvestments'].append(incproject.loc['CashAndEquivalents']),
         ass.loc['RetainedEarnings'].append(incproject.loc['RetainedEarnings'])],
        'linear', ['Total Equity','Cash Projections', 'Retained Earnings'],
        (6.4, 4.8), False, 'Cash and Cash Equivalents Projection',
        'AAPL 2022', 'sec.gov')
ovb.lineovb([ass.loc['StockholdersEquity'].append(incproject.loc['TotalEquity']),
         ass.loc['cashAndShortTermInvestments'].append(incproject.loc['CashAndEquivalents']),
         ass.loc['RetainedEarnings'].append(incproject.loc['RetainedEarnings'])],
        'linear', ['Total Equity','Cash Projections', 'Retained Earnings'],
        (6.4, 4.8), False, 'Cash and Cash Equivalents Projection',
        'AAPL 2022', 'sec.gov')
p.linep([ass.loc['StockholdersEquity'].append(incproject.loc['TotalEquity']),
         ass.loc['cashAndShortTermInvestments'].append(incproject.loc['CashAndEquivalents']),
         ass.loc['RetainedEarnings'].append(incproject.loc['RetainedEarnings'])],
        'linear', ['Total Equity','Cash Projections', 'Retained Earnings'],
        (6.4, 4.8), False, 'Cash and Cash Equivalents Projection',
        'AAPL 2022', 'sec.gov')

