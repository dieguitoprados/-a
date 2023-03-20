# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 00:51:13 2023

@author: diego
"""
import json
import requests
import time
import pandas_datareader.data as web
import statsmodels.api as sm
import datetime as dt
import pandas as pd
import numpy as np
import importlib
from tqdm import tqdm
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
import fmpsdk as fmp

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
apikey='cdcb171caeb7cc3ab258fb24c77918a1'
from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')

import openai

# Set up OpenAI API credentials
# openai.api_key = "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"
directory = 'C:\\Users\\diego\\OneDrive\\Documents\\GitHub\\-a\\companyfacts\\CIK0000049279.json'
data_json=json.load(open(directory))

import os
os.environ["OPENAI_API_KEY"] = 'YOUR_OPENAI_API_KEY'

import llama_index 

# Create an instance of the LlamaIndex class
index = llama_index.LlamaIndex()

# Define the path to the directory containing your JSON files
data_dir = directory
# Define the name of the index
index_name = 'my_index'

# Define the maximum number of documents to index
max_docs = 10000

# Define the size of the chunks to read from the files
chunk_size = 1000

# Add the files to the index in chunks
for i in range(0, max_docs, chunk_size):
    # Read a chunk of documents from the files
    docs = []
    for j in range(chunk_size):
        try:
            with open(f'{data_dir}/{i+j}.json') as f:
                doc = json.load(f)
                docs.append(doc)
        except:
            pass
    # Add the chunk of documents to the index
    index.add_documents(docs, index_name)

# Save the index to disk
index.save_index(index_name, '/path/to/index/directory')








# Define a prompt to provide context for GPT-3
# prompt = "Based on the following financial data, please generate a commentary on the company's current assets:\n\n" + str(f.clean_financials(fmp.balance_sheet_statement(apikey, 'ASTS')).transpose().iloc[:7]) + "\n\n"

# response = openai.Completion.create(
#     engine="text-davinci-002",
#     prompt=prompt,
#     max_tokens=1024,
#     n=1,
#     stop=None,
#     temperature=0.7,
# )

# commentary = response.choices[0].text.strip()
# print(commentary)



