from .sp500_parser import Sp500Parser

class DowJonesParser(Sp500Parser):

    def __init__(self):
        super(DowJonesParser, self).__init__()
        self.url = 'https://www.cnyes.com/usastock/hotprice.aspx?page=hot&kind=idnu'
        self.filename = 'dowjones.txt'
