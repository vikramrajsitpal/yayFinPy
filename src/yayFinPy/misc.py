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
# - Vikramraj Sitpal
# - Tianyang Zhan

import yfinance as yf
from .enumerations import *
from .exceptions import *
from decimal import Decimal


class Misc():
    """
    A Yahoo Finance parser for currently unsupported securities.

    This module uses the yfinance API to get data for valid tickers not currently supported by yayFinPy.
    The list of currently yayFinPy supported securities are: Stock(), MutualFund(), Currency(), TreasuryBonds(), and ETF().

    Methods
    -------
    info(self)
        Get the information for the current security object.

    For more methods on the unsupported security, use the yf_ticker property and refer to ``yfinance.Ticker``

    A typical application of this class first initialize an object with a valid ticker symbol, then use the
    info() method to extract raw information.

    Example usage:
        
        try:
            security = Misc("GC=F")
            
            # fetch raw info
            info = security.info()

        except:
            print("Invalid Input Ticker")
    """

    def __init__(self, ticker_symbol: str):
        """
        The constructor of the Misc class for initializing a currently unsupported security object.
        
        Parameters
        ----------
        ticker_symbol :str
            A valid ticker symbol.
        
        Raises
        ------
        InputError
            if the input ticker_symbol is not a valid ticker.
        """
        self.__security = yf.Ticker(ticker_symbol)
        self.__quote_type = QuoteType.MISC
        try:
            self.__ticker_symbol = self.__security.info['symbol']
            self.__price = Decimal(self.__security.info['regularMarketPrice'])
        except:
            raise InputError(ticker_symbol, "Invalid Ticker: does not have either symbol OR price")
    
    @property
    def ticker_symbol(self):
        """
        Get the ticker symbol of the security.
        
        Returns
        -------
        str
            the ticker symbol of the security.
        """
        return self.__ticker_symbol
    
    @property
    def yf_ticker(self):
        """
        Get the yfinance Ticker object for the security.
        
        Returns
        -------
        yfinance.Ticker
            the initialized yfinance Ticker object.
        """
        return self.__security
    
    @property
    def quote_type(self) -> QuoteType:
        """
        Get the quote type of the security.
        
        Returns
        -------
        QuoteType
            the quote type of the security.
        """
        return self.__quote_type
    
    @property
    def price(self) -> Decimal:
        """
        Get the price of the security.
        
        Returns
        -------
        Decimal
            the quote type of the security.
        returns the current regular market price of the security.
        """
        return self.__price

    
    def info(self) -> dict:
        """
        Get the information of the security object.
        
        Returns
        -------
        dict
            the information of the security.
        """
        return self.__security.info