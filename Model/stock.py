#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 18:58:42 2018

"""

import datetime
import quandl                         # handles financial api
import pandas as pd

from Model.file import File
from Model.constants import MARKET    # configuration
from Model.codes import Codes
from Model.env import Env

class Stock(File):
    def __init__(self, code):
        codes = Codes()
        if not codes.code_in_base(code):
            print("Code " + code + " is not referenced in Quandl")
            print("Stock not created")
            return None
        super().__init__(name = code)
        self.data = pd.DataFrame()
        self.code = code
        self.full_code = MARKET + code
        self.full_name = codes.data.at[code, 'FULL_NAME']
        self.description = codes.data.at[code, 'DESCRIPTION']
        self.first_date = codes.data.at[code, 'FIRST_DATE']
        self.include_in_analysis = codes.data.at[code, 'INCLUDE_FOR_ANALYSIS']
        self.indicators = []
        self.strategies = []
        self.last_date = None
        self.save(self)
        
    def __eq__(self, other):
        if isinstance(other, Stock):
            is_data_equal = True
            for column in self.data.columns:
                is_data_equal = is_data_equal and self.data[column].equals(other.data[column])
            for column in other.data.columns:
                is_data_equal = is_data_equal and self.data[column].equals(other.data[column])
            return super().__eq__(other) \
                    and is_data_equal \
                    and self.code == other.code \
                    and self.full_code == other.full_code \
                    and self.first_date == other.first_date \
                    and self.include_in_analysis == other.include_in_analysis \
                    and self.indicators == other.indicators \
                    and self.strategies == other.strategies \
                    and self.last_date == other.last_date
        return False
        
    def add_indicator(self, indicator_name):
        indicator = File(indicator_name, class_type = "Indicator").load()
        indicator.apply_on_stock(self)
        if not (indicator_name in self.indicators):
            self.indicators.append(indicator.name)
        self.save(self)
        
    def get_position(self, date):
        # returns the position of a given date within stock data
        return self.data.index.get_loc(date)
        
    def refresh(self, verbose = False, replace = False, to_date = None):
        # updates stock data with the latest data from quandl, computes indicators for the new values and computes orders for all strategies in Strategy
        if replace: self.__init__(self.code, self.indicators, self.strategies)
        if not self.uptodate():
            df = self.get_data_from_api()[:to_date]
            self.data = pd.concat([self.data, df]).reset_index().drop_duplicates(subset='DATE', keep='first').set_index('DATE')
            self.last_date = self.data.iloc[-1].name
            
            for indicator_name in self.indicators:
                indicator = File(indicator_name, class_type = 'Indicator').load()
                indicator.apply_on_stock(self)
                
            """for strategy in self.strategies:
                strategy.apply_on_stock(self, verbose)
            self._set_last_refresh()"""
            
            self.save(self)
            if verbose: print(self.code + " successfully updated!")
 
    def get_data_from_api(self):
        # returns dataframe from quandl api and formats it
        i = 0
        while i < 10:
            try:
                df = quandl.get(self.full_code, start_date=self.first_date)
            except Exception:
                i = i + 1
                if i == 10:
                    print('Max attempts reached')
                    print('Execution failed on stock : ' + self.code)
                    return None
                print('Error on stock : ' + self.code)
                print('Attempt ' + str(i))
                continue
            break
        df = df.reset_index()
        df = df.rename(index=str, columns={
            'Date':'DATE',
            'Open':'OPEN',
            'High':'HIGH',
            'Low':'LOW',
            'Last':'CLOSE',
            'Volume':'VOLUME',
            'Turnover':'TURNOVER'
        })
        df.DATE = pd.to_datetime(df.DATE)
        df = df.set_index('DATE')
        df = df.fillna(method = 'ffill')
        return df   
    
    def uptodate(self):
        if self.last_date is None: return False
        if self.env == Env.TEST or self.env == Env.DEV: return False
        last_update = pd.to_datetime(self.last_update.date())
        last_date = pd.to_datetime(self.last_date.date())
        today = pd.to_datetime(datetime.datetime.now().date())
        if last_update == today:
            return True
        elif today.weekday == 0:
            if (today-last_date).days == 3 and datetime.datetime.now().hour < 18:
                return True
        elif today.weekday == 5 and (today-last_date).days == 1:
            return True
        elif today.weekday == 6 and (today-last_date).days == 2:
            return True
        elif (today-last_date).days == 1 and datetime.datetime.now().hour < 18:
            return True
        else:
            return False 