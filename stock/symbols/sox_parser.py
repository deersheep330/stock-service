from .sp500_parser import Sp500Parser

class SoxParser(Sp500Parser):

    def __init__(self):
        super(SoxParser, self).__init__()
        self.url = 'https://www.cnyes.com/usastock/sector_content.aspx?kind=SOX'
        self.symbol_xpath = "//table[contains(@id, 'stock')]//tr//td[1]/a"
        self.name_xpath = "//table[contains(@id, 'stock')]//tr/td[2]"
        self.filename = 'sox.txt'
