 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 19:16:15 2018

"""

from Model.file import File

class Indicator(File):
    """ This object contains all known technical indicators.
        It is defined by a function capable of computing the indicator on a given Series"""
    
    def __init__(self, name, compute):
        super().__init__(name = name)
        self.history = {}
        self.compute = compute
        self.save(self)
        
    def __eq__(self, other):
        if isinstance(other, Indicator):
            return  self.name == other.name \
                    and self.history == other.history
        return False
                
    def apply_on_stock(self, stock, verbose = False):
        # updates stock.data with computed value of indicator
        if verbose: print("Updating indicator " + self.name + " on stock " + stock.code + "...")
        if not self.name in stock.indicators: # if the indicator is not in stock data yet, creates it
            stock.data[self.name] = None
        stock.data[self.name] = self.compute(stock.data)
        self.history[stock.name] = stock.last_date
        self.save(self)
        if verbose: print("Indicator " + self.name + " successfully updated on stock " + stock.name + "!")
    
    def drop(self, stocks):
        for stock_name in list(self.history.keys()):
            stock = File(stock_name).load()
            stock.drop_column(self.name)
            stock.save(stock)
        super().drop(self)
        