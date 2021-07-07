from datetime import datetime, timedelta

from stock.db import query_newer_than, create_engine, start_session, query_symbol_newer_than, query_unique
from stock.models import TwseClosePrice, UsClosePrice, StockSymbol
from stock.trend_chart.trend import Trend
from stock.utilities import get_db_connection_url, is_tw_stock, how_many_days_ago


class TrendChart():

    def __init__(self, model=None):
        self.model = model
        self.symbols = set()
        self.popularities = []
        self.trends = []
        self.days = 14
        self.today = how_many_days_ago(1)
        self.dates = [(self.today - timedelta(i)).strftime("%Y/%m/%d") for i in reversed(range(self.days))]
        print(self.dates)

        self.engine = create_engine(get_db_connection_url())
        self.session = start_session(self.engine)

        self.__get_symbols__()
        for symbol in self.symbols:
            _popularity = self.__get_popularity__(symbol.symbol)
            _price = self.__get_price__(symbol.symbol)
            _total_popularity = sum(_popularity)
            self.trends.append(Trend(symbol.symbol, symbol.name, self.dates, _popularity, _price, _total_popularity))

        self.trends.sort(key=lambda trend: trend.total_popularity, reverse=True)

    def __get_symbols__(self):
        if self.model is None:
            raise RuntimeError('model should be specified')

        _symbols = query_newer_than(self.session, self.model, self.model.date, how_many_days_ago(self.days))
        for symbol in _symbols:
            stock_symbol = query_unique(self.session, StockSymbol, StockSymbol.symbol, symbol.symbol)
            self.symbols.add(stock_symbol)

    def __get_popularity__(self, symbol):

        popularities = [0] * self.days

        print(f'==> get popularity for {symbol}')

        _popularities = query_symbol_newer_than(
            self.session,
            self.model,
            self.model.symbol,
            symbol,
            self.model.date,
            how_many_days_ago(self.days))

        for popularity in _popularities:
            day_diff = (self.today - popularity.date).days
            popularities[self.days - 1 - day_diff] = popularity.popularity

        return popularities

    def __get_price__(self, symbol):

        prices = [0] * self.days

        print(f'==> get price for {symbol}')

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

        for price in _prices:
            try:
                day_diff = (self.today - price.date).days
                prices[self.days - 1 - day_diff] = price.price
            except Exception as e:
                print('==> __get_price__ error!')
                print(e)
                print(self.today, price.date, (self.today - price.date).days)

        return prices
