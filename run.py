import yfinance as yf
from Strategy import Strategy
from Engine import Engine

# example data
data = (yf.Ticker('AAPL').history(
    start='2020-01-01',
    end='2022-12-31',
    interval='1d'))

# inherit from Strategy base class
class BuySellSwitchStrategy(Strategy):

    # override/implement on_bar
    def on_bar(self):

        if self.position_size == 0:
            self.buy('AAPL', 1)
        else:
            self.sell('AAPL', 1)

e = Engine()
e.add_data(data)
e.add_strategy(BuySellSwitchStrategy())
e.run()