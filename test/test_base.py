from decimal import Decimal
from yayFinPy.currency import Currency
from yayFinPy.stock import Stock
from yayFinPy.enumerations import QuoteType, Duration


def test_base_methods1():
    try:
        stock = Stock("AAPL")
        assert (stock != None)
        assert (type(stock.quote_type) == QuoteType)
        assert (type(stock.price) == Decimal)
        assert (type(stock.volume) == Decimal)
        assert (type(stock.opening_price) == Decimal)
        assert (type(stock.day_high) == Decimal)
        assert (type(stock.day_low) == Decimal)
        assert (type(stock.exchange) == str)
        return 1
    except Exception as e:
        print("Test Failed: test_base_methods1", e)
    return 0


def test_base_methods2():
    try:
        currency = Currency("JPY=X")
        assert (currency != None)
        assert (type(currency.quote_type) == QuoteType)
        assert (type(currency.price) == Decimal)
        assert (type(currency.volume) == Decimal)
        assert (type(currency.opening_price) == Decimal)
        assert (type(currency.day_high) == Decimal)
        assert (type(currency.day_low) == Decimal)
        assert (type(currency.exchange) == str)
        return 1
    except Exception as e:
        print("Test Failed: test_base_methods2", e)
    return 0


def test_baseclass_failure():
    try:
        Stock("INVALID")
    except:
        return 1
    print("Test Failed: test_constructor_failure")
    return 0

def test_base_indicators1():
    try:
        stock = Stock("AAPL")
        assert (stock != None)
        assert (len(stock.historical_data(duration=Duration.DAY_5)) == 5)
        assert (len(stock.moving_average()) == 22)
        assert (len(stock.commodity_channel_index()) == 22)
        assert (len(stock.accumulation_distribution()) == 22)
        assert (len(stock.standard_deviation()) == 22)
        return 1
    except Exception as e:
        print("Test Failed: test_base_indicators1", e)
    return 0

def test_base_indicators2():
    try:
        currency = Currency("JPY=X")
        assert (currency != None)
        assert (len(currency.historical_data(duration=Duration.DAY_5)) == 5)
        assert (len(currency.moving_average()) == 23)
        assert (len(currency.commodity_channel_index()) == 23)
        assert (len(currency.accumulation_distribution()) == 23)
        assert (len(currency.standard_deviation()) == 23)
        return 1
    except Exception as e:
        print("Test Failed: test_base_indicators2", e)
    return 0

if __name__ == '__main__':
    success = []
    success.append(test_base_methods1())
    success.append(test_base_methods2())
    success.append(test_base_indicators1())
    success.append(test_base_indicators2())
    success.append(test_baseclass_failure())
    print("Base Test Done: (%d/%d) Successful"%(sum(success), len(success)))