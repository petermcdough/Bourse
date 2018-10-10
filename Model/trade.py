#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 12:21:51 2018

@author: hugofayolle
"""

from Model.file import File
from Model.constants import TAX
import numpy as np

class Trade:
    def __init__(self, opening_date, closing_date, stock, status, bid_price, last_price):
        self.opening_date = opening_date
        self.closing_date = closing_date
        self.stock = stock.name
        self.status = status
        self.bid_price = bid_price
        self.last_price = last_price
        self.performance = self.get_performance()
        
    def __eq__(self, other):
        if isinstance(other, Trade):
            return  self.opening_date == other.opening_date \
                    and self.closing_date == other.closing_date \
                    and self.stock == other.stock \
                    and self.status == other.status \
                    and self.bid_price == other.bid_price \
                    and self.last_price == other.last_price \
                    and self.performance == other.performance
        return False
        
    def __repr__(self):
        if self.performance is None:
            performance = " "
        else:
            performance = str(np.round((self.performance - 1)*100,3)) + "%"
        text = str(self.opening_date) + '\t'
        text = text + str(self.closing_date)
        if self.closing_date is None:
            text = text + "\t\t"
        text = text + "\t"
        text = text + str(self.stock) + '\t'
        text = text + self.status + '\t'
        if self.status != 'awaiting buy' and self.status != 'awaiting sell':
            text = text + '\t'
        text = text + str(self.bid_price) + '\t' \
                + str(self.last_price) + '\t' \
                + performance
        return text
            
    def get_performance(self):
        if self.bid_price is None:
            return None
        else:
            return self.last_price / self.bid_price * (1 - TAX) * (1 - TAX)
    
    def buy_awaiting(self):
        stock = File(self.stock, "Stock").load()
        position = stock.data.index.get_loc(self.opening_date)
        if position + 1 < len(stock.data):
            bid_price = stock.data.iloc[position + 1].OPEN
            self.set_bid_price(bid_price)
            self.set_opening_date(stock.data.iloc[position + 1].name)
            self.update_price(bid_price)
            self.change_status('pending')
    
    def sell_awaiting(self):
        stock = File(self.stock, "Stock").load()
        position = stock.data.index.get_loc(self.closing_date)
        if position + 1 < len(stock.data):
            self.close(stock.data.iloc[position + 1].name, stock.data.iloc[position + 1].OPEN)
            
    def awaiting_sell(self, last_price, closing_date):
        self.closing_date = closing_date
        self.update_price(last_price)
        self.change_status('awaiting sell')

    def close(self, closing_date, closing_price):
        self.closing_date = closing_date
        self.update_price(closing_price)
        self.status = 'closed'
        
    def set_bid_price(self, bid_price):
        self.bid_price = bid_price
    
    def set_opening_date(self, opening_date):
        self.opening_date = opening_date
        
    def change_status(self, status):
        self.status = status
    
    def get_key(self):
        return self.stock, self.status
    
    def update_price(self, last_price):
        self.last_price = last_price
        self.performance = self.get_performance()
                            
def open_trade(opening_date, stock, bid_price, status = 'pending'):
    return Trade(
            opening_date = opening_date,
            closing_date = None,
            stock = stock,
            status = status,
            bid_price = bid_price,
            last_price = bid_price)