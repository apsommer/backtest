from gc import get_stats

import numpy as np
import pandas as pd
from tqdm import tqdm
from Trade import Trade

class Engine:

    def __init__(self, initial_cash=100000):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.data = None
        self.strategy = None
        self.current_idx = None
        self.trading_days = 252 # working days per year
        self.risk_free_rate = 0 # for sharpe ratio calculation
        self.cash_series = { }
        self.stock_series = { }

    def add_data(self, data: pd.DataFrame):
        self.data = data

    def add_strategy(self, strategy):
        self.strategy = strategy

    def run(self):

        # pass data to strategy
        self.strategy.data = self.data
        # self.strategy.cash = self.cash

        # tqdm is command line progress bar
        for idx in tqdm(self.data.index):
            self.current_idx = idx
            self.strategy.current_idx = self.current_idx
            self.strategy.on_bar()
            self._fill_orders()

            # track cash and stock holdings
            self.cash_series[idx] = self.cash
            self.stock_series[idx] = self.strategy.position_size * self.data.loc[self.current_idx]['Close']

        return get_stats()

    def _fill_orders(self):

        for order in self.strategy.orders:

            # todo set fill_price to open
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
                # self.strategy.cash = self.cash

        # clearing orders here assumes all limits orders are valid DAY, not GTC
        self.strategy.orders = []

    def get_stats(self):

        portfolio = pd.DataFrame({
            'stock': self.stock_series,
            'cash': self.cash_series})

        # benchmark reference: buy and hold max allowed shares from start to end
        portfolio_ref = (
                (self.initial_cash / self.data.loc[self.data.index[0]]['Open'])
                * self.data.Close)

        metrics = { }

        # percent return
        metrics['total_return'] = (
                ((self.data.loc[self.current_idx]['Close']
                * self.strategy.position_size + self.cash) / self.initial_cash - 1) * 100)

        # assets under management
        portfolio['total_aum'] = (
                portfolio['stock']
                + portfolio['cash'])

        # average exposure: percent of stock relative to total aum
        metrics['exposure_pct'] = (
            ((portfolio['stock'] / portfolio['total_aum'])
            * 100).mean())

        # annualized returns: ((1 + r_1) * (1 + r_2) * ... * (1 + r_n)) ^ (1/n) - 1
        aum = portfolio.total_aum
        metrics['returns_annualized'] = (
                ((aum.iloc[-1] / aum.iloc[0])
                ** (1 / ((aum.index[-1] - aum.index[0]).days / 365)) - 1)
                * 100)

        ref = portfolio_ref
        metrics['returns_annualized_ref'] = (
                ((ref.iloc[-1] / ref.iloc[0])
                ** (1 / ((ref.index[-1] - ref.index[0]).days / 365)) - 1)
                * 100)

        # annualized volatility: std_dev * sqrt(periods/year)
        metrics['volatility_ann'] = (
                aum.pct_change().std() * np.sqrt(self.trading_days) * 100)
        metrics['volatility_ann_ref'] = (
                ref.pct_change().std() * np.sqrt(self.trading_days) * 100)

        # sharpe ratio: (rate - risk_free_rate) / volatility
        metrics['sharpe_ratio'] = (
                (metrics['returns_annualized']
                 - self.risk_free_rate) / metrics['volatility_ann'])
        metrics['sharpe_ratio_ref'] = (
                (metrics['returns_annualized_ref']
                 - self.risk_free_rate) / metrics['volatility_ann_ref'])

        # max drawdown, percent
        metrics['max_drawdown'] = get_max_drawdown(portfolio.total_aum)
        metrics['max_drawdown_ref'] = get_max_drawdown(portfolio_ref)

        return metrics

def get_max_drawdown(close):
    roll_max = close.cummax()
    daily_drawdown = close / roll_max - 1.0
    max_daily_drawdown = daily_drawdown.cummin()
    return max_daily_drawdown.min() * 100

def print_stats(metrics):
    print("")
    print("Performance:")
    print("")
    for stat, value in metrics.items():
        print("{}: {}".format(stat, round(value, 5)))
    print("")