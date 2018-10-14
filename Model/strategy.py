#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:51:05 2018

"""

from Model.file import File
from Model.trade import Trade, open_trade

import pandas as pd

class Strategy(File):
    def __init__(self, name, buy_condition, sell_condition, description = ''):
        super().__init__(name = name)
        self.description = description
        self.buy_condition = buy_condition
        self.sell_condition = sell_condition
        self.trades = []
        self.history = {}
        self.last_status = {}
        self.save(self)
        
    def __eq__(self, other):
        if isinstance(other, Strategy):
            return  self.trades == other.trades \
                    and self.name == other.name \
                    and self.history == other.history \
                    and self.last_status == other.last_status
        return False
    
    def print_trades(self):
        text = "Name : " + self.name + "\n"
        text = text + "Last refresh : " + str(self.last_update) + "\n"
        text = text + "OPENING_DATE\t\tCLOSING_DATE\t\tSTOCK\tSTATUS\t\tBID\tLAST\tPERF\n"
        for trade in self.trades:
            text = text + Trade.__repr__(trade) + "\n"
        print(text)
       
    def add_trade(self, trade):
        self.trades.append(trade)
        
    def drop_trade(self, trade):
        self.trades.remove(trade)
        self.save(self)
        
    def refresh(self, stocks, verbose = False):
        self.handle_awaiting_trades(stocks)
        for stock in stocks:
            if not self.name in stock.strategies:
                stock.strategies.append(self.name)
                stock.save(stock)
            if not self.contains(stock):
                self.initialize(stock)
            while self.history[stock.name] < stock.last_date:
                data_to_update = stock.data[self.history[stock.name]:]
                iterator = data_to_update.itertuples()
                row = iterator.__next__()
                if self.last_status[stock.name] == 'awaiting buy':
                    self.order.sell(row, self.get_awaint)
                if self.last_status[stock.name] == 'pending':
                    trade = self.get_pending_trade(stock)
                    try:
                        while not self.sell_condition(stock, row, trade)['state']:
                            row = iterator.__next__()
                        selling_date = self.sell_condition(stock, row, trade)['date']
                        selling_price = self.sell_condition(stock, row, trade)['price']
                        if selling_price is None:
                            selling_price = row.CLOSE
                            status = 'awaiting_sell'
                        else:
                            status = 'pending'
                        self.sell(trade = trade, date = selling_date, price = selling_price, status = status)
                    except StopIteration:
                        trade.update_price(row.CLOSE)
                elif self.last_status[stock.name] == 'closed':
                    try:
                        while not self.buy_condition(stock, row)['state']:
                            row = iterator.__next__()
                        buying_date = self.buy_condition(stock, row)['date']
                        buying_price = self.buy_condition(stock, row)['price']
                        if buying_price is None:
                            status = 'awaiting buy'
                        else:
                            status = 'pending'
                        self.buy(stock = stock, date = buying_date, price = buying_price, status = status)
                    except StopIteration:
                        pass
                elif self.last_status[stock.name] == 'pass':
                    try:
                        while self.buy_condition(stock, row)['state']:
                            row = iterator.__next__()
                        self.last_status[stock.name] = 'closed'
                    except StopIteration:
                        pass
                self.history[stock.name] = row.Index
        self.save(self)
        if verbose: print('Trades for strategy ' + str(self.name) + ' successfully updated.')
    
    def buy(self, stock, date, price, status):
        trade = open_trade(opening_date = date, stock = stock, bid_price = price, status = status)
        self.last_status[stock.name] = status
        self.add_trade(trade)
    
    def sell(self, trade, date, price, status):
        if status == 'awaiting_sell':
            trade.awaiting_sell(last_price = price, closing_date = date)
            self.last_status[trade.stock]= 'awaiting_sell'
        else:
            trade.close(closing_date = date, closing_price = price)
            self.last_status[trade.stock] = 'pass'       
    
    def contains(self, stock):
        return stock.name in self.last_status.keys()

    def initialize(self, stock):
        self.history[stock.name] = stock.first_date
        self.last_status[stock.name] = 'pass'
    
    def handle_awaiting_trades(self, stocks):
        awaiting_buys, awaiting_sells = self.get_awaiting_trades(stocks)
        for trade in awaiting_buys:
            trade.buy_awaiting()
            self.last_status[trade.stock] = 'pending'
        for trade in awaiting_sells:
            trade.sell_awaiting()
            self.last_status[trade.stock] = 'pass'
        
    def get_awaiting_trades(self, stocks):
        awaiting_buys = [t for t in self.trades if t.status == 'awaiting buy' and t.stock in [s.name for s in stocks]]
        awaiting_sells = [t for t in self.trades if t.status == 'awaiting sell' and t.stock in [s.name for s in stocks]]
        return (awaiting_buys, awaiting_sells)
    
    def get_pending_trade(self, stock):
        return [t for t in self.trades if t.status == 'pending' and t.stock == stock.name][0]
    
    def get_closed_trades(self):
        return [t for t in self.trades if t.status == 'closed']
    
    def average_trade_duration(self):
        df = self.to_dataframe()
        df = df[df.STATUS == 'closed']
        return (df.CLOSING_DATE - df.OPENING_DATE).dt.days.sum() / len(df)
    
    def best(self, limit = 5):
        df = self.to_dataframe()
        return df.sort_values(by=["PERFORMANCE"], ascending=False)[:limit]
    
    def worst(self, limit = 5):
        df = self.to_dataframe()
        return df.sort_values(by=["PERFORMANCE"], ascending=True)[:limit]
    
    def won(self):
        return [t for t in self.trades if t.performance > 1]
    
    def lost(self):
        return [t for t in self.trades if t.performance < 1]
        
    def to_dataframe(self):
        df = pd.DataFrame(columns = ['OPENING_DATE', 'CLOSING_DATE', 'STOCK_NAME', 'STATUS', 'BID_PRICE', 'LAST_PRICE', 'PERFORMANCE'])
        i = 0
        for trade in self.trades:
            df.loc[i] = [trade.opening_date, trade.closing_date, trade.stock, trade.status, trade.bid_price, trade.last_price, trade.performance]
            i = i+1
        return df
    
    def summary(self):
        print(self.name + " : " + str(round(self.global_performance(), 2)) + "% in " + str(len(self.trades)) + " trades.")
        print("Average trade duration : " + str(self.average_trade_duration()) + " days.")
        print("Number of won trades : " + str(len(self.won())))
        print("Number of lost trades : " + str(len(self.lost())))
        print("Best trades")
        print(self.best().to_string())
        print("Worst trades")
        print(self.worst().to_string())
        print()
        
    def global_performance(self):
        df = self.to_dataframe()
        return df.PERFORMANCE.sum() - len(df)