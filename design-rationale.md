# These are the design decisions we made for this API:
*The requirement tag IDs influenced by design decisions are listed for each design rationale stated below:*

### Creating new class abstractions for different securities (#base_all, #stock_all, #mf_all, #curr_all, #crypto_all, #bond_all, #ETF_all)
The original yfinance API uses a Ticker class as the abstraction for all securities. This causes the class methods to return different sets of key-value pairs and even irrelevant values for different securities. 
This makes the API difficult to use and violates principle U6. (APIs should be approachable). In our design, we consider U6 as the most important design principle to us since we need to ensure that the new API does not have a steep learning curve.
Therefore, we created new classes for Stock, Mutual Fund, Currency, TreasuryBonds, and ETF that extend a base class containing all shared attributes for all securities like price and volume.
To provide exhaustive coverage for the original yfinance API, we also provided a Misc() class to return the raw data collected from the original API.


### Selecting attributes and methods for different securities (#base_all, #stock_all, #mf_all, #curr_all, #crypto_all, #bond_all, #ETF_all)
During our development, we faced situations where different design principles conflict with each other; for example, we need to choose between U1. (Don’t make users do anything library could do for them) and F2. (API should be as small as possible but no smaller–when in doubt, leave it out).
We decide not to include the methods for getting the volume moving average aside from the closing price moving average. 
The advantage of including the extra methods is that we are giving users more flexibility over operations on the data (U1). 
However, the disadvantage is that the API quickly grows large (F2) with methods that might not be useful to the users.
To resolve this conflict, we consulted Professor Duane Seppi @ CMU and collected valuable feedback for the domain conventions in finance.
Then we referred to the feedback we collected and selected a minimal set of functionalities that are essential to our users. This process also allows us to follow principle U5. (An API must be appropriate to its audience).


### Making variables private (#base_all, #stock_all, #mf_all, #curr_all, #crypto_all, #bond_all, #ETF_all)
In financial related problems, the cost of error is high. With this in mind, we decide to keep all class variables private and only providing getter properties to access the selected subset of variables.
In addition, we decide to keep all classes immutable except the Portfolio class. These decisions follow Q1. (Minimize mutability) and Q2. (Minimize accessibility) and allow us to improve the quality of the API and reduce the opportunity for error.


### Adding custom exceptions (#err_all)
The original yfinance API fails silently when invalid input was given. It will return a dictionary with some empty key-value pairs or in some cases, unpredictable results from web-scraping. In our design, we fixed this issue by raising multiple custom errors for different types of errors that are possible.

For example, we raise an InputError when the input is invalid, a SecurityTypeError when the ticker is a valid ticker and but not for the particular security class object, NewsError when there is an error in retrieving data for related news of a stock security. This follows Q4. (Prevent failure, or fail quickly, predictably, and informatively). Adding custom exceptions not only exposes the errors from the input parameters but also provides a more informative way of error tracing.


### Changing String parameters to more specific types (#base_all)
The original API uses a lot of string parameters which is error prone. In our design, we decided to change the string parameters to more specific types. For example, we changed the dates to date type, and created enums for quote type and time durations. This design follows M3.3. (Don’t use String if a more appropriate type exists).


### Adding portfolio class (#port_all)
If a user of the API has a diverse set of securities and wants to analyze it to see how their portfolio is doing, the original yfinance API doesn’t provide any way for users to do that. In yayFinPy we provide a portfolio class exposed as a module to allow users to create a custom portfolio and update details on buying. The user can use the methods of this class to analyze the portfolio and look at the returns or current value. Users can add any of our defined securities to the portfolio.


### Provide easier data analysis (#base_all)
Based on our interactions with users in this domain, we found that one of the most popular use cases of the yfinance API is for analysis of financial information. In our redesigned API, we  make it easier for users to perform data analysis by providing some common technical indicators and additional security specific methods for a better user experience. This adheres to the design principles U1. Don’t make users do anything the library could do for them and U6. APIs should be approachable.


### Having a separate mutual funds class (#mf_all)
Most of the securities part of the API have some common attributes and methods. However, the attributes and methods of mutual funds are different from these securities. Instead of removing some common attributes and methods from the base class to accommodate mutual funds as a derived class of the base class, we decided to keep the base class for the other securities and created a new class for mutual funds.
