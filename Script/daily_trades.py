#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 20:32:34 2018

"""

import quandl
import sys
import smtplib
import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if '/Users/' in os.getcwd():
    sys.path.insert(0, os.path.expanduser("~/Documents/GitHub/Bourse/"))
elif '/home/' in os.getcwd():
    sys.path.insert(0, "/home/petermcdough/Bourse/")

from Model.constants import API_KEY, SELECTED_STRATEGY, EMAIL, PWD
from Model.exploration import load_stocks, get_strategy, refresh_stocks

def send_email(stocks_to_buy, stocks_to_sell):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL, base64.b64decode(PWD).decode('utf-8'))
    
    msg = MIMEMultipart()
    msg['From'] = "Bourse Advisor"
    msg['To'] = EMAIL
    msg['Subject'] =  SELECTED_STRATEGY + " - trades of the day"
    if stocks_to_buy is None:
        stocks_to_buy = "Aucun"
    if stocks_to_sell is None:
        stocks_to_sell = "Aucun"
    message = \
        "Stocks à acheter : " + str(stocks_to_buy) + "\n" \
        + "Stocks à vendre : " + str(stocks_to_sell)
    msg.attach(MIMEText(message))
    server.sendmail(EMAIL, EMAIL, msg.as_string())
    server.quit()

def main():
    quandl.ApiConfig.api_key = API_KEY # mandatory to make api calls on quandl
    refresh_stocks(verbose = True)
    stocks = load_stocks()
    strategy = get_strategy(SELECTED_STRATEGY)
    strategy.refresh(stocks, verbose = True)
    buy, sell = strategy.get_awaiting_trades(stocks)
    send_email(
            stocks_to_buy = [trade.stock for trade in buy],
            stocks_to_sell = [trade.stock for trade in sell])
    print("Email sent.")
    
if __name__ == "__main__":
    main()