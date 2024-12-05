import yfinance as yf
from yfinance.utils import auto_adjust

from Strategy import Strategy
from Engine import Engine, print_stats

class BuySellSwitchLimit(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            limit_price = self.close * 0.995
            self.buy_limit('AAPL', size = 100, limit_price = limit_price)
            # print(self.current_idx, "buy")
        else:
            limit_price = self.close * 1.005
            self.sell_limit('AAPL', size = 100, limit_price = limit_price)
            # print(self.current_idx, "sell")

# todo can not match publication
#  timestamps coming adjusted to EST, makes sense
#  auto_adjust = False affects prices slightly
#  dividends since article?
#  very close, but not identical results
data = (yf.Ticker('AAPL').history(
    start = '2022-12-01',
    end = '2022-12-31',
    interval = '1d',
    auto_adjust = False)) # affects the prices just slightly, can not match publication!

print(data)

# execute backtest
engine = Engine()
engine.add_data(data)
engine.add_strategy(BuySellSwitchLimit())
stats = engine.run()

# display results in terminal
print_stats(stats)
