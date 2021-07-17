import pickle
import redis

from stock.trend_chart import PttTrendChart, ReunionTrendChart
from stock.utilities import get_redis_host

if __name__ == '__main__':

    # get redis connection
    r = redis.Redis(host=get_redis_host(), port=6379, db=0)

    # generate ptt trend chart and store in redis
    ptt_trend_chart = PttTrendChart()
    ptt_data = pickle.dumps(ptt_trend_chart.trends[:8])
    r.set('ptt', ptt_data)
    print('store ptt trend chart in redis ok:')
    print(pickle.loads(r.get('ptt')))

    # generate reunion trend chart and store in redis
    reunion_trend_chart = ReunionTrendChart()
    reunion_data = pickle.dumps(reunion_trend_chart.trends[:8])
    r.set('reunion', reunion_data)
    print('store reunion trend chart in redis ok:')
    print(pickle.loads(r.get('reunion')))
