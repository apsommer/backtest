class Trade():
    def __init__(self, ticker, side, size, price, type, idx):
        self.ticker = ticker
        self.side = side
        self.price = price
        self.size = size
        self.type = type
        self.idx = idx

    # string representation of class, called "dunder" for double under underscores
    def __repr__(self):
        return f'<Trade: {self.idx} {self.ticker} {self.size}@{self.price}>'