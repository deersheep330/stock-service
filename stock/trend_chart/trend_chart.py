from stock.db import query_newer_than, create_engine, start_session, query_symbol_newer_than
from stock.models import TwseClosePrice, UsClosePrice
from stock.utilities import get_db_connection_url, is_tw_stock, how_many_days_ago


class TrendChart():

    def __init__(self, model=None):
        self.model = model
        self.symbols = set()
        self.trends = []
        self.days = 14

        self.engine = create_engine(get_db_connection_url())
        self.session = start_session(self.engine)

        self.__get_symbols__()
        self.__get_prices__()

    def __get_symbols__(self):
        if self.model is None:
            raise RuntimeError('model should be specified')

        _symbols = query_newer_than(self.session, self.model, self.model.date, how_many_days_ago(self.days))
        for symbol in _symbols:
            self.symbols.add(symbol.symbol)

    def __get_prices__(self):
        for symbol in self.symbols:
            prices = [0] * self.days
            print(f'for {symbol}')
            if is_tw_stock(symbol):
                _prices = query_symbol_newer_than(
                    self.session,
                    TwseClosePrice,
                    TwseClosePrice.symbol,
                    symbol,
                    TwseClosePrice.date,
                    how_many_days_ago(self.days))
            else:
                _prices = query_symbol_newer_than(
                    self.session,
                    UsClosePrice,
                    UsClosePrice.symbol,
                    symbol,
                    UsClosePrice.date,
                    how_many_days_ago(self.days))
            print(_prices[0].price)
