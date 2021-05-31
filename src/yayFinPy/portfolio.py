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
# Author:
# - Vikramraj Sitpal
# - Tianyang Zhan

from .misc import Misc
from .etf import ETF
from .stock import Stock
from .mutual_fund import MutualFund
from .treasury_bonds import TreasuryBond
from .currency import Currency
from .exceptions import *
from .enumerations import *
from decimal import *
from datetime import date
from decimal import Decimal
import yfinance as yf
import pandas as pd
from numpy import NaN as nan
from collections import namedtuple, OrderedDict


PortfolioInfo = namedtuple('PortfolioInfo', ['qty', 'buying_price'])
PortfolioInfo.__doc__ = """
Named Tuple PortfolioInfo
qty -> Quantity of the Security in portfolio
buying_price -> buying price of the security in portfolio
"""


class Portfolio():
    """
    A Portfolio class exposed as a module to create and analyse a custom
    portfolio. It can take any valid security type as input.

    This is the only mutable class in the entire API as someone's Portfolio
    can keep changing.

    One can initialise a Portfolio object using a pre-defined dictionary 
    format or can call the methods to add securities one by one.

    A Portfolio, in simple terms, is a group of securities which has a value
    equal to combined value of all its component securities.

    Note: qty -> Quantity

	Methods
	-------
	diversification(self)
        Shows diversification within the Portfolio

	as_dataframe(self)
        Returns the Portfolio information as pandas DataFrame

    add_to_portfolio(self, ticker: str, qty: Decimal, buying_price: Decimal = None)
        Adds a security to portfolio

    remove_from_portfolio(self, ticker: str)
        Removes a security from portfolio

    update_qty(self, ticker: str, new_qty: Decimal)
        Updates the quantity of a particular security

    update_buying_price(self, ticker: str, buying_price: Decimal)
        Updated buying prices of a particular security

    returns(self)
        Returns the current gain/loss (if negative) based on buying price
        and the current value of the Portfolio

    value(self)
        Returns the total value of the Portfolio

    get_portfolio_objects(self)
        Returns individual objects of the security on which more analysis can
        be done

    get_portfolio_info(self)
        Returns Portfolio information as a dictionary in a specific format as
        was taken in input

	Example usage:
		
        portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000)), "JPY=X": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(10))})

        returns = portfolio.returns()
		value = portfolio.value()

        assets = portfolio.get_portfolio_objects()

        portfolio.update_qty("BTC-USD", Decimal(2))
		portfolio.update_buying_price("BTC-USD", Decimal(47000))
		p_info = portfolio.get_portfolio_info()

        portfolio.remove_from_portfolio("JPY=X")

    """

    def __init__(self, tkr_qty_bp: dict = None):
        """
        The constructor of the Portfolio class for initializing a Portfolio object.

        Creates new Data structures.
        Parameters
		----------
		tkr_qty_bp :dict, optional
			A valid dictionary with:
                key: str -> ticker
                value: (quantity: Decimal, buying price: Decimal) PortfolioInfo
                named tuple
		
		Raises
		------
		InputError
			if the input key in the dict is not a valid ticker.
		ParsingError
			if the failure occurs when parsing data using the input dict. 
        """
        self.__portfolio = dict()
        self.__portfolio_objs = dict()
        self.__portfolio_bp = dict()
        
        if tkr_qty_bp:
            for t, ps in tkr_qty_bp.items():
                self.add_to_portfolio(t, ps.qty, ps.buying_price)
        

    def __str__(self):
        """
        Returns
        -------
        str
            Print the Portfolio as string
        """

        s = "Security\tType\Quantity\tBuying Price\n=====================================================\n"


        for t, o in self.__portfolio.items():
            s += t + "\t"
            s += self.__portfolio_objs[t].quote_type.value + "\t"
            s += str(o) + "\t"
            if self.__portfolio_bp[t] is None:
                s += "NA\t"
            else:
                s += str(self.__portfolio_bp[t]) + "\n"

        return s

    def diversification(self) -> pd.DataFrame:
        """
        Returns
        -------
        pandas.DataFrame
            Shows how diverse the portfolio is based on the data.
            Calculates the percentage per security group as per its current value wrt the entire portfolio.
            Serves to show well as well as be used as data-structure to use
            values.
        """
        df_dict = OrderedDict()
        df_dict["Security Type"] = []
        df_dict["Current Value"] = []
        for t, val in self.__portfolio_objs.items():
            df_dict["Security Type"].append(val.quote_type.value)
            df_dict["Current Value"].append(val.price * self.__portfolio[t])
        
        df = pd.DataFrame(df_dict)
        df_sum = df.groupby(["Security Type"]).agg({'Current Value': 'sum'})

        df_sum["Percentage"] = 100 * df_sum["Current Value"] / df_sum["Current Value"].sum()
        return df_sum


    def as_dataframe(self) -> pd.DataFrame:
        """
        Returns
        -------
        pandas.DataFrame
            pandas dataframe with portfolio info as table
            Serves to print well as well as be used as data-structure to extract
            values.
        """

        df_dict = OrderedDict()
        df_dict["Ticker Symbol"] = []
        df_dict["Security Type"] = []
        df_dict["Buying Price"] = []
        df_dict["Quantity"] = []
        df_dict["Value"] = []

        for t, val in self.__portfolio_objs.items():
            df_dict["Ticker Symbol"].append(t)
            df_dict["Security Type"].append(val.quote_type.value)
            if self.__portfolio_bp[t] is None:
                df_dict["Buying Price"].append(nan)
            else:
                df_dict["Buying Price"].append(self.__portfolio_bp[t])
            df_dict["Quantity"].append(self.__portfolio[t])
            df_dict["Value"].append(val.price * self.__portfolio[t])
        
        df = pd.DataFrame(df_dict)
        return df

    def add_to_portfolio(self, ticker: str, qty: Decimal, 
        buying_price: Decimal = None):
        """
        Adds given security to the Portfolio with given qty owned

        Parameters
        ----------
        ticker: str
            The security as ticker symbol
        qty: Decimal
            Amount of the security owned
        buying_price: Decimal, optional
            Not used mandatorily to initialise the security in a portfolio.
            May choose to mention now add later if needs to see returns
        """
        if not isinstance(ticker, str):
            raise ParsingError("Invalid Ticker type","expected type 'str'")

        if ticker in self.__portfolio:
            raise InputError("Ticker exists", "Input Ticker " + ticker)
        
        if not isinstance(qty, Decimal):
            raise ParsingError("Invalid qty type","expected type 'Decimal'")

        security = yf.Ticker(ticker)

        if 'quoteType' in security.info:
            if security.info['quoteType'] in QuoteType._value2member_map_:
                quote_type = QuoteType(security.info['quoteType'])
            else:
                quote_type = QuoteType.MISC
        else:
            raise InputError("Invalid Ticker Symbol", "Input Ticker " + ticker)

        if qty < Decimal(0):
            raise InputError("Invalid qty", "Input Ticker " + ticker)

        if buying_price is not None:
            if not isinstance(buying_price, Decimal):
                raise ParsingError("Invalid buying_price type","expected type 'Decimal'")

            if buying_price < Decimal(0):
                 raise InputError("Invalid buying price", "Input Ticker " + ticker)
            
        
        self.__portfolio_bp[ticker] = buying_price 
        self.__portfolio[ticker] = qty

        if quote_type == QuoteType.EQUITY:
            security = Stock(ticker)
        elif quote_type == QuoteType.ETF:
            security = ETF(ticker)
        elif (quote_type == QuoteType.CRYPTOCURRENCY or quote_type == QuoteType.CURRENCY):
            security = Currency(ticker)
        elif quote_type == QuoteType.INDEX:
            security = TreasuryBond(ticker)
        elif quote_type == QuoteType.MUTUALFUND:
            security = MutualFund(ticker)
        else:
            security = Misc(ticker)
        
       
        self.__portfolio_objs[ticker] = security
        

    

    def remove_from_portfolio(self, ticker: str):
        """
        Removes given security from the Portfolio

        Parameters
        ----------
        ticker: str
            The security as ticker symbol
        """

        if not isinstance(ticker, str):
            raise ParsingError("Invalid Ticker type","expected type 'str'")

        if ticker not in self.__portfolio:
            raise InputError("Ticker Symbol not in Portfolio", "Input Ticker " + ticker)

        else:
            del self.__portfolio[ticker]
            del self.__portfolio_objs[ticker]
            del self.__portfolio_bp[ticker]


    def update_qty(self, ticker: str, new_qty: Decimal):
        """
        Updates qty owned for a given security

        Parameters
        ----------
        ticker: str
            The security as ticker symbol
        new_qty: Decimal
            new qty which is owned in this Portfolio
        """

        if not isinstance(ticker, str):
            raise ParsingError("Invalid Ticker type","expected type 'str'")

        if not isinstance(new_qty, Decimal):
            raise ParsingError("Invalid qty type","expected type 'Decimal'")
        
        if ticker not in self.__portfolio:
            raise InputError("Ticker Symbol not in Portfolio", "Input Ticker " + ticker)

        if (Decimal(0) > new_qty):
                raise InputError("Invalid qty", "Needs to be >= 0")
        
        else:
            self.__portfolio[ticker] = new_qty


    def update_buying_price(self, ticker: str, buying_price: Decimal):
        """
        Updates buying price at which a given security was bought

        Parameters
        ----------
        ticker: str
            The security as ticker symbol
        buying_price: Decimal
            new buying price
        """

        if not isinstance(ticker, str):
            raise ParsingError("Invalid Ticker type","expected type 'str'")
    
        if ticker not in self.__portfolio:
            raise InputError("Ticker Symbol not in Portfolio", "Input Ticker " + ticker)

        if (Decimal(0) > buying_price):
                raise InputError("Invalid buying_price", "Needs to be >= 0")

        self.__portfolio_bp[ticker] = buying_price
        

    def returns(self) -> Decimal:
        """
        Get the monetary returns on the Portfolio.
        
        Returns
        -------
        Decimal
            the returns of the Portfolio, calculated as:
            Current value of the portfolio - total buying price of the portfolio
        """
        if not self.__portfolio:
            return Decimal(0)
        
        val = self.value()

        buy_price = sum(self.__portfolio_bp.values())

        rets = val - buy_price

        return rets

    def value(self) -> Decimal:
        """
        Get the value of the Portfolio.
        
        Returns
        -------
        Decimal
            the value of the Portfolio calculated as:
            Today's price of the security * qty owned in Portfolio
        """
        if not self.__portfolio:
            return Decimal(0)

        val = Decimal(0)

        for t, o in self.__portfolio_objs.items():
            val += (o.price * self.__portfolio[t])
        
        return val
                

    def get_portfolio_objects(self) -> dict:
        """
        Get the information of the security object(s) which Portfolio contains.
        
        Returns
        -------
        dict
            key: Ticker, value: security object
        """
        if not self.__portfolio_objs:
            return dict()
        
        else:
            return self.__portfolio_objs
    
    def get_portfolio_info(self) -> dict:
        """
        Get the information on buying price and qty which Portfolio contains.
        
        Returns
        -------
        dict
            key: Ticker, value: PortfolioInfo named tuple
        """
        if not self.__portfolio_objs:
            return dict()
        
        else:
            ret_dict = dict()
            for t, o in self.__portfolio.items():
                ret_dict[t] = PortfolioInfo(qty=o, buying_price=self.__portfolio_bp[t])
            
            return ret_dict