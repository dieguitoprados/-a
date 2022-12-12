# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 21:29:40 2022

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
import datetime as dt
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

tickr='AAPL'

edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
filings=edgar.get_submissions(f.cik(tickr))
filings=pd.DataFrame(filings['filings']['recent'])
facts=edgar.get_company_facts(f.cik(tickr))


#Assumptions



#Income Statement
inc=pd.DataFrame()
Revenue=f.cleanfinanual(facts, 'RevenueFromContractWithCustomerExcludingAssessedTax')['val'].rename('Revenue')
OperatingIncomeLoss=f.cleanfinanual(facts, 'OperatingIncomeLoss')['val'].rename('OperatingIncomeLoss')
CostOfGoodSold=f.cleanfinanual(facts, 'CostsAndExpenses')['val'].rename('CostOfGoodSold')
InterestExpense=f.cleanfinanual(facts, 'InterestExpense')['val'].rename('InterestExpense')
InvestmentIncomeInterest=f.cleanfinanual(facts, 'InvestmentIncomeInterest')['val'].rename('InvestmentIncomeInterest')
Depreciation=f.cleanfinanual(facts, 'Depreciation')['val'].rename('Depreciation')
IncomeTaxesPaidNet=f.cleanfinanual(facts, 'IncomeTaxesPaidNet')
# IncomeTaxesPaidNet=IncomeTaxesPaidNet.groupby(IncomeTaxesPaidNet.index.year).sum()
# RetainedEarningsAccumulatedDeficit=f.clean(facts, 'RetainedEarningsAccumulatedDeficit')['val'].rename('RetainedEarningsAccumulatedDeficit')
inc=inc.append([Revenue,OperatingIncomeLoss,CostOfGoodSold,InterestExpense,InvestmentIncomeInterest,
                Depreciation])
#Balance Sheet 
bal=pd.DataFrame()










