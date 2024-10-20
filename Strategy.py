from Order import Order

class Strategy():

    def __init__(self):
        self.current_idx = None
        self.data = None
        self.orders = []
        self.trades = []

    def buy(self, ticker, size=1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'buy',
                size = size,
                idx = self.current_idx
            ))

    def sell(self, ticker, size=1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'sell',
                size = -size,
                idx = self.current_idx
            ))

    @property
    def position_size(self):
        return sum([trade.size for trade in self.trades])

    # creators will override/implement
    def on_bar(self):
        pass
