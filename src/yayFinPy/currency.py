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
# - Tianyang Zhan

import pandas as pd
from decimal import *
from .base import _BaseSecurity
from datetime import date
from .exceptions import *
from .enumerations import *

class Currency(_BaseSecurity):
	"""
	A Yahoo Finance parser for currency and cryptocurrency.

	This module covers the most important attributes of a currency pair:
	bid, ask, bid size, ask size, base currency, quote currency, circulating supply, name, short name;

	And attributes common to all Securities:
	price, opening price, closing price, volume, day high, day low, exchange, ticker symbol, quote type.

	For more methods on the security, refer to ``base._BaseSecurity``


	Methods
	-------
	to_df(self)
		Convert the Currency object as a single-row Pandas DataFrame object.

	to_dict(self)
		Convert the Currency object as a dictionary.


	A typical application of this class first initialize an object with a valid ticker symbol, then use the
	class properties to extract information.

	Example usage:
		
		try:
			currency = Currency("CNY=X")
			# fetch price
			price = currency.price

			# fetch currency pair
			base_currency = currency.base_currency
			quote_currency = currency.quote_currency
			print("Results: Price=%f, Base Currency=%s, Quote Currency=%s"
									%(price, base_currency, quote_currency))
		except:
			print("Invalid Input Ticker")
	"""

	def __init__(self, ticker_symbol:str):
		"""
		The constructor of the Currency class for initializing a Currency object.
		
		Parameters
		----------
		ticker_symbol :str
			A valid ticker symbol for currency or cryptocurrency.
		
		Raises
		------
		InputError
			if the input ticker_symbol is not a valid Currency ticker.
		ParsingError
			if the failure occurs when parsing data using the input ticker. 
		"""
		self.__ticker = None
		self.__ticker_symbol = ticker_symbol
		self.__bid = None
		self.__bid_size = None
		self.__ask = None
		self.__ask_size = None
		self.__base_currency = None
		self.__quote_currency = None
		self.__circulating_supply = None
		self.__name = None
		self.__short_name = None
		self._init_ticker()

	def _init_ticker(self):
		
		super().__init__(self.__ticker_symbol)
		self.__ticker = self._BaseSecurity__security
		
		# ticker validation
		quote_type = self.__ticker.info['quoteType']
		if quote_type is QuoteType.CRYPTOCURRENCY and quote_type is QuoteType.CURRENCY:
			raise InputError("Invalid Ticker Symbol for Currency", "Input Ticker " + self.__ticker_symbol)

		# init currency class
		try:
			self.__bid = Decimal('NaN') if not self.__ticker.info['bid'] else Decimal(self.__ticker.info['bid'])
			self.__bid_size = Decimal('NaN') if not self.__ticker.info['bidSize'] else Decimal(self.__ticker.info['bidSize'])
			self.__ask = Decimal('NaN') if not self.__ticker.info['ask'] else Decimal(self.__ticker.info['ask'])
			self.__ask_size = Decimal('NaN') if not self.__ticker.info['askSize'] else Decimal(self.__ticker.info['askSize'])
			self.__circulating_supply = Decimal('NaN') if not self.__ticker.info['circulatingSupply'] else Decimal(self.__ticker.info['circulatingSupply'])
			self.__short_name = self.__ticker.info['shortName']
			self.__name = self.__short_name if 'name' not in self.__ticker.info else self.__ticker.info['name']  
			self.__base_currency = self.__short_name.split("/")[0] if '/' in self.__short_name else self.__short_name.split(" ")[1]
			self.__quote_currency = self.__short_name.split("/")[1] if '/' in self.__short_name else self.__short_name.split(" ")[0]
		except Exception as e:
			raise ParsingError(self.__ticker_symbol, "Failed to parse data. " + e)
	

	def __str__(self):
		return "Ticker Symbol: %s, Name: %s, Short Name: %s\n"%(self.__ticker_symbol, self.__name, self.__short_name) 

	def to_df(self):
		"""
		Convert the Currency object as a single-row Pandas DataFrame object.
		
		Returns
		-------
		Pandas.DataFrame
			the transformed information of the currency
		"""
		return pd.DataFrame.from_dict(self.to_dict(),orient='index').T

	def to_dict(self):
		"""
		Convert the Currency object as a dictionary.
		
		Returns
		-------
		dict
			the transformed information of the currency
		"""
		base_dict = super().to_dict()
		currency_dict = {"name": self.name, "short_name": self.short_name, "base_currency": self.base_currency, "quote_currency": self.quote_currency, 
				"bid": self.bid, "bid_size": self.bid_size, "ask": self.ask, "ask_size": self.ask_size, "circulating_supply": self.circulating_supply}
		currency_dict.update(base_dict)
		return currency_dict
	@property
	def bid(self):
		"""
		Get the bid price of the Currency object.
		
		Returns
		-------
		Decimal
			the bid of the currency.
		"""
		return self.__bid
	
	@property
	def bid_size(self):
		"""
		Get the bid size of the Currency object.
		
		Returns
		-------
		Decimal
			the bid size of the currency.
		"""
		return self.__bid_size
	
	@property
	def ask(self):
		"""
		Get the ask price of the Currency object.
		
		Returns
		-------
			the ask of the currency.
		"""
		return self.__ask
	
	@property
	def ask_size(self):
		"""
		Get the ask size of the Currency object.
		
		Returns
		-------
		Decimal
			the ask size of the currency.
		"""
		return self.__ask_size
	
	@property
	def base_currency(self):
		"""
		Get the base currency of the Currency object.
		
		Returns
		-------
		str
			the symbol of the base currency.
		"""
		return self.__base_currency
	
	@property
	def quote_currency(self):
		"""
		Get the quote currency of the Currency object.
		
		Returns
		-------
		str
			the symbol of the quote currency.
		"""
		return self.__quote_currency
	
	@property
	def circulating_supply(self):
		"""
		Get the circulation supply of the Currency object.
		
		Returns
		-------
		Decimal
			the supply of the currency.
		"""
		return self.__circulating_supply

	@property
	def name(self):
		"""
		Get the name of the Currency object.
		
		Returns
		-------
		str
			the name of the currency.
		"""
		return self.__name
	
	@property
	def short_name(self):
		"""
		Get the short name of the Currency object.
		
		Returns
		-------
		str
			the short name of the currency.
		"""
		return self.__short_name
	