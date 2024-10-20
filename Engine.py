import pandas as pd
from tqdm import tqdm

from Trade import Trade


class Engine():

    def __init__(self, initial_cash=100000):

        # private var
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.data = None
        self.strategy = None
        self.current_idx = None

    def add_data(self, data: pd.DataFrame):
        self.data = data

    def add_strategy(self, strategy):
        self.strategy = strategy

    def run(self):
        self.strategy.data = self.data

        # tqdm is command line progress bar
        for idx in tqdm(self.data.index):
            self.current_idx = idx
            self.strategy.current_idx = self.current_idx
            self.fill_orders()
            self.strategy.on_bar()

    def _fill_orders(self):

        for order in self.strategy.orders:

            can_fill = False

            # long: ensure enough cash exists to purchase qty
            if order.side == 'buy' and self.cash >= self.data.loc[self.current_idx]['Open'] * order.size:
                can_fill = True

            # flatten (short): ensure position size is larger than qty sell
            elif order.side == 'sell' and self.strategy.position_size >= order.size:
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
                print(trade)

        # clear orders since they are processed
        self.strategy.orders = []

    def _get_stats(self):

        metrics = { }

        # calculate total percent return
        total_return = 100 * ((self.data.loc[self.current_idx]['Close']
            * self.strategy.position_size + self.cash) / self.initial_cash - 1)

        metrics['total_return'] = total_return

        return metrics