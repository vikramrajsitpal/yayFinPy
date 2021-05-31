import sys
sys.path.append("../src/yayFinPy")
from typing import List
from decimal import *
from yayFinPy.etf import ETF
import pandas as pd

def test_constructor():
	try:
		etf = ETF("QQQ")
		assert(etf != None)
		return 1
	except Exception as e:
		print("Test Failed: test_constructor: ", e)
	return 0

def test_constructor_failure():
	try:
		etf = ETF("INVALID")
	except:
		return 1
	print("Test Failed: test_constructor_failure")
	return 0

def test_etf_attributes():   
	try:
		etf = ETF("QQQ")
		assert(etf != None)
		assert(type(etf.bid) == Decimal)
		assert(type(etf.ask) == Decimal)
		assert(type(etf.bid_size) == Decimal)
		assert(type(etf.ask_size) == Decimal)
		assert(type(etf.name) == str)
		assert(type(etf.summary) == str)
		assert(type(etf.assets) == Decimal)
		assert(type(etf.returns()) == Decimal)
		assert(etf.name == "Invesco QQQ Trust, Series 1")
		return 1
	except Exception as e:
		print("Test Failed: test_etf_attributes", e)
	return 0


def test_etf_dividends():
	try:
		etf = ETF("QQQ")
		dividends = etf.dividends
		assert(type(dividends) == type(pd.Series(dtype='float64')))
		return 1
	except Exception as e:
		print("Test Failed: test_etf_dividends", e)
	return 0    


def test_etf_returns():
	try:
		etf = ETF("QQQ")
		returns_val = etf.returns()
		assert(type(returns_val) == Decimal)
		return 1
	except Exception as e:
		print("Test Failed: test_etf_returns", e)
	return 0    



if __name__ == '__main__':
	success = []
	success.append(test_constructor())
	success.append(test_constructor_failure())
	success.append(test_etf_attributes())
	success.append(test_etf_dividends())
	success.append(test_etf_returns())

	print("ETF Test Done: (%d/%d) Successful"%(sum(success), len(success)))