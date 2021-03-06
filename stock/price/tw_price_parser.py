import time
from datetime import datetime, timedelta, date
import requests

from stock.db import create_engine, start_session, insert, delete_older_than
from stock.models import TwseOpenPrice, TwseClosePrice
from stock.utilities import get_db_connection_url, get_fugle_api_token


class TwPriceParser():

    def __init__(self):

        # get api token
        self.token = get_fugle_api_token()

        # setup db connection
        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)

        session = start_session(self.engine)
        count = delete_older_than(session, TwseOpenPrice, TwseOpenPrice.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old TwseOpenPrice records')
        count = delete_older_than(session, TwseClosePrice, TwseClosePrice.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old TwseClosePrice records')
        session.commit()
        session.close()

        self.__reset__()

    def __reset__(self):
        self.symbol = None
        self.price_open = None
        self.price_close = None
        self.datetime = None
        self.change = None
        self.percentage = None

    def parse(self, symbol):

        self.__reset__()

        try:
            self.symbol = symbol
            url = f'https://api.fugle.tw/realtime/v0.2/intraday/quote?symbolId={self.symbol}&apiToken={self.token}'

            print(f'==> parse url: {url}')
            resp = requests.get(url)
            json = resp.json()
            self.price_open = float(json['data']['quote']['priceOpen']['price'])
            self.price_close = float(json['data']['quote']['trade']['price'])
            #self.datetime = json['data']['quote']['priceOpen']['at']
            #self.datetime = datetime.strptime(self.datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
            self.datetime = date.today()

            # for close price
            self.change = float(json['data']['quote']['change'])
            self.percentage = "{:4.2f}".format(float(json['data']['quote']['changePercent']) * 100)

            print(f'{self.symbol} {self.price_open} {self.price_close} {self.datetime} {self.change} {self.percentage}')
        except Exception as e:
            print(e)
        finally:
            time.sleep(5)
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

        if self.symbol is None or self.price_close is None or self.datetime is None or self.change is None or self.percentage is None:
            print(f'some data missing! cannot write to db: {self.datetime}|{self.symbol}|{self.price_close}|{self.change}|{self.percentage}')
            return

        session = start_session(self.engine)
        insert(session, TwseClosePrice, {
            'symbol': self.symbol,
            'date': self.datetime,
            'price': self.price_close,
            'change': self.change,
            'percentage': self.percentage
        })
        session.commit()
        session.close()
