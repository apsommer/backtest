import yfinance as yf
from Strategy import Strategy
from Engine import Engine, print_stats
import backtesting as backtesting

class BuySellSwitch(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            self.buy('AAPL', 1)
            # print(self.current_idx, "buy")
        else:
            self.sell('AAPL', 1)
            # print(self.current_idx, "sell")

data = (yf.Ticker('AAPL').history(
    start = '2022-12-01',
    end = '2022-12-31',
    interval = '1d'))

# execute backtest
engine = Engine()
engine.add_data(data)
engine.add_strategy(BuySellSwitch())
stats = engine.run()
print_stats(stats)
# engine.print_trades()

########################################################################################################################
""" Validate strategy by duplicating it with popular backtesting library backtesting.py """

# inherit from Strategy base class
class BacktestingBuySellSwitchStrategy(backtesting.Strategy):
    def init(self):
        pass
    def next(self):
        if self.position.size == 0:
            self.buy(size = 1)
        else:
            self.sell(size = 1)

# execute backtest
bt = (backtesting.Backtest(
    data,
    BacktestingBuySellSwitchStrategy,
    cash = 100000))

# display results in terminal
output = bt.run()
print(output)