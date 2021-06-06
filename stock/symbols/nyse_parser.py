from .symbol_parser import SymbolParser
import requests
from ..utilities import remove_common_words_from_corp_name


class NYSEParser(SymbolParser):

    def __init__(self):
        self.url = 'https://www.nyse.com/api/quotes/filter'
        self.payload = {
            "instrumentType": "EQUITY",
            "pageNumber": 1,
            "sortColumn": "NORMALIZED_TICKER",
            "sortOrder": "ASC",
            "maxResultsPerPage": 8000,
            "filterToken": ""
        }
        self.filename = 'nyse.txt'
        super(NYSEParser, self).__init__()

    def parse(self):
        print(f'==> request page: {self.url}')
        resp = requests.post(self.url, json=self.payload)
        resp_json = resp.json()

        self.dict = {}
        for entry in resp_json:
            _symbol = entry['normalizedTicker']
            _name = remove_common_words_from_corp_name(entry['instrumentName'])
            if len(_name) > 64:
                _name = _name[:64]
            self.dict[_symbol] = _name

        print(f'==> get {len(self.dict)} symbols')

        return self
