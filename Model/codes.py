#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:02:02 2018

"""

from Model.constants import MARKET, START_DATE
from Model.file import File

import pandas as pd
import quandl

class Codes(File):
    def __init__(self):
        super().__init__('stock_infos')
        self.data = self.load()
        
    def add(self, code, full_name, description, first_date, include_in_analysis):
        if self.code_in_base(code):
            print("code " + code + " already in base, use self.modify if you want to change this value")
        else:
             # check if code is references in Quandl
            if not test_code(code):
                print('Code is not referenced in Quandl')
                print('Data not saved')
                return None
            # check date format
            first_date = check_date_format(first_date) 
            if first_date is None: return None
            # check if include_in_analysis is yes or no
            include_in_analysis = str(include_in_analysis).lower()
            if include_in_analysis != 'yes' and include_in_analysis != 'no':
                print("Please provide a 'yes' or 'no' value for parameter 'include_in_analysis'")
                print('Data not saved')
                return None
            self.data.loc[code]([full_name, description, first_date, include_in_analysis])
            self.data = self.data.sortindex()
            self.file.save(self.data)
            
    def change_first_date(self, code, new_first_date):
        new_first_date = check_date_format(new_first_date)
        if new_first_date is None:
            return None
        else:
            if not self.code_in_base(code):
                print('Code not in base')
                print('Data not saved')
            else:
                self.data.at[code, 'FIRST_DATE'] = new_first_date
                self.file.save(self.data)

    def change_analysis_status(self, code, new_status):
        if not code_in_base(self, code):
            print('Code not in base')
            print('Data not saved')
        else:
            self.data.at[code, 'INCLUDE_FOR_ANALYSIS'] = new_status
            self.file.save(self.data)
    
    def code_in_base(self, code):
        return code in list(self.data.index)
    
    def remove(self, code):
        if not self.code_in_base(code):
            print("code " + code + " not in base.")
        else:
            self.data = self.data.drop(code)
            self.file.save(self.data)

def check_date_format(date):
    try: 
        new_date = pd.to_datetime(date)
    except ValueError as v:
        print('Error occurred : ' + v.args[0])
        print('Data not saved')
        return None
    return new_date
     
def test_code(code):
    try:
        quandl.get(MARKET + code, start_date = START_DATE)
    except:
        return False
    return True