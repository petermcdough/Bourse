#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 20:32:34 2018

"""

import quandl
import sys
import base64
import os

if '/Users/' in os.getcwd():
    sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/Bourse/"))
elif '/home/' in os.getcwd():
    sys.path.insert(0, "/home/petermcdough/Bourse/")

from Model.constants import API_KEY, SELECTED_STRATEGY, EMAIL, PWD
from Model.email import AdvisorEmail, User
from Model.exploration import load_stocks, get_strategy, refresh_stocks

def main():
    quandl.ApiConfig.api_key = API_KEY # mandatory to make api calls on quandl
    refresh_stocks(verbose = True)
    stocks = load_stocks()
    strategy = get_strategy(SELECTED_STRATEGY)
    strategy.refresh(stocks, verbose = True)
    buy, sell = strategy.get_awaiting_trades(stocks)
    email = AdvisorEmail( \
                from_ = User(email = EMAIL, password = base64.b64decode(PWD).decode('utf-8'), name = 'Stock Advisor'), \
                to = EMAIL,
                strategy_name = SELECTED_STRATEGY, \
                stocks_to_buy = [trade.stock for trade in buy], \
                stocks_to_sell = [trade.stock for trade in sell])
    email.send()
    
if __name__ == "__main__":
    main()