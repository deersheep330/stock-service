from .symbol_parser import SymbolParser
from twstock import twse, tpex, __update_codes as update_codes
from ..utilities import remove_non_han_from_corp_name

class TWSEParser(SymbolParser):

    def __init__(self):
        self.filename = 'twse.txt'
        super(TWSEParser, self).__init__()
        update_codes()

    def __contains_special_words_in_symbol(self, symbol):
        specials = ['A', 'B', 'C', 'D', 'E', 'F', 'X']
        for special in specials:
            if special in symbol:
                return True
        return False

    def __contains_special_words_in_name(self, name):
        specials = ['售', '購', '牛', '熊']
        for special in specials:
            if special in name:
                return True
        return False

    def parse(self):
        self.dict = {}
        temp = {}
        temp.update(twse)
        temp.update(tpex)
        for item in temp.items():

            if self.__contains_special_words_in_symbol(item[1].code) or self.__contains_special_words_in_name(item[1].name):
                continue

            name = remove_non_han_from_corp_name(item[1].name)
            if len(name) == 0:
                continue
            else:
                self.dict[item[1].code] = name

        print(f'==> get {len(self.dict)} symbols')

        return self
