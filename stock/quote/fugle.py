from datetime import datetime, timedelta, time
import json
import os
from pprint import pprint
import asyncio
import requests
from pytz import timezone

from stock.db import create_engine, insert, start_session, delete_older_than
from stock.models import FugleOverBought, FugleOverSold
from stock.utilities import get_fugle_api_token, get_db_connection_url


class Fugle():

    def __init__(self, type, symbol):

        # setup db connection
        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)

        session = start_session(self.engine)
        count = delete_older_than(session, FugleOverBought, FugleOverBought.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old FugleOverBought records')
        count = delete_older_than(session, FugleOverSold, FugleOverSold.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old FugleOverSold records')
        session.commit()
        session.close()

        # get api token
        self.token = get_fugle_api_token()

        self.type = type
        self.symbol = symbol
        self.url = f'https://api.fugle.tw/realtime/v0/intraday/quote?symbolId={self.symbol}&apiToken={self.token}'

        # call API every 30 seconds
        self.tick = 30

        self.quotes = []

        self.ask_units = 0
        self.bid_units = 0
        self.diff_units = 0

        self.prev_ask = {
            'price': 0,
            'unit': 0
        }
        self.prev_bid = {
            'price': 0,
            'unit': 0
        }

        self.on_time = time(9, 1)
        self.off_time = time(13, 32)

        self.is_closed = False
        self.date = None

    def is_active(self):
        now = datetime.now(timezone('Asia/Taipei')).time()
        if self.on_time < now < self.off_time:
            return True
        else:
            return False

    async def exec(self):

        while self.is_active() and not self.is_closed:
            self.quote()
            self.diff()
            await asyncio.sleep(self.tick)

        if len(self.quotes) != 0:
            self.date = datetime.strptime(self.quotes[-1]['at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            self.diff_units = int(self.ask_units - self.bid_units)
        print(f'[{self.symbol}] {self.date} quote =====>')
        print(f'market close ? {self.is_closed}')
        print(f'ask = {self.ask_units}, bid = {self.bid_units}')
        print(f'ask - bid = {self.diff_units}')

    def quote(self):
        try:
            resp = requests.get(self.url)
            json = resp.json()
            self.is_closed = json['data']['quote']['isClosed']
            self.quotes.append(json['data']['quote']['order'])
            self.quotes[-1]['trade'] = json['data']['quote']['trade']

            # less than 5 order prices
            for ele in reversed(self.quotes[-1]['bestAsks']):
                if ele['price'] == 0:
                    self.quotes[-1]['bestAsks'].remove(ele)
            for ele in reversed(self.quotes[-1]['bestBids']):
                if ele['price'] == 0:
                    self.quotes[-1]['bestBids'].remove(ele)

            # no transaction
            if len(self.quotes[-1]['bestAsks']) == 0 and len(self.quotes[-1]['bestBids']) == 0:
                pass

            # corrupt data
            if len(self.quotes[-1]['bestAsks']) == 0:
                self.quotes[-1]['bestAsks'].append(self.quotes[-1]['bestBids'][0])
                self.quotes[-1]['bestAsks'][0]['unit'] = 0
            elif len(self.quotes[-1]['bestBids']) == 0:
                self.quotes[-1]['bestBids'].append(self.quotes[-1]['bestAsks'][-1])
                self.quotes[-1]['bestBids'][0]['unit'] = 0

            print(f"{self.symbol} / {self.quotes[-1]['trade']['price']} / {self.quotes[-1]['at']}")
        except Exception as e:
            print(e)

    def diff(self):
        try:
            record = self.quotes[-1]
            # no transaction
            if len(record['bestAsks']) == 0 and len(record['bestBids']) == 0:
                pass
            cur_ask = record['bestAsks'][0]
            cur_bid = record['bestBids'][-1]
            # broken data
            if cur_ask['price'] == 0 or cur_bid['price'] == 0:
                pass
            # initialize
            if self.prev_ask['price'] == 0 and self.prev_bid['price'] == 0 \
                    and self.prev_ask['unit'] == 0 and self.prev_bid['unit'] == 0:
                self.prev_ask['price'] = cur_ask['price']
                self.prev_ask['unit'] = cur_ask['unit']
                self.prev_bid['price'] = cur_bid['price']
                self.prev_bid['unit'] = cur_bid['unit']
            else:
                # ask side
                if cur_ask['price'] == self.prev_ask['price']:
                    if cur_ask['unit'] < self.prev_ask['unit']:
                        self.ask_units += self.prev_ask['unit'] - cur_ask['unit']
                elif cur_ask['price'] > self.prev_ask['price']:
                    self.ask_units += self.prev_ask['unit']

                self.prev_ask['price'] = cur_ask['price']
                self.prev_ask['unit'] = cur_ask['unit']

                # bid side
                if cur_bid['price'] == self.prev_bid['price']:
                    if cur_bid['unit'] < self.prev_bid['unit']:
                        self.bid_units += self.prev_bid['unit'] - cur_bid['unit']
                elif cur_bid['price'] < self.prev_bid['price']:
                    self.bid_units += self.prev_bid['unit']

                self.prev_bid['price'] = cur_bid['price']
                self.prev_bid['unit'] = cur_bid['unit']

            self.diff_units = self.ask_units - self.bid_units
        except Exception as e:
            print(f'diff for symbol {self.symbol} exception: {e}')
            pprint(self.quotes)

    def dump_to_file(self):
        if len(self.quotes) == 0:
            pass
        else:
            print(f'==> dump quotes to file...')
            filename = os.path.join(os.getcwd(), 'dump', f'dump-{self.symbol}.txt')
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w+', encoding='utf-8') as f:
                json.dump(self.quotes, f, ensure_ascii=False, indent=4)

    def save_to_db(self):

        if len(self.quotes) == 0:
            return

        print(f'==> {self.symbol} save to db: {self.date} {self.diff_units}')

        session = start_session(self.engine)
        if self.type == 'overbought':
            insert(session, FugleOverBought, {
                'symbol': self.symbol,
                'date': self.date,
                'quantity': self.diff_units
            })
            session.commit()
        elif self.type == 'oversold':
            insert(session, FugleOverSold, {
                'symbol': self.symbol,
                'date': self.date,
                'quantity': self.diff_units
            })
            session.commit()
        else:
            raise Exception(f'unsupported type: {self.type}')
        session.close()
