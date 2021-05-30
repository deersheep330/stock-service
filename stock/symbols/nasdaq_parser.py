from .sp500_parser import Sp500Parser

class NasdaqParser(Sp500Parser):

    def __init__(self):
        super(NasdaqParser, self).__init__()
        self.url = 'https://www.cnyes.com/usastock/hotprice.aspx?page=hot&kind=nasdaq100'
        self.filename = 'nasdaq.txt'
