#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 12:42:54 2018

"""

import sys
import quandl
import dill as pickle
import numpy as np
import os
import base64

if '/Users/' in os.getcwd():
    sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/Bourse/"))
elif '/home/' in os.getcwd():
    sys.path.insert(0, "/home/petermcdough/Bourse/")

from functools import partial
from Model.email import AdvisorEmail, User
from Model.env import Env
from Model.stock import Stock
from Model.indicator import Indicator
from Model.file import File
from Model.functions import Function
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
        EMAIL, \
        PWD
        
EMPTY_STOCK = pickle.load(open(TEST_FOLDER + "empty_stock.p", "rb" ))
REFRESHED_EMPTY_STOCK = pickle.load(open(TEST_FOLDER + "refreshed_empty_stock.p", "rb" ))
REFRESHED_NOT_EMPTY_STOCK = pickle.load(open(TEST_FOLDER + "refreshed_not_empty_stock.p", "rb" ))
REFRESHED_STOCK_WITH_INDICATORS = pickle.load(open(TEST_FOLDER + "refreshed_stock_with_indicators.p", "rb" ))
STOCK_WITH_INDICATORS = pickle.load(open(TEST_FOLDER + "stock_with_indicators.p", "rb" ))
EMPTY_INDICATOR = pickle.load(open(TEST_FOLDER + "empty_indicator.p", "rb" ))
APPLIED_INDICATOR = pickle.load(open(TEST_FOLDER + "applied_indicator.p", "rb" ))
EMPTY_STRATEGY = pickle.load(open(TEST_FOLDER + "empty_strategy.p", "rb" ))
APPLIED_STRATEGY = pickle.load(open(TEST_FOLDER + "applied_strategy.p", "rb" ))
STOCK_WITH_APPLIED_STRATEGY = pickle.load(open(TEST_FOLDER + "stock_with_applied_strategy.p", "rb" ))
STRATEGY_AWAITING_BUY_BEFORE = pickle.load(open(TEST_FOLDER + "strategy_awaiting_buy_before.p", "rb" ))
STRATEGY_AWAITING_BUY_AFTER = pickle.load(open(TEST_FOLDER + "strategy_awaiting_buy_after.p", "rb" ))
STRATEGY_AWAITING_SELL_BEFORE = pickle.load(open(TEST_FOLDER + "strategy_awaiting_sell_before.p", "rb" ))
STRATEGY_AWAITING_SELL_AFTER = pickle.load(open(TEST_FOLDER + "strategy_awaiting_sell_after.p", "rb" ))
STRATEGY_PASS = pickle.load(open(TEST_FOLDER + "strategy_pass.p", "rb" ))

def sma(df, window, column = 'CLOSE'):
    return df[column].rolling(window = window).mean()

def TEST_BUY_CONDITION(stock, row):
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

def TEST_SELL_CONDITION(stock, row, trade):
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

SMA = Function('SMA', sma)

def compare(test, base, test_name):
    if test == base:
        print(test_name + ": ok")
    else:
        sys.exit(test_name + ": nok")
        
def stock_creation():
    test = Stock(TEST_STOCK)
    compare(test, EMPTY_STOCK, "Stock creation")

def stock_load():
    File(TEST_STOCK, class_type = 'Stock').load()
    print("Loading stock: ok")
    
def stock_refresh():
    test = File(TEST_STOCK, class_type = 'Stock').load()
    test.refresh(to_date = TEST_REFRESH_DATE_EMPTY)
    compare(test, REFRESHED_EMPTY_STOCK, "Empty stock refresh")
    test.refresh(to_date = TEST_REFRESH_DATE_NOT_EMPTY)  
    compare(test, REFRESHED_NOT_EMPTY_STOCK, "Not empty stock refresh")
    
def function_creation():
    Function('SMA', SMA)
    print("Function creation: ok")
    
def indicator_creation():
    test = Indicator('SMA80', partial(SMA.execute, window = 80))
    Indicator('SMA150', partial(SMA.execute, window = 150))
    compare(test, EMPTY_INDICATOR, "Indicator creation")
    
def indicator_add():
    test = File(TEST_STOCK, class_type = 'Stock').load()
    test.add_indicator('SMA80')
    test.add_indicator('SMA150')
    compare(test, STOCK_WITH_INDICATORS, "Add indicators")
    test = File('SMA80', class_type = 'Indicator').load()
    compare(test, APPLIED_INDICATOR, "Applied indicator attributes")
    
def refresh_with_indicators():
    test = File(TEST_STOCK, class_type = 'Stock').load()
    test.refresh(to_date = TEST_REFRESH_DATE_WITH_INDICATORS)
    compare(test, REFRESHED_STOCK_WITH_INDICATORS, "Refresh with indicators")
    
def strategy_creation():
    test = Strategy('SMA80_SMA150', TEST_BUY_CONDITION, TEST_SELL_CONDITION)
    compare(test, EMPTY_STRATEGY, "Strategy creation")
    
def strategy_apply():
    stock = File(TEST_STOCK, class_type = 'Stock').load()
    test = File('SMA80_SMA150', class_type = 'Strategy').load()
    test.refresh([stock])
    compare(test, APPLIED_STRATEGY, "Apply strategy")
    compare(stock, STOCK_WITH_APPLIED_STRATEGY, "Applied strategy")
    
def strategy_awaiting_buy():
    stock = Stock(TEST_AWAITING_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_BUY_1)
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    test = Strategy('SMA80_SMA150', TEST_BUY_CONDITION, TEST_SELL_CONDITION)
    test.refresh([stock])
    compare(test, STRATEGY_AWAITING_BUY_BEFORE, "Awaiting buy before")
    test.refresh([stock])
    print("Reiteration: ok")
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_BUY_2)
    test.refresh([stock])
    compare(test, STRATEGY_AWAITING_BUY_AFTER, "Awaiting buy after")
    
def strategy_awaiting_sell():
    stock = Stock(TEST_AWAITING_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_SELL_1)
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    test = File('SMA80_SMA150', class_type = 'Strategy').load()
    test.refresh([stock])
    compare(test, STRATEGY_AWAITING_SELL_BEFORE, "Awaiting sell before")
    test.refresh([stock])    
    print("Reiteration: ok")
    stock.refresh(to_date = TEST_REFRESH_DATE_AWAITING_SELL_2)
    test.refresh([stock])
    compare(test, STRATEGY_AWAITING_SELL_AFTER, "Awaiting sell after")
    
def strategy_pass():
    stock = Stock(TEST_PASS_TRADE_STOCK)
    stock.refresh(to_date = TEST_REFRESH_DATE_PASS)
    stock.add_indicator('SMA80')
    stock.add_indicator('SMA150')
    test = Strategy('SMA80_SMA150', TEST_BUY_CONDITION, TEST_SELL_CONDITION)
    test.refresh([stock])
    compare(test, STRATEGY_PASS, "Pass strategy")
    
def send_email():
    test = AdvisorEmail(
                from_ = User(email = EMAIL, password = base64.b64decode(PWD).decode('utf-8'), name = 'Stock Advisor'), \
                to = EMAIL,
                strategy_name = 'SMA80_SMA150', \
                stocks_to_buy = ['test_stock_to_buy'], \
                stocks_to_sell = ['test_stock_to_sell'])
    test.send()
    if test.sent:
        print("Email sent: ok")
    else:
        sys.exit("Email sent: nok")
    
def main():
    quandl.ApiConfig.api_key = API_KEY
    
    if ENVIRONMENT != Env.TEST:
        print('Set environment to TEST in the constants file before running the script.')
        print('Script aborted.')
    else:  
        stock_creation()
        stock_load()
        stock_refresh()
        function_creation()
        indicator_creation()    
        indicator_add()    
        refresh_with_indicators()
        strategy_creation()    
        strategy_apply()
        strategy_awaiting_buy()         
        strategy_awaiting_sell()
        strategy_pass()
        send_email()

if __name__ == "__main__":
    main()