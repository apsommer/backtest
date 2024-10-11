import yfinance as yf

from SimpleStrategyTest import SimpleStrategyTest
from Engine import Engine

# example data
data = (yf.Ticker('AAPL').history(start='2020-01-01', end='2022-12-31', interval='1d'))

e = Engine()
e.add_data(data)
e.add_strategy(SimpleStrategyTest())
e.run()