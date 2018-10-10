#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 18:49:39 2018

@author: hugofayolle
"""

from enum import Enum

class Env(Enum):
    DEV = 'Development/'
    PROD = 'Production/'
    TEST = 'Test/'
    
    def __repr__(self):
        return 'Environment: ' + self.name
    
    def __str__(self):
        return 'Environment: ' + self.name
