

class Trend():

    def __init__(self, symbol, name, dates, popularities, prices, total_popularity):
        self.symbol = symbol
        self.name = name
        self.dates = dates
        self.popularities = popularities
        self.prices = prices
        self.total_popularity = total_popularity
        print(f'==> new trend created for {symbol} {name}')
        print(self.dates)
        print(self.popularities)
        print(self.prices)
        print(f'total popularity = {self.total_popularity}')

    def __repr__(self):
        return repr((self.symbol, self.name, self.total_popularity))
