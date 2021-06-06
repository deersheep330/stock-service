from stock.db import create_engine, create_all_tables_from_orm
from stock.symbols import Sp500Parser, DowJonesParser, NasdaqParser, SoxParser, TWSEParser, NYSEParser
from pprint import pprint

from stock.utilities import get_db_connection_url

if __name__ == '__main__':

    print('==> init database')

    engine = create_engine(get_db_connection_url())
    create_all_tables_from_orm(engine)

    print('==> parsing symbols start')

    nyse = NYSEParser().parse().dump_to_file().insert_into_db().get_dict()

    #pprint(nyse)

    sp500 = Sp500Parser().parse().dump_to_file().insert_into_db().get_dict()

    #pprint(sp500)

    dowjones = DowJonesParser().dump_to_file().parse().insert_into_db().get_dict()

    #pprint(dowjones)

    nasdaq = NasdaqParser().parse().dump_to_file().insert_into_db().get_dict()

    #pprint(nasdaq)

    sox = SoxParser().parse().dump_to_file().insert_into_db().get_dict()

    #pprint(sox)

    twse = TWSEParser().parse().dump_to_file().insert_into_db().get_dict()

    #pprint(twse)

    print('==> update done')