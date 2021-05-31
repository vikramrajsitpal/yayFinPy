Yet Another Yahoo! Finance Python API (yayFinPy)
================================================

Ever since [Yahoo! finance](https://finance.yahoo.com) decommissioned
their historical data API, many programs that relied on it to stop working.

**yfinance** solved this problem by offering a reliable, threaded,
and Pythonic way to download historical market data from Yahoo! finance.


This API: **yayFinPy**, which is short for Yet Another Yahoo Finance Python API
improves upon **yfinance** and part of academic course project at CMU in the 
course **API Design and Implementation - 17780** taught by:
**Josh Bloch and Charlie Garrod.**

We found a significant number of flaws and challenges in the API which  makes it 
a suitable API to target for improvement. We believe that improving this API 
would have a significant impact on the users of this API. In addition to fixing 
the API, we completely restructured the API to make it approachable and easy to 
use and added several additional features like stock sentiment analysis, tweets,
custom portfolio management, and many more.

-----

Quick Start
===========


> Note: Yahoo! finance datetimes are received as UTC.

Financial Modules
----
~~~~~
More details in the code documentation.
- Stock()
- MutualFund()
- Currency()
- TreasuryBonds()
- ETF()
- Misc()
- Portfolio()
~~~~~~

Enumerations
----
~~~~~~
- QuoteType:
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    CURRENCY = "CURRENCY"
    EQUITY = "EQUITY"
    ETF = "ETF"
    INDEX = "INDEX"
    MUTUALFUND = "MUTUALFUND"
    MISC = "MISC"

- Interval:
    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    DAY_1 = "1d"
    DAY_5 = "5d"
    WEEK_1 = "1wk"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"

- Duration:
    DAY_1 = "1d"
    DAY_5 = "5d"
    MONTH_1 = "1mo"
    MONTH_3 = "3mo"
    MONTH_6 = "6mo"
    YEAR_1 = "1y"
    YEAR_2 = "2y"
    YEAR_5 = "5y"
    YEAR_10 = "10y"
    YEAR_TO_DATE = "ytd"
    MAX = "max"

- Multiplier:
    ONCE = 1
    TWICE = 2
    THRICE = 3
    QUADRICE = 4
    HALF = 0.5
    QUARTER = 0.25

~~~~~~~~

Exceptions
-----
~~~~~~~
- InputError
- ParsingError
- TwitterError
- NewsError
- SecurityTypeError
- YfinanceError
~~~~~~~

Sample client code
---------
```python

import matplotlib.pyplot as plt
from decimal import *
from datetime import date
from yayFinPy.portfolio import Portfolio, PortfolioInfo
from yayFinPy.currency import Currency
from yayFinPy.enumerations import *
from yayFinPy.exceptions import *

# download data
currency = Currency("CNY=X")
data = currency.download_data(duration=Duration.MONTH_1, interval=Interval.DAY_1,
						start=date(2021,1,1), end=date(2021,5,15),
						threads=False)

# manage portfolio
portfolio = Portfolio({
                    "BTC-USD": PortfolioInfo(qty=Decimal(1), buying_price=Decimal(50000)), # currency
                    "QASGX": PortfolioInfo(qty=Decimal(50), buying_price=Decimal(31)), # mutual fund
                    "^TNX": PortfolioInfo(qty=Decimal(1000), buying_price=Decimal(1.55)), # treasury bond
                    "GOOG": PortfolioInfo(qty=Decimal(10), buying_price=Decimal(2300)), # stock
                    "VFH": PortfolioInfo(qty=Decimal(50), buying_price=Decimal(90)), # etf
					})

portfolio.add_to_portfolio("AAPL", qty=Decimal(10), buying_price=Decimal(2300)) # stock

# show protfolio info
print("Value: %f, Returns: %f"%(portfolio.value(), portfolio.returns()))
diversification_df = portfolio.diversification()
print(diversification_df)


# analyze individual assets
assets = portfolio.get_portfolio_objects()
# get currency info
crypto_btc = assets["BTC-USD"]
print("Base Currency=%s, Quote Currency=%s, Price=%f\n\n" 
					%(crypto_btc.base_currency, crypto_btc.quote_currency, crypto_btc.price))
# get stock info
stock_goog = assets["GOOG"]
print(stock_goog.company_data)
print("Price=%f, PE_Ratio=%f\n\n"%(stock_goog.price, stock_goog.pe_ratio))


# technical indicators and visualizations
bop = stock_goog.balance_of_power(duration=Duration.YEAR_1)
std = stock_goog.standard_deviation(duration=Duration.YEAR_5, timeperiod=100, dev=Multiplier.TWICE)
plt.plot(std)
plt.show()

```


Code documentation
----
You should be able to find the code documentation under 
``` /doc``` folder.
Here is the [link](./doc/yayFinPy/).

----
Installation
===========

Clone this repository using:

```bash
$ git clone https://github.com/cmu-api-design/Team13.git

$ cd Team13/src/

$ pip install .
 
```
----
Testing
===========
We have provided the user with basic unit tests which use asserts to ensure the proper behaviour of the API.


```bash
$ cd Team13/test/

$ python3 <testfile>.py
 
```

----
Requirements
===========

* [Python](https://www.python.org) >= 3.4+
* [Pandas](https://github.com/pydata/pandas) >= 0.23.1
* [Numpy](http://www.numpy.org) >= 1.11.1
* [requests](http://docs.python-requests.org/en/master/) >= 2.14.2
* [lxml](https://pypi.org/project/lxml/) >= 4.5.1
* [yfinance](https://pypi.org/project/yfinance) >= 0.1.59
* [TA-Lib](https://pypi.org/project/TA-Lib) >= 0.4.19
* [google](https://pypi.org/project/google/) >= 3.0.0
* [sentifish](https://pypi.org/project/sentifish/) >= 1.11.4
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) >= 4.9.3

----
Legal Stuff
===========

**yayFinPy** is distributed under the **Apache Software License**. 
See the [LICENSE](./src/LICENSE.txt) file in the release for details.