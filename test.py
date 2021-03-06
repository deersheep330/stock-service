import requests

from stock.institutions import InstitutionsOverboughtParser, InstitutionsOversoldParser
from stock.price import UsPriceParser, TwPriceParser
from stock.ptt import PttTrends
from stock.quote import Fugle
from stock.reunion import ReunionTrends
from stock.symbols import Sp500Parser, DowJonesParser, NasdaqParser, SoxParser, TWSEParser, NYSEParser
from stock.trend_chart import PttTrendChart, ReunionTrendChart
from stock.utilities import get_db_connection_url
from stock.db import create_engine, create_all_tables_from_orm


if __name__ == '__main__':

    print('==> init database')

    engine = create_engine(get_db_connection_url())
    create_all_tables_from_orm(engine)

    print('[1] symbol test:')

    nyse = NYSEParser().parse().insert_into_db().get_dict()
    sp500 = Sp500Parser().parse().insert_into_db().get_dict()
    dowjones = DowJonesParser().insert_into_db().get_dict()
    nasdaq = NasdaqParser().insert_into_db().parse().get_dict()
    sox = SoxParser().parse().insert_into_db().get_dict()
    twse = TWSEParser().parse().insert_into_db().get_dict()

    print('[2] ptt test:')

    print('ignore')
    #trends = PttTrends()

    print('[3] reunion test:')

    print('ignore')
    #trends = ReunionTrends()

    print('[4] institutions test:')

    overbought_parser = InstitutionsOverboughtParser()
    overbought_parser.parse()
    oversold_parser = InstitutionsOversoldParser()
    oversold_parser.parse()

    print('[5] quote test:')

    fugle = Fugle('overbought', '2330')
    resp = requests.get(fugle.url)
    json = resp.json()
    print(json['data']['quote'])

    print('[6] price test:')

    us_price_parser = UsPriceParser()
    us_price_parser.parse('T')
    tw_price_parser = TwPriceParser()
    tw_price_parser.parse('1220')

    print('[7] trend charts test:')

    ptt_trend_chart = PttTrendChart()
    print(ptt_trend_chart.trends)

    reunion_trend_chart = ReunionTrendChart()
    print(reunion_trend_chart.trends)
