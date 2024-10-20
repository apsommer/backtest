import yfinance as yf
from Strategy import Strategy
from Engine import Engine
import backtesting as backtesting

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

# execute backtest
e = Engine()
e.add_data(data)
e.add_strategy(BuySellSwitchStrategy())

# display results in terminal
print("\n")
e.run()
print("\n")

########################################################################################################################
########################################################################################################################
########################################################################################################################

""" Validate BuySellSwitchStrategy by duplicating it using popular backtesting library backtesting.py """

# inherit from Strategy base class
class BacktestingBuySellSwitchStrategy(backtesting.Strategy):
    def init(self):
        pass
    def next(self):
        if self.position.size == 0:
            self.buy(size=1)
        else:
            self.sell(size=1)

# execute backtest
bt = backtesting.Backtest(data, BacktestingBuySellSwitchStrategy, cash=100000)
stats = bt.run()

# display results in terminal
print(stats)
print("\n")
# bt.plot()