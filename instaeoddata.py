# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 18:02:19 2023

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
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=SPY&interval=5min&apikey=I9MAV4MUJC2LWW69'
r = requests.get(url)
data = r.json()
spy=pd.DataFrame(data['Time Series (5min)']).transpose()

p.linep([spy['4. close']], 'linear', ['SPY'], (6.8,4.8), True, 'SPY EOD DATA', '02/01/2023', 'alphavantage.com')
