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
            )
        )

    def sell(self, ticker, size=1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'sell',
                size = -size,
                idx = self.current_idx
            )
        )

    def buy_limit(self, ticker, limit_price, size = 1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'buy',
                size = size,
                idx = self.current_idx,
                order_type='limit',
                limit_price = limit_price
            )
        )

    def sell_limit(self, ticker, limit_price, size = 1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'sell',
                size = size,
                idx = self.current_idx,
                order_type='limit',
                limit_price = limit_price
            )
        )

    @property
    def position_size(self):
        return sum([trade.size for trade in self.trades])

    # creators will override/implement
    def on_bar(self):
        pass
