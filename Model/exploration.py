#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 20:51:18 2018

"""

from Model.codes import Codes
from Model.file import File
import matplotlib.pyplot as plt
import numpy as np

def add_indicator(indicator_name):
    stocks = load_stocks()
    for stock in stocks:
        stock.add_indicator(indicator_name)
        
def add_strategy(strategy_name):
    stocks = load_stocks()
    strategy = get_strategy(strategy_name)
    strategy.refresh(stocks)

def load_stocks():
    stocks = []
    codes = Codes()
    for index, _ in codes.data[codes.data.INCLUDE_FOR_ANALYSIS].iterrows():
        stocks.append(File(index, class_type = 'Stock').load())
    return stocks

def get_stock(code):
    return File(code, class_type='Stock').load()

def get_strategy(strategy_name):
    return File(strategy_name, class_type='Strategy').load()

def get_indicator(indicator_name):
    return File(indicator_name, class_type='Indicator').load()

def get_function(function_name):
    return File(function_name, class_type='Function').load()
    
def refresh_stocks(verbose = None, to_date = None):
    stocks = load_stocks()
    for stock in stocks:
        stock.refresh(to_date = to_date, verbose = verbose)
    
def plot_stock(code, indicators = [], strategy_name = None, figsize = (10,5), labelbottom = False, labelleft = False):
    stock = get_stock(code)
    if not strategy_name is None:
        strategy = get_strategy(strategy_name)
        trades = strategy.to_dataframe()
    else:
        strategy = None
    colors = ['blue', 'black']
    fig, axis = plt.subplots(nrows = 1, ncols=1, sharex = False, sharey = False, figsize=figsize)
    for ax in np.array(axis).reshape(-1):
        ax.plot(stock.data.index, stock.data.CLOSE)
        k = 0
        for indicator in indicators:
            ax.plot(stock.data.index, stock.data[indicator.name], color = colors[k])
            k = k+1
        ax.set_title(stock.name, fontsize = 8, y = 0.98)
        if not strategy is None:
            df = trades[trades.STOCK_NAME == stock.name]
            for index, row in df.iterrows():
                opening_date = row.OPENING_DATE
                closing_date = row.CLOSING_DATE
                ax.axvline(row.OPENING_DATE, color='grey', linestyle ='dashed', linewidth=0.5)
                if str(closing_date) == 'NaT':
                    closing_date = stock.last_date
                else:
                    ax.axvline(row.CLOSING_DATE, color='grey', linestyle ='dashed', linewidth=0.5)                    
                sub_stock = stock.data.loc[opening_date:closing_date]
                if row.PERFORMANCE >= 1:
                    color = 'green'
                else:
                    color = 'red'
                ax.plot(sub_stock.index, sub_stock.CLOSE, color=color)
        ax.tick_params(axis='both', which='both', bottom=True, labelbottom=True, left=True, labelleft=True)
    plt.show()
    
    
def plot_all_stocks(strategy_name = None, figsize = (20,130), labelbottom = False, labelleft = False):
    j = 0
    stocks = load_stocks()
    strategy = get_strategy(strategy_name)
    nrows = int(len(stocks) / 4) + 1
    ncols = min(len(stocks), 4)
    fig, axis = plt.subplots(nrows = nrows, ncols=ncols, sharex = False, sharey = False, figsize=figsize)
    trades = strategy.to_dataframe()
    for ax in np.array(axis).reshape(-1):
        if j < len(stocks):
            stock = stocks[j]
            ax.plot(stock.data.index, stock.data.CLOSE)
            ax.set_title(stock.name, fontsize = 8, y = 0.98)
            df = trades[trades.STOCK_NAME == stock.name]
            for index, row in df.iterrows():
                if not strategy is None:
                    opening_date = row.OPENING_DATE
                    closing_date = row.CLOSING_DATE
                    ax.axvline(row.OPENING_DATE, color='grey', linestyle ='dashed', linewidth=0.5)
                    if str(closing_date) == 'NaT':
                        closing_date = stock.last_date
                    else:
                        ax.axvline(row.CLOSING_DATE, color='grey', linestyle ='dashed', linewidth=0.5)                    
                    sub_stock = stock.data.loc[opening_date:closing_date]
                    if row.PERFORMANCE >= 1:
                        color = 'green'
                    else:
                        color = 'red'
                    ax.plot(sub_stock.index, sub_stock.CLOSE, color=color)
            ax.tick_params(axis='both', which='both', bottom=False, labelbottom=labelbottom, left=False, labelleft=labelleft)
            j = j + 1
    plt.show()
    
def bids_of_the_day(strategy):
    stocks = load_stocks()
    for stock in stocks:
        stock.refresh()
    strategy.refresh(stocks)
    print([t for t in strategy.trades if t.status == 'awaiting buy'])
    print([t for t in strategy.trades if t.status == 'awaiting sell'])