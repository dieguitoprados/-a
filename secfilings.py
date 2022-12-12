# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 22:14:19 2022

@author: diego
"""
import pandas as pd
import datetime as dt
import tqdm
from sec_edgar_api import EdgarClient
import plots as p
import functions_diego as f
import json
edgar = EdgarClient(user_agent="<Sample Company Name> <Admin Contact>@<Sample Company Domain>")
sub=edgar.get_submissions(cik="0001101239")
filings=pd.DataFrame(sub['filings']['recent'])
edgar.get_frames(taxonomy="us-gaap", tag="CashAndCashEquivalentsAtCarryingValue", unit="USD", year="2019", quarter=1)
facts=edgar.get_company_facts(f.cik('NFLX'))
facts=edgar.get_company_facts(cik="320193")
assett=edgar.get_frames(taxonomy="us-gaap", tag="Assets", unit="USD", year="2022", quarter=1)
assets=pd.DataFrame(assett['data'])
asse=edgar.get_frames(taxonomy="us-gaap", tag="Cash", unit="USD", year="2021", quarter=4)
asse=pd.DataFrame(asse['data'])
import os
# assign directory
directory = 'C:\\Users\\diego\\Downloads\\companyfacts'
 
# iterate over files in
# that directory
directories=[]
for filename in os.listdir(directory):
    directories.append(os.path.join(directory, filename))
    # checking if it is a file
cik=[]
for file in os.listdir(directory):
    cik.append(file)
cik = [i.replace('CIK','') for i in cik]
cik = [i.replace('.json','') for i in cik]
directory = 'C:\\Users\\diego\\Downloads\\companyfacts\\CIK0001101239.json'
equ=json.load(open(directory))
equ=equ['facts']['us-gaap']

fact=[]

nd=[]
ns=[]
for name in equ:
    try:
        fact.append(pd.DataFrame(equ[name]['units']['USD']))
    except Exception: nd.append(name)
for name in equ:
    try:
        fact.append(pd.DataFrame(equ[name]['units']['shares']))
    except Exception: ns.append(name)
    
    
for name in equ:
    print(name+':'+ '\n'+'  -'+str(equ[name]['description'])+ '\n')
    
    
assets=pd.DataFrame(equ['Assets']['units']['USD'])

ass=assets.drop_duplicates('end')
ass=f.clean(ass)
p.linep([assets['val'].sort_values().reindex(assets[''])], 'linear', ['Assets'], 10, False, 'Assets', 'all us companies for 2022 Q1 as reprted on 10Q', 'SEC filings')
