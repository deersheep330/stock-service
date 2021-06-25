from pprint import pprint
from datetime import datetime, timedelta
import requests
from lxml import etree

from stock.db import create_engine, start_session, insert, delete_older_than
from stock.models import TwseOverBought, TwseOverSold
from stock.utilities import get_db_connection_url


class InstitutionsParser():

    def __init__(self):

        self.connection_url = get_db_connection_url()
        self.engine = create_engine(self.connection_url)
        self.session = start_session(self.engine)

        count = delete_older_than(self.session, TwseOverBought, TwseOverBought.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old TwseOverBought records')
        count = delete_older_than(self.session, TwseOverSold, TwseOverSold.date,
                                  datetime.now().date() - timedelta(days=180))
        print(f'delete {count} old TwseOverSold records')
        self.session.commit()

        self.max_count = 12
        self.url = 'https://www.cnyes.com/twstock/a_institutional7.aspx'
        self.symbol_xpath = "//*[contains(@class, 'fLtBx')]//tbody//tr//td[1]//a"
        self.foreign_xpath = "//*[contains(@class, 'fLtBx')]//tbody//tr//td[3]"
        self.quantity_xpath = "//*[contains(@class, 'fLtBx')]//tbody//tr//td[6]"
        self.dict = {}
        self.date_xpath = "//*[contains(@class, 'tydate')]"
        self.date = None
        self.model = 'twse_over_bought'

    def exclude_condition(self, input):
        if input <= 0:
            return True
        else:
            return False

    def parse(self):
        print(f'==> parse page: {self.url}')
        resp = requests.get(self.url, timeout=60)
        resp.raise_for_status()
        content = resp.text
        tree = etree.HTML(content)

        self.date = datetime.strptime(tree.xpath(self.date_xpath)[0].text.strip(), '%Y-%m-%d')
        print(self.date)
        symbols = tree.xpath(self.symbol_xpath)
        foreigns = tree.xpath(self.foreign_xpath)
        quantities = tree.xpath(self.quantity_xpath)
        self.dict = {}
        for symbol, foreign, quantity in zip(symbols, foreigns, quantities):
            if len(self.dict) >= self.max_count:
                break
            elif self.exclude_condition(int(foreign.text.strip())):
                continue
            else:
                self.dict[symbol.text.strip()] = int(quantity.text.strip())
        pprint(self.dict)
        return self

    def save_to_db(self):

        model = None
        if self.model == 'twse_over_bought':
            model = TwseOverBought
        elif self.model == 'twse_over_sold':
            model = TwseOverSold
        else:
            raise Exception(f'unsupported model type: {self.model}')

        for key, value in self.dict.items():
            try:
                insert(self.session, model, {
                    'symbol': key,
                    'date': self.date,
                    'quantity': value
                })
            except Exception as e:
                print(e)
        self.session.commit()
        self.session.close()
