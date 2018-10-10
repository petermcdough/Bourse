#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:39:19 2018

@author: hugofayolle
"""

from Model.env import Env

API_KEY = "WkHc4vJGHBT4Xtuma14T" # API key to access quandl
MARKET = 'EURONEXT/'             # prefix of the code of a stock
TAX = 0.0004                     # tax (percentage) applied when buying / selling stock
FIGSIZE = (15,6)                 # dimensions of plots
LOCAL = True
if LOCAL:    
    SAVE_FOLDER = "/Users/hugofayolle/Desktop/Bourse/Bourse/Data/"
else:
    SAVE_FOLDER = "/home/hugofayolle/Bourse/Data/"
TEST_FOLDER = SAVE_FOLDER + "Test/Test_set/"
START_DATE = "2014-01-01"
ENVIRONMENT = Env.DEV
SELECTED_STRATEGY = 'SMA80_SMA150'
EMAIL = 'fdjc6590@gmail.com'
PWD = 'cEFzU3cwcmQ='

if ENVIRONMENT == Env.TEST:
    TEST_REFRESH_DATE_EMPTY = '2018-09-21'
    TEST_REFRESH_DATE_NOT_EMPTY = '2018-09-25'
    TEST_REFRESH_DATE_WITH_INDICATORS = '2018-09-28'
    TEST_REFRESH_DATE_AWAITING_BUY_1 = '2014-12-04'
    TEST_REFRESH_DATE_AWAITING_BUY_2 = '2014-12-05'
    TEST_REFRESH_DATE_AWAITING_SELL_1 = '2015-07-13'
    TEST_REFRESH_DATE_AWAITING_SELL_2 = '2015-07-14'
    TEST_REFRESH_DATE_PASS = '2018-09-21'
    TEST_STOCK = 'ORA'
    TEST_AWAITING_TRADE_STOCK = 'ORA'
    TEST_PASS_TRADE_STOCK = 'UMI'