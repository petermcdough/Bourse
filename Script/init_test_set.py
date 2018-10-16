#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 19:27:03 2018

"""

import quandl                              # handles api calls
import sys
import os
import numpy as np

if '/Users/' in os.getcwd():
    sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/Bourse/"))
elif '/home/' in os.getcwd():
    sys.path.insert(0, "/home/petermcdough/Bourse/")

from functools import partial
from Model.env import Env
from Model.functions import Function
from Model.stock import Stock
from Model.indicator import Indicator
from Model.strategy import Strategy
from Model.constants import \
        API_KEY, \
        ENVIRONMENT, \
        TEST_FOLDER, \
        TEST_STOCK, \
        TEST_AWAITING_TRADE_STOCK, \
        TEST_PASS_TRADE_STOCK, \
        TEST_REFRESH_DATE_EMPTY, \
        TEST_REFRESH_DATE_NOT_EMPTY, \
        TEST_REFRESH_DATE_WITH_INDICATORS, \
        TEST_REFRESH_DATE_AWAITING_BUY_1, \
        TEST_REFRESH_DATE_AWAITING_BUY_2, \
        TEST_REFRESH_DATE_AWAITING_SELL_1, \
        TEST_REFRESH_DATE_AWAITING_SELL_2, \
        TEST_REFRESH_DATE_PASS, \
        SAVE_FOLDER 

def sma(df, window, column = 'CLOSE'):
    return df[column].rolling(window = window).mean()

SMA = Function('SMA', sma)

def test_buy_condition(stock, row):
    date = None
    price = None
    status = None
    if np.isnan(row.SMA80) or np.isnan(row.SMA150):
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

def test_sell_condition(stock, row, trade):
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

def init_empty_stock():
    stock = Stock(TEST_STOCK)
    os.rename(SAVE_FOLDER + stock.path, TEST_FOLDER + 'empty_stock.p')

def init_refreshed_empty_stock():
    stock = Stock(TEST_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_EMPTY)
    os.rename(SAVE_FOLDER + stock.path, TEST_FOLDER + 'refreshed_empty_stock.p')
    
def init_refreshed_not_empty_stock():
    stock = Stock(TEST_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_NOT_EMPTY)
    os.rename(SAVE_FOLDER + stock.path, TEST_FOLDER + 'refreshed_not_empty_stock.p')
    
def init_refreshed_stock_with_indicators():
    stock = Stock(TEST_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_WITH_INDICATORS)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    os.rename(SAVE_FOLDER + stock.path, TEST_FOLDER + 'refreshed_stock_with_indicators.p')
    
def init_stock_with_indicators():
    stock = Stock(TEST_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_NOT_EMPTY)
    indicator = Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    os.rename(SAVE_FOLDER + stock.path, TEST_FOLDER + 'stock_with_indicators.p')
    os.rename(SAVE_FOLDER + indicator.path, TEST_FOLDER + 'applied_indicator.p')
    
def init_empty_indicator():
    indicator = Indicator('SMA80', partial(SMA.execute, window = 80))
    os.rename(SAVE_FOLDER + indicator.path, TEST_FOLDER + 'empty_indicator.p')
    
def init_empty_strategy():
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'empty_strategy.p')
    
def init_applied_strategy():
    stock = Stock(TEST_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_WITH_INDICATORS)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    strategy.refresh([stock])
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'applied_strategy.p')
    os.rename(SAVE_FOLDER + stock.path, TEST_FOLDER + 'stock_with_applied_strategy.p')
        
def init_strategy_awaiting_buy_before():
    stock = Stock(TEST_AWAITING_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_BUY_1)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    strategy.refresh([stock])
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'strategy_awaiting_buy_before.p')
    
def init_strategy_awaiting_buy_after():
    stock = Stock(TEST_AWAITING_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_BUY_2)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    strategy.refresh([stock])
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'strategy_awaiting_buy_after.p')
    
def init_strategy_awaiting_sell_before():
    stock = Stock(TEST_AWAITING_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_SELL_1)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    strategy.refresh([stock])
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'strategy_awaiting_sell_before.p')
    
def init_strategy_awaiting_sell_after():
    stock = Stock(TEST_AWAITING_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_SELL_2)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    strategy.refresh([stock])
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'strategy_awaiting_sell_after.p')
    
def init_strategy_pass():    
    stock = Stock(TEST_PASS_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_PASS)
    Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    strategy = Strategy('SMA80_SMA150', test_buy_condition, test_sell_condition)
    strategy.refresh([stock])
    os.rename(SAVE_FOLDER + strategy.path, TEST_FOLDER + 'strategy_pass.p')    
              
def main():
    quandl.ApiConfig.api_key = API_KEY
    
    if ENVIRONMENT != Env.TEST:
        print('Set environment to TEST in the constants file before running the script.')
        print('Script aborted.')
    else:  
        init_empty_stock()
        init_refreshed_empty_stock()
        init_refreshed_not_empty_stock()
        init_refreshed_stock_with_indicators()
        init_stock_with_indicators()
        init_empty_indicator()
        init_empty_strategy()
        init_applied_strategy()
        init_strategy_awaiting_buy_before()
        init_strategy_awaiting_buy_after()
        init_strategy_awaiting_sell_before()
        init_strategy_awaiting_sell_after()
        init_strategy_pass()


if __name__ == "__main__":
    main()