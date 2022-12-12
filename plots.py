# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 23:34:52 2022

@author: diego
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
import matplotlib.pylab as pl
from matplotlib import lines
from matplotlib import patches
import matplotlib.dates as mdate


s=time.time()
import functions_diego as f
importlib.reload(f)

import classes_diego as c
importlib.reload(c)
print("--- %s seconds ---" % (time.time() - s))
apikey='d60d2f087ecf05f94a3b9b3df34310a9'

def col(dark):
    if dark==False:
        g1='#008037'
        g2='#7ED957'
        g3='#C9E265'
        g4='black'
        g5='#BBFFFF'
        g6='#AEEEEE'
        g7='#96CDCD'
        g8='#668B8B'
        g9='#FF82AB'
        g10='#CD6889'
        g11='white'
        colors=[]
        colors=[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11]
    return colors

    if dark==True:
        g1='#008037'
        g2='#7ED957'
        g3='#C9E265'
        g4='White'
        g5='#BBFFFF'
        g6='#AEEEEE'
        g7='#96CDCD'
        g8='#668B8B'
        g9='#FF82AB'
        g10='#CD6889'
        g11='white'
        
        colors=[g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,g11]
    return colors




def layout(size,dark, l='linear'):

    if dark == True:
        # colors = pl.cm.YlGn(np.linspace(0,1,len(v)))
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(size))  
        ax.spines.top.set_visible(False)
        ax.spines.right.set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        colors=col(dark)
        im = plt.imread('glogo.png')
        plt.rcParams['figure.dpi'] = 300
        plt.yscale(l)

        # colors=colors[:len(v)]
        
        

    if dark == False:
        # colors = pl.cm.viridis(np.linspace(0,1,len(v)))
        plt.style.use('seaborn-ticks')
        fig, ax = plt.subplots(figsize=(size))  
        ax.spines.top.set_visible(False)
        ax.spines.right.set_visible(False)
        # ax.spines.left.set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        colors=col(dark)
        im = plt.imread('glogo.png')
        plt.rcParams['figure.dpi'] = 300
        plt.yscale(l)

        # colors=colors[:len(v)]

        
    return fig, ax, colors, im
        
# def sec_ax(s, ax):
#     if s[0]==True:
#         secax=ax.secondary_yaxis('right')
#         secax.set_ylabel(s[1])
#     else:
#         pass
#     return secax


def line(v, t, colors,ax):
        for i in range(len(v)):
            try:
                ax.plot(v[i], color=colors[i], label=t[i], linewidth=0.7, alpha=0.9)
            except: Exception
            pass
        ax.legend()    
        plt.tight_layout()
def bar(fig, bars,t, colors,ax):
                
        # plt.bar(x.index,h, color=colors[1], linewidth=0.7, alpha=0.9)
        # ax.legend()    
        # plt.tight_layout()
        barWidth=0.9/len(bars)
        r=list()
        
        r.append(np.arange(len(bars[0])))
        for i in range(1,len(bars)):
            r.append(list())

            r[i] = [x + barWidth for x in r[i-1]]
        for i in range(len(bars)):
            try:
        # Make the plot
                plt.bar(r[i], bars[i], color=colors[i], width=barWidth, edgecolor='white', label=t[i])
            except: Exception
            pass

        # Add xticks on the middle of the group bars
        # plt.xlabel('group', fontweight='bold')

        try:
            plt.xticks(r[0]+barWidth*((len(bars)-1)*0.5), bars[0].index.year, rotation=75)
        except: Exception
        pass
        try:
            plt.xticks(r[0]+barWidth*((len(bars)-1)*0.5), bars[0].index.year, rotation=75)
        except: Exception
        pass
    
        plt.legend()
        fig.tight_layout()
            
def addt(fig,colors,title,subtitle,source, dark,logo=True):
    # Make room below on top and bottom
    fig.subplots_adjust(top=0.825, bottom=0.15)
    if dark==True:
        c='white'
    else:
        c='black'
    # Add title
    fig.text(
        0, 0.92, title, 
        fontsize=15,
        fontweight="bold", 
        fontfamily="Econ Sans Cnd", color=c
    )
    # Add subtitle
    fig.text(
        0, 0.875, subtitle, 
        fontsize=12, 
        fontfamily="Econ Sans Cnd", color=c
    )

    # Add caption
    fig.text(
        0, 0.06, source, color='#a2a2a2', 
        fontsize=8, fontfamily="Econ Sans Cnd"
    )
    # Add authorship
    fig.text(
        0, 0.005, "Diego Prados. Seeking Alpha Contributor", color='#a2a2a2',
        fontsize=16, fontfamily="Helvetica"
    )

    # # Add line and rectangle on top.
    # fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color=colors[1], solid_capstyle="butt"))
    # fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color=colors[1]))
 
def addlogo(im,fig):
    newax = fig.add_axes([0.8,0.8,0.2,0.2], anchor='NE', zorder=1)
    newax.imshow(im)
    newax.axis('off')
    plt.show()
    
def logg(l):
    if l ==True:
        plt.yscale('log')
    else:
        pass

def recs(ax, inn):
    recs=f.recdays()
    for i in inn:
        ax.axvspan(recs[i].index[0], recs[i].index[-1], color='grey', alpha=0.2)


# def formatter():
#     ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
#     scale_y = 1e6
#     ticks_y = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
#     ax.yaxis.set_major_formatter(ticks_y)

    

def linep(v,l, t,size, dark, title, subtitle, source):
    fig, ax, colors, im=layout(size, dark, l)
    line(v, t, colors,ax)
    addt(fig, colors, title, subtitle, source, dark)
    # if s[0]==True:
    #     secax=sec_ax()
    # return secax
    addlogo(im, fig)
    # logg(l)
    # fig.tight_layout()
    fig

