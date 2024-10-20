import yfinance as yf
from backtesting import Backtest, Strategy

""" Validate BuySellSwitchStrategy by duplicating it using popular
backtesting library backtesting.py """

# example data
data = (yf.Ticker('AAPL').history(
    start='2020-01-01',
    end='2022-12-31',
    interval='1d'))

# inherit from Strategy base class
class BuySellSwitchStrategy(Strategy):
    def init(self):
        pass
    def next(self):
        if self.position.size == 0:
            self.buy(size=1)
        else:
            self.sell(size=1)

bt = Backtest(data, BuySellSwitchStrategy, cash=10000)
stats = bt.run()
print(stats)
# bt.plot()