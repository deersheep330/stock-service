from stock.db import create_engine, start_session, insert
from stock.models import ReunionTrend
from stock.utilities import get_db_connection_url
from .reunion_parser import ReunionParser


class ReunionTrends():

    def __init__(self):

        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)
        self.session = start_session(self.engine)

        self.parser = ReunionParser()
        self.parser.parse()

        self.dict = {}
        '''
        n = len(self.parser.list) * 10
        for symbol in self.parser.list:
            self.dict[symbol] = n
            n -= 10
        '''
        total_num = sum(self.parser.num_list)
        for symbol, num in zip(self.parser.list, self.parser.num_list):
            self.dict[symbol] = int(1000 * num / total_num)

    def get_popularities(self):
        return self.dict

    def save_to_db(self):
        for key, value in self.dict.items():
            try:
                insert(self.session, ReunionTrend, {
                    'symbol': key,
                    'popularity': value
                })
            except Exception as e:
                print(e)
        self.session.commit()
        self.session.close()
