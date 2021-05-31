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
# Authors:
# - Chirag Sachdeva
# - Vikramraj Sitpal
# - Tianyang Zhan

from decimal import Decimal
import yfinance as yf
import talib
from datetime import date
from .enumerations import *
from .exceptions import *


class _BaseSecurity():
    """
    A class used to represent Base Securities. It contains attributes and methods common to all security types.
    Securities such as Stock, Mutual Fund, ETFs, Currency, Cryptocurrency etc extend the base class.
    ...

    Methods
    -------
    quote_type()
        returns the quote type of the security. (Refer to QuoteType Enum).

    ticker_symbol()
        returns the ticker symbol associated with security.

    price()
        returns the current market price of the security.

    volume()
        returns the present day traded market volume of security.

    opening_price()
        returns the opening market price of security.

    closing_price()
        returns the closing market price of security.

    day_high()
        returns the day's highest market price of security.

    day_low()
        returns the day's lowest market price of security.

    exchange()
        returns the exchange in which security is being traded.

    to_dict()
        returns the information about the security as key-value pairs.

    download_data(duration: Duration = Duration.MONTH_1,
                 interval: Interval = Interval.DAY_1,
                 start: date = None, end: date = None,
                 threads: bool = True)
        downloads price, volume data for a security.

    historical_data(duration: Duration = Duration.MONTH_1, interval: Interval = Interval.DAY_1)
        returns price, volume data for a security.

    moving_average(duration: Duration = Duration.MONTH_1, timeperiod=7)
         returns moving average price for a security averaged on timeperiod for given duration.

    bollinger_bands(duration: Duration = Duration.MONTH_1, timeperiod=7,
                    dev_up=Multiplier.TWICE, dev_down=Multiplier.TWICE)
         returns upperband, middleband, lowerband for price of a security averaged on timeperiod for given duration.
         and deviation multiples.

    rate_of_change_ratio(duration: Duration = Duration.MONTH_1, timeperiod=7)
        returns rate of change of ratio (price/previous price) averaged on timeperiod for a given duration.

    relative_strength_index(duration: Duration = Duration.MONTH_1, timeperiod=7)
        returns relative strength index averaged on timeperiod for a given duration. It measures the magnitude of recent
        price changes to evaluate overbought or oversold conditions in the price of a security.

    balance_of_power(duration: Duration = Duration.MONTH_1)
        returns Balance Of Power (BOP) indicator for a security. This indicator uses price to
        measure buying and selling pressure.

    commodity_channel_index(duration: Duration = Duration.MONTH_1, timeperiod=7)
        returns the CCI market indicator used to track market movements that may indicate buying or selling.

    accumulation_distribution(duration: Duration = Duration.MONTH_1)
        returns the accumulation/distribution indicator (AD) indicator that uses volume and price to assess whether
        a stock is being accumulated or distributed.

    linear_regression(duration: Duration = Duration.MONTH_1, timeperiod=7)
        returns the linear regression indicator used for trend identification and trend following.

    standard_deviation(duration: Duration = Duration.MONTH_1, timeperiod=7, dev=Multiplier.ONCE)
        returns the Standard deviation indicator which is the statistical measure of market volatility,
        measuring how widely prices are dispersed from the average price.

    variance(duration: Duration = Duration.MONTH_1, timeperiod=7, dev=Multiplier.ONCE)
        returns Variance indicator which is the statistical measure of market volatility, obtained by squaring the
        standard deviation

    time_series_forecast(duration: Duration = Duration.MONTH_1, timeperiod=7)
        returns Time Series Forecast (TSF) indicator, which is based on a linear regression technique that uses the
        least squares method to fit a straight line to data points.

    """

    def __init__(self, ticker):
        """
        Parameters
        ----------
        ticker : str
            The ticker symbol for a security

        Raises
        ------
        InputError
            If invalid ticker symbol
        ParsingError
            If data of API can't be parsed
        """
        self.__security = yf.Ticker(ticker)

        # ticker validation
        if 'quoteType' in self.__security.info:
            if self.__security.info['quoteType'] in QuoteType._value2member_map_:
                self.__quote_type = QuoteType(self.__security.info['quoteType'])
            else:
                self.__quote_type = QuoteType.MISC
        else:
            raise InputError("Invalid Ticker Symbol", "Input Ticker " + ticker)

        try:
            self.__ticker_symbol = self.__security.info['symbol']
            self.__price = Decimal(self.__security.info['regularMarketPrice'])
            self.__vol = Decimal(self.__security.info['regularMarketVolume'])
            self.__open_price = Decimal(self.__security.info['regularMarketOpen'])
            self.__close_price = Decimal(self.__security.info['regularMarketPreviousClose'])
            self.__day_high = Decimal(self.__security.info['regularMarketDayHigh'])
            self.__day_low = Decimal(self.__security.info['regularMarketDayLow'])
            self.__exchange = self.__security.info['exchange']
        except Exception as e:
            raise ParsingError(self.__ticker_symbol, "Failed to parse data. " + e)

    @property
    def quote_type(self):
        """
        Returns
        -------
        QuoteType
            returns the quote type of the security. (Refer to QuoteType Enum).
        """
        return self.__quote_type

    @property
    def ticker_symbol(self):
        """
        Returns
        -------
        str
            returns the ticker symbol associated with security.
        """
        return self.__ticker_symbol

    @property
    def price(self):
        """
        Returns
        -------
        Decimal
            returns the current regular market price of the security.
        """
        return self.__price

    @property
    def volume(self):
        """
        Returns
        -------
        Decimal
            returns the present day traded market volume of security.
        """
        return self.__vol

    @property
    def opening_price(self):
        """
        Returns
        -------
        Decimal
            returns the opening market price of security.
        """
        return self.__open_price

    @property
    def closing_price(self):
        """
        Returns
        -------
        Decimal
            returns the closing market price of security.
        """
        return self.__close_price

    @property
    def day_high(self):
        """
        Returns
        -------
        Decimal
            returns the day's highest market price of security.
        """
        return self.__day_high

    @property
    def day_low(self):
        """
        Returns
        -------
        Decimal
            returns the day's lowest market price of security.
        """
        return self.__day_low

    @property
    def exchange(self):
        """
        Returns
        -------
        str
            returns the exchange in which security is being traded.
        """
        return self.__exchange

    def to_dict(self):
        """
        Returns
        -------
        dict
            returns the information about the security as key-value pairs.
        """
        return {"ticker_symbol": self.ticker_symbol, "quote_type": self.quote_type.value,
                "price": self.price, "opening_price": self.opening_price, "closing_price": self.closing_price,
                "day_low": self.day_low, "day_high": self.day_high, "exchange": self.exchange, "volume": self.volume}

    def download_data(self, duration: Duration = Duration.MONTH_1,
                      interval: Interval = Interval.DAY_1,
                      start: date = None, end: date = None,
                      threads: bool = False):
        """
        downloads price, volume data for a security.

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
        if start is not None:
            start = str(start)
        if end is not None:
            end = str(end)
        return yf.download(self.__ticker_symbol, period=duration.value, interval=interval.value, start=start, end=end,
                           threads=threads)

    def historical_data(self, duration: Duration = Duration.MONTH_1, interval: Interval = Interval.DAY_1):
        """
        Returns
        -------
        Pandas.Dataframe
            returns price, volume data for a security.

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
        returns moving average price for a security averaged on timeperiod for given duration.

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

    def bollinger_bands(self, duration: Duration = Duration.MONTH_1, timeperiod=7, dev_up=Multiplier.TWICE,
                        dev_down=Multiplier.TWICE):
        """
        returns upperband, middleband, lowerband for price of a security averaged on timeperiod for given duration.
            and deviation multiples.

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        timeperiod: int, optional
            Time period for which the data is averaged (default is 7 days)
        dev_up: Multiplier, optional
            Deviation multiplier for upper band (default is 2x)
        dev_down: Multiplier, optional
            Deviation multiplier for lower band (default is 2x)
        """
        if timeperiod < 2:
            timeperiod = 2
        if timeperiod > 1000:
            timeperiod = 1000
        close = self.__security.history(period=duration.value)['Close']
        return talib.BBANDS(close, timeperiod=timeperiod, nbdevup=dev_up.value, nbdevdn=dev_down.value, matype=0)

    def rate_of_change_ratio(self, duration: Duration = Duration.MONTH_1, timeperiod=7):
        """
        returns rate of change of ratio (price/previous price) averaged on timeperiod for a given duration.

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
        return talib.ROCR(close, timeperiod=timeperiod)

    def relative_strength_index(self, duration: Duration = Duration.MONTH_1, timeperiod=7):
        """
        returns relative strength index averaged on timeperiod for a given duration. It measures the magnitude of recent
        price changes to evaluate overbought or oversold conditions in the price of a security.
        It is a momentum indicator.

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
        return talib.RSI(close, timeperiod=timeperiod)

    def balance_of_power(self, duration: Duration = Duration.MONTH_1):
        """
        returns Balance Of Power (BOP) data for a given duration for a security. This indicator uses price to
        measure buying and selling pressure. It determines the strength of the buyers and sellers by looking at
        how strongly the price has changed, rather than using volume.
        It is calculated as: BOP = (Close - Open) / (High - Low)

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        """
        close = self.__security.history(period=duration.value)['Close']
        open = self.__security.history(period=duration.value)['Open']
        high = self.__security.history(period=duration.value)['High']
        low = self.__security.history(period=duration.value)['Low']
        return talib.BOP(open, high, low, close)

    def commodity_channel_index(self, duration: Duration = Duration.MONTH_1, timeperiod=7):
        """
        returns the CCI market indicator used to track market movements that may indicate buying or selling.
        CCI is calculated with the following formula: (Typical Price - Simple Moving Average) / (0.015 x Mean Deviation)
        Despite its name, the CCI can be used in any market and is not just for commodities.

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
        high = self.__security.history(period=duration.value)['High']
        low = self.__security.history(period=duration.value)['Low']
        return talib.CCI(high, low, close, timeperiod=timeperiod)

    def accumulation_distribution(self, duration: Duration = Duration.MONTH_1):
        """
        returns the accumulation/distribution indicator (AD) indicator that uses volume and price to assess whether
        a stock is being accumulated or distributed.
        The A/D measure seeks to identify divergences between the stock price and volume flow.
        This provides insight into how strong a trend is.
        If the price is rising but the indicator is falling it suggests that buying or accumulation volume may not be
        enough to support the price rise and a price decline could be forthcoming.

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)

        """
        close = self.__security.history(period=duration.value)['Close']
        high = self.__security.history(period=duration.value)['High']
        low = self.__security.history(period=duration.value)['Low']
        vol = self.__security.history(period=duration.value)['Volume']
        return talib.AD(high, low, close, vol)

    def linear_regression(self, duration: Duration = Duration.MONTH_1, timeperiod=7):
        """
        returns Linear Regression Indicator used for trend identification and trend following in a similar to moving averages.
        It has advantage of having less lag than the moving average, responding quicker to changes in direction.
        The downside is that it is more prone to whipsaws.

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
        return talib.LINEARREG(close, timeperiod=timeperiod)

    def standard_deviation(self, duration: Duration = Duration.MONTH_1, timeperiod=7, dev=Multiplier.ONCE):
        """
        returns the Standard deviation indicator which is the statistical measure of market volatility,
        measuring how widely prices are dispersed from the average price.

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        timeperiod: int, optional
            Time period for which the data is averaged (default is 7 days)
        dev: Multiplier, optional
            Deviation multiplier of data from normal (default is 1x)
        """
        if timeperiod < 2:
            timeperiod = 2
        if timeperiod > 1000:
            timeperiod = 1000
        close = self.__security.history(period=duration.value)['Close']
        return talib.STDDEV(close, timeperiod=timeperiod, nbdev=dev.value)

    def variance(self, duration: Duration = Duration.MONTH_1, timeperiod=7, dev=Multiplier.ONCE):
        """
        returns Variance indicator which is the statistical measure of market volatility, obtained by squaring the
        standard deviation

        Parameters
        ----------
        duration: Duration, optional
            The duration for which the data is required (default is 1 month)
        timeperiod: int, optional
            Time period for which the data is averaged (default is 7 days)
        dev: Multiplier, optional
            Deviation multiplier of data from normal (default is 1x)
        """
        if timeperiod < 2:
            timeperiod = 2
        if timeperiod > 1000:
            timeperiod = 1000
        close = self.__security.history(period=duration.value)['Close']
        return talib.VAR(close, timeperiod=timeperiod, nbdev=dev.value)

    def time_series_forecast(self, duration: Duration = Duration.MONTH_1, timeperiod=7):
        """
        returns Time Series Forecast (TSF) indicator, which is based on a linear regression technique that uses the
        least squares method to fit a straight line to data points.

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
        return talib.TSF(close, timeperiod=timeperiod)