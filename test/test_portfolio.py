from decimal import *
from yayFinPy.portfolio import Portfolio, PortfolioInfo
from yayFinPy.currency import Currency
from yayFinPy.enumerations import *
from yayFinPy.exceptions import *

def test_constructor():
	try:
		portfolio = Portfolio()
		assert(portfolio != None)
		assets = portfolio.get_portfolio_objects()
		assert(len(assets) == 0)
		return 1
	except Exception as e:
		print("Test Failed: test_constructor: ", e)
	return 0

def test_optinal_constructor():
	try:

		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000)), "JPY=X": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(10))})
		assert(portfolio != None)
		assets = portfolio.get_portfolio_objects()
		assert(len(assets) == 2)
		assert(assets["BTC-USD"].quote_type == QuoteType.CRYPTOCURRENCY)
		assert(assets["JPY=X"].quote_type == QuoteType.CURRENCY)
		return 1
	except Exception as e:
		print("Test Failed: test_optinal_constructor: ", e)
	return 0

def test_invalid_constructor():
	try:
		portfolio = Portfolio({"BTC": PortfolioInfo(qty=Decimal(-1), buying_price=Decimal(50000))})
		print("Test Failed: test_invalid_constructor")
		return 0
	except InputError:
		return 1
	return 0

def test_returns_values():
	try:
		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000))})
		assert(portfolio != None)
		returns = portfolio.returns()
		value = portfolio.value()
		assert(isinstance(returns, Decimal))
		assert(isinstance(value, Decimal))
		assert(value > 0)
		return 1
	except Exception as e:
		print("Test Failed: test_returns_values: ", e)
	return 0

def test_update():
	try:
		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000))})
		assert(portfolio != None)
		p_info = portfolio.get_portfolio_info()
		assert(len(p_info) == 1)
		assert(p_info["BTC-USD"].qty == Decimal(1))
		assert(p_info["BTC-USD"].buying_price == Decimal(50000))
		
		portfolio.update_qty("BTC-USD", Decimal(2))
		portfolio.update_buying_price("BTC-USD", Decimal(47000))
		p_info = portfolio.get_portfolio_info()
		assert(p_info["BTC-USD"].qty == Decimal(2))
		assert(p_info["BTC-USD"].buying_price == Decimal(47000))
		return 1
	except Exception as e:
		print("Test Failed: test_update: ", e)
	return 0

def test_invalid_update():
	try:
		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000))})
		portfolio.update_qty("BTC", Decimal(2))
		print("Test Failed: test_invalid_update")
		return 0
	except InputError:
		return 1
	return 0

def test_remove():
	try:
		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000)), "JPY=X": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(10))})
		assert(portfolio != None)
		assets = portfolio.get_portfolio_objects()
		assert(len(assets) == 2)
		portfolio.remove_from_portfolio("JPY=X")
		assets = portfolio.get_portfolio_objects()
		assert(len(assets) == 1)
		assert(assets.keys() == set(["BTC-USD"]))
		return 1
	except Exception as e:
		print("Test Failed: test_remove: ", e)
	return 0

def test_invalid_remove():
	try:
		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000))})
		portfolio.remove_from_portfolio("BTC")
		print("Test Failed: test_invalid_remove")
		return 0
	except InputError:
		return 1
	return 0

def test_diversification():
	try:
		portfolio = Portfolio({"BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000)), "JPY=X": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(10))})
		assert(portfolio != None)
		df = portfolio.diversification()
		assert(df.shape[1] == 2)
		assert(abs(df["Percentage"].sum() - Decimal(100)) < 0.0001)
		return 1
	except Exception as e:
		print("Test Failed: test_diversification: ", e)
	return 0

if __name__ == '__main__':
	success = []
	success.append(test_constructor())
	success.append(test_invalid_constructor())
	success.append(test_optinal_constructor())
	success.append(test_returns_values())
	success.append(test_update())
	success.append(test_invalid_update())
	success.append(test_remove())
	success.append(test_invalid_remove())
	success.append(test_diversification())
	print("Portfolio Test Done: (%d/%d) Successful"%(sum(success), len(success)))