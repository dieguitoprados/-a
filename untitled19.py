# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:25:37 2022

@author: diegu
"""
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


import classes_diego as c
import plots as p



apikey='d60d2f087ecf05f94a3b9b3df34310a9'

main=st.selectbox('APPS', ('Home', 'Stocks', 'ETFs & Indices','Cryptocurrencies','Forex', 'Fixed income', 'Commodities'))
if main == 'Home':
    ch=st.selectbox('Quick options:', ('Home', 'Wire news', 'Calendars','Main indices','Hot stocks', 'Commodities'  ))
    
    if ch=='Home':
        inde=pd.DataFrame()
        av=fmp.available_indexes(apikey)
        
        for i in range(0, len(av)):
            
        
            inde[av[i]['symbol']]=f.clean_financials(fmp.historical_price_full(apikey, av[i]['symbol'])).close
        
        
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots()  
        ax.plot(inde['^TYX'], color='limegreen', label='30 yr: '+str(inde['^TYX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^TNX'], color='green', label='10 yr: '+str(inde['^TNX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^FVX'], color='forestgreen', label='5 yr: '+str(inde['^FVX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^IRX'], color='darkgreen', label='13 wk: '+str(inde['^IRX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        # ax2=ax.twinx()
        
        # ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
        # ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
        # ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                              ncol=2, mode="expand", borderaxespad=0.)
        ax.yaxis.grid(True, color='palegreen', alpha=0.3)
        # ax2.yaxis.grid(True, color='palegreen', alpha=0.3)
        ax.xaxis.grid(True, color='palegreen', alpha=0.3)
        
        # ax.xaxis.set_major_formatter(
        #     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.set_facecolor('none')
        ax.set_xlabel('Treasury yields',  color='seagreen',
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
    
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots()  
        ax.plot(inde['^VIX'], color='limegreen', label='VIX: '+str(inde['^VIX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^VXN'], color='green', label='Nasdaq 100 Volatility Index: '+str(inde['^VXN'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^RVX'], color='forestgreen', label='Russel 3000 Volatility Index: '+str(inde['^RVX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^VVIX'], color='darkgreen', label='VVIX: '+str(inde['^VVIX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        # ax2=ax.twinx()
        
        # ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
        # ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
        # ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                              ncol=2, mode="expand", borderaxespad=0.)
        ax.yaxis.grid(True, color='palegreen', alpha=0.3)
        # ax2.yaxis.grid(True, color='palegreen', alpha=0.3)
        ax.xaxis.grid(True, color='palegreen', alpha=0.3)
        
        # ax.xaxis.set_major_formatter(
        #     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.set_facecolor('none')
        ax.set_xlabel('Volatility indexes',  color='seagreen',
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


        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots()  
        ax.plot(inde['^VIX'], color='limegreen', label='VIX: '+str(inde['^VIX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^VXN'], color='green', label='Nasdaq 100 Volatility Index: '+str(inde['^VXN'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^RVX'], color='forestgreen', label='Russel 3000 Volatility Index: '+str(inde['^RVX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        ax.plot(inde['^VVIX'], color='darkgreen', label='VVIX: '+str(inde['^VVIX'].iat[-1])+'%', linewidth=0.7, alpha=0.9)
        # ax2=ax.twinx()
        
        # ax2.plot(financials[0][1][3]['returnOnEquity']*100, color='black', label='PE ratio', linewidth=1, alpha=0.8)
        # ax2.plot(indexes['^GSPC'], color='limegreen', label='PE ratio', linewidth=1, alpha=0.5)
        # ax2.plot(indma50['^VIX'], color='yellowgreen', label='PE ratio', linewidth=2, alpha=0.8)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                              ncol=2, mode="expand", borderaxespad=0.)
        ax.yaxis.grid(True, color='palegreen', alpha=0.3)
        # ax2.yaxis.grid(True, color='palegreen', alpha=0.3)
        ax.xaxis.grid(True, color='palegreen', alpha=0.3)
        
        # ax.xaxis.set_major_formatter(
        #     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.set_facecolor('none')
        ax.set_xlabel('Volatility indexes',  color='seagreen',
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
    
    
    
    
    if ch=='Wire news':
        r=requests.get('https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=XJ0LXsOASAnkltrGDXBpxFnOxlxpBsg9').json()
        
        
        for i in range(0,len(r['results'])):
            st.header(r['results'][i]['title'])
            st.subheader(r['results'][i]['first_published_date'])
            st.markdown(r['results'][i]['url'])
            
        
    if ch == 'Calendars':
        d = st.date_input('Date', dt.datetime.now() )
        ty=st.selectbox('Calendars', ('Economic', 'Earnings', 'IPO', 'Dividends'))
        if ty == 'Economic':
            ceco=fmp.calendar.economic_calendar(apikey, )
            for i in range (0, len(ceco)):
                while ceco[i]['date'] == d:
                    st.header(str(d))
                    
        
        ce=fmp.calendar.earning_calendar(apikey)
        
        
    if ch== 'Main indices':
        
        ind=fmp.indexes(apikey)
        st.header('Americas')
        st.subheader('USA')
        for i in [58, 59]:
            st.metric(str(ind[i]['name']),str (ind[i]['price']), str(ind[i]['change'])+ ' | ' +str(ind[i]['changesPercentage'])+'%')
        # col[1].markdown(ind[][])
        
        
        
    if ch== 'Hot stocks':
        col1, col2, col3=st.columns((3))
        
        i=fmp.indexes(apikey)
        a=fmp.stock_market.actives(apikey)
        g=fmp.stock_market.gainers(apikey)
        l=fmp.stock_market.losers(apikey)
        p=fmp.stock_market.sectors_performance(apikey)
        
        col1.subheader('Gainers')
        for i in range (0,9):
            col1.markdown(g[i]['ticker']+' || '+g[i]['companyName']+' || '+'📈'+g[i]['changesPercentage']+'%')
        col2.subheader('Loosers')
        for i in range (0,9):
            col2.markdown(l[i]['ticker']+' || '+l[i]['companyName']+' || '+'📉'+l[i]['changesPercentage']+'%')
        ...
        with col3:
        
            st.subheader('Active')
            for i in range (0,9):
                st.markdown((a[i]['ticker']+' || '+a[i]['companyName']+' || '+a[i]['changesPercentage']+'%'))
            
    # if ch == 'Commodities':
    
if main == 'Stocks':



    symbol= st.text_input("stock", '')
    url= f'https://financialmodelingprep.com/image-stock/{symbol}.png'
    st.image(url)
    option=st.sidebar.selectbox("Options",('Home', 'Financials', 'Horizontal', 'Valuation', 'News',
                                           'Stats', 'Technical analysis', 'Screener', 'SEC Filings',
                                           'Insider Transactions', 'Options', 'Social Sentiment'))
    
    
    end=dt.datetime.now()
    start=[end-dt.timedelta(days=365*10)]

    prices=fmp.historical_chart(apikey, symbol, '4hour')
    p=pd.DataFrame(prices)
    p=p.set_index(p['date'])
    # fig = px.line(p, x='date', y='close', title='Price of '+symbol+' || '+"price in "+fmp.balance_sheet_statement(apikey, symbol)[0]['reportedCurrency'])
    
    # st.plotly_chart(fig)
    
    if symbol != '':
        
        if option == 'Home':
            o=fmp.company_profile(apikey, symbol)
    
            
            st.header(str(o[0]['companyName'])+' | '+str(o[0]['exchange'])+' | '+str(o[0]['symbol'])+
                      ' | ISIN:'+str(o[0]['isin'])+' | CIK:'+str(o[0]['cik']))
            st.metric('Price',str(o[0]['price'])+' '+o[0]['currency'], str(np.round(o[0]['changes'],4))+'  |  '+str(np.round(np.round(o[0]['changes'],4)/(o[0]['price']-np.round(o[0]['changes'],4))*100,4))+'%')
            st.subheader('Sector and industry: '+str(o[0]['sector'])+' | '+str(o[0]['industry'])) 
            
            fig=plt.figure(figsize=(12,5))
            plt.title('Time series of '+symbol)
            plt.xlabel('Time')
            plt.ylabel('Prices')
            
            df=pd.DataFrame(f.clean_financials(fmp.historical_price_full(apikey, symbol))        )
            df['sp']=pd.DataFrame(f.clean_financials(fmp.historical_price_full(apikey, '^GSPC'))['close']).reindex(df.index, method='bfill')
            dff=pd.DataFrame(f.clean_financials(fmp.historical_chart(apikey, '^GSPC',  '1min'))['close'])
            dff['symbol']=pd.DataFrame(f.clean_financials(fmp.historical_chart(apikey, symbol, '1min'))['close']).reindex(dff.index, method='bfill')
            # df=df.reindex(index=df.index[::-1])
            # df=df.set_index('date')

            r=st.radio('Time:', ('Intraday', 'Daily'))
            if r== 'Intraday':
                
                
                fig, ax=f.lineplot_normalised([dff['symbol']], 'Intraday price performance '+symbol[0])
                
                # plt.style.use('seaborn-darkgrid')
                # fig, ax = plt.subplots()  
                # ax.plot(dff['close']/dff['close'][0], color='forestgreen', label=symbol+': '+str(dff.symbol.iat[-1]), linewidth=0.7, alpha=0.9)
                # ax.plot(dff['symbol']/dff['symbol'][0], color='limegreen', label='S&P500: '+str(dff.close.iat[-1]), linewidth=0.7, alpha=0.9)
                # ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                #                       ncol=2, mode="expand", borderaxespad=0.)
                # ax.yaxis.grid(True, color='palegreen', alpha=0.3)
                # # ax2.yaxis.grid(True, color='palegreen', alpha=0.3)
                # ax.xaxis.grid(True, color='palegreen', alpha=0.3)
                
                # # ax.xaxis.set_major_formatter(
                # #     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
                # ax.set_facecolor('none')
                # ax.set_xlabel('Treasury yields',  color='seagreen',
                #               weight='bold')
                # # ax.legend()
                # ax.text(
                #         0.5,
                #         0.5,
                #         'Greenfield Capital Advisors Group S.L.',
                #         horizontalalignment='center',
                #         verticalalignment='top',color = 'black', weight='bold',
                #         fontsize=18, alpha=0.5,
                #         transform=ax.transAxes)
                # fig.tight_layout()
    
                
                st.pyplot(fig)            
            if r== 'Daily':
            
                plt.style.use('seaborn-darkgrid')
                fig, ax = plt.subplots()  
                ax.plot((df['close']/df['close'][0])-1, color='forestgreen', label=symbol+': '+str(df.close.iat[-1]), linewidth=0.7, alpha=0.9)
                ax.plot(df['sp']/df['sp'][0]-1, color='limegreen', label='S&P500: '+str(df.sp.iat[-1]), linewidth=0.7, alpha=0.9)
                ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                                      ncol=2, mode="expand", borderaxespad=0.)
                ax.yaxis.grid(True, color='palegreen', alpha=0.3)
                # ax2.yaxis.grid(True, color='palegreen', alpha=0.3)
                ax.xaxis.grid(True, color='palegreen', alpha=0.3)
                
                # ax.xaxis.set_major_formatter(
                #     mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
                ax.set_facecolor('none')
                ax.set_xlabel(symbol+' Price performance vs. S&P500',  color='seagreen',
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
            
            
            st.subheader('Company profile')
            st.markdown(str(o[0]['description']))
            st.subheader('Website')
            st.markdown(o[0]['website'])
            # st.subheader('')
            # st.markdown(str(o[0]['']))
            # st.subheader('')
            # st.markdown(str(o[0]['']))
            # st.subheader('')
            # st.markdown(str(o[0]['']))
        if option== 'Horizontal':
            opti=st.selectbox('Choose:', ('Main', 'Balance Sheet', 'Income Statement', 'Cash Flow'))
            
            if opti=='Main':
            
                rating=fmp.historical_rating(apikey, symbol, 15)
                r=pd.DataFrame(rating)
                r=r.set_index('date')
                r=r[r.columns[2:]]
                rc=r.columns
                r=r.transpose()
                r=r[r.columns[::-1]]
                st.dataframe(r)
                opt=st.selectbox('Plot', (rc))
                st.bar_chart(r.loc[opt])
                
            if opti=='Balance Sheet':
            
                bg=fmp.balance_sheet_statement_growth(apikey, symbol, 15)
                bgg=pd.DataFrame(bg)
                bgg=bgg.set_index('date')
                bgg=bgg[bgg.columns[2:]]
                bgc=bgg.columns
                bgg=bgg.transpose()
                bgg=bgg[bgg.columns[::-1]]
                st.dataframe(bgg)
                opt=st.selectbox('Plot', bgc)
                st.bar_chart(bgg.loc[opt])
                
            if opti=='Income Statement':
            
                bg=fmp.income_statement_growth(apikey, symbol, 15)
                bgg=pd.DataFrame(bg)
                bgg=bgg.set_index('date')
                bgg=bgg[bgg.columns[2:]]
                bgc=bgg.columns
                bgg=bgg.transpose()
                bgg=bgg[bgg.columns[::-1]]
                st.dataframe(bgg)
                opt=st.selectbox('Plot', bgc)
                st.bar_chart(bgg.loc[opt])
                
            if opti=='Balance Sheet':
            
                bg=fmp.cash_flow_statement(apikey, symbol, 15)
                bgg=pd.DataFrame(bg)
                bgg=bgg.set_index('date')
                bgg=bgg[bgg.columns[2:]]
                bgc=bgg.columns
                bgg=bgg.transpose()
                bgg=bgg[bgg.columns[::-1]]
                st.dataframe(bgg)
                opt=st.selectbox('Plot', bgc)
                st.bar_chart(bgg.loc[opt])
            
            
            
        if option == 'Financials':
            
            data=st.sidebar.selectbox('Choose',('Balance Sheet','Income Statement','Cashflow Statement'))
            
            if data == 'Balance Sheet':
                
                time=st.radio('Time Interval:',( 'quarter','annual'))
                
                balance_sheets=fmp.company_valuation.balance_sheet_statement(apikey, symbol, time, 30)                
                # bsar=fmp.balance_sheet_statement_as_reported(apikey, symbol, 'quarter', 30)

                # bb=pd.DataFrame(bsar)
                # bb=bb.transpose()

                # ii=pd.DataFrame(fmp.income_statement_as_reported(apikey, symbol, 'quarter', 30))
                # ii=ii.transpose()

                balance_sheet=pd.DataFrame(balance_sheets)
                balance_sheet=balance_sheet.set_index('date')
                bsc=balance_sheet[balance_sheet.columns[7:]]
                bsc=bsc.columns
                balance_sheet=balance_sheet.transpose()
                balance_sheet=balance_sheet[balance_sheet.columns[::-1]]
                dates=pd.DataFrame(balance_sheet.columns)
    
                st.header("Balance Sheet")
                st.markdown('Currency: '+str(balance_sheets[0]['reportedCurrency']))
                st.subheader("Current Assets")
                current_ass = balance_sheet.iloc[7:14,:]
                st.dataframe(current_ass)            
                st.subheader("Non Current Assets")            
                non_curr_ass = balance_sheet.iloc[15:24,:]
                st.dataframe(non_curr_ass)             
                st.subheader("Current Liabilities")            
                curr_liab = balance_sheet.iloc[25:30,:]
                st.dataframe(curr_liab)             
                st.subheader("Non Current Liabilities")            
                non_curr_liab = balance_sheet.iloc[31:38,:]
                st.dataframe(non_curr_liab)             
                st.subheader("Equity")            
                equity = balance_sheet.iloc[38:51,:]
                st.dataframe(equity) 
                
                opt=st.multiselect('Histogram', (bsc))
                plt.style.use('seaborn-darkgrid')

                fig, ax = plt.subplots(figsize=(8,5))
                a=cm.Greens(np.linspace(0,1,len(opt)))
                width=0.9/len(opt)
                x=np.arange(0, len(balance_sheet.loc[opt[1]]))
                
                if (len(opt)%2):
                    try:
                        bars=plt.bar(x+(len(opt)-1)*width/2, balance_sheet[opt[1]], width)
                        bars=plt.bar(x+(len(opt)-1)*width/2, balance_sheet[opt[2]], width)
                        bars=plt.bar(x+(len(opt)-1)*width/2, balance_sheet[opt[3]], width)
                        bars=plt.bar(x-(len(opt)-1)*width/2, balance_sheet[opt[4]], width)
                        bars=plt.bar(x+(len(opt)-1)*width/2, balance_sheet[opt[5]], width)
                        bars=plt.bar(x-(len(opt)-1)*width/2, balance_sheet[opt[6]], width)
                        bars=plt.bar(x+(len(opt)-1)*width/2, balance_sheet[opt[7]], width)
                        bars=plt.bar(x-(len(opt)-1)*width/2, balance_sheet[opt[8]], width)
                        bars=plt.bar(x-(len(opt)-1)*width/2, balance_sheet[opt[9]], width)
                        bars=plt.bar(x-(len(opt)-1)*width/2, balance_sheet[opt[10]], width)
                    except: Exception
                    pass
                else:
                    try:
                        plt.bar(x, opt[1])
                        plt.bar(x+(len(opt)-1)*width/2, opt[2])
                        plt.bar(x-(len(opt)-1)*width/2, opt[3])
                        plt.bar(x+(len(opt)-2)*width/2, opt[4])
                        plt.bar(x-(len(opt)-2)*width/2, opt[5])
                        plt.bar(x+(len(opt)-3)*width/2, opt[6])
                        plt.bar(x-(len(opt)-3)*width/2, opt[7])
                        plt.bar(x+(len(opt)-4)*width/2, opt[8])
                        plt.bar(x-(len(opt)-4)*width/2, opt[9])
                    except: Exception
                    pass
                    
                ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                      ncol=2, mode="expand", borderaxespad=0.)
                plt.xticks(rotation = 80)
                # Axis formatting.
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.tick_params(bottom=False, left=False)
                ax.set_axisbelow(True)
                ax.yaxis.grid(False)
                ax.xaxis.grid(False)
                
                ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
                scale_y = 1e6
                ticks_y = matplotlib.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
                ax.yaxis.set_major_formatter(ticks_y)
                ax.set_ylabel('In millions', color='darkgreen')
                # ax.set_xlabel(plt.legend())
                ax.set_xlabel(symbol+' Balance Sheet statement ',  color='darkgreen',
                             weight='bold')
                # ax.legend()
                ax.set_facecolor("white")
                fig.text(
                        0.75,
                        0,
                        'Greenfield Capital Advisors Group S.L.',
                        color='black',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()
                st.pyplot(fig)

                
            if data == 'Income Statement':
                time=st.radio('Time Interval:',( 'quarter','annual'))
                
                income_statements=fmp.company_valuation.income_statement(apikey, symbol, time, 30)
    
                income_statement=pd.DataFrame(income_statements)
                income_statement=income_statement.set_index(income_statement['calendarYear']+' '+income_statement['period'])
                income_statement=income_statement.transpose()
                income_statement=income_statement[income_statement.columns[::-1]]
                dates=pd.DataFrame(income_statement.columns)
                # dq = [dates[i] for i in range(len(dates)) if i % 2 != 0]                
                
    
                st.header("Income Statement")
                st.markdown('Currency: ' + income_statements[0]['reportedCurrency'])
                st.subheader("Revenues")
                revenues=income_statement.iloc[8:11,:]
                st.dataframe(revenues)
                st.subheader("Operating Expenses & Income")
                opex=income_statement.iloc[12:19,:]
                opex.loc['operatingIncome']=income_statement.loc['operatingIncome']
                st.dataframe(opex)
                st.subheader("EBITDA")
                ebitda=income_statement.iloc[20:23,:]
                st.dataframe(ebitda)
                st.subheader("EBT")
                ebt=income_statement.iloc[26:28,:]
                st.dataframe(ebt)
                st.subheader("Net Income")
                net_inc=income_statement.iloc[29:31,:]
                st.dataframe(net_inc)
                
                opt=st.selectbox('Histogram', ('revenue', 'costOfRevenue', 'grossProfit', 'researchAndDevelopmentExpenses',
                                               'generalAndAdministrativeExpenses', 'sellingAndMarketingExpenses', 'sellingGeneralAndAdministrativeExpenses',
                                               'otherExpenses', 'operatingExpenses', 'operatingIncome', 'costAndExpenses',
                                               'interestIncome', 'interestExpense', 'depreciationAndAmortization', 'ebitda', 'totalOtherIncomeExpensesNet',
                                               'incomeBeforeTax', 'incomeTaxExpense', 'netIncome', 'eps', 'epsdiluted', 'weightedAverageShsOut','weightedAverageShsOutDil' ))

                fig = plt.figure()
                ax = fig.add_axes([0,0,1,1])
                plt.title(opt)
                ax.bar(dates[0],income_statement.loc[opt])
                # plt.xticks(dq)
                # plt.yscale('log')
                st.pyplot(fig)
            
    # fmp.enterprise_values(apikey, symbol)
            
            if data == 'Cashflow Statement':
                time=st.radio('Time Interval:',( 'quarter','annual'))
                cashflow_statements=fmp.company_valuation.cash_flow_statement(apikey, symbol,time, 30)
    
                cashflow_statement=pd.DataFrame(cashflow_statements)
                cashflow_statement=cashflow_statement.set_index('date')
                cashflow_statement=cashflow_statement.transpose()
                cashflow_statement=cashflow_statement[cashflow_statement.columns[::-1]]
                dates=pd.DataFrame(cashflow_statement.columns)
    
                
                st.header("Cashflow Statement")
                st.markdown('Currency: ' + cashflow_statements[0]['reportedCurrency'])
    
                st.dataframe(cashflow_statement.iloc[7:,:])
                
                # comp=fmp.stock_screener(apikey, industry='Communication Equipment', limit=600)
                # c=pd.DataFrame(comp)
                # c=c[c.exchangeShortName.isin(['NYSE','NASDAQ'])]
                # ratios=pd.DataFrame(index=(fmp.financial_ratios(apikey, symbol, 'quarter', 1)[0].keys()))
                # for stock in c['symbol']:
                #     try:
                    
                #         ratios[stock]=fmp.financial_ratios(apikey, stock, 'quarter', 1)[0].values()
                #     except Exception:
                #         continue
                    
                #     p=pd.DataFrame()
                # for i in range(3, len(ratios)):
                #     print(np.mean(ratios.iloc[i]))
                #     # for i in range(0,len(c)):
                        # ratios[stock]=pd.DataFrame(fmp.financial_ratios(apikey, stock, 'quarter', 1)[0].values())
                # opt=st.selectbox('Histogram', (
                # c=c[us]
                
        if option == 'Valuation':
    
            balance_sheets=fmp.company_valuation.balance_sheet_statement(apikey, symbol, 'quarter', 20)
                    
            balance_sheet=pd.DataFrame(balance_sheets)
            balance_sheet=balance_sheet.set_index('date')
            balance_sheet=balance_sheet.transpose()
            balance_sheet=balance_sheet[balance_sheet.columns[::-1]]
            dates=pd.DataFrame(balance_sheet.columns)
    
            
            income_statements=fmp.company_valuation.income_statement(apikey, symbol, 'quarter')
    
            income_statement=pd.DataFrame(income_statements)
            income_statement=income_statement.set_index('date')
            income_statement=income_statement.transpose()
            income_statement=income_statement[income_statement.columns[::-1]]
    
            cashflow_statements=fmp.company_valuation.cash_flow_statement(apikey, symbol, 'quarter')
    
            cashflow_statement=pd.DataFrame(cashflow_statements)
            cashflow_statement=cashflow_statement.set_index('date')
            cashflow_statement=cashflow_statement.transpose()
            cashflow_statement=cashflow_statement[cashflow_statement.columns[::-1]]
            
            opt=st.selectbox('Options', ('Compare','Liquidity & Solvency','Profitability & Efficiency','Valuation', 'Discounted Cash Flow'))
            ls=pd.DataFrame()
            ls['index']=dates
            ls=ls.set_index('index')
            ps=pd.DataFrame()        
            
            data=pd.DataFrame()
            data['index']=dates
            data=data.set_index('index')
            
            #Data
            dex=(income_statement.loc['costOfRevenue']+income_statement.loc['operatingExpenses']-income_statement.loc['depreciationAndAmortization'])/365
            price=fmp.stock_time_series.quote_short(apikey, symbol)
            # avg_inv=
            
            #Activity Ratios
            # ls['Inventary turnover']=
            
            # Liquidity 
            ls['Current ratio']=balance_sheet.loc['totalCurrentAssets']/balance_sheet.loc['totalCurrentLiabilities']
            ls['Quick ratio']=(balance_sheet.loc['cashAndShortTermInvestments']+balance_sheet.loc['netReceivables'])/balance_sheet.loc['totalCurrentLiabilities']
            ls['Cash ratio']=balance_sheet.loc['cashAndShortTermInvestments']/balance_sheet.loc['totalCurrentLiabilities']
            ls['Defensive interval']=(balance_sheet.loc['cashAndShortTermInvestments']+balance_sheet.loc['netReceivables'])/dex
            #Solvency
            ls['Debt to assets']=balance_sheet.loc['totalLiabilities']/balance_sheet.loc['totalAssets']
            ls['Debt to capital']=balance_sheet.loc['totalLiabilities']/(balance_sheet.loc['totalStockholdersEquity']+balance_sheet.loc['totalLiabilities'])
            ls['Debt to equity']=balance_sheet.loc['totalLiabilities']/balance_sheet.loc['totalStockholdersEquity']
            ls['Leverage ratio']=balance_sheet.loc['totalAssets']/balance_sheet.loc['totalStockholdersEquity']
            ls['FFO to Debt']=(income_statement.loc['netIncome']+income_statement.loc['depreciationAndAmortization']-income_statement.loc['interestIncome'])/balance_sheet.loc['totalLiabilities']
            
            
            #Coverage
            ls['Interest coverage']=(income_statement.loc['ebitda']-income_statement.loc['depreciationAndAmortization'])/(income_statement.loc['interestExpense']-income_statement.loc['interestIncome'])
            ls['EBIT interest coverage']=(income_statement.loc['ebitda']-income_statement.loc['depreciationAndAmortization'])/income_statement.loc['interestExpense']
            ls['EBITDA interest coverage']=income_statement.loc['ebitda']/income_statement.loc['interestExpense']
            ls['FFO interest coverage']=(income_statement.loc['netIncome']+income_statement.loc['depreciationAndAmortization']-income_statement.loc['interestIncome'])/income_statement.loc['interestExpense']
            
            
            #Profitability(margenes-returns-)
            ls['Gross profit margin']=income_statement.loc['grossProfitRatio']
            ls['Operating Margin']=income_statement.loc['operatingIncomeRatio']
            ls['EBT Margin']=income_statement.loc['incomeBeforeTaxRatio']
            ls['Net profit margin']=income_statement.loc['netIncomeRatio']
            
            ls['Operating ROA']=income_statement.loc['operatingIncome']/balance_sheet.loc['totalAssets']
            ls['ROA']=income_statement.loc['netIncome']/balance_sheet.loc['totalAssets']#average
            ls['ROTA']=(income_statement.loc['ebitda']-income_statement.loc['depreciationAndAmortization'])/balance_sheet.loc['totalAssets']
            ls['ROE']=income_statement.loc['netIncome']/balance_sheet.loc['totalEquity']
            
            #Valuation
            
            
            rats=fmp.financial_ratios(apikey, symbol, 'quarter', 20)
            rf=pd.DataFrame(rats)
            rf=rf.set_index('date')
            rf=rf[rf.columns[2:]]
            rc=rf.columns
            rf=rf.transpose()
            rf=rf[rf.columns[::-1]]
            
            
        
            if opt == 'Compare':
                
                # st.set_option('deprecation.showPyplotGlobalUse', False)
                
                fmp.discounted_cash_flow(apikey, symbol)
                fmp.enterprise_values(apikey, symbol, 'quarter', 20)
                lp=fmp.historical_daily_discounted_cash_flow(apikey, symbol, 300)
                st.subheader("Main Ratios")    
                st.dataframe(rf)
                ox=st.multiselect('Plot:', rf.index)
                
                fig=plt.figure()
                
                # for element in ox:
                for i in range(0, len(ox)):
                         
                        plt.figure(figsize=(12,5))
                        plt.title('Time series of '+ox[i]+' | '+symbol)
                        plt.xlabel('Time')
                        plt.ylabel('')
                        # plt.plot(self.data_table['date'],self.data_table['price2'], self.data_table['price1'])
                        ax = plt.gca()
                        ax = rf.loc[ox[i]].plot(kind='line', x=rf.columns, ax=ax, grid=True, label=symbol+'s '+ox[i])
                        ax.legend(loc=2)
                        st.pyplot()

                
            if opt == 'Liquidity & Solvency':
                l=ls.transpose()            
                li=l.iloc[0:4,:]
                lit=l.iloc[0:3,:].transpose()
                so=l.iloc[4:9,:]
                sot=so.transpose()
                st.subheader('Liquidity')
                st.dataframe(li)
                st.subheader('Solvency')
                st.dataframe(so)
                
                pl=st.selectbox('Plot', ('Liquidity', 'Solvency'))
                if pl == 'Liquidity':
                    fig=plt.figure(figsize=(12,5))
                    plt.title('Liquidity ratios')
                    plt.xlabel('Time')
                    # plt.plot(self.data_table['date'],self.data_table['price2'], self.data_table['price1'])
                    ax = plt.gca()
                    for elements in lit:
                        elements=lit[elements].plot(kind='line', ax=ax, grid=True, label=elements)
                        elements.legend(loc=2)
                    # plt.yscale('log')    
    
                    st.pyplot(fig)
                if pl == 'Solvency':
                    fig=plt.figure(figsize=(12,5))
                    plt.title('Solvency ratios')
                    plt.xlabel('Time')
                    # plt.plot(self.data_table['date'],self.data_table['price2'], self.data_table['price1'])
                    ax = plt.gca()
                    for elements in sot:
                        elements=sot[elements].plot(kind='line', ax=ax, grid=True, label=elements)
                        elements.legend(loc=2)
                    # plt.yscale('log')    
    
                    st.pyplot(fig)
    
                
                # na=st.multiselect('Plot', rc)
                # st.line_chart(rf.loc[na])
            if opt=='Profitability & Efficiency':
                o=ls.transpose()
                
                i=o.iloc[9:12]
                n=o.iloc[16:21,:]
                l=o.iloc[13:16,:]
                st.subheader('Interest coverage')
    
                st.dataframe(i)
                st.subheader('Efficiency')
                st.dataframe(n)
                st.subheader('Profitability')
                st.dataframe(l)
            if opt== 'Discounted Cash Flow':
                dcf=fmp.discounted_cash_flow(apikey, symbol)
                dcfday=fmp.historical_daily_discounted_cash_flow(apikey, symbol,550)
                
                dcfdf=pd.DataFrame(dcfday)
                p=fmp.historical_price_full(apikey, symbol)
        if option == 'Technical analysis':
            st.subheader('Technical analysis')
            p=fmp.historical_price_full(apikey, symbol, 600, )
            prices=pd.DataFrame(p)
            # prices['date']=pd.to_datetime(prices['date'])
            prices=prices.set_index('date')
            # pricess=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo').json()['Time Series (5min)']
            l=prices.index
            l=l.transpose()
            # i=st.selectbox('Intraday'('4H', '1D', '1W', '1M'))
            
            sma=pd.DataFrame()
            sma['date']=l[::-1]
            sma=sma.set_index('date')

            sma['sma50']=prices['close'].rolling(window=50).mean()
            sma100=prices['close'].rolling(window=100).mean()
            sma200=prices['close'].rolling(window=200).mean()
            
            # sma50=fmp.technical_indicators(apikey, symbol,50, 'sma')
            # sma100=fmp.technical_indicators(apikey, symbol,100, 'sma')
            # sma200=fmp.technical_indicators(apikey, symbol,200, 'sma')
            
            
            
            fig = go.Figure(go.Candlestick(x=l,
                                           open=prices['open'],
                                           high= prices['high'],
                                           low=prices['low'],
                                           close=prices['close'],
                                           name=symbol
                                           )
                            )
            
            fig.add_trace(go.Scatter(x=l, 
                         y=sma['sma50'], 
                         opacity=0.7, 
                         line=dict(color='blue', width=2), 
                         name='MA 50'))
            fig.add_trace(go.Scatter(x=l, 
                                     y=sma200, 
                                     opacity=0.7, 
                                     line=dict(color='green', width=2), 
                                     name='MA 200'))
            
            
            st.plotly_chart(fig,use_container_width = True)
                        
        
        if option == 'Stats':
            prices=pd.DataFrame(fmp.historical_price_full(apikey, symbol))
            rr=pd.DataFrame()
            prices=prices.set_index('date')
            rr['Values']=None
            rr=rr.transpose()
            rr['Mean']=np.mean(prices['changePercent'])
            rr['Median']=np.median(prices['changePercent'])
            rr['Standard deviation']=np.std(prices['changePercent'])
            rr['Beta']=fmp.company_profile(apikey, symbol)[0]['beta']
            rr['Skewness']=scipy.stats.skew(prices['changePercent'])
            rr['Kurtosis']=scipy.stats.kurtosis(prices['changePercent'])
            rr['Sharpe']=rr['Mean'] / rr['Standard deviation'] * np.sqrt(252)
            rr['VaR 95%']=np.percentile(prices['changePercent'],5)
            rr['CVaR 95%']= np.mean(prices['changePercent'][prices['changePercent'] <= np.percentile(prices['changePercent'],5)])
            
            
            nb_decimals = 4
            plot_str = 'mean: ' + str(np.round(rr['Mean']['Values'],nb_decimals))\
                + ' | median: ' + str(np.round(rr['Median']['Values'],nb_decimals))\
                + ' | std dev: ' + str(np.round(rr['Standard deviation']['Values'],nb_decimals))\
                + ' | skewness: ' + str(np.round(rr['Skewness']['Values'],nb_decimals)) + '\n'\
                + 'kurtosis: ' + str(np.round(rr['Kurtosis']['Values'],nb_decimals))\
                + ' | Sharpe annual: ' + str(np.round(rr['Sharpe']['Values'],nb_decimals))\
                + ' | VaR 95%: ' + str(np.round(rr['VaR 95%']['Values'],nb_decimals))\
                + ' | CVaR 95%: ' + str(np.round(rr['CVaR 95%']['Values'],nb_decimals))
                
            # ri=pd.DataFrame()
            # ri['Standard Deviation']=None
            # ri['Standard Deviation']=rr.loc(['Standard deviation'])
            # rr=rr.transpose()
            # counts, bins = np.histogram(prices['changePercent'], bins=range(0, 60, 5))
            # bins = 0.5 * (bins[:-1] + bins[1:])
            
            # fig = px.express.bar(x=bins, y=counts, labels={'x':f'Histogram for {symbol} daily returns', 'y':'count'})
            # fig.show()
            
            # fig = px.histogram(prices['changePercent'], x=f'Histogram for {symbol} daily returns')
            # st.bar_chart(prices['changePercent'], 900, 400, True)
            
            fig=plt.figure()
            plt.hist(prices['changePercent'],bins=120)
            plt.title(symbol+' Daily Returns')
            plt.xlabel(plot_str)
            
            st.pyplot(fig)
            
            
            # rr['CVaR 95%'] = np.mean(prices['close'][prices['close'] <= rr['VaR 95%']])
            st.subheader('Risk Metrics')
            # st.markdown('Mean is:'+np.round(rr['Standard deviation'],4)+'')
            st.dataframe(rr)
        if option == 'Social Sentiment':
            lol=st.selectbox('Options', ('Stocktwits','Twitter', 'Reddit', 'Google Trends'))
            if lol == 'Stocktwits':
                nft='NFT'
                
        if option== 'News':
            select=st.selectbox('Options', ('Press releases', 'News and articles'))
            news=fmp.stock_news(apikey, symbol, 20)            
            press=fmp.press_releases(apikey, symbol, 20)
            if select == 'News and articles':
    
                st.image(news[0]['image'])
                for i in range(0,len(news)):
                    st.subheader('*'+news[i]['site']+'*'+' | '+news[i]['title'])
                    st.markdown(news[i]['text'])
                    st.markdown(news[i]['publishedDate']+' | '+news[i]['url'])
                    
            if select== 'Press releases':
                st.image(news[2]['image'])
                for i in range(0, len(press)):
                    st.subheader(press[i]['title']+' | '+press[i]['date'])
                    st.markdown(press[i]['text'])
                    
                    
        if option == 'SEC Filings':
            year=st.number_input('Year', 2013, 2022)
            Q=st.selectbox('Quarter', ('Q1', 'Q2', 'Q3', 'Q4'))
            filings=fmp.sec_filings(apikey, symbol)
            # for i in range(0,len(filings)):
            #     st.selectbox('Forms', (filings[i]['type']+' | '+filings[i]['acceptedDate']))
            # st.markdown("""
            # <embed src="https://www.sec.gov/Archives/edgar/data/88205/000008820522000013/0000088205-22-000013-index.htm" width="400" height="400">
            # """, unsafe_allow_html=True  )      
            # cf=fmp.form_13f(apikey, fmp.company_profile(apikey, symbol)['cik'].values())
            j=requests.get(f'https://fmpcloud.io/api/v4/financial-reports-json?symbol={symbol}'+f'&year={year}'+f'&period={Q}'+f'&apikey={apikey}').json()
            # t=requests.get(f'https://fmpcloud.io/api/v4/financial-reports-json?symbol={symbol}'+f'&year=2020&period=Q1&apikey={apikey}').text()
            opt=st.selectbox('Topic', j.keys())
            for i in range (0,len(j[opt])):
                opti=st.markdown(j[opt][i])
                
                
        if option=='Insider Transactions':
            ins=fmp.insider_trading(apikey, symbol, limit=100)
            ni=pd.DataFrame(ins)
    
            fmp.commodities.commodities_list(apikey)
            for i in range(0, len(ni)):
                st.markdown(ni['transactionDate'][i]+' | '+ni['reportingName'][i]+' | '+ni['typeOfOwner'][i]+' | '+str(ni['securitiesOwned'][i])+' | '+ni['transactionType'][i]+' | '+ni['acquistionOrDisposition'][i]+' | '+str(ni['securitiesTransacted'][i])+' | '+str(ni['price'][i])+' | '+ni['securityName'][i])
            # for element in j:
    
                # st.markdown(element)
                # for elements in j[element]:
                #     st.markdown(elements)