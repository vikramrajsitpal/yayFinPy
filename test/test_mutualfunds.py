from decimal import Decimal
import pandas as pd
from yayFinPy.mutual_fund import MutualFund

def test_constructor():
	try:
		mf = MutualFund("VFIAX")
		assert(mf != None)
		return 1
	except Exception as e:
		print("Test Failed: test_constructor: ", e)
	return 0

def test_constructor_failure():
	try:
		mf = MutualFund("INVALID")
	except:
		return 1
	print("Test Failed: test_constructor_failure")
	return 0

def test_mutualfund_attributes():   
	try:
		mf = MutualFund("VFIAX")
		assert(mf != None)
		assert(type(mf.price) == Decimal)
		assert(type(mf.closing_price) == Decimal)
		assert(type(mf.exchange) == str)
		assert(type(mf.expense_ratio) == Decimal)
		assert(type(mf.name) == str)
		assert(type(mf.business_summary) == str)
		assert(type(mf.holdings_turnover) == Decimal)
		assert(type(mf.total_assets) == Decimal)
		assert(type(mf.overall_rating) == Decimal)
		assert(type(mf.risk_rating) == Decimal)
		assert(type(mf.mf_yield) == Decimal)
		assert(type(mf.ytd_return) == Decimal)
		assert(mf.name == "Vanguard 500 Index Fd Admiral S")
		return 1
	except Exception as e:
		print("Test Failed: test_mutualfund_attributes", e)
	return 0



def test_mutualfund_dividends():
	try:
		mf = MutualFund("VFIAX")
		dividends = mf.dividends
		assert(type(dividends) == type(pd.Series(dtype='float64')))
		return 1
	except Exception as e:
		print("Test Failed: test_mutualfund_dividends", e)
	return 0   

if __name__ == '__main__':
	success = []
	success.append(test_constructor())
	success.append(test_constructor_failure())
	success.append(test_mutualfund_attributes())
	success.append(test_mutualfund_dividends())


	print("Mutual funds Test Done: (%d/%d) Successful"%(sum(success), len(success)))