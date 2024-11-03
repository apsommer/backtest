import yfinance as yf
from Strategy import Strategy
from Engine import Engine, print_stats

class BuyAndSellSwitchStrategy(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            limit_price = self.close * 0.995
            self.buy_limit('AAPL', size = 100, limit_price = limit_price)
            print(self.current_idx, "buy")
        else:
            limit_price = self.close * 1.005
            self.sell_limit('AAPL', size = 100, limit_price = limit_price)
            print(self.current_idx, "sell")

data = (yf.Ticker('AAPL').history(
    start = '2022-12-01',
    end = '2022-12-31',
    interval = '1d'))

# execute backtest
engine = Engine()
engine.add_data(data)
engine.add_strategy(BuyAndSellSwitchStrategy())
engine.run()

# display results in terminal
stats = engine.get_stats()
print_stats(stats)
