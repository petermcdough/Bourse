#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 19:15:20 2018

"""

from Model.file import File

class Order(File):
    """ This object contains all functions that define the way an order is passed"""
    def __init__(self, name, buy_model, sell_model):
        super().__init__(name = name)
        self.buy = buy_model
        self.sell = sell_model
        self.save(self)