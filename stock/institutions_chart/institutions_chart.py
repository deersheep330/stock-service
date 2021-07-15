from datetime import datetime, timedelta

from stock.db import query_newer_than, create_engine, start_session, query_symbol_newer_than, query_unique, \
    query_date_equal_to, query_symbol_date_equal_to
from stock.models import TwseClosePrice, UsClosePrice, StockSymbol, TwseOverBought, FugleOverBought, TwseOverSold, \
    FugleOverSold
from stock.trend_chart.trend import Trend
from stock.utilities import get_db_connection_url, is_tw_stock, how_many_days_ago


class InstitutionsChart():

    def __init__(self, type='buy'):
        if type == 'buy':
            self.institution_model = TwseOverBought
            self.fugle_model = FugleOverBought
        else:
            self.institution_model = TwseOverSold
            self.fugle_model = FugleOverSold

        self.trends = []

        self.engine = create_engine(get_db_connection_url())
        self.session = start_session(self.engine)

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        day_before_yesterday = yesterday - timedelta(days=1)
        print(yesterday)
        print(day_before_yesterday)

        yesterday_results = query_date_equal_to(self.session,
                                                self.institution_model,
                                                self.institution_model.date,
                                                yesterday)
        day_before_yesterday_results = query_date_equal_to(self.session,
                                                self.institution_model,
                                                self.institution_model.date,
                                                day_before_yesterday)
        print(yesterday_results)
        print(day_before_yesterday_results)

        if len(yesterday_results) == 0 or len(day_before_yesterday_results) == 0:
            self.trends = []
        else:
            for i in range(len(yesterday_results)):
                yesterday_result = yesterday_results[i]
                for j in range(len(day_before_yesterday_results)):
                    day_before_yesterday_result = day_before_yesterday_results[j]
                    if yesterday_result.symbol == day_before_yesterday_result.symbol:
                        stock_symbol = query_unique(self.session, StockSymbol, StockSymbol.symbol, yesterday_result.symbol)
                        fugle_result = query_symbol_date_equal_to(self.session, self.fugle_model, self.fugle_model.symbol, yesterday_result.symbol, self.fugle_model.date, today)
                        print(fugle_result)
                        trend = {}
                        trend[day_before_yesterday_result.date.strftime('%Y-%m-%d')] = day_before_yesterday_result.quantity
                        trend[yesterday_result.date.strftime('%Y-%m-%d')] = yesterday_result.quantity
                        trend[today.strftime('%Y-%m-%d') + ' predict'] = fugle_result.quantity
                        self.trends.append({
                            'symbol': stock_symbol.symbol,
                            'name': stock_symbol.name,
                            'trends': trend
                        })
        print(self.trends)
