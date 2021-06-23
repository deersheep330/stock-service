from datetime import datetime, timedelta

from stock.db import create_engine, start_session, query_newer_than
from stock.models import PttTrend, ReunionTrend, TwseOverBought, TwseOverSold
from stock.price import UsPriceParser
from stock.price import TwPriceParser
from stock.utilities import get_db_connection_url


def is_tw_stock(_symbol):
    return any(char.isdigit() for char in _symbol)


if __name__ == '__main__':

    print('==> close_price_entry')

    us_price_parser = UsPriceParser()
    tw_price_parser = TwPriceParser()

    engine = create_engine(get_db_connection_url())
    session = start_session(engine)

    symbol_set = set()
    symbols = query_newer_than(session, PttTrend, PttTrend.date, datetime.now().date() - timedelta(days=14))
    for symbol in symbols:
        symbol_set.add(symbol.symbol)
    symbols = query_newer_than(session, ReunionTrend, ReunionTrend.date, datetime.now().date() - timedelta(days=14))
    for symbol in symbols:
        symbol_set.add(symbol.symbol)
    symbols = query_newer_than(session, TwseOverBought, TwseOverBought.date, datetime.now().date() - timedelta(days=3))
    for symbol in symbols:
        symbol_set.add(symbol.symbol)
    symbols = query_newer_than(session, TwseOverSold, TwseOverSold.date, datetime.now().date() - timedelta(days=3))
    for symbol in symbols:
        symbol_set.add(symbol.symbol)

    for symbol in symbol_set:
        if is_tw_stock(symbol):
            try:
                tw_price_parser.parse(symbol).save_close_price_to_db()
                print(f'parse {symbol} close price = {tw_price_parser.price_close}')
            except Exception as e:
                print(e)
        else:
            try:
                us_price_parser.parse(symbol).save_to_db()
                print(f'parse {symbol} close price = {us_price_parser.price}')
            except Exception as e:
                print(e)
