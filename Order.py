class Order():
    def __init__(self, ticker, size, side, idx, order_type = 'market', limit_price = None):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.idx = idx
        self.type = order_type
        self.limit_price = limit_price