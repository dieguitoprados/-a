# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 18:37:12 2022

@author: diego
"""

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

tag = pd.read_csv("tag.txt", sep="\t")
num = pd.read_csv("num.txt", sep="\t").head()
pre = pd.read_csv("pre.txt", sep="\t").head(200)
sub = pd.read_csv("sub.txt", sep="\t")

gaap=tag[tag['version']=='us-gaap/2021']
