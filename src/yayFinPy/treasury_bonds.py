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
from .enumerations import *
from .exceptions import *
import copy
from datetime import date
from decimal import *



class TreasuryBond(_BaseSecurity):
    """
    A Yahoo Finance parser for Treasury Bond securities.

    This module covers the most important attributes of a Treasury Bond security:
    name, age, returns, returns_percentage;

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
            tb = TreasuryBond("^TNX")
            #get bond name
            name = tb.name

            # fetch age
            tb_age = tb.age

            # calculate returns percentage
            tb_returns = tb.returns_percentage(period=Duration.YEAR_1, interval=Interval.MONTH_1)
            
        except:
            print("Invalid Input Ticker")

    """

    def __init__(self,ticker_symbol=None):
        """The constructor of the TreasuryBond class for initializing a TreasuryBond object.
		
        Parameters
        ----------
        ticker_symbol :str
          A valid ticker symbol for an TreasuryBond security.
        
        Raises
        ------
        InputError
          If the input ticker_symbol is not a valid TreasuryBond ticker or data is not retrieved.
        SecurityTypeError
          If the Security type of the ticker is other than TreasuryBond, this error is raised.
        """

        self.__ticker_symbol = ticker_symbol
        super().__init__(self.__ticker_symbol)
        try:
            self.__security = self._BaseSecurity__security
            s = self.__security.info
            if 'quoteType' in self.__security.info.keys() and QuoteType(self.__security.info['quoteType']) == QuoteType("INDEX") :
                self.__quote_type = QuoteType(s['quoteType'])
            else:
                raise SecurityTypeError(self.__ticker_symbol, "Ticker Symbol does not match Treasury Bond Security")

            self.__name = s["shortName"]
            self.__age = Decimal(s["maxAge"])
        except:
            raise InputError(ticker_symbol,"API data retrieval error")


    @property
    def name(self):
        """
        Get the name of the TreasuryBond security.
        
        Returns
        -------
        str
          the name of the TreasuryBond security.
        """      

        return self.__name

    @property
    def age(self):
        """
        Get the max age of the Treasury Bond security.
        
        Returns
        -------
        str
          the max age of the Treasury Bond security.
        """
        return self.__age


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
        Returns absolute Treasury Bond returns for period using specified interval.

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
            absolute Treasury Bond return amount.
        """      
        return Decimal(self.__calculate_returns(period,interval,False,start,end))

    def returns_percentage(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1,
                start:date = None, end:date = None):
        """
        Returns percentage of Treasury Bond returns for period using specified interval.

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
            percentage return of a Treasury Bond.
        """     
        return Decimal(self.__calculate_returns(period,interval,True,start,end))