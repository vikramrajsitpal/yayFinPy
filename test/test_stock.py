from typing import List
from decimal import Decimal
from yayFinPy.stock import Stock
import pandas as pd

def test_constructor():
	try:
		stock = Stock("AAPL")
		assert(stock != None)
		return 1
	except Exception as e:
		print("Test Failed: test_constructor: ", e)
	return 0
def test_constructor_failure():
	try:
		stock = Stock("INVALID")
	except:
		return 1
	print("Test Failed: test_constructor_failure")
	return 0
def test_stock_attributes():   
	try:
		stock = Stock("AAPL")
		assert(stock != None)
		assert(type(stock.bid) == Decimal)
		assert(type(stock.ask) == Decimal)
		assert(type(stock.bid_size) == Decimal)
		assert(type(stock.ask_size) == Decimal)
		assert(type(stock.name) == str)
		assert(type(stock.pe_ratio) == Decimal)
		assert(type(stock.peg_ratio) == Decimal)
		assert(type(stock.market_cap) == Decimal)
		assert(stock.name == "Apple Inc.")
		return 1
	except Exception as e:
		print("Test Failed: test_stock_attributes", e)
	return 0
def test_stock_splits():
	try:
		stock = Stock("AAPL")
		splits = stock.splits
		assert(type(splits) == type(pd.Series(dtype='float64')))
		return 1
	except Exception as e:
		print("Test Failed: test_stock_splits", e)
	return 0  

def test_stock_dividends():
	try:
		stock = Stock("AAPL")
		dividends = stock.dividends
		assert(type(dividends) == type(pd.Series(dtype='float64')))
		return 1
	except Exception as e:
		print("Test Failed: test_stock_dividends", e)
	return 0   

def test_stock_news():
	try:
		stock = Stock("AAPL")
		news = stock.related_news()
		assert(type(news) == list)
		if len(news) > 0:
			assert(type(news[0]) == str)
		assert(len(news) <= 20)
		return 1
	except Exception as e:
		print("Test Failed: test_stock_news", e)
	return 0 

def test_stock_tweets():
	try:
		stock = Stock("AAPL")
		tweets = stock.tweets("invalid",
							"invalid",
							"",
							"")
		return 0
	except Exception as e:
		#test expected to fail
		return 1

def test_stock_sentiments():
	try:
		stock = Stock("AAPL")
		sentiment_score = stock.sentiment()
		return 0
	except Exception as e:
		return 1 #test expected to fail
	return 0    

def test_stock_returns():
	try:
		stock = Stock("AAPL")
		returns_val = stock.returns()
		assert(type(returns_val) == Decimal)
		return 1
	except Exception as e:
		print("Test Failed: test_stock_returns", e)
	return 0  

def test_stock_companyData():
	try:
		stock = Stock("AAPL")
		companyData = stock.company_data
		assert(type(str(companyData)) == str)
		return 1
	except Exception as e:
		print("Test Failed: test_stock_companyData", e)
	return 0      

if __name__ == '__main__':
	success = []
	success.append(test_constructor())
	success.append(test_constructor_failure())
	success.append(test_stock_attributes())
	success.append(test_stock_splits())
	success.append(test_stock_dividends())
	success.append(test_stock_returns())
	success.append(test_stock_news())
	success.append(test_stock_tweets())
	success.append(test_stock_sentiments())
	success.append(test_stock_companyData())
	print("Stock Test Done: (%d/%d) Successful"%(sum(success), len(success)))