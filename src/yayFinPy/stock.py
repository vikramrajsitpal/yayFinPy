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
import copy
from .enumerations import *
from .exceptions import *
from decimal import *
from googlesearch import search
from datetime import date
from sentifish import Sentiment
import tweepy
 


class CompanyData:
    """
    Stores data about the Stock issuing company in a encapsulated class object.
    """
    
    def __init__(self,name,address,business_summary,logo_url,industry_sector,profits,country,website):
        """
        Constructor for CompanyData class storing company details in a unified object.
        """
        self.__name  = name
        self.__address = address
        self.__business_summary = business_summary
        self.__logo_url = logo_url
        self.__industry_sector = industry_sector
        self.__profits = profits
        self.__country = country
        self.__website = website

    @property
    def name(self):
        """Returns company name

        Returns
        -------
        str
            company name
        """  
        return self.__name

    @property
    def address(self):
        """Returns company location address

        Returns
        -------
        str
            company location address
        """  
        return self.__address
    
    @property
    def business_summary(self):
        """Returns company business summary

        Returns
        -------
        str
            company business summary
        """  
        return self.__business_summary
    
    @property
    def industry_sector(self):
        """Returns industry sector

        Returns
        -------
        str
            company industry sector
        """  
        return self.__industry_sector
    
    @property
    def profits(self):
        """Returns company annual profit figures

        Returns
        -------
        Decimal
            company anual profits
        """  
        return Decimal(self.__profits)

    @property
    def country(self):
        """Returns company's home country

        Returns
        -------
        str
            company's home country
        """  
        return self.__country
    
    @property
    def wesbite(self):
        """Returns company website url

        Returns
        -------
        str
            company website url
        """        
        return self.__website

    @property
    def logo_url(self):
        """Returns company logo url

        Returns
        -------
        str
            company logo url
        """
        return self.__logo_url

    def __str__(self):
        """Returns string representation of CompanyData

        Returns
        -------
        str
            string representation of CompanyData
        """
        return "Company Name: "+self.__name \
        +"\naddress: "+self.__address \
        +"\nsummary: "+self.__business_summary \
        +"\nLogo Url: "+self.__logo_url \
        +"\nCountry: "+self.__country \
        +"\nwesbite: "+self.__website \
        +"\nIndustry Sector: "+self.__industry_sector \
        +"\nProfits: "+str(self.__profits) + "\n"


    
