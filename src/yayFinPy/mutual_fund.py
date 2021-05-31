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
# Implementation - 17780 by Josh Bloch and Charlie Garrod.
# 
# Authors:
# - Shubham Gupta
# - Vasudev Luthra

import yfinance as yf
import talib
from .enumerations import *
from .exceptions import *
from datetime import date
from decimal import *

class MutualFund():

    """
    A Yahoo Finance parser API for Mutual Funds.

    This module covers the most important attributes of mutual funds such as:

    Business summary,risk rating, yields, dividends, pe ratio , ytd return, holdings turnover, assets,
    price, opening price, closing price, day high, day low, exchange, ticker symbol, quote type.
    
    Methods
    -------

    download(self, period, interval, start, end, threads)
      downloads mutual fund data.
    
    historical_data(self)
      returns historical data of mutual fund price.
    
    moving_average(self)
      returns moving average of mutual fund price.

    A typical application of this class first initialize an object with a valid ticker symbol, then use the
	class properties to extract information.

	Example usage:
		
    try:
      mf = MutualFund("VFIAX")
      # fetch price
      price = mf.price

      # business summary of mutual fund
      summary = mf.business_summary()

      # Moving average of mf price
      moving_avg = mf.moving_average(duration=Duration.MONTH_1)

    except:
      print("Invalid Input Ticker")
    """
    def __init__(self, ticker):
        """
        Parameters
        ----------
        ticker : str
            The ticker symbol for a mutual fund security

        Raises
        ------
        ParsingError
          If data is not retrieved.
        InputError
          If the input ticker_symbol is not a valid Mutual Fund ticker
        SecurityTypeError
          If the Security type of the ticker is other than Mutual Fund, this error is raised.
        """

        self.__security = None
        try:
            self.__security = yf.Ticker(ticker)
        except:
            raise ParsingError(ticker, "Error in data retrieval.")

        if len(self.__security.info) <= 1:
            raise InputError(ticker, "Invalid Ticker Symbol.")

        # ticker validation
        if 'quoteType' in self.__security.info.keys() and QuoteType(self.__security.info['quoteType']) == QuoteType("MUTUALFUND") :
            self.__quote_type = QuoteType(self.__security.info['quoteType'])
        else:
            raise SecurityTypeError(self.__ticker_symbol, "Ticker Symbol does not match Mutual Fund type")
            
        try:
            self.__ticker_symbol = self.__security.info['symbol']
            self.__price = Decimal(self.__security.info['regularMarketPrice'])
            self.__close_price = Decimal(self.__security.info['regularMarketPreviousClose'])
            self.__exchange = self.__security.info['exchange']
            self.__business_summary = self.__security.info['longBusinessSummary']
            self.__expense_ratio = Decimal(self.__security.info['annualReportExpenseRatio'])
            self.__holdings_turnover = Decimal(self.__security.info['annualHoldingsTurnover'])
            self.__total_assets = Decimal(self.__security.info['totalAssets'])
            self.__overall_rating = Decimal(self.__security.info['morningStarOverallRating'])
            self.__risk_rating = Decimal(self.__security.info['morningStarRiskRating'])
            self.__yield = Decimal(self.__security.info['yield'])
            self.__ytd_return = Decimal(self.__security.info['ytdReturn'])
            self.__name = self.__security.info['shortName']
        except:
            raise YfinanceError(ticker, "Missing underlying Yfinance data.")


    def download(self, period:Duration = Duration.MONTH_1, 
                interval: Interval = Interval.DAY_1, 
                start:date = None, end:date = None, 
                threads: bool = True):
        """
        downloads price, volume data for a Mutual Fund.

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        interval: Interval, optional
            In what intervals should the data be reported (default is 1 day)
        start: date, optional
            The date from which the data is required (default is None)
        end: date, optional
            The date up to which the data is required (default is None)
        threads: bool, optional
            Should multiple threads be used to download the data (default is False)
        """
        return self.__security.download(self, period, interval, start, end,
                                        threads)

    @property
    def quote_type(self):
        """
        returns the quote type of the security (mutual fund here). (Refer to QuoteType Enum).
        """
        return self.__quote_type    
    
    @property
    def name(self):
        """
        Get the name of the mutual fund security.
        
        Returns
        -------
        str
          the name of the mutual fund security.
        """
        return self.__name

    @property
    def overall_rating(self):
        """
        Get the overall rating of the mutual fund security.
        
        Returns
        -------
        str
          the overall rating of the mutual fund security.
        """

        return self.__overall_rating

    
    @property
    def risk_rating(self):
        """
        Get the risk rating of the mutual fund security.
        
        Returns
        -------
        str
          the risk rating of the mutual fund security.
        """

        return self.__risk_rating
    
    @property
    def mf_yield(self):
        """
        Get the yield of the mutual fund security.
        
        Returns
        -------
        str
          the yield of the mutual fund security.
        """

        return self.__yield

    @property
    def ytd_return(self):
        """
        Get the ytd return of the mutual fund security.
        
        Returns
        -------
        str
          the ytd return of the mutual fund security.
        """

        return self.__ytd_return

    @property
    def total_assets(self):
        """
        Get the total assets of the mutual fund security.
        
        Returns
        -------
        str
          the total assets of the mutual fund security.
        """

        return self.__total_assets

    @property
    def holdings_turnover(self):
        """
        Get the holdings turnover of the mutual fund security.
        
        Returns
        -------
        str
          the holdings turnover of the mutual fund security.
        """

        return self.__holdings_turnover
    
    @property
    def expense_ratio(self):
        """
        Get the expense ratio of the mutual fund security.
        
        Returns
        -------
        str
          the expense ratio of the mutual fund security.
        """

        return self.__expense_ratio

    @property
    def business_summary(self):
        """
        Get the business summary of the mutual fund security.
        
        Returns
        -------
        str
          the business summary of the mutual fund security.
        """

        return self.__business_summary
    
    @property
    def ticker_symbol(self):
        """
        Get the ticker symbol of the mutual fund security.
        
        Returns
        -------
        str
          the ticker symbol of the mutual fund security.
        """
        return self.__ticker_symbol

    @property
    def price(self):
        """
        Get the current price of the mutual fund security.
        
        Returns
        -------
        str
          the current price of the mutual fund security.
        """
        return self.__price

    @property
    def closing_price(self):
        """
        Get the closing price of the mutual fund security.
        
        Returns
        -------
        str
          the closing price of the mutual fund security.
        """
        return self.__close_price

    @property
    def exchange(self):
        """
        Get the exchange of the mutual fund security.
        
        Returns
        -------
        str
          the exchange of the mutual fund security.
        """
        return self.__exchange

    def historical_data(self, duration: Duration = Duration.MONTH_1, interval: Interval = Interval.DAY_1):
        """
        returns price, volume data for a mutual fund.

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        interval: Interval, optional
            In what intervals should the data be reported (default is 1 day)
        """
        return self.__security.history(period=duration.value, interval=interval.value)

    def moving_average(self, duration: Duration = Duration.MONTH_1, timeperiod=7):
        """
        returns moving average price for a mutual fund averaged on timeperiod for given duration.

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        timeperiod: int, optional
            Time period for which the data is averaged (default is 7 days)
        """
        if timeperiod < 2:
            timeperiod = 2
        if timeperiod > 1000:
            timeperiod = 1000
        close = self.__security.history(period=duration.value)['Close']
        return talib.SMA(close, timeperiod=timeperiod)

    @property
    def dividends(self):
      """
      Returns dataframe of mutual fund security dividends.

      Returns
      -------
      Pandas.DataFrame
          dataframe of mutual fund security dividends
      """       
      return self.__security.dividends