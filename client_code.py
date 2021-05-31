#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Part of academic course project at CMU in the course API Design and 
# Implmentation - 17780 by Josh Bloch and Charlie Garrod.
# 
# Author:
# - Tianyang Zhan

import matplotlib.pyplot as plt
from decimal import *
from datetime import date
from yayFinPy.portfolio import Portfolio, PortfolioInfo
from yayFinPy.currency import Currency
from yayFinPy.enumerations import *
from yayFinPy.exceptions import *

# download data
currency = Currency("CNY=X")
data = currency.download_data(duration=Duration.MONTH_1, interval=Interval.DAY_1,
						start=date(2021,1,1), end=date(2021,5,15),
						threads=False)

# manage portfolio
portfolio = Portfolio({
						"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000)), # currency
						"QASGX": PortfolioInfo(qty=Decimal(50), buying_price=Decimal(31)), # mutual fund
						"^TNX": PortfolioInfo(qty=Decimal(1000), buying_price=Decimal(1.55)), # treasury bond
						"GOOG": PortfolioInfo(qty=Decimal(10), buying_price=Decimal(2300)), # stock
						"VFH": PortfolioInfo(qty=Decimal(50), buying_price=Decimal(90)), # etf
					})

portfolio.add_to_portfolio("AAPL", qty=Decimal(10), buying_price=Decimal(2300)) # stock

# show protfolio info
print("Value: %f, Returns: %f"%(portfolio.value(), portfolio.returns()))
diversification_df = portfolio.diversification()
print(diversification_df)


# analyze individual assets
assets = portfolio.get_portfolio_objects()
# get currency info
crypto_btc = assets["BTC-USD"]
print("Base Currency=%s, Quote Currency=%s, Price=%f\n\n" 
					%(crypto_btc.base_currency, crypto_btc.quote_currency, crypto_btc.price))
# get stock info
stock_goog = assets["GOOG"]
print(stock_goog.company_data)
print("Price=%f, PE_Ratio=%f\n\n"%(stock_goog.price, stock_goog.pe_ratio))


# technical indicators and visualizations
bop = stock_goog.balance_of_power(duration=Duration.YEAR_1)
std = stock_goog.standard_deviation(duration=Duration.YEAR_5, timeperiod=100, dev=Multiplier.TWICE)
plt.plot(std)
plt.show()