class Stock(_BaseSecurity):
    """
    A Yahoo Finance parser API for Stocks and Equity.

	This module covers the most important attributes of stocks:
	Company Data, stock splits, peg ratio, dividends, market cap, ask, ask size, bid, bid size, pe ratio , name;

	And attributes common to all Securities:
	price, opening price, closing price, volume, day high, day low, exchange, ticker symbol, quote type.

	For more methods on the security, refer to ``base._BaseSecurity``

	Methods
	-------
    related_news(self)
		returns upto 20 top news links related to a stock.

    tweets(self)
		returns upto 20 top tweets related to a stock.

    sentiment(self)
		returns average sentiment score based on tweet data.

    industry_recommendations(self)
		Returns dataframe of mutualfund stock holders.

	company_summary(self)
		Returns company summary.
    
    returns(self,period,interval,start_date,end_date)
        returns stock returns for a specific period and interval

    returns_percentage(self,period,interval,start_date,end_date)
        returns stock returns in percentage for specific period and interval


    A typical application of this class first initialize an object with a valid ticker symbol, then use the
	class properties to extract information.

	Example usage:
		
        try:
            stock_goog = Stock("GOOG")
            # fetch price
            price = stock_goog.price

            # fetch market cap
            stock_market_cap = stock_goog.market_cap

            # get 1 year returns
            returns = stock_goog.returns(period=Duration.YEAR_1)

            # get related news links
            news_list = stock_goog.related_news()
            
        except:
            print("Invalid Input Ticker")
    """

    def __init__(self,ticker_symbol):
        """
        The constructor of the Stock class for initializing a Stock object.
		
		Parameters
		----------
		ticker_symbol :str
			A valid ticker symbol for a Stock.
		
		Raises
		------
		InputError
			if the input ticker_symbol is not a valid Stock ticker or data is not retrieved.
		SecurityTypeError
			if the Security type of the ticker is other than Stock, this error is raised.
        """
        
        self.__ticker_symbol = ticker_symbol
        super().__init__(self.__ticker_symbol)
        try:
            self.__security = self._BaseSecurity__security

            s = self.__security.info
            if 'quoteType' in self.__security.info.keys() and QuoteType(self.__security.info['quoteType']) == QuoteType("EQUITY") :
                self.__quote_type = QuoteType(self.__security.info['quoteType'])
            else:
                raise SecurityTypeError(self.__ticker_symbol, "Ticker Symbol does not match Stock security")
            
            self.__company_data = CompanyData(s["longName"],s["address1"],
                                             s["longBusinessSummary"],s["logo_url"],
                                             s["sector"],s["profitMargins"],s["country"],
                                             s["website"])
            
            self.__stock_splits = self.__security.splits
            self.__peg_ratio = Decimal(s["pegRatio"])
            self.__dividends = self.__security.dividends
            self.__market_cap = Decimal(s["marketCap"])
            self.__ask = Decimal(s["ask"])
            self.__ask_size = Decimal(s["askSize"])
            self.__bid = Decimal(s["bid"])
            self.__bid_size = Decimal(s["bidSize"])
            self.__pe_ratio = Decimal(s["trailingPE"])
            self.__name = s["shortName"]
            self.__news = None
            self.__tweets = None
        except:
            raise InputError(ticker_symbol,"API data retrieval error")


    @property
    def name(self):
        """Returns name of company issuing stock.

        Returns
        -------
        str
            String name of Stock
        """
        return self.__name

    @property
    def company_data(self):
        """Returns object providing company details.

        Returns
        -------
        CompanyData
            Object providing company details
        """
        return copy.deepcopy(self.__company_data)

    @property
    def splits(self):
      """Returns dataframe of stock splits.

        Returns
        -------
        Pandas.DataFrame
            dataframe of stock splits
        """    
      return copy.deepcopy(self.__stock_splits)

    @property
    def dividends(self):
        """Returns dataframe of security dividends.

        Returns
        -------
        Pandas.DataFrame
            dataframe of security dividends
        """    
        return copy.deepcopy(self.__dividends)
    

    @property
    def market_cap(self):
        """Returns market cap of company.

        Returns
        -------
        Decimal
            market cap of company.
        """
        return self.__market_cap

    @property
    def peg_ratio(self):
        """Returns stock price earnings growth ratio.

        Returns
        -------
        Decimal
            Stock PEG ratio
        """   
        return self.__peg_ratio

    @property
    def ask(self):
        """Returns ask price for Stock Object.

        Returns
        -------
        Decimal
            ask price for Stock Object
        """     
        return self.__ask

    @property
    def ask_size(self):
        """Returns ask size for Stock.

        Returns
        -------
        Decimal
            ask size for Stock
        """      
        return self.__ask_size

    @property
    def bid(self):
        """Returns bid price for Stock Object.

        Returns
        -------
        Decimal
            bid price for Stock Object
        """
        return self.__bid

    @property
    def bid_size(self):
        """Returns bid size for Stock.

        Returns
        -------
        Decimal
            ask bid for Stock
        """      
        return self.__bid_size

    @property
    def pe_ratio(self):
        """Returns price earnings ratio for Stock.

        Returns
        -------
        Decimal
            rice earnings ratio for Stock
        """       
        return self.__pe_ratio

    
    def __calculate_returns(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1, percentage = False,
                start:date = None, end:date = None): 
        historic_data = self.historical_data(duration=period,interval=interval)
        open_price = historic_data.iloc[0]["Open"]
        close_price = historic_data.iloc[-1]["Close"]
        total_return = close_price - open_price
        for i,dividend in enumerate(historic_data["Dividends"]):
            if dividend > 0:
                total_return += dividend*((historic_data.iloc[i]["Open"]+historic_data.iloc[i]["Close"])/2)
        if not percentage:
            return total_return
        else:
            return (total_return/open_price) * 100

    def returns(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1, 
                start:date = None, end:date = None):
        """
        Returns absolute Stock returns for period using specified interval.

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
            absolute stock return amount.
        """
        return Decimal(self.__calculate_returns(period,interval,False,start,end))

    def returns_percentage(self,period:Duration = Duration.YEAR_1, 
                interval: Interval = Interval.MONTH_1,
                start:date = None, end:date = None):
        """
        Returns percentage Stock returns for period using specified interval.

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
            percentage return of a stock.
        """    
        return Decimal(self.__calculate_returns(period,interval,True,start,end))

    
    def company_summary(self):
        """Prints company data summary.
        """
        print(self.company_data)
    

    def sentiment(self):
        """Returns average Sentiment Score of top 20 tweets.

        Returns
        -------
        Decimal
            Sentiment score from 0 to 1. with 1 being most positive and 0 least.

        Raises
        ------
        TwitterError
            Riased when error in calling twitter API.
        """
        if self.__tweets is None:
            raise TwitterError(self.__ticker_symbol ," Error getting twitter data.")

        if len(self.__tweets) == 0:
            raise TwitterError(self.__ticker_symbol ," Error getting twitter data.")
        sentiments = []
        for t in self.__tweets:
            obj = Sentiment(t)
            sentiments.append(obj.analyze())
        return Decimal(sum(sentiments)/len(sentiments))

    

    def industry_recommendations(self):
        """Returns dataframe of industry recommendations.

        Returns
        -------
        Pandas.DataFrame
            dataframe of industry recommendations
        """  
        return self.__security.recommendations
    

    def tweets(self,consumer_key, consumer_secret, access_token,access_token_secret):
        """[summary]

        Parameters
        ----------
        consumer_key : str
            twitter API consumer key
        consumer_secret : str
             twitter API consumer Secret
        access_token : str
             twitter API access token
        access_token_secret : str
             twitter API access token secret

        Returns
        -------
        list[str]
            list of upto 20 tweets from twitter for Stock symbol.

        Raises
        ------
        TwitterError
            Riased when error in calling or authenticating twitter API.
        """
        if self.__tweets is None:
            self.__tweets = []
            # Authenticate to Twitter
            try:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)

                # Create API object
                api = tweepy.API(auth, wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
                for tweet in api.search(q="$TSLA", lang="en", rpp=20):
                    self.__tweets.append(tweet.text)
            except:
                raise TwitterError(self.__ticker_symbol ," Error getting twitter data. Check API keys.")
        return self.__tweets
    
    def related_news(self):
        """Returns a list of links to news items related to the Stock.

        Returns
        -------
        list[str]
            list of links to news items related to the Stock.

        Raises
        ------
        NewsError
            Raised when error occurs in getting news links.
        """
        news_list = []
        for news_article in search(self.__ticker_symbol, tld="com", num=20, stop=20, pause=2):
            news_list.append(news_article)

        if len(news_list) == 0:
                raise NewsError(self.__ticker_symbol ," Error getting related news.")

        return news_list

    @property
    def financials(self):
        """Returns dataframe of stock financials.

        Returns
        -------
        Pandas.DataFrame
            dataframe of stock financials
        """  
        return self.__security.financials

    @property
    def calendar(self):
        """Returns dataframe of stock Calendar.

        Returns
        -------
        Pandas.DataFrame
            dataframe of stock Calendar
        """     
        return self.__security.calendar

    @property
    def cashflow(self):
        """Returns dataframe of cashflow.

        Returns
        -------
        Pandas.DataFrame
            dataframe of cashflow
        """     
        return self.__security.cashflow

    @property
    def earnings(self):
        """Returns dataframe of earnings.

        Returns
        -------
        Pandas.DataFrame
            dataframe of earnings
        """      
        return self.__security.earnings


    @property
    def major_holders(self):
        """Returns dataframe of major stock holders.

        Returns
        -------
        Pandas.DataFrame
            dataframe of major stock holders
        """    
        return self.__security.major_holders

    @property   
    def actions(self):
        """Returns dataframe of splits and dividends.

        Returns
        -------
        Pandas.DataFrame
            dataframe of splits and dividends
        """      
        return self.__security.actions

    @property   
    def balance_sheet(self):
        """Returns dataframe containing balance sheet.

        Returns
        -------
        Pandas.DataFrame
            dataframe of containing balance sheet
        """    
        return self.__security.balance_sheet

    @property
    def institutional_holders(self):
        """Returns dataframe of institutional stock holders.

        Returns
        -------
        Pandas.DataFrame
            dataframe of institutional stock holders
        """      
        return self.__security.institutional_holders

    @property
    def mutualfund_holders(self):
        """Returns dataframe of mutualfund stock holders.

        Returns
        -------
        Pandas.DataFrame
            dataframe of mutualfund stock holders
        """    
        return self.__security.mutualfund_holders