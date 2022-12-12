import datetime as dt
import streamlit as st
import pandas as pd
import numpy as np
import requests
import fmpsdk as fmp
import datetime as dt
import matplotlib.pyplot as plt
import plotly as pt
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as scipy
import tqdm
import functions_diego as f
import matplotlib.cm as cm
import matplotlib
import flexitext
import matplotlib.ticker as mtick
import statsmodels.api as sm


import functions_diego as f
import classes_diego as c

from fredapi import Fred
fred = Fred(api_key='97606ccae6e98b9ef43f33fb7d7b4492')
eonia = fred.get_series()
dff = fred.get_series('FEDFUNDS')
sonia = fred.get_series('IUDSOIA')
apikey='d60d2f087ecf05f94a3b9b3df34310a9'
today = dt.date.today()





sp=pd.DataFrame(index=f.clean_financials(fmp.historical_price_full(apikey, '^GSPC')).index)
sp['sp']=f.clean_financials(fmp.historical_price_full(apikey, '^GSPC'))['close']
sp['dff']=dff
sp=sp.fillna(method='ffill')
sp=sp/sp.shift(1)-1
sp=sp.dropna()
sp[sp['dff']>0.01]
plt.scatter(sp['sp'], sp['dff'])


Y=sp['sp']
X=sp['dff']
model = sm.OLS(Y,X)
results = model.fit()

print(results.summary())

y=dt.date(1999, 6, 26)
eonia=eonia.loc[y:]
sonia=sonia.loc[y:]
dff=dff.loc[y:]


plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()  
ax.plot(eonia, color='forestgreen', linewidth=0.7,label='ECB EONIA', alpha=0.9)
ax.plot(sonia, color='limegreen', linewidth=0.7,label='BoE SONIA', alpha=0.9)
ax.plot(dff, color='black', linewidth=0.7,linestyle='--',label='Effective Federal Funds Rate', alpha=0.9)
ax.legend()
ax.yaxis.grid(True, color='palegreen', alpha=0.3)
ax.xaxis.grid(True, color='palegreen', alpha=0.3)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_facecolor('none')
ax.set_xlabel('Main Interest Rates',  color='seagreen',
              weight='bold')
# ax.legend()
ax.text(
        0.5,
        0.5,
        'Greenfield Capital Advisors Group S.L.',
        horizontalalignment='center',
        verticalalignment='top',color = 'black', weight='bold',
        fontsize=18, alpha=0.5,
        transform=ax.transAxes)
fig.tight_layout()
st.pyplot(fig)
