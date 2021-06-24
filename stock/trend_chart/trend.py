

class Trend():

    def __init__(self, symbol, dates, popularities, prices, total_popularity):
        self.symbol = symbol
        self.dates = dates
        self.popularities = popularities
        self.prices = prices
        self.total_popularity = total_popularity
        print(f'==> new trend created for {symbol}')
        print(self.dates)
        print(self.popularities)
        print(self.prices)
        print(f'total popularity = {self.total_popularity}')
