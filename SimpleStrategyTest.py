from Strategy import Strategy

# inherit from Strategy base class
class SimpleStrategyTest(Strategy):

    # override/implement on_bar
    def on_bar(self):

        if self.position_size == 0:
            self.buy('AAPL', 1)
        else:
            self.sell('AAPL', 1)
