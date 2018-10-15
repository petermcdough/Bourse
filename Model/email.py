#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:00:07 2018

"""

import os
import sys
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if '/Users/' in os.getcwd():
    sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/Bourse/"))
elif '/home/' in os.getcwd():
    sys.path.insert(0, "/home/petermcdough/Bourse/")
    
from Model.file import File

class User():
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self.name == other.name \
                    and self.email == other.email \
                    and self.password == other.password
        return False   

class Email(File):
    def __init__(self, from_, to, subject, message, name = None):
        if name is None:
            name = str(datetime.datetime.now().date())
        super().__init__(name = name)
        self.from_ = from_
        self.to = to
        self.subject = subject
        self.message = message
        self.sent = False
        self.save(self)
    
    def send(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.from_.email, self.from_.password)
        msg = MIMEMultipart()
        msg['From'] = self.from_.name
        msg['To'] = self.to
        msg['Subject'] =  self.subject
        msg.attach(MIMEText(self.message))
        server.sendmail(self.from_.name, self.to, msg.as_string())
        server.quit()
        self.sent = True
        self.save(self)

class AdvisorEmail(Email):
    def __init__(self, from_, to, strategy_name, stocks_to_buy, stocks_to_sell):
        self.stocks_to_buy = stocks_to_buy
        self.stocks_to_sell = stocks_to_sell
        self.strategy_name = strategy_name
        if self.stocks_to_buy is None:
            stocks_to_buy = "Aucun"
        else:
            stocks_to_buy = self.stocks_to_buy
        if self.stocks_to_sell is None:
            stocks_to_sell = "Aucun"
        else:
            stocks_to_sell = self.stocks_to_sell
        message = \
            "Stocks à acheter : " + str(stocks_to_buy) + "\n" \
            + "Stocks à vendre : " + str(stocks_to_sell)
        super().__init__(from_ = from_, to = to, subject = self.strategy_name + " - trades of the day", message = message)
    
    def __eq__(self, other):
        if isinstance(other, AdvisorEmail):
            return super().__eq__(other) \
                    and self.from_ == other.from_\
                    and self.to == other.to \
                    and self.subject == other.subject \
                    and self.message == other.message \
                    and self.strategy_name == other.strategy_name \
                    and self.stocks_to_buy == other.stocks_to_buy \
                    and self.stocks_to_sell == other.stocks_to_sell
        return False        