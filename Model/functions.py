#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 19:09:02 2018

"""

from Model.file import File

class Function(File):
    def __init__(self, name, execute):
        super().__init__(name = name)
        self.name = name
        self.execute = execute
        self.save(self)
        
"""
def SMA(df, window, column):
   return df[column].rolling(window).mean()
    
def EMA(df, column, span):
    return df[column].ewm(span=span,min_periods=0,adjust=True,ignore_na=False).mean()
    
def MACD(df, column, span1 = 12, span2 = 26):
    return EMA(df, column, span1) - EMA(df, column, span2)
    
class Conditions:
    def MICK_BUYS(index, stock):
        focus = stock.data.loc[index-13:index]
        condition_1 = focus.iloc[-1]['MACD'] > focus.iloc[-1]['SIG_MACD']
        focus = focus[:-1]
        condition_2 = (len(focus[focus.MACD > focus.SIG_MACD]) == len(focus))
        condition_3 = (len(focus[focus.MACD > focus.SIG_MACD]) == 0)
        return condition_1 and (condition_2 or condition_3)
    
    def MICK_SELLS(index, stock, position):
        focus = stock.data[index-13:index]
        condition_1 = focus.iloc[-1]['MACD'] < focus.iloc[-1]['SIG_MACD']
        focus = focus[:-1]
        condition_2 = (len(focus[focus.MACD > focus.SIG_MACD]) == len(focus))
        condition_3 = (len(focus[focus.MACD > focus.SIG_MACD]) == 0)
        return condition_1 and (condition_2 or condition_3)
    
    def SMA_BUY(index, stock, SMA_1, SMA_2):
        focus = stock.data.loc[index]
        condition = focus[SMA_1] > focus[SMA_2]
        return condition
    
    def SMA_SELL(index, stock, SMA_1, SMA_2):
        focus = stock.data.loc[index]
        condition = focus[SMA_1] > focus[SMA_2]
        return condition
    
    def SOPHIE_BUYS(index, stock):
        focus = stock.data.loc[index]
        condition = focus['SMA20'] > focus['SMA50']
        return condition
    
    def SOPHIE_SELLS(index, stock, position):
        focus = stock.data.loc[index]
        condition = focus['SMA20'] < focus['SMA50']
        return condition
    
    def SAM_BUYS(index, stock):
        focus = stock.data.loc[index]
        condition = focus['SMA50'] > focus['SMA100']
        return condition
    
    def SAM_SELLS(index, stock, position):
        focus = stock.data.loc[index]
        condition = focus['SMA50'] < focus['SMA100']
        return condition
    
    def SAM_SELLS_AUGMENTED(index, stock, position):
        index_opening_date = stock.data[stock.data.DATE == position.opening_date].index[0]
        delta_indexes = index - index_opening_date
        if delta_indexes == 24:
            condition_1 = (stock.data.at[index, 'CLOSE'] < position.buying_price)
        else :
            condition_1 = False
        return condition_1 or Conditions.SAM_SELLS(index, stock, position)
    
    def SIMON_BUYS(index, stock):
        focus = stock.data.loc[index]
        condition = focus['SMA20'] > focus['SMA100']
        return condition
    
    def SIMON_SELLS(index, stock, position):
        focus = stock.data.loc[index]
        condition = focus['SMA20'] < focus['SMA100']
        return condition
    
    def SIMON_SELLS_AUGMENTED(index, stock, position):
        index_opening_date = stock.data[stock.data.DATE == position.opening_date].index[0]
        delta_indexes = index - index_opening_date
        if delta_indexes == 24:
            condition_1 = (stock.data.at[index, 'CLOSE'] < position.buying_price)
        else :
            condition_1 = False
        return condition_1 or Conditions.SIMON_SELLS(index, stock, position)"""