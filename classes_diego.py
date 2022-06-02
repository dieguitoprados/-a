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
import waterfall_chart
from scipy.stats import norm
import matplotlib


import functions_diego as f
importlib.reload(f)



class get_data():
    
    def __init__(self, stocks, apikey):
        
        self.apikey=apikey
        self.stocks=stocks
        self.lenst=len(self.stocks)
        self.financials=[]
        self.price=[]
        self.annual=bool()
        self.dates=pd.DataFrame()
        self.price_ratios=[]
        
        self.plotin=None

        self.sp=fmp.sp500_constituent(apikey)
        self.sp_fin=[]
        self.sp_rat=[]
        
        
        

        
    def get_financials(self): 
        for i in range(0,len(self.stocks)):
            try:
                self.financials.append(list())
                self.financials[i].append(self.stocks[i])
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(list())
                self.financials[i].append(list())
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
         for i in range(len(self.sp)):
            self.sp_fin.append(list())
            self.sp_fin[i].append(self.sp[i]['symbol'])
            self.sp_fin[i].append(self.sp[i]['name'])
            self.sp_fin[i].append(f.clean_financials(pd.DataFrame(fmp.balance_sheet_statement(self.apikey, self.sp[i]['symbol']))))
            self.sp_fin[i].append(f.clean_financials(pd.DataFrame(fmp.income_statement(self.apikey, self.sp[i]['symbol']))))
            self.sp_fin[i].append(f.clean_financials(pd.DataFrame(fmp.cash_flow_statement(self.apikey, self.sp[i]['symbol']))))
            self.sp_fin[i].append(pd.DataFrame(fmp.financial_ratios_ttm(self.apikey, self.sp[i]['symbol'])))
         return self.sp_fin
    def sp_ratios(self):
        for i in range(len(self.sp)):
            try:
                self.sp_fin.append(list())
                self.sp_fin[i].append(self.sp[i]['symbol'])
                self.sp_fin[i].append(self.sp[i]['name'])
                self.sp_fin[i].append(pd.DataFrame(fmp.financial_ratios_ttm(self.apikey, self.sp[i]['symbol'])))
            except Exception:
                pass

        return self.sp_rat
     
    
    def get_price(self):
        for i in range(0,len(self.stocks)):
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
            
    def histt(self):
        for i in range(0,len(self.stocks)):
            plt.style.use('seaborn-darkgrid')
            fig, ax = plt.subplots()  
            for n in range(0,len(self.inputs)):
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['currentRatio'], label='currentRatio',marker='o', markersize=4, color='limegreen')
            ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                                  ncol=2, mode="expand", borderaxespad=0.)
            plt.xticks(rotation = 80)
            ax.yaxis.grid(True, color='palegreen', alpha=0.3)


            ax.set_facecolor("white")
            ax.set_xlabel(plt.legend())
            ax.set_xlabel(self.stocks[i]+' Liquidity Ratios TTM',  color='seagreen',
                          weight='bold')
# ax.legend()
            ax.text(
                    0.75,
                    0.02,
                    'Greenfield Capital Advisors Group S.L.',
                    horizontalalignment='center',
                    verticalalignment='top',
                    transform=ax.transAxes)
            fig.tight_layout()

            
    
    
    def hist_inc(self):
        for i in range(0, len(self.financials)):
            try:
                plt.style.use('seaborn-darkgrid')

                fig, ax = plt.subplots(figsize=(8,5))
                
                # Save the chart so we can loop through the bars below.
                    
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='lime',height=self.financials[i][1][1]['revenue'],label='revenue',tick_label=self.financials[i][1][1].index.strftime('%d/%m/%Y'))
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='limegreen',height=self.financials[i][1][1]['grossProfit'],label='grossProfit')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='seagreen',height=self.financials[i][1][1]['ebitda'],label='ebitda')
                for bar in bars:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.3,
                        round(bar.get_height()/1000000, 1),
                        horizontalalignment='center',
                        color='black',
                        weight='bold',size=8
                    )
                
                bars=plt.bar(x=np.arange(self.financials[i][1][1]['revenue'].size),color='forestgreen',height=self.financials[i][1][1]['netIncome'],label='netIncome')
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
            
    def liquidity(self):
        for i in range(0, len(self.stocks)):
            try:
                plt.style.use('seaborn-darkgrid')
                fig, ax = plt.subplots()  
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['currentRatio'], label='currentRatio',marker='o', markersize=4, color='limegreen')
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['quickRatio'],label='quickRatio',marker='o', markersize=4, color='forestgreen')
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['cashRatio'],label='cashRatio',marker='o', markersize=4, color='seagreen')
                ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                                      ncol=2, mode="expand", borderaxespad=0.)
                plt.xticks(rotation = 80)
                ax.yaxis.grid(True, color='palegreen', alpha=0.3)


                ax.set_facecolor("white")
                ax.set_xlabel(plt.legend())
                ax.set_xlabel(self.stocks[i]+' Liquidity Ratios TTM',  color='seagreen',
                              weight='bold')
