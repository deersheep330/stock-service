import json
import os

from stock.db import upsert, start_session, create_engine
from stock.models import StockSymbol
from stock.utilities import get_db_connection_url


class SymbolParser():

    def __init__(self):
        self.dict = None
        self.filename = 'symbols.txt'
        self.connection_url = get_db_connection_url()

    def parse(self):
        raise RuntimeError('should implement parse function')

    def get_dict(self):
        return self.dict

    def dump_to_file(self):

        if self.dict is None or len(self.dict) == 0:
            print('no symbols to dump...')
        else:
            print(f'==> dump symbols to file...')

            filename = os.path.join(os.getcwd(), 'dump', self.filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w+', encoding='utf-8') as f:
                json.dump(self.dict, f, ensure_ascii=False, indent=4)

        return self

    def insert_into_db(self):

        if self.dict is None or len(self.dict) == 0:
            print('no symbols to insert into db...')
        else:
            print(f'==> insert symbols into db...')

            engine = create_engine(self.connection_url)
            session = start_session(engine)
            count = 0

            try:
                for key, value in self.dict.items():
                    _dict = {'symbol': key, 'name': value}
                    rowcount = upsert(session, StockSymbol, _dict)
                    count += rowcount
                print(f'{count} records inserted')
            except Exception as e:
                print(e)
            finally:
                session.commit()
                session.close()

        return self
