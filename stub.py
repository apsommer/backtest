import pandas as pd
from tqdm import tqdm

class Engine():

    # initialize
    def __init__(self, initial_cash=100000):

        # private var
        self.cash = initial_cash
        self.data = None
        self.strategy = None
        self.current_idx = None

    # setters
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
            self._fill_orders()
            # self.strategy.on_bar()
            print(idx)

    def _fill_orders(self):
        pass

class Strategy():
    def __init__(self):
        pass

class Trade():
     def __init__(self):
        pass

class Order():
    def __init__(self):
        pass