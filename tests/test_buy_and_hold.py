import yfinance as yf
from Strategy import Strategy
from Engine import Engine, print_stats

class BuyAndHoldStrategy(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            limit_price = self.close * 0.995
            self.buy_limit('AAPL', size = 8.319, limit_price = limit_price)
            print(self.current_idx, "buy_limit")

# example data
data = (yf.Ticker('AAPL').history(
    start = '2020-12-01',
    end = '2022-12-31',
    interval = '1d'))

# execute backtest
engine = Engine(initial_cash = 1000)
engine.add_data(data)
engine.add_strategy(BuyAndHoldStrategy())
stats = engine.run()

# display results in terminal
print_stats(stats)
