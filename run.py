import yfinance as yf
from Strategy import Strategy
from Engine import Engine
from print_dict import print_dict
import backtesting as backtesting

# example data
data = (yf.Ticker('AAPL').history(
    start='2022-12-01',
    end='2022-12-31',
    interval='1d'))

# inherit from Strategy base class
class BuySellSwitchStrategy(Strategy):

    # override/implement on_bar
    def on_bar(self):

        if self.position_size == 0:
            limit_price = self.close * 0.995
            self.buy_limit('AAPL', size = 100, limit_price = limit_price)
            print(self.current_idx, "buy_limit")
        else:
            limit_price = self.close * 1.005
            self.sell_limit('AAPL', size = 100, limit_price = limit_price)
            print(self.current_idx, "sell_limit")

# execute backtest
engine = Engine()
engine.add_data(data)
engine.add_strategy(BuySellSwitchStrategy())
engine.run()

# display results in terminal
stats = engine.get_stats()
print("\n")
print_dict(stats)
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