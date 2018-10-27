#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:39:19 2018

"""

from Model.env import Env

import os

if '/Users/' in os.getcwd():    
    SAVE_FOLDER = os.path.expanduser("~/Documents/GitHub/Bourse/Data/")
elif '/home/' in os.getcwd():
    SAVE_FOLDER = "/home/petermcdough/Bourse/Data/"
else:
    print("Error, path not recognized.")

API_KEY = "WkHc4vJGHBT4Xtuma14T" # API key to access quandl
MARKET = 'EURONEXT/'             # prefix of the code of a stock
TAX = 0.0004                     # tax (percentage) applied when buying / selling stock
FIGSIZE = (15,6)                 # dimensions of plots
TEST_FOLDER = SAVE_FOLDER + "Test/Test_set/"
START_DATE = "2014-01-01"
ENVIRONMENT = Env.PROD
SELECTED_STRATEGY = 'SMA80_SMA150_STOCHASTICS'
EMAIL = 'fdjc6590@gmail.com'
PWD = 'cEFzU3cwcmQ='
DEV_REFRESH_DATE = '2018-10-19'

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