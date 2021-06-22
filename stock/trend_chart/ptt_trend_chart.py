from stock.models import PttTrend
from .trend_chart import TrendChart


class PttTrendChart(TrendChart):

    def __init__(self):
        super().__init__(PttTrend)