def barp(bars,l, t,size, dark, title, subtitle, source):
    fig, ax, colors, im=layout(size, dark, l)
    bar(fig,bars,t, colors,ax)
    addt(fig, colors, title, subtitle, source, dark)

    addlogo(im, fig)
    # logg(l)
    # fig.tight_layout()
    fig
























    
    
    
class eod_data():
    
    def __init__(self, apikey, fredapikey):
        
        self.apikey=apikey
        self.fredapikey=fredapikey
        self.today=dt.date.today()
        self.yesterday = self.today - dt.timedelta(days=1)
        
    def USA_eod(self):
        sp=f.clean_financials(fmp.historical_chart(self.apikey, '^GSPC', '1min'))
        spt=sp[self.today:]
        spy=sp[self.yesterday:]
        spy=spy[:self.today]
        
        nas=f.clean_financials(fmp.historical_chart(self.apikey,'^IXIC' , '1min'))
        nast=nas[self.today:]
        nasy=nas[self.yesterday:]
        nasy=nasy[:self.today]        
        
        russ=f.clean_financials(fmp.historical_chart(self.apikey,'^RUA' , '1min'))
        russt=russ[self.today:]
        russy=russ[self.yesterday:]
        russy=russy[:self.today]        
        
        djia=f.clean_financials(fmp.historical_chart(self.apikey, '^DJI', '1min'))
        djiat=djia[self.today:]
        djiay=djia[self.yesterday:]
        djiay=djiay[:self.today]        
        
        
        
        fig=linep([(spt['close']/spy['close'][-1])-1,(nast['close']/nasy['close'][-1])-1,(russt['close']/russy['close'][-1])-1,(djiat['close']/djiay['close'][-1])-1,],False,
                  ['SP 500', 'Nasdaq', 'Russel 3000', 'Dow jones ind.' ],10, False, 'Indices americanos intradia ' + str(self.today), 'Crecimiento diario en %', 'FMPCloud.io')
        
        return fig
    
    def asia_pacific_eod(self):
        sp=f.clean_financials(fmp.historical_chart(self.apikey, '^HSI', '1min'))
        spt=sp[self.today:]
        spy=sp[self.yesterday:]
        spy=spy[:self.today]
        
        nas=f.clean_financials(fmp.historical_chart(self.apikey,'IMOEX.ME' , '1min'))
        nast=nas[self.today:]
        nasy=nas[self.yesterday:]
        nasy=nasy[:self.today]        
        
        russ=f.clean_financials(fmp.historical_chart(self.apikey,'^N225' , '1min'))
        russt=russ[self.today:]
        russy=russ[self.yesterday:]
        russy=russy[:self.today]        
        
        djia=f.clean_financials(fmp.historical_chart(self.apikey, '^AORD', '1min'))
        djiat=djia[self.today:]
        djiay=djia[self.yesterday:]
        djiay=djiay[:self.today]   
        
        djiaa=f.clean_financials(fmp.historical_chart(self.apikey, '^KS11', '1min'))
        djiata=djiaa[self.today:]
        djiaya=djiaa[self.yesterday:]
        djiaya=djiaya[:self.today]        
        
        
        
        fig=linep([(spt['close']/spy['close'][-1])-1,(nast['close']/nasy['close'][-1])-1,(russt['close']/russy['close'][-1])-1,(djiat['close']/djiay['close'][-1])-1,(djiata['close']/djiaya['close'][-1])-1],False,
                  ['Heng Seng (Hong Kong)', 'MOEX (Moscú)', 'Nikkei (Tokio)', 'Australia', 'Kospi (Seúl)' ],10, False, 'Indices Asia-Pacifico intradía ' + str(self.today), 'Crecimiento diario en %', 'FMPCloud.io')
        
        return fig
    def EU_eod(self):
        sp=f.clean_financials(fmp.historical_chart(self.apikey, '^STOXX50E', '1min'))
        spt=sp[self.today:]
        spy=sp[self.yesterday:]
        spy=spy[:self.today]
        
        nas=f.clean_financials(fmp.historical_chart(self.apikey,'^N100' , '1min'))
        nast=nas[self.today:]
        nasy=nas[self.yesterday:]
        nasy=nasy[:self.today]        
        
        russ=f.clean_financials(fmp.historical_chart(self.apikey,'^FCHI' , '1min'))
        russt=russ[self.today:]
        russy=russ[self.yesterday:]
        russy=russy[:self.today]        
        
        djia=f.clean_financials(fmp.historical_chart(self.apikey, '^FTSE', '1min'))
        djiat=djia[self.today:]
        djiay=djia[self.yesterday:]
        djiay=djiay[:self.today]        
        
        djiaa=f.clean_financials(fmp.historical_chart(self.apikey, '^GDAXI', '1min'))
        djiata=djiaa[self.today:]
        djiaya=djiaa[self.yesterday:]
        djiaya=djiaya[:self.today]        
        
        
        fig=linep([(spt['close']/spy['close'][-1])-1,(nast['close']/nasy['close'][-1])-1,(russt['close']/russy['close'][-1])-1,(djiat['close']/djiay['close'][-1])-1,(djiata['close']/djiaya['close'][-1])-1],False,
                      ['Stoxx50', 'EuroNext100', 'CAC40 (Paris)', 'FTSE (Londres)', 'DAX35 (Frankfurt)' ],10, False, 'Indices Europeos principales intradia ' + str(self.today), 'Crecimiento diario en %', 'FMPCloud.io')
        
        return fig
        
        

