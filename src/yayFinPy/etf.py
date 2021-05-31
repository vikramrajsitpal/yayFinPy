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

from .base import _BaseSecurity
from .exceptions import *
from .enumerations import *
import copy
from decimal import *
from datetime import date
   
class ETF(_BaseSecurity):

    """
    A Yahoo Finance parser for ETF securities.

    This module covers the most important attributes of an ETF security:
    name, summary, dividends, bid, ask, bid size, ask size, assets, returns, returns_percentage;

    And attributes common to all Securities:
    price, opening price, closing price, volume, day high, day low, exchange, ticker symbol, quote type.

    For more methods on the security, refer to ``base._BaseSecurity``


    Methods
    -------
    returns(self,period,interval,start_date,end_date)
        returns stock returns for a specific period and interval

    returns_percentage(self,period,interval,start_date,end_date)
        returns stock returns in percentage for specific period and interval

    
    A typical application of this class first initialize an object with a valid ticker symbol, then use the
	class properties to extract information.
	
    Example usage:
		
		try:
			etf = ETF("SPY")
			# fetch dividends
			dividends_df = etf.dividends

            # calculate returns
            etf_returns = etf.returns(period=Duration.YEAR_1, interval=Interval.MONTH_1)

            # get etf assets
			assets = etf.assets
            
		except:
			print("Invalid Input Ticker")

    """

    def __init__(self,ticker_symbol=None):
        """The constructor of the ETF class for initializing an ETF object.
		
        Parameters
        ----------
        ticker_symbol :str
          A valid ticker symbol for an ETF security.
        
        Raises
        ------
        InputError
          If the input ticker_symbol is not a valid ETF ticker or data is not retrieved.
        SecurityTypeError
          If the Security type of the ticker is other than ETF, this error is raised.
        """

        self.__ticker_symbol = ticker_symbol
        super().__init__(self.__ticker_symbol)
        try:
            self.__security = self._BaseSecurity__security
            if 'quoteType' in self.__security.info.keys() and QuoteType(self.__security.info['quoteType']) == QuoteType("ETF") :
                self.__quote_type = QuoteType(self.__security.info['quoteType'])
            else:
                raise SecurityTypeError(self.__ticker_symbol, "Ticker Symbol does not match ETF Security")

            s = self.__security.info
            self.__business_summary = s["longBusinessSummary"]
            self.__name = s["shortName"]
            self.__dividends = self.__security.dividends
            self.__ask = Decimal(s["ask"])
            self.__ask_size = Decimal(s["askSize"])
            self.__bid = Decimal(s["bid"])
            self.__bid_size = Decimal(s["bidSize"])
            self.__assets = Decimal(s["totalAssets"])
        except:
            raise InputError(ticker_symbol,"API data retrieval error")

    @property
    def name(self):
        """
        Get the name of the ETF security.
        
        Returns
        -------
        str
          the name of the ETF security.
        """

        return self.__name

    @property
    def summary(self):
        """
        Get the business summary of the ETF security.
        
        Returns
        -------
        str
          the business summary of the ETF security.
        """

        return self.__business_summary


    @property
    def dividends(self):
        """
        Returns dataframe of ETF security dividends.

        Returns
        -------
        Pandas.DataFrame
            dataframe of ETF security dividends
        """        
        return copy.deepcopy(self.__dividends)


    @property
    def ask(self):
        """
        Get the ask price of the ETF security.
        
        Returns
        -------
          the ask of the ETF security.
        """
        return self.__ask

    @property
    def ask_size(self):
        """
        Get the ask size of the ETF security.
        
        Returns
        -------
        Decimal
          the ask size of the ETF security.
        """
        return self.__ask_size
    
    @property
    def bid(self):
        """
        Get the bid price of the ETF security.
        
        Returns
        -------
        Decimal
          the bid of the ETF security.
        """
        return self.__bid

    @property
    def bid_size(self):
        """
        Get the bid size of the ETF security.
        
        Returns
        -------
        Decimal
          the bid size of the ETF security.
        """    

        return self.__bid_size

    @property
    def assets(self):
        """
        Get the current total assets of the ETF security.
        
        Returns
        -------
        Decimal
          the current total assets of the ETF security.
        """   

        return self.__assets
    

    def __calculate_returns(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1, percentage = False,
                start:date = None, end:date = None):
   
        historic_data = self.historical_data(duration=period,interval=interval)
        open_price = historic_data.iloc[0]["Open"]
        close_price = historic_data.iloc[-1]["Close"]
        total_return = close_price - open_price
        if not percentage:
            return total_return
        else:
            return (total_return/open_price) * 100

    def returns(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1, 
                start:date = None, end:date = None):
        """
        Returns absolute ETF returns for period using specified interval.

        Parameters
        ----------
        period : Duration, optional
            Time period for returns, by default Duration.YEAR_1
        interval : Interval, optional
            Interval for return calculation, by default Interval.MONTH_1
        start : date, optional
            end date for return duration, by default None, use Duration
        end : date, optional
            end date for return duration, by default None, use Duration

        Returns
        -------
        Decimal
            absolute ETF return amount.
        """     
        return Decimal(self.__calculate_returns(period,interval,False,start,end))

    def returns_percentage(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1,
                start:date = None, end:date = None):
        """
        Returns percentage ETF returns for period using specified interval.

        Parameters
        ----------
        period : Duration, optional
            Time period for returns, by default Duration.YEAR_1
        interval : Interval, optional
            Interval for return calculation, by default Interval.MONTH_1
        start : date, optional
            end date for return duration, by default None, use Duration
        end : date, optional
            end date for return duration, by default None, use Duration

        Returns
        -------
        Decimal
            percentage return of an ETF.
        """       
        return Decimal(self.__calculate_returns(period,interval,True,start,end))