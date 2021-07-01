from datetime import datetime, timedelta

from dateutil import parser, tz
import requests
from lxml import etree

from stock.db import insert, start_session, create_engine, delete_older_than
from stock.models import UsClosePrice
from stock.utilities import get_db_connection_url


class UsPriceParser():

    def __init__(self):
        # setup db connection
        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)

        session = start_session(self.engine)
        count = delete_older_than(session, UsClosePrice, UsClosePrice.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old UsClosePrice records')
        session.commit()
        session.close()

        self.__reset__()

    def __reset__(self):
        self.symbol = None
        self.price = None
        self.datetime = None

    def parse(self, symbol):

        self.__reset__()

        try:
            self.symbol = symbol
            url = f'https://www.marketwatch.com/investing/stock/{self.symbol}'

            print(f'==> parse url: {url}')
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            content = resp.text
            tree = etree.HTML(content)

            dates = tree.xpath("//*[contains(@field, 'date')]")
            prices = tree.xpath("//*[contains(@field, 'Last')]")

            if len(dates) == 0 or len(prices) == 0:
                raise Exception(f'cannot get date or price for {self.symbol}')

            self.datetime = parser.parse(dates[0].text)
            self.datetime = self.datetime.replace(tzinfo=tz.gettz('America/New_York'))
            self.datetime = self.datetime.astimezone(tz.gettz('Asia/Taipei'))

            self.price = float(prices[0].text.replace('$', ''))

            print(f'{self.symbol} {self.price} {self.datetime}')
        except Exception as e:
            print(e)
        finally:
            return self

    def save_to_db(self):

        if self.symbol is None or self.price is None or self.datetime is None:
            print(f'some data missing! cannot write to db: {self.datetime}|{self.symbol}|{self.price}')
            return

        session = start_session(self.engine)
        insert(session, UsClosePrice, {
            'symbol': self.symbol,
            'date': self.datetime,
            'price': self.price
        })
        session.commit()
        session.close()
