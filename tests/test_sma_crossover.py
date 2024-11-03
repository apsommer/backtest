import yfinance as yf
from Engine import Engine, print_stats
from Strategy import Strategy

class SMACrossover(Strategy):

    def on_bar(self):

        # if flat, ...
        if self.position_size == 0:

            # buy, limit
            if self.data.loc[self.current_idx].sma_12 > self.data.loc[self.current_idx].sma_24:

                limit_price = self.close * 0.995

                # buy as many as possible
                order_size = self.cash / limit_price
                self.buy_limit('AAPL', size = order_size, limit_price = limit_price)

            # sell, limit
            elif self.data.loc[self.current_idx].sma_12 < self.data.loc[self.current_idx].sma_24:

                # sell to cover open long, never short
                limit_price = self.close * 1.005
                self.sell_limit('AAPL', size = self.position_size, limit_price = limit_price)

# example data
data = (yf.Ticker('AAPL').history(
    start = '2010-12-01',
    end = '2022-12-31',
    interval = '1d'))

# add few more data rows
data['sma_12'] = data.Close.rolling(12).mean()
data['sma_24'] = data.Close.rolling(24).mean()

# execute backtest
engine = Engine(initial_cash = 1000)
engine.add_data(data)
engine.add_strategy(SMACrossover())
stats = engine.run()

# display results in terminal
print_stats(stats)
