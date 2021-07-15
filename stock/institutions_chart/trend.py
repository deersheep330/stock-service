

class Trend():

    def __init__(self, symbol, name, dates, quantities, prices, total_quantities):
        self.symbol = symbol
        self.name = name
        self.dates = dates
        self.quantities = quantities
        self.prices = prices
        self.total_quantities = total_quantities
        print(f'==> new trend created for {symbol} {name}')
        print(self.dates)
        print(self.quantities)
        print(self.prices)
        print(f'total quantities = {self.total_quantities}')

    def __repr__(self):
        return repr((self.symbol, self.name, self.total_quantities))
