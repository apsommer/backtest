import pandas as pd
from tqdm import tqdm
from Trade import Trade

class Engine():

    def __init__(self, initial_cash=100000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.data = None
        self.strategy = None
        self.current_idx = None
        self.cash_series = { }
        self.stock_series = { }

    def add_data(self, data: pd.DataFrame):
        self.data = data

    def add_strategy(self, strategy):
        self.strategy = strategy

    def run(self):

        # pass data to strategy
        self.strategy.data = self.data

        # tqdm is command line progress bar
        for idx in tqdm(self.data.index):
            self.current_idx = idx
            self.strategy.current_idx = self.current_idx
            self.strategy.on_bar()
            self._fill_orders()

            # track cash and stock holdings
            self.cash_series[idx] = self.cash
            self.stock_series[idx] = self.strategy.position_size * self.data.loc[self.current_idx]['Close']

    def _fill_orders(self):

        for order in self.strategy.orders:

            # todo temp
            #  set fill_price to open
            fill_price = self.data.loc[self.current_idx]['Open']

            can_fill = False

            # long: ensure enough cash exists to purchase qty
            if order.side == 'buy' and self.cash >= self.data.loc[self.current_idx]['Open'] * order.size:

                # limit buy filled if limit_price >= low
                if order.type == 'limit':

                    if order.limit_price >= self.data.loc[self.current_idx]['Low']:
                        fill_price = order.limit_price
                        can_fill = True
                        print(self.current_idx, 'Buy Filled. ', "limit",order.limit_price," / low", self.data.loc[self.current_idx]['Low'])

                    else:
                        print(self.current_idx,'Buy NOT filled. ', "limit",order.limit_price," / low", self.data.loc[self.current_idx]['Low'])

                # market, always fills
                else:
                    can_fill = True

            # flatten (short): ensure position size is larger than qty sell
            elif order.side == 'sell' and self.strategy.position_size >= order.size:

                # limit sell filled if limit_price <= high
                if order.type == 'limit':

                    if order.limit_price <= self.data.loc[self.current_idx]['High']:
                        fill_price = order.limit_price
                        can_fill = True
                        print(self.current_idx, 'Sell filled. ', "limit", order.limit_price, " / high", self.data.loc[self.current_idx]['High'])

                    else:
                        print(self.current_idx, 'Sell NOT filled. ', "limit", order.limit_price, " / high", self.data.loc[self.current_idx]['High'])

                # market, always fills
                else:
                    can_fill = True

            if can_fill:
                trade = Trade(
                    ticker = order.ticker,
                    side = order.side,
                    price = self.data.loc[self.current_idx]['Open'],
                    size = order.size,
                    type = order.type,
                    idx = self.current_idx)

                self.strategy.trades.append(trade)
                self.cash -= trade.price * trade.size
                # print(trade)

        # clearing orders here assumes all limits orders are valid DAY, not GTC
        self.strategy.orders = []

    def get_stats(self):

        metrics = { }

        # calculate total percent return
        total_return = 100 * ((self.data.loc[self.current_idx]['Close']
            * self.strategy.position_size + self.cash) / self.initial_cash - 1)

        metrics['total_return'] = total_return
        return metrics