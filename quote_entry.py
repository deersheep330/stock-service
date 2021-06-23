import asyncio
from datetime import timedelta, datetime

from stock.db import create_engine, start_session, query_date_equal_to, query_unique
from stock.models import TwseOverBought, TwseOverSold, StockSymbol
from stock.quote import Fugle
from stock.utilities import get_db_connection_url

if __name__ == '__main__':

    print('==> quote_entry')

    # setup db connection
    connection_url = get_db_connection_url()
    engine = create_engine(connection_url)
    session = start_session(engine)

    over_boughts = []
    over_solds = []
    _datetime = datetime.now().date()
    retry = 0
    max_retry = 7

    while len(over_boughts) == 0 or len(over_solds) == 0:
        print(f'try to get date for datetime = {_datetime}')
        over_boughts = query_date_equal_to(session, TwseOverBought, TwseOverBought.date, _datetime)
        over_solds = query_date_equal_to(session, TwseOverSold, TwseOverSold.date, _datetime)
        _datetime -= timedelta(days=1)
        retry += 1
        if retry > max_retry:
            break

    if len(over_boughts) == 0 or len(over_solds) == 0:
        raise Exception('Cannot get TWSE oversold/overbought records')
    else:
        print(f'over_boughts: {[item.symbol for item in over_boughts]}')
        print(f'over_solds: {[item.symbol for item in over_solds]}')

    symbols = []
    tasks = []
    for ele in over_boughts:
        symbols.append(Fugle('overbought', ele.symbol))
        tasks.append(symbols[-1].exec())

    for ele in over_solds:
        symbols.append(Fugle('oversold', ele.symbol))
        tasks.append(symbols[-1].exec())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    # if idle for a long time, db connection could be closed,
    # read a dummy value to reactivate the connection
    try:
        print(f'==> test read before write')
        res = query_unique(session, StockSymbol, StockSymbol.symbol, 'AAPL')
        print(f'==> get symbol {res}')
    except Exception as e:
        print(e)

    # read again to test if connection resumed or not
    try:
        print(f'==> try again test read before write')
        res = query_unique(session, StockSymbol, StockSymbol.symbol, 'AAPL')
        print(f'==> get symbol {res}')
    except Exception as e:
        print(e)

    for symbol in symbols:
        symbol.dump_to_file()
        symbol.save_to_db()
