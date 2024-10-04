class Order():
    def __init__(self, ticker, size, side, idx):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.type = 'market'
        self.idx = idx