# Stonks

(C) 2020 Mark M. Bailey, PhD

## About

This is a set of tools I built to pull and analyze stock prices.  Stock prices can be pulled from the World Trading Data API (www.worldtradingdata.com, key required), or they can be acquired through other means.  This set of tools can also be used to generate synthetic price lists in order to test out the analytical features (or for anything else you can come up with).  The "analyze()" class will generate an analysis object from the input price list, which can be analyzed using either a stochastic oscillator or a relative strength index indicator (or both).  An output of "Hold", "Sell", or "Buy" signal can be extracted from the analysis based on the most recent indicator values.<br />

Disclaimer: I do this mostly for fun (I like to code, I'm a data science nerd and I like stocks; but I'm just a math professor and not qualified to offer financial advice).<br />

If you want to make this better, let's collaborate!

## Installation

`pip install stonk-momentum`

## Sample usage

### Initial import

`import stonk_momentum`

### Access historic stock data

Note that this requires an API key from World Trading Data (www.worldtradingdata.com).<br />

`stock = stonks.stock_API(API_KEY)`<br />
Parameters:<br />
* API_KEY = World Trading Data API Key (str).

`daily_price_dictionary = stock.daily(TKR, time_delta, beta=True, EX='^IXIC')`<br />
Parameters:<br />
* TKR = Ticker symbol (str).
* time_delta = Specifies the number of days into the past (from today) to pull historic closing prices (int).
* beta = Boolean to include beta calculation in output dictionary (default=True).
* EX = Exchange on which to base beta calculation (default = '^IXIC')
* output = dictionary

`intraday_price_dictionary = intraday(TKR, range_=1, interval=60, beta=True, EX='^IXIC')`<br />
Parameters:<br />
* TKR = Ticker symbol (str).
* range_ = Specifies the number of days you want to return data for (int or str).
* interval = Specifies the interval (in minutes) of time between the data (int or str).
* interval = Boolean to include beta calculation in output dictionary (default=True).
* EX = Exchange on which to base beta calculation (default = '^IXIC')
* output = dictionary

### Generate synthetic stock price data

If you don't have API access or other real stock data and want to mess around with simulations, this class will generate synthetic price data (either bullish random price or oscillating random price).  Note that these generators are imperfect and will sometimes generate negative prices (if you'd like to contribute to this project and make this function better, please feel free!).<br />

`synthetic_price_generator = stonks.syn_stock()`<br />
`synthetic_prices =  synthetic_price_generator.oscillator(n, scale=1)`<br />
`synthetic_prices =  synthetic_price_generator.bullish_random(n, scale=1)`<br />
Parameters:<br />
* n = Number of prices to simulate.
* scale = Standard deviation (spread or “width”) of the distribution. Must be non-negative.

### Calculate momentum indicators

This class will calculate either a stochastic oscillator or relative strength index indicator for a list of stock prices.  Sell or buy signals are also generated.<br />

`stock = analyze(input_, closing_prices='closing_prices')`<br />
Parameters:<br />
* input_ = Price list or dictionary (generated from daily_price_dictionary).
* closing_prices = Key for prices dictionary (default is 'closing_prices').

`stock_object = stock.stochastic_oscillator(n, c=3)`<br />
`output = stock_object.stochastic_output`<br />
`signal = stock_object.stochastic_assessment`<br />
Parameters:<br />
* n = Period size (int).
* c = Moving average size (default is 3).
* output = JSON output (Within the 'assessment' list, a value of -1 means the stock is oversold, and 1 indicates that it is overbought.  A value of 0 means neither).
* signal = Buy, Sell, or Hold signal based on most recent stochastic output.

`stock_object = stock.RSI(n)`<br />
`output = stock_object.RSI_output`<br />
`signal = stock_object.RSI_assessment`<br />
Parameters:<br />
* n = Period size (int).
* output = JSON output (Within the 'assessment' list, a value of -1 means the stock is oversold, and 1 indicates that it is overbought.  A value of 0 means neither).
* signal = Buy, Sell, or Hold signal based on most recent stochastic output.