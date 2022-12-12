# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 18:16:17 2022

@author: diego
"""
import fmpsdk as fmp
import pandas as pd
import datetime as dt
import tqdm
from sec_edgar_api import EdgarClient
import plots as p
import functions_diego as f
import json
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

tickr='AAPL'

edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
sub=edgar.get_submissions(f.cik(tickr))
filings=pd.DataFrame(sub['filings']['recent'])
facts=edgar.get_company_facts(f.cik(tickr))

ass=pd.DataFrame()

bal=pd.DataFrame()
for name in ['CashAndCashEquivalentsAtCarryingValue','MarketableSecuritiesCurrent' ]:
    try:
        bal=bal.append(f.clean(facts, 'CashAndCashEquivalentsAtCarryingValue'))['val'].rename('cashAndCashEquivalents')
        bal=bal.append(f.clean(facts, 'MarketableSecuritiesCurrent')['val'].rename('shortTermInvestments'))
        bal=bal.append((bal.iloc[1].fillna(0)+bal.iloc[0].fillna(0)).rename('cashAndShortTermInvestments'))
        bal=bal.append(f.clean(facts, 'InventoryNet')['val'].rename('inventory'))
        bal=bal.append(f.clean(facts, 'AccountsReceivableNetCurrent')['val'])
        bal=bal.append(f.clean(facts, 'NontradeReceivablesCurrent')['val'])
        bal=bal.append((bal.iloc[1].fillna(0)+bal.iloc[0].fillna(0)).rename('netReceivables'))
        bal=bal.append(f.clean(facts, 'OtherAssetsCurrent')['val'].rename('other_current'))
        bal=bal.append(f.clean(facts, 'AssetsCurrent')['val'].rename('totalasscurr'))
    except Exception:
        pass
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()
# bal=bal.append()





cashAndCashEquivalents=f.clean(facts, 'CashAndCashEquivalentsAtCarryingValue')['val'].rename('cashAndCashEquivalents')
shortTermInvestments=f.clean(facts, 'MarketableSecuritiesCurrent')['val'].rename('shortTermInvestments')
cashAndShortTermInvestments=pd.DataFrame().append([cashAndCashEquivalents, shortTermInvestments])

cashAndShortTermInvestments=(cashAndShortTermInvestments.iloc[1].fillna(0)+cashAndShortTermInvestments.iloc[0].fillna(0)).rename('cashAndShortTermInvestments')

inventory=f.clean(facts, 'InventoryNet')['val'].rename('inventory')

acc=f.clean(facts, 'AccountsReceivableNetCurrent')['val']
non=f.clean(facts, 'NontradeReceivablesCurrent')['val']
netReceivables=pd.DataFrame().append([acc, non])
# netReceivables=acc

netReceivables=(netReceivables.iloc[1].fillna(0)+netReceivables.iloc[0].fillna(0)).rename('netReceivables')

other_current=f.clean(facts, 'OtherAssetsCurrent')['val'].rename('other_current')

totalasscurr=f.clean(facts, 'AssetsCurrent')['val'].rename('totalasscurr')

MarketableSecuritiesNoncurrent=f.clean(facts, 'MarketableSecuritiesNoncurrent')['val'].rename('MarketableSecuritiesNoncurrent')

PropertyPlantAndEquipmentNet=f.clean(facts, 'PropertyPlantAndEquipmentNet')['val'].rename('PropertyPlantAndEquipmentNet')

Goodwill=f.clean(facts, 'Goodwill')['val'].rename('Goodwill')

IntangibleAssetsNetExcludingGoodwill=f.clean(facts, 'IntangibleAssetsNetExcludingGoodwill')['val'].rename('IntangibleAssetsNetExcludingGoodwill')

OtherAssetsNoncurrent=f.clean(facts, 'OtherAssetsNoncurrent')['val'].rename('OtherAssetsNoncurrent')

AssetsNoncurrent=f.clean(facts, 'AssetsNoncurrent')['val'].rename('AssetsNoncurrent')

totalass=f.clean(facts, 'Assets')['val'].rename('totalass')

ass=pd.DataFrame()
ass=ass.append([cashAndCashEquivalents, shortTermInvestments,cashAndShortTermInvestments,netReceivables,other_current, inventory, 
                totalasscurr,MarketableSecuritiesNoncurrent, PropertyPlantAndEquipmentNet,Goodwill,IntangibleAssetsNetExcludingGoodwill,OtherAssetsNoncurrent,
                AssetsNoncurrent, totalass])


balan=f.clean_financials(fmp.balance_sheet_statement(apikey, tickr)).transpose()
incomest=f.clean_financials(fmp.income_statement(apikey, tickr)).transpose()
cfst=f.clean_financials(fmp.cash_flow_statement(apikey, tickr)).transpose()

AccountsPayable=f.clean(facts, 'AccountsPayableCurrent')['val'].rename('AccountsPayable')


currliab=f.clean(facts, 'LiabilitiesCurrent')['val'].rename('LiabilitiesCurrent')
liab=f.clean(facts, 'Liabilities')['val'].rename('Liabilities')
pasivo=f.clean(facts, 'LiabilitiesAndStockholdersEquity')['val'].rename('LiabilitiesAndStockholdersEquity')
noncurrliab=f.clean(facts, 'LiabilitiesNoncurrent')['val'].rename('LiabilitiesCurrent')
LongTermDebt=f.clean(facts, 'LongTermDebtNoncurrent')['val'].rename('LongTermDebtNonCurrent')
TaxesPayableCurrent=f.clean(facts, 'TaxesPayableCurrent')['val'].rename('TaxesPayableCurrent')
DeferredRevenueCurrent=f.clean(facts, 'DeferredRevenueCurrent')['val'].rename('DeferredRevenueCurrent')
OtherLiabilitiesCurrent=f.clean(facts, 'OtherLiabilitiesCurrent')['val'].rename('OtherLiabilitiesCurrent')

pas=pd.DataFrame()








# Easy Balaance
# def EasyBalance(tickr):










