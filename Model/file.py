#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:23:44 2018

"""

from Model.constants import ENVIRONMENT, SAVE_FOLDER
from Model.env import Env

import os
import dill as pickle
import pandas as pd
import datetime


class File:
    def __init__(self, name, class_type = None):
        self.name = name
        if class_type is None:
            self.type = self.__class__.__name__
        else:
            self.type = class_type
        self.env = ENVIRONMENT
        self.filename = self.env.value + self.type + "/" + self.name + ".p"
        self.folder = SAVE_FOLDER
        self.path = self.folder + self.filename
        self.creation_date = pd.to_datetime(datetime.datetime.now().replace(microsecond = 0))
        self.last_update = self.creation_date
            
    def __eq__(self, other):
        if isinstance(other, File):
            return  self.name == other.name \
                    and self.type == other.type \
                    and self.env == other.env \
                    and self.filename == other.filename \
                    and self.folder == other.folder \
                    and self.path == other.path
        return False
        
    def __repr__(self):
        if self.env == Env.PROD:
            return self.type + " : " + self.name
        else:
            return self.type + " : " + self.name + ' (' + self.env.name + ')'
        
    def drop(self):
        os.remove(self.path)

    def load(self):
        return pickle.load(open(self.path, "rb" ))

    def save(self, obj):
        pickle.dump(obj, open(self.path, "wb" ))
        self.last_update = pd.to_datetime(datetime.datetime.now().replace(microsecond = 0))
        
    def get_attributes(self):
        for (k,v) in self.__dict__.items():
            print(k + ' : ' + str(v))
    