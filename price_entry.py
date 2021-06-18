from stock.price import UsPriceParser
from stock.price import TwPriceParser

if __name__ == '__main__':

    # ptt 7 days => close price
    # reunion 7 days => close price

    # twse over bought / sold 1 day => open price

    us_price_parser = UsPriceParser()
    us_price_parser.parse('T').save_to_db()

    tw_price_parser = TwPriceParser()
    tw_price_parser.parse('1220').save_open_price_to_db()
    tw_price_parser.parse('1225').save_close_price_to_db()
