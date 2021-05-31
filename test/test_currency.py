from decimal import Decimal
from yayFinPy.currency import Currency

def test_constructor():
	try:
		currency = Currency("JPY=X")
		assert(currency != None)
		return 1
	except Exception as e:
		print("Test Failed: test_constructor: ", e)
	return 0

def test_crypto_constructor():
	try:
		currency = Currency("BTC-USD")
		assert(currency != None)
		return 1
	except Exception as e:
		print("Test Failed: test_crypto_constructor: ", e)
	return 0

def test_constructor_failure():
	try:
		currency = Currency("INVALID")
	except:
		return 1
	print("Test Failed: test_constructor_failure")
	return 0

def test_currency_attributes():
	try:
		currency = Currency("JPY=X")
		assert(currency != None)
		assert(type(currency.bid) == Decimal)
		assert(type(currency.ask) == Decimal)
		assert(type(currency.bid_size) == Decimal)
		assert(type(currency.ask_size) == Decimal)
		assert(type(currency.circulating_supply) == Decimal)
		assert(type(currency.name) == str)
		assert(currency.short_name == "USD/JPY")
		assert(currency.base_currency == "USD")
		assert(currency.quote_currency == "JPY")
		return 1
	except Exception as e:
		print("Test Failed: test_currency_attributes", e)
	return 0

if __name__ == '__main__':
	success = []
	success.append(test_constructor())
	success.append(test_crypto_constructor())
	success.append(test_constructor_failure())
	success.append(test_currency_attributes())
	print("Currency Test Done: (%d/%d) Successful"%(sum(success), len(success)))