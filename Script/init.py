#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 18:51:26 2018

"""

import quandl                              # handles api calls
import sys
import os
from functools import partial

if '/Users/' in os.getcwd():
    sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/Bourse/"))
elif '/home/' in os.getcwd():
    sys.path.insert(0, "/home/petermcdough/Bourse/")

from Model.codes import Codes
from Model.constants import API_KEY, ENVIRONMENT, DEV_REFRESH_DATE
from Model.env import Env
from Model.exploration import add_indicator
from Model.functions import Function
from Model.indicator import Indicator      
from Model.stock import Stock
from Model.strategy import Strategy

def SMA_(df, window, column = 'CLOSE'):
    return df[column].rolling(window = window).mean()

def PER_K_(df, window, roll):
    low = df['LOW'].rolling(window=window).min()
    high = df['HIGH'].rolling(window=window).max()
    close = df['CLOSE']
    return 100*((close - low) / (high - low)).rolling(window=roll).mean()

def buy_condition(stock, row):
    date = None
    price = None
    status = None
    if str(row.PER_K) == 'nan' or str(row.PER_D) == 'nan' or str(row.SMA80) == 'nan' or str(row.SMA150) == 'nan':
        state = True
    else:
        pos = stock.data.index.get_loc(row.Index)
        prev_row = stock.data.iloc[pos - 1]
        state = (row.PER_K > row.PER_D and row.SMA80 > row.SMA150*1 and (row.SMA80 - prev_row.SMA80 > 0))
        if state == True:
            pos = stock.data.index.get_loc(row.Index)
            if pos + 1 == len(stock.data):
                price = None
                status = 'awaiting buy'
                date = row.Index
            else:
                next_row = stock.data.iloc[pos + 1]
                price = next_row.OPEN
                status = 'pending'
                date = next_row.name
    return {'state': state, 'date': date, 'price': price, 'status': status}

def sell_condition(stock, row, trade):
    date = None
    price = None
    status = None                          
    state = (row.SMA80*1 < row.SMA150)
    if state == True:
        pos = stock.data.index.get_loc(row.Index)
        if pos + 1 == len(stock.data):
            price = None
            status = 'awaiting sell'
            date = row.Index
        else:
            next_row = stock.data.iloc[pos + 1]
            price = next_row.OPEN
            status = 'closed'
            date = next_row.name
    return {'state': state, 'date': date, 'price': price, 'status': status}

def init_stock():
    codes = Codes()
    stocks = []
    if ENVIRONMENT == Env.DEV:
        to_date = DEV_REFRESH_DATE
    else:
        to_date = None
    for index, row in codes.data[codes.data.INCLUDE_FOR_ANALYSIS].iterrows():
        stocks.append(Stock(index))
    for stock in stocks:
        stock.refresh(verbose = True, to_date = to_date)
        
def init_strategy():
    SMA = Function('SMA', SMA_)
    PER_K = Function('PER_K', PER_K_)
    Indicator('PER_K', partial(PER_K.execute, window = 10, roll = 1))
    Indicator('PER_D', partial(PER_K.execute, window = 10, roll = 3))   
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    add_indicator('SMA80')
    add_indicator('SMA150')
    add_indicator('PER_K')
    add_indicator('PER_D')
    Strategy('SMA80_SMA150_STOCHASTICS', buy_condition, sell_condition)
    print('Strategy SMA80_SMA150_STOCHASTICS successfully created.')
    
def main():
    quandl.ApiConfig.api_key = API_KEY # mandatory to make api calls on quandl
    init_stock()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-strat":
            init_strategy() 
    
if __name__ == "__main__":
    main()