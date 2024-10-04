class Trade():
    def __init__(self, ticker, side, size, price, type, idx):
        self.ticker = ticker
        self.side = side
        self.price = price
        self.size = size
        self.type = type
        self.idx = idx