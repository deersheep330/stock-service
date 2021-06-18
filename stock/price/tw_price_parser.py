import datetime
import requests

from stock.db import create_engine, start_session, insert
from stock.models import TwseOpenPrice, TwseClosePrice
from stock.utilities import get_db_connection_url, get_fugle_api_token


class TwPriceParser():

    def __init__(self):

        # get api token
        self.token = get_fugle_api_token()

        # setup db connection
        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)

        self.__reset__()

    def __reset__(self):
        self.symbol = None
        self.price_open = None
        self.price_close = None
        self.datetime = None

    def parse(self, symbol):

        self.__reset__()

        try:
            self.symbol = symbol
            url = f'https://api.fugle.tw/realtime/v0/intraday/quote?symbolId={self.symbol}&apiToken={self.token}'

            print(f'==> parse url: {url}')
            resp = requests.get(url)
            json = resp.json()
            self.price_open = float(json['data']['quote']['priceOpen']['price'])
            self.price_close = float(json['data']['quote']['trade']['price'])
            self.datetime = json['data']['quote']['priceOpen']['at']
            self.datetime = datetime.datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S.%fZ')

            print(f'{self.symbol} {self.price_open} {self.price_close} {self.datetime}')
        except Exception as e:
            print(e)
        finally:
            return self

    def save_open_price_to_db(self):

        if self.symbol is None or self.price_open is None or self.datetime is None:
            print(f'some data missing! cannot write to db: {self.datetime}|{self.symbol}|{self.price_open}')
            return

        session = start_session(self.engine)
        insert(session, TwseOpenPrice, {
            'symbol': self.symbol,
            'date': self.datetime,
            'price': self.price_open
        })
        session.commit()
        session.close()

    def save_close_price_to_db(self):

        if self.symbol is None or self.price_close is None or self.datetime is None:
            print(f'some data missing! cannot write to db: {self.datetime}|{self.symbol}|{self.price_close}')
            return

        session = start_session(self.engine)
        insert(session, TwseClosePrice, {
            'symbol': self.symbol,
            'date': self.datetime,
            'price': self.price_close
        })
        session.commit()
        session.close()
