**17780: Summary of requirements and use cases over time based on user interviews**

**Team Members:**
1. Chirag Sachdeva (csachdev)
2. Vikramraj Sitpal (vsitpal)
3. Tianyang Zhan (tzhan)
4. Shubham Gupta (shubhamg)
5. Vasudev Luthra (vasudevl)

### Requirements considered before user interviews (April 10th, 2021)

Based on over 300+ [issues](https://github.com/ranaroussi/yfinance/issues) on the [yfinance](https://pypi.org/project/yfinance/) 
API github [repository](https://github.com/ranaroussi/yfinance) and team members prior experience using the API, we 
listed out initial shortcomings and flaws in the yfinance API.
We identified that yfinance was a widely used public API in the domain of finance. On analysing a lot of user codes, we realized 
that most users were using this API for either downloading or pulling the historical price or volume data for specific 
securities (mostly limited to Stocks, Currency and ETFs). In addition to this, a lot of users were using this data to either do technical analysis or deploy machine learning algorithms. 
Based on the issues encountered by users, we identified key areas where the API had some serious issues. These were as follows:
* Structure : It lacked the key layer of abstraction and grouped all securities as tickers.
* Utility : It should do what it says and do it well like accessing different security specific information. In addition, it should make it easy for the users to perform common things like technical analysis.
* Handling exception : It fails to handle several edge cases, and considers any ticker as a valid ticker.

(More information about each can be found in the Design Rational and Report)

So the main requirements considered during this stage were to develop a layer of abstract for just Stocks and group other securities together 
.In addition, handle edge cases well and improve utility by providing better field access methods.
These were detailed in the Project Proposal.

### Requirements considered after Interview - I (April 22nd, 2021)

First interview with Prof. Duane Seppi (THE BNY Mellon Professor of Finance at CMU) help us identify the key securities 
that were of importance and lay down a skeleton of how the API abstraction would look like.  Based on the discussion, we developed the following table consisting of requirements, 
its relative importance in API (out of 5), current status (if it is done implemented, if it is pending to be implemented, if it is removed from requirements) 
and tacking ID for development purposes.

| ID        | Requirements                     | Priority (out of 5)  | Status (done, pending, reject) |
|-----------|----------------------------------|----------------------|--------------------------------|
| stock_all | Stock class                      | 5                    | pending                        |
| bond_all  | Bond and Treasuries class        | 5                    | pending                        |
| curr_all  | Currency class                   | 5                    | pending                        |
| mf_all    | Mutual Fund class                | 5                    | pending                        |
| base_all  | Base class + Group of Securities | 5                    | pending                        |
| visual    | Visualization functions          | 2                    | pending                        |
| ti_avg    | Weekly moving Avg                | 3                    | pending                        |
| base_1    | Field Accessors for each         | 5                    | pending                        |
| comm_all  | Commodity Futures                | 2                    | pending                        |
| base_2    | Historical performance           | 3                    | pending                        |
| err_all   | Error handling                   | 5                    | pending                        |

The requirements helped us in identifying the key securities to look into before refining the design 
and identifying key attributes and methods for each.
### Requirements considered after Interview - II (April 29nd, 2021)

The second interview help us in getting a feedback on attributes and methods related to selected securities.
Based on the interview we restructured our design to make the Base class more general and incorporate several popular technical
indicators:
* Price indicators-  Bollinger Bands, Moving Averages, Rate of change ratio, RSI, Linear Regression, Standard Deviation, Variance, Time Series Forecast
* Momentum Indicator- Balance Of Power, Commodity Channel Index
* Volume Indicator- Chaikin A/D Line

| ID         | Requirements                 | Priority (out of 5)  | Status (done, pending, reject) |
|------------|------------------------------|----------------------|--------------------------------|
| stock_all  | Stock class                  | 5                    | done                           |
| stock_1    | Company Data Dic             | 4                    | done                           |
| stock_2    | PE, PEG, Market data         | 4                    | done                           |
| stock_3    | Dividends, Stock splits info | 5                    | done                           |
| bond_all   | Bond and Treasuries class    | 5                    | pending                        |
| bond_1     | Maturity                     | 4                    | pending                        |
| bond_2     | Safety Rating                | 4                    | pending                        |
| bond_3     | Interest Interval            | 3                    | pending                        |
| bond_4     | Prepayment Risk              | 3                    | pending                        |
| curr_all   | Currency class               | 5                    | pending                        |
| curr_1     | Base currency                | 5                    | done                           |
| curr_2     | Ask, Ask size                | 3                    | done                           |
| curr_3     | Bid, Bid size                | 3                    | done                           |
| crypto_all | Similar currency class       | 5                    | pending                        |
| mf_all     | Mutual Fund class            | 5                    | pending                        |
| base_all   | Base class                   | 5                    | done                           |
| visual     | Visualization functions      | 2                    | reject                         |
| ti_avg     | Weekly moving Avg            | 3                    | reject                         |
| ti_price   | price technical indicators   | 4                    | done                           |
| ti_vol     | vol technical indicator      | 4                    | done                           |
| ti_mom     | momentum technical indicator | 4                    | done                           |
| base_1     | Field Accessors for each     | 5                    | done                           |
| comm_all   | Commodity Futures            | 2                    | reject                         |
| base_2     | Historical performance       | 3                    | done                           |
| err_all    | Error handling               | 5                    | pending                        |


### Modification in Requirements during implementation phase and Interview  - III (May 8th, 2021)

During the third interview, based on the feedback, we separated ETF from Stock class since certain information 
was not relevant for ETF (like company info, PE ratio etc). 
We also decided to remove the Commodities-futures security class and instead add a Miscellaneous class 
(to account for a security that's not stock, bond, ETF, mutual fund, currency, cryptocurrency). 
Another important decision based on common use cases and a responsible replacement for Tickers class was to add a 
Portfolio class to manage a group of Securities. 

| ID         | Requirements                   | Priority (out of 5)  | Status (done, pending, reject) |
|------------|--------------------------------|----------------------|--------------------------------|
| stock_all  | Stock class                    | 5                    | done                           |
| stock_1    | Company Data Dic               | 4                    | done                           |
| stock_2    | PE, PEG, Market data           | 4                    | done                           |
| stock_3    | Dividends, Stock splits info   | 5                    | done                           |
| bond_all   | Bond (Treasuries) class        | 5                    | done                           |
| bond_1     | Maturity                       | 4                    | done                           |
| bond_2     | Safety Rating                  | 4                    | reject                         |
| bond_3     | Interest Interval              | 3                    | done                           |
| bond_4     | Returns                        | 5                    | done                           |
| bond_5     | Prepayment Risk                | 3                    | reject                         |
| curr_all   | Currency class                 | 5                    | done                           |
| curr_1     | Base currency                  | 5                    | done                           |
| curr_2     | Ask, Ask size                  | 3                    | done                           |
| curr_3     | Bid, Bid size                  | 3                    | done                           |
| crypto_all | Similar currency class         | 5                    | done                           |
| mf_all     | Mutual Fund class              | 5                    | done                           |
| mf_1       | Interest, dividend             | 4                    | done                           |
| mf_2       | ratings                        | 4                    | done                           |
| mf_3       | expense ratio, yield, turnover | 3                    | done                           |
| base_all   | Base class                     | 5                    | done                           |
| visual     | Visualization functions        | 2                    | reject                         |
| ti_avg     | Weekly moving Avg              | 3                    | reject                         |
| ti_price   | price technical indicators     | 4                    | done                           |
| ti_vol     | vol technical indicator        | 4                    | done                           |
| ti_mom     | momentum technical indicator   | 4                    | done                           |
| base_1     | Field Accessors for each       | 5                    | done                           |
| comm_all   | Commodity Futures              | 2                    | reject                         |
| base_2     | Historical performance         | 3                    | done                           |
| err_all    | Error handling                 | 5                    | pending                        |
| port_all   | Portfolio class                | 5                    | pending                        |
| ETF_all    | ETF class                      | 5                    | done                           |
| misc_all   | Miscellaneous class            | 4                    | pending                        |

### Final Interview and Review (May 10th, 2021)

During the final interview we went over each of the security classes in detail and got feedback on improvements regarding 
what additional functionalities can be added to make the API more useful.
The current yfinance API had limited functionalities and was very broken. 
This yayFinPy helps overcome those shortcomings by fixing the flaws and extending the utility of API by providing several helpful functions.
In addition to the price, volume and momentum related technical indicators and the portfolio utility functionalities added during the 
prior interview stages, in this interview we were suggested several stock related functionalities to enhance the API. 
We concluded on adding functionalities like getting the news related to the stock, getting sentiment from public posts, getting tweets and
providing additional stats about institutional holdings, major holders and mutual funds containing stocks.

| ID         | Requirements                   | Priority (out of 5)  | Status (done, pending, reject) |
|------------|--------------------------------|----------------------|--------------------------------|
| stock_all  | Stock class                    | 5                    | done                           |
| stock_1    | Company Data Dic               | 4                    | done                           |
| stock_2    | PE, PEG, Market data           | 4                    | done                           |
| stock_3    | Dividends, Stock splits info   | 5                    | done                           |
| bond_all   | Bond (Treasuries) class        | 5                    | done                           |
| bond_1     | Maturity                       | 4                    | done                           |
| bond_2     | Safety Rating                  | 4                    | reject                         |
| bond_3     | Interest Interval              | 3                    | done                           |
| bond_4     | Returns                        | 5                    | done                           |
| bond_5     | Prepayment Risk                | 3                    | reject                         |
| curr_all   | Currency class                 | 5                    | done                           |
| curr_1     | Base currency                  | 5                    | done                           |
| curr_2     | Ask, Ask size                  | 3                    | done                           |
| curr_3     | Bid, Bid size                  | 3                    | done                           |
| crypto_all | Similar currency class         | 5                    | done                           |
| mf_all     | Mutual Fund class              | 5                    | done                           |
| mf_1       | Interest, dividend             | 4                    | done                           |
| mf_2       | ratings                        | 4                    | done                           |
| mf_3       | expense ratio, yield, turnover | 3                    | done                           |
| base_all   | Base class                     | 5                    | done                           |
| visual     | Visualization functions        | 2                    | reject                         |
| ti_avg     | Weekly moving Avg              | 3                    | reject                         |
| ti_price   | price technical indicators     | 4                    | done                           |
| ti_vol     | vol technical indicator        | 4                    | done                           |
| ti_mom     | momentum technical indicator   | 4                    | done                           |
| base_1     | Field Accessors for each       | 5                    | done                           |
| comm_all   | Commodity Futures              | 2                    | reject                         |
| base_2     | Historical performance         | 3                    | done                           |
| err_all    | Error handling                 | 5                    | done                           |
| port_all   | Portfolio class                | 5                    | done                           |
| ETF_all    | ETF class                      | 5                    | done                           |
| misc_all   | Miscellaneous class            | 4                    | done                           |
| stock_4    | Sentiment Analysis             | 4                    | done                           |
| stock_5    | Tweets                         | 4                    | done                           |
| stock_6    | News                           | 5                    | done                           |
| stock_7    | Industrial Recommendation      | 5                    | done                           |
| stock_8    | financials                     | 5                    | done                           |
| stock_9    | cashflow, earnings             | 5                    | done                           |
| stock_10   | major holders, mutual funds    | 4                    | done                           |
