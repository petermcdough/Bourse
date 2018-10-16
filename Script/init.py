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
from Model.constants import API_KEY
from Model.exploration import add_indicator
from Model.functions import Function
from Model.indicator import Indicator      
from Model.stock import Stock
from Model.strategy import Strategy

def SMA_(df, window, column = 'CLOSE'):
    return df[column].rolling(window = window).mean()

def buy_condition(stock, row):
    date = None
    price = None
    status = None
    if str(row.SMA80) == 'nan' or str(row.SMA150) == 'nan':
        state = True
    else:
        state = row.SMA80 > row.SMA150
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
    state = row.SMA80 < row.SMA150
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
    for index, row in codes.data[codes.data.INCLUDE_FOR_ANALYSIS].iterrows():
        stocks.append(Stock(index))
    for stock in stocks:
        stock.refresh(verbose = True)
        
def init_strategy():
    SMA = Function('SMA', SMA_)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    add_indicator('SMA80')
    add_indicator('SMA150')
    Strategy('SMA80_SMA150', buy_condition, sell_condition)
    print('Strategy SMA80_SMA150 successfully created.')
    
def main():
    quandl.ApiConfig.api_key = API_KEY # mandatory to make api calls on quandl
    init_stock()
    if len(sys.argv) > 1:
        if sys.argv[1] == "-strat":
            init_strategy() 
    
if __name__ == "__main__":
    main()