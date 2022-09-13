# -*- coding: utf-8 -*-
"""
Created on Thu May  5 01:14:22 2022

@author: diegu
"""
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
from scipy.stats import skew, kurtosis, chi2, linregress
from scipy.stats import norm
import matplotlib
from tqdm import tqdm
import matplotlib.cm as cm


import functions_diego as f
import plots as p



class get_data():
    
    def __init__(self, apikey):
        
        self.apikey=apikey
        # self.stocks=stocks
        # self.lenst=len(self.stocks)
        self.financials=[]
        self.price=[]
        self.annual=bool()
        self.dates=pd.DataFrame()
        self.price_ratios=[]
        
        self.plotin=None

        self.sp=fmp.sp500_constituent(apikey)
        self.sp_fin=[]
        self.sp_rat=pd.DataFrame(index=fmp.financial_ratios_ttm(apikey, 'MMM')[0].keys())
        
        
        
        

        
    def get_financials(self, stocks): 
        self.stocks=stocks
        for i in tqdm(range(0,len(self.stocks)), desc = 'Retrieving financials'):
            try:
                self.financials.append(list())
                self.financials[i].append(self.stocks[i])
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(fmp.quote(self.apikey, self.stocks[i])[0]['name'])
                self.financials[i][1].append(f.clean_financials(fmp.balance_sheet_statement(self.apikey, self.stocks[i],'quarter', 15)))
                self.financials[i][1].append(f.clean_financials(fmp.income_statement(self.apikey, self.stocks[i],'quarter', 15)))
                self.financials[i][1].append(f.clean_financials(fmp.cash_flow_statement(self.apikey, self.stocks[i],'quarter', 15)))
                self.financials[i][1].append(f.clean_financials(fmp.financial_ratios(self.apikey, self.stocks[i],period='quarter',limit=15)))
                self.financials[i][2].append(f.clean_financials(fmp.balance_sheet_statement(self.apikey, self.stocks[i],'annual', 15)))
                self.financials[i][2].append(f.clean_financials(fmp.income_statement(self.apikey, self.stocks[i],'annual', 15)))
                self.financials[i][2].append(f.clean_financials(fmp.cash_flow_statement(self.apikey, self.stocks[i],'annual', 15)))
                self.financials[i][2].append(f.clean_financials(fmp.financial_ratios(self.apikey, self.stocks[i],period='annual',limit=15)))
                self.financials[i][3].append(f.ttm(f.clean_financials(fmp.balance_sheet_statement(self.apikey, self.stocks[i],'quarter', 15))))
                self.financials[i][3].append(f.ttm(f.clean_financials(fmp.income_statement(self.apikey, self.stocks[i],'quarter', 15))))
                self.financials[i][3].append(f.ttm(f.clean_financials(fmp.cash_flow_statement(self.apikey, self.stocks[i],'quarter', 15))))
                
            
            
            except Exception:
                pass

        return self.financials       
    
    def sp_financials(self):
        for i in tqdm(range(0,len(self.sp)), desc = 'Retrieving financials'):
            try:
                self.sp_fin.append(list())
                self.sp_fin[i].append(self.sp[i]['symbol'])
                self.sp_fin[i].append(self.sp[i]['name'])
                self.sp_fin[i].append(self.sp[i]['sector'])
                self.sp_fin[i].append(self.sp[i]['subSector'])
                self.sp_fin[i].append(f.clean_financials(pd.DataFrame(fmp.balance_sheet_statement(self.apikey, self.sp[i]['symbol']))))
                self.sp_fin[i].append(f.clean_financials(pd.DataFrame(fmp.income_statement(self.apikey, self.sp[i]['symbol']))))
                self.sp_fin[i].append(f.clean_financials(pd.DataFrame(fmp.cash_flow_statement(self.apikey, self.sp[i]['symbol']))))
                self.sp_fin[i].append(pd.DataFrame(fmp.financial_ratios_ttm(self.apikey, self.sp[i]['symbol'])))
            except: Exception
            pass
        return self.sp_fin
    def sp_ratios(self):
        for i in tqdm(range(0,len(self.sp)), desc = 'Retrieving financials'):
            try:
                self.sp_rat[self.sp[i]['symbol']]=pd.DataFrame(fmp.financial_ratios_ttm(self.apikey, self.sp[i]['symbol'])).transpose()
            except Exception:
                pass
        cat=pd.DataFrame(index=('sector', 'industry'))
        for i in range(len(self.sp)):
            cat[self.sp[i]['symbol']]=self.sp[i]['sector'], self.sp[i]['subSector']
        cat=cat.transpose()
        
        self.sp_rat=self.sp_rat.transpose()
        self.sp_rat['industry']=cat['industry']
        self.sp_rat['sector']=cat['sector']
        self.sp_rat=self.sp_rat.replace('None', 0)
        self.sp_rat=self.sp_rat.fillna( 0)
        return self.sp_rat
     
    
    def get_price(self, stocks):
        self.stocks=stocks
        for i in tqdm(range(0,len(self.stocks)), desc = 'Retrieving prices'):
            try:
                self.price.append(list())
                self.price[i].append(self.stocks[i])
                self.price[i].append(f.clean_financials(fmp.historical_price_full(self.apikey, self.stocks[i])))
                self.price[i].append(f.clean_financials(fmp.historical_chart(self.apikey, self.stocks[i], '1min')))
                self.financials[i][4].append(self.financials[i][3][0].reindex(self.price[i][1].index,method='ffill').dropna())
                self.financials[i][4].append(self.financials[i][3][1].reindex(self.price[i][1].index,method='ffill').dropna())
                self.financials[i][4].append(self.financials[i][3][2].reindex(self.price[i][1].index,method='ffill').dropna())
            
            except Exception:
                pass            
        return self.price
    def get_price_ratios(self):
        for i in range(0, len(self.stocks)):
            i
    
            
    def hist_inc(self):
        for i in range(0, len(self.financials)):
            try:
                plt.style.use('seaborn-darkgrid')

                fig, ax = plt.subplots(figsize=(8,5))
                
                # Save the chart so we can loop through the bars below.
                    
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='#008037',height=self.financials[i][1][1]['revenue'],label='revenue',tick_label=self.financials[i][1][1].index.strftime('%d/%m/%Y'))
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='forestgreen',height=self.financials[i][1][1]['grossProfit'],label='grossProfit')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='#7ED957',height=self.financials[i][1][1]['ebitda'],label='ebitda')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='#C9E265',height=self.financials[i][1][1]['netIncome'],label='netIncome')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() -3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                    
                    


                ax.legend()
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
                ax.set_ylabel('Income in millions', color='darkgreen')
                # ax.set_xlabel(plt.legend())
                ax.set_xlabel(self.stocks[i]+' Income statement ',  color='darkgreen',
                             weight='bold')
                # ax.legend()
                ax.set_facecolor("white")
                ax.text(
                        0.75,
                        0,
                        'Greenfield Capital Advisors Group S.L.',
                        color='black',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()

            except Exception:
                pass
    def expenses(self):
        for i in range(0, len(self.financials)):
            try:
                plt.style.use('seaborn-darkgrid')

                fig, ax = plt.subplots()
                
                # Save the chart so we can loop through the bars below.
                    
                bars=ax.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='lime',height=self.financials[i][1][1]['costOfRevenue'],label='costOfRevenue',tick_label=self.financials[i][1][1].index)
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                    
                bars=ax.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='seagreen',height=self.financials[i][1][1]['sellingGeneralAndAdministrativeExpenses'],label='sellGen&Admin')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                    
                bars=ax.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='limegreen',height=self.financials[i][1][1]['researchAndDevelopmentExpenses'],label='R&D')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=ax.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='forestgreen',height=self.financials[i][1][1]['netIncome'],label='netIncome')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() -3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )

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

                # ax.set_xlabel(plt.legend())
                ax.set_ylabel('Income', labelpad=15, color='darkgreen')
                ax.set_xlabel(self.stocks[i]+' Income statement ',  color='darkgreen',
                             weight='bold')
                # ax.legend()
                ax.set_facecolor("white")
                ax.text(
                        0.75,
                        0.02,
                        'Greenfield Capital: Diego Prados',
                        color='black',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()
                plt.savefig(self.stocks[i]+'_Expenses_'+str(dt.date.today()),dpi=600)
            except Exception:
                pass
            
    def liquidity(self, dark=False):
        for i in range(0, len(self.financials)):
            try:
                
                fig=p.linep([self.financials[i][1][3]['currentRatio'],self.financials[i][1][3]['quickRatio'],self.financials[i][1][3]['cashRatio']], 'linear', ['Current Ratio','Quick Ratio','Cash Ratio'], 10, dark, self.financials[i][5],'Ratios de liquidez' , 'FMPCloud.io')
                plt.savefig(self.stocks[i]+'_Liquidity_Ratios_'+str(dt.date.today()),dpi=600)
                fig
            except Exception:
                pass
            
    def margins(self, dark=False):
        for i in range(0, len(self.financials)):
            try:
                
                fig=p.linep([self.financials[i][1][3]['grossProfitMargin'],self.financials[i][1][3]['operatingProfitMargin'],self.financials[i][1][3]['netProfitMargin']], 'linear', ['Gross Profit Margin','Operating Profit Margin','Net Profit Margin'], 10, dark, self.financials[i][5],' Liquidity Ratios' , 'FMPCloud.io')
                plt.savefig(self.financials[i][0]+'_Profit_Margins_'+str(dt.date.today()),dpi=600)
                fig
            except Exception:
                pass
            
            
    def profitability(self, dark=False):
        for i in range(0, len(self.financials)):
            try:
                
                
                fig=p.linep([self.financials[i][1][3]['returnOnAssets'],self.financials[i][1][3]['returnOnEquity'],self.financials[i][1][3]['returnOnCapitalEmployed']], 'linear', ['ROA','ROE','ROCE'], 10, dark, self.financials[i][5],' Efficiency ratios' , 'FMPCloud.io')
                plt.savefig(self.financials[i][0]+'_profit_ratios_'+str(dt.date.today()),dpi=600)
                fig
            except Exception:
                pass
            
    def solvency(self, dark=False):
        for i in range(0, len(self.financials)):
            try:
                fig=p.linep([self.financials[i][1][3]['debtEquityRatio'],self.financials[i][1][3]['debtRatio'],self.financials[i][1][3]['totalDebtToCapitalization'],self.financials[i][1][3]['longTermDebtToCapitalization']], 'linear', ['D/E Ratio','Debt Ratio','Total debt to cap','LT Debt to cap' ], 10, dark, self.financials[i][5],'Debt Ratios' , 'FMPCloud.io')
                plt.savefig(self.financials[i][0]+'_debt_ratios_'+str(dt.date.today()),dpi=600)
                fig
            except Exception:
                pass
                            
                        
    def scatterplot(self, x, y, xl, yl):
        plt.figure()
        plt.title('Scatterplot of '+x+y)
        plt.scatter(x,y)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.grid()
        plt.show()
            
    def hist_returns(self):
        for i in range (0, len(self.stocks)):


            # ax.spines['top'].set_visible(False)
            # ax.spines['right'].set_visible(False)
            # ax.spines['left'].set_visible(False)
            # ax.spines['bottom'].set_visible(False)
            # ax.tick_params(bottom=False, left=False)
            # ax.set_axisbelow(True)
            # ax.yaxis.grid(False)
            # ax.xaxis.grid(False)


            # Plot
            #     Plot histogram
            mean = np.mean(self.price[i][1]['changePercent'])
            std = np.std(self.price[i][1]['changePercent'])
            skewness= skew(self.price[i][1]['changePercent'])
            kurt = kurtosis(self.price[i][1]['changePercent']) # excess kurtosis
            per_05,per_25,per_75,per_95 = np.percentile(self.price[i][1]['changePercent'],5),np.percentile(self.price[i][1]['changePercent'],25),np.percentile(self.price[i][1]['changePercent'],75),np.percentile(self.price[i][1]['changePercent'],95)
            median = np.median(self.price[i][1]['changePercent'])
            nb_decimals=3
            plot_str = self.stocks[i]+'  Histogram of Returns' + '\n'\
                +'mean ' + str(np.round(mean,nb_decimals))\
                + ' | std dev ' + str(np.round(std,nb_decimals))\
                + ' | skewness ' + str(np.round(skewness,nb_decimals))\
                + ' | kurtosis ' + str(np.round(kurt,nb_decimals)) + '\n'\
                + 'p05% ' + str(np.round(per_05,nb_decimals))\
                + ' | p20% ' + str(np.round(per_25,nb_decimals))\
                + ' | median ' + str(np.round(median,nb_decimals))\
                + ' | p80% ' + str(np.round(per_75,nb_decimals))\
                + ' | p95% ' + str(np.round(per_95,nb_decimals))
            fig, ax = plt.subplots()
            plt.style.use('seaborn-darkgrid')        
            cm = plt.cm.get_cmap('YlGn')
            n, bins, patches = plt.hist(self.price[i][1]['changePercent'], bins=90, facecolor='#2ab0ff', edgecolor='#e0e0e0', linewidth=0.5, alpha=0.7, density=True)
            
            n = n.astype('int') # it MUST be integer
            bin_centers = 0.5 * (bins[:-1] + bins[1:])

            # scale values to interval [0,1]
            col = bin_centers - min(bin_centers)
            col /= max(col)
            
            for c, p in zip(col, patches):
                plt.setp(p, 'facecolor', cm(c))
            ax.plot()
            x=np.linspace(mean - 3*std, mean + 3*std, 100)
            plt.plot(x,norm.pdf(x, mean, std),linestyle = ":", alpha=0.75,color='darkgreen')
            plt.xlabel(plot_str, color='forestgreen',weight='bold')
                # Quantile lines
            
            # X
                # Limit x range to 0-4
            
            # Y
            # ax.set_ylim(0, 1)
            # ax.set_yticklabels([])
            # ax.set_ylabel("")
            
            # Annotations
            # ax.text(per_05,0.3, "5%", size = 10, alpha = 0.8)
            ax.axvline(per_05,0,0.32, linestyle = ":", alpha=0.75,color='limegreen')
            # ax.text(per_25, 0.75, "25%", size = 10, alpha = 0.8)
            ax.axvline(per_25,0,0.46, linestyle = ":", alpha=0.75,color='forestgreen')
            # ax.text(median,0.85, "50%", size = 12, alpha = 0.8)
            ax.axvline(median,0,0.54, linestyle = ":", alpha=0.75,color='forestgreen')
            # ax.text(mean,0.85, "Avg.", size = 12, alpha = 0.8)
            ax.axvline(mean,0,0.54, linestyle = ":", alpha=0.75,color='forestgreen')
            # ax.text(per_75,0.2, "75%", size = 10, alpha = 0.8)
            ax.axvline(per_75,0,0.46, linestyle = ":", alpha=0.75,color='forestgreen')
            # ax.text(per_95,0.65, "95%", size = 10, alpha =.8)
            ax.axvline(per_95,0,0.32, linestyle = ":", alpha=0.75,color='limegreen')
            
            # Overall
            ax.set_facecolor("white")

            ax.text(0.2, 0.2,
                    'Greenfield Capital Advisors Group S.L.',
                    horizontalalignment='center',
                    verticalalignment='top', size=28, alpha=0.5, color='green')

            plt.show() 
        
        
        
        
    def scatt( x, y, cat):

        df=pd.DataFrame(x)
        df['y']=y
        df['cat']=cat
        fig, ax = plt.subplots(figsize=(12, 8))#;ax.scatter(x, y)
        color=cm.viridis(np.linspace(0,1,12))
        i=0
        for name, group in df:
        #     plt.scatter(group.x, group.y, marker='o', linestyle='', markersize=12, label=name, cmap='Greens')         
            i+=1
            plt.scatter(group.x, group.y, color=color[i], label=name )
            plt.legend()

    

class finmodeling():
    def __init__(self, apikey):
        self.apikey=apikey
        self.stocks=None
        self.financials=None
        self.price=None
        self.rd_spread=None
        
        self.i_paid=None
        self.i_rec=None
        self.rd_current=None
        self.re_capm=None
        self.re_gordon=None
        self.re_gordon_2=None
        self.re_gordon_2=None
        
        
        
        
        
        
        
    def data(self, stocks):
        self.stocks=stocks
        for i in tqdm(range(0,len(self.stocks)), desc = 'Retrieving financials'):
            try:
                self.financials.append(list())
                self.financials[i].append(self.stocks[i])
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(fmp.quote(self.apikey, self.stocks[i])[0]['name'])
                self.financials[i][1].append(f.clean_financials(fmp.balance_sheet_statement(self.apikey, self.stocks[i],'quarter', 15)))
                self.financials[i][1].append(f.clean_financials(fmp.income_statement(self.apikey, self.stocks[i],'quarter', 15)))
                self.financials[i][1].append(f.clean_financials(fmp.cash_flow_statement(self.apikey, self.stocks[i],'quarter', 15)))
                self.financials[i][1].append(f.clean_financials(fmp.financial_ratios(self.apikey, self.stocks[i],period='quarter',limit=15)))
                self.financials[i][2].append(f.clean_financials(fmp.balance_sheet_statement(self.apikey, self.stocks[i],'annual', 15)))
                self.financials[i][2].append(f.clean_financials(fmp.income_statement(self.apikey, self.stocks[i],'annual', 15)))
                self.financials[i][2].append(f.clean_financials(fmp.cash_flow_statement(self.apikey, self.stocks[i],'annual', 15)))
                self.financials[i][2].append(f.clean_financials(fmp.financial_ratios(self.apikey, self.stocks[i],period='annual',limit=15)))
                self.financials[i][3].append(f.ttm(f.clean_financials(fmp.balance_sheet_statement(self.apikey, self.stocks[i],'quarter', 15))))
                self.financials[i][3].append(f.ttm(f.clean_financials(fmp.income_statement(self.apikey, self.stocks[i],'quarter', 15))))
                self.financials[i][3].append(f.ttm(f.clean_financials(fmp.cash_flow_statement(self.apikey, self.stocks[i],'quarter', 15))))
                
                self.price.append(list())
                self.price[i].append(self.stocks[i])
                self.price[i].append(f.clean_financials(fmp.historical_price_full(self.apikey, self.stocks[i])))
                self.price[i].append(f.clean_financials(fmp.historical_chart(self.apikey, self.stocks[i], '1min')))
                self.financials[i][4].append(self.financials[i][3][0].reindex(self.price[i][1].index,method='ffill').dropna())
                self.financials[i][4].append(self.financials[i][3][1].reindex(self.price[i][1].index,method='ffill').dropna())
                self.financials[i][4].append(self.financials[i][3][2].reindex(self.price[i][1].index,method='ffill').dropna())
                        
                self.price[i].append(self.financials[i]*self.price[i][1]['close'])
            
            except Exception:
                pass

        return self.financials, self.price 
        
        
    
        
            
        
###intentar meter todos los balances de las empresas de stocks en un nested dictionary
###LA BASE PARA ESTUDIOS DE MERCADO