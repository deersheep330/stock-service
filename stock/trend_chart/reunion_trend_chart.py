from stock.models import ReunionTrend
from .trend_chart import TrendChart


class ReunionTrendChart(TrendChart):

    def __init__(self):
        super().__init__(ReunionTrend)