# ax.legend()
                ax.text(
                        0.75,
                        0.02,
                        'Greenfield Capital: Diego Prados',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()
                plt.savefig(self.stocks[i]+'_Liquidity_Ratios_'+str(dt.date.today()),dpi=600)

            except Exception:
                pass
    def margins(self):
        for i in range(0, len(self.stocks)):
            try:
                plt.style.use('seaborn-darkgrid')
                fig, ax = plt.subplots()  
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['grossProfitMargin'], label='grossProfitMargin',marker='o', markersize=4, color='limegreen')
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['operatingProfitMargin'],label='operatingProfitMargin',marker='o', markersize=4, color='forestgreen')
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['netProfitMargin'],label='netProfitMargin',marker='o', markersize=4, color='seagreen')
                ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                                      ncol=2, mode="expand", borderaxespad=0.)
                plt.xticks(rotation = 80)
                ax.yaxis.grid(True, color='palegreen', alpha=0.3)


                ax.set_facecolor("white")
                ax.set_xlabel(plt.legend())
                ax.set_xlabel(self.stocks[i]+' Profit Margins TTM',  color='seagreen',
                              weight='bold')
# ax.legend()
                ax.text(
                        0.75,
                        0.02,
                        'Greenfield Capital: Diego Prados',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()
                plt.savefig(self.stocks[i]+'_Profit_Margins_'+str(dt.date.today()),dpi=600)

            except Exception:
                pass
            
            
    def profitability(self):
        for i in range(0, len(self.stocks)):
            try:
                plt.style.use('seaborn-darkgrid')
                fig, ax = plt.subplots()  
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['returnOnAssets'], label='ROA',marker='o', markersize=4, color='limegreen')
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['returnOnEquity'],label='ROE',marker='o', markersize=4, color='forestgreen')
                plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['returnOnCapitalEmployed'],label='ROCE',marker='o', markersize=4, color='seagreen')
                ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                                      ncol=2, mode="expand", borderaxespad=0.)
                plt.xticks(rotation = 80)
                ax.yaxis.grid(True, color='palegreen', alpha=0.3)


                ax.set_facecolor("white")
                ax.set_xlabel(plt.legend())
                ax.set_xlabel(self.stocks[i]+' Profitability Ratios TTM',  color='seagreen',
                              weight='bold')
# ax.legend()
                ax.text(
                        0.75,
                        0.02,
                        'Greenfield Capital: Diego Prados',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()
                plt.savefig(self.stocks[i]+'_profit_ratios_'+str(dt.date.today()),dpi=600)

            except Exception:
                pass
                            
                        
    def scatterplot(self, x, y):
        plt.figure()
        plt.title('Scatterplot of '+x+y)
        plt.scatter(x,y)
        plt.plot(x, self.predictor_linreg, color='green')
        plt.ylabel(self.ric)
        plt.xlabel(self.benchmark)
        plt.grid()
        plt.show()
            
    def solvency(self):
        for i in range(0, len(self.stocks)):
            try:
                plt.style.use('seaborn-darkgrid')
                fig, ax = plt.subplots()  
                try:
                    plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['debtEquityRatio'], label='debtEquityRatio',marker='o', markersize=4, color='lime')
                except Exception:
                    pass
                try:
                    plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['debtRatio'], label='debtRatio',marker='o', markersize=4, color='limegreen')
                except Exception:
                    pass                
                try:
                    plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['totalDebtToCapitalization'],label='totalDebtToCapitalization',marker='o', markersize=4, color='forestgreen')
                except Exception:
                    pass                
                try:
                    plt.plot(self.financials[i][1][3].index,self.financials[i][1][3]['longTermDebtToCapitalization'],label='longTermDebtToCapitalization',marker='o', markersize=4, color='seagreen')
                except Exception:
                    pass
                ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
                                      ncol=2, mode="expand", borderaxespad=0.)
                plt.xticks(rotation = 80)
                ax.yaxis.grid(True, color='palegreen', alpha=0.3)


                ax.set_facecolor("white")
                ax.set_xlabel(plt.legend())
                ax.set_xlabel(self.stocks[i]+' Debt Ratios TTM',  color='seagreen',
                              weight='bold')

                ax.text(
                        0.75,
                        0.02,
                        'Greenfield Capital: Diego Prados',
                        horizontalalignment='center',
                        verticalalignment='top',
                        transform=ax.transAxes)
                fig.tight_layout()
                plt.savefig(self.stocks[i]+'_debt_ratios_'+str(dt.date.today()),dpi=600)

            except Exception:
                pass
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
        
            
        
###intentar meter todos los balances de las empresas de stocks en un nested dictionary
###LA BASE PARA ESTUDIOS DE MERCADO