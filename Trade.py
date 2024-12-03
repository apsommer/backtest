class Trade():
    def __init__(self, ticker, side, size, price, trade_type, idx):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.type = trade_type
        self.idx = idx
        self.price = price

    # string representation of class, called "dunder" for double under underscores
    def __repr__(self):
        return f'<Trade: {self.idx} {self.ticker} {self.size}@{self.price}>'