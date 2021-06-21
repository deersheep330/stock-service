from datetime import datetime, timedelta

from stock.db import create_engine, start_session, query_newer_than
from stock.models import TwseOverBought, TwseOverSold
from stock.price import TwPriceParser
from stock.utilities import get_db_connection_url


if __name__ == '__main__':

    print('==> open_price_entry')

    tw_price_parser = TwPriceParser()

    engine = create_engine(get_db_connection_url())
    session = start_session(engine)

    symbol_set = set()
    symbols = query_newer_than(session, TwseOverBought, TwseOverBought.date, datetime.now().date() - timedelta(days=3))
    for symbol in symbols:
        symbol_set.add(symbol.symbol)
    symbols = query_newer_than(session, TwseOverSold, TwseOverSold.date, datetime.now().date() - timedelta(days=3))
    for symbol in symbols:
        symbol_set.add(symbol.symbol)

    for symbol in symbol_set:
        try:
            tw_price_parser.parse(symbol).save_open_price_to_db()
            print(f'parse {symbol} open price = {tw_price_parser.price_open}')
        except Exception as e:
            print(e)
