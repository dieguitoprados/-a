# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 17:58:36 2022

@author: diegu
"""
import datetime as dt
from dateutil.relativedelta import relativedelta
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

import plots as p
import functions_diego as f
import ovbapp as ovb

# st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.write("Options")
option=st.sidebar.selectbox("Options",('AXA Dinamico','AXA Responsable','AXA Moderado'))
logo = 'ovbb.png'
st.image(logo)
st.title(option)


if option == 'AXA Dinamico':

    lovol = yf.Ticker("0P0000XR51") # LU0861579265  
    euroz = yf.Ticker("0P0000Q27O.F") # LU0528102642
    amerigr = yf.Ticker("0P0000PNXM.F") # LU0232575059
    framnextg = yf.Ticker("0P0000XUN1.F") # LU0868490383
    fworlde = yf.Ticker("0P00000LI4.F") # LU0115769746
    bnp = yf.Ticker("0P0000YSYY.F") # LU0823422141
    framevtrends = yf.Ticker("0P0000YJLF.F") # LU0503938879
    
    lop=lovol.history(period='2y')
    loin=lovol.info
    
    eup=euroz.history(period='2y')
    euin=euroz.info
    
    amgrp=amerigr.history(period='2y')
    amgrin=amerigr.info
    
    ngenp=framnextg.history(period='2y')
    ngenin=framnextg.info
    
    worldp=fworlde.history(period='2y')
    worldin=fworlde.info
    
    bnpp=bnp.history(period='2y')
    bnpin=bnp.info
    
    evtrendp=framevtrends.history(period='1y')
    evtrendin=framevtrends.info

    s=st.selectbox('Options', ('Visión general', 'BNP Paribas Disruptive Tech', 'AXA WF Framlington Evolving Trends',
                               'Fidelity World', 'Low Volatility Equity Portfolio','American Growth','Framlington Next Generation','Eurozone Equity Portfolio' ))
    
    st.header(s)
    v=[f.normalize(lop['Close']), f.normalize(eup['Close']),
                      f.normalize(amgrp['Close']),f.normalize(ngenp['Close']),
                      f.normalize(worldp['Close']),f.normalize(bnpp['Close']),
                      f.normalize(evtrendp['Close'])]
    t=['low vol', 'EuroZone', 'American Growth', 'NextGen', 'World', 'BNP Tech', 'Megarends' ]
    title='AXA Dinámico'
    subtitle='precios medidos en EUR sin descontar comisiones'
    source='Yahoo finance'
    # fig=ovb.lineovb([f.normalize(lop['Close']), f.normalize(eup['Close']),
    #                  f.normalize(amgrp['Close']),f.normalize(ngenp['Close']),
    #                  f.normalize(worldp['Close']),f.normalize(bnpp['Close']),
    #                  f.normalize(evtrendp['Close'])], 'linear',['low vol', 'EuroZone', 'American Growth', 'NextGen', 'World', 'BNP Tech', 'Megarends' ],
    #                 10, False, 'AXA Dinámico', 'precios medidos en EUR sin descontar comisiones',
    #                 'Yahoo finance')
    # fig, ax, colors,im=ovb.layoutovb()
    # ovb.lineov([f.normalize(lop['Close']), f.normalize(eup['Close']),f.normalize(amgrp['Close']),f.normalize(ngenp['Close']),f.normalize(worldp['Close']),f.normalize(bnpp['Close']),f.normalize(evtrendp['Close'])], ['low vol', 'EuroZone', 'American Growth', 'NextGen', 'World', 'BNP Tech', 'Megarends' ], colors,ax)
    # ovb.addt(fig, colors, 'AXA Dinámico', 'precios medidos en EUR sin descontar comisiones', 'Yahoo finance')
    # ovb.addlogo(im, fig)
    # fig
    # g1='#003A65'
    g1='white'
    g2='#00B7E5'
    g3='#006666'
    g4='#8BBF18'
    g5='#CC0066'
    g6='#FFCC33'
    g7='lightgrey'
    g8='gainsboro'
    colors=[]
    colors=[g1,g2,g3,g4,g5,g6,g7,g8]
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots()  
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    im = plt.imread('ovbb.png')
    
    
    
    
    for i in range(len(v)):
        try:
            ax.plot(v[i], color=colors[i], label=t[i], linewidth=0.7, alpha=0.9)
        except: Exception
        pass
    # ax.legend(fancybox=True)    
    plt.tight_layout()
            
    # Make room below on top and bottom
    fig.subplots_adjust(top=0.825, bottom=0.15)
    c='white'
    # Add title
    fig.text(
        0, 0.92, title, 
        fontsize=15,
        fontweight="bold", 
        fontfamily="Sans Serif", color=c
    )
    # Add subtitle
    fig.text(
        0, 0.875, subtitle, 
        fontsize=12, 
        fontfamily="Sans Serif", color=c
    )
    
    # Add caption
    fig.text(
        0, 0.06, source, color='lightgrey', 
        fontsize=8, fontfamily="Sans Serif"
    )
    # Add authorship
    fig.text(
        0, 0.005, "Diego Prados. OVB Madrid 7", color='lightgrey',
        fontsize=16, fontfamily="Sans Serif"
    )
    
        # # Add line and rectangle on top.
        # fig.add_artist(lines.Line2D([0, 1], [1, 1], lw=3, color=colors[1], solid_capstyle="butt"))
        # fig.add_artist(patches.Rectangle((0, 0.975), 0.05, 0.025, color=colors[1]))
     
    newax = fig.add_axes([0.8,0.8,0.2,0.2], anchor='NE', zorder=1)
    newax.imshow(im)
    newax.axis('off')
    fig.patch.set_facecolor('#003A65')
    ax.set_facecolor('#003A65')
    plt.rcParams['figure.dpi'] = 300
    # plt.show()
    
    # fig=u.linee([f.normalize(lop['Close']), f.normalize(eup['Close']),
    #                   f.normalize(amgrp['Close']),f.normalize(ngenp['Close']),
    #                   f.normalize(worldp['Close']),f.normalize(bnpp['Close']),
    #                   f.normalize(evtrendp['Close'])],['low vol', 'EuroZone', 'American Growth', 'NextGen', 'World', 'BNP Tech', 'Megarends' ],
    #                  'AXA Dinámico', 'precios medidos en EUR sin descontar comisiones',
    #                 'Yahoo finance')
    
    st.pyplot(fig)
        
    if s == 'Visión general':
        
        c1, c2=st.columns(2)
        
        with c1:
    
            st.subheader('BNP Paribas Disruptive Tech')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F00000PXI1&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')
            st.text('')
            
            st.subheader('AXA WF Framlington Evolving Trends')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F00000PTGC&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')
            
            
            st.subheader('Fidelity World')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F0GBR04LVV&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')
        
        with c2:
        
            st.subheader('Low Volatility Equity Portfolio')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F00000PA64&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')
           
            
            st.subheader('American Growth')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F0000044UE&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')
            
            
            st.subheader('Framlington Next Generation')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F00000PCHH&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')
            
            st.subheader('Eurozone Equity Portfolio')
            st.image('https://www.morningstar.es/es/funds/WebGraph/growth10k4year.aspx?id=F00000JUYM&currencyId=EUR&investmenttype=FO&MsRestructureDate=&IMARestructureDate=&RestructureDate=&ShowCategory=1&ShowIndex=1')




































