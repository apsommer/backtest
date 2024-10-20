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
engine = Engine()
engine.add_data(data)
engine.add_strategy(BuySellSwitchStrategy())
engine.run()

# display results in terminal
stats = engine.get_stats()
print(stats)
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

# display results in terminal
stats = bt.run()
print(stats)
# bt.plot